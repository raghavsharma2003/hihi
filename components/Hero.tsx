import { BRAND } from "@/config/business";
import HeroScene from "./HeroScene";

const HEADLINE_WORDS = ["Your", "genset", "sells", "you", "power", "at"];

export default function Hero() {
  return (
    <section
      id="top"
      aria-labelledby="hero-heading"
      className="mx-auto grid max-w-page items-center gap-10 px-4 pb-16 pt-28 md:grid-cols-[7fr_5fr] md:gap-16 md:px-6 md:pb-24 md:pt-40"
    >
      <div>
        <h1
          id="hero-heading"
          className="font-display text-[44px] font-extrabold leading-[1.02] tracking-[-0.02em] md:text-88"
        >
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
          className="hero-rise mt-6 max-w-[38rem] text-18 text-midnight/80 md:text-22"
          style={{ animationDelay: "640ms" }}
        >
          We serve the same hour at <strong className="font-semibold">₹13</strong>{" "}
          — from a battery we design, our software runs, and a contract
          guarantees. Your diesel bill drops by half or more.
        </p>
        <div
          className="hero-rise mt-8 flex flex-wrap items-center gap-4"
          style={{ animationDelay: "760ms" }}
        >
          <a
            href="#calculator"
            className="rounded-full bg-current px-7 py-3.5 text-16 font-semibold text-surface transition-transform duration-150 ease-out hover:scale-[1.03] active:scale-[0.98]"
          >
            See your savings →
          </a>
          <a
            href="#how-it-works"
            className="rounded-full border border-line bg-surface px-7 py-3.5 text-16 font-semibold text-midnight transition-colors duration-150 hover:border-current hover:text-current"
          >
            How it works ↓
          </a>
        </div>
        <ul
          className="hero-rise mt-10 flex flex-wrap gap-2"
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
      <div id="hero-scene" className="hero-rise" style={{ animationDelay: "400ms" }}>
        <HeroScene />
      </div>
    </section>
  );
}
