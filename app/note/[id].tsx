import { Ionicons } from '@expo/vector-icons';
import * as Clipboard from 'expo-clipboard';
import { useLocalSearchParams, useRouter } from 'expo-router';
import * as Sharing from 'expo-sharing';
import React, { useCallback, useMemo, useState } from 'react';
import { Alert, Pressable, ScrollView, TextInput, View } from 'react-native';
import Animated, { FadeIn } from 'react-native-reanimated';
import { useSafeAreaInsets } from 'react-native-safe-area-context';

import { ActionItemRow } from '@/components/ActionItemRow';
import { AudioPlayer } from '@/components/AudioPlayer';
import { Button, IconButton } from '@/components/Button';
import { Card, Divider, Tag } from '@/components/Layout';
import { ThinkingLines } from '@/components/Shimmer';
import { Text } from '@/components/Text';
import { deleteRecording } from '@/capture/storage';
import { useNote } from '@/db/hooks';
import {
  deleteNote,
  setActionStatus,
  setPinned,
  updateTitle,
  updateTranscript,
} from '@/db/notes';
import type { ActionItem } from '@/db/types';
import { runActionItem } from '@/services/actions';
import { useGoogleConnection } from '@/services/googleAuth';
import { requestEnrichment } from '@/services/orchestrator';
import { isAiConfigured } from '@/services/supabase';
import { useTheme } from '@/theme';
import { formatNoteTimestamp } from '@/utils/time';

