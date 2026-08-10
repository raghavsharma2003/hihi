"use client";

import { useEffect, useState } from "react";
import { BRAND } from "@/config/business";

type Status = "idle" | "sending" | "sent" | "error";

/** Strong ease-out — the one curve this form uses. */
const EASE_OUT = "ease-[cubic-bezier(0.23,1,0.32,1)]";

/** True one frame after mount, so a freshly rendered node can transition in. */
function useEntered() {
  const [entered, setEntered] = useState(false);
  useEffect(() => {
    const id = requestAnimationFrame(() => setEntered(true));
    return () => cancelAnimationFrame(id);
  }, []);
  return entered;
}

/**
 * Lead capture: name, phone, pincode, business type.
 * POSTs to the placeholder API route; WhatsApp deep link as the alternative.
 */
export default function LeadForm({ context }: { context: string }) {
  const [status, setStatus] = useState<Status>("idle");

  async function submit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const form = e.currentTarget;
    const data = Object.fromEntries(new FormData(form).entries());
    setStatus("sending");
    try {
      const res = await fetch("/api/lead", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ...data, context }),
      });
      if (!res.ok) throw new Error(`lead POST failed: ${res.status}`);
      setStatus("sent");
    } catch {
      setStatus("error");
    }
  }

  const whatsappHref = `https://wa.me/${BRAND.whatsappNumber}?text=${encodeURIComponent(
    `Hi ${BRAND.name} — I'd like a free savings audit for my ${context === "society" ? "housing society" : "building"}.`,
  )}`;

  if (status === "sent") {
    return <SuccessPanel />;
  }

  return (
    <form onSubmit={submit} className="grid gap-3">
      <div className="grid gap-3 sm:grid-cols-2">
        <Field name="name" label="Name" autoComplete="name" />
        <Field
          name="phone"
          label="Phone"
          type="tel"
          autoComplete="tel"
          pattern="[0-9+ -]{10,15}"
          title="10-digit mobile number"
        />
        <Field
          name="pincode"
          label="Pincode"
          inputMode="numeric"
          pattern="[0-9]{6}"
          title="6-digit pincode"
        />
        <div>
          <label
            htmlFor="lead-type"
            className="mb-1 block text-14 font-semibold"
          >
            Business type
          </label>
          <select
            id="lead-type"
            name="businessType"
            required
            className="w-full rounded-input border border-line bg-surface px-3 py-2 text-16"
            defaultValue={context === "society" ? "Housing society" : ""}
          >
            <option value="" disabled>
              Select one
            </option>
            <option>Dealership</option>
            <option>Hospital or clinic</option>
            <option>Hotel or banquet</option>
            <option>Bank or office</option>
            <option>Housing society</option>
            <option>Other commercial</option>
          </select>
        </div>
      </div>
      {status === "error" && <ErrorNote />}
      <div className="flex flex-wrap items-center gap-3">
        <button
          type="submit"
          disabled={status === "sending"}
          className={`rounded-full bg-current px-6 py-3 text-16 font-semibold text-surface transition-[transform,opacity] duration-150 ${EASE_OUT} [@media(hover:hover)_and_(pointer:fine)]:hover:scale-[1.03] active:scale-[0.98] active:duration-100 disabled:opacity-60`}
        >
          {status === "sending" ? "Sending…" : "Request the free audit"}
        </button>
        <a
          href={whatsappHref}
          target="_blank"
          rel="noopener noreferrer"
          className={`rounded-full border border-current px-6 py-3 text-16 font-semibold text-current transition-[background-color,transform] duration-150 ${EASE_OUT} hover:bg-sky active:scale-[0.98] active:duration-100`}
        >
          WhatsApp us instead
        </a>
      </div>
    </form>
  );
}

/** Rare, first-time moment: it gets the fade + 4px rise. */
function SuccessPanel() {
  const entered = useEntered();
  return (
    <div
      className={`rounded-card border border-line bg-sky p-4 transition-[opacity,transform] duration-200 ${EASE_OUT} ${
        entered ? "translate-y-0 opacity-100" : "translate-y-[4px] opacity-0"
      }`}
    >
      <p className="text-16 font-semibold">Audit request received.</p>
      <p className="mt-1 text-14 text-midnight/70">
        We call within one working day, and your one-page money map arrives
        within 72 hours of the site visit.
      </p>
    </div>
  );
}

/** Fade only — an error the user must read should not slide under their eye. */
function ErrorNote() {
  const entered = useEntered();
  return (
    <p
      role="alert"
      className={`text-14 font-semibold text-dieselclay transition-opacity duration-150 ${EASE_OUT} ${
        entered ? "opacity-100" : "opacity-0"
      }`}
    >
      The request didn&apos;t go through. Try again, or use WhatsApp below.
    </p>
  );
}

function Field({
  name,
  label,
  type = "text",
  ...rest
}: {
  name: string;
  label: string;
  type?: string;
} & React.InputHTMLAttributes<HTMLInputElement>) {
  return (
    <div>
      <label htmlFor={`lead-${name}`} className="mb-1 block text-14 font-semibold">
        {label}
      </label>
      <input
        id={`lead-${name}`}
        name={name}
        type={type}
        required
        className="w-full rounded-input border border-line bg-surface px-3 py-2 text-16 placeholder:text-midnight/40"
        {...rest}
      />
    </div>
  );
}
