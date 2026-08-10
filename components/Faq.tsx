"use client";

import { useState } from "react";
import { BRAND } from "@/config/business";
import Eyebrow from "./Eyebrow";

const ITEMS = [
  {
    q: "Who pays for the battery?",
    a: "You do — usually with money a genset retrofit or overhaul was about to eat anyway. We design the system and negotiate vendor rates, take a design fee, and never mark up hardware. The asset sits on your books from day one.",
  },
  {
    q: "What if the cut is longer than the battery?",
    a: "The genset auto-starts and takes over — it never leaves your site. The battery carries the first stretch (and the vast majority of typical cuts end inside it), so the genset runs rarely and briefly instead of every single time.",
  },
  {
    q: "Is lithium safe?",
    a: "We install LFP chemistry only — the stable one, not the phone-battery kind. Cabinets are sited outdoors with thermal management, and the insurer covering the system is named in your contract.",
  },
  {
    q: "What exactly do we pay monthly?",
    a: "A service fee tied to verified savings, set in the contract. The savings ledger is computed from your own meter data every month; if the savings aren't there, the fee is the first thing under review.",
  },
  {
    q: `What happens if ${BRAND.name} disappears?`,
    a: "You own the asset outright. The system runs on open protocols, so any competent integrator can take over operation. Your power never depends on our company existing.",
  },
  {
    q: "Which areas first?",
    a: `${BRAND.region} corridors first — where diesel hours and GRAP restrictions bite hardest. The audit form asks your pincode so we can tell you honestly when we can serve you.`,
  },
];

/** Strong ease-out — the row, the icon and the copy all land on one curve. */
const EASE_OUT = "ease-[cubic-bezier(0.23,1,0.32,1)]";

export default function Faq() {
  const [open, setOpen] = useState<number>(0);

  return (
    <section
      id="faq"
      aria-labelledby="faq-heading"
      className="mx-auto max-w-page scroll-mt-24 px-4 py-16 md:px-6 md:py-24"
    >
      <Eyebrow>08 / Straight answers</Eyebrow>
      <h2
        id="faq-heading"
        className="mt-2 font-display text-40 font-bold tracking-tight md:text-56"
      >
        Asked before signing.
      </h2>

      <div className="mt-10 max-w-[72ch] divide-y divide-line rounded-card border border-line bg-surface shadow-card">
        {ITEMS.map((item, i) => {
          const isOpen = open === i;
          return (
            <div key={i}>
              <button
                onClick={() => setOpen(isOpen ? -1 : i)}
                aria-expanded={isOpen}
                aria-controls={`faq-a-${i}`}
                className="flex w-full items-center justify-between gap-4 px-5 py-4 text-left text-16 font-semibold transition-colors duration-150 ease-[ease] hover:text-current active:text-current md:px-6 md:py-5 md:text-18"
              >
                {item.q}
                <svg
                  viewBox="0 0 16 16"
                  aria-hidden="true"
                  className={`h-4 w-4 shrink-0 transition-transform duration-[250ms] ${EASE_OUT} ${isOpen ? "rotate-45" : ""}`}
                >
                  <path d="M8 2 v12 M2 8 h12" stroke="#1847C9" strokeWidth="2" strokeLinecap="round" />
                </svg>
              </button>
              {/* grid-template-rows 0fr→1fr: the one height-ish transition
                  worth its layout cost, and it retargets mid-flight when the
                  row is toggled twice quickly. */}
              <div
                id={`faq-a-${i}`}
                role="region"
                className={`grid transition-[grid-template-rows] duration-[250ms] ${EASE_OUT}`}
                style={{ gridTemplateRows: isOpen ? "1fr" : "0fr" }}
              >
                <div
                  className={`overflow-hidden transition-opacity duration-[200ms] ${EASE_OUT} ${
                    isOpen ? "opacity-100" : "opacity-0"
                  }`}
                >
                  <p className="px-5 pb-5 text-16 text-midnight/75 md:px-6 md:pb-6">
                    {item.a}
                  </p>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </section>
  );
}
