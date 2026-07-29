import { setActionExternalId } from '@/db/notes';
import type { ActionItem, Note } from '@/db/types';
import { createCalendarEvent, createGmailDraft } from './googleApi';

/**
 * Turns an extracted action item into something real in the user's Google
 * account, then records the resulting id so the UI can show it is already done
 * and never create a duplicate.
 */
export async function runActionItem(item: ActionItem, note: Pick<Note, 'title' | 'transcript'>) {
  switch (item.kind) {
    case 'event':
    case 'reminder': {
      // An item with no time still deserves a slot: default to the next hour so
      // the user gets an event they can drag, rather than an error.
      const start = item.dueAt ?? nextHour();
      const event = await createCalendarEvent({
        title: item.text,
        startMs: start,
        durationMinutes: item.durationMinutes ?? (item.kind === 'reminder' ? 15 : 30),
        description: `From your Echo note “${note.title}”.`,
      });
      await setActionExternalId(item.id, event.id);
      return { kind: 'event' as const, url: event.htmlLink };
    }

    case 'email': {
      if (!item.recipient) {
        throw new Error('This note did not mention who the email is for.');
      }
      const draft = await createGmailDraft({
        to: item.recipient,
        subject: item.text.length > 78 ? `${item.text.slice(0, 75)}…` : item.text,
        body: `${item.text}\n\n—\nDrafted from a voice note in Echo.`,
      });
      await setActionExternalId(item.id, draft.id);
      return { kind: 'email' as const, url: null };
    }

    case 'task':
    default:
      // Tasks live in Echo; there is nothing to push anywhere.
      return { kind: 'task' as const, url: null };
  }
}

function nextHour(): number {
  const date = new Date();
  date.setMinutes(0, 0, 0);
  date.setHours(date.getHours() + 1);
  return date.getTime();
}
