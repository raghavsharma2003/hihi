import { createClient } from 'npm:@supabase/supabase-js@2';

import { errorResponse, json, preflight, requireAuthHeader } from '../_shared/http.ts';

/**
 * Fallback transcription for the cases on-device recognition cannot cover:
 * the recogniser needed a network it did not have, the locale is not installed,
 * or recording was interrupted before any words were committed.
 *
 * Optional. Without OPENAI_API_KEY this returns 503 and the app keeps the note
 * exactly as it is — audio saved, transcript empty and editable by hand.
 */

const WHISPER_ENDPOINT = 'https://api.openai.com/v1/audio/transcriptions';

interface RequestBody {
  /** Storage path in the `recordings` bucket, "<user-id>/<note-id>.wav". */
  audioPath?: string;
  language?: string;
}

Deno.serve(async (request: Request) => {
  if (request.method === 'OPTIONS') return preflight();
  if (request.method !== 'POST') return errorResponse('Use POST.', 405);

  const token = requireAuthHeader(request);
  if (!token) return errorResponse('Missing Authorization header.', 401);

  const openaiKey = Deno.env.get('OPENAI_API_KEY');
  if (!openaiKey) {
    return errorResponse(
      'OPENAI_API_KEY is not set, so server-side transcription is disabled.',
      503,
    );
  }

  let body: RequestBody;
  try {
    body = (await request.json()) as RequestBody;
  } catch {
    return errorResponse('Body must be JSON.');
  }

  if (!body.audioPath) return errorResponse('audioPath is required.');

  // Download through the caller's own token so storage RLS still applies — the
  // service role key is never used to read a user's recording.
  const supabase = createClient(
    Deno.env.get('SUPABASE_URL')!,
    Deno.env.get('SUPABASE_ANON_KEY')!,
    { global: { headers: { Authorization: `Bearer ${token}` } } },
  );

  const { data: file, error: downloadError } = await supabase.storage
    .from('recordings')
    .download(body.audioPath);

  if (downloadError || !file) {
    return errorResponse(`Could not read the recording: ${downloadError?.message ?? 'not found'}`, 404);
  }

  const form = new FormData();
  form.append('file', file, body.audioPath.split('/').pop() ?? 'audio.wav');
  form.append('model', 'whisper-1');
  form.append('response_format', 'json');
  if (body.language) {
    // Whisper expects a bare ISO-639-1 code, not the BCP-47 tag the recogniser uses.
    form.append('language', body.language.split('-')[0]);
  }

  try {
    const response = await fetch(WHISPER_ENDPOINT, {
      method: 'POST',
      headers: { Authorization: `Bearer ${openaiKey}` },
      body: form,
    });

    if (!response.ok) {
      const detail = await response.text();
      return errorResponse(`Transcription failed: ${detail.slice(0, 300)}`, 502);
    }

    const result = (await response.json()) as { text?: string };
    return json({ transcript: result.text ?? '' });
  } catch (err) {
    const message = err instanceof Error ? err.message : 'Unknown error';
    return errorResponse(`Transcription failed: ${message}`, 502);
  }
});
