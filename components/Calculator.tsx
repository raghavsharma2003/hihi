"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import { CALC, INPUT_BOUNDS, OFFERINGS } from "@/config/business";
import { calculate, estimateKw, type CalcInput, type Mode } from "@/lib/calculator";
import { formatINR, formatKwh, formatLitres, formatYears } from "@/lib/format";
import Eyebrow from "./Eyebrow";
import LeadForm from "./LeadForm";
import Odometer from "./Odometer";
import RangeField from "./RangeField";

/** Strong ease-out, the one curve every entrance and settle here uses. */
const EASE_OUT = "ease-[cubic-bezier(0.23,1,0.32,1)]";

export default function Calculator() {
  const [mode, setMode] = useState<Mode>("commercial");

  // commercial inputs
  const cb = INPUT_BOUNDS.commercial;
  const [bill, setBill] = useState<number>(cb.bill.default);
  const [cDiesel, setCDiesel] = useState<number>(cb.diesel.default);
  const [kw, setKw] = useState<number>(cb.kw.default);
  const [kwNotSure, setKwNotSure] = useState(false);

  // society inputs
  const sb = INPUT_BOUNDS.society;
  const [flats, setFlats] = useState<number>(sb.flats.default);
  const [sDiesel, setSDiesel] = useState<number>(sb.diesel.default);
  const [cutHours, setCutHours] = useState<number>(sb.cutHours.default);

  const [formOpen, setFormOpen] = useState(false);

  const result = useMemo(() => {
    const input: CalcInput =
      mode === "commercial"
        ? { mode, bill, diesel: cDiesel, kw: kwNotSure ? null : kw }
        : { mode, flats, diesel: sDiesel, cutHours };
    return calculate(input);
  }, [mode, bill, cDiesel, kw, kwNotSure, flats, sDiesel, cutHours]);

  // Mobile sticky bar: visible while the calculator section is on screen
  const sectionRef = useRef<HTMLElement>(null);
  const resultRef = useRef<HTMLDivElement>(null);
  const [barVisible, setBarVisible] = useState(false);
  useEffect(() => {
    const section = sectionRef.current;
    const resultPanel = resultRef.current;
    if (!section || !resultPanel) return;
    let sectionIn = false;
    let resultIn = false;
    const update = () => setBarVisible(sectionIn && !resultIn);
    const io1 = new IntersectionObserver(
      ([e]) => { sectionIn = e.isIntersecting; update(); },
      { threshold: 0.05 },
    );
    const io2 = new IntersectionObserver(
      ([e]) => { resultIn = e.isIntersecting; update(); },
      { threshold: 0.2 },
    );
    io1.observe(section);
    io2.observe(resultPanel);
    return () => { io1.disconnect(); io2.disconnect(); };
  }, []);

  const range = `${formatINR(result.monthlySavingLow)}–${formatINR(result.monthlySavingHigh)}`;

  return (
    <section
      id="calculator"
      ref={sectionRef}
      aria-labelledby="calculator-heading"
      className="mx-auto max-w-page scroll-mt-24 px-4 py-16 md:px-6 md:py-24"
    >
      <Eyebrow>Your number</Eyebrow>
      <h2
        id="calculator-heading"
        className="mt-2 font-display text-40 font-bold tracking-tight md:text-56"
      >
        What would your building save?
      </h2>

      <div className="mt-6 grid gap-6 rounded-card border border-line bg-surface p-4 shadow-card md:mt-10 md:grid-cols-2 md:gap-10 md:p-10">
        {/* Inputs */}
        <div className="min-w-0">
          {/* Two equal columns, so the selection is one pill sliding between
              them rather than two backgrounds crossfading. */}
          <div
            role="tablist"
            aria-label="Site type"
            className="relative inline-grid grid-cols-2 rounded-full border border-line bg-daylight p-1"
          >
            <span
              aria-hidden="true"
              style={{
                transform:
                  mode === "society" ? "translateX(100%)" : "translateX(0)",
              }}
              className={`pointer-events-none absolute inset-y-1 left-1 w-[calc(50%-0.25rem)] rounded-full bg-current transition-transform duration-200 ${EASE_OUT}`}
            />
            {(["commercial", "society"] as const).map((m) => (
              <button
                key={m}
                role="tab"
                aria-selected={mode === m}
                onClick={() => setMode(m)}
                className={`relative rounded-full px-4 py-2 text-14 font-semibold transition-[color,transform] duration-200 ${EASE_OUT} active:scale-[0.97] active:duration-100 ${
                  mode === m
                    ? "text-surface"
                    : "text-midnight/70 hover:text-midnight"
                }`}
              >
                {m === "commercial" ? "Commercial" : "Society"}
              </button>
            ))}
          </div>

          <div className="mt-6 grid gap-6">
            {mode === "commercial" ? (
              <>
                <RangeField
                  label="Monthly electricity bill"
                  value={bill}
                  min={cb.bill.min}
                  max={cb.bill.max}
                  step={cb.bill.step}
                  onChange={setBill}
                  format={formatINR}
                />
                <RangeField
                  label="Monthly diesel spend"
                  value={cDiesel}
                  min={cb.diesel.min}
                  max={cb.diesel.max}
                  step={cb.diesel.step}
                  onChange={setCDiesel}
                  format={formatINR}
                />
                <div>
                  <RangeField
                    label="Connection size"
                    value={kwNotSure ? estimateKw(bill) : kw}
                    min={cb.kw.min}
                    max={cb.kw.max}
                    step={cb.kw.step}
                    onChange={setKw}
                    format={(v) => `${v} kW`}
                    disabled={kwNotSure}
                  />
                  <label className="mt-2 flex cursor-pointer items-center gap-2 text-14 text-midnight/70">
                    <input
                      type="checkbox"
                      checked={kwNotSure}
                      onChange={(e) => setKwNotSure(e.target.checked)}
                      className="h-4 w-4 accent-[#1847C9]"
                    />
                    Not sure — estimate it from my bill
                  </label>
                </div>
              </>
            ) : (
              <>
                <RangeField
                  label="Number of flats"
                  value={flats}
                  min={sb.flats.min}
                  max={sb.flats.max}
                  step={sb.flats.step}
                  onChange={setFlats}
                  format={(v) => `${v} flats`}
                />
                <RangeField
                  label="Monthly society diesel spend"
                  value={sDiesel}
                  min={sb.diesel.min}
                  max={sb.diesel.max}
                  step={sb.diesel.step}
                  onChange={setSDiesel}
                  format={formatINR}
                />
                <RangeField
                  label="Power cut hours per day"
                  value={cutHours}
                  min={sb.cutHours.min}
                  max={sb.cutHours.max}
                  step={sb.cutHours.step}
                  onChange={setCutHours}
                  format={(v) => `${v} h/day`}
                />
              </>
            )}
          </div>
        </div>

        {/* Results */}
        <div
          ref={resultRef}
          aria-live="polite"
          className="min-w-0 rounded-card bg-sky/60 p-4 md:p-8"
        >
          {/* Keyed on the verdict: the honest-fail copy and the savings
              readout are different answers, so one fades out of the way of
              the other instead of hard-cutting. */}
          <StateFade key={result.viable ? "viable" : "not-yet"}>
            {result.viable ? (
              <>
                <p className="text-16 font-semibold text-midnight/70">
                  You&apos;d save
                </p>
                <p className="mt-1 font-display font-bold tracking-tight text-sunink">
                  <Odometer
                    value={range}
                    className="text-28 sm:text-40 md:text-40 lg:text-56"
                  />
                </p>
                <p className="text-16 font-semibold text-midnight/70">
                  per month
                </p>

                <dl className="mt-6 grid grid-cols-2 gap-x-4 gap-y-5">
                  <Stat
                    label="Yearly savings"
                    value={`${formatINR(result.yearlySavingLow)}–${formatINR(result.yearlySavingHigh)}`}
                    tone="sunsave"
                  />
                  <Stat
                    label="Diesel avoided / yr"
                    value={formatLitres(result.litresPerYear)}
                  />
                  <Stat
                    label="Payback on your system"
                    value={`${formatYears(result.paybackLowYears)}–${formatYears(result.paybackHighYears)} yrs`}
                  />
                  <Stat
                    label="Your system size"
                    value={`~${formatKwh(result.battKwh)}`}
                  />
                </dl>

                <p className="mt-6 text-14 text-midnight/60">
                  Same formulas we use in paid audits. Ranges, not promises —
                  your real cut-log sharpens them.
                </p>
              </>
            ) : (
              <>
                <p className="font-display text-28 font-bold tracking-tight">
                  A battery may not pay for you yet — and we&apos;d tell you that
                  in person too.
                </p>
                <p className="mt-4 text-16 text-midnight/80">
                  {mode === "commercial"
                    ? `Below ₹${(CALC.MIN_COMMERCIAL_DIESEL / 1000).toFixed(0)}k a month of diesel, the maths rarely clears. `
                    : "With under an hour of cuts a day, the maths rarely clears. "}
                  If you already own a lithium inverter, our{" "}
                  {OFFERINGS.autopilotPrice} Autopilot software is your product —
                  it earns its fee on tariff timing alone.
                </p>
                <a
                  href="#software"
                  className={`mt-6 inline-block rounded-full border border-current px-5 py-2.5 text-16 font-semibold text-current transition-[background-color,transform] duration-150 ${EASE_OUT} hover:bg-surface active:scale-[0.97] active:duration-100`}
                >
                  See Autopilot
                </a>
              </>
            )}
          </StateFade>

          {result.viable && (
            <div className="mt-6 border-t border-line pt-6">
              {formOpen ? (
                <LeadForm context={mode} />
              ) : (
                <button
                  onClick={() => setFormOpen(true)}
                  className={`w-full rounded-full bg-current px-6 py-3 text-16 font-semibold text-surface transition-transform duration-150 ${EASE_OUT} [@media(hover:hover)_and_(pointer:fine)]:hover:scale-[1.02] active:scale-[0.98] active:duration-100`}
                >
                  Get this verified free — book the audit
                </button>
              )}
            </div>
          )}
        </div>
      </div>

      {/* Mobile sticky live-result bar */}
      <div
        aria-hidden={!barVisible}
        className={`fixed inset-x-0 bottom-0 z-40 border-t border-line bg-surface/95 px-4 py-3 shadow-card backdrop-blur-md transition-transform duration-[250ms] ${EASE_OUT} md:hidden ${
          barVisible ? "translate-y-0" : "translate-y-full"
        }`}
      >
        <div className="flex items-center justify-between gap-3">
          {result.viable ? (
            <p className="font-mono text-14">
              saves{" "}
              <span className="tabular font-medium text-sunink">{range}</span>
              /mo
            </p>
          ) : (
            <p className="font-mono text-14 text-midnight/70">
              battery may not pay yet
            </p>
          )}
          <a
            href="#calculator"
            onClick={() => setFormOpen(true)}
            className={`shrink-0 rounded-full bg-current px-4 py-2 text-14 font-semibold text-surface transition-transform duration-150 ${EASE_OUT} active:scale-[0.97] active:duration-100`}
          >
            Free audit
          </a>
        </div>
      </div>
    </section>
  );
}

/**
 * Fades its subtree in on mount. Used with a key so the two verdict states
 * hand over instead of teleporting. Opacity only — the panel is a block of
 * numbers being read, so it must not slide.
 */
function StateFade({ children }: { children: React.ReactNode }) {
  const [entered, setEntered] = useState(false);

  useEffect(() => {
    const id = requestAnimationFrame(() => setEntered(true));
    return () => cancelAnimationFrame(id);
  }, []);

  return (
    <div
      className={`transition-opacity duration-200 ${EASE_OUT} ${
        entered ? "opacity-100" : "opacity-0"
      }`}
    >
      {children}
    </div>
  );
}

function Stat({
  label,
  value,
  tone,
}: {
  label: string;
  value: string;
  tone?: "sunsave";
}) {
  return (
    <div>
      <dt className="text-12 font-semibold uppercase tracking-[0.08em] text-midnight/60">
        {label}
      </dt>
      <dd
        className={`tabular mt-1 font-mono text-18 font-medium ${
          tone === "sunsave" ? "text-sunink" : "text-midnight"
        }`}
      >
        {value}
      </dd>
    </div>
  );
}
