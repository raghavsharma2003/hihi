"use client";

import { useEffect, useRef, useState } from "react";
import { BRAND } from "@/config/business";
import { getGsap, prefersReducedMotion } from "@/lib/gsap";
import Eyebrow from "./Eyebrow";

/**
 * S3 — the moment the power cuts. Scroll-pinned briefly; scrub progress
 * drives both halves: without us the windows die and the genset coughs on,
 * with us the battery bridges in ≤20ms and the lifts don't notice.
 */
export default function CutMoment() {
  const sectionRef = useRef<HTMLElement>(null);
  const [p, setP] = useState(0); // 0..1 scrub progress
  const [staticMode, setStaticMode] = useState(false);

  useEffect(() => {
    if (prefersReducedMotion()) {
      setStaticMode(true);
      setP(1);
      return;
    }
    const { ScrollTrigger } = getGsap();
    const el = sectionRef.current;
    if (!el) return;
    const pinned = window.innerWidth >= 768;
    const st = ScrollTrigger.create({
      trigger: el,
      start: pinned ? "top top" : "top 75%",
      end: pinned ? "+=120%" : "bottom 55%",
      pin: pinned,
      scrub: 0.4,
      onUpdate: (self) => setP(self.progress),
    });
    return () => st.kill();
  }, []);

  // phase timings along the pin
  const cutAt = 0.22; // grid snaps
  const gensetAt = 0.55; // genset finally starts
  const cut = p >= cutAt;
  const gensetOn = p >= gensetAt;
  // seconds counter between cut and genset start (0 → 8s)
  const gapSeconds = Math.min(
    8,
    Math.max(0, ((p - cutAt) / (gensetAt - cutAt)) * 8),
  );

  return (
    <section
      ref={sectionRef}
      aria-labelledby="cut-heading"
      className="bg-sky/40 py-16 md:py-0 md:min-h-screen md:flex md:flex-col md:justify-center"
    >
      <div className="mx-auto w-full max-w-page px-4 md:px-6 md:pt-20">
        <Eyebrow>02 / The moment the power cuts</Eyebrow>
        <h2
          id="cut-heading"
          className="mt-2 max-w-[26ch] font-display text-40 font-bold tracking-tight md:text-56"
        >
          Same street. Same cut. Two very different minutes.
        </h2>

        <div className="mt-8 grid gap-4 md:mt-12 md:grid-cols-2 md:gap-8">
          <Half
            title={`Without`}
            cut={cut}
            powered={gensetOn}
            poweredBy="genset"
            gapSeconds={cut && !gensetOn ? gapSeconds : null}
            rate={gensetOn ? "₹32/unit" : cut ? "—" : "₹8/unit"}
            rateTone={gensetOn ? "dieselclay" : "midnight"}
            staticMode={staticMode}
          />
          <Half
            title={`With`}
            cut={cut}
            powered
            poweredBy="battery"
            gapSeconds={null}
            rate={cut ? "₹13/unit" : "₹8/unit"}
            rateTone={cut ? "sunsave" : "midnight"}
            staticMode={staticMode}
          />
        </div>

        <p className="mt-6 max-w-[64ch] text-14 text-midnight/60 md:text-16">
          Long cut? The genset auto-starts as reserve. It stays. We just make
          sure it rarely runs.
        </p>
      </div>
    </section>
  );
}

