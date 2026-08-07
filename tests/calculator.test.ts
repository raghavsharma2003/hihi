import { describe, expect, it } from "vitest";
import { calculate, estimateKw } from "@/lib/calculator";

describe("commercial calculation", () => {
  const input = {
    mode: "commercial" as const,
    bill: 150000,
    diesel: 64000,
    kw: 50,
  };

  it("implements the brief's formulas exactly", () => {
    const r = calculate(input);
    const dgEffUnits = 64000 / 32; // 2000
    const replaced = 0.78 * dgEffUnits; // 1560
    const dieselSaving = replaced * (32 - 13); // 29640
    const demandTrim = Math.min(50, 50) * 0.12 * 200; // 1200
    const battKwh = (50 * 2) / 0.9; // 111.11
    const tariffGain = battKwh * 0.9 * 26; // 2600
    const monthly = dieselSaving + demandTrim + tariffGain;

    expect(r.monthlySavingLow).toBeCloseTo(monthly * 0.85, 5);
    expect(r.monthlySavingHigh).toBeCloseTo(monthly * 1.15, 5);
    expect(r.yearlySavingLow).toBeCloseTo(monthly * 0.85 * 12, 5);
    expect(r.battKwh).toBeCloseTo(battKwh, 5);
    expect(r.capexLow).toBeCloseTo(battKwh * 18000, 5);
    expect(r.capexHigh).toBeCloseTo(battKwh * 20000, 5);
    expect(r.litresPerYear).toBeCloseTo((replaced * 12) / 3.1, 5);
    expect(r.viable).toBe(true);
  });

  it("caps demand trim at 50 kW", () => {
    const at50 = calculate({ ...input, kw: 50 });
    const at100 = calculate({ ...input, kw: 100 });
    // higher kW still helps via battery size, but demand trim is capped:
    // difference must come only from tariff gain + capex, i.e. the delta of
    // monthly savings equals delta of tariff gain
    const battDelta = at100.battKwh - at50.battKwh;
    const expectedDelta = battDelta * 0.9 * 26;
    const monthlyDelta =
      at100.monthlySavingHigh / 1.15 - at50.monthlySavingHigh / 1.15;
    expect(monthlyDelta).toBeCloseTo(expectedDelta, 4);
  });

  it("fails honestly below ₹10k diesel", () => {
    expect(calculate({ ...input, diesel: 9999 }).viable).toBe(false);
    expect(calculate({ ...input, diesel: 10000 }).viable).toBe(true);
  });

  it("estimates kW from the bill when not sure", () => {
    const kw = estimateKw(150000);
    expect(kw).toBeGreaterThanOrEqual(10);
    expect(kw).toBeLessThanOrEqual(100);
    const r = calculate({ ...input, kw: null });
    expect(r.battKwh).toBeCloseTo((kw * 2) / 0.9, 5);
  });
});

describe("society calculation", () => {
  const input = {
    mode: "society" as const,
    flats: 250,
    diesel: 150000,
    cutHours: 2,
  };

  it("sizes the battery from flats and skips demand trim", () => {
    const r = calculate(input);
    const battKwh = 250 * 1.2; // 300
    const replaced = 0.78 * (150000 / 32);
    const dieselSaving = replaced * 19;
    const tariffGain = battKwh * 0.9 * 26;
    const monthly = dieselSaving + tariffGain; // no demand trim

    expect(r.battKwh).toBe(battKwh);
    expect(r.monthlySavingLow).toBeCloseTo(monthly * 0.85, 5);
    expect(r.viable).toBe(true);
  });

  it("fails honestly under 1 cut-hour a day", () => {
    expect(calculate({ ...input, cutHours: 0.5 }).viable).toBe(false);
    expect(calculate({ ...input, cutHours: 1 }).viable).toBe(true);
  });
});

describe("payback", () => {
  it("uses the capex band over the savings band", () => {
    const r = calculate({
      mode: "commercial",
      bill: 150000,
      diesel: 64000,
      kw: 50,
    });
    expect(r.paybackLowYears).toBeCloseTo(
      r.capexLow / (12 * r.monthlySavingHigh),
      6,
    );
    expect(r.paybackHighYears).toBeCloseTo(
      r.capexHigh / (12 * r.monthlySavingLow),
      6,
    );
    expect(r.paybackLowYears).toBeLessThan(r.paybackHighYears);
  });
});
