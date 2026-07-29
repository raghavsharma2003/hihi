import * as AuthSession from 'expo-auth-session';
import * as SecureStore from 'expo-secure-store';
import * as WebBrowser from 'expo-web-browser';
import { useCallback, useEffect, useState } from 'react';
import { Platform } from 'react-native';

// Completes the auth session when the browser redirects back into the app.
WebBrowser.maybeCompleteAuthSession();

const STORE_KEY = 'echo.google.tokens';

/**
 * `calendar.events` and `gmail.compose` are the narrowest scopes that still
 * allow Echo to create an event or a draft. `gmail.readonly` is what powers the
 * inbox digest; it is a restricted scope, so a production build needs Google's
 * verification review before it works for anyone outside the test users list.
 */
export const GOOGLE_SCOPES = [
  'openid',
  'profile',
  'email',
  'https://www.googleapis.com/auth/calendar.events',
  'https://www.googleapis.com/auth/calendar.readonly',
  'https://www.googleapis.com/auth/gmail.compose',
  'https://www.googleapis.com/auth/gmail.readonly',
];

export const googleDiscovery: AuthSession.DiscoveryDocument = {
  authorizationEndpoint: 'https://accounts.google.com/o/oauth2/v2/auth',
  tokenEndpoint: 'https://oauth2.googleapis.com/token',
  revocationEndpoint: 'https://oauth2.googleapis.com/revoke',
  userInfoEndpoint: 'https://openidconnect.googleapis.com/v1/userinfo',
};

interface StoredTokens {
  accessToken: string;
  refreshToken: string | null;
  /** Epoch ms. */
  expiresAt: number;
  email: string | null;
  scopes: string[];
}

function clientId(): string | undefined {
  if (Platform.OS === 'ios') return process.env.EXPO_PUBLIC_GOOGLE_IOS_CLIENT_ID;
  if (Platform.OS === 'android') return process.env.EXPO_PUBLIC_GOOGLE_ANDROID_CLIENT_ID;
  return process.env.EXPO_PUBLIC_GOOGLE_WEB_CLIENT_ID;
}

export function isGoogleConfigured(): boolean {
  return Boolean(clientId());
}

/**
 * Google's installed-app flow accepts the app's bundle id / package name as a
 * custom scheme. Using that (rather than the Expo proxy) keeps the flow working
 * in standalone builds, which is where it matters.
 */
export function googleRedirectUri(): string {
  return AuthSession.makeRedirectUri({
    native: 'com.echo.voicenotes:/oauthredirect',
    scheme: 'echo',
  });
}

// ── Token storage ───────────────────────────────────────────────────────────

async function readTokens(): Promise<StoredTokens | null> {
  try {
    const raw = await SecureStore.getItemAsync(STORE_KEY);
    return raw ? (JSON.parse(raw) as StoredTokens) : null;
  } catch {
    return null;
  }
}

async function writeTokens(tokens: StoredTokens | null): Promise<void> {
  try {
    if (tokens) await SecureStore.setItemAsync(STORE_KEY, JSON.stringify(tokens));
    else await SecureStore.deleteItemAsync(STORE_KEY);
  } catch (err) {
    console.warn('[echo] could not persist Google tokens', err);
  }
}

/**
 * Returns a usable access token, refreshing it first if it is within a minute
 * of expiry. Returns null when the user has not connected Google, or when the
 * refresh token has been revoked and they must reconnect.
 */
export async function getAccessToken(): Promise<string | null> {
  const stored = await readTokens();
  if (!stored) return null;

  if (Date.now() < stored.expiresAt - 60_000) return stored.accessToken;

  if (!stored.refreshToken) {
    // Nothing to refresh with — force a reconnect rather than failing every
    // subsequent API call with a confusing 401.
    await writeTokens(null);
    return null;
  }

  try {
    const refreshed = await AuthSession.refreshAsync(
      { clientId: clientId()!, refreshToken: stored.refreshToken },
      googleDiscovery,
    );

    const next: StoredTokens = {
      accessToken: refreshed.accessToken,
      // Google only re-issues a refresh token occasionally; keep the old one.
      refreshToken: refreshed.refreshToken ?? stored.refreshToken,
      expiresAt: Date.now() + (refreshed.expiresIn ?? 3600) * 1000,
      email: stored.email,
      scopes: stored.scopes,
    };
    await writeTokens(next);
    return next.accessToken;
  } catch (err) {
    console.warn('[echo] Google token refresh failed; disconnecting', err);
    await writeTokens(null);
    return null;
  }
}

