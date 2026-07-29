import { Ionicons } from '@expo/vector-icons';
import * as Haptics from 'expo-haptics';
import { useRouter } from 'expo-router';
import React, { useCallback, useEffect, useRef, useState } from 'react';
import { Pressable, ScrollView, View } from 'react-native';
import Animated, {
  Easing,
  FadeIn,
  useAnimatedStyle,
  useSharedValue,
  withRepeat,
  withSpring,
  withTiming,
} from 'react-native-reanimated';
import { useSafeAreaInsets } from 'react-native-safe-area-context';

import { Button, IconButton } from '@/components/Button';
import { Text } from '@/components/Text';
import { LiveWaveform } from '@/components/Waveform';
import { adoptRecording, deleteRecording } from '@/capture/storage';
import { useVoiceCapture } from '@/capture/useVoiceCapture';
import { createNote, updateAudioUri } from '@/db/notes';
import { requestEnrichment } from '@/services/orchestrator';
import { useTheme } from '@/theme';

function formatDuration(ms: number): string {
  const total = Math.floor(ms / 1000);
  const minutes = Math.floor(total / 60);
  const seconds = total % 60;
  return `${minutes}:${seconds.toString().padStart(2, '0')}`;
}

/** The pulsing ring behind the stop button — a heartbeat that says "still live". */
function RecordingPulse({ active }: { active: boolean }) {
  const theme = useTheme();
  const pulse = useSharedValue(0);

  useEffect(() => {
    if (active) {
      pulse.value = withRepeat(
        withTiming(1, { duration: 1800, easing: Easing.out(Easing.quad) }),
        -1,
        false,
      );
    } else {
      pulse.value = withTiming(0, { duration: 200 });
    }
  }, [active, pulse]);

  const style = useAnimatedStyle(() => ({
    transform: [{ scale: 1 + pulse.value * 0.55 }],
    opacity: (1 - pulse.value) * 0.35,
  }));

  return (
    <Animated.View
      pointerEvents="none"
      style={[
        style,
        {
          position: 'absolute',
          width: 96,
          height: 96,
          borderRadius: 48,
          backgroundColor: theme.color.ember,
        },
      ]}
    />
  );
}

