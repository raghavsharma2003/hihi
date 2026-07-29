import React, { useEffect } from 'react';
import { View, type ViewStyle } from 'react-native';
import Animated, {
  Easing,
  useAnimatedStyle,
  useSharedValue,
  withRepeat,
  withTiming,
} from 'react-native-reanimated';

import { useTheme } from '@/theme';

/**
 * Placeholder for content the assistant is still writing. It breathes rather
 * than sweeping a highlight across, because several of these appear in a list
 * at once and a synchronised sweep reads as a glitch.
 */
export function Shimmer({
  width,
  height = 12,
  style,
}: {
  width: number | `${number}%`;
  height?: number;
  style?: ViewStyle;
}) {
  const theme = useTheme();
  const pulse = useSharedValue(0.35);

  useEffect(() => {
    pulse.value = withRepeat(
      withTiming(0.75, { duration: 900, easing: Easing.inOut(Easing.quad) }),
      -1,
      true,
    );
  }, [pulse]);

  const animated = useAnimatedStyle(() => ({ opacity: pulse.value }));

  return (
    <Animated.View
      style={[
        animated,
        {
          width,
          height,
          borderRadius: height / 2,
          backgroundColor: theme.color.surfaceRaised,
        },
        style,
      ]}
    />
  );
}

/** The "assistant is thinking" affordance used on a note that is enriching. */
export function ThinkingLines({ lines = 2 }: { lines?: number }) {
  const theme = useTheme();
  return (
    <View style={{ gap: theme.space.sm }}>
      {Array.from({ length: lines }).map((_, i) => (
        <Shimmer key={i} width={i === lines - 1 ? '62%' : '100%'} height={11} />
      ))}
    </View>
  );
}
