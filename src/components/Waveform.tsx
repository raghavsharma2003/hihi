import React, { memo, useMemo } from 'react';
import { View } from 'react-native';
import Animated, {
  useAnimatedStyle,
  useDerivedValue,
  withTiming,
  type SharedValue,
} from 'react-native-reanimated';

import { useTheme } from '@/theme';

const BAR_W = 3;
const BAR_GAP = 3;
const MIN_H = 3;

/**
 * The bar that is currently being fed by the microphone. Animated on the UI
 * thread so it tracks the voice without competing with JS work (transcript
 * updates, database writes) happening on every utterance.
 */
function LiveBar({
  level,
  height,
  color,
}: {
  level: SharedValue<number>;
  height: number;
  color: string;
}) {
  const h = useDerivedValue(() =>
    withTiming(MIN_H + level.value * (height - MIN_H), { duration: 90 }),
  );
  const style = useAnimatedStyle(() => ({ height: h.value }));
  return (
    <Animated.View
      style={[
        style,
        { width: BAR_W, borderRadius: BAR_W / 2, backgroundColor: color },
      ]}
    />
  );
}

export interface LiveWaveformProps {
  /** Amplitude history, oldest first, each 0..1. */
  history: number[];
  /** Current microphone level, driven on the UI thread. */
  level: SharedValue<number>;
  height?: number;
  /** Dims the trail when paused so the live bar still reads as "now". */
  active?: boolean;
}

/**
 * Scrolling amplitude trail: history flows leftward while the rightmost bar
 * tracks the live signal. Seeing your own voice move is what makes recording
 * feel like it is working — a static "Recording…" label does not.
 */
export const LiveWaveform = memo(function LiveWaveform({
  history,
  level,
  height = 76,
  active = true,
}: LiveWaveformProps) {
  const theme = useTheme();

  return (
    <View
      accessibilityElementsHidden
      importantForAccessibility="no-hide-descendants"
      style={{
        height,
        flexDirection: 'row',
        alignItems: 'center',
        justifyContent: 'flex-end',
        gap: BAR_GAP,
        overflow: 'hidden',
      }}
    >
      {history.map((amp, i) => {
        // Older bars fade out, so the trail reads as a tail rather than a wall.
        const age = (history.length - i) / history.length;
        return (
          <View
            key={i}
            style={{
              width: BAR_W,
              height: Math.max(MIN_H, amp * height),
              borderRadius: BAR_W / 2,
              backgroundColor: theme.color.ember,
              opacity: active ? Math.max(0.18, 1 - age * 0.85) : 0.2,
            }}
          />
        );
      })}
      <LiveBar level={level} height={height} color={theme.color.ember} />
    </View>
  );
});

export interface StaticWaveformProps {
  /** Amplitude samples captured at record time, each 0..1. */
  samples: number[];
  /** Playback position, 0..1. Bars before it are filled. */
  progress: number;
  height?: number;
  /** Bars to draw. Samples are resampled to fit. */
  resolution?: number;
  tone?: 'ember' | 'muted';
}

/**
 * The recorded waveform, replayed under the scrubber. It is the same shape the
 * user watched while speaking, which makes a note recognisable at a glance
 * before its title has even loaded.
 */
export const StaticWaveform = memo(function StaticWaveform({
  samples,
  progress,
  height = 44,
  resolution = 56,
  tone = 'ember',
}: StaticWaveformProps) {
  const theme = useTheme();

  // Resample to a fixed bar count so every note's waveform occupies the same
  // width regardless of how long it is.
  const bars = useMemo(() => {
    if (samples.length === 0) return new Array(resolution).fill(0.12);
    const out: number[] = [];
    const bucket = samples.length / resolution;
    for (let i = 0; i < resolution; i++) {
      const start = Math.floor(i * bucket);
      const end = Math.max(start + 1, Math.floor((i + 1) * bucket));
      let peak = 0;
      for (let j = start; j < end && j < samples.length; j++) {
        peak = Math.max(peak, samples[j] ?? 0);
      }
      out.push(Math.max(0.08, peak));
    }
    return out;
  }, [samples, resolution]);

  const filledColor = tone === 'ember' ? theme.color.ember : theme.color.text;
  const playedCount = Math.round(progress * bars.length);

  return (
    <View
      accessibilityElementsHidden
      importantForAccessibility="no-hide-descendants"
      style={{
        height,
        flexDirection: 'row',
        alignItems: 'center',
        gap: 2,
      }}
    >
      {bars.map((amp, i) => (
        <View
          key={i}
          style={{
            flex: 1,
            height: Math.max(MIN_H, amp * height),
            borderRadius: 1.5,
            backgroundColor: i < playedCount ? filledColor : theme.color.borderStrong,
          }}
        />
      ))}
    </View>
  );
});
