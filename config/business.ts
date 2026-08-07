/**
 * Single source of truth for the brand and every number the site shows.
 * The brand name WILL change — rename it here and nowhere else.
 * Calculator constants mirror the formulas used in paid audits; change them
 * here and the calculator, copy chips, and design-tokens page all follow.
 */

export const BRAND = {
  name: "PranaWatt",
  workingNameNote: "PranaWatt is a working name.",
  region: "NCR",
  established: "est. 2026",
  phone: "+91 98100 00000",
  whatsappNumber: "919810000000",
  email: "audit@pranawatt.example",
} as const;

export const CALC = {
  /** ₹/unit a diesel genset effectively charges */
  DG_RATE: 32,
  /** ₹/unit we serve the same hour at */
  SERVE_RATE: 13,
  /** share of genset units the battery realistically replaces */
  REPLACE_FACTOR: 0.78,
  /** demand-trim: ₹/kW-month recovered on sanctioned demand, conservative */
  DEMAND_TRIM_RATE: 200,
  DEMAND_TRIM_FACTOR: 0.12,
  DEMAND_TRIM_KW_CAP: 50,
  /** tariff arbitrage: ₹/unit-day on the free portion, ~26 free-portion days */
  TARIFF_GAIN_PER_UNIT_DAY: 0.9,
  TARIFF_GAIN_DAYS: 26,
  /** result shown as a range, not a promise */
  RANGE_LOW: 0.85,
  RANGE_HIGH: 1.15,
  /** battery sizing */
  SOCIETY_KWH_PER_FLAT: 1.2,
  COMMERCIAL_KWH_PER_KW: 2 / 0.9,
  /** capex ₹/kWh, with honest band */
  CAPEX_PER_KWH: 19000,
  CAPEX_PER_KWH_LOW: 18000,
  CAPEX_PER_KWH_HIGH: 20000,
  /** litres: ₹ of diesel per unit → litres via ~3.1 units per litre */
  UNITS_PER_LITRE: 3.1,
  /** honest-fail thresholds */
  MIN_COMMERCIAL_DIESEL: 10000,
  MIN_SOCIETY_CUT_HOURS: 1,
  /** grid tariff used to estimate connection size when the visitor is not sure */
  EST_GRID_RATE: 8.5,
  EST_RUN_HOURS_PER_MONTH: 300,
} as const;

export const INPUT_BOUNDS = {
  commercial: {
    bill: { min: 20000, max: 500000, step: 5000, default: 150000 },
    diesel: { min: 0, max: 200000, step: 2500, default: 40000 },
    kw: { min: 10, max: 100, step: 5, default: 50 },
  },
  society: {
    flats: { min: 100, max: 800, step: 10, default: 250 },
    diesel: { min: 50000, max: 500000, step: 5000, default: 150000 },
    cutHours: { min: 0.5, max: 6, step: 0.5, default: 2 },
  },
} as const;

export const PRICES_LADDER = [
  { label: "own solar", range: "₹3.2", value: 3.2, tone: "current" },
  { label: "grid tariff", range: "₹7–9", value: 8, tone: "midnight" },
  { label: "grid effective, peak + demand", range: "₹10–15.6", value: 13, tone: "sunsave" },
  { label: "diesel genset", range: "₹28–32", value: 32, tone: "dieselclay" },
] as const;

export const OFFERINGS = {
  commercialSavings: "₹17–28k/mo",
  societySavings: "₹70k–1.1L/mo",
  autopilotPrice: "₹149–199/mo",
  autopilotPool: "₹250–700/mo pool",
  commercialCapex: "₹9–11L",
  societyCapex: "₹42–55L",
  contractYears: "5–7 year",
} as const;
