/**
 * Indian commercial street at dusk: society tower, dealership, clinic,
 * a genset with a clay smoke wisp, and our battery cabinet glowing current.
 * Flat 2px-outline style, palette-locked, all inline SVG.
 * Windows flicker ON sequentially on load (CSS, reduced-motion safe).
 */
export default function HeroScene() {
  return (
    <svg
      viewBox="0 0 720 400"
      role="img"
      aria-label="Illustrated Indian commercial street at dusk: a housing society tower, a car dealership and a clinic with lit windows, a diesel genset trailing smoke, and a battery cabinet glowing blue"
      className="hero-scene w-full"
    >
      <style>{`
        .hs-win { fill: #E4EDFB; opacity: 0.35; }
        .hs-win.lit { animation: hsFlick 250ms cubic-bezier(0.22,1,0.36,1) forwards; }
        @keyframes hsFlick {
          0% { fill: #E4EDFB; opacity: 0.35; }
          40% { fill: #EFA00B; opacity: 0.4; }
          60% { fill: #E4EDFB; opacity: 0.4; }
          100% { fill: #EFA00B; opacity: 0.9; }
        }
        .hs-smoke { animation: hsSmoke 4s ease-in-out infinite; transform-origin: 118px 268px; }
        @keyframes hsSmoke {
          0%, 100% { transform: translateY(0) scale(1); opacity: 0.7; }
          50% { transform: translateY(-6px) scale(1.06); opacity: 0.45; }
        }
        @media (prefers-reduced-motion: reduce) {
          .hs-win.lit { animation: none; fill: #EFA00B; opacity: 0.9; }
          .hs-smoke { animation: none; }
        }
      `}</style>

      {/* ground */}
      <line x1="0" y1="330" x2="720" y2="330" stroke="#0A1B2E" strokeWidth="2" />

      {/* ══ society tower (left) ══ */}
      <rect x="60" y="70" width="130" height="260" rx="4" fill="#FFFFFF" stroke="#0A1B2E" strokeWidth="2" />
      <rect x="60" y="70" width="130" height="18" rx="4" fill="#E4EDFB" stroke="#0A1B2E" strokeWidth="2" />
      {/* water tank */}
      <rect x="92" y="46" width="36" height="24" rx="4" fill="#E4EDFB" stroke="#0A1B2E" strokeWidth="2" />
      {/* windows: 5 rows x 3 cols */}
      {[0, 1, 2, 3, 4].map((r) =>
        [0, 1, 2].map((c) => (
          <rect
            key={`t${r}${c}`}
            x={76 + c * 36}
            y={102 + r * 42}
            width="24"
            height="26"
            rx="2"
            className={`hs-win ${(r + c) % 2 === 0 ? "lit" : ""}`}
            style={{ animationDelay: `${200 + (r * 3 + c) * 60}ms` }}
            stroke="#0A1B2E"
            strokeWidth="2"
          />
        )),
      )}

      {/* ══ genset between tower and dealership ══ */}
      <rect x="212" y="286" width="64" height="44" rx="6" fill="#FFFFFF" stroke="#0A1B2E" strokeWidth="2" />
      <rect x="220" y="296" width="26" height="24" rx="2" fill="#E4EDFB" stroke="#0A1B2E" strokeWidth="2" />
      <circle cx="260" cy="308" r="7" fill="#FFFFFF" stroke="#0A1B2E" strokeWidth="2" />
      {/* exhaust pipe + clay smoke wisp */}
      <path d="M268 286 v-14 h8" fill="none" stroke="#0A1B2E" strokeWidth="2" />
      <g className="hs-smoke">
        <path
          d="M278 270 c 10 -8 2 -18 12 -24 c 10 -6 4 -16 14 -20"
          fill="none"
          stroke="#B3402F"
          strokeWidth="2"
          strokeLinecap="round"
          opacity="0.7"
        />
        <path
          d="M280 274 c 14 -4 10 -14 22 -18"
          fill="none"
          stroke="#B3402F"
          strokeWidth="2"
          strokeLinecap="round"
          opacity="0.4"
        />
      </g>

      {/* ══ dealership (center) ══ */}
      <rect x="300" y="180" width="200" height="150" rx="4" fill="#FFFFFF" stroke="#0A1B2E" strokeWidth="2" />
      {/* signage */}
      <rect x="300" y="180" width="200" height="30" rx="4" fill="#E4EDFB" stroke="#0A1B2E" strokeWidth="2" />
      <rect x="336" y="188" width="128" height="14" rx="7" fill="#FFFFFF" stroke="#0A1B2E" strokeWidth="2" />
      {/* showroom glass */}
      <rect
        x="316" y="226" width="122" height="86" rx="4"
        className="hs-win lit"
        style={{ animationDelay: "480ms" }}
        stroke="#0A1B2E" strokeWidth="2"
      />
      {/* car glyph inside */}
      <g stroke="#0A1B2E" strokeWidth="2" fill="#FFFFFF">
        <path d="M334 292 h84 a6 6 0 0 0 6 -6 v-8 a8 8 0 0 0 -8 -8 h-14 l-12 -14 h-30 l-12 14 h-8 a8 8 0 0 0 -8 8 v8 a6 6 0 0 0 6 6 z" />
        <circle cx="352" cy="294" r="8" />
        <circle cx="404" cy="294" r="8" />
      </g>
      {/* door */}
      <rect x="452" y="252" width="32" height="78" rx="2" fill="#E4EDFB" stroke="#0A1B2E" strokeWidth="2" />

      {/* ══ battery cabinet (ours, glowing current) ══ */}
      <g>
        <rect x="524" y="256" width="58" height="74" rx="6" fill="#E4EDFB" stroke="#1847C9" strokeWidth="2" />
        <rect x="534" y="268" width="38" height="8" rx="2" fill="#1847C9" />
        <rect x="534" y="282" width="38" height="8" rx="2" fill="#1847C9" opacity="0.7" />
        <rect x="534" y="296" width="38" height="8" rx="2" fill="#1847C9" opacity="0.4" />
        {/* bolt mark */}
        <path
          d="M550 310 l8 0 l-5 9 l10 -1 l-14 13 l4 -9 l-8 0 z"
          fill="#1847C9"
          stroke="none"
        />
      </g>

      {/* ══ clinic (right) ══ */}
      <rect x="606" y="210" width="100" height="120" rx="4" fill="#FFFFFF" stroke="#0A1B2E" strokeWidth="2" />
      <rect x="606" y="210" width="100" height="24" rx="4" fill="#E4EDFB" stroke="#0A1B2E" strokeWidth="2" />
      {/* cross sign */}
      <g fill="#B3402F">
        <rect x="650" y="188" width="8" height="24" rx="2" />
        <rect x="642" y="196" width="24" height="8" rx="2" />
      </g>
      {[0, 1].map((r) =>
        [0, 1].map((c) => (
          <rect
            key={`c${r}${c}`}
            x={620 + c * 40}
            y={246 + r * 40}
            width="26"
            height="26"
            rx="2"
            className={`hs-win ${r === 0 ? "lit" : ""}`}
            style={{ animationDelay: `${640 + (r * 2 + c) * 80}ms` }}
            stroke="#0A1B2E"
            strokeWidth="2"
          />
        )),
      )}

      {/* streetlight */}
      <g stroke="#0A1B2E" strokeWidth="2" fill="none">
        <path d="M508 330 v-100 q0 -10 10 -10 h6" />
        <circle cx="530" cy="220" r="5" fill="#EFA00B" stroke="#0A1B2E" />
      </g>
    </svg>
  );
}
