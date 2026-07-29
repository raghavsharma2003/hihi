# Echo

A voice-first notes app for iOS and Android. Talk, and Echo keeps **both** halves
of what you said — the recording and the text — then pulls out the things you
actually need to do and puts them on your calendar.

Built with Expo (React Native), SQLite on-device, and Supabase for sync and the
assistant.

---

## What it does

**Record by talking.** One tap from any screen. The transcript streams in live as
you speak, with a waveform that moves with your voice, so you can see it is
working without stopping to check.

**Both formats, always.** Every note keeps the original audio *and* the
transcript. Play the recording back with a waveform scrubber, or tap any phrase
in the transcript to jump to that exact moment. Correct the text by hand if the
recogniser mis-heard a name — your edit is never overwritten.

**It reads your notes.** Claude turns each note into a real title, a short
summary, and a list of the commitments buried in it. "Call Priya tomorrow at
ten" becomes a calendar event with the time already resolved.

**Calendar and mail.** Connect Google and Echo shows your next day and a half,
surfaces unread mail, and turns extracted actions into real calendar events and
Gmail drafts with one tap.

**Works with nothing configured.** Recording, transcription, search, playback and
editing are all on-device. Supabase adds sync, audio backup and the assistant.
Google adds calendar and mail. Each is independent and optional.

---

## Quick start

```bash
npm install
cp .env.example .env      # every value is optional — see below
npx expo start
```

The app needs a **development build**, not Expo Go: speech recognition and audio
recording are native modules.

```bash
npx expo run:ios          # or: npx expo run:android
```

With an empty `.env` you get the full local experience — record, transcribe,
search, play back, edit. The two sections below turn on everything else.

---

## Turning on sync and the assistant

Create a Supabase project, then:

```bash
./scripts/setup-supabase.sh <project-ref>
```

That links the repo, pushes the schema and row-level-security policies, creates
the private `recordings` bucket, and deploys both edge functions.

Then give the assistant a key and point the app at the project:

```bash
supabase secrets set ANTHROPIC_API_KEY=sk-ant-...
```

```dotenv
# .env
EXPO_PUBLIC_SUPABASE_URL=https://<project-ref>.supabase.co
EXPO_PUBLIC_SUPABASE_ANON_KEY=<anon / publishable key>
```

Restart the dev server after editing `.env` — `EXPO_PUBLIC_` variables are
inlined at build time.

Sign in from **Settings → Sync & assistant**. Echo emails a six-digit code; there
is no password and no magic-link deep-link plumbing.

### Optional: server-side transcription fallback

On-device recognition covers almost everything, but it needs a network on some
Android devices and does not support every locale. If you want a fallback for
those cases:

```bash
supabase secrets set OPENAI_API_KEY=sk-...
```

Without it, a note whose recognition failed keeps its audio and an empty,
editable transcript.

---

## Turning on calendar and mail

