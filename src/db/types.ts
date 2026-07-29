/** Where a note stands with the cloud. Notes are usable at every stage. */
export type SyncStatus =
  /** Exists only on this device. Either there is no backend, or we haven't pushed yet. */
  | 'local'
  /** Pushed and matching the server. */
  | 'synced'
  /** Edited since the last push. */
  | 'dirty'
  /** Last push failed; the sync engine will retry with backoff. */
  | 'failed';

/** Where a note stands with the assistant. */
export type EnrichStatus =
  /** Queued for the assistant. */
  | 'pending'
  /** Assistant produced a title, summary and action items. */
  | 'done'
  /** Assistant call failed; the raw note is intact and it can be retried. */
  | 'failed'
  /** No backend configured, so the note keeps its locally-derived title. */
  | 'skipped';

export type ActionKind = 'task' | 'event' | 'email' | 'reminder';
export type ActionStatus = 'open' | 'done' | 'dismissed';

export interface Note {
  id: string;
  createdAt: number;
  updatedAt: number;

  /** Assistant-written, or the first sentence of the transcript until then. */
  title: string;
  /** Assistant-written one-paragraph gist. Empty until enrichment lands. */
  summary: string;
  /** Full text, as recognised on-device or corrected by the user. */
  transcript: string;
  /** True once the user has hand-edited the transcript — enrichment won't clobber it. */
  transcriptEdited: boolean;

  /** file:// path to the recording on this device. */
  audioUri: string | null;
  /** Storage object path once uploaded. */
  audioRemotePath: string | null;
  durationMs: number;
  /** Amplitude samples (0..1) captured while recording, for the waveform. */
  amplitudes: number[];

  language: string;
  pinned: boolean;
  archived: boolean;

  enrichStatus: EnrichStatus;
  syncStatus: SyncStatus;
  remoteId: string | null;

  tags: string[];
}

export interface NoteSegment {
  id: string;
  noteId: string;
  startMs: number;
  endMs: number;
  text: string;
}

export interface ActionItem {
  id: string;
  noteId: string;
  text: string;
  kind: ActionKind;
  status: ActionStatus;
  /** Epoch ms when this is due / when the event starts. */
  dueAt: number | null;
  /** Event duration in minutes, for `kind: 'event'`. */
  durationMinutes: number | null;
  /** For `kind: 'email'`: who it goes to. */
  recipient: string | null;
  /** ID in Google Calendar / Gmail once this has been acted on. */
  externalId: string | null;
  createdAt: number;
}

/** A note plus everything the UI needs to render it. */
export interface NoteWithDetails extends Note {
  actionItems: ActionItem[];
  segments: NoteSegment[];
}

export interface NoteDraft {
  transcript: string;
  audioUri: string | null;
  durationMs: number;
  amplitudes: number[];
  language: string;
  segments: Omit<NoteSegment, 'id' | 'noteId'>[];
}
