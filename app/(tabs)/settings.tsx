import { Ionicons } from '@expo/vector-icons';
import Constants from 'expo-constants';
import { useRouter } from 'expo-router';
import React, { useCallback, useState } from 'react';
import { Alert, Pressable, ScrollView, TextInput, View } from 'react-native';

import { Button } from '@/components/Button';
import { Card, Divider, Screen, Tag } from '@/components/Layout';
import { Text } from '@/components/Text';
import { formatBytes, totalRecordingBytes } from '@/capture/storage';
import { useNotes } from '@/db/hooks';
import { useSupabaseAuth } from '@/services/auth';
import { useGoogleConnection } from '@/services/googleAuth';
import { isBackendConfigured } from '@/services/supabase';
import { runSyncCycle } from '@/services/sync';
import { useTheme } from '@/theme';

function Row({
  icon,
  title,
  detail,
  right,
  onPress,
}: {
  icon: keyof typeof Ionicons.glyphMap;
  title: string;
  detail?: string;
  right?: React.ReactNode;
  onPress?: () => void;
}) {
  const theme = useTheme();
  const content = (
    <View
      style={{
        flexDirection: 'row',
        alignItems: 'center',
        gap: theme.space.md,
        paddingVertical: theme.space.md,
      }}
    >
      <Ionicons name={icon} size={19} color={theme.color.textMuted} />
      <View style={{ flex: 1, gap: 2 }}>
        <Text variant="ui">{title}</Text>
        {detail ? (
          <Text variant="caption" tone="faint" numberOfLines={2}>
            {detail}
          </Text>
        ) : null}
      </View>
      {right}
      {onPress ? <Ionicons name="chevron-forward" size={16} color={theme.color.textFaint} /> : null}
    </View>
  );

  if (!onPress) return content;
  return (
    <Pressable
      accessibilityRole="button"
      accessibilityLabel={title}
      accessibilityHint={detail}
      onPress={onPress}
      style={({ pressed }) => ({ opacity: pressed ? 0.6 : 1 })}
    >
      {content}
    </Pressable>
  );
}

function SectionTitle({ children }: { children: string }) {
  const theme = useTheme();
  return (
    <Text
      variant="overline"
      tone="faint"
      style={{ marginTop: theme.space.xl, marginBottom: theme.space.sm }}
    >
      {children}
    </Text>
  );
}

