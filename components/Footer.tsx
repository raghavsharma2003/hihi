import { BRAND } from "@/config/business";

export default function Footer() {
  return (
    <footer className="border-t border-line bg-surface">
      <div className="mx-auto flex max-w-page flex-col gap-6 px-4 py-10 md:flex-row md:items-end md:justify-between md:px-6">
        <div>
          <p className="font-display text-22 font-bold tracking-tight">
            {BRAND.name}
          </p>
          <p className="mt-1 max-w-[48ch] text-14 text-midnight/60">
            Distributed energy for Indian commercial buildings and housing
            societies. {BRAND.region} · {BRAND.established}.
          </p>
        </div>
        <div className="font-mono text-12 text-midnight/50">
          <p>{BRAND.workingNameNote}</p>
          <p className="mt-1">
            Savings shown are calculator estimates, verified only by an audit.
          </p>
          <p className="mt-1">
            © 2026 {BRAND.name}. Placeholder legal — terms and privacy to
            follow.
          </p>
        </div>
      </div>
    </footer>
  );
}
