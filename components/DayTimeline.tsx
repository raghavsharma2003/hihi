"use client";

import { useEffect, useRef, useState } from "react";
import { getGsap, MQ } from "@/lib/gsap";
import Eyebrow from "./Eyebrow";

/**
 * S4 — a day at your site. Desktop: pinned for ~1.4 viewport-heights, the
 * sun/moon scrubs across a 24h timeline as the battery charges cheap and
 * serves peak. Mobile: same timeline, tap-to-step. Reduced motion: static
 * evening state with every annotation visible.
 *
 * The pin starts at "top top" and the section reserves NAV_HEIGHT of top
 * padding (md:pt-[72px]) so the fixed nav never covers the clock; the timeline
 * art is height-capped so the whole scene fits a 768px-tall viewport.
 */

const CUT_HOUR = 13.5;

const STEPS = [
  { hour: 6, label: "06:00" },
  { hour: 12, label: "12:00" },
  { hour: 13.6, label: "13:36" },
  { hour: 20, label: "20:00" },
];

/** battery state of charge (0..1) across the day */
function socAt(h: number): number {
  let soc: number;
  if (h < 9) soc = 0.6;
  else if (h < 17) soc = 0.6 + ((h - 9) / 8) * 0.35;
  else if (h < 18) soc = 0.95;
  else if (h < 23) soc = 0.95 - ((h - 18) / 5) * 0.6;
  else soc = 0.35 + ((h - 23) / 1) * 0.05;
  // surprise cut: a sharp draw for ~40 minutes
  if (h >= CUT_HOUR && h < CUT_HOUR + 0.7) {
    soc -= 0.12 * Math.min(1, (h - CUT_HOUR) / 0.3);
  } else if (h >= CUT_HOUR + 0.7 && h < 17) {
    soc -= 0.12 * Math.max(0, 1 - (h - CUT_HOUR - 0.7) / 1.5);
  }
  return Math.max(0.32, Math.min(0.95, soc));
}

type Phase = "night" | "charging" | "cut" | "shoulder" | "peak";

function phaseAt(h: number): Phase {
  if (h >= CUT_HOUR && h < CUT_HOUR + 0.7) return "cut";
  if (h >= 9 && h < 17) return "charging";
  if (h >= 18 && h < 23) return "peak";
  if (h >= 17 && h < 18) return "shoulder";
  return "night";
}

const PHASE_COPY: Record<Phase, { text: string; tone: string }> = {
  night: { text: "grid hours · battery resting", tone: "text-midnight/60" },
  charging: { text: "charging at ₹6.4 — the cheap band", tone: "text-current" },
  cut: {
    text: "surprise cut = our best-paid hour (₹21/unit vs ₹1)",
    tone: "text-sunsave",
  },
  shoulder: { text: "topped up, waiting for peak", tone: "text-midnight/60" },
  peak: { text: "serving at peak, not buying it", tone: "text-sunsave" },
};

