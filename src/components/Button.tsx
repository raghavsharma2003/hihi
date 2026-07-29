import { Ionicons } from '@expo/vector-icons';
import * as Haptics from 'expo-haptics';
import React, { useCallback } from 'react';
import { ActivityIndicator, Pressable, type StyleProp, View, type ViewStyle } from 'react-native';
import Animated, { useAnimatedStyle, useSharedValue, withSpring } from 'react-native-reanimated';

import { Text } from './Text';
import { useTheme } from '@/theme';

type Variant = 'primary' | 'secondary' | 'ghost' | 'assistant' | 'danger';
type Size = 'sm' | 'md' | 'lg';

export interface ButtonProps {
  label: string;
  onPress?: () => void;
  variant?: Variant;
  size?: Size;
  icon?: keyof typeof Ionicons.glyphMap;
  iconPosition?: 'leading' | 'trailing';
  disabled?: boolean;
  loading?: boolean;
  /** Stretch to the width of the parent. */
  block?: boolean;
  haptic?: false | 'light' | 'medium' | 'success';
  style?: StyleProp<ViewStyle>;
  accessibilityHint?: string;
}

const AnimatedPressable = Animated.createAnimatedComponent(Pressable);

const SIZES: Record<Size, { height: number; padH: number; gap: number; icon: number }> = {
  sm: { height: 36, padH: 14, gap: 6, icon: 15 },
  md: { height: 46, padH: 18, gap: 8, icon: 17 },
  lg: { height: 54, padH: 24, gap: 10, icon: 19 },
};

export function Button({
  label,
  onPress,
  variant = 'primary',
  size = 'md',
  icon,
  iconPosition = 'leading',
  disabled = false,
  loading = false,
  block = false,
  haptic = 'light',
  style,
  accessibilityHint,
}: ButtonProps) {
  const theme = useTheme();
  const scale = useSharedValue(1);
  const dims = SIZES[size];
  const inert = disabled || loading;

  const skin = {
    primary: {
      bg: theme.color.text,
      fg: theme.color.bg,
      border: 'transparent',
    },
    secondary: {
      bg: theme.color.surfaceRaised,
      fg: theme.color.text,
      border: theme.color.border,
    },
    ghost: {
      bg: 'transparent',
      fg: theme.color.textMuted,
      border: 'transparent',
    },
    assistant: {
      bg: theme.color.sageSoft,
      fg: theme.color.sage,
      border: theme.color.sageBorder,
    },
    danger: {
      bg: theme.color.dangerSoft,
      fg: theme.color.danger,
      border: 'transparent',
    },
  }[variant];

  const animatedStyle = useAnimatedStyle(() => ({ transform: [{ scale: scale.value }] }));

  const handlePressIn = useCallback(() => {
    scale.value = withSpring(0.965, theme.motion.press);
  }, [scale, theme.motion.press]);

  const handlePressOut = useCallback(() => {
    scale.value = withSpring(1, theme.motion.press);
  }, [scale, theme.motion.press]);

  const handlePress = useCallback(() => {
    if (inert) return;
    if (haptic === 'light') void Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
    else if (haptic === 'medium') void Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium);
    else if (haptic === 'success')
      void Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
    onPress?.();
  }, [haptic, inert, onPress]);

  const iconNode = icon ? <Ionicons name={icon} size={dims.icon} color={skin.fg} /> : null;

  return (
    <AnimatedPressable
      accessibilityRole="button"
      accessibilityLabel={label}
      accessibilityHint={accessibilityHint}
      accessibilityState={{ disabled: inert, busy: loading }}
      disabled={inert}
      onPress={handlePress}
      onPressIn={handlePressIn}
      onPressOut={handlePressOut}
      style={[
        animatedStyle,
        {
          height: dims.height,
          paddingHorizontal: dims.padH,
          borderRadius: theme.radius.pill,
          backgroundColor: skin.bg,
          borderWidth: skin.border === 'transparent' ? 0 : 1,
          borderColor: skin.border,
          flexDirection: 'row',
          alignItems: 'center',
          justifyContent: 'center',
          gap: dims.gap,
          alignSelf: block ? 'stretch' : 'flex-start',
          opacity: inert ? 0.45 : 1,
        },
        style,
      ]}
    >
      {loading ? (
        <ActivityIndicator size="small" color={skin.fg} />
      ) : (
        <>
          {iconPosition === 'leading' ? iconNode : null}
          <Text
            variant={size === 'sm' ? 'uiSmall' : 'ui'}
            weight="600"
            style={{ color: skin.fg }}
            numberOfLines={1}
          >
            {label}
          </Text>
          {iconPosition === 'trailing' ? iconNode : null}
        </>
      )}
    </AnimatedPressable>
  );
}

export interface IconButtonProps {
  icon: keyof typeof Ionicons.glyphMap;
  onPress?: () => void;
  accessibilityLabel: string;
  size?: number;
  tone?: 'default' | 'muted' | 'ember' | 'sage' | 'danger';
  /** Draws a surface behind the glyph. */
  filled?: boolean;
  disabled?: boolean;
  style?: StyleProp<ViewStyle>;
}

/** A tap target that is only a glyph. Always keeps a 44pt hit area. */
export function IconButton({
  icon,
  onPress,
  accessibilityLabel,
  size = 22,
  tone = 'default',
  filled = false,
  disabled = false,
  style,
}: IconButtonProps) {
  const theme = useTheme();
  const scale = useSharedValue(1);

  const color = {
    default: theme.color.text,
    muted: theme.color.textMuted,
    ember: theme.color.ember,
    sage: theme.color.sage,
    danger: theme.color.danger,
  }[tone];

  const animatedStyle = useAnimatedStyle(() => ({ transform: [{ scale: scale.value }] }));
  const box = Math.max(44, size + 20);

  return (
    <AnimatedPressable
      accessibilityRole="button"
      accessibilityLabel={accessibilityLabel}
      accessibilityState={{ disabled }}
      disabled={disabled}
      onPress={() => {
        void Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
        onPress?.();
      }}
      onPressIn={() => {
        scale.value = withSpring(0.9, theme.motion.press);
      }}
      onPressOut={() => {
        scale.value = withSpring(1, theme.motion.press);
      }}
      style={[
        animatedStyle,
        {
          width: box,
          height: box,
          alignItems: 'center',
          justifyContent: 'center',
          borderRadius: theme.radius.pill,
          backgroundColor: filled ? theme.color.surfaceRaised : 'transparent',
          opacity: disabled ? 0.4 : 1,
        },
        style,
      ]}
    >
      <View pointerEvents="none">
        <Ionicons name={icon} size={size} color={color} />
      </View>
    </AnimatedPressable>
  );
}