export async function disconnectGoogle(): Promise<void> {
  const stored = await readTokens();
  if (stored?.accessToken) {
    try {
      await AuthSession.revokeAsync(
        { token: stored.accessToken, clientId: clientId()! },
        googleDiscovery,
      );
    } catch {
      // Revocation is best-effort: the local tokens are cleared either way.
    }
  }
  await writeTokens(null);
}

export interface GoogleConnection {
  configured: boolean;
  connected: boolean;
  email: string | null;
  connecting: boolean;
  error: string | null;
  connect: () => Promise<void>;
  disconnect: () => Promise<void>;
  refresh: () => Promise<void>;
}

export function useGoogleConnection(): GoogleConnection {
  const [tokens, setTokens] = useState<StoredTokens | null>(null);
  const [connecting, setConnecting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const configured = isGoogleConfigured();

  const reload = useCallback(async () => {
    setTokens(await readTokens());
  }, []);

  useEffect(() => {
    let active = true;
    void (async () => {
      const stored = await readTokens();
      if (active) setTokens(stored);
    })();
    return () => {
      active = false;
    };
  }, []);

  const [request, , promptAsync] = AuthSession.useAuthRequest(
    {
      clientId: clientId() ?? 'unconfigured',
      scopes: GOOGLE_SCOPES,
      redirectUri: googleRedirectUri(),
      responseType: AuthSession.ResponseType.Code,
      usePKCE: true,
      extraParams: {
        // Required to receive a refresh token, which is what lets Echo act on
        // a note hours later without sending the user back through consent.
        access_type: 'offline',
        prompt: 'consent',
      },
    },
    googleDiscovery,
  );

  const connect = useCallback(async () => {
    if (!configured) {
      setError('No Google client ID is configured. Add one to .env and restart the app.');
      return;
    }
    if (!request) return;

    setConnecting(true);
    setError(null);

    try {
      const result = await promptAsync();
      if (result.type !== 'success' || !result.params.code) {
        if (result.type === 'error') setError(result.params.error_description ?? 'Sign-in failed.');
        return;
      }

      const exchanged = await AuthSession.exchangeCodeAsync(
        {
          clientId: clientId()!,
          code: result.params.code,
          redirectUri: googleRedirectUri(),
          extraParams: request.codeVerifier ? { code_verifier: request.codeVerifier } : undefined,
        },
        googleDiscovery,
      );

      // Fetch the address so Settings can show which account is connected.
      let email: string | null = null;
      try {
        const profile = await fetch(googleDiscovery.userInfoEndpoint!, {
          headers: { Authorization: `Bearer ${exchanged.accessToken}` },
        });
        if (profile.ok) email = ((await profile.json()) as { email?: string }).email ?? null;
      } catch {
        // Not fatal — the connection works without knowing the address.
      }

      const next: StoredTokens = {
        accessToken: exchanged.accessToken,
        refreshToken: exchanged.refreshToken ?? null,
        expiresAt: Date.now() + (exchanged.expiresIn ?? 3600) * 1000,
        email,
        scopes: GOOGLE_SCOPES,
      };
      await writeTokens(next);
      setTokens(next);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Could not connect to Google.');
    } finally {
      setConnecting(false);
    }
  }, [configured, promptAsync, request]);

  const disconnect = useCallback(async () => {
    await disconnectGoogle();
    setTokens(null);
  }, []);

  return {
    configured,
    connected: Boolean(tokens),
    email: tokens?.email ?? null,
    connecting,
    error,
    connect,
    disconnect,
    refresh: reload,
  };
}
