import type { Metadata } from "next";
import { BRAND, CALC } from "@/config/business";

export const metadata: Metadata = {
  title: `${BRAND.name} — Design tokens`,
};

const COLORS = [
  { name: "--daylight", hex: "#F6F8FB", role: "page background (cool light paper)" },
  { name: "--surface", hex: "#FFFFFF", role: "cards, calculator panel" },
  { name: "--midnight", hex: "#0A1B2E", role: "all text, dark sections — never pure black" },
  { name: "--current", hex: "#1847C9", role: "PRIMARY: us, the grid done right, everything interactive" },
  { name: "--sky", hex: "#E4EDFB", role: "washes, section tints, illustration fills" },
  { name: "--sunsave", hex: "#EFA00B", role: "ONLY savings numbers and solar — money glows warm" },
  { name: "--dieselclay", hex: "#B3402F", role: "ONLY diesel, cost, waste — never decorative" },
  { name: "border", hex: "#DFE5EE", role: "1px borders everywhere (the current line alone is 2px)" },
];

/**
 * The live scale. Keys never change; values above 22 are fluid, so one class
 * covers every viewport. Line-height and tracking ship inside each token —
 * tracking is size-specific, tightening as the type grows.
 */
const SCALE = [
  { key: "12", cls: "text-12", css: "0.75rem", lh: "1.5", tr: "+0.005em", role: "chips, legal, axis" },
  { key: "14", cls: "text-14", css: "0.875rem", lh: "1.55", tr: "+0.002em", role: "captions, nav, tables" },
  { key: "16", cls: "text-16", css: "1rem", lh: "1.6", tr: "0", role: "body, buttons" },
  { key: "18", cls: "text-18", css: "1.125rem", lh: "1.6", tr: "0", role: "body from md up" },
  { key: "22", cls: "text-22", css: "1.375rem", lh: "1.4", tr: "-0.01em", role: "lede, card titles, brand" },
  {
    key: "28",
    cls: "text-28",
    css: "clamp(1.375rem, 1.15rem + 0.95vw, 1.75rem)",
    lh: "1.18",
    tr: "-0.015em",
    role: "₹ figures, h3 — 22 → 28px",
  },
  {
    key: "40",
    cls: "text-40",
    css: "clamp(1.65rem, 1.2rem + 1.8vw, 2.5rem)",
    lh: "1.1",
    tr: "-0.02em",
    role: "section heads, base — 26 → 40px",
  },
  {
    key: "56",
    cls: "text-56",
    css: "clamp(2.125rem, 0.55rem + 3.55vw, 3.5rem)",
    lh: "1.06",
    tr: "-0.025em",
    role: "section heads, md up — 34 → 56px",
  },
  {
    key: "88",
    cls: "text-88",
    css: "clamp(2.625rem, 1.55rem + 4.8vw, 5.5rem)",
    lh: "1.04",
    tr: "-0.03em",
    role: "hero only — 42 → 88px",
  },
];

const GAPS = [8, 16, 24, 40, 64, 96, 160];

const FLUID_SPACE = [
  { name: "py-section", css: "clamp(4rem, 2.65rem + 5.9vw, 6rem)", role: "every section band: 64px → 96px" },
  { name: "pt-hero-top", css: "clamp(7rem, 5.2rem + 8vw, 10rem)", role: "hero clearance under the fixed nav" },
  { name: "h-chart", css: "clamp(17rem, 14.9rem + 9.5vw, 22.5rem)", role: "price-ladder plot height" },
];

