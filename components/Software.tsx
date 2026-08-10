import Eyebrow from "./Eyebrow";
import Reveal from "./Reveal";

/**
 * S7 — the software teaser. Three illustrated UI frames drawn flat in the
 * system palette (never screenshots), tilted 2° and straightening on enter.
 */
export default function Software() {
  return (
    <section
      id="software"
      aria-labelledby="software-heading"
      className="scroll-mt-24 bg-sky/40 py-16 md:py-24"
    >
      <div className="mx-auto max-w-page px-4 md:px-6">
        <Eyebrow>05 / The software</Eyebrow>
        <h2
          id="software-heading"
          className="mt-2 max-w-[24ch] font-display text-40 font-bold tracking-tight md:text-56"
        >
          The battery is hardware. The product is the brain.
        </h2>

        <div className="mt-10 grid gap-6 md:grid-cols-3">
          <Frame delay={0} title="Live dispatch" caption="grid, battery and genset flows — every minute, every site">
            <DispatchMock />
          </Frame>
          <Frame delay={70} title="Savings ledger" caption="verified ₹, month by month — the number our fee is judged against">
            <LedgerMock />
          </Frame>
          <Frame delay={140} title="Cut-risk forecast" caption="the locked reserve, re-sized by hour from your cut history">
            <ForecastMock />
          </Frame>
        </div>

        <p className="mt-8 text-16 text-midnight/70 md:text-18">
          Every site reports every minute. You see what we see.
        </p>
      </div>
    </section>
  );
}

function Frame({
  title,
  caption,
  delay = 0,
  children,
}: {
  title: string;
  caption: string;
  /** 70ms steps: enough to read as a sequence, short enough to feel like one move. */
  delay?: number;
  children: React.ReactNode;
}) {
  return (
    <Reveal as="figure" delay={delay} className="soft-frame">
      <div className="overflow-hidden rounded-card border border-line bg-surface shadow-card">
        <div className="flex items-center gap-1.5 border-b border-line bg-daylight px-4 py-2.5">
          <span className="h-2 w-2 rounded-full bg-line" />
          <span className="h-2 w-2 rounded-full bg-line" />
          <span className="ml-2 font-mono text-12 text-midnight/60">
            {title.toLowerCase()}
          </span>
        </div>
        {children}
      </div>
      <figcaption className="mt-3 text-14 text-midnight/65">
        <span className="font-semibold text-midnight">{title}.</span> {caption}
      </figcaption>
    </Reveal>
  );
}

function DispatchMock() {
  return (
    <svg viewBox="0 0 280 170" className="w-full" role="img" aria-label="Illustrated dispatch screen: energy flowing from grid and battery to the building, genset idle">
      <rect x="16" y="16" width="72" height="30" rx="6" fill="#E4EDFB" stroke="#1847C9" strokeWidth="2" />
      <text x="52" y="35" textAnchor="middle" fontSize="11" fill="#1847C9" fontFamily="var(--font-mono)">grid</text>
      <rect x="16" y="70" width="72" height="30" rx="6" fill="#E4EDFB" stroke="#1847C9" strokeWidth="2" />
      <text x="52" y="89" textAnchor="middle" fontSize="11" fill="#1847C9" fontFamily="var(--font-mono)">battery</text>
      <rect x="16" y="124" width="72" height="30" rx="6" fill="#FFFFFF" stroke="#0A1B2E" strokeWidth="2" opacity="0.5" />
      <text x="52" y="143" textAnchor="middle" fontSize="11" fill="#0A1B2E" opacity="0.6" fontFamily="var(--font-mono)">genset·off</text>
      <g stroke="#1847C9" strokeWidth="2" fill="none">
        <path d="M88 31 C 130 31 130 85 168 85" />
        <path d="M88 85 h80" />
      </g>
      <path d="M88 139 C 130 139 130 95 168 95" stroke="#DFE5EE" strokeWidth="2" fill="none" strokeDasharray="4 4" />
      <rect x="168" y="55" width="96" height="60" rx="6" fill="#FFFFFF" stroke="#0A1B2E" strokeWidth="2" />
      {[0, 1, 2].map((c) => (
        <rect key={c} x={180 + c * 26} y="67" width="16" height="14" rx="2" fill="#EFA00B" opacity="0.85" stroke="#0A1B2E" strokeWidth="2" />
      ))}
      <text x="216" y="105" textAnchor="middle" fontSize="11" fill="#0A1B2E" opacity="0.6" fontFamily="var(--font-mono)">your site</text>
    </svg>
  );
}

function LedgerMock() {
  const rows = [56, 62, 58, 71, 66, 74];
  return (
    <svg viewBox="0 0 280 170" className="w-full" role="img" aria-label="Illustrated savings ledger: six monthly bars stepping upward with verified rupee savings">
      {rows.map((v, i) => (
        <g key={i}>
          <rect
            x={24 + i * 42}
            y={150 - v}
            width="26"
            height={v}
            rx="4"
            fill="#EFA00B"
            opacity="0.85"
          />
          <line x1={24 + i * 42} y1="150" x2={50 + i * 42} y2="150" stroke="#0A1B2E" strokeWidth="2" />
        </g>
      ))}
      <text x="24" y="30" fontSize="12" fill="#0A1B2E" opacity="0.65" fontFamily="var(--font-mono)">verified savings / mo</text>
      <text x="256" y="70" textAnchor="end" fontSize="14" fill="#EFA00B" fontFamily="var(--font-mono)">₹24,310</text>
    </svg>
  );
}

function ForecastMock() {
  return (
    <svg viewBox="0 0 280 170" className="w-full" role="img" aria-label="Illustrated cut-risk dial: reserved battery share by hour of day">
      <defs>
        <pattern id="fchatch" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
          <rect width="7" height="7" fill="#E4EDFB" />
          <line x1="0" y1="0" x2="0" y2="7" stroke="#1847C9" strokeWidth="2" />
        </pattern>
      </defs>
      <circle cx="90" cy="88" r="52" fill="#FFFFFF" stroke="#0A1B2E" strokeWidth="2" />
      <path d="M90 88 L90 36 A52 52 0 0 1 135 62 Z" fill="url(#fchatch)" stroke="#1847C9" strokeWidth="2" />
      <text x="90" y="152" textAnchor="middle" fontSize="11" fill="#0A1B2E" opacity="0.6" fontFamily="var(--font-mono)">reserved 30%</text>
      {[0.5, 0.3, 0.7, 0.9, 0.4].map((v, i) => (
        <rect
          key={i}
          x={176 + i * 20}
          y={130 - v * 80}
          width="12"
          height={v * 80}
          rx="3"
          fill={v > 0.6 ? "#B3402F" : "#E4EDFB"}
          opacity={v > 0.6 ? 0.8 : 1}
          stroke="#0A1B2E"
          strokeWidth="2"
        />
      ))}
      <text x="222" y="152" textAnchor="middle" fontSize="11" fill="#0A1B2E" opacity="0.6" fontFamily="var(--font-mono)">cut risk by hour</text>
    </svg>
  );
}
