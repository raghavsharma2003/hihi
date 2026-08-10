import { CALC } from "@/config/business";

export type Mode = "commercial" | "society";

export interface CommercialInput {
  mode: "commercial";
  /** ₹/month electricity bill */
  bill: number;
  /** ₹/month diesel spend */
  diesel: number;
  /** connection size in kW; null = "not sure" */
  kw: number | null;
}

export interface SocietyInput {
  mode: "society";
  flats: number;
  /** ₹/month society diesel spend */
  diesel: number;
  /** power-cut hours per day */
  cutHours: number;
}

export type CalcInput = CommercialInput | SocietyInput;

export interface CalcResult {
  viable: boolean;
  monthlySavingLow: number;
  monthlySavingHigh: number;
  yearlySavingLow: number;
  yearlySavingHigh: number;
  litresPerYear: number;
  paybackLowYears: number;
  paybackHighYears: number;
  battKwh: number;
  capexLow: number;
  capexHigh: number;
}

/** Estimate connection size from the bill when the visitor picks "not sure". */
export function estimateKw(bill: number): number {
  const unitsPerMonth = bill / CALC.EST_GRID_RATE;
  const kw = unitsPerMonth / CALC.EST_RUN_HOURS_PER_MONTH;
  return Math.min(100, Math.max(10, Math.round(kw)));
}

export function calculate(input: CalcInput): CalcResult {
  const isSociety = input.mode === "society";

  const viable = isSociety
    ? input.cutHours >= CALC.MIN_SOCIETY_CUT_HOURS
    : input.diesel >= CALC.MIN_COMMERCIAL_DIESEL;

  const kw = isSociety ? 0 : input.kw ?? estimateKw(input.bill);

  const battKwh = isSociety
    ? input.flats * CALC.SOCIETY_KWH_PER_FLAT
    : kw * CALC.COMMERCIAL_KWH_PER_KW;

  const dgEffUnits = input.diesel / CALC.DG_RATE;
  const replaced = CALC.REPLACE_FACTOR * dgEffUnits;
  const dieselSaving = replaced * (CALC.DG_RATE - CALC.SERVE_RATE);

  const demandTrim = isSociety
    ? 0
    : Math.min(kw, CALC.DEMAND_TRIM_KW_CAP) *
      CALC.DEMAND_TRIM_FACTOR *
      CALC.DEMAND_TRIM_RATE;

  const tariffGain =
    battKwh * CALC.TARIFF_GAIN_PER_UNIT_DAY * CALC.TARIFF_GAIN_DAYS;

  const monthly = dieselSaving + demandTrim + tariffGain;
  const monthlySavingLow = monthly * CALC.RANGE_LOW;
  const monthlySavingHigh = monthly * CALC.RANGE_HIGH;

  const capexLow = battKwh * CALC.CAPEX_PER_KWH_LOW;
  const capexHigh = battKwh * CALC.CAPEX_PER_KWH_HIGH;

  return {
    viable,
    monthlySavingLow,
    monthlySavingHigh,
    yearlySavingLow: monthlySavingLow * 12,
    yearlySavingHigh: monthlySavingHigh * 12,
    litresPerYear: (replaced * 12) / CALC.UNITS_PER_LITRE,
    paybackLowYears: capexLow / (12 * monthlySavingHigh),
    paybackHighYears: capexHigh / (12 * monthlySavingLow),
    battKwh,
    capexLow,
    capexHigh,
  };
}
