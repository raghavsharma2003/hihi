import { Directory, File, Paths } from 'expo-file-system';

/**
 * Recordings live in the document directory, not the cache directory. The OS is
 * free to evict the cache under storage pressure, and losing the audio half of a
 * note the user believes is saved is not a recoverable failure.
 */
const RECORDINGS_DIR = 'recordings';

export function recordingsDirectory(): Directory {
  const dir = new Directory(Paths.document, RECORDINGS_DIR);
  if (!dir.exists) dir.create({ intermediates: true });
  return dir;
}

/** Directory URI to hand to the recogniser as its output location. */
export function recordingsDirectoryUri(): string {
  return recordingsDirectory().uri;
}

export function audioFileName(noteIdOrStamp: string, extension = 'wav'): string {
  return `${noteIdOrStamp}.${extension}`;
}

/** Bytes on disk, or 0 if the file is missing. */
export function audioSize(uri: string | null): number {
  if (!uri) return 0;
  try {
    const file = new File(uri);
    return file.exists ? (file.size ?? 0) : 0;
  } catch {
    return 0;
  }
}

export function audioExists(uri: string | null): boolean {
  if (!uri) return false;
  try {
    return new File(uri).exists;
  } catch {
    return false;
  }
}

/**
 * Moves a freshly captured recording to its permanent name once the note it
 * belongs to has an id. Returns the new URI, or the original if the move fails
 * — a recording in the wrong place still beats no recording.
 */
export function adoptRecording(sourceUri: string, noteId: string): string {
  try {
    const source = new File(sourceUri);
    if (!source.exists) return sourceUri;

    const extension = sourceUri.split('.').pop() ?? 'wav';
    const target = new File(recordingsDirectory(), audioFileName(noteId, extension));
    if (target.exists) target.delete();

    source.moveSync(target);
    return target.uri;
  } catch {
    return sourceUri;
  }
}

export function deleteRecording(uri: string | null): void {
  if (!uri) return;
  try {
    const file = new File(uri);
    if (file.exists) file.delete();
  } catch {
    // A recording we cannot delete is a leak, not a crash. Storage housekeeping
    // will sweep it; failing the surrounding delete would be worse.
  }
}

/** Total bytes held by recordings — shown in Settings so storage is legible. */
export function totalRecordingBytes(): number {
  try {
    return recordingsDirectory()
      .list()
      .reduce((sum, entry) => (entry instanceof File ? sum + (entry.size ?? 0) : sum), 0);
  } catch {
    return 0;
  }
}

export function formatBytes(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(0)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}