export default function DayTimeline() {
  const sectionRef = useRef<HTMLElement>(null);
  const [hour, setHour] = useState(6);
  const [isMobile, setIsMobile] = useState(false);
  const [staticMode, setStaticMode] = useState(false);
  const [stepIdx, setStepIdx] = useState(0);
  const hourProxy = useRef({ h: 6 });

  useEffect(() => {
    const { gsap, ScrollTrigger } = getGsap();
    const el = sectionRef.current;
    if (!el) return;

    const mm = gsap.matchMedia();
    mm.add(MQ, (context) => {
      const reduced = Boolean(context.conditions?.reduced);
      const desktop = Boolean(context.conditions?.desktop);

      setStaticMode(reduced);
      setIsMobile(!reduced && !desktop);

      if (reduced) {
        setHour(20);
        return;
      }
      // Mobile keeps the tap-to-step buttons instead of a scrub.
      if (!desktop) return;

      ScrollTrigger.create({
        trigger: el,
        start: "top top",
        // ~1.4 viewport-heights for a full 24h sweep.
        end: () => `+=${Math.round(window.innerHeight * 1.4)}`,
        pin: true,
        anticipatePin: 1,
        // Lenis smooths the scroll itself — keep the scrub short or the sun
        // lags visibly behind the pointer.
        scrub: 0.5,
        invalidateOnRefresh: true,
        onUpdate: (self) => setHour(self.progress * 24),
        onRefresh: (self) => setHour(self.progress * 24),
      });
    });

    return () => mm.revert();
  }, []);

  const goToStep = (i: number) => {
    setStepIdx(i);
    if (staticMode) {
      setHour(STEPS[i].hour);
      return;
    }
    const { gsap } = getGsap();
    gsap.to(hourProxy.current, {
      h: STEPS[i].hour,
      duration: 0.6,
      ease: "power3.out",
      onUpdate: () => setHour(hourProxy.current.h),
    });
  };

  const phase = phaseAt(hour);
  const soc = socAt(hour);
  const hh = Math.floor(hour) % 24;
  const mm = Math.floor((hour % 1) * 60);
  const clock = `${String(hh).padStart(2, "0")}:${String(mm).padStart(2, "0")}`;

  return (
    <section
      ref={sectionRef}
      id="how-it-works"
      aria-labelledby="day-heading"
      className="scroll-mt-24 py-16 md:flex md:min-h-screen md:flex-col md:justify-center md:pb-8 md:pt-[72px]"
    >
      <div className="mx-auto w-full max-w-page px-4 md:px-6">
        <Eyebrow>03 / How it works</Eyebrow>
        <div className="mt-2 flex flex-wrap items-end justify-between gap-4">
          <h2
            id="day-heading"
            className="max-w-[22ch] font-display text-40 font-bold tracking-tight md:text-56"
          >
            A day at your site.
          </h2>
          <p className="tabular font-mono text-28 font-medium text-current md:text-40">
            {clock}
          </p>
        </div>

        <div className="overflow-x-auto">
          <div className="min-w-[640px]">
            <TimelineSvg hour={hour} soc={soc} phase={phase} />
          </div>
        </div>

        <p
          aria-live="polite"
          className={`mt-4 min-h-[1.6em] font-mono text-14 font-medium md:text-16 ${PHASE_COPY[phase].tone}`}
        >
          {PHASE_COPY[phase].text}
        </p>

        {(isMobile || staticMode) && (
          <div className="mt-6 flex flex-wrap gap-2" role="group" aria-label="Step through the day">
            {STEPS.map((s, i) => (
              <button
                key={s.label}
                onClick={() => goToStep(i)}
                aria-pressed={stepIdx === i}
                className={`rounded-full border px-4 py-2 font-mono text-14 transition-colors duration-150 ${
                  stepIdx === i
                    ? "border-current bg-current text-surface"
                    : "border-line bg-surface text-midnight/70"
                }`}
              >
                {s.label}
              </button>
            ))}
          </div>
        )}

        <p className="mt-6 max-w-[62ch] text-14 text-midnight/60 md:mt-4 md:text-16">
          The hatched floor of the battery never drains — always reserved for
          cuts, sized from your site&apos;s own 30-day cut log.
        </p>
      </div>
    </section>
  );
}

