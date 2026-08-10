"use client";

import { useEffect, useRef } from "react";

/** A stagger step longer than this reads as the page loading, not as rhythm. */
const MAX_DELAY = 240;

/**
 * Scroll reveal that fires once and never re-animates.
 * CSS in globals.css handles motion; reduced-motion renders final state.
 *
 * Firing rule: threshold 0 with a -10% bottom root margin. A percentage
 * threshold never resolves for an element taller than the viewport (a phone
 * reading a full-height section would wait forever); the root margin gives the
 * "slightly inside the fold" feel without that failure mode.
 *
 * Stagger: pass `delay` as `index * 60..80`. It is capped at 240ms so a long
 * list's tail never sits blank.
 */
export default function Reveal({
  children,
  className = "",
  delay = 0,
  as: Tag = "div",
}: {
  children: React.ReactNode;
  className?: string;
  delay?: number;
  as?: "div" | "section" | "li" | "figure" | "p";
}) {
  const ref = useRef<HTMLElement | null>(null);
  const staggerDelay = Math.max(0, Math.min(delay, MAX_DELAY));

  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    const io = new IntersectionObserver(
      (entries) => {
        for (const entry of entries) {
          if (entry.isIntersecting) {
            el.classList.add("is-in");
            io.disconnect();
          }
        }
      },
      { threshold: 0, rootMargin: "0px 0px -10% 0px" },
    );
    io.observe(el);
    return () => io.disconnect();
  }, []);

  return (
    <Tag
      ref={ref as React.RefObject<never>}
      className={`reveal ${className}`}
      style={staggerDelay ? { transitionDelay: `${staggerDelay}ms` } : undefined}
    >
      {children}
    </Tag>
  );
}
