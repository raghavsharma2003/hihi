"use client";

import { useEffect, useRef, useState } from "react";
import { PRICES_LADDER } from "@/config/business";
import Eyebrow from "./Eyebrow";

const TONE_FILL: Record<string, string> = {
  current: "bg-sky border border-current/40",
  midnight: "bg-midnight/10 border border-midnight/20",
  sunsave: "bg-sunsave/25 border border-sunsave/60",
  dieselclay: "bg-dieselclay border border-dieselclay",
};

const TONE_TEXT: Record<string, string> = {
  current: "text-current",
  midnight: "text-midnight",
  sunsave: "text-sunsave",
  dieselclay: "text-dieselclay",
};

export default function FourPrices() {
  const ref = useRef<HTMLElement>(null);
  const [grown, setGrown] = useState(false);

  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      setGrown(true);
      return;
    }
    const io = new IntersectionObserver(
      ([e]) => {
        if (e.isIntersecting) {
          setGrown(true);
          io.disconnect();
        }
      },
      { threshold: 0.35 },
    );
    io.observe(el);
    return () => io.disconnect();
  }, []);

  const max = Math.max(...PRICES_LADDER.map((p) => p.value));

  return (
    <section
      ref={ref}
      aria-labelledby="prices-heading"
      className="mx-auto max-w-page px-4 py-section md:px-6"
    >
      <Eyebrow>01 / The problem</Eyebrow>
      <h2
        id="prices-heading"
        className="mt-2 max-w-[24ch] font-display text-40 font-bold tracking-tight md:text-56"
      >
        One unit of electricity, four different prices.
      </h2>

      {/* One shared 3-row grid — ₹ labels / plot / names — rather than four
          independent columns. The label row is reserved, so the tallest bar
          (diesel, 100%) can never shove its ₹28–32 out of the chart and into
          the heading; and because the rows are shared, a name that wraps to
          three lines can't shorten its own bar off the common baseline. */}
      <div
        className="mt-8 grid h-chart grid-rows-[auto_minmax(0,1fr)_auto] gap-x-2 sm:gap-x-4 md:mt-12 md:gap-x-6 lg:gap-x-8"
        style={{
          gridTemplateColumns: `repeat(${PRICES_LADDER.length}, minmax(0, 1fr))`,
        }}
      >
        {PRICES_LADDER.map((p, i) => (
          <p
            key={`v-${p.label}`}
            className={`tabular mb-2 self-end whitespace-nowrap text-center font-mono text-12 font-medium sm:text-14 md:text-22 ${TONE_TEXT[p.tone]} ${grown ? "opacity-100" : "opacity-0"}`}
            style={{ transition: `opacity 400ms cubic-bezier(0.22,1,0.36,1) ${i * 120 + 300}ms` }}
          >
            {p.range}
          </p>
        ))}

        {PRICES_LADDER.map((p, i) => {
          const h = (p.value / max) * 100;
          const isDiesel = p.tone === "dieselclay";
          return (
            <div key={`b-${p.label}`} className="flex min-h-0 items-end">
              <div
                id={isDiesel ? "diesel-bar" : undefined}
                className={`w-full origin-bottom rounded-t-card ${TONE_FILL[p.tone]}`}
                style={{
                  height: `${h}%`,
                  transform: grown ? "scaleY(1)" : "scaleY(0)",
                  transition: `transform 600ms ${
                    isDiesel
                      ? "cubic-bezier(0.34,1.4,0.5,1)"
                      : "cubic-bezier(0.22,1,0.36,1)"
                  } ${i * 120}ms`,
                }}
              />
            </div>
          );
        })}

        {PRICES_LADDER.map((p) => (
          <p
            key={`l-${p.label}`}
            className="mt-3 text-balance text-center text-12 font-semibold leading-snug text-midnight/70 md:text-14"
          >
            {p.label}
          </p>
        ))}
      </div>

      <p className="mx-auto mt-8 max-w-[52ch] text-center text-16 text-midnight/70 md:mt-12 md:text-18">
        Every genset hour is bought at the top of this ladder. Our whole
        business is moving you down it.
      </p>
    </section>
  );
}
