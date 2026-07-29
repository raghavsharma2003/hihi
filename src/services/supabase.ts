import AsyncStorage from '@react-native-async-storage/async-storage';
import { createClient, type SupabaseClient } from '@supabase/supabase-js';
import 'react-native-url-polyfill/auto';

const url = process.env.EXPO_PUBLIC_SUPABASE_URL;
const anonKey = process.env.EXPO_PUBLIC_SUPABASE_ANON_KEY;

/**
 * Echo is local-first: recording, transcription, search and playback all work
 * with no backend at all. Supabase adds cross-device sync, audio backup and the
 * assistant. Every caller therefore has to handle a null client rather than
 * assume one exists.
 */
export const supabase: SupabaseClient | null =
  url && anonKey
    ? createClient(url, anonKey, {
        auth: {
          storage: AsyncStorage,
          autoRefreshToken: true,
          persistSession: true,
          // There is no URL to parse a session out of in a native app.
          detectSessionInUrl: false,
        },
      })
    : null;

export function isBackendConfigured(): boolean {
  return supabase !== null;
}

/**
 * Enrichment runs in an edge function, so it needs the same backend. Kept as a
 * separate predicate because the two could diverge later (a user could have
 * sync without the assistant).
 */
export function isAiConfigured(): boolean {
  return supabase !== null;
}

export class BackendUnavailableError extends Error {
  constructor() {
    super('No Supabase project is configured.');
    this.name = 'BackendUnavailableError';
  }
}

/** Signed-in user id, or null when signed out or running without a backend. */
export async function currentUserId(): Promise<string | null> {
  if (!supabase) return null;
  const { data } = await supabase.auth.getUser();
  return data.user?.id ?? null;
}

/**
 * Calls a Supabase edge function with the caller's session attached.
 * Throws `BackendUnavailableError` when there is nothing to call.
 */
export async function invokeFunction<T>(
  name: string,
  body: Record<string, unknown>,
): Promise<T> {
  if (!supabase) throw new BackendUnavailableError();

  const { data, error } = await supabase.functions.invoke<T>(name, { body });
  if (error) throw error;
  if (data === null) throw new Error(`Edge function "${name}" returned no data.`);
  return data;
}