export default function SettingsScreen() {
  const theme = useTheme();
  const router = useRouter();
  const auth = useSupabaseAuth();
  const google = useGoogleConnection();
  const { data: archived } = useNotes(undefined, true);

  const [emailInput, setEmailInput] = useState('');
  const [codeInput, setCodeInput] = useState('');
  const [syncing, setSyncing] = useState(false);
  const [storageBytes, setStorageBytes] = useState(() => totalRecordingBytes());

  const handleSyncNow = useCallback(async () => {
    setSyncing(true);
    try {
      await runSyncCycle();
    } finally {
      setSyncing(false);
      setStorageBytes(totalRecordingBytes());
    }
  }, []);

  return (
    <Screen>
      <View style={{ paddingHorizontal: theme.space.lg, paddingTop: theme.space.sm }}>
        <Text variant="display">Settings</Text>
      </View>

      <ScrollView
        contentContainerStyle={{
          paddingHorizontal: theme.space.lg,
          paddingBottom: theme.space.xxxl,
        }}
        showsVerticalScrollIndicator={false}
        keyboardShouldPersistTaps="handled"
      >
        {/* ── Cloud sync ───────────────────────────────────────────────── */}
        <SectionTitle>SYNC & ASSISTANT</SectionTitle>

        {!isBackendConfigured() ? (
          <Card style={{ gap: theme.space.sm }}>
            <View style={{ flexDirection: 'row', alignItems: 'center', gap: theme.space.sm }}>
              <Ionicons name="phone-portrait-outline" size={18} color={theme.color.text} />
              <Text variant="ui">On this device only</Text>
            </View>
            <Text variant="caption" tone="faint" style={{ lineHeight: 18 }}>
              Recording, transcription, search and playback all work offline. Add a Supabase project
              to .env to back up your notes, sync across devices, and get summaries and action items
              from the assistant.
            </Text>
          </Card>
        ) : auth.session ? (
          <Card padded={false} style={{ paddingHorizontal: theme.space.base }}>
            <Row
              icon="cloud-done-outline"
              title="Signed in"
              detail={auth.email ?? undefined}
              right={<Tag label="Synced" tone="sage" />}
            />
            <Divider />
            <Row
              icon="sync-outline"
              title={syncing ? 'Syncing…' : 'Sync now'}
              detail="Pushes new notes and pulls anything from your other devices."
              onPress={() => void handleSyncNow()}
            />
            <Divider />
            <Row
              icon="log-out-outline"
              title="Sign out"
              detail="Notes stay on this device."
              onPress={() => {
                Alert.alert('Sign out?', 'Your notes stay on this device.', [
                  { text: 'Cancel', style: 'cancel' },
                  { text: 'Sign out', style: 'destructive', onPress: () => void auth.signOut() },
                ]);
              }}
            />
          </Card>
        ) : auth.awaitingCode ? (
          <Card style={{ gap: theme.space.md }}>
            <Text variant="uiSmall" tone="muted">
              We sent a six-digit code to your email. Enter it to finish signing in.
            </Text>
            <TextInput
              autoFocus
              value={codeInput}
              onChangeText={setCodeInput}
              placeholder="123456"
              placeholderTextColor={theme.color.textFaint}
              keyboardType="number-pad"
              maxLength={6}
              accessibilityLabel="Verification code"
              style={{
                backgroundColor: theme.color.surfaceRaised,
                borderRadius: theme.radius.md,
                borderWidth: 1,
                borderColor: theme.color.border,
                paddingHorizontal: theme.space.md,
                height: 46,
                color: theme.color.text,
                fontFamily: theme.type.numeric.fontFamily,
                fontSize: 18,
                letterSpacing: 4,
              }}
            />
            {auth.error ? (
              <Text variant="caption" tone="danger">
                {auth.error}
              </Text>
            ) : null}
            <View style={{ flexDirection: 'row', gap: theme.space.sm }}>
              <Button
                label="Verify"
                onPress={() => void auth.verifyCode(codeInput)}
                disabled={codeInput.length < 6}
              />
              <Button label="Cancel" variant="ghost" onPress={auth.cancelCode} />
            </View>
          </Card>
        ) : (
          <Card style={{ gap: theme.space.md }}>
            <Text variant="uiSmall" tone="muted" style={{ lineHeight: 21 }}>
              Sign in to back up your recordings and get summaries and action items from your notes.
            </Text>
            <TextInput
              value={emailInput}
              onChangeText={setEmailInput}
              placeholder="you@example.com"
              placeholderTextColor={theme.color.textFaint}
              keyboardType="email-address"
              autoCapitalize="none"
              autoComplete="email"
              accessibilityLabel="Email address"
              style={{
                backgroundColor: theme.color.surfaceRaised,
                borderRadius: theme.radius.md,
                borderWidth: 1,
                borderColor: theme.color.border,
                paddingHorizontal: theme.space.md,
                height: 46,
                color: theme.color.text,
                fontFamily: theme.type.ui.fontFamily,
                fontSize: theme.type.ui.fontSize,
              }}
            />
            {auth.error ? (
              <Text variant="caption" tone="danger">
                {auth.error}
              </Text>
            ) : null}
            <Button
              label="Email me a code"
              onPress={() => void auth.sendCode(emailInput)}
              disabled={!emailInput.includes('@')}
            />
          </Card>
        )}

        {/* ── Google ───────────────────────────────────────────────────── */}
        <SectionTitle>CALENDAR & MAIL</SectionTitle>

        <Card style={{ gap: theme.space.md }}>
          {!google.configured ? (
            <>
              <Text variant="ui">Google is not set up</Text>
              <Text variant="caption" tone="faint" style={{ lineHeight: 18 }}>
                Add EXPO_PUBLIC_GOOGLE_IOS_CLIENT_ID / _ANDROID_CLIENT_ID to .env and rebuild to
                bring your calendar and mail into Echo.
              </Text>
            </>
          ) : google.connected ? (
            <>
              <View style={{ flexDirection: 'row', alignItems: 'center', gap: theme.space.sm }}>
                <Ionicons name="logo-google" size={17} color={theme.color.text} />
                <View style={{ flex: 1 }}>
                  <Text variant="ui">Connected</Text>
                  {google.email ? (
                    <Text variant="caption" tone="faint">
                      {google.email}
                    </Text>
                  ) : null}
                </View>
                <Tag label="Active" tone="sage" />
              </View>
              <Text variant="caption" tone="faint" style={{ lineHeight: 18 }}>
                Echo can read your upcoming events and unread mail, create events, and save drafts.
                It never sends mail on your behalf.
              </Text>
              <Button
                label="Disconnect"
                variant="danger"
                size="sm"
                onPress={() => void google.disconnect()}
              />
            </>
          ) : (
            <>
              <Text variant="uiSmall" tone="muted" style={{ lineHeight: 21 }}>
                Connect Google so Echo can put what you say on your calendar and draft the emails you
                mention.
              </Text>
              {google.error ? (
                <Text variant="caption" tone="danger">
                  {google.error}
                </Text>
              ) : null}
              <Button
                label="Connect Google"
                icon="logo-google"
                loading={google.connecting}
                onPress={() => void google.connect()}
              />
            </>
          )}
        </Card>

        {/* ── Library ──────────────────────────────────────────────────── */}
        <SectionTitle>LIBRARY</SectionTitle>

        <Card padded={false} style={{ paddingHorizontal: theme.space.base }}>
          <Row
            icon="archive-outline"
            title="Archived notes"
            detail={archived.length === 1 ? '1 note' : `${archived.length} notes`}
            onPress={() => router.push('/archive')}
          />
          <Divider />
          <Row
            icon="disc-outline"
            title="Recordings on this device"
            detail={formatBytes(storageBytes)}
          />
        </Card>

        {/* ── About ────────────────────────────────────────────────────── */}
        <SectionTitle>ABOUT</SectionTitle>

        <Card padded={false} style={{ paddingHorizontal: theme.space.base }}>
          <Row
            icon="mic-outline"
            title="Echo"
            detail={`Version ${Constants.expoConfig?.version ?? '1.0.0'}`}
          />
          <Divider />
          <Row
            icon="lock-closed-outline"
            title="Where your notes live"
            detail="Audio and transcripts are stored on this device. They leave it only if you sign in to sync, or connect Google to create an event or draft."
          />
        </Card>
      </ScrollView>
    </Screen>
  );
}
