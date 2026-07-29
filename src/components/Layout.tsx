import { Ionicons } from '@expo/vector-icons';
import React from 'react';
import { Pressable, type StyleProp, StyleSheet, View, type ViewStyle } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';

import { Text } from './Text';
import { useTheme } from '@/theme';

export function Screen({
  children,
  style,
  edges = ['top'],
}: {
  children: React.ReactNode;
  style?: StyleProp<ViewStyle>;
  edges?: ('top' | 'bottom')[];
}) {
  const theme = useTheme();
  const insets = useSafeAreaInsets();
  return (
    <View
      style={[
        {
          flex: 1,
          backgroundColor: theme.color.bg,
          paddingTop: edges.includes('top') ? insets.top : 0,
          paddingBottom: edges.includes('bottom') ? insets.bottom : 0,
        },
        style,
      ]}
    >
      {children}
    </View>
  );
}

export function Card({
  children,
  style,
  tone = 'surface',
  padded = true,
}: {
  children: React.ReactNode;
  style?: StyleProp<ViewStyle>;
  tone?: 'surface' | 'assistant' | 'ember' | 'plain';
  padded?: boolean;
}) {
  const theme = useTheme();
  const skin = {
    surface: { bg: theme.color.surface, border: theme.color.border },
    assistant: { bg: theme.color.sageSoft, border: theme.color.sageBorder },
    ember: { bg: theme.color.emberSoft, border: theme.color.emberBorder },
    plain: { bg: 'transparent', border: 'transparent' },
  }[tone];

  return (
    <View
      style={[
        {
          backgroundColor: skin.bg,
          borderRadius: theme.radius.lg,
          borderWidth: skin.border === 'transparent' ? 0 : 1,
          borderColor: skin.border,
          padding: padded ? theme.space.base : 0,
        },
        style,
      ]}
    >
      {children}
    </View>
  );
}

export function Divider({ inset = 0 }: { inset?: number }) {
  const theme = useTheme();
  return (
    <View
      style={{
        height: StyleSheet.hairlineWidth,
        backgroundColor: theme.color.border,
        marginLeft: inset,
      }}
    />
  );
}

export function SectionHeader({
  title,
  action,
  onAction,
  style,
}: {
  title: string;
  action?: string;
  onAction?: () => void;
  style?: StyleProp<ViewStyle>;
}) {
  const theme = useTheme();
  return (
    <View
      style={[
        {
          flexDirection: 'row',
          alignItems: 'center',
          justifyContent: 'space-between',
          paddingHorizontal: theme.space.lg,
          paddingTop: theme.space.xl,
          paddingBottom: theme.space.sm,
        },
        style,
      ]}
    >
      <Text variant="overline" tone="faint">
        {title.toUpperCase()}
      </Text>
      {action ? (
        <Pressable onPress={onAction} hitSlop={12} accessibilityRole="button">
          <Text variant="caption" tone="muted" weight="600">
            {action}
          </Text>
        </Pressable>
      ) : null}
    </View>
  );
}

/** Small status/category label. Never interactive — use Button for that. */
export function Tag({
  label,
  tone = 'neutral',
  icon,
}: {
  label: string;
  tone?: 'neutral' | 'ember' | 'sage' | 'gold' | 'danger';
  icon?: keyof typeof Ionicons.glyphMap;
}) {
  const theme = useTheme();
  const skin = {
    neutral: { bg: theme.color.surfaceRaised, fg: theme.color.textMuted },
    ember: { bg: theme.color.emberSoft, fg: theme.color.ember },
    sage: { bg: theme.color.sageSoft, fg: theme.color.sage },
    gold: { bg: theme.color.goldSoft, fg: theme.color.gold },
    danger: { bg: theme.color.dangerSoft, fg: theme.color.danger },
  }[tone];

  return (
    <View
      style={{
        flexDirection: 'row',
        alignItems: 'center',
        gap: 4,
        paddingHorizontal: 9,
        paddingVertical: 4,
        borderRadius: theme.radius.sm,
        backgroundColor: skin.bg,
      }}
    >
      {icon ? <Ionicons name={icon} size={12} color={skin.fg} /> : null}
      <Text variant="caption" weight="600" style={{ color: skin.fg, fontSize: 12 }}>
        {label}
      </Text>
    </View>
  );
}

export function EmptyState({
  icon,
  title,
  body,
  children,
}: {
  icon: keyof typeof Ionicons.glyphMap;
  title: string;
  body?: string;
  children?: React.ReactNode;
}) {
  const theme = useTheme();
  return (
    <View
      style={{
        flex: 1,
        alignItems: 'center',
        justifyContent: 'center',
        paddingHorizontal: theme.space.xxl,
        gap: theme.space.md,
      }}
    >
      <View
        style={{
          width: 62,
          height: 62,
          borderRadius: theme.radius.pill,
          backgroundColor: theme.color.surface,
          borderWidth: 1,
          borderColor: theme.color.border,
          alignItems: 'center',
          justifyContent: 'center',
          marginBottom: theme.space.xs,
        }}
      >
        <Ionicons name={icon} size={26} color={theme.color.textFaint} />
      </View>
      <Text variant="title" align="center">
        {title}
      </Text>
      {body ? (
        <Text variant="uiSmall" tone="muted" align="center" style={{ lineHeight: 22 }}>
          {body}
        </Text>
      ) : null}
      {children ? <View style={{ marginTop: theme.space.sm }}>{children}</View> : null}
    </View>
  );
}
