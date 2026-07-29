-- ─────────────────────────────────────────────────────────────────────────────
-- Echo — voice notes schema
--
-- Every row belongs to exactly one user and is only ever reachable by that
-- user. The client is local-first, so this schema is a mirror of the device's
-- SQLite rather than the source of truth: ids are generated on the device and
-- upserted here, which is what lets a note exist (and be edited) offline.
-- ─────────────────────────────────────────────────────────────────────────────

create extension if not exists "pgcrypto";

-- ── notes ────────────────────────────────────────────────────────────────────

create table if not exists public.notes (
  -- Client-generated UUID. Not a server default: the device must be able to
  -- create a note with a stable id while offline.
  id                uuid primary key,
  user_id           uuid not null references auth.users (id) on delete cascade,

  created_at        timestamptz not null default now(),
  updated_at        timestamptz not null default now(),

  title             text not null default '',
  summary           text not null default '',
  transcript        text not null default '',
  transcript_edited boolean not null default false,

  -- Storage object path in the `recordings` bucket, e.g. "<uid>/<note>.wav".
  audio_path        text,
  duration_ms       integer not null default 0,
  -- Amplitude samples (0..1) so the waveform renders identically on any device.
  amplitudes        jsonb not null default '[]'::jsonb,

  language          text not null default 'en-US',
  pinned            boolean not null default false,
  archived          boolean not null default false,
  tags              jsonb not null default '[]'::jsonb,

  -- Assistant-extracted action items, carried with the note so a second device
  -- inherits them without paying for enrichment again.
  action_items      jsonb not null default '[]'::jsonb,

  -- Soft delete: the tombstone has to reach every device before the row goes.
  deleted_at        timestamptz,

  constraint notes_duration_nonnegative check (duration_ms >= 0)
);

-- The sync engine pulls by "everything for me changed since X".
create index if not exists notes_user_updated_idx
  on public.notes (user_id, updated_at desc);

create index if not exists notes_user_created_idx
  on public.notes (user_id, created_at desc)
  where deleted_at is null;

-- Full-text search over the words the user actually said, for server-side
-- search once a library outgrows what the device wants to scan.
create index if not exists notes_transcript_fts_idx
  on public.notes
  using gin (to_tsvector('english', coalesce(title, '') || ' ' || coalesce(transcript, '')));

-- ── row level security ───────────────────────────────────────────────────────

alter table public.notes enable row level security;

-- Four explicit policies rather than one `for all`: an accidental permissive
-- write policy is far easier to spot when the verbs are separated.
create policy "read own notes"
  on public.notes for select
  using (auth.uid() = user_id);

create policy "insert own notes"
  on public.notes for insert
  with check (auth.uid() = user_id);

create policy "update own notes"
  on public.notes for update
  using (auth.uid() = user_id)
  with check (auth.uid() = user_id);

create policy "delete own notes"
  on public.notes for delete
  using (auth.uid() = user_id);

-- ── updated_at ───────────────────────────────────────────────────────────────
-- The client owns `updated_at` (it is the conflict-resolution key), so the
-- trigger only fills it in when a write omits it entirely.

create or replace function public.touch_updated_at()
returns trigger
language plpgsql
as $$
begin
  if new.updated_at is null or new.updated_at = old.updated_at then
    new.updated_at := greatest(old.updated_at, now());
  end if;
  return new;
end;
$$;

drop trigger if exists notes_touch_updated_at on public.notes;
create trigger notes_touch_updated_at
  before update on public.notes
  for each row execute function public.touch_updated_at();

-- ── audio storage ────────────────────────────────────────────────────────────
-- Private bucket. Recordings are reached through short-lived signed URLs, never
-- public links: a voice note is as sensitive as a diary entry.

insert into storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
values (
  'recordings',
  'recordings',
  false,
  104857600, -- 100 MB, comfortably past an hour of 16 kHz mono speech
  array['audio/wav', 'audio/x-wav', 'audio/mp4', 'audio/m4a', 'audio/mpeg', 'audio/aac']
)
on conflict (id) do nothing;

-- Objects are keyed "<user-id>/<note-id>.<ext>", so the first path segment is
-- the authorisation check.
create policy "read own recordings"
  on storage.objects for select
  using (bucket_id = 'recordings' and (storage.foldername(name))[1] = auth.uid()::text);

create policy "upload own recordings"
  on storage.objects for insert
  with check (bucket_id = 'recordings' and (storage.foldername(name))[1] = auth.uid()::text);

create policy "replace own recordings"
  on storage.objects for update
  using (bucket_id = 'recordings' and (storage.foldername(name))[1] = auth.uid()::text);

create policy "delete own recordings"
  on storage.objects for delete
  using (bucket_id = 'recordings' and (storage.foldername(name))[1] = auth.uid()::text);
