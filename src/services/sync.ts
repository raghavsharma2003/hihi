import { File } from 'expo-file-system';

import { getDb, getSetting, notifyDbChanged, setSetting } from '@/db/client';
import {
  actionItemsForSync,
  hardDeleteSynced,
  notesNeedingPush,
  replaceActionItems,
  setSyncState,
} from '@/db/notes';
import type { ActionItem, Note } from '@/db/types';
import { currentUserId, supabase } from './supabase';

const BUCKET = 'recordings';
const PULL_CURSOR_KEY = 'sync.pullCursor';

/** Shape of a row in the `notes` table. Mirrors supabase/migrations. */
interface RemoteNote {
  id: string;
  user_id: string;
  created_at: string;
  updated_at: string;
  title: string;
  summary: string;
  transcript: string;
  transcript_edited: boolean;
  audio_path: string | null;
  duration_ms: number;
  amplitudes: number[];
  language: string;
  pinned: boolean;
  archived: boolean;
  tags: string[];
  action_items: ActionItem[];
  deleted_at: string | null;
}

function toRemote(
  note: Note,
  userId: string,
  deletedAt: number | null,
  actionItems: ActionItem[],
): RemoteNote {
  return {
    id: note.id,
    user_id: userId,
    created_at: new Date(note.createdAt).toISOString(),
    updated_at: new Date(note.updatedAt).toISOString(),
    title: note.title,
    summary: note.summary,
    transcript: note.transcript,
    transcript_edited: note.transcriptEdited,
    audio_path: note.audioRemotePath,
    duration_ms: note.durationMs,
    amplitudes: note.amplitudes,
    language: note.language,
    pinned: note.pinned,
    archived: note.archived,
    tags: note.tags,
    action_items: actionItems,
    deleted_at: deletedAt ? new Date(deletedAt).toISOString() : null,
  };
}

/**
 * Uploads a note's recording once. Returns the storage path, or null if there
 * is nothing to upload — a failed upload is not fatal: the note row still syncs
 * and the audio is retried on the next cycle.
 */
async function uploadAudio(note: Note, userId: string): Promise<string | null> {
  if (!supabase || !note.audioUri || note.audioRemotePath) return note.audioRemotePath;

  try {
    const file = new File(note.audioUri);
    if (!file.exists) return null;

    const extension = note.audioUri.split('.').pop() ?? 'wav';
    const path = `${userId}/${note.id}.${extension}`;
    const bytes = await file.bytes();

    const { error } = await supabase.storage.from(BUCKET).upload(path, bytes, {
      contentType: extension === 'wav' ? 'audio/wav' : 'audio/mp4',
      upsert: true,
    });
    if (error) throw error;

    return path;
  } catch (err) {
    console.warn('[echo] audio upload failed', err);
    return null;
  }
}

async function push(userId: string): Promise<void> {
  if (!supabase) return;

  const db = await getDb();
  const pending = await notesNeedingPush(20);

  for (const note of pending) {
    // `notesNeedingPush` selects live and soft-deleted rows alike, so read the
    // tombstone directly rather than inferring it.
    const row = await db.getFirstAsync<{ deleted_at: number | null }>(
      'SELECT deleted_at FROM notes WHERE id = ?;',
      note.id,
    );
    const deletedAt = row?.deleted_at ?? null;

    try {
      const audioPath = deletedAt ? note.audioRemotePath : await uploadAudio(note, userId);
      const actionItems = deletedAt ? [] : await actionItemsForSync(note.id);

      const { error } = await supabase
        .from('notes')
        .upsert(
          toRemote({ ...note, audioRemotePath: audioPath }, userId, deletedAt, actionItems),
        );
      if (error) throw error;

      await setSyncState(note.id, 'synced', { remoteId: note.id, audioRemotePath: audioPath });
    } catch (err) {
      console.warn('[echo] note push failed', note.id, err);
      await setSyncState(note.id, 'failed');
    }
  }

  // Tombstones that made it to the server can leave the device.
  await hardDeleteSynced();
}

async function pull(userId: string): Promise<void> {
  if (!supabase) return;

  const cursor = (await getSetting(PULL_CURSOR_KEY)) ?? '1970-01-01T00:00:00.000Z';

  const { data, error } = await supabase
    .from('notes')
    .select('*')
    .eq('user_id', userId)
    .gt('updated_at', cursor)
    .order('updated_at', { ascending: true })
    .limit(200);

  if (error) {
    console.warn('[echo] pull failed', error);
    return;
  }
  if (!data || data.length === 0) return;

  const db = await getDb();
  let newest = cursor;

  for (const remote of data as RemoteNote[]) {
    const remoteUpdated = new Date(remote.updated_at).getTime();
    if (remote.updated_at > newest) newest = remote.updated_at;

    const local = await db.getFirstAsync<{ updated_at: number; sync_status: string }>(
      'SELECT updated_at, sync_status FROM notes WHERE id = ?;',
      remote.id,
    );

    // An unpushed local edit is the user's most recent intent — never let a
    // stale server row overwrite it. It will win on the next push instead.
    if (local && (local.sync_status === 'dirty' || local.updated_at > remoteUpdated)) continue;

    if (remote.deleted_at) {
      await db.runAsync('DELETE FROM notes WHERE id = ?;', remote.id);
      continue;
    }

    await db.runAsync(
      `INSERT INTO notes (
         id, created_at, updated_at, title, summary, transcript, transcript_edited,
         audio_uri, audio_remote_path, duration_ms, amplitudes, language,
         pinned, archived, enrich_status, sync_status, remote_id, tags, deleted_at
       ) VALUES (?, ?, ?, ?, ?, ?, ?, NULL, ?, ?, ?, ?, ?, ?, 'done', 'synced', ?, ?, NULL)
       ON CONFLICT(id) DO UPDATE SET
         updated_at        = excluded.updated_at,
         title             = excluded.title,
         summary           = excluded.summary,
         transcript        = excluded.transcript,
         transcript_edited = excluded.transcript_edited,
         audio_remote_path = excluded.audio_remote_path,
         duration_ms       = excluded.duration_ms,
         amplitudes        = excluded.amplitudes,
         language          = excluded.language,
         pinned            = excluded.pinned,
         archived          = excluded.archived,
         tags              = excluded.tags,
         sync_status       = 'synced';`,
      remote.id,
      new Date(remote.created_at).getTime(),
      remoteUpdated,
      remote.title,
      remote.summary,
      remote.transcript,
      remote.transcript_edited ? 1 : 0,
      remote.audio_path,
      remote.duration_ms,
      JSON.stringify(remote.amplitudes ?? []),
      remote.language,
      remote.pinned ? 1 : 0,
      remote.archived ? 1 : 0,
      remote.id,
      JSON.stringify(remote.tags ?? []),
    );

    if (Array.isArray(remote.action_items)) {
      await replaceActionItems(remote.id, remote.action_items);
    }
  }

  await setSetting(PULL_CURSOR_KEY, newest);
  notifyDbChanged();
}

/**
 * One push-then-pull pass. Silently does nothing when there is no backend or
 * nobody is signed in, which is the normal state for a local-only user.
 */
export async function runSyncCycle(): Promise<void> {
  if (!supabase) return;

  const userId = await currentUserId();
  if (!userId) return;

  await push(userId);
  await pull(userId);
}

/** Signed URL for a recording that lives only in the cloud. */
export async function remoteAudioUrl(path: string | null): Promise<string | null> {
  if (!supabase || !path) return null;
  const { data, error } = await supabase.storage.from(BUCKET).createSignedUrl(path, 3600);
  if (error) return null;
  return data.signedUrl;
}
