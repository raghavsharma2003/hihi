import type { Config } from "tailwindcss";

// Design tokens are the ONLY palette. No Tailwind default colors anywhere.
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
      dieselclay: "#B3402F",
      line: "#DFE5EE",
    },
    fontFamily: {
      display: ["var(--font-display)", "sans-serif"],
      body: ["var(--font-body)", "sans-serif"],
      mono: ["var(--font-mono)", "monospace"],
    },
    fontSize: {
      "12": ["12px", { lineHeight: "1.5" }],
      "14": ["14px", { lineHeight: "1.5" }],
      "16": ["16px", { lineHeight: "1.6" }],
      "18": ["18px", { lineHeight: "1.6" }],
      "22": ["22px", { lineHeight: "1.45" }],
      "28": ["28px", { lineHeight: "1.25" }],
      "40": ["40px", { lineHeight: "1.1" }],
      "56": ["56px", { lineHeight: "1.05" }],
      "88": ["88px", { lineHeight: "1.0" }],
    },
    extend: {
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
