/**
 * Shared HTTP plumbing for Echo's edge functions.
 */

export const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
};

export function json(body: unknown, status = 200): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: { ...corsHeaders, 'Content-Type': 'application/json' },
  });
}

export function preflight(): Response {
  return new Response('ok', { headers: corsHeaders });
}

export function errorResponse(message: string, status = 400): Response {
  return json({ error: message }, status);
}

/**
 * Every function here is called by a signed-in device. Requiring the caller's
 * JWT means a leaked anon key alone cannot spend the project's model budget.
 */
export function requireAuthHeader(request: Request): string | null {
  const header = request.headers.get('Authorization');
  if (!header?.startsWith('Bearer ')) return null;
  const token = header.slice('Bearer '.length).trim();
  return token.length > 0 ? token : null;
}