export default function NoteDetailScreen() {
  const theme = useTheme();
  const router = useRouter();
  const insets = useSafeAreaInsets();
  const { id } = useLocalSearchParams<{ id: string }>();

  const { data: note, loading } = useNote(id);
  const google = useGoogleConnection();

  const [editingTranscript, setEditingTranscript] = useState(false);
  const [draftTranscript, setDraftTranscript] = useState('');
  const [editingTitle, setEditingTitle] = useState(false);
  const [draftTitle, setDraftTitle] = useState('');
  const [positionMs, setPositionMs] = useState(0);
  const [seekRequest, setSeekRequest] = useState<number | null>(null);

  const openActions = useMemo(
    () => note?.actionItems.filter((a) => a.status !== 'dismissed') ?? [],
    [note],
  );

  // The segment currently being spoken, so the transcript can follow playback.
  const activeSegmentId = useMemo(() => {
    if (!note || note.segments.length === 0) return null;
    const current = note.segments.find((s) => positionMs >= s.startMs && positionMs < s.endMs);
    return current?.id ?? null;
  }, [note, positionMs]);

  const handleShare = useCallback(async () => {
    if (!note) return;
    const text = [note.title, '', note.summary, '', note.transcript].filter(Boolean).join('\n');
    await Clipboard.setStringAsync(text);

    // Offer the audio too when the platform has a share sheet — the recording is
    // half of what the user made.
    if (note.audioUri && (await Sharing.isAvailableAsync())) {
      await Sharing.shareAsync(note.audioUri, {
        dialogTitle: note.title,
        mimeType: 'audio/wav',
      });
    } else {
      Alert.alert('Copied', 'The note text is on your clipboard.');
    }
  }, [note]);

  const handleDelete = useCallback(() => {
    if (!note) return;
    Alert.alert('Delete this note?', 'The recording and the transcript will both be removed.', [
      { text: 'Cancel', style: 'cancel' },
      {
        text: 'Delete',
        style: 'destructive',
        onPress: async () => {
          deleteRecording(note.audioUri);
          await deleteNote(note.id);
          router.back();
        },
      },
    ]);
  }, [note, router]);

  const handleRunAction = useCallback(
    async (item: ActionItem) => {
      if (!note) return;
      try {
        await runActionItem(item, note);
      } catch (err) {
        Alert.alert(
          'Could not complete that',
          err instanceof Error ? err.message : 'Something went wrong talking to Google.',
        );
      }
    },
    [note],
  );

  if (loading && !note) {
    return <View style={{ flex: 1, backgroundColor: theme.color.bg }} />;
  }

  if (!note) {
    return (
      <View
        style={{
          flex: 1,
          backgroundColor: theme.color.bg,
          alignItems: 'center',
          justifyContent: 'center',
          gap: theme.space.base,
        }}
      >
        <Text variant="title">This note is gone</Text>
        <Button label="Back to notes" variant="secondary" onPress={() => router.back()} />
      </View>
    );
  }

  const enriching = note.enrichStatus === 'pending';
  const aiUnavailable = note.enrichStatus === 'skipped' || !isAiConfigured();

  return (
    <View style={{ flex: 1, backgroundColor: theme.color.bg, paddingTop: insets.top }}>
      {/* Header */}
      <View
        style={{
          flexDirection: 'row',
          alignItems: 'center',
          justifyContent: 'space-between',
          paddingHorizontal: theme.space.xs,
          paddingBottom: theme.space.xs,
        }}
      >
        <IconButton icon="chevron-back" accessibilityLabel="Back" onPress={() => router.back()} />
        <View style={{ flexDirection: 'row' }}>
          <IconButton
            icon={note.pinned ? 'bookmark' : 'bookmark-outline'}
            accessibilityLabel={note.pinned ? 'Unpin note' : 'Pin note'}
            tone={note.pinned ? 'default' : 'muted'}
            onPress={() => void setPinned(note.id, !note.pinned)}
          />
          <IconButton
            icon="share-outline"
            accessibilityLabel="Share note"
            tone="muted"
            onPress={handleShare}
          />
          <IconButton
            icon="trash-outline"
            accessibilityLabel="Delete note"
            tone="muted"
            onPress={handleDelete}
          />
        </View>
      </View>

      <ScrollView
        contentContainerStyle={{
          paddingHorizontal: theme.space.lg,
          paddingBottom: insets.bottom + theme.space.xxxl,
        }}
        showsVerticalScrollIndicator={false}
        keyboardDismissMode="interactive"
      >
        {/* Title */}
        {editingTitle ? (
          <TextInput
            autoFocus
            value={draftTitle}
            onChangeText={setDraftTitle}
            onBlur={async () => {
              setEditingTitle(false);
              if (draftTitle.trim() && draftTitle !== note.title) {
                await updateTitle(note.id, draftTitle);
              }
            }}
            returnKeyType="done"
            accessibilityLabel="Note title"
            style={{
              ...theme.type.title,
              color: theme.color.text,
              paddingVertical: theme.space.sm,
            }}
          />
        ) : (
          <Pressable
            accessibilityRole="button"
            accessibilityLabel={`Rename note. Current title: ${note.title}`}
            onPress={() => {
              setDraftTitle(note.title);
              setEditingTitle(true);
            }}
            style={{ paddingVertical: theme.space.sm }}
          >
            <Text variant="title">{note.title}</Text>
          </Pressable>
        )}

        <Text variant="caption" tone="faint" style={{ marginBottom: theme.space.lg }}>
          {formatNoteTimestamp(note.createdAt)}
        </Text>

        {/* Playback */}
        <Card style={{ marginBottom: theme.space.lg }}>
          <AudioPlayer
            uri={note.audioUri}
            amplitudes={note.amplitudes}
            fallbackDurationMs={note.durationMs}
            onPositionChange={setPositionMs}
            seekToMs={seekRequest}
            onSeekHandled={() => setSeekRequest(null)}
          />
        </Card>

        {/* Assistant summary */}
        {enriching ? (
          <Card tone="assistant" style={{ marginBottom: theme.space.lg, gap: theme.space.md }}>
            <View style={{ flexDirection: 'row', alignItems: 'center', gap: 6 }}>
              <Ionicons name="sparkles-outline" size={14} color={theme.color.sage} />
              <Text variant="overline" tone="sage">
                READING YOUR NOTE
              </Text>
            </View>
            <ThinkingLines lines={3} />
          </Card>
        ) : note.summary ? (
          <Animated.View entering={FadeIn.duration(theme.motion.slow)}>
            <Card tone="assistant" style={{ marginBottom: theme.space.lg, gap: theme.space.md }}>
              <View style={{ flexDirection: 'row', alignItems: 'center', gap: 6 }}>
                <Ionicons name="sparkles" size={14} color={theme.color.sage} />
                <Text variant="overline" tone="sage">
                  SUMMARY
                </Text>
              </View>
              <Text variant="body" style={{ fontSize: 16, lineHeight: 26 }}>
                {note.summary}
              </Text>
              {note.tags.length > 0 ? (
                <View style={{ flexDirection: 'row', flexWrap: 'wrap', gap: 6 }}>
                  {note.tags.map((tag) => (
                    <Tag key={tag} label={tag} tone="sage" />
                  ))}
                </View>
              ) : null}
            </Card>
          </Animated.View>
        ) : note.enrichStatus === 'failed' ? (
          <Card style={{ marginBottom: theme.space.lg, gap: theme.space.md }}>
            <Text variant="uiSmall" tone="muted">
              The assistant could not read this note. Your recording and transcript are safe.
            </Text>
            <Button
              label="Try again"
              variant="secondary"
              size="sm"
              icon="refresh"
              onPress={() => requestEnrichment(note.id)}
            />
          </Card>
        ) : aiUnavailable ? (
          <Card style={{ marginBottom: theme.space.lg, gap: theme.space.sm }}>
            <Text variant="uiSmall" tone="muted">
              Connect a Supabase project to get summaries, action items and calendar suggestions from
              your notes. Recording and transcription work without it.
            </Text>
          </Card>
        ) : null}

        {/* Action items */}
        {openActions.length > 0 ? (
          <View style={{ marginBottom: theme.space.lg }}>
            <Text variant="overline" tone="faint" style={{ marginBottom: theme.space.xs }}>
              WHAT TO DO
            </Text>
            <Card padded={false} style={{ paddingHorizontal: theme.space.base }}>
              {openActions.map((item, index) => (
                <View key={item.id}>
                  {index > 0 ? <Divider /> : null}
                  <ActionItemRow
                    item={item}
                    canRunAction={google.connected}
                    onToggleDone={(a) =>
                      void setActionStatus(a.id, a.status === 'done' ? 'open' : 'done')
                    }
                    onDismiss={(a) => void setActionStatus(a.id, 'dismissed')}
                    onRunAction={handleRunAction}
                  />
                </View>
              ))}
            </Card>
            {!google.connected && openActions.some((a) => a.kind !== 'task') ? (
              <Text variant="caption" tone="faint" style={{ marginTop: theme.space.sm }}>
                Connect Google in Settings to add these to your calendar or draft the emails.
              </Text>
            ) : null}
          </View>
        ) : null}

        {/* Transcript */}
        <View
          style={{
            flexDirection: 'row',
            alignItems: 'center',
            justifyContent: 'space-between',
            marginBottom: theme.space.xs,
          }}
        >
          <Text variant="overline" tone="faint">
            TRANSCRIPT
          </Text>
          <Pressable
            accessibilityRole="button"
            accessibilityLabel={editingTranscript ? 'Save transcript' : 'Edit transcript'}
            hitSlop={10}
            onPress={async () => {
              if (editingTranscript) {
                if (draftTranscript !== note.transcript) {
                  await updateTranscript(note.id, draftTranscript);
                }
                setEditingTranscript(false);
              } else {
                setDraftTranscript(note.transcript);
                setEditingTranscript(true);
              }
            }}
          >
            <Text variant="caption" tone="muted" weight="600">
              {editingTranscript ? 'Done' : 'Edit'}
            </Text>
          </Pressable>
        </View>

        {editingTranscript ? (
          <TextInput
            multiline
            autoFocus
            value={draftTranscript}
            onChangeText={setDraftTranscript}
            accessibilityLabel="Transcript"
            style={{
              ...theme.type.body,
              color: theme.color.text,
              backgroundColor: theme.color.surface,
              borderRadius: theme.radius.md,
              borderWidth: 1,
              borderColor: theme.color.borderStrong,
              padding: theme.space.base,
              minHeight: 180,
              textAlignVertical: 'top',
            }}
          />
        ) : note.segments.length > 0 ? (
          // With timings we can make the transcript a navigation surface: tap a
          // phrase to hear exactly that moment.
          <Text variant="body">
            {note.segments.map((segment) => (
              <Text
                key={segment.id}
                variant="body"
                onPress={() => setSeekRequest(segment.startMs)}
                style={
                  segment.id === activeSegmentId
                    ? { backgroundColor: theme.color.emberSoft, color: theme.color.text }
                    : undefined
                }
                accessibilityRole="button"
                accessibilityLabel={`Play from: ${segment.text}`}
              >
                {segment.text}{' '}
              </Text>
            ))}
          </Text>
        ) : note.transcript ? (
          <Text variant="body" selectable>
            {note.transcript}
          </Text>
        ) : (
          <Text variant="uiSmall" tone="faint">
            No words were recognised in this recording. You can still play the audio, or type the
            transcript yourself.
          </Text>
        )}
      </ScrollView>
    </View>
  );
}
