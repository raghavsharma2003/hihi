#!/usr/bin/env bash
#
# Links this repo to a Supabase project and pushes everything Echo needs:
# the schema, row level security, the private recordings bucket, and both
# edge functions.
#
# Usage:
#   ./scripts/setup-supabase.sh <project-ref>
#
# Find <project-ref> in your Supabase dashboard URL:
#   https://supabase.com/dashboard/project/<project-ref>

set -euo pipefail

PROJECT_REF="${1:-}"

if [[ -z "$PROJECT_REF" ]]; then
  echo "Usage: $0 <project-ref>" >&2
  echo "Find it in your dashboard URL: supabase.com/dashboard/project/<project-ref>" >&2
  exit 1
fi

if ! command -v supabase >/dev/null 2>&1; then
  echo "The Supabase CLI is not installed." >&2
  echo "  brew install supabase/tap/supabase   # macOS" >&2
  echo "  npm i -g supabase                    # anywhere" >&2
  exit 1
fi

echo "▸ Linking to $PROJECT_REF…"
supabase link --project-ref "$PROJECT_REF"

echo "▸ Pushing schema, RLS policies and the recordings bucket…"
supabase db push

echo "▸ Deploying edge functions…"
supabase functions deploy enrich-note
supabase functions deploy transcribe-audio

cat <<'EOF'

✓ Backend is live.

Two things left:

1. Give the assistant a key (required for summaries and action items):

     supabase secrets set ANTHROPIC_API_KEY=sk-ant-...

   Optional server-side transcription fallback, for when on-device
   recognition cannot run:

     supabase secrets set OPENAI_API_KEY=sk-...

2. Point the app at the project. In .env:

     EXPO_PUBLIC_SUPABASE_URL=https://<project-ref>.supabase.co
     EXPO_PUBLIC_SUPABASE_ANON_KEY=<anon/publishable key>

   Both are under Project Settings → API. Restart the dev server after
   editing .env — EXPO_PUBLIC_ vars are inlined at build time.

EOF
