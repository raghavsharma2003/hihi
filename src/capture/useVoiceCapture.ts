import {
  ExpoSpeechRecognitionModule,
  useSpeechRecognitionEvent,
  type ExpoSpeechRecognitionErrorCode,
} from 'expo-speech-recognition';
import { useCallback, useEffect, useRef, useState } from 'react';
import { Platform } from 'react-native';
import { useSharedValue, type SharedValue } from 'react-native-reanimated';

import { recordingsDirectoryUri } from './storage';

export type CaptureStatus =
  | 'idle'
  | 'starting'
  | 'listening'
  | 'stopping'
  /** Recording ended; the file and final transcript are ready. */
  | 'done'
  | 'error';

export interface CaptureSegment {
  startMs: number;
  endMs: number;
  text: string;
}

export interface CaptureResult {
  transcript: string;
  audioUri: string | null;
  durationMs: number;
  amplitudes: number[];
  segments: CaptureSegment[];
  language: string;
}

/** Bars kept on screen in the live waveform. */
const TRAIL_LENGTH = 42;
/** Volume sampling cadence. Fast enough to look live, slow enough to be cheap. */
const VOLUME_INTERVAL_MS = 100;
/** Amplitude samples stored per second on the saved waveform. */
const STORED_SAMPLE_INTERVAL_MS = 250;

/**
 * Maps the recogniser's -2..10 volume scale onto 0..1.
 *
 * The raw scale is heavily bottom-weighted — ordinary speech sits around 1-4 —
 * so a linear map leaves the waveform nearly flat. The square root expands that
 * low end, which is the range the user is actually in.
 */
function normalizeVolume(value: number): number {
  const clamped = Math.max(0, Math.min(8, value));
  return Math.sqrt(clamped / 8);
}

function joinTranscript(chunks: string[], interim: string): string {
  return [...chunks, interim]
    .map((part) => part.trim())
    .filter(Boolean)
    .join(' ')
    .replace(/\s+/g, ' ')
    .trim();
}

export interface VoiceCapture {
  status: CaptureStatus;
  /** Everything recognised so far, including the in-flight phrase. */
  transcript: string;
  /** The phrase currently being recognised, not yet committed. */
  interim: string;
  durationMs: number;
  /** Amplitude trail for the live waveform. */
  trail: number[];
  /** Live microphone level, driven on the UI thread. */
  level: SharedValue<number>;
  error: string | null;
  /** True while the user is speaking, as opposed to merely recording silence. */
  speaking: boolean;

  start: (language?: string) => Promise<void>;
  /** Resolves once the final transcript and audio file are both available. */
  stop: () => Promise<CaptureResult | null>;
  /** Throws the recording away. */
  cancel: () => void;
  reset: () => void;
}

/**
 * Runs one recording session: live transcription and a persisted audio file
 * from a single microphone stream.
 *
 * The two outputs come from the same recogniser rather than a parallel recorder,
 * because two components contending for the microphone fails on both platforms —
 * on iOS the audio session is exclusive, and on Android the second opener gets
 * silence.
 */
