import { useRouter } from 'expo-router';
import React, { useCallback } from 'react';
import { FlatList, View } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';

import { IconButton } from '@/components/Button';
import { EmptyState } from '@/components/Layout';
import { NoteCard } from '@/components/NoteCard';
import { Text } from '@/components/Text';
import { useNotes } from '@/db/hooks';
import { setArchived, setPinned } from '@/db/notes';
import { useTheme } from '@/theme';

export default function ArchiveScreen() {
  const theme = useTheme();
  const router = useRouter();
  const insets = useSafeAreaInsets();
  const { data: notes, loading } = useNotes(undefined, true);

  // In the archive, the swipe action restores rather than archives again.
  const handleRestore = useCallback((id: string) => void setArchived(id, false), []);
  const handlePin = useCallback((id: string, pinned: boolean) => void setPinned(id, pinned), []);

  return (
    <View style={{ flex: 1, backgroundColor: theme.color.bg, paddingTop: insets.top }}>
      <View
        style={{
          flexDirection: 'row',
          alignItems: 'center',
          gap: theme.space.xs,
          paddingHorizontal: theme.space.xs,
          paddingBottom: theme.space.sm,
        }}
      >
        <IconButton icon="chevron-back" accessibilityLabel="Back" onPress={() => router.back()} />
        <Text variant="title">Archive</Text>
      </View>

      {!loading && notes.length === 0 ? (
        <EmptyState
          icon="archive-outline"
          title="Nothing archived"
          body="Swipe a note left in your list to tuck it away here."
        />
      ) : (
        <FlatList
          data={notes}
          keyExtractor={(item) => item.id}
          renderItem={({ item }) => (
            <NoteCard note={item} onArchive={handleRestore} onTogglePin={handlePin} />
          )}
          ItemSeparatorComponent={() => (
            <View
              style={{ height: 1, backgroundColor: theme.color.border, marginLeft: theme.space.lg }}
            />
          )}
          contentContainerStyle={{ paddingBottom: insets.bottom + theme.space.xxl }}
          showsVerticalScrollIndicator={false}
        />
      )}
    </View>
  );
}
