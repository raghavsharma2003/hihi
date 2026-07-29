import { Ionicons } from '@expo/vector-icons';
import React, { useCallback, useMemo, useState } from 'react';
import { SectionList, TextInput, View } from 'react-native';

import { EmptyState, Screen } from '@/components/Layout';
import { NoteCard } from '@/components/NoteCard';
import { Text } from '@/components/Text';
import { useNotes } from '@/db/hooks';
import { setArchived, setPinned } from '@/db/notes';
import type { Note } from '@/db/types';
import { useTheme } from '@/theme';
import { dateGroupLabel } from '@/utils/time';

interface Section {
  title: string;
  data: Note[];
}

/**
 * Pinned notes are their own section at the top; everything else is grouped by
 * recency. Grouping by day is what makes a long list scannable — a flat feed of
 * timestamps is not.
 */
function groupNotes(notes: Note[]): Section[] {
  const pinned = notes.filter((n) => n.pinned);
  const rest = notes.filter((n) => !n.pinned);

  const sections: Section[] = [];
  if (pinned.length > 0) sections.push({ title: 'Pinned', data: pinned });

  let current: Section | null = null;
  for (const note of rest) {
    const label = dateGroupLabel(note.createdAt);
    if (!current || current.title !== label) {
      current = { title: label, data: [] };
      sections.push(current);
    }
    current.data.push(note);
  }
  return sections;
}

export default function NotesScreen() {
  const theme = useTheme();
  const [search, setSearch] = useState('');
  const [searching, setSearching] = useState(false);

  const { data: notes, loading } = useNotes(search);
  const sections = useMemo(() => groupNotes(notes), [notes]);

  const handleArchive = useCallback((id: string) => void setArchived(id, true), []);
  const handlePin = useCallback((id: string, pinned: boolean) => void setPinned(id, pinned), []);

  const showEmpty = !loading && notes.length === 0;

  return (
    <Screen>
      {/* Header */}
      <View
        style={{
          paddingHorizontal: theme.space.lg,
          paddingTop: theme.space.sm,
          paddingBottom: theme.space.md,
          flexDirection: 'row',
          alignItems: 'center',
          justifyContent: 'space-between',
        }}
      >
        <Text variant="display">Notes</Text>
        <Ionicons
          name={searching ? 'close' : 'search'}
          size={22}
          color={theme.color.textMuted}
          onPress={() => {
            setSearching((was) => !was);
            if (searching) setSearch('');
          }}
          accessibilityRole="button"
          accessibilityLabel={searching ? 'Close search' : 'Search notes'}
          style={{ padding: 11 }}
        />
      </View>

      {searching ? (
        <View style={{ paddingHorizontal: theme.space.lg, paddingBottom: theme.space.md }}>
          <TextInput
            autoFocus
            value={search}
            onChangeText={setSearch}
            placeholder="Search words you said…"
            placeholderTextColor={theme.color.textFaint}
            returnKeyType="search"
            clearButtonMode="while-editing"
            accessibilityLabel="Search notes"
            style={{
              backgroundColor: theme.color.surface,
              borderWidth: 1,
              borderColor: theme.color.border,
              borderRadius: theme.radius.md,
              paddingHorizontal: theme.space.md,
              height: 44,
              color: theme.color.text,
              fontFamily: theme.type.ui.fontFamily,
              fontSize: theme.type.ui.fontSize,
            }}
          />
        </View>
      ) : null}

      {showEmpty ? (
        search ? (
          <EmptyState
            icon="search-outline"
            title="Nothing matches"
            body={`No note mentions “${search}”. Echo searches every word you have said, so try a different phrase.`}
          />
        ) : (
          <EmptyState
            icon="mic-outline"
            title="Say something"
            body="Tap the microphone and start talking. Echo keeps the recording and the transcript, then pulls out what you need to do."
          />
        )
      ) : (
        <SectionList
          sections={sections}
          keyExtractor={(item) => item.id}
          renderItem={({ item }) => (
            <NoteCard note={item} onArchive={handleArchive} onTogglePin={handlePin} />
          )}
          renderSectionHeader={({ section }) => (
            <View
              style={{
                backgroundColor: theme.color.bg,
                paddingHorizontal: theme.space.lg,
                paddingTop: theme.space.lg,
                paddingBottom: theme.space.sm,
              }}
            >
              <Text variant="overline" tone="faint">
                {section.title.toUpperCase()}
              </Text>
            </View>
          )}
          ItemSeparatorComponent={() => (
            <View style={{ height: 1, backgroundColor: theme.color.border, marginLeft: theme.space.lg }} />
          )}
          contentContainerStyle={{ paddingBottom: theme.space.xxxl }}
          stickySectionHeadersEnabled
          keyboardDismissMode="on-drag"
          keyboardShouldPersistTaps="handled"
          showsVerticalScrollIndicator={false}
        />
      )}
    </Screen>
  );
}