export default function CaptureScreen() {
  const theme = useTheme();
  const router = useRouter();
  const insets = useSafeAreaInsets();
  const capture = useVoiceCapture();

  const [saving, setSaving] = useState(false);
  const scrollRef = useRef<ScrollView>(null);
  const startedRef = useRef(false);
  const stopScale = useSharedValue(1);

  // Start listening the moment the screen appears. Making the user tap a second
  // time after already tapping record loses the first sentence of the thought.
  useEffect(() => {
    if (startedRef.current) return;
    startedRef.current = true;
    void capture.start();
  }, [capture]);

  // Keep the newest words in view as they arrive.
  useEffect(() => {
    if (capture.transcript) {
      scrollRef.current?.scrollToEnd({ animated: true });
    }
  }, [capture.transcript]);

  const handleCancel = useCallback(() => {
    capture.cancel();
    router.back();
  }, [capture, router]);

  const handleStop = useCallback(async () => {
    if (saving) return;
    setSaving(true);
    void Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);

    const result = await capture.stop();

    // Nothing said and nothing captured — discard rather than leave an empty
    // note in the list for the user to clean up.
    if (!result || (!result.transcript.trim() && !result.audioUri)) {
      if (result?.audioUri) deleteRecording(result.audioUri);
      capture.reset();
      router.back();
      return;
    }

    try {
      const noteId = await createNote({
        transcript: result.transcript,
        audioUri: result.audioUri,
        durationMs: result.durationMs,
        amplitudes: result.amplitudes,
        language: result.language,
        segments: result.segments,
      });

      // Give the recording the note's id so the two stay associated even if the
      // capture temp file naming ever changes.
      if (result.audioUri) {
        const finalUri = adoptRecording(result.audioUri, noteId);
        if (finalUri !== result.audioUri) await updateAudioUri(noteId, finalUri);
      }

      requestEnrichment();
      capture.reset();
      router.replace({ pathname: '/note/[id]', params: { id: noteId } });
    } catch (err) {
      console.error('[echo] failed to save note', err);
      setSaving(false);
    }
  }, [capture, router, saving]);

  const stopStyle = useAnimatedStyle(() => ({ transform: [{ scale: stopScale.value }] }));

  const listening = capture.status === 'listening' || capture.status === 'starting';
  const hasError = capture.status === 'error';

  return (
    <View style={{ flex: 1, backgroundColor: theme.color.bg, paddingTop: insets.top }}>
      {/* Header: leave, and the running length of the note. */}
      <View
        style={{
          flexDirection: 'row',
          alignItems: 'center',
          justifyContent: 'space-between',
          paddingHorizontal: theme.space.md,
          paddingBottom: theme.space.sm,
        }}
      >
        <IconButton
          icon="close"
          accessibilityLabel="Discard recording"
          tone="muted"
          onPress={handleCancel}
        />
        <View style={{ flexDirection: 'row', alignItems: 'center', gap: theme.space.sm }}>
          {listening ? (
            <View
              style={{
                width: 7,
                height: 7,
                borderRadius: 4,
                backgroundColor: theme.color.ember,
              }}
            />
          ) : null}
          <Text variant="numeric" tone={listening ? 'default' : 'muted'} tabular>
            {formatDuration(capture.durationMs)}
          </Text>
        </View>
        <View style={{ width: 44 }} />
      </View>

      {/* Transcript. The point of the screen: proof it is hearing you. */}
      <ScrollView
        ref={scrollRef}
        style={{ flex: 1 }}
        contentContainerStyle={{
          paddingHorizontal: theme.space.xl,
          paddingTop: theme.space.lg,
          paddingBottom: theme.space.xxl,
          flexGrow: 1,
          justifyContent: capture.transcript ? 'flex-start' : 'center',
        }}
        showsVerticalScrollIndicator={false}
      >
        {hasError ? (
          <Animated.View entering={FadeIn.duration(theme.motion.base)} style={{ gap: theme.space.base }}>
            <Ionicons name="alert-circle-outline" size={28} color={theme.color.danger} />
            <Text variant="body" tone="danger">
              {capture.error}
            </Text>
            <View style={{ flexDirection: 'row', gap: theme.space.sm }}>
              <Button
                label="Try again"
                variant="secondary"
                onPress={() => {
                  capture.reset();
                  void capture.start();
                }}
              />
              <Button label="Close" variant="ghost" onPress={handleCancel} />
            </View>
          </Animated.View>
        ) : capture.transcript ? (
          <Text variant="body" selectable>
            {/* Committed text reads normally; the phrase still being recognised
                is dimmed, so the user can see the recogniser catching up. */}
            {capture.transcript.slice(0, capture.transcript.length - capture.interim.length)}
            <Text variant="body" tone="faint">
              {capture.interim}
            </Text>
          </Text>
        ) : (
          <Animated.View entering={FadeIn.delay(400).duration(theme.motion.slow)}>
            <Text variant="display" tone="faint" align="center">
              {listening ? 'Listening…' : 'Getting ready…'}
            </Text>
            <Text
              variant="uiSmall"
              tone="faint"
              align="center"
              style={{ marginTop: theme.space.md }}
            >
              Just start talking. Echo saves the audio and the words.
            </Text>
          </Animated.View>
        )}
      </ScrollView>

      {/* Waveform + stop. */}
      <View
        style={{
          paddingBottom: Math.max(insets.bottom, theme.space.lg) + theme.space.base,
          paddingHorizontal: theme.space.xl,
          gap: theme.space.xl,
        }}
      >
        <View style={{ height: 78, justifyContent: 'center' }}>
          {!hasError ? (
            <LiveWaveform history={capture.trail} level={capture.level} active={listening} />
          ) : null}
        </View>

        {!hasError ? (
          <View style={{ alignItems: 'center', justifyContent: 'center', height: 80 }}>
            <RecordingPulse active={listening} />
            <Animated.View style={stopStyle}>
              <Pressable
                accessibilityRole="button"
                accessibilityLabel="Stop and save note"
                disabled={saving}
                onPressIn={() => {
                  stopScale.value = withSpring(0.93, theme.motion.press);
                }}
                onPressOut={() => {
                  stopScale.value = withSpring(1, theme.motion.press);
                }}
                onPress={handleStop}
                style={[
                  theme.shadow('high'),
                  {
                    width: 78,
                    height: 78,
                    borderRadius: 39,
                    backgroundColor: theme.color.ember,
                    alignItems: 'center',
                    justifyContent: 'center',
                    opacity: saving ? 0.6 : 1,
                  },
                ]}
              >
                <Ionicons name={saving ? 'hourglass-outline' : 'stop'} size={30} color="#FFFFFF" />
              </Pressable>
            </Animated.View>
          </View>
        ) : null}

        <Text variant="caption" tone="faint" align="center">
          {saving ? 'Saving your note…' : listening ? 'Tap to finish' : ' '}
        </Text>
      </View>
    </View>
  );
}
