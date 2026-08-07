import Reveal from "./Reveal";

const TURNAWAYS = [
  "No real power cuts and no diesel bill → a battery won't pay; we'll say so.",
  "Rented premises without the owner in the room → fix that first.",
  "Want the genset gone entirely → we won't promise that; it stays as your reserve.",
];

/**
 * S9 — the honesty section. This replaces social proof until real sites exist.
 */
export default function WhoShouldnt() {
  return (
    <section
      aria-labelledby="honesty-heading"
      className="dark-band bg-midnight py-16 text-surface md:py-24"
    >
      <div className="mx-auto max-w-page px-4 md:px-6">
        <p className="font-mono text-12 font-medium uppercase tracking-[0.14em] text-sky">
          07 / Who shouldn&apos;t buy
        </p>
        <h2
          id="honesty-heading"
          className="mt-2 font-display text-40 font-bold tracking-tight md:text-56"
        >
          We turn customers away. Here&apos;s who.
        </h2>
        <ul className="mt-10 grid gap-6 md:max-w-[70ch]">
          {TURNAWAYS.map((t, i) => (
            <Reveal as="li" key={i} delay={i * 120} className="flex gap-4 border-b border-surface/15 pb-6 text-18 leading-relaxed text-surface/90 md:text-22">
              <svg aria-hidden="true" viewBox="0 0 12 12" className="mt-2 h-3 w-3 shrink-0 md:mt-2.5">
                <path d="M1 1 L11 11 M11 1 L1 11" stroke="#E4EDFB" strokeWidth="2" strokeLinecap="round" opacity="0.7" />
              </svg>
              <span>{t}</span>
            </Reveal>
          ))}
        </ul>
        <p className="mt-10 max-w-[62ch] text-16 text-sky/80 md:text-18">
          Honest sizing is our sales strategy. The audit tells you the truth
          even when the truth is &ldquo;not yet.&rdquo;
        </p>
      </div>
    </section>
  );
}
