import { Ionicons } from '@expo/vector-icons';
import { useRouter } from 'expo-router';
import React, { useCallback } from 'react';
import { Pressable, RefreshControl, ScrollView, View } from 'react-native';

import { ActionItemRow } from '@/components/ActionItemRow';
import { Button } from '@/components/Button';
import { Card, Divider, EmptyState, Screen } from '@/components/Layout';
import { Text } from '@/components/Text';
import { useOpenActions } from '@/db/hooks';
import { setActionStatus } from '@/db/notes';
import type { ActionItem } from '@/db/types';
import { runActionItem } from '@/services/actions';
import { listUpcomingEvents, type CalendarEvent } from '@/services/googleApi';
import { useGoogleConnection } from '@/services/googleAuth';
import { useTheme } from '@/theme';
import { formatTimeOfDay } from '@/utils/time';
import { useAsync } from '@/utils/useAsync';
import { useNow } from '@/utils/useNow';

function EventRow({ event, now }: { event: CalendarEvent; now: number }) {
  const theme = useTheme();
  const live = now >= event.startMs && now < event.endMs;
  const past = now >= event.endMs;

  return (
    <View
      style={{
        flexDirection: 'row',
        gap: theme.space.md,
        paddingVertical: theme.space.md,
        opacity: past ? 0.45 : 1,
      }}
    >
      <View style={{ width: 46, alignItems: 'flex-end', paddingTop: 1 }}>
        <Text variant="caption" tone={live ? 'ember' : 'muted'} weight="600" tabular>
          {event.allDay ? 'All day' : formatTimeOfDay(event.startMs)}
        </Text>
      </View>

      {/* A rail rather than a bullet, so a glance reads the day as a timeline. */}
      <View
        style={{
          width: 2,
          borderRadius: 1,
          backgroundColor: live ? theme.color.ember : theme.color.border,
        }}
      />

      <View style={{ flex: 1, gap: 3 }}>
        <Text variant="ui" numberOfLines={2}>
          {event.title}
        </Text>
        {event.location ? (
          <Text variant="caption" tone="faint" numberOfLines={1}>
            {event.location}
          </Text>
        ) : null}
      </View>

      {live ? <Text variant="caption" tone="ember" weight="700">NOW</Text> : null}
    </View>
  );
}

export default function TodayScreen() {
  const theme = useTheme();
  const router = useRouter();
  const google = useGoogleConnection();
  const { data: actions } = useOpenActions();
  // Drives the "NOW" marker, so the schedule stays honest while the screen is open.
  const now = useNow();

  const events = useAsync<CalendarEvent[]>(
    async () => (google.connected ? listUpcomingEvents(36) : []),
    [google.connected],
  );

  const handleRunAction = useCallback(async (item: ActionItem) => {
    await runActionItem(item, { title: 'Echo note', transcript: '' });
    events.reload();
    // `events` is a stable-enough handle; re-running on every render would
    // reload the calendar continuously.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const nothingAtAll = actions.length === 0 && (events.data?.length ?? 0) === 0;

  return (
    <Screen>
      <View style={{ paddingHorizontal: theme.space.lg, paddingTop: theme.space.sm }}>
        <Text variant="display">Today</Text>
      </View>

      <ScrollView
        contentContainerStyle={{ paddingBottom: theme.space.xxxl, flexGrow: 1 }}
        showsVerticalScrollIndicator={false}
        refreshControl={
          <RefreshControl
            refreshing={events.loading && google.connected}
            onRefresh={events.reload}
            tintColor={theme.color.textMuted}
          />
        }
      >
        {/* Calendar */}
        <View style={{ paddingHorizontal: theme.space.lg, paddingTop: theme.space.lg }}>
          <Text variant="overline" tone="faint" style={{ marginBottom: theme.space.sm }}>
            SCHEDULE
          </Text>

          {!google.connected ? (
            <Card style={{ gap: theme.space.md }}>
              <Text variant="uiSmall" tone="muted" style={{ lineHeight: 21 }}>
                {google.configured
                  ? 'Connect Google to see your next day and a half here, and to turn what you say into calendar events.'
                  : 'Add a Google client ID to .env to bring your calendar and mail into Echo.'}
              </Text>
              {google.configured ? (
                <Button
                  label="Connect Google"
                  variant="secondary"
                  size="sm"
                  icon="logo-google"
                  loading={google.connecting}
                  onPress={() => void google.connect()}
                />
              ) : null}
            </Card>
          ) : events.error ? (
            <Card style={{ gap: theme.space.sm }}>
              <Text variant="uiSmall" tone="muted">
                Could not load your calendar. Pull down to try again.
              </Text>
            </Card>
          ) : (events.data?.length ?? 0) === 0 ? (
            <Card>
              <Text variant="uiSmall" tone="muted">
                {events.loading ? 'Loading your schedule…' : 'Nothing scheduled. Enjoy the space.'}
              </Text>
            </Card>
          ) : (
            <Card padded={false} style={{ paddingHorizontal: theme.space.base }}>
              {events.data!.map((event, index) => (
                <View key={event.id}>
                  {index > 0 ? <Divider /> : null}
                  <EventRow event={event} now={now} />
                </View>
              ))}
            </Card>
          )}
        </View>

        {/* Action items pulled out of notes */}
        <View style={{ paddingHorizontal: theme.space.lg, paddingTop: theme.space.xl }}>
          <Text variant="overline" tone="faint" style={{ marginBottom: theme.space.sm }}>
            FROM YOUR NOTES
          </Text>

          {actions.length === 0 ? (
            <Card>
              <Text variant="uiSmall" tone="muted">
                Nothing outstanding. Anything you mention in a note that sounds like a task will
                show up here.
              </Text>
            </Card>
          ) : (
            <Card padded={false} style={{ paddingHorizontal: theme.space.base }}>
              {actions.map((item, index) => (
                <View key={item.id}>
                  {index > 0 ? <Divider /> : null}
                  <ActionItemRow
                    item={item}
                    canRunAction={google.connected}
                    onToggleDone={(a) => void setActionStatus(a.id, 'done')}
                    onDismiss={(a) => void setActionStatus(a.id, 'dismissed')}
                    onRunAction={handleRunAction}
                  />
                  <Pressable
                    accessibilityRole="link"
                    accessibilityLabel={`Open note: ${item.noteTitle}`}
                    onPress={() =>
                      router.push({ pathname: '/note/[id]', params: { id: item.noteId } })
                    }
                    hitSlop={6}
                    style={{
                      flexDirection: 'row',
                      alignItems: 'center',
                      gap: 4,
                      paddingBottom: theme.space.md,
                      paddingLeft: 34,
                    }}
                  >
                    <Ionicons name="return-down-forward" size={12} color={theme.color.textFaint} />
                    <Text variant="caption" tone="faint" numberOfLines={1}>
                      {item.noteTitle}
                    </Text>
                  </Pressable>
                </View>
              ))}
            </Card>
          )}
        </View>

        {nothingAtAll && !google.connected ? (
          <View style={{ flex: 1, minHeight: 160 }}>
            <EmptyState
              icon="sunny-outline"
              title="A clear day"
              body="Record a note and anything actionable in it lands here."
            />
          </View>
        ) : null}
      </ScrollView>
    </Screen>
  );
}