export function useVoiceCapture(): VoiceCapture {
  const [status, setStatus] = useState<CaptureStatus>('idle');
  const [interim, setInterim] = useState('');
  const [committed, setCommitted] = useState<string[]>([]);
  const [durationMs, setDurationMs] = useState(0);
  const [trail, setTrail] = useState<number[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [speaking, setSpeaking] = useState(false);

  const level = useSharedValue(0);

  // Refs hold everything the native event handlers touch. Handlers are
  // registered once and must not close over stale state.
  const startedAtRef = useRef(0);
  const committedRef = useRef<string[]>([]);
  const segmentsRef = useRef<CaptureSegment[]>([]);
  const amplitudesRef = useRef<number[]>([]);
  const lastStoredSampleRef = useRef(0);
  const audioUriRef = useRef<string | null>(null);
  const languageRef = useRef('en-US');

  /** Elapsed ms when the current recogniser session began, so segment
   *  timestamps stay absolute across continuous-mode restarts. */
  const sessionOffsetRef = useRef(0);
  /** True from the moment the user asks to stop until finalisation completes. */
  const stoppingRef = useRef(false);
  /** True while a session should be running — drives auto-restart on Android. */
  const wantsListeningRef = useRef(false);
  /** Consecutive auto-restarts, to avoid a restart storm on a broken recogniser. */
  const restartCountRef = useRef(0);

  const finalizeRef = useRef<((result: CaptureResult | null) => void) | null>(null);
  const audioEndedRef = useRef(false);
  const recognitionEndedRef = useRef(false);

  const tickRef = useRef<ReturnType<typeof setInterval> | null>(null);

  const clearTick = useCallback(() => {
    if (tickRef.current) {
      clearInterval(tickRef.current);
      tickRef.current = null;
    }
  }, []);

  const resetSessionState = useCallback(() => {
    committedRef.current = [];
    segmentsRef.current = [];
    amplitudesRef.current = [];
    lastStoredSampleRef.current = 0;
    audioUriRef.current = null;
    sessionOffsetRef.current = 0;
    restartCountRef.current = 0;
    audioEndedRef.current = false;
    recognitionEndedRef.current = false;
    stoppingRef.current = false;
    wantsListeningRef.current = false;
    setCommitted([]);
    setInterim('');
    setTrail([]);
    setDurationMs(0);
    setSpeaking(false);
    level.value = 0;
  }, [level]);

  /**
   * Resolves the pending `stop()` once both the recogniser and the audio writer
   * have reported in. Waiting for only one of them yields either a truncated
   * transcript or a zero-byte file.
   */
  const tryFinalize = useCallback(() => {
    if (!finalizeRef.current) return;
    if (!recognitionEndedRef.current) return;
    // `audioend` never fires if the session failed before audio started.
    if (!audioEndedRef.current && audioUriRef.current !== null) return;

    const resolve = finalizeRef.current;
    finalizeRef.current = null;
    clearTick();

    const elapsed = startedAtRef.current > 0 ? Date.now() - startedAtRef.current : 0;
    const transcript = joinTranscript(committedRef.current, '');

    level.value = 0;
    setStatus('done');
    setSpeaking(false);

    resolve({
      transcript,
      audioUri: audioUriRef.current,
      durationMs: elapsed,
      amplitudes: amplitudesRef.current.slice(),
      segments: segmentsRef.current.slice(),
      language: languageRef.current,
    });
  }, [clearTick, level]);

  // ── Native events ─────────────────────────────────────────────────────────

  useSpeechRecognitionEvent('start', () => {
    restartCountRef.current = 0;
    setStatus('listening');
  });

  useSpeechRecognitionEvent('audiostart', (event) => {
    if (event.uri) audioUriRef.current = event.uri;
  });

  useSpeechRecognitionEvent('audioend', (event) => {
    if (event.uri) audioUriRef.current = event.uri;
    audioEndedRef.current = true;
    tryFinalize();
  });

  useSpeechRecognitionEvent('speechstart', () => setSpeaking(true));
  useSpeechRecognitionEvent('speechend', () => setSpeaking(false));

  useSpeechRecognitionEvent('result', (event) => {
    const best = event.results[0];
    if (!best) return;

    if (event.isFinal) {
      const text = best.transcript.trim();
      if (text) {
        committedRef.current = [...committedRef.current, text];
        setCommitted(committedRef.current);
      }

      // Segment timings are relative to the current recogniser session; shift
      // them so tap-to-seek lines up with the single continuous audio file.
      for (const seg of best.segments ?? []) {
        const segText = seg.segment.trim();
        if (!segText) continue;
        segmentsRef.current.push({
          startMs: sessionOffsetRef.current + seg.startTimeMillis,
          endMs: sessionOffsetRef.current + seg.endTimeMillis,
          text: segText,
        });
      }

      setInterim('');
    } else {
      setInterim(best.transcript);
    }
  });

  useSpeechRecognitionEvent('volumechange', (event) => {
    const amplitude = normalizeVolume(event.value);
    level.value = amplitude;

    setTrail((prev) => {
      const next = prev.length >= TRAIL_LENGTH ? prev.slice(1) : prev.slice();
      next.push(amplitude);
      return next;
    });

    // The stored waveform is sampled more coarsely than the live one — it only
    // needs enough resolution to be recognisable at thumbnail size.
    const now = Date.now();
    if (now - lastStoredSampleRef.current >= STORED_SAMPLE_INTERVAL_MS) {
      lastStoredSampleRef.current = now;
      amplitudesRef.current.push(amplitude);
    }
  });

  useSpeechRecognitionEvent('end', () => {
    // On Android, continuous mode still ends the session after a long silence.
    // If the user has not asked to stop, transparently start another one so a
    // pause mid-thought does not truncate the note.
    if (wantsListeningRef.current && !stoppingRef.current && restartCountRef.current < 12) {
      restartCountRef.current += 1;
      sessionOffsetRef.current = Date.now() - startedAtRef.current;
      try {
        ExpoSpeechRecognitionModule.start({
          lang: languageRef.current,
          interimResults: true,
          continuous: true,
          addsPunctuation: true,
          volumeChangeEventOptions: { enabled: true, intervalMillis: VOLUME_INTERVAL_MS },
          // Audio already began in the first session; asking to persist again
          // would open a second writer and truncate the first file.
          recordingOptions: { persist: false },
        });
        return;
      } catch {
        // Fall through to finalisation below.
      }
    }

    recognitionEndedRef.current = true;
    wantsListeningRef.current = false;
    tryFinalize();
  });

  useSpeechRecognitionEvent('error', (event) => {
    // "no-speech" during a pause is expected in continuous mode, and the `end`
    // handler will restart the session — surfacing it would be noise.
    if (event.error === 'no-speech' && wantsListeningRef.current && !stoppingRef.current) {
      return;
    }
    // The user cancelled; `cancel()` already tore state down.
    if (event.error === 'aborted') return;

    setError(describeError(event.error, event.message));
    wantsListeningRef.current = false;
    recognitionEndedRef.current = true;
    setStatus('error');
    clearTick();
    tryFinalize();
  });

  // ── Controls ──────────────────────────────────────────────────────────────

  const start = useCallback(
    async (language = 'en-US') => {
      setError(null);
      setStatus('starting');
      resetSessionState();
      languageRef.current = language;

      const permission = await ExpoSpeechRecognitionModule.requestPermissionsAsync();
      if (!permission.granted) {
        setError(
          'Echo needs microphone and speech recognition access to take voice notes. You can grant it in Settings.',
        );
        setStatus('error');
        return;
      }

      startedAtRef.current = Date.now();
      lastStoredSampleRef.current = Date.now();
      wantsListeningRef.current = true;

      try {
        ExpoSpeechRecognitionModule.start({
          lang: language,
          interimResults: true,
          continuous: true,
          addsPunctuation: true,
          volumeChangeEventOptions: { enabled: true, intervalMillis: VOLUME_INTERVAL_MS },
          recordingOptions: {
            persist: true,
            outputDirectory: recordingsDirectoryUri(),
            outputFileName: `capture_${startedAtRef.current}.wav`,
          },
          // Android's default recogniser stops aggressively on silence; these
          // give the user room to think mid-note.
          androidIntentOptions: {
            EXTRA_SPEECH_INPUT_COMPLETE_SILENCE_LENGTH_MILLIS: 4000,
            EXTRA_SPEECH_INPUT_POSSIBLY_COMPLETE_SILENCE_LENGTH_MILLIS: 4000,
          },
          iosCategory: {
            category: 'playAndRecord',
            categoryOptions: ['defaultToSpeaker', 'allowBluetooth'],
            mode: 'measurement',
          },
        });
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Could not start recording.');
        setStatus('error');
        wantsListeningRef.current = false;
        return;
      }

      clearTick();
      tickRef.current = setInterval(() => {
        setDurationMs(Date.now() - startedAtRef.current);
      }, 200);
    },
    [clearTick, resetSessionState],
  );

  const stop = useCallback((): Promise<CaptureResult | null> => {
    if (!wantsListeningRef.current && status !== 'listening') {
      return Promise.resolve(null);
    }

    stoppingRef.current = true;
    wantsListeningRef.current = false;
    setStatus('stopping');
    setDurationMs(Date.now() - startedAtRef.current);

    return new Promise<CaptureResult | null>((resolve) => {
      finalizeRef.current = resolve;
      try {
        ExpoSpeechRecognitionModule.stop();
      } catch {
        recognitionEndedRef.current = true;
        audioEndedRef.current = true;
        tryFinalize();
      }

      // The recogniser occasionally never emits `end` — most often when it is
      // stopped during a network round-trip. Resolve with what we have rather
      // than leaving the user on a spinner with an unsaved note.
      setTimeout(() => {
        if (finalizeRef.current) {
          recognitionEndedRef.current = true;
          audioEndedRef.current = true;
          tryFinalize();
        }
      }, 4000);
    });
  }, [status, tryFinalize]);

  const cancel = useCallback(() => {
    wantsListeningRef.current = false;
    stoppingRef.current = true;
    finalizeRef.current = null;
    try {
      ExpoSpeechRecognitionModule.abort();
    } catch {
      // Already stopped.
    }
    clearTick();
    resetSessionState();
    setStatus('idle');
  }, [clearTick, resetSessionState]);

  const reset = useCallback(() => {
    clearTick();
    resetSessionState();
    setError(null);
    setStatus('idle');
  }, [clearTick, resetSessionState]);

  // Never leave the microphone open behind a unmounted screen.
  useEffect(
    () => () => {
      clearTick();
      if (wantsListeningRef.current) {
        try {
          ExpoSpeechRecognitionModule.abort();
        } catch {
          // Nothing to release.
        }
      }
    },
    [clearTick],
  );

  return {
    status,
    transcript: joinTranscript(committed, interim),
    interim,
    durationMs,
    trail,
    level,
    error,
    speaking,
    start,
    stop,
    cancel,
    reset,
  };
}

function describeError(code: ExpoSpeechRecognitionErrorCode, message: string): string {
  switch (code) {
    case 'not-allowed':
    case 'service-not-allowed':
      return 'Microphone or speech recognition permission was denied. Enable it in Settings to record.';
    case 'network':
      return 'Speech recognition needs a network connection on this device. Your audio is still being recorded.';
    case 'language-not-supported':
      return 'This language is not available for speech recognition on this device.';
    case 'audio-capture':
      return 'The microphone is unavailable. Close other apps that may be using it and try again.';
    case 'busy':
      return 'The speech recogniser is busy. Try again in a moment.';
    case 'interrupted':
      return 'Recording was interrupted by another app or a call.';
    case 'speech-timeout':
    case 'no-speech':
      return 'No speech was detected.';
    default:
      return message || 'Recording failed. Please try again.';
  }
}

/** Whether speech recognition can run at all on this device. */
export function isRecognitionAvailable(): boolean {
  try {
    return ExpoSpeechRecognitionModule.isRecognitionAvailable();
  } catch {
    return Platform.OS !== 'web';
  }
}
