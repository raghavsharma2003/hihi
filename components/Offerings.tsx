import { OFFERINGS } from "@/config/business";
import Eyebrow from "./Eyebrow";
import Reveal from "./Reveal";

const CARDS = [
  {
    title: "Battery for Commercial",
    line: "Dealerships, hospitals, hotels, banquet halls — your capital, our design, our software, a written uptime guarantee.",
    stat: OFFERINGS.commercialSavings,
    statLabel: "typical saving",
  },
  {
    title: "Battery for Societies",
    line: "200+ flat societies: one system replaces most genset hours and the committee sees the ledger monthly.",
    stat: OFFERINGS.societySavings,
    statLabel: "typical saving",
  },
  {
    title: "Autopilot",
    line: "Already own a lithium inverter? Our software alone times your charging and discharge around the tariff.",
    stat: OFFERINGS.autopilotPool,
    statLabel: `earns · costs ${OFFERINGS.autopilotPrice}`,
  },
];

export default function Offerings() {
  return (
    <section
      id="savings"
      aria-labelledby="offerings-heading"
      className="mx-auto max-w-page scroll-mt-24 px-4 py-16 md:px-6 md:py-24"
    >
      <Eyebrow>04 / What we are</Eyebrow>
      <h2
        id="offerings-heading"
        className="mt-2 font-display text-40 font-bold tracking-tight md:text-56"
      >
        Three products. One job: cheaper hours.
      </h2>

      <div className="mt-10 grid gap-4 md:grid-cols-3 md:gap-6">
        {CARDS.map((c, i) => (
          <Reveal
            key={c.title}
            delay={i * 70}
            className="rounded-card border border-line bg-surface p-6 shadow-card"
          >
            <h3 className="font-display text-22 font-bold tracking-tight">
              {c.title}
            </h3>
            <p className="mt-3 text-16 text-midnight/75">{c.line}</p>
            <p className="tabular mt-6 font-mono text-28 font-medium text-sunink">
              {c.stat}
            </p>
            <p className="font-mono text-12 uppercase tracking-[0.08em] text-midnight/55">
              {c.statLabel}
            </p>
          </Reveal>
        ))}
      </div>

      <Reveal className="mt-6 flex flex-wrap gap-2">
        {[
          "diesel ≥₹10k/mo → battery",
          "lithium + no diesel → autopilot",
          "neither → we say “not yet”",
        ].map((chip) => (
          <span
            key={chip}
            className="rounded-full border border-line bg-daylight px-3 py-1.5 font-mono text-12 text-midnight/70"
          >
            {chip}
          </span>
        ))}
      </Reveal>
    </section>
  );
}