In the [Google Cloud Console](https://console.cloud.google.com/apis/credentials),
enable the **Google Calendar API** and **Gmail API**, then create an OAuth 2.0
client for each platform you build:

| Platform | Client type | Redirect / identifier |
| --- | --- | --- |
| iOS | iOS | Bundle ID `com.echo.voicenotes` |
| Android | Android | Package `com.echo.voicenotes` + your signing SHA-1 |
| Web / Expo Go | Web application | `https://auth.expo.io/@<you>/echo-voice-notes` |

```dotenv
EXPO_PUBLIC_GOOGLE_IOS_CLIENT_ID=...apps.googleusercontent.com
EXPO_PUBLIC_GOOGLE_ANDROID_CLIENT_ID=...apps.googleusercontent.com
EXPO_PUBLIC_GOOGLE_WEB_CLIENT_ID=...apps.googleusercontent.com
```

Connect from **Settings → Calendar & mail**.

> **Before you ship:** `gmail.readonly` (the inbox digest) and `gmail.compose`
> (drafts) are *restricted* scopes. They work immediately for accounts you add
> as test users on the OAuth consent screen, but reaching real users requires
> Google's verification review. Calendar scopes are not restricted.
>
> Echo never sends mail. It only creates drafts, which you review and send
> yourself.

---

## How it is put together

```
app/                        Screens (expo-router, file-based)
  (tabs)/
    index.tsx               Notes list — grouped by day, swipe to pin/archive
    today.tsx               Agenda: calendar + open action items
    inbox.tsx               Unread mail digest
    settings.tsx            Connections, storage, archive
  capture.tsx               The recorder
  note/[id].tsx             Playback, transcript, action items
  archive.tsx

src/
  capture/                  Recording + live transcription engine
  components/               UI kit and screen-level components
  db/                       SQLite schema, repository, reactive hooks
  services/                 Supabase, sync, Google, assistant orchestration
  theme/                    Design tokens
  utils/

supabase/
  migrations/               Schema, RLS, storage bucket
  functions/
    enrich-note/            Claude — title, summary, action items
    transcribe-audio/       Optional Whisper fallback
```

### Local-first, by design

A note is written to on-device SQLite the instant you stop talking, and is fully
usable from that moment — searchable, playable, editable. Everything after that
(assistant enrichment, cloud sync, audio upload) is a background job that
retries with backoff and never blocks the interface.

That is what makes the app usable on a train with no signal, and it is why the
device generates note IDs rather than the server: a note has to exist and be
editable before it has ever touched the network.

**Conflict resolution.** Sync is last-write-wins on `updated_at`, with one
exception: a local edit that has not been pushed yet always beats the server
copy, because it is the most recent thing the user actually did.

### One microphone, two outputs

Recording and transcription come from a *single* capture session rather than a
recorder and a recogniser running side by side. Two components contending for
the microphone fails on both platforms — iOS audio sessions are exclusive, and
on Android the second opener gets silence. `expo-speech-recognition` persists
the audio while it recognises, which gives both outputs from one stream.

On Android the recogniser still ends a session after a long silence, so the
capture engine transparently restarts it and offsets the new session's segment
timings — a pause mid-thought does not truncate the note.

### Where your data lives

Audio and transcripts are on the device. They leave it only if you sign in to
sync (your own Supabase project, private storage bucket, RLS scoped to your user
id, signed URLs only) or connect Google to create an event or draft.

The Anthropic key lives in a Supabase secret and is used from an edge function,
so it is never in the app bundle.

---

## Design notes

The palette gives each accent exactly one meaning, which is what lets a glance
read state without a label: **ember** is live voice and nothing else — the
record button, the waveform, the recording pulse. **Sage** is machine-authored
content — summaries, extracted actions, suggestions. **Gold** is pinned.

Type is split between a serif for anything the user authored or the app presents
as *writing* (titles, transcripts) and a sans for chrome (buttons, tabs,
labels). A screen full of text reads like a note rather than a settings panel.

Recording occupies the centre of the tab bar rather than a corner, so it is
reachable with either thumb from any screen at the moment a thought arrives.

---

## Commands

```bash
npm start              # dev server
npm run ios            # build and run on iOS
npm run android        # build and run on Android
npm run typecheck      # tsc --noEmit
npm run db:push        # push migrations
npm run fn:deploy      # deploy edge functions
```

---

## Known constraints

- **`expo-speech-recognition` is published for SDK 56**; this project is on SDK
  57. It bundles and its native API surface is stable, but it is the one
  dependency to re-check when upgrading. Pin it deliberately.
- **Speech recognition needs a development build.** It does not work in Expo Go.
- **Gmail scopes need Google verification** before non-test users can connect
  (see above).
- **Segment-level timings** (tap a phrase to seek) come from the platform
  recogniser: always available on iOS, and on Android only on API 34+ with
  on-device recognition. Where they are missing, the transcript renders as plain
  text and playback still works.
