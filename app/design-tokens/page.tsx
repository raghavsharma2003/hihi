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

const SCALE = [12, 14, 16, 18, 22, 28, 40, 56, 88];
const GAPS = [8, 16, 24, 40, 64, 96, 160];

export default function DesignTokens() {
  return (
    <main className="mx-auto max-w-page px-4 py-16 md:px-6">
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
              <p className="font-mono text-12 text-midnight/55">{c.hex}</p>
              <p className="mt-2 text-14 text-midnight/75">{c.role}</p>
            </div>
          </div>
        ))}
      </div>

      <h2 className="mt-16 font-display text-28 font-bold tracking-tight">Type</h2>
      <div className="mt-6 grid gap-6 rounded-card border border-line bg-surface p-6 shadow-card">
        <div>
          <p className="font-mono text-12 uppercase tracking-[0.08em] text-midnight/55">
            display · Bricolage Grotesque 700/800 · tracking -0.02em
          </p>
          <p className="mt-1 font-display text-40 font-bold tracking-tight">
            Your genset sells you power.
          </p>
        </div>
        <div>
          <p className="font-mono text-12 uppercase tracking-[0.08em] text-midnight/55">
            body · IBM Plex Sans 400/600 · 16–18px · 1.6
          </p>
          <p className="mt-1 max-w-[62ch] text-18">
            We serve the same hour at ₹13 — from a battery we design, our
            software runs, and a contract guarantees.
          </p>
        </div>
        <div>
          <p className="font-mono text-12 uppercase tracking-[0.08em] text-midnight/55">
            data · IBM Plex Mono · every ₹ figure, unit, label chip, axis
          </p>
          <p className="tabular mt-1 font-mono text-28 font-medium text-sunsave">
            ₹24,310/mo saved
          </p>
        </div>
      </div>

      <h2 className="mt-16 font-display text-28 font-bold tracking-tight">Scale</h2>
      <div className="mt-6 rounded-card border border-line bg-surface p-6 shadow-card">
        {SCALE.map((s) => (
          <p key={s} className="flex items-baseline gap-4 border-b border-line py-2 last:border-0">
            <span className="tabular w-10 shrink-0 font-mono text-12 text-midnight/55">{s}</span>
            <span className="truncate font-display font-bold tracking-tight" style={{ fontSize: s }}>
              ₹32 a unit
            </span>
          </p>
        ))}
      </div>

      <h2 className="mt-16 font-display text-28 font-bold tracking-tight">Spacing · layout</h2>
      <div className="mt-6 rounded-card border border-line bg-surface p-6 shadow-card">
        <p className="text-16 text-midnight/75">
          12-column grid, max-width 1200px, 8px base. Allowed gaps only:
        </p>
        <div className="mt-4 flex flex-wrap items-end gap-4">
          {GAPS.map((g) => (
            <div key={g} className="text-center">
              <div className="w-8 rounded-t-[4px] bg-sky" style={{ height: g }} />
              <p className="tabular mt-1 font-mono text-12 text-midnight/55">{g}</p>
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

      <h2 className="mt-16 font-display text-28 font-bold tracking-tight">Business constants</h2>
      <div className="mt-6 overflow-x-auto rounded-card border border-line bg-surface p-6 shadow-card">
        <table className="w-full text-left text-14">
          <thead>
            <tr className="border-b border-line font-mono text-12 uppercase tracking-[0.08em] text-midnight/55">
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

      <p className="mt-16 font-mono text-12 text-midnight/50">
        {BRAND.workingNameNote} Rename it in config/business.ts — nowhere else.
      </p>
    </main>
  );
}
