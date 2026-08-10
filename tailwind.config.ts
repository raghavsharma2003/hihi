import type { Config } from "tailwindcss";

// Design tokens are the ONLY palette. No Tailwind default colors anywhere.
//
// TYPE SCALE — the keys 12…88 never change, but their values are fluid above
// 22. Each key ships its own line-height AND tracking, because tracking is
// size-specific: display sizes need negative tracking (letters read too far
// apart as they grow), body text sits at ~0, the smallest UI text gets a hair
// of positive tracking. A single `text-88` therefore reads correctly at every
// width — no `text-[44px] md:text-88` breakpoint jumps anywhere.
//
//   key   360px    768px    1280px+   role
//   88    42.0     61.7     86.2/88   hero headline only
//   56    34.0     36.1     54.2/56   section headings, md and up
//   40    26.4     33.0     40        section headings, base
//   28    22.0     25.7     28        ₹ figures, h3
//
const config: Config = {
  content: [
    "./app/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}",
    "./config/**/*.{ts,tsx}",
  ],
  theme: {
    colors: {
      transparent: "transparent",
      daylight: "#F6F8FB",
      surface: "#FFFFFF",
      midnight: "#0A1B2E",
      current: "#1847C9",
      sky: "#E4EDFB",
      sunsave: "#EFA00B",
      sunink: "#B36D00",
      dieselclay: "#B3402F",
      line: "#DFE5EE",
    },
    fontFamily: {
      display: ["var(--font-display)", "sans-serif"],
      body: ["var(--font-body)", "sans-serif"],
      mono: ["var(--font-mono)", "monospace"],
    },
    fontSize: {
      // Fixed at the small end — UI text must never shrink below legible size.
      "12": ["0.75rem", { lineHeight: "1.5", letterSpacing: "0.005em" }],
      "14": ["0.875rem", { lineHeight: "1.55", letterSpacing: "0.002em" }],
      "16": ["1rem", { lineHeight: "1.6", letterSpacing: "0em" }],
      "18": ["1.125rem", { lineHeight: "1.6", letterSpacing: "0em" }],
      "22": ["1.375rem", { lineHeight: "1.4", letterSpacing: "-0.01em" }],
      // Fluid from here up. Leading tightens as size grows (1.18 → 1.04).
      "28": [
        "clamp(1.375rem, 1.15rem + 0.95vw, 1.75rem)",
        { lineHeight: "1.18", letterSpacing: "-0.015em" },
      ],
      "40": [
        "clamp(1.65rem, 1.2rem + 1.8vw, 2.5rem)",
        { lineHeight: "1.1", letterSpacing: "-0.02em" },
      ],
      "56": [
        "clamp(2.125rem, 0.55rem + 3.55vw, 3.5rem)",
        { lineHeight: "1.06", letterSpacing: "-0.025em" },
      ],
      "88": [
        "clamp(2.625rem, 1.55rem + 4.8vw, 5.5rem)",
        { lineHeight: "1.04", letterSpacing: "-0.03em" },
      ],
    },
    extend: {
      spacing: {
        // Fluid vertical rhythm. `section` passes through the old anchors
        // (64px at 360, 96px from 900 up) without the hard py-16 → py-24 step.
        section: "clamp(4rem, 2.65rem + 5.9vw, 6rem)",
        // Hero top: fixed-nav clearance + air (112px → 160px).
        "hero-top": "clamp(7rem, 5.2rem + 8vw, 10rem)",
        // Price-ladder plot height (272px → 360px).
        chart: "clamp(17rem, 14.9rem + 9.5vw, 22.5rem)",
      },
      borderRadius: {
        card: "12px",
        input: "8px",
      },
      boxShadow: {
        card: "0 8px 24px rgba(10,27,46,0.07)",
      },
      maxWidth: {
        page: "1200px",
      },
      transitionTimingFunction: {
        out: "cubic-bezier(0.22,1,0.36,1)",
      },
    },
  },
  plugins: [],
};

export default config;
