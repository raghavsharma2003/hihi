"use client";

import { useEffect, useState } from "react";
import { BRAND } from "@/config/business";

const LINKS = [
  { href: "#how-it-works", label: "How it works" },
  { href: "#savings", label: "Savings" },
  { href: "#software", label: "Software" },
  { href: "#faq", label: "FAQ" },
];

export default function Nav() {
  const [shrunk, setShrunk] = useState(false);

  useEffect(() => {
    const onScroll = () => setShrunk(window.scrollY > 24);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  // Translucent layer, content scrolls under it. The only animated property is
  // padding on this fixed element — nothing below it moves, and the row's own
  // children never change size, so the shrink can't shift the layout.
  return (
    <header
      className="fixed inset-x-0 top-0 z-50 border-b border-line/70 bg-daylight/85 backdrop-blur-md transition-[padding] duration-200 ease-out"
      style={{ paddingBlock: shrunk ? "0.5rem" : "1rem" }}
    >
      <nav
        aria-label="Main"
        className="mx-auto flex max-w-page items-center justify-between gap-3 px-4 md:gap-6 md:px-6"
      >
        <a
          href="#top"
          className="font-display text-22 font-bold tracking-tight text-midnight"
        >
          {BRAND.name}
        </a>
        <div className="hidden items-center gap-6 md:flex lg:gap-8">
          {LINKS.map((l) => (
            <a
              key={l.href}
              href={l.href}
              className="whitespace-nowrap text-14 font-semibold text-midnight/80 transition-colors duration-150 hover:text-current"
            >
              {l.label}
            </a>
          ))}
        </div>
        <a
          href="#calculator"
          className="whitespace-nowrap rounded-full bg-current px-4 py-2.5 text-14 font-semibold text-surface transition-transform duration-150 ease-out hover:scale-[1.03] active:scale-[0.98] md:px-5"
        >
          Book a free audit
        </a>
      </nav>
    </header>
  );
}