function TimelineSvg({
  hour,
  soc,
  phase,
}: {
  hour: number;
  soc: number;
  phase: Phase;
}) {
  const W = 800;
  const x = (h: number) => (h / 24) * W;
  const sunUp = hour >= 6 && hour <= 18.5;
  // celestial arc across the sky strip
  const arcY = (h: number, up: boolean) => {
    const t = up ? (h - 6) / 12.5 : ((h + 24 - 18.5) % 24) / 11.5;
    return 64 - Math.sin(Math.PI * Math.min(1, Math.max(0, t))) * 40;
  };

  const battX = 620;
  const battY = 84;
  const battH = 100;
  const battW = 64;
  const lockedFrac = 0.3;
  const socTop = battY + battH - soc * battH;
  const serving = phase === "peak" || phase === "cut";
  const charging = phase === "charging";

  return (
    <svg
      viewBox="0 0 800 320"
      role="img"
      aria-label="24-hour timeline: the battery charges from the grid in the cheap daytime band, then serves the building through the evening peak; a hatched reserve at the bottom of the battery never drains"
      className="mt-6 w-full md:mt-4 md:max-h-[42vh]"
    >
      <defs>
        <pattern id="lockhatch" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
          <rect width="8" height="8" fill="#E4EDFB" />
          <line x1="0" y1="0" x2="0" y2="8" stroke="#1847C9" strokeWidth="2" />
        </pattern>
        <clipPath id="battclip">
          <rect x={battX} y={battY} width={battW} height={battH} rx="6" />
        </clipPath>
      </defs>

      {/* ── sun / moon ── */}
      {sunUp ? (
        <g>
          <circle cx={x(hour)} cy={arcY(hour, true)} r="12" fill="#EFA00B" />
          {[0, 45, 90, 135, 180, 225, 270, 315].map((a) => (
            <line
              key={a}
              x1={x(hour) + 16 * Math.cos((a * Math.PI) / 180)}
              y1={arcY(hour, true) + 16 * Math.sin((a * Math.PI) / 180)}
              x2={x(hour) + 21 * Math.cos((a * Math.PI) / 180)}
              y2={arcY(hour, true) + 21 * Math.sin((a * Math.PI) / 180)}
              stroke="#EFA00B"
              strokeWidth="2"
              strokeLinecap="round"
            />
          ))}
        </g>
      ) : (
        <path
          d={`M ${x(hour % 24)} ${arcY(hour % 24, false) - 12}
              a 12 12 0 1 0 8 21 a 10 10 0 1 1 -8 -21 z`}
          fill="#E4EDFB"
          stroke="#0A1B2E"
          strokeWidth="2"
        />
      )}

      {/* ── tariff band (cost over the day) ── */}
      <g>
        {/* baseline */}
        <line x1="0" y1="260" x2={W} y2="260" stroke="#DFE5EE" strokeWidth="2" />
        {/* stepped tariff area: mid → cheap dip → peak → mid */}
        <path
          d={`M0 226 H${x(9)} V244 H${x(17)} V226 H${x(18)} V198 H${x(23)} V226 H${W} V260 H0 Z`}
          fill="#E4EDFB"
          opacity="0.9"
        />
        {/* peak segment carries cost colour */}
        <rect x={x(18)} y="198" width={x(23) - x(18)} height="62" fill="#B3402F" opacity="0.14" />
        <path
          d={`M0 226 H${x(9)} V244 H${x(17)} V226 H${x(18)} V198 H${x(23)} V226 H${W}`}
          fill="none"
          stroke="#0A1B2E"
          strokeWidth="2"
          strokeLinejoin="round"
        />
        {/* band labels */}
        <text x={x(13)} y="238" textAnchor="middle" fontSize="12" fill="#1847C9" fontFamily="var(--font-mono)">cheap ₹6.4</text>
        <text x={x(20.5)} y="192" textAnchor="middle" fontSize="12" fill="#B3402F" fontFamily="var(--font-mono)">peak</text>
        {/* hour ticks */}
        {[0, 6, 12, 18, 24].map((h) => (
          <g key={h}>
            <line x1={x(h)} y1="260" x2={x(h)} y2="266" stroke="#0A1B2E" strokeWidth="2" />
            <text x={x(h)} y="282" textAnchor={h === 0 ? "start" : h === 24 ? "end" : "middle"} fontSize="12" fill="#0A1B2E" opacity="0.55" fontFamily="var(--font-mono)">
              {String(h % 24).padStart(2, "0")}:00
            </text>
          </g>
        ))}
        {/* cut event marker */}
        <g>
          <line x1={x(CUT_HOUR)} y1="226" x2={x(CUT_HOUR)} y2="266" stroke="#B3402F" strokeWidth="2" strokeDasharray="4 4" />
          <circle cx={x(CUT_HOUR)} cy="222" r="5" fill="#B3402F" />
          <text x={x(CUT_HOUR)} y="302" textAnchor="middle" fontSize="12" fill="#B3402F" fontFamily="var(--font-mono)">cut</text>
        </g>
        {/* now marker */}
        <line x1={x(hour)} y1="200" x2={x(hour)} y2="260" stroke="#1847C9" strokeWidth="2" />
      </g>

      {/* ── battery ↔ building mini-scene (right) ── */}
      <g>
        {/* battery shell */}
        <rect x={battX} y={battY} width={battW} height={battH} rx="6" fill="#FFFFFF" stroke="#1847C9" strokeWidth="2" />
        {/* charge fill */}
        <g clipPath="url(#battclip)">
          <rect
            x={battX}
            y={socTop}
            width={battW}
            height={battY + battH - socTop}
            fill="#1847C9"
            opacity="0.25"
          />
          {/* locked reserve */}
          <rect
            x={battX}
            y={battY + battH * (1 - lockedFrac)}
            width={battW}
            height={battH * lockedFrac}
            fill="url(#lockhatch)"
          >
            <title>
              always reserved for cuts — sized from your site&apos;s own 30-day
              cut log
            </title>
          </rect>
        </g>
        {/* SoC line */}
        <line x1={battX} y1={socTop} x2={battX + battW} y2={socTop} stroke="#1847C9" strokeWidth="2" />
        <text x={battX + battW / 2} y={battY - 10} textAnchor="middle" fontSize="12" fill="#0A1B2E" opacity="0.6" fontFamily="var(--font-mono)">
          battery {Math.round(soc * 100)}%
        </text>

        {/* flow arrow: grid→battery when charging, battery→building when serving */}
        {charging && (
          <g stroke="#1847C9" strokeWidth="2" fill="none">
            <path d={`M${battX - 46} ${battY + 50} h34`} />
            <path d={`M${battX - 18} ${battY + 44} l6 6 l-6 6`} />
          </g>
        )}
        {serving && (
          <g stroke="#EFA00B" strokeWidth="2" fill="none">
            <path d={`M${battX + battW} ${battY + 50} h30`} />
            <path d={`M${battX + battW + 24} ${battY + 44} l6 6 l-6 6`} />
          </g>
        )}

        {/* building */}
        <rect x={battX + battW + 40} y={battY + 10} width="70" height="90" rx="4" fill="#FFFFFF" stroke="#0A1B2E" strokeWidth="2" />
        {[0, 1, 2].map((r) => (
          <rect
            key={r}
            x={battX + battW + 52}
            y={battY + 20 + r * 26}
            width="18"
            height="16"
            rx="2"
            fill={serving ? "#EFA00B" : "#E4EDFB"}
            opacity={serving ? 0.85 : 0.6}
            stroke="#0A1B2E"
            strokeWidth="2"
          />
        ))}
      </g>
    </svg>
  );
}
