import { Ionicons } from '@expo/vector-icons';
import { useRouter } from 'expo-router';
import React, { useCallback, useRef } from 'react';
import { Pressable, View } from 'react-native';
import { Swipeable } from 'react-native-gesture-handler';

import { ThinkingLines } from './Shimmer';
import { Text } from './Text';
import { StaticWaveform } from './Waveform';
import type { Note } from '@/db/types';
import { useTheme } from '@/theme';
import { formatDuration, formatNoteTime } from '@/utils/time';

/** Roughly two lines of preview text, so cards stay a predictable height. */
function snippet(note: Note): string {
  const source = note.summary || note.transcript;
  return source.length > 150 ? `${source.slice(0, 150).trimEnd()}…` : source;
}

function SwipeAction({
  icon,
  label,
  color,
  onPress,
}: {
  icon: keyof typeof Ionicons.glyphMap;
  label: string;
  color: string;
  onPress: () => void;
}) {
  return (
    <Pressable
      accessibilityRole="button"
      accessibilityLabel={label}
      onPress={onPress}
      style={{
        width: 78,
        alignItems: 'center',
        justifyContent: 'center',
        gap: 5,
        backgroundColor: color,
      }}
    >
      <Ionicons name={icon} size={20} color="#FFFFFF" />
      <Text variant="caption" style={{ color: '#FFFFFF', fontSize: 11 }} weight="600">
        {label}
      </Text>
    </Pressable>
  );
}

export interface NoteCardProps {
  note: Note;
  onArchive: (id: string) => void;
  onTogglePin: (id: string, pinned: boolean) => void;
}

export function NoteCard({ note, onArchive, onTogglePin }: NoteCardProps) {
  const theme = useTheme();
  const router = useRouter();
  const swipeRef = useRef<Swipeable>(null);

  const open = useCallback(() => {
    router.push({ pathname: '/note/[id]', params: { id: note.id } });
  }, [note.id, router]);

  const enriching = note.enrichStatus === 'pending' && !note.summary;

  return (
    <Swipeable
      ref={swipeRef}
      friction={2}
      rightThreshold={40}
      overshootRight={false}
      renderRightActions={() => (
        <View style={{ flexDirection: 'row' }}>
          <SwipeAction
            icon={note.pinned ? 'bookmark' : 'bookmark-outline'}
            label={note.pinned ? 'Unpin' : 'Pin'}
            color={theme.color.gold}
            onPress={() => {
              swipeRef.current?.close();
              onTogglePin(note.id, !note.pinned);
            }}
          />
          <SwipeAction
            icon="archive-outline"
            label="Archive"
            color={theme.color.textFaint}
            onPress={() => {
              swipeRef.current?.close();
              onArchive(note.id);
            }}
          />
        </View>
      )}
    >
      <Pressable
        accessibilityRole="button"
        accessibilityLabel={note.title}
        accessibilityHint="Opens the note"
        onPress={open}
        style={({ pressed }) => ({
          backgroundColor: pressed ? theme.color.surfacePressed : theme.color.bg,
          paddingHorizontal: theme.space.lg,
          paddingVertical: theme.space.base,
          gap: theme.space.sm,
        })}
      >
        <View style={{ flexDirection: 'row', alignItems: 'flex-start', gap: theme.space.sm }}>
          <View style={{ flex: 1, gap: 5 }}>
            <Text variant="heading" numberOfLines={2}>
              {note.title}
            </Text>

            {enriching ? (
              <View style={{ paddingTop: 4, paddingBottom: 2 }}>
                <ThinkingLines lines={2} />
              </View>
            ) : snippet(note) ? (
              <Text variant="uiSmall" tone="muted" numberOfLines={2} style={{ lineHeight: 20 }}>
                {snippet(note)}
              </Text>
            ) : null}
          </View>

          {note.pinned ? (
            <Ionicons name="bookmark" size={15} color={theme.color.gold} style={{ marginTop: 4 }} />
          ) : null}
        </View>

        <View style={{ flexDirection: 'row', alignItems: 'center', gap: theme.space.md }}>
          <Text variant="caption" tone="faint" tabular>
            {formatNoteTime(note.createdAt)}
          </Text>

          {note.durationMs > 0 ? (
            <View style={{ flexDirection: 'row', alignItems: 'center', gap: 4 }}>
              <Ionicons name="mic-outline" size={12} color={theme.color.textFaint} />
              <Text variant="caption" tone="faint" tabular>
                {formatDuration(note.durationMs)}
              </Text>
            </View>
          ) : null}

          {/* A miniature of the waveform the user watched while speaking, which
              makes a note recognisable before its title is even read. */}
          {note.amplitudes.length > 0 ? (
            <View style={{ flex: 1, maxWidth: 90, opacity: 0.5 }}>
              <StaticWaveform samples={note.amplitudes} progress={0} height={14} resolution={22} tone="muted" />
            </View>
          ) : (
            <View style={{ flex: 1 }} />
          )}

          {note.syncStatus === 'failed' ? (
            <Ionicons name="cloud-offline-outline" size={13} color={theme.color.danger} />
          ) : null}
        </View>
      </Pressable>
    </Swipeable>
  );
}
