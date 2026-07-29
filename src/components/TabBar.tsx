import { Ionicons } from '@expo/vector-icons';
import * as Haptics from 'expo-haptics';
import { useRouter } from 'expo-router';
import type { BottomTabBarProps } from 'expo-router/js-tabs';
import React from 'react';
import { Pressable, View } from 'react-native';
import Animated, { useAnimatedStyle, useSharedValue, withSpring } from 'react-native-reanimated';
import { useSafeAreaInsets } from 'react-native-safe-area-context';

import { Text } from './Text';
import { useTheme } from '@/theme';

const ICONS: Record<string, { on: keyof typeof Ionicons.glyphMap; off: keyof typeof Ionicons.glyphMap }> =
  {
    index: { on: 'albums', off: 'albums-outline' },
    today: { on: 'today', off: 'today-outline' },
    inbox: { on: 'mail', off: 'mail-outline' },
    settings: { on: 'settings', off: 'settings-outline' },
  };

const LABELS: Record<string, string> = {
  index: 'Notes',
  today: 'Today',
  inbox: 'Inbox',
  settings: 'Settings',
};

const AnimatedPressable = Animated.createAnimatedComponent(Pressable);

/**
 * Recording is the reason the app exists, so it gets the centre of the bar
 * rather than a corner button — reachable with either thumb, from any tab, at
 * the moment a thought arrives.
 */
function RecordButton() {
  const theme = useTheme();
  const router = useRouter();
  const scale = useSharedValue(1);
  const animated = useAnimatedStyle(() => ({ transform: [{ scale: scale.value }] }));

  return (
    <AnimatedPressable
      accessibilityRole="button"
      accessibilityLabel="Record a voice note"
      accessibilityHint="Opens the recorder and starts listening"
      onPress={() => {
        void Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium);
        router.push('/capture');
      }}
      onPressIn={() => {
        scale.value = withSpring(0.92, theme.motion.press);
      }}
      onPressOut={() => {
        scale.value = withSpring(1, theme.motion.press);
      }}
      style={[
        animated,
        theme.shadow('high'),
        {
          width: 62,
          height: 62,
          borderRadius: 31,
          backgroundColor: theme.color.ember,
          alignItems: 'center',
          justifyContent: 'center',
          marginTop: -26,
        },
      ]}
    >
      <Ionicons name="mic" size={27} color="#FFFFFF" />
    </AnimatedPressable>
  );
}

function TabItem({
  routeName,
  focused,
  onPress,
}: {
  routeName: string;
  focused: boolean;
  onPress: () => void;
}) {
  const theme = useTheme();
  const icons = ICONS[routeName];
  if (!icons) return <View style={{ flex: 1 }} />;

  return (
    <Pressable
      accessibilityRole="tab"
      accessibilityState={{ selected: focused }}
      accessibilityLabel={LABELS[routeName]}
      onPress={onPress}
      style={{ flex: 1, alignItems: 'center', justifyContent: 'center', gap: 3, paddingTop: 10 }}
    >
      <Ionicons
        name={focused ? icons.on : icons.off}
        size={21}
        color={focused ? theme.color.text : theme.color.textFaint}
      />
      <Text
        variant="caption"
        style={{ fontSize: 10.5, color: focused ? theme.color.text : theme.color.textFaint }}
        weight={focused ? '600' : '500'}
      >
        {LABELS[routeName]}
      </Text>
    </Pressable>
  );
}

export function TabBar({ state, navigation }: BottomTabBarProps) {
  const theme = useTheme();
  const insets = useSafeAreaInsets();

  const left = state.routes.filter((r) => r.name === 'index' || r.name === 'today');
  const right = state.routes.filter((r) => r.name === 'inbox' || r.name === 'settings');

  const renderItem = (route: (typeof state.routes)[number]) => {
    const index = state.routes.findIndex((r) => r.key === route.key);
    const focused = state.index === index;
    return (
      <TabItem
        key={route.key}
        routeName={route.name}
        focused={focused}
        onPress={() => {
          const event = navigation.emit({ type: 'tabPress', target: route.key, canPreventDefault: true });
          if (!focused && !event.defaultPrevented) navigation.navigate(route.name);
        }}
      />
    );
  };

  return (
    <View
      style={{
        flexDirection: 'row',
        alignItems: 'flex-start',
        backgroundColor: theme.color.bg,
        borderTopWidth: 1,
        borderTopColor: theme.color.border,
        paddingBottom: Math.max(insets.bottom, 10),
        paddingHorizontal: theme.space.xs,
      }}
    >
      {left.map(renderItem)}
      <View style={{ width: 78, alignItems: 'center' }}>
        <RecordButton />
      </View>
      {right.map(renderItem)}
    </View>
  );
}
