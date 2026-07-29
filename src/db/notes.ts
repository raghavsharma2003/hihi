import * as Crypto from 'expo-crypto';

import { getDb, notifyDbChanged } from './client';
import type {
  ActionItem,
  ActionStatus,
  EnrichStatus,
  Note,
  NoteDraft,
  NoteSegment,
  NoteWithDetails,
  SyncStatus,
} from './types';

// ── Row shapes as stored ────────────────────────────────────────────────────

interface NoteRow {
  id: string;
  created_at: number;
  updated_at: number;
  title: string;
  summary: string;
  transcript: string;
  transcript_edited: number;
  audio_uri: string | null;
  audio_remote_path: string | null;
  duration_ms: number;
  amplitudes: string;
  language: string;
  pinned: number;
  archived: number;
  enrich_status: string;
  sync_status: string;
  remote_id: string | null;
  tags: string;
}

interface ActionRow {
  id: string;
  note_id: string;
  text: string;
  kind: string;
  status: string;
  due_at: number | null;
  duration_minutes: number | null;
  recipient: string | null;
  external_id: string | null;
  created_at: number;
}

function parseJsonArray<T>(raw: string, fallback: T[]): T[] {
  try {
    const parsed = JSON.parse(raw);
    return Array.isArray(parsed) ? (parsed as T[]) : fallback;
  } catch {
    return fallback;
  }
}

function toNote(row: NoteRow): Note {
  return {
    id: row.id,
    createdAt: row.created_at,
    updatedAt: row.updated_at,
    title: row.title,
    summary: row.summary,
    transcript: row.transcript,
    transcriptEdited: row.transcript_edited === 1,
    audioUri: row.audio_uri,
    audioRemotePath: row.audio_remote_path,
    durationMs: row.duration_ms,
    amplitudes: parseJsonArray<number>(row.amplitudes, []),
    language: row.language,
    pinned: row.pinned === 1,
    archived: row.archived === 1,
    enrichStatus: row.enrich_status as EnrichStatus,
    syncStatus: row.sync_status as SyncStatus,
    remoteId: row.remote_id,
    tags: parseJsonArray<string>(row.tags, []),
  };
}

function toAction(row: ActionRow): ActionItem {
  return {
    id: row.id,
    noteId: row.note_id,
    text: row.text,
    kind: row.kind as ActionItem['kind'],
    status: row.status as ActionStatus,
    dueAt: row.due_at,
    durationMinutes: row.duration_minutes,
    recipient: row.recipient,
    externalId: row.external_id,
    createdAt: row.created_at,
  };
}

/**
 * A readable title from the transcript alone, used immediately at save time so
 * a new note is never nameless while the assistant works (or when there is no
 * assistant configured at all).
 */
export function deriveTitle(transcript: string): string {
  const clean = transcript.trim().replace(/\s+/g, ' ');
  if (!clean) return 'Untitled note';

  // Prefer the first sentence; fall back to a word-boundary truncation.
  const sentence = clean.split(/(?<=[.!?])\s/)[0] ?? clean;
  const candidate = sentence.length <= 64 ? sentence : clean.slice(0, 64);
  const trimmed =
    candidate.length < clean.length
      ? candidate.replace(/\s+\S*$/, '').replace(/[,;:.\-–—]$/, '')
      : candidate;

  const title = (trimmed || clean.slice(0, 48)).replace(/[.!?]$/, '');
  return title.charAt(0).toUpperCase() + title.slice(1);
}

// ── Reads ───────────────────────────────────────────────────────────────────

