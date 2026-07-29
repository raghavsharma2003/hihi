import Anthropic from 'npm:@anthropic-ai/sdk@0.115.0';

import { errorResponse, json, preflight, requireAuthHeader } from '../_shared/http.ts';

/**
 * Reads a voice note and returns the things a transcript alone does not give
 * you: a title worth scanning in a list, a summary, and the commitments buried
 * in the middle of a rambling thought.
 *
 * Runs server-side so the model key never ships in the app bundle.
 */

const MODEL = 'claude-opus-5';

/**
 * Structured outputs guarantee the response parses. Times are ISO strings and
 * "unknown" is the empty string rather than null — a flat, non-nullable schema
 * is markedly more reliable than one built out of anyOf branches, and the
 * client normalises the empty cases anyway.
 */
const OUTPUT_SCHEMA = {
  type: 'object',
  properties: {
    title: {
      type: 'string',
      description:
        'A specific, scannable title of at most 8 words. Name the actual subject — never "Voice note" or "Meeting notes".',
    },
    summary: {
      type: 'string',
      description:
        'Two or three sentences capturing what the note is actually about, in the speaker\'s own framing. Empty string if the note is one short thought that the title already covers.',
    },
    tags: {
      type: 'array',
      description: 'Up to 4 lowercase single-word topics. Empty array if nothing is distinctive.',
      items: { type: 'string' },
    },
    actionItems: {
      type: 'array',
      description:
        'Only things the speaker committed to or asked for. Do not invent follow-ups, and do not turn observations into tasks.',
      items: {
        type: 'object',
        properties: {
          text: {
            type: 'string',
            description: 'The action, phrased as an imperative. e.g. "Send Priya the Q3 forecast".',
          },
          kind: {
            type: 'string',
            enum: ['task', 'event', 'email', 'reminder'],
            description:
              'event = something happening at a specific time with other people. email = a message the speaker said they would send. reminder = a time-bound personal nudge. task = everything else.',
          },
          dueAt: {
            type: 'string',
            description:
              'ISO 8601 datetime resolved against the recording time and time zone given in the prompt. Empty string if no time was mentioned. Never guess a time that was not said.',
          },
          durationMinutes: {
            type: 'integer',
            description: 'Length in minutes if one was stated. 0 if not.',
          },
          recipient: {
            type: 'string',
            description:
              'For an email, who it goes to — an address if said, otherwise the name. Empty string otherwise.',
          },
        },
        required: ['text', 'kind', 'dueAt', 'durationMinutes', 'recipient'],
        additionalProperties: false,
      },
    },
  },
  required: ['title', 'summary', 'tags', 'actionItems'],
  additionalProperties: false,
} as const;

const SYSTEM = `You process voice notes into something the speaker can act on.

These are spoken, not written. Expect false starts, repetition, filler, and transcription errors — read for intent rather than literal words, and silently correct obvious mis-hearings (names, numbers, homophones).

Rules that matter:
- The title names the subject. "Pricing change for enterprise tier", not "Voice note about pricing".
- Extract only commitments the speaker actually made or asked for. A note that is pure thinking-aloud has no action items, and returning an empty array is the correct answer.
- Resolve relative times ("tomorrow morning", "next Tuesday at 3") against the recording timestamp and time zone you are given. If a phrase is genuinely ambiguous, leave dueAt empty rather than guessing.
- Write the summary in the speaker's own terms. Do not add advice, encouragement, or commentary.
- Match the language of the transcript.`;

interface RequestBody {
  transcript?: string;
  recordedAt?: string;
  timeZone?: string;
  language?: string;
}

Deno.serve(async (request: Request) => {
  if (request.method === 'OPTIONS') return preflight();
  if (request.method !== 'POST') return errorResponse('Use POST.', 405);

  if (!requireAuthHeader(request)) {
    return errorResponse('Missing Authorization header.', 401);
  }

  const apiKey = Deno.env.get('ANTHROPIC_API_KEY');
  if (!apiKey) {
    return errorResponse(
      'ANTHROPIC_API_KEY is not set. Run: supabase secrets set ANTHROPIC_API_KEY=sk-ant-...',
      503,
    );
  }

  let body: RequestBody;
  try {
    body = (await request.json()) as RequestBody;
  } catch {
    return errorResponse('Body must be JSON.');
  }

  const transcript = body.transcript?.trim();
  if (!transcript) return errorResponse('A transcript is required.');

  // A transcript far longer than any plausible voice note is either a bug or an
  // attempt to run up the bill; truncate rather than refuse, so the user still
  // gets a usable note.
  const clipped = transcript.length > 24_000 ? `${transcript.slice(0, 24_000)}…` : transcript;

  const recordedAt = body.recordedAt ?? new Date().toISOString();
  const timeZone = body.timeZone ?? 'UTC';

  const client = new Anthropic({ apiKey });

  try {
    const response = await client.messages.create({
      model: MODEL,
      max_tokens: 8000,
      system: SYSTEM,
      output_config: {
        // Extraction from a short transcript does not need deep deliberation;
        // most of the difficulty is date arithmetic, which medium handles.
        effort: 'medium',
        format: { type: 'json_schema', schema: OUTPUT_SCHEMA },
      },
      messages: [
        {
          role: 'user',
          content: [
            `Recorded at: ${recordedAt}`,
            `Speaker's time zone: ${timeZone}`,
            body.language ? `Recognised language: ${body.language}` : '',
            '',
            'Transcript:',
            clipped,
          ]
            .filter(Boolean)
            .join('\n'),
        },
      ],
    });

    // Opus 5 can decline a request outright; that arrives as a 200 with a
    // refusal stop reason and empty content, so check before reading content.
    if (response.stop_reason === 'refusal') {
      return errorResponse('The assistant declined to process this note.', 422);
    }

    const text = response.content.find((block) => block.type === 'text');
    if (!text || text.type !== 'text') {
      return errorResponse('The assistant returned no usable content.', 502);
    }

    // Guaranteed to parse by the output schema, but a malformed response should
    // surface as a clean error rather than a stack trace.
    try {
      return json(JSON.parse(text.text));
    } catch {
      return errorResponse('The assistant returned malformed JSON.', 502);
    }
  } catch (err) {
    const message = err instanceof Error ? err.message : 'Unknown error';
    console.error('[enrich-note] failed', message);
    return errorResponse(`Enrichment failed: ${message}`, 502);
  }
});
