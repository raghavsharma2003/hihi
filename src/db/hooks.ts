import { useCallback, useEffect, useRef, useState } from 'react';

import { subscribeToDb } from './client';
import { getNote, listNotes, listOpenActions } from './notes';
import type { ActionItem, Note, NoteWithDetails } from './types';

export interface QueryState<T> {
  data: T;
  loading: boolean;
  error: Error | null;
  refetch: () => void;
}

/**
 * Runs an async read and re-runs it whenever the local database changes. Every
 * write helper calls `notifyDbChanged`, so a screen stays current without any
 * manual invalidation at the call sites.
 */
export function useDbQuery<T>(
  run: () => Promise<T>,
  initial: T,
  deps: readonly unknown[] = [],
): QueryState<T> {
  const [data, setData] = useState<T>(initial);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  // Guards against a slow earlier query resolving after a newer one and
  // overwriting fresh data with stale data.
  const generation = useRef(0);
  const mounted = useRef(true);

  const execute = useCallback(async () => {
    const gen = ++generation.current;
    try {
      const result = await run();
      if (mounted.current && gen === generation.current) {
        setData(result);
        setError(null);
      }
    } catch (err) {
      if (mounted.current && gen === generation.current) {
        setError(err instanceof Error ? err : new Error(String(err)));
      }
    } finally {
      if (mounted.current && gen === generation.current) setLoading(false);
    }
    // `run` is intentionally excluded: callers pass an inline closure, and the
    // explicit `deps` list is what decides when the query is stale.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, deps);

  useEffect(() => {
    mounted.current = true;
    void execute();
    const unsubscribe = subscribeToDb(() => void execute());
    return () => {
      mounted.current = false;
      unsubscribe();
    };
  }, [execute]);

  return { data, loading, error, refetch: execute };
}

export function useNotes(search?: string, archived = false): QueryState<Note[]> {
  return useDbQuery<Note[]>(() => listNotes({ search, archived }), [], [search, archived]);
}

export function useNote(id: string | undefined): QueryState<NoteWithDetails | null> {
  return useDbQuery<NoteWithDetails | null>(
    () => (id ? getNote(id) : Promise.resolve(null)),
    null,
    [id],
  );
}

export function useOpenActions(): QueryState<(ActionItem & { noteTitle: string })[]> {
  return useDbQuery<(ActionItem & { noteTitle: string })[]>(() => listOpenActions(), [], []);
}