export async function listNotes(options?: {
  search?: string;
  archived?: boolean;
  limit?: number;
}): Promise<Note[]> {
  const db = await getDb();
  const archived = options?.archived ? 1 : 0;
  const limit = options?.limit ?? 500;
  const search = options?.search?.trim();

  // Pinned first, then newest. Search matches title, summary or transcript so
  // a half-remembered phrase from the middle of a note still finds it.
  const rows = search
    ? await db.getAllAsync<NoteRow>(
        `SELECT * FROM notes
         WHERE deleted_at IS NULL AND archived = ?
           AND (title LIKE ? OR summary LIKE ? OR transcript LIKE ?)
         ORDER BY pinned DESC, created_at DESC
         LIMIT ?;`,
        archived,
        `%${search}%`,
        `%${search}%`,
        `%${search}%`,
        limit,
      )
    : await db.getAllAsync<NoteRow>(
        `SELECT * FROM notes
         WHERE deleted_at IS NULL AND archived = ?
         ORDER BY pinned DESC, created_at DESC
         LIMIT ?;`,
        archived,
        limit,
      );

  return rows.map(toNote);
}

export async function getNote(id: string): Promise<NoteWithDetails | null> {
  const db = await getDb();
  const row = await db.getFirstAsync<NoteRow>(
    'SELECT * FROM notes WHERE id = ? AND deleted_at IS NULL;',
    id,
  );
  if (!row) return null;

  const [actionRows, segmentRows] = await Promise.all([
    db.getAllAsync<ActionRow>(
      'SELECT * FROM action_items WHERE note_id = ? ORDER BY created_at ASC;',
      id,
    ),
    db.getAllAsync<NoteSegment & { note_id: string; start_ms: number; end_ms: number }>(
      'SELECT id, note_id, start_ms, end_ms, text FROM note_segments WHERE note_id = ? ORDER BY start_ms ASC;',
      id,
    ),
  ]);

  return {
    ...toNote(row),
    actionItems: actionRows.map(toAction),
    segments: segmentRows.map((s) => ({
      id: s.id,
      noteId: s.note_id,
      startMs: s.start_ms,
      endMs: s.end_ms,
      text: s.text,
    })),
  };
}

/** Every open action item across all notes, soonest first. Powers the agenda. */
export async function listOpenActions(): Promise<(ActionItem & { noteTitle: string })[]> {
  const db = await getDb();
  const rows = await db.getAllAsync<ActionRow & { note_title: string }>(
    `SELECT a.*, n.title AS note_title
     FROM action_items a
     JOIN notes n ON n.id = a.note_id
     WHERE a.status = 'open' AND n.deleted_at IS NULL
     ORDER BY (a.due_at IS NULL), a.due_at ASC, a.created_at DESC;`,
  );
  return rows.map((r) => ({ ...toAction(r), noteTitle: r.note_title }));
}

export async function countNotes(): Promise<number> {
  const db = await getDb();
  const row = await db.getFirstAsync<{ n: number }>(
    'SELECT COUNT(*) AS n FROM notes WHERE deleted_at IS NULL AND archived = 0;',
  );
  return row?.n ?? 0;
}

// ── Writes ──────────────────────────────────────────────────────────────────

export async function createNote(draft: NoteDraft): Promise<string> {
  const db = await getDb();
  const id = Crypto.randomUUID();
  const now = Date.now();

  await db.withTransactionAsync(async () => {
    await db.runAsync(
      `INSERT INTO notes (
         id, created_at, updated_at, title, summary, transcript, transcript_edited,
         audio_uri, audio_remote_path, duration_ms, amplitudes, language,
         pinned, archived, enrich_status, sync_status, remote_id, tags
       ) VALUES (?, ?, ?, ?, '', ?, 0, ?, NULL, ?, ?, ?, 0, 0, 'pending', 'local', NULL, '[]');`,
      id,
      now,
      now,
      deriveTitle(draft.transcript),
      draft.transcript,
      draft.audioUri,
      draft.durationMs,
      JSON.stringify(draft.amplitudes),
      draft.language,
    );

    for (const seg of draft.segments) {
      await db.runAsync(
        'INSERT INTO note_segments (id, note_id, start_ms, end_ms, text) VALUES (?, ?, ?, ?, ?);',
        Crypto.randomUUID(),
        id,
        seg.startMs,
        seg.endMs,
        seg.text,
      );
    }
  });

  notifyDbChanged();
  return id;
}

