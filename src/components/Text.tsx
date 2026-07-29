import React from 'react';
import { Text as RNText, type TextProps as RNTextProps, type TextStyle } from 'react-native';

import { useTheme } from '@/theme';

type Variant = keyof ReturnType<typeof useTheme>['type'];
type Tone = 'default' | 'muted' | 'faint' | 'ember' | 'sage' | 'gold' | 'danger' | 'onAccent';

export interface TextProps extends RNTextProps {
  variant?: Variant;
  tone?: Tone;
  weight?: '400' | '500' | '600' | '700';
  align?: TextStyle['textAlign'];
  /** Renders digits at a fixed width so counters don't shift as they tick. */
  tabular?: boolean;
}

/**
 * The only text primitive in the app. Everything reads from the type scale, so
 * there are no ad-hoc font sizes to drift out of sync.
 */
export function Text({
  variant = 'ui',
  tone = 'default',
  weight,
  align,
  tabular,
  style,
  ...rest
}: TextProps) {
  const theme = useTheme();

  const toneColor: Record<Tone, string> = {
    default: theme.color.text,
    muted: theme.color.textMuted,
    faint: theme.color.textFaint,
    ember: theme.color.ember,
    sage: theme.color.sage,
    gold: theme.color.gold,
    danger: theme.color.danger,
    onAccent: theme.color.textOnAccent,
  };

  return (
    <RNText
      {...rest}
      style={[
        theme.type[variant] as TextStyle,
        { color: toneColor[tone] },
        weight ? { fontWeight: weight } : null,
        align ? { textAlign: align } : null,
        tabular ? { fontVariant: ['tabular-nums'] } : null,
        style,
      ]}
    />
  );
}
