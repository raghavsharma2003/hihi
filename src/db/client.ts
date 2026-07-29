import * as SQLite from 'expo-sqlite';

const DB_NAME = 'echo.db';

/**
 * Ordered, append-only migrations. Never edit a statement that has shipped —
 * add a new entry instead, or devices that already ran it will diverge.
 */
const MIGRATIONS: string[] = [
  // 1 — core note storage
  `
  CREATE TABLE IF NOT EXISTS notes (
    id                TEXT PRIMARY KEY NOT NULL,
    created_at        INTEGER NOT NULL,
    updated_at        INTEGER NOT NULL,
    title             TEXT NOT NULL DEFAULT '',
    summary           TEXT NOT NULL DEFAULT '',
    transcript        TEXT NOT NULL DEFAULT '',
    transcript_edited INTEGER NOT NULL DEFAULT 0,
    audio_uri         TEXT,
    audio_remote_path TEXT,
    duration_ms       INTEGER NOT NULL DEFAULT 0,
    amplitudes        TEXT NOT NULL DEFAULT '[]',
    language          TEXT NOT NULL DEFAULT 'en-US',
    pinned            INTEGER NOT NULL DEFAULT 0,
    archived          INTEGER NOT NULL DEFAULT 0,
    enrich_status     TEXT NOT NULL DEFAULT 'pending',
    sync_status       TEXT NOT NULL DEFAULT 'local',
    remote_id         TEXT,
    tags              TEXT NOT NULL DEFAULT '[]',
    deleted_at        INTEGER
  );

  CREATE INDEX IF NOT EXISTS idx_notes_created  ON notes (deleted_at, archived, created_at DESC);
  CREATE INDEX IF NOT EXISTS idx_notes_sync     ON notes (sync_status);
  CREATE INDEX IF NOT EXISTS idx_notes_enrich   ON notes (enrich_status);

  CREATE TABLE IF NOT EXISTS note_segments (
    id       TEXT PRIMARY KEY NOT NULL,
    note_id  TEXT NOT NULL REFERENCES notes(id) ON DELETE CASCADE,
    start_ms INTEGER NOT NULL,
    end_ms   INTEGER NOT NULL,
    text     TEXT NOT NULL
  );
  CREATE INDEX IF NOT EXISTS idx_segments_note ON note_segments (note_id, start_ms);

  CREATE TABLE IF NOT EXISTS action_items (
    id               TEXT PRIMARY KEY NOT NULL,
    note_id          TEXT NOT NULL REFERENCES notes(id) ON DELETE CASCADE,
    text             TEXT NOT NULL,
    kind             TEXT NOT NULL DEFAULT 'task',
    status           TEXT NOT NULL DEFAULT 'open',
    due_at           INTEGER,
    duration_minutes INTEGER,
    recipient        TEXT,
    external_id      TEXT,
    created_at       INTEGER NOT NULL
  );
  CREATE INDEX IF NOT EXISTS idx_actions_note   ON action_items (note_id);
  CREATE INDEX IF NOT EXISTS idx_actions_status ON action_items (status, due_at);

  CREATE TABLE IF NOT EXISTS settings (
    key   TEXT PRIMARY KEY NOT NULL,
    value TEXT NOT NULL
  );
  `,
];

let dbPromise: Promise<SQLite.SQLiteDatabase> | null = null;

async function migrate(db: SQLite.SQLiteDatabase): Promise<void> {
  await db.execAsync('PRAGMA journal_mode = WAL;');
  await db.execAsync('PRAGMA foreign_keys = ON;');

  const row = await db.getFirstAsync<{ user_version: number }>('PRAGMA user_version;');
  const current = row?.user_version ?? 0;

  for (let version = current; version < MIGRATIONS.length; version++) {
    await db.withTransactionAsync(async () => {
      await db.execAsync(MIGRATIONS[version]!);
    });
    // PRAGMA can't be parameterised, and `version` is a loop index we control.
    await db.execAsync(`PRAGMA user_version = ${version + 1};`);
  }
}

/** Opens (once) and migrates the local database. Safe to call from anywhere. */
export function getDb(): Promise<SQLite.SQLiteDatabase> {
  if (!dbPromise) {
    dbPromise = (async () => {
      const db = await SQLite.openDatabaseAsync(DB_NAME);
      await migrate(db);
      return db;
    })().catch((err) => {
      // Let the next caller retry rather than caching a rejected promise
      // forever — a transient open failure shouldn't brick the session.
      dbPromise = null;
      throw err;
    });
  }
  return dbPromise;
}

// ── Change notification ─────────────────────────────────────────────────────
// Screens subscribe to this instead of polling. Every write helper below bumps
// it, so any open list or detail view re-reads exactly once per mutation.

type Listener = () => void;
const listeners = new Set<Listener>();
let revision = 0;

export function subscribeToDb(listener: Listener): () => void {
  listeners.add(listener);
  return () => listeners.delete(listener);
}

export function getDbRevision(): number {
  return revision;
}

export function notifyDbChanged(): void {
  revision += 1;
  listeners.forEach((l) => l());
}

// ── Settings ────────────────────────────────────────────────────────────────

export async function getSetting(key: string): Promise<string | null> {
  const db = await getDb();
  const row = await db.getFirstAsync<{ value: string }>(
    'SELECT value FROM settings WHERE key = ?;',
    key,
  );
  return row?.value ?? null;
}

export async function setSetting(key: string, value: string): Promise<void> {
  const db = await getDb();
  await db.runAsync(
    'INSERT INTO settings (key, value) VALUES (?, ?) ON CONFLICT(key) DO UPDATE SET value = excluded.value;',
    key,
    value,
  );
}