/** Marks the note dirty so the sync engine picks the change up. */
async function touch(id: string): Promise<void> {
  const db = await getDb();
  await db.runAsync(
    `UPDATE notes
     SET updated_at = ?,
         sync_status = CASE WHEN sync_status = 'synced' THEN 'dirty' ELSE sync_status END
     WHERE id = ?;`,
    Date.now(),
    id,
  );
}

export async function updateTranscript(id: string, transcript: string): Promise<void> {
  const db = await getDb();
  await db.runAsync('UPDATE notes SET transcript = ?, transcript_edited = 1 WHERE id = ?;', transcript, id);
  await touch(id);
  notifyDbChanged();
}

export async function updateTitle(id: string, title: string): Promise<void> {
  const db = await getDb();
  await db.runAsync('UPDATE notes SET title = ? WHERE id = ?;', title.trim() || 'Untitled note', id);
  await touch(id);
  notifyDbChanged();
}

export async function setPinned(id: string, pinned: boolean): Promise<void> {
  const db = await getDb();
  await db.runAsync('UPDATE notes SET pinned = ? WHERE id = ?;', pinned ? 1 : 0, id);
  await touch(id);
  notifyDbChanged();
}

export async function setArchived(id: string, archived: boolean): Promise<void> {
  const db = await getDb();
  await db.runAsync('UPDATE notes SET archived = ? WHERE id = ?;', archived ? 1 : 0, id);
  await touch(id);
  notifyDbChanged();
}

/** Soft delete, so a pending sync can propagate the deletion to the server. */
export async function deleteNote(id: string): Promise<void> {
  const db = await getDb();
  await db.runAsync(
    "UPDATE notes SET deleted_at = ?, sync_status = CASE WHEN sync_status = 'local' THEN 'local' ELSE 'dirty' END WHERE id = ?;",
    Date.now(),
    id,
  );
  notifyDbChanged();
}

/** Points a note at its recording after the file has been given a stable name. */
export async function updateAudioUri(id: string, audioUri: string): Promise<void> {
  const db = await getDb();
  await db.runAsync('UPDATE notes SET audio_uri = ? WHERE id = ?;', audioUri, id);
  notifyDbChanged();
}

export async function setSyncState(
  id: string,
  status: SyncStatus,
  fields?: { remoteId?: string | null; audioRemotePath?: string | null },
): Promise<void> {
  const db = await getDb();
  await db.runAsync(
    `UPDATE notes
     SET sync_status = ?,
         remote_id = COALESCE(?, remote_id),
         audio_remote_path = COALESCE(?, audio_remote_path)
     WHERE id = ?;`,
    status,
    fields?.remoteId ?? null,
    fields?.audioRemotePath ?? null,
    id,
  );
  notifyDbChanged();
}

export async function setEnrichStatus(id: string, status: EnrichStatus): Promise<void> {
  const db = await getDb();
  await db.runAsync('UPDATE notes SET enrich_status = ? WHERE id = ?;', status, id);
  notifyDbChanged();
}

export interface EnrichmentResult {
  title?: string;
  summary?: string;
  tags?: string[];
  actionItems?: {
    text: string;
    kind: ActionItem['kind'];
    dueAt?: number | null;
    durationMinutes?: number | null;
    recipient?: string | null;
  }[];
}

/**
 * Applies what the assistant produced. A title the user has already renamed, or
 * a transcript they have corrected, is never overwritten — their edit wins.
 */
