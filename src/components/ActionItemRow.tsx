import { Ionicons } from '@expo/vector-icons';
import * as Haptics from 'expo-haptics';
import React, { useState } from 'react';
import { ActivityIndicator, Pressable, View } from 'react-native';

import { Text } from './Text';
import type { ActionItem } from '@/db/types';
import { useTheme } from '@/theme';
import { formatDueDate } from '@/utils/time';

const KIND_ICON: Record<ActionItem['kind'], keyof typeof Ionicons.glyphMap> = {
  task: 'checkmark-circle-outline',
  event: 'calendar-outline',
  email: 'mail-outline',
  reminder: 'alarm-outline',
};

const KIND_CTA: Record<ActionItem['kind'], string | null> = {
  task: null,
  event: 'Add to calendar',
  email: 'Draft email',
  reminder: 'Add to calendar',
};

export interface ActionItemRowProps {
  item: ActionItem;
  onToggleDone: (item: ActionItem) => void;
  onDismiss: (item: ActionItem) => void;
  /** Runs the item's integration (calendar/Gmail). Resolves when finished. */
  onRunAction?: (item: ActionItem) => Promise<void>;
  /** Whether Google is connected — decides if the CTA is offered. */
  canRunAction: boolean;
}

/**
 * One thing the assistant extracted from a note. The row's job is to make
 * acting on it a single tap: the CTA is the whole point, so it is never hidden
 * behind a menu.
 */
export function ActionItemRow({
  item,
  onToggleDone,
  onDismiss,
  onRunAction,
  canRunAction,
}: ActionItemRowProps) {
  const theme = useTheme();
  const [running, setRunning] = useState(false);

  const done = item.status === 'done';
  const cta = KIND_CTA[item.kind];
  const alreadyRun = Boolean(item.externalId);

  const handleRun = async () => {
    if (!onRunAction || running) return;
    setRunning(true);
    try {
      await onRunAction(item);
      void Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
    } finally {
      setRunning(false);
    }
  };

  return (
    <View
      style={{
        flexDirection: 'row',
        alignItems: 'flex-start',
        gap: theme.space.md,
        paddingVertical: theme.space.md,
      }}
    >
      <Pressable
        accessibilityRole="checkbox"
        accessibilityState={{ checked: done }}
        accessibilityLabel={item.text}
        onPress={() => {
          void Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
          onToggleDone(item);
        }}
        hitSlop={10}
        style={{ paddingTop: 1 }}
      >
        <Ionicons
          name={done ? 'checkmark-circle' : 'ellipse-outline'}
          size={22}
          color={done ? theme.color.sage : theme.color.textFaint}
        />
      </Pressable>

      <View style={{ flex: 1, gap: 6 }}>
        <Text
          variant="ui"
          tone={done ? 'faint' : 'default'}
          style={done ? { textDecorationLine: 'line-through' } : undefined}
        >
          {item.text}
        </Text>

        <View style={{ flexDirection: 'row', alignItems: 'center', gap: theme.space.md, flexWrap: 'wrap' }}>
          <View style={{ flexDirection: 'row', alignItems: 'center', gap: 4 }}>
            <Ionicons name={KIND_ICON[item.kind]} size={12} color={theme.color.textFaint} />
            <Text variant="caption" tone="faint">
              {item.kind === 'task' ? 'Task' : item.kind === 'event' ? 'Event' : item.kind === 'email' ? 'Email' : 'Reminder'}
            </Text>
          </View>

          {item.dueAt ? (
            <Text variant="caption" tone="faint" tabular>
              {formatDueDate(item.dueAt)}
            </Text>
          ) : null}

          {item.recipient ? (
            <Text variant="caption" tone="faint" numberOfLines={1}>
              → {item.recipient}
            </Text>
          ) : null}
        </View>

        {cta && !done ? (
          alreadyRun ? (
            <View style={{ flexDirection: 'row', alignItems: 'center', gap: 5 }}>
              <Ionicons name="checkmark-done" size={13} color={theme.color.sage} />
              <Text variant="caption" tone="sage" weight="600">
                {item.kind === 'email' ? 'Draft created' : 'Added to calendar'}
              </Text>
            </View>
          ) : canRunAction ? (
            <Pressable
              accessibilityRole="button"
              accessibilityLabel={cta}
              onPress={handleRun}
              disabled={running}
              hitSlop={8}
              style={{
                flexDirection: 'row',
                alignItems: 'center',
                gap: 5,
                alignSelf: 'flex-start',
                paddingVertical: 5,
                paddingHorizontal: 10,
                borderRadius: theme.radius.sm,
                backgroundColor: theme.color.sageSoft,
                borderWidth: 1,
                borderColor: theme.color.sageBorder,
              }}
            >
              {running ? (
                <ActivityIndicator size="small" color={theme.color.sage} />
              ) : (
                <Ionicons name="add" size={13} color={theme.color.sage} />
              )}
              <Text variant="caption" tone="sage" weight="600">
                {running ? 'Working…' : cta}
              </Text>
            </Pressable>
          ) : null
        ) : null}
      </View>

      {!done ? (
        <Pressable
          accessibilityRole="button"
          accessibilityLabel={`Dismiss: ${item.text}`}
          onPress={() => onDismiss(item)}
          hitSlop={10}
          style={{ paddingTop: 2 }}
        >
          <Ionicons name="close" size={16} color={theme.color.textFaint} />
        </Pressable>
      ) : null}
    </View>
  );
}
