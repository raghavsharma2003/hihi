import { format, isThisYear, isToday, isYesterday, differenceInCalendarDays } from 'date-fns';

/** Compact timestamp for list rows: "14:32", "Yesterday", "12 Mar". */
export function formatNoteTime(epochMs: number): string {
  const date = new Date(epochMs);
  if (isToday(date)) return format(date, 'HH:mm');
  if (isYesterday(date)) return 'Yesterday';
  if (isThisYear(date)) return format(date, 'd MMM');
  return format(date, 'd MMM yyyy');
}

/** Full timestamp for the detail header. */
export function formatNoteTimestamp(epochMs: number): string {
  const date = new Date(epochMs);
  if (isToday(date)) return `Today at ${format(date, 'HH:mm')}`;
  if (isYesterday(date)) return `Yesterday at ${format(date, 'HH:mm')}`;
  return format(date, "d MMM yyyy 'at' HH:mm");
}

/** Section title a note belongs under in the list. */
export function dateGroupLabel(epochMs: number): string {
  const date = new Date(epochMs);
  if (isToday(date)) return 'Today';
  if (isYesterday(date)) return 'Yesterday';

  const days = differenceInCalendarDays(new Date(), date);
  if (days < 7) return 'This week';
  if (days < 30) return 'This month';
  if (isThisYear(date)) return format(date, 'MMMM');
  return format(date, 'MMMM yyyy');
}

/** mm:ss for durations under an hour, h:mm:ss beyond. */
export function formatDuration(ms: number): string {
  const total = Math.round(ms / 1000);
  const hours = Math.floor(total / 3600);
  const minutes = Math.floor((total % 3600) / 60);
  const seconds = total % 60;

  if (hours > 0) {
    return `${hours}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
  }
  return `${minutes}:${seconds.toString().padStart(2, '0')}`;
}

/** Time of day for calendar rows. */
export function formatTimeOfDay(epochMs: number): string {
  return format(new Date(epochMs), 'HH:mm');
}

export function formatDueDate(epochMs: number): string {
  const date = new Date(epochMs);
  if (isToday(date)) return `Today ${format(date, 'HH:mm')}`;
  if (isYesterday(date)) return `Yesterday ${format(date, 'HH:mm')}`;
  return format(date, 'd MMM, HH:mm');
}
