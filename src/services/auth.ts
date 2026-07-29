import type { Session } from '@supabase/supabase-js';
import { useCallback, useEffect, useState } from 'react';

import { supabase } from './supabase';

export interface AuthState {
  configured: boolean;
  session: Session | null;
  email: string | null;
  loading: boolean;
  /** Set once a code has been sent and we are waiting for the user to type it. */
  awaitingCode: boolean;
  error: string | null;
  sendCode: (email: string) => Promise<void>;
  verifyCode: (code: string) => Promise<void>;
  cancelCode: () => void;
  signOut: () => Promise<void>;
}

/**
 * Email one-time codes rather than magic links: a six-digit code works the same
 * whether the user opens their mail on this phone or another device, and it
 * needs no deep-link plumbing or extra provider setup.
 */
export function useSupabaseAuth(): AuthState {
  const [session, setSession] = useState<Session | null>(null);
  // With no backend there is no session to look up, so this is never loading.
  const [loading, setLoading] = useState(() => supabase !== null);
  const [pendingEmail, setPendingEmail] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!supabase) return;

    void supabase.auth.getSession().then(({ data }) => {
      setSession(data.session);
      setLoading(false);
    });

    const { data: subscription } = supabase.auth.onAuthStateChange((_event, next) => {
      setSession(next);
      if (next) setPendingEmail(null);
    });

    return () => subscription.subscription.unsubscribe();
  }, []);

  const sendCode = useCallback(async (email: string) => {
    if (!supabase) return;
    setError(null);
    const trimmed = email.trim();

    const { error: sendError } = await supabase.auth.signInWithOtp({
      email: trimmed,
      options: { shouldCreateUser: true },
    });

    if (sendError) {
      setError(sendError.message);
      return;
    }
    setPendingEmail(trimmed);
  }, []);

  const verifyCode = useCallback(
    async (code: string) => {
      if (!supabase || !pendingEmail) return;
      setError(null);

      const { error: verifyError } = await supabase.auth.verifyOtp({
        email: pendingEmail,
        token: code.trim(),
        type: 'email',
      });

      if (verifyError) {
        setError(verifyError.message);
        return;
      }
      setPendingEmail(null);
    },
    [pendingEmail],
  );

  const signOut = useCallback(async () => {
    if (!supabase) return;
    await supabase.auth.signOut();
    setSession(null);
  }, []);

  return {
    configured: supabase !== null,
    session,
    email: session?.user.email ?? null,
    loading,
    awaitingCode: pendingEmail !== null,
    error,
    sendCode,
    verifyCode,
    cancelCode: () => setPendingEmail(null),
    signOut,
  };
}
