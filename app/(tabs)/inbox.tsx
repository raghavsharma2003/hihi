import { Ionicons } from '@expo/vector-icons';
import * as Linking from 'expo-linking';
import React from 'react';
import { Pressable, RefreshControl, ScrollView, View } from 'react-native';

import { Button } from '@/components/Button';
import { Card, Divider, EmptyState, Screen } from '@/components/Layout';
import { Text } from '@/components/Text';
import { listInboxDigest, type InboxMessage } from '@/services/googleApi';
import { useGoogleConnection } from '@/services/googleAuth';
import { useTheme } from '@/theme';
import { formatNoteTime } from '@/utils/time';
import { useAsync } from '@/utils/useAsync';

function MessageRow({ message }: { message: InboxMessage }) {
  const theme = useTheme();

  return (
    <Pressable
      accessibilityRole="link"
      accessibilityLabel={`Open email from ${message.from}: ${message.subject}`}
      onPress={() => {
        // Deep-links into the Gmail app when installed, and the web client
        // otherwise — Echo is a digest, not a mail client.
        void Linking.openURL(`https://mail.google.com/mail/u/0/#inbox/${message.threadId}`);
      }}
      style={({ pressed }) => ({
        paddingVertical: theme.space.md,
        gap: 4,
        opacity: pressed ? 0.6 : 1,
      })}
    >
      <View style={{ flexDirection: 'row', alignItems: 'center', gap: theme.space.sm }}>
        <Text variant="uiSmall" weight="600" numberOfLines={1} style={{ flex: 1 }}>
          {message.from}
        </Text>
        <Text variant="caption" tone="faint" tabular>
          {formatNoteTime(message.receivedMs)}
        </Text>
      </View>
      <Text variant="uiSmall" numberOfLines={1}>
        {message.subject}
      </Text>
      <Text variant="caption" tone="faint" numberOfLines={2} style={{ lineHeight: 17 }}>
        {message.snippet}
      </Text>
    </Pressable>
  );
}

export default function InboxScreen() {
  const theme = useTheme();
  const google = useGoogleConnection();

  const messages = useAsync<InboxMessage[]>(
    async () => (google.connected ? listInboxDigest(12) : []),
    [google.connected],
  );

  return (
    <Screen>
      <View
        style={{
          paddingHorizontal: theme.space.lg,
          paddingTop: theme.space.sm,
          flexDirection: 'row',
          alignItems: 'baseline',
          justifyContent: 'space-between',
        }}
      >
        <Text variant="display">Inbox</Text>
        {google.connected && messages.data ? (
          <Text variant="caption" tone="faint">
            {messages.data.length} unread
          </Text>
        ) : null}
      </View>

      {!google.connected ? (
        <EmptyState
          icon="mail-outline"
          title="Bring your mail in"
          body={
            google.configured
              ? 'Echo shows what is waiting for you and can draft replies straight from a voice note.'
              : 'Add a Google client ID to .env, then connect your account to see unread mail here.'
          }
        >
          {google.configured ? (
            <Button
              label="Connect Google"
              icon="logo-google"
              loading={google.connecting}
              onPress={() => void google.connect()}
            />
          ) : null}
        </EmptyState>
      ) : (
        <ScrollView
          contentContainerStyle={{
            paddingHorizontal: theme.space.lg,
            paddingTop: theme.space.lg,
            paddingBottom: theme.space.xxxl,
            flexGrow: 1,
          }}
          showsVerticalScrollIndicator={false}
          refreshControl={
            <RefreshControl
              refreshing={messages.loading}
              onRefresh={messages.reload}
              tintColor={theme.color.textMuted}
            />
          }
        >
          {messages.error ? (
            <Card style={{ gap: theme.space.md }}>
              <Text variant="uiSmall" tone="muted" style={{ lineHeight: 21 }}>
                Could not read your inbox. Gmail&rsquo;s read scope needs Google verification before
                it works outside your own test users.
              </Text>
              <Text variant="caption" tone="faint">
                {messages.error.message}
              </Text>
            </Card>
          ) : (messages.data?.length ?? 0) === 0 ? (
            <Card>
              <View style={{ flexDirection: 'row', alignItems: 'center', gap: theme.space.sm }}>
                <Ionicons name="checkmark-done" size={18} color={theme.color.sage} />
                <Text variant="uiSmall" tone="muted">
                  {messages.loading ? 'Checking your mail…' : 'Inbox zero. Nothing unread this week.'}
                </Text>
              </View>
            </Card>
          ) : (
            <Card padded={false} style={{ paddingHorizontal: theme.space.base }}>
              {messages.data!.map((message, index) => (
                <View key={message.id}>
                  {index > 0 ? <Divider /> : null}
                  <MessageRow message={message} />
                </View>
              ))}
            </Card>
          )}
        </ScrollView>
      )}
    </Screen>
  );
}
