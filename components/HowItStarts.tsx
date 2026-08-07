import Eyebrow from "./Eyebrow";
import Reveal from "./Reveal";

const STEPS = [
  {
    title: "Free audit",
    body: "We read 12 months of bills and your DG log; you get a one-page money map in 72 hours.",
  },
  {
    title: "Design & procurement",
    body: "You buy the system from vendors at our negotiated rates; we take a design fee, never a hardware margin.",
  },
  {
    title: "We run it",
    body: "5–7 year contract, uptime guaranteed in writing, fee tied to verified savings.",
  },
];

export default function HowItStarts() {
  return (
    <section
      aria-labelledby="steps-heading"
      className="mx-auto max-w-page px-4 py-16 md:px-6 md:py-24"
    >
      <Eyebrow>06 / How it starts</Eyebrow>
      <h2
        id="steps-heading"
        className="mt-2 font-display text-40 font-bold tracking-tight md:text-56"
      >
        Three steps, and the first is on us.
      </h2>

      <ol className="mt-10 grid gap-4 md:grid-cols-3 md:gap-6">
        {STEPS.map((s, i) => (
          <Reveal as="li" key={s.title} delay={i * 120} className="relative rounded-card border border-line bg-surface p-6 shadow-card">
            <span className="tabular font-mono text-14 font-medium text-current">
              step {i + 1} / 3
            </span>
            <h3 className="mt-2 font-display text-22 font-bold tracking-tight">
              {s.title}
            </h3>
            <p className="mt-3 text-16 text-midnight/75">{s.body}</p>
          </Reveal>
        ))}
      </ol>
    </section>
  );
}