export default function DesignTokens() {
  return (
    <main className="mx-auto max-w-page px-4 py-section md:px-6">
      <p className="font-mono text-12 font-medium uppercase tracking-[0.14em] text-current">
        {BRAND.name} design system
      </p>
      <h1 className="mt-2 font-display text-40 font-bold tracking-tight md:text-56">
        Tokens
      </h1>
      <p className="mt-4 max-w-[62ch] text-16 text-midnight/75 md:text-18">
        Colors mean things here — money saved glows warm, money burned is clay,
        everything interactive is current blue. That consistency is the visual
        language. Every value on this page is defined once, in{" "}
        <code className="font-mono text-14">tailwind.config.ts</code> and{" "}
        <code className="font-mono text-14">config/business.ts</code>.
      </p>

      <h2 className="mt-16 font-display text-28 font-bold tracking-tight">Palette</h2>
      <div className="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {COLORS.map((c) => (
          <div key={c.name} className="overflow-hidden rounded-card border border-line bg-surface shadow-card">
            <div className="h-20" style={{ backgroundColor: c.hex }} />
            <div className="p-4">
              <p className="font-mono text-14 font-medium">{c.name}</p>
              <p className="font-mono text-12 text-midnight/70">{c.hex}</p>
              <p className="mt-2 text-14 text-midnight/75">{c.role}</p>
            </div>
          </div>
        ))}
      </div>

      <h2 className="mt-16 font-display text-28 font-bold tracking-tight">Type</h2>
      <div className="mt-6 grid gap-6 rounded-card border border-line bg-surface p-6 shadow-card">
        <div>
          <p className="font-mono text-12 uppercase tracking-[0.08em] text-midnight/70">
            display · Bricolage Grotesque 700/800 · tracking −0.02em to −0.03em
          </p>
          <p className="mt-1 font-display text-40 font-bold tracking-tight">
            Your genset sells you power.
          </p>
        </div>
        <div>
          <p className="font-mono text-12 uppercase tracking-[0.08em] text-midnight/70">
            body · IBM Plex Sans 400/600 · 16–18px fluid · 1.6 · tracking 0
          </p>
          <p className="mt-1 max-w-[68ch] text-18">
            We serve the same hour at ₹13 — from a battery we design, our
            software runs, and a contract guarantees.
          </p>
        </div>
        <div>
          <p className="font-mono text-12 uppercase tracking-[0.08em] text-midnight/70">
            data · IBM Plex Mono · every ₹ figure, unit, label chip, axis
          </p>
          <p className="tabular mt-1 font-mono text-28 font-medium text-sunsave">
            ₹24,310/mo saved
          </p>
        </div>
      </div>

      <h2 className="mt-16 font-display text-28 font-bold tracking-tight">Scale</h2>
      <p className="mt-3 max-w-[68ch] text-16 text-midnight/75">
        Nine keys, unchanged. 12–22 are fixed — UI text should not shrink. 28
        and up are fluid: the specimen below is rendered with the real class,
        so it resizes as you resize this window. No display size is ever set
        per breakpoint.
      </p>
      <div className="mt-6 rounded-card border border-line bg-surface p-6 shadow-card">
        {SCALE.map((s) => (
          <div
            key={s.key}
            className="grid gap-2 border-b border-line py-4 last:border-0 last:pb-0 md:grid-cols-[9rem_minmax(0,1fr)]"
          >
            <p className="font-mono text-12 text-midnight/70">
              <span className="tabular font-medium text-midnight">text-{s.key}</span>
              <br />
              {s.lh} / {s.tr}
            </p>
            <div className="min-w-0">
              <p className={`truncate font-display font-bold ${s.cls}`}>
                ₹32 a unit
              </p>
              <p className="mt-2 font-mono text-12 text-midnight/70">
                {s.css} · {s.role}
              </p>
            </div>
          </div>
        ))}
      </div>

      <h2 className="mt-16 font-display text-28 font-bold tracking-tight">Spacing · layout</h2>
      <div className="mt-6 rounded-card border border-line bg-surface p-6 shadow-card">
        <p className="text-16 text-midnight/75">
          12-column grid, max-width 1200px, 8px base. Page gutters are fixed —
          16px, 24px from md — so every section&apos;s left edge lines up.
          Allowed gaps only:
        </p>
        <div className="mt-4 flex flex-wrap items-end gap-4">
          {GAPS.map((g) => (
            <div key={g} className="text-center">
              <div className="w-8 rounded-t-[4px] bg-sky" style={{ height: g }} />
              <p className="tabular mt-1 font-mono text-12 text-midnight/70">{g}</p>
            </div>
          ))}
        </div>
        <p className="mt-6 text-16 text-midnight/75">
          Vertical rhythm is fluid, so the page never goes cramped at 360 or
          bloated at 1536:
        </p>
        <div className="mt-4 grid gap-3">
          {FLUID_SPACE.map((f) => (
            <div key={f.name} className="border-b border-line pb-3 last:border-0 last:pb-0">
              <p className="font-mono text-14 font-medium">{f.name}</p>
              <p className="font-mono text-12 text-midnight/70">{f.css}</p>
              <p className="text-14 text-midnight/75">{f.role}</p>
            </div>
          ))}
        </div>
        <p className="mt-6 text-16 text-midnight/75">
          Radius: 12px cards · 8px inputs · full-round chips. One shadow only:{" "}
          <code className="font-mono text-14">0 8px 24px rgba(10,27,46,0.07)</code>.
          Motion: micro 150–250ms, reveals 400–600ms, easing{" "}
          <code className="font-mono text-14">cubic-bezier(0.22,1,0.36,1)</code>.
        </p>
      </div>

      <h2 className="mt-16 font-display text-28 font-bold tracking-tight">Contrast</h2>
      <div className="mt-6 rounded-card border border-line bg-surface p-6 shadow-card">
        <p className="max-w-[68ch] text-16 text-midnight/75">
          Midnight on daylight: <span className="font-mono text-14">/70</span>{" "}
          = 6.3:1 and <span className="font-mono text-14">/65</span> = 5.3:1
          both clear 4.5:1. <span className="font-mono text-14">/60</span> is
          4.5:1 on white but only 4.5:1-minus on daylight, and{" "}
          <span className="font-mono text-14">/50</span> is 3.3:1 — never use
          it for text a reader needs. Floor: body and placeholders ≥ 4.5:1,
          text at 24px+ (or 18.66px bold) ≥ 3:1.
        </p>
      </div>

      <h2 className="mt-16 font-display text-28 font-bold tracking-tight">Business constants</h2>
      <div className="mt-6 overflow-x-auto rounded-card border border-line bg-surface p-6 shadow-card">
        <table className="w-full text-left text-14">
          <thead>
            <tr className="border-b border-line font-mono text-12 uppercase tracking-[0.08em] text-midnight/70">
              <th className="py-2 pr-4">constant</th>
              <th className="py-2">value</th>
            </tr>
          </thead>
          <tbody className="font-mono">
            {Object.entries(CALC).map(([k, v]) => (
              <tr key={k} className="border-b border-line last:border-0">
                <td className="py-2 pr-4">{k}</td>
                <td className="tabular py-2">{String(v)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <p className="mt-16 font-mono text-12 text-midnight/70">
        {BRAND.workingNameNote} Rename it in config/business.ts — nowhere else.
      </p>
    </main>
  );
}
