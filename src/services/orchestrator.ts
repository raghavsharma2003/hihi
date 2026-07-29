import { AppState, type AppStateStatus } from 'react-native';

import {
  applyEnrichment,
  notesNeedingEnrichment,
  setEnrichStatus,
  type EnrichmentResult,
} from '@/db/notes';
import type { ActionItem } from '@/db/types';
import { BackendUnavailableError, invokeFunction, isAiConfigured } from './supabase';
import { runSyncCycle } from './sync';

/**
 * Coordinates the two things that happen to a note after it is saved: the
 * assistant reads it, and it gets pushed to the cloud. Both are optional, both
 * retry, and neither ever blocks the UI — a note is fully usable the instant it
 * is written to SQLite.
 */

const POLL_INTERVAL_MS = 30_000;

let timer: ReturnType<typeof setInterval> | null = null;
let appStateSub: { remove: () => void } | null = null;
let running = false;

/** Notes that failed enrichment this session, with their next retry time. */
const enrichBackoff = new Map<string, number>();

interface EnrichResponse {
  title?: string;
  summary?: string;
  tags?: string[];
  actionItems?: {
    text: string;
    kind?: string;
    dueAt?: string | number | null;
    durationMinutes?: number | null;
    recipient?: string | null;
  }[];
}

const VALID_KINDS: ActionItem['kind'][] = ['task', 'event', 'email', 'reminder'];

/**
 * Normalises whatever the model returned into the shapes the database expects.
 * The edge function constrains the output schema, but a client that trusts a
 * model's JSON without checking is one bad response away from a crash.
 */
function coerceEnrichment(raw: EnrichResponse): EnrichmentResult {
  const actionItems = (raw.actionItems ?? [])
    .filter((item) => typeof item?.text === 'string' && item.text.trim().length > 0)
    .slice(0, 12)
    .map((item) => {
      const kind = VALID_KINDS.includes(item.kind as ActionItem['kind'])
        ? (item.kind as ActionItem['kind'])
        : 'task';

      // The output schema uses "" and 0 for "not mentioned" rather than null,
      // because a flat non-nullable schema is more reliable for the model to
      // satisfy. Normalise those back to null here.
      let dueAt: number | null = null;
      if (typeof item.dueAt === 'number' && Number.isFinite(item.dueAt)) {
        dueAt = item.dueAt;
      } else if (typeof item.dueAt === 'string' && item.dueAt.trim()) {
        const parsed = Date.parse(item.dueAt);
        if (!Number.isNaN(parsed)) dueAt = parsed;
      }

      const durationMinutes =
        typeof item.durationMinutes === 'number' && item.durationMinutes > 0
          ? item.durationMinutes
          : null;

      const recipient =
        typeof item.recipient === 'string' && item.recipient.trim() ? item.recipient.trim() : null;

      return { text: item.text.trim(), kind, dueAt, durationMinutes, recipient };
    });

  return {
    title: typeof raw.title === 'string' && raw.title.trim() ? raw.title.trim().slice(0, 120) : undefined,
    summary: typeof raw.summary === 'string' ? raw.summary.trim() : undefined,
    tags: Array.isArray(raw.tags)
      ? raw.tags.filter((t): t is string => typeof t === 'string').slice(0, 6)
      : undefined,
    actionItems,
  };
}

async function enrichPending(): Promise<void> {
  if (!isAiConfigured()) {
    // Mark them skipped so the UI stops showing a spinner that will never end.
    for (const note of await notesNeedingEnrichment(20)) {
      await setEnrichStatus(note.id, 'skipped');
    }
    return;
  }

  const notes = await notesNeedingEnrichment(3);
  const now = Date.now();

  for (const note of notes) {
    const retryAt = enrichBackoff.get(note.id);
    if (retryAt && now < retryAt) continue;

    try {
      const response = await invokeFunction<EnrichResponse>('enrich-note', {
        transcript: note.transcript,
        recordedAt: new Date(note.createdAt).toISOString(),
        // Lets the model resolve "tomorrow at 9" into a real timestamp.
        timeZone: Intl.DateTimeFormat().resolvedOptions().timeZone,
        language: note.language,
      });

      await applyEnrichment(note.id, coerceEnrichment(response));
      enrichBackoff.delete(note.id);
    } catch (err) {
      if (err instanceof BackendUnavailableError) {
        await setEnrichStatus(note.id, 'skipped');
        continue;
      }

      await setEnrichStatus(note.id, 'failed');
      // Exponential-ish backoff so a broken key doesn't hammer the function.
      const previous = enrichBackoff.get(note.id) ?? 0;
      const delay = Math.min(15 * 60_000, previous ? (previous - now) * 2 || 60_000 : 60_000);
      enrichBackoff.set(note.id, now + delay);
      console.warn('[echo] enrichment failed', err);
    }
  }
}

async function tick(): Promise<void> {
  if (running) return;
  running = true;
  try {
    await enrichPending();
    await runSyncCycle();
  } catch (err) {
    console.warn('[echo] background cycle failed', err);
  } finally {
    running = false;
  }
}

function handleAppStateChange(state: AppStateStatus): void {
  // Coming back to the foreground is the moment the user is most likely to be
  // looking at stale data, so catch up immediately rather than on the next tick.
  if (state === 'active') void tick();
}

export function startBackgroundWork(): void {
  if (timer) return;
  void tick();
  timer = setInterval(() => void tick(), POLL_INTERVAL_MS);
  appStateSub = AppState.addEventListener('change', handleAppStateChange);
}

export function stopBackgroundWork(): void {
  if (timer) {
    clearInterval(timer);
    timer = null;
  }
  appStateSub?.remove();
  appStateSub = null;
}

/**
 * Nudges the loop to run now — called right after a note is saved so the
 * assistant starts reading it while the user is still on the note screen.
 */
export function requestEnrichment(noteId?: string): void {
  if (noteId) enrichBackoff.delete(noteId);
  void tick();
}
