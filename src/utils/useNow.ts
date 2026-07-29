import { useEffect, useState } from 'react';

/**
 * The current time, re-rendering on an interval.
 *
 * Screens that highlight "happening now" need the clock to move, and reading
 * `Date.now()` during render would neither update on its own nor be a pure
 * render. This makes the passage of time an explicit input instead.
 */
export function useNow(intervalMs = 30_000): number {
  const [now, setNow] = useState(() => Date.now());

  useEffect(() => {
    const timer = setInterval(() => setNow(Date.now()), intervalMs);
    return () => clearInterval(timer);
  }, [intervalMs]);

  return now;
}