export async function applyEnrichment(id: string, result: EnrichmentResult): Promise<void> {
  const db = await getDb();
  const now = Date.now();

  await db.withTransactionAsync(async () => {
    if (result.title) {
      await db.runAsync('UPDATE notes SET title = ? WHERE id = ?;', result.title, id);
    }
    if (result.summary !== undefined) {
      await db.runAsync('UPDATE notes SET summary = ? WHERE id = ?;', result.summary, id);
    }
    if (result.tags) {
      await db.runAsync('UPDATE notes SET tags = ? WHERE id = ?;', JSON.stringify(result.tags), id);
    }

    if (result.actionItems) {
      // Replace only the items the assistant owns; anything the user already
      // completed or dismissed stays put.
      await db.runAsync("DELETE FROM action_items WHERE note_id = ? AND status = 'open';", id);
      for (const item of result.actionItems) {
        await db.runAsync(
          `INSERT INTO action_items
             (id, note_id, text, kind, status, due_at, duration_minutes, recipient, external_id, created_at)
           VALUES (?, ?, ?, ?, 'open', ?, ?, ?, NULL, ?);`,
          Crypto.randomUUID(),
          id,
          item.text,
          item.kind,
          item.dueAt ?? null,
          item.durationMinutes ?? null,
          item.recipient ?? null,
          now,
        );
      }
    }

    await db.runAsync(
      `UPDATE notes SET enrich_status = 'done', updated_at = ?,
         sync_status = CASE WHEN sync_status = 'synced' THEN 'dirty' ELSE sync_status END
       WHERE id = ?;`,
      now,
      id,
    );
  });

  notifyDbChanged();
}

export async function setActionStatus(actionId: string, status: ActionStatus): Promise<void> {
  const db = await getDb();
  await db.runAsync('UPDATE action_items SET status = ? WHERE id = ?;', status, actionId);
  notifyDbChanged();
}

export async function setActionExternalId(actionId: string, externalId: string): Promise<void> {
  const db = await getDb();
  await db.runAsync('UPDATE action_items SET external_id = ? WHERE id = ?;', externalId, actionId);
  notifyDbChanged();
}

// ── Queues consumed by the sync engine ──────────────────────────────────────

export async function notesNeedingEnrichment(limit = 5): Promise<Note[]> {
  const db = await getDb();
  const rows = await db.getAllAsync<NoteRow>(
    `SELECT * FROM notes
     WHERE deleted_at IS NULL AND enrich_status IN ('pending', 'failed') AND transcript <> ''
     ORDER BY created_at DESC LIMIT ?;`,
    limit,
  );
  return rows.map(toNote);
}

export async function notesNeedingPush(limit = 20): Promise<Note[]> {
  const db = await getDb();
  const rows = await db.getAllAsync<NoteRow>(
    `SELECT * FROM notes
     WHERE sync_status IN ('local', 'dirty', 'failed')
     ORDER BY updated_at ASC LIMIT ?;`,
    limit,
  );
  return rows.map(toNote);
}

/** Action items for one note, in the shape the sync engine ships to the server. */
export async function actionItemsForSync(noteId: string): Promise<ActionItem[]> {
  const db = await getDb();
  const rows = await db.getAllAsync<ActionRow>(
    'SELECT * FROM action_items WHERE note_id = ? ORDER BY created_at ASC;',
    noteId,
  );
  return rows.map(toAction);
}

/**
 * Replaces a note's action items with the server's copy. Used on pull, so a
 * second device inherits what the assistant extracted (and what the user has
 * already ticked off) without re-running enrichment.
 */
export async function replaceActionItems(noteId: string, items: ActionItem[]): Promise<void> {
  const db = await getDb();
  await db.withTransactionAsync(async () => {
    await db.runAsync('DELETE FROM action_items WHERE note_id = ?;', noteId);
    for (const item of items) {
      await db.runAsync(
        `INSERT INTO action_items
           (id, note_id, text, kind, status, due_at, duration_minutes, recipient, external_id, created_at)
         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);`,
        item.id || Crypto.randomUUID(),
        noteId,
        item.text,
        item.kind,
        item.status,
        item.dueAt,
        item.durationMinutes,
        item.recipient,
        item.externalId,
        item.createdAt || Date.now(),
      );
    }
  });
}

export async function hardDeleteSynced(): Promise<void> {
  const db = await getDb();
  await db.runAsync("DELETE FROM notes WHERE deleted_at IS NOT NULL AND sync_status = 'synced';");
}
