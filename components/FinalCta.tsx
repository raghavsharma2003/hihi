import { BRAND } from "@/config/business";

/**
 * S11 — where the current line terminates: it forms the CTA button's border
 * and pulses once (the ring markup lives in CurrentLine; the button carries
 * the id it targets).
 */
export default function FinalCta() {
  const whatsappHref = `https://wa.me/${BRAND.whatsappNumber}?text=${encodeURIComponent(
    `Hi ${BRAND.name} — I'd like a free savings audit.`,
  )}`;

  return (
    <section
      aria-labelledby="final-cta-heading"
      className="mx-auto max-w-page px-4 py-20 text-center md:px-6 md:py-32"
    >
      <h2
        id="final-cta-heading"
        className="mx-auto max-w-[18ch] font-display text-40 font-bold tracking-tight md:text-56"
      >
        Find out what your diesel is really costing you.
      </h2>
      <p className="mx-auto mt-4 max-w-[44ch] text-16 text-midnight/70 md:text-18">
        The audit is free, takes one site visit, and ends in a one-page money
        map — even when the answer is &ldquo;not yet.&rdquo;
      </p>
      <div className="mt-10 flex flex-col items-center gap-4">
        <a
          id="final-cta-button"
          href="#calculator"
          className="cta-terminal relative rounded-full bg-current px-10 py-4 text-18 font-semibold text-surface transition-transform duration-150 ease-[cubic-bezier(0.23,1,0.32,1)] [@media(hover:hover)_and_(pointer:fine)]:hover:scale-[1.03] active:scale-[0.98] active:duration-100"
        >
          Book the free audit
        </a>
        <div className="flex flex-wrap items-center justify-center gap-4 font-mono text-14 text-midnight/70">
          <a
            href={`tel:${BRAND.phone.replace(/ /g, "")}`}
            className="transition-colors duration-150 ease-[ease] hover:text-current"
          >
            {BRAND.phone}
          </a>
          <span aria-hidden="true" className="text-line">·</span>
          <a
            href={whatsappHref}
            target="_blank"
            rel="noopener noreferrer"
            className="transition-colors duration-150 ease-[ease] hover:text-current"
          >
            WhatsApp us
          </a>
        </div>
      </div>
    </section>
  );
}
