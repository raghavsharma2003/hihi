import { getAccessToken } from './googleAuth';

const CALENDAR_BASE = 'https://www.googleapis.com/calendar/v3';
const GMAIL_BASE = 'https://gmail.googleapis.com/gmail/v1/users/me';

export class GoogleNotConnectedError extends Error {
  constructor() {
    super('Google is not connected.');
    this.name = 'GoogleNotConnectedError';
  }
}

async function googleFetch<T>(url: string, init?: RequestInit): Promise<T> {
  const token = await getAccessToken();
  if (!token) throw new GoogleNotConnectedError();

  const response = await fetch(url, {
    ...init,
    headers: {
      Authorization: `Bearer ${token}`,
      'Content-Type': 'application/json',
      ...(init?.headers ?? {}),
    },
  });

  if (!response.ok) {
    const body = await response.text();
    throw new Error(`Google API ${response.status}: ${body.slice(0, 300)}`);
  }
  return (await response.json()) as T;
}

// ── Calendar ────────────────────────────────────────────────────────────────

export interface CalendarEvent {
  id: string;
  title: string;
  startMs: number;
  endMs: number;
  allDay: boolean;
  location: string | null;
  hangoutLink: string | null;
  htmlLink: string | null;
}

interface RawEvent {
  id: string;
  summary?: string;
  location?: string;
  hangoutLink?: string;
  htmlLink?: string;
  start?: { dateTime?: string; date?: string };
  end?: { dateTime?: string; date?: string };
}

function toCalendarEvent(raw: RawEvent): CalendarEvent {
  const allDay = Boolean(raw.start?.date);
  const start = raw.start?.dateTime ?? raw.start?.date;
  const end = raw.end?.dateTime ?? raw.end?.date;
  return {
    id: raw.id,
    title: raw.summary ?? '(no title)',
    startMs: start ? new Date(start).getTime() : 0,
    endMs: end ? new Date(end).getTime() : 0,
    allDay,
    location: raw.location ?? null,
    hangoutLink: raw.hangoutLink ?? null,
    htmlLink: raw.htmlLink ?? null,
  };
}

/** Events between now and `hoursAhead`, ordered by start time. */
export async function listUpcomingEvents(hoursAhead = 36, maxResults = 25): Promise<CalendarEvent[]> {
  const timeMin = new Date().toISOString();
  const timeMax = new Date(Date.now() + hoursAhead * 3600_000).toISOString();

  const url =
    `${CALENDAR_BASE}/calendars/primary/events?` +
    new URLSearchParams({
      timeMin,
      timeMax,
      singleEvents: 'true',
      orderBy: 'startTime',
      maxResults: String(maxResults),
    }).toString();

  const data = await googleFetch<{ items?: RawEvent[] }>(url);
  return (data.items ?? []).map(toCalendarEvent);
}

export interface CreateEventInput {
  title: string;
  startMs: number;
  durationMinutes?: number;
  description?: string;
}

export async function createCalendarEvent(input: CreateEventInput): Promise<CalendarEvent> {
  const duration = input.durationMinutes ?? 30;
  const body = {
    summary: input.title,
    description: input.description,
    start: {
      dateTime: new Date(input.startMs).toISOString(),
      // Letting Google resolve the zone from the device avoids events landing
      // an hour out when the user travels or DST shifts.
      timeZone: Intl.DateTimeFormat().resolvedOptions().timeZone,
    },
    end: {
      dateTime: new Date(input.startMs + duration * 60_000).toISOString(),
      timeZone: Intl.DateTimeFormat().resolvedOptions().timeZone,
    },
  };

  const raw = await googleFetch<RawEvent>(`${CALENDAR_BASE}/calendars/primary/events`, {
    method: 'POST',
    body: JSON.stringify(body),
  });
  return toCalendarEvent(raw);
}

// ── Gmail ───────────────────────────────────────────────────────────────────

export interface InboxMessage {
  id: string;
  threadId: string;
  from: string;
  subject: string;
  snippet: string;
  receivedMs: number;
  unread: boolean;
}

interface RawMessage {
  id: string;
  threadId: string;
  snippet?: string;
  internalDate?: string;
  labelIds?: string[];
  payload?: { headers?: { name: string; value: string }[] };
}

function header(raw: RawMessage, name: string): string {
  const found = raw.payload?.headers?.find((h) => h.name.toLowerCase() === name.toLowerCase());
  return found?.value ?? '';
}

/** Cleans `"Jane Doe" <jane@x.com>` down to a display name. */
function displayName(from: string): string {
  const match = from.match(/^\s*"?([^"<]*?)"?\s*<.+>\s*$/);
  const name = match?.[1]?.trim();
  return name || from.replace(/[<>]/g, '').trim();
}

/**
 * Recent unread mail, hydrated one message at a time — Gmail's list endpoint
 * returns ids only, so the detail fetches are unavoidable. Capped at a small
 * number because this is a digest, not an email client.
 */
export async function listInboxDigest(limit = 12): Promise<InboxMessage[]> {
  const listUrl =
    `${GMAIL_BASE}/messages?` +
    new URLSearchParams({
      q: 'in:inbox is:unread newer_than:7d',
      maxResults: String(limit),
    }).toString();

  const list = await googleFetch<{ messages?: { id: string }[] }>(listUrl);
  const ids = (list.messages ?? []).map((m) => m.id);
  if (ids.length === 0) return [];

  const messages = await Promise.all(
    ids.map((id) =>
      googleFetch<RawMessage>(
        `${GMAIL_BASE}/messages/${id}?` +
          new URLSearchParams({
            format: 'metadata',
            // Repeated params are how the Gmail API takes a header list.
            metadataHeaders: 'From',
          }).toString() +
          '&metadataHeaders=Subject&metadataHeaders=Date',
      ).catch(() => null),
    ),
  );

  return messages
    .filter((m): m is RawMessage => m !== null)
    .map((raw) => ({
      id: raw.id,
      threadId: raw.threadId,
      from: displayName(header(raw, 'From')),
      subject: header(raw, 'Subject') || '(no subject)',
      snippet: raw.snippet ?? '',
      receivedMs: raw.internalDate ? Number(raw.internalDate) : 0,
      unread: raw.labelIds?.includes('UNREAD') ?? true,
    }))
    .sort((a, b) => b.receivedMs - a.receivedMs);
}

/** RFC 2822 message, base64url-encoded as Gmail's API requires. */
function encodeMessage(to: string, subject: string, body: string): string {
  const mime = [
    `To: ${to}`,
    `Subject: ${subject}`,
    'Content-Type: text/plain; charset="UTF-8"',
    'MIME-Version: 1.0',
    '',
    body,
  ].join('\r\n');

  // btoa is only safe for latin1, so encode UTF-8 to bytes first.
  const bytes = new TextEncoder().encode(mime);
  let binary = '';
  bytes.forEach((byte) => {
    binary += String.fromCharCode(byte);
  });

  return btoa(binary).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
}

export interface CreateDraftInput {
  to: string;
  subject: string;
  body: string;
}

export async function createGmailDraft(input: CreateDraftInput): Promise<{ id: string }> {
  const draft = await googleFetch<{ id: string }>(`${GMAIL_BASE}/drafts`, {
    method: 'POST',
    body: JSON.stringify({ message: { raw: encodeMessage(input.to, input.subject, input.body) } }),
  });
  return { id: draft.id };
}