function Half({
  title,
  cut,
  powered,
  poweredBy,
  gapSeconds,
  rate,
  rateTone,
  staticMode,
}: {
  title: string;
  cut: boolean;
  powered: boolean;
  poweredBy: "genset" | "battery";
  gapSeconds: number | null;
  rate: string;
  rateTone: "dieselclay" | "sunsave" | "midnight";
  staticMode: boolean;
}) {
  const isUs = poweredBy === "battery";
  const windowsLit = !cut || powered;
  const gensetRunning = !isUs && cut && powered;

  return (
    <figure className="rounded-card border border-line bg-surface p-4 shadow-card md:p-6">
      <figcaption className="flex items-baseline justify-between">
        <span className="font-semibold">
          {title}{" "}
          <span className={isUs ? "text-current" : "text-midnight/60"}>
            {BRAND.name}
          </span>
        </span>
        <span
          className={`tabular font-mono text-16 font-medium md:text-22 ${
            rateTone === "dieselclay"
              ? "text-dieselclay"
              : rateTone === "sunsave"
                ? "text-sunsave"
                : "text-midnight"
          }`}
        >
          {rate}
        </span>
      </figcaption>

      <svg
        viewBox="0 0 320 200"
        role="img"
        aria-label={
          isUs
            ? "Building with battery: the grid line snaps but every window stays lit"
            : "Building without battery: the grid line snaps, windows go dark, then a diesel genset starts with smoke"
        }
        className="mt-4 w-full"
      >
        {/* grid line in from the left; snaps on cut */}
        {cut ? (
          <>
            <path d="M0 100 h44" fill="none" stroke="#0A1B2E" strokeWidth="2" strokeLinecap="round" />
            <path d="M58 100 h20" fill="none" stroke="#0A1B2E" strokeWidth="2" strokeDasharray="3 5" opacity="0.4" />
          </>
        ) : (
          <path d="M0 100 h78" fill="none" stroke="#1847C9" strokeWidth="2" />
        )}

        {/* building */}
        <rect x="96" y="40" width="150" height="130" rx="4" fill="#FFFFFF" stroke="#0A1B2E" strokeWidth="2" />
        {[0, 1, 2].map((r) =>
          [0, 1, 2].map((c) => (
            <rect
              key={`${r}${c}`}
              x={112 + c * 42}
              y={56 + r * 34}
              width="26"
              height="22"
              rx="2"
              fill={windowsLit ? "#EFA00B" : "#0A1B2E"}
              opacity={windowsLit ? 0.85 : 0.15}
              stroke="#0A1B2E"
              strokeWidth="2"
              style={{ transition: "fill 250ms, opacity 250ms" }}
            />
          )),
        )}
        {/* lift shaft marker */}
        <rect x="196" y="132" width="34" height="38" rx="2" fill="#E4EDFB" stroke="#0A1B2E" strokeWidth="2" />
        <path d="M208 146 l5 -6 l5 6 M208 156 l5 6 l5 -6" fill="none" stroke="#0A1B2E" strokeWidth="2" strokeLinecap="round" />

        {isUs ? (
          <g>
            {/* battery cabinet bridging instantly */}
            <rect
              x="256" y="112" width="44" height="58" rx="6"
              fill="#E4EDFB" stroke="#1847C9" strokeWidth="2"
            />
            <rect x="264" y="122" width="28" height="7" rx="2" fill="#1847C9" />
            <rect x="264" y="134" width="28" height="7" rx="2" fill="#1847C9" opacity="0.7" />
            <rect x="264" y="146" width="28" height="7" rx="2" fill="#1847C9" opacity="0.4" />
            <path
              d="M246 100 h10 v40"
              fill="none"
              stroke={cut ? "#1847C9" : "#DFE5EE"}
              strokeWidth="2"
              style={{ transition: "stroke 150ms" }}
            />
          </g>
        ) : (
          <g
            style={
              gensetRunning && !staticMode
                ? { animation: "gensetShake 300ms linear infinite" }
                : undefined
            }
          >
            <rect x="256" y="132" width="52" height="38" rx="6" fill="#FFFFFF" stroke="#0A1B2E" strokeWidth="2" />
            <rect x="262" y="140" width="20" height="20" rx="2" fill="#E4EDFB" stroke="#0A1B2E" strokeWidth="2" />
            <circle cx="294" cy="150" r="6" fill={gensetRunning ? "#B3402F" : "#FFFFFF"} stroke="#0A1B2E" strokeWidth="2" style={{ transition: "fill 250ms" }} />
            {gensetRunning && (
              <>
                <path d="M300 132 v-10 h6" fill="none" stroke="#0A1B2E" strokeWidth="2" />
                <path d="M308 118 c 6 -6 0 -12 8 -18" fill="none" stroke="#B3402F" strokeWidth="2" strokeLinecap="round" opacity="0.7" />
              </>
            )}
          </g>
        )}
      </svg>

      <div className="mt-3 flex min-h-[3.5rem] items-center">
        {isUs ? (
          <p className="font-mono text-14 md:text-16">
            <span className="font-medium text-current">≤20 ms.</span>{" "}
            <span className="text-midnight/70">
              The lifts don&apos;t even notice.
            </span>
          </p>
        ) : gapSeconds !== null ? (
          <p className="tabular font-mono text-14 text-dieselclay md:text-16">
            dark for {gapSeconds.toFixed(1)}s… genset cranking
          </p>
        ) : cut ? (
          <p className="font-mono text-14 text-midnight/70 md:text-16">
            genset running · smoke, noise, ₹32 metered
          </p>
        ) : (
          <p className="font-mono text-14 text-midnight/50 md:text-16">
            grid up · everything normal
          </p>
        )}
      </div>
    </figure>
  );
}
