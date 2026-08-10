import { BRAND } from "@/config/business";
import HeroScene from "./HeroScene";

const HEADLINE_WORDS = ["Your", "genset", "sells", "you", "power", "at"];

export default function Hero() {
  // Stacked until lg: between 768 and 1024 a two-column split starves both the
  // headline and the streetscape. From lg the split is 7fr/5fr.
  return (
    <section
      id="top"
      aria-labelledby="hero-heading"
      className="mx-auto grid max-w-page items-center gap-10 px-4 pb-section pt-hero-top md:gap-12 md:px-6 lg:grid-cols-[minmax(0,7fr)_minmax(0,5fr)] lg:gap-14 xl:gap-16"
    >
      <div>
        {/* One fluid size, 42px at 360 → 88px at 1320+. Leading and tracking
            ride along in the token, so no per-breakpoint overrides. */}
        <h1 id="hero-heading" className="font-display text-88 font-extrabold">
          {HEADLINE_WORDS.map((w, i) => (
            <span key={i} className="hero-word" style={{ animationDelay: `${i * 80}ms` }}>
              {w}{" "}
            </span>
          ))}
          <span
            className="hero-word whitespace-nowrap text-dieselclay"
            style={{ animationDelay: `${HEADLINE_WORDS.length * 80}ms` }}
          >
            ₹32 a unit.
          </span>
        </h1>
        <p
          className="hero-rise mt-5 max-w-[52ch] text-18 text-midnight/80 md:mt-6 md:text-22"
          style={{ animationDelay: "640ms" }}
        >
          We serve the same hour at <strong className="font-semibold">₹13</strong>{" "}
          — from a battery we design, our software runs, and a contract
          guarantees. Your diesel bill drops by half or more.
        </p>
        <div
          className="hero-rise mt-8 flex flex-wrap items-center gap-3 sm:gap-4"
          style={{ animationDelay: "760ms" }}
        >
          <a
            href="#calculator"
            className="rounded-full bg-current px-6 py-3.5 text-16 font-semibold text-surface transition-transform duration-150 ease-out hover:scale-[1.03] active:scale-[0.98] sm:px-7"
          >
            See your savings →
          </a>
          <a
            href="#how-it-works"
            className="rounded-full border border-line bg-surface px-6 py-3.5 text-16 font-semibold text-midnight transition-colors duration-150 hover:border-current hover:text-current sm:px-7"
          >
            How it works ↓
          </a>
        </div>
        <ul
          className="hero-rise mt-8 flex flex-wrap gap-2 md:mt-10"
          style={{ animationDelay: "880ms" }}
        >
          {[
            `${BRAND.region} · ${BRAND.established}`,
            "genset stays as reserve",
            "savings verified monthly",
          ].map((chip) => (
            <li
              key={chip}
              className="rounded-full border border-line bg-surface px-3 py-1.5 font-mono text-12 text-midnight/70"
            >
              {chip}
            </li>
          ))}
        </ul>
      </div>
      {/* Capped while stacked so the streetscape never dwarfs the copy on a
          tablet; uncapped once it has a column of its own. */}
      <div
        id="hero-scene"
        className="hero-rise mx-auto w-full max-w-[34rem] lg:mx-0 lg:max-w-none"
        style={{ animationDelay: "400ms" }}
      >
        <HeroScene />
      </div>
    </section>
  );
}
