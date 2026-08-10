import { BRAND } from "@/config/business";

export default function Footer() {
  return (
    <footer className="border-t border-line bg-surface">
      {/* Same page gutters and max width as every section above, so the brand
          line sits on the same left edge as the headings. */}
      <div className="mx-auto flex max-w-page flex-col gap-8 px-4 py-12 md:flex-row md:items-end md:justify-between md:gap-16 md:px-6 md:py-16">
        <div>
          <p className="font-display text-22 font-bold tracking-tight">
            {BRAND.name}
          </p>
          <p className="mt-2 max-w-[52ch] text-14 text-midnight/70">
            Distributed energy for Indian commercial buildings and housing
            societies. {BRAND.region} · {BRAND.established}.
          </p>
        </div>
        {/* /70 not /50 — these lines carry the honesty of the page (working
            name, estimate caveat), so they have to clear 4.5:1. */}
        <div className="max-w-[56ch] space-y-1.5 font-mono text-12 text-midnight/70">
          <p>{BRAND.workingNameNote}</p>
          <p>
            Savings shown are calculator estimates, verified only by an audit.
          </p>
          <p>
            © 2026 {BRAND.name}. Placeholder legal — terms and privacy to
            follow.
          </p>
        </div>
      </div>
    </footer>
  );
}
