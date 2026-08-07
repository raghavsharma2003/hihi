# PranaWatt — landing page

Single-page marketing site for an Indian distributed-energy operator: batteries
for commercial buildings and housing societies, sold on radical honesty and a
live savings calculator. Built to beat basepowercompany.com at its own game,
with India-specific pain (diesel ₹32/unit, GRAP, DG billing) baked in.

## Run

```bash
npm install
npm run dev        # http://localhost:3000
npm run build      # production build
npm start          # serve the production build
npm test           # calculator formula unit tests (vitest)
npm run lint
```

## Where to change things

| What | Where |
| --- | --- |
| **Brand name** (it WILL change) | `config/business.ts` → `BRAND.name` — the only place it exists |
| Phone / WhatsApp / region | `config/business.ts` → `BRAND` |
| Every calculator constant | `config/business.ts` → `CALC` (formulas in `lib/calculator.ts`, tests in `tests/`) |
| Slider ranges & defaults | `config/business.ts` → `INPUT_BOUNDS` |
| Color/type/spacing tokens | `tailwind.config.ts` + `app/globals.css` — rendered live at `/design-tokens` |
| Lead capture | `app/api/lead/route.ts` (placeholder — wire to CRM/sheet before launch) |

## Architecture

- **Next.js 14 App Router + TypeScript + Tailwind** (custom tokens only — no
  default palette) **+ GSAP ScrollTrigger** for the three scroll moments:
  the page-long "current line", the S3 power-cut pin, and the S4 day scrub.
- All illustration is inline SVG in the system palette; no images, no Lottie.
- `prefers-reduced-motion` renders everything final-state and static.
- The calculator has an honest-fail state: below ₹10k/mo diesel (commercial)
  or under 1 cut-hour/day (society) it refuses to show a rosy number and
  routes to the Autopilot software product instead.

## Deploy

Any Node host: `npm run build && npm start`. For a fully static export, point
the lead form at an external endpoint, drop `app/api/`, and add
`output: "export"` to `next.config.mjs`.

## Page map

Nav → Hero (₹32 hook) → S2 four prices → S3 the cut moment (pinned) →
S4 a day at your site (scrubbed) → S5 calculator → S6 offerings →
S7 software → S8 three steps → S9 who shouldn't buy → FAQ → final CTA →
footer. `/design-tokens` renders the design system itself.
