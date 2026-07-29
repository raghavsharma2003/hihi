import { Ionicons } from '@expo/vector-icons';
import { setAudioModeAsync, useAudioPlayer, useAudioPlayerStatus } from 'expo-audio';
import * as Haptics from 'expo-haptics';
import React, { useCallback, useEffect, useMemo, useState } from 'react';
import { LayoutChangeEvent, Pressable, View } from 'react-native';

import { IconButton } from './Button';
import { Text } from './Text';
import { StaticWaveform } from './Waveform';
import { audioExists } from '@/capture/storage';
import { useTheme } from '@/theme';
import { formatDuration } from '@/utils/time';

const SPEEDS = [1, 1.5, 2] as const;
const SKIP_SECONDS = 15;

export interface AudioPlayerProps {
  uri: string | null;
  /** Waveform captured at record time. */
  amplitudes: number[];
  /** Recorded length, used until the decoder reports the real duration. */
  fallbackDurationMs: number;
  /** Fired continuously during playback so the transcript can follow along. */
  onPositionChange?: (positionMs: number) => void;
  /** Set to seek externally, e.g. when the user taps a transcript line. */
  seekToMs?: number | null;
  onSeekHandled?: () => void;
}

/**
 * Playback for a note's recording. The waveform doubles as the scrubber — the
 * shape is meaningful here (it is the user's own voice), so spending the width
 * on it beats a plain progress bar.
 */
export function AudioPlayer({
  uri,
  amplitudes,
  fallbackDurationMs,
  onPositionChange,
  seekToMs,
  onSeekHandled,
}: AudioPlayerProps) {
  const theme = useTheme();
  const [speedIndex, setSpeedIndex] = useState(0);
  const [trackWidth, setTrackWidth] = useState(0);

  // Checking the filesystem is cheap and synchronous, so derive this rather
  // than round-tripping through an effect — the player must never be handed a
  // URI whose file has been removed.
  const missing = useMemo(() => Boolean(uri) && !audioExists(uri), [uri]);

  const player = useAudioPlayer(uri && !missing ? { uri } : undefined, { updateInterval: 120 });
  const status = useAudioPlayerStatus(player);

  // Playback must be audible when the ringer switch is silenced — a voice note
  // the user deliberately pressed play on should not be silent.
  useEffect(() => {
    void setAudioModeAsync({ playsInSilentMode: true, allowsRecording: false });
  }, []);

  const durationSec =
    status.duration && status.duration > 0 ? status.duration : fallbackDurationMs / 1000;
  const positionSec = status.currentTime ?? 0;
  const progress = durationSec > 0 ? Math.min(1, positionSec / durationSec) : 0;

  useEffect(() => {
    onPositionChange?.(positionSec * 1000);
  }, [onPositionChange, positionSec]);

  // Honour a seek requested by the transcript.
  useEffect(() => {
    if (seekToMs == null) return;
    void player.seekTo(Math.max(0, seekToMs / 1000));
    if (!status.playing) player.play();
    onSeekHandled?.();
    // `status.playing` is read as a snapshot at seek time; re-running on every
    // status tick would fight the user's own play/pause.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [seekToMs]);

  // Rewind a finished note so pressing play starts it over rather than doing
  // nothing at the very end of the track.
  useEffect(() => {
    if (status.didJustFinish) void player.seekTo(0);
  }, [player, status.didJustFinish]);

  const togglePlay = useCallback(() => {
    void Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
    if (status.playing) player.pause();
    else player.play();
  }, [player, status.playing]);

  const skip = useCallback(
    (seconds: number) => {
      const next = Math.max(0, Math.min(durationSec, positionSec + seconds));
      void player.seekTo(next);
    },
    [durationSec, player, positionSec],
  );

  const cycleSpeed = useCallback(() => {
    const next = (speedIndex + 1) % SPEEDS.length;
    setSpeedIndex(next);
    player.setPlaybackRate(SPEEDS[next]!);
  }, [player, speedIndex]);

  const handleScrub = useCallback(
    (event: { nativeEvent: { locationX: number } }) => {
      if (trackWidth <= 0 || durationSec <= 0) return;
      const ratio = Math.max(0, Math.min(1, event.nativeEvent.locationX / trackWidth));
      void player.seekTo(ratio * durationSec);
    },
    [durationSec, player, trackWidth],
  );

  const onTrackLayout = useCallback((event: LayoutChangeEvent) => {
    setTrackWidth(event.nativeEvent.layout.width);
  }, []);

  if (!uri || missing) {
    return (
      <View
        style={{
          flexDirection: 'row',
          alignItems: 'center',
          gap: theme.space.sm,
          paddingVertical: theme.space.md,
        }}
      >
        <Ionicons name="cloud-offline-outline" size={16} color={theme.color.textFaint} />
        <Text variant="caption" tone="faint">
          {uri
            ? 'The recording is not on this device. The transcript is complete.'
            : 'No audio was captured for this note.'}
        </Text>
      </View>
    );
  }

  return (
    <View style={{ gap: theme.space.md }}>
      <Pressable
        onPress={handleScrub}
        onLayout={onTrackLayout}
        accessibilityRole="adjustable"
        accessibilityLabel="Playback position"
        accessibilityValue={{
          min: 0,
          max: Math.round(durationSec),
          now: Math.round(positionSec),
        }}
        hitSlop={{ top: 12, bottom: 12 }}
      >
        <StaticWaveform samples={amplitudes} progress={progress} height={46} resolution={58} />
      </Pressable>

      <View style={{ flexDirection: 'row', justifyContent: 'space-between' }}>
        <Text variant="caption" tone="faint" tabular>
          {formatDuration(positionSec * 1000)}
        </Text>
        <Text variant="caption" tone="faint" tabular>
          {formatDuration(durationSec * 1000)}
        </Text>
      </View>

      <View
        style={{
          flexDirection: 'row',
          alignItems: 'center',
          justifyContent: 'center',
          gap: theme.space.base,
        }}
      >
        <IconButton
          icon="play-back"
          size={19}
          tone="muted"
          accessibilityLabel={`Back ${SKIP_SECONDS} seconds`}
          onPress={() => skip(-SKIP_SECONDS)}
        />

        <Pressable
          accessibilityRole="button"
          accessibilityLabel={status.playing ? 'Pause' : 'Play'}
          onPress={togglePlay}
          style={{
            width: 56,
            height: 56,
            borderRadius: 28,
            backgroundColor: theme.color.ember,
            alignItems: 'center',
            justifyContent: 'center',
          }}
        >
          <Ionicons
            name={status.playing ? 'pause' : 'play'}
            size={24}
            color="#FFFFFF"
            // The play triangle is visually off-centre in a circle; nudge it.
            style={{ marginLeft: status.playing ? 0 : 3 }}
          />
        </Pressable>

        <IconButton
          icon="play-forward"
          size={19}
          tone="muted"
          accessibilityLabel={`Forward ${SKIP_SECONDS} seconds`}
          onPress={() => skip(SKIP_SECONDS)}
        />

        <Pressable
          accessibilityRole="button"
          accessibilityLabel={`Playback speed ${SPEEDS[speedIndex]}x`}
          onPress={cycleSpeed}
          hitSlop={12}
          style={{
            paddingHorizontal: 10,
            paddingVertical: 6,
            borderRadius: theme.radius.sm,
            backgroundColor: theme.color.surfaceRaised,
            marginLeft: theme.space.xs,
          }}
        >
          <Text variant="caption" tone="muted" weight="600" tabular>
            {SPEEDS[speedIndex]}×
          </Text>
        </Pressable>
      </View>
    </View>
  );
}
