"use client";

import { useEffect, useRef, useState } from "react";

const DIGITS = "0123456789";

/**
 * Rolls each digit vertically over 250ms when the value changes.
 * Non-digit characters (₹ , . – L k) render static. Reduced motion: no roll.
 */
export default function Odometer({
  value,
  className = "",
}: {
  value: string;
  className?: string;
}) {
  const [reduced, setReduced] = useState(false);

  useEffect(() => {
    const mq = window.matchMedia("(prefers-reduced-motion: reduce)");
    setReduced(mq.matches);
    const onChange = (e: MediaQueryListEvent) => setReduced(e.matches);
    mq.addEventListener("change", onChange);
    return () => mq.removeEventListener("change", onChange);
  }, []);

  if (reduced) {
    return <span className={`tabular ${className}`}>{value}</span>;
  }

  return (
    <span className={`tabular inline-flex ${className}`} aria-hidden="false">
      {value.split("").map((ch, i) =>
        DIGITS.includes(ch) ? (
          <Digit key={`${i}-d`} digit={Number(ch)} />
        ) : (
          <span key={`${i}-s`}>{ch}</span>
        ),
      )}
    </span>
  );
}

function Digit({ digit }: { digit: number }) {
  const ref = useRef<HTMLSpanElement>(null);

  useEffect(() => {
    const el = ref.current;
    if (el) el.style.transform = `translateY(${-digit}em)`;
  }, [digit]);

  return (
    <span
      className="inline-block overflow-hidden align-baseline"
      style={{ height: "1em", lineHeight: 1 }}
    >
      <span
        ref={ref}
        className="inline-flex flex-col transition-transform duration-[250ms] ease-out"
        style={{ transform: `translateY(${-digit}em)` }}
      >
        {DIGITS.split("").map((d) => (
          <span key={d} style={{ height: "1em", lineHeight: 1 }}>
            {d}
          </span>
        ))}
      </span>
    </span>
  );
}
