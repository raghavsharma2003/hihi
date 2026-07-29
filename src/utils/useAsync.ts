import { useCallback, useEffect, useRef, useState } from 'react';

export interface AsyncState<T> {
  data: T | null;
  loading: boolean;
  error: Error | null;
  reload: () => void;
}

/**
 * Runs a one-shot async read (a network call, typically) with the usual
 * loading/error plumbing and a manual reload for pull-to-refresh.
 */
export function useAsync<T>(run: () => Promise<T>, deps: readonly unknown[] = []): AsyncState<T> {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  const generation = useRef(0);
  const mounted = useRef(true);

  const execute = useCallback(async () => {
    const gen = ++generation.current;
    setLoading(true);
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
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, deps);

  useEffect(() => {
    mounted.current = true;
    void execute();
    return () => {
      mounted.current = false;
    };
  }, [execute]);

  return { data, loading, error, reload: execute };
}
