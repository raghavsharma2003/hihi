/** Indian-format money: ₹48,500 / ₹1.2L / ₹1.05Cr — mono-friendly, short. */
export function formatINR(value: number): string {
  const v = Math.round(value);
  if (v >= 10000000) return `₹${trim((v / 10000000).toFixed(2))}Cr`;
  if (v >= 100000) return `₹${trim((v / 100000).toFixed(1))}L`;
  return `₹${v.toLocaleString("en-IN")}`;
}

/** Full Indian grouping, no abbreviation: ₹1,05,000 */
export function formatINRFull(value: number): string {
  return `₹${Math.round(value).toLocaleString("en-IN")}`;
}

export function formatYears(value: number): string {
  if (!isFinite(value)) return "—";
  return trim(value.toFixed(1));
}

export function formatKwh(value: number): string {
  return `${Math.round(value)} kWh`;
}

export function formatLitres(value: number): string {
  return `${Math.round(value).toLocaleString("en-IN")} L`;
}

function trim(s: string): string {
  return s.replace(/\.0+$/, "").replace(/(\.\d*[1-9])0+$/, "$1");
}
