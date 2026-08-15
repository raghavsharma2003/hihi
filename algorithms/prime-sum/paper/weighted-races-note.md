# Weighted Chebyshev races: the density curve δ(m) and its two ends

**Positioning (calibrated by an adversarial literature review — see the end).**
This work contributes computational evidence toward Problem 12 of the
Comparative Prime Number Theory problem list (Hamieh–Kadiri–Martin–Ng, arXiv:2407.03530,
posed by Koyama): the relation between the *weighted* formulation of
Chebyshev's bias (Aoki–Koyama school) and the classical *logarithmic
density* formulation (Rubinstein–Sarnak). We connect the two by computing,
for the first time for any weighted prime race, the Rubinstein–Sarnak
densities δ(m) across the whole delicate range, extending the race to
growing weights m > 0 (untouched in the literature), deriving the
density's asymptotic dissolution law in the weight aspect, and — since
the final version — proving an interpolation theorem (existence,
continuity in the weight, and an explicit rate for δ(m) → 1 on
(−1/2, 0], under GRH + LI; see item 4 below).

**The object.** D_m(x) = Σ_{p≤x, p≡3(4)} p^m − Σ_{p≡1(4)} p^m. The m ≤ 0
structure has an established literature: Aoki–Koyama (JNT 2023) proved the
critical (1/2)·log log x deflection at m = −1/2 under DRH; Sheth (2024)
under GRH; Shimada–Koyama (Aug 2025) frame m = −1/2 as the sign-change
threshold; Humphries (JNT 2013) established the same phase structure for
the weighted Liouville function; the frozen limits for m < −1/2 are
differences of Meissel–Mertens AP constants (Languasco–Zaccagnini 2010;
the difference is OEIS A086239, the constants A368645/A368646). Our claims are the pieces none of these contain.

## What is new here

1. **First numerical Rubinstein–Sarnak densities for a weighted race**
   (GRH + LI, as throughout this literature), kernel derived from our
   uniform explicit-formula framework: a_γ(m) = (2m+1)/√((m+½)²+γ²),
   bias normalized to 1, 511 self-computed zeros of L(s,χ₄), Monte Carlo
   with zero-density tail. Calibration anchor: δ(0) = 0.99593 ± 0.00003,
   matching Rubinstein–Sarnak's 0.9959.

   | m | δ(m) | exact log-measure at 10¹⁰ (sieve) |
   |---|---|---|
   | 0 | 0.99593 | (converges too slowly at 10¹⁰ — classical) |
   | 1 | 0.79731 | 0.79380 |
   | 2 | 0.69468 | 0.69275 |
   | 3 | 0.64577 | 0.64900 |

2. **The growing-weight regime m > 0**: first flip at p = 5 for every
   m ≥ 1 (vs Leech's 26,861 for counting); lead changes to 10¹⁰:
   3,082 (m=0) → 125,624 → 159,942 → 199,540. No prior work treats
   races with growing weights.

3. **The dissolution law** (weight-aspect analogue of the Fiorilli–Martin
   density asymptotic; cf. Meng's k-aspect dissolution): with
   Var(m) ~ 2(m+½)·log(2(m+½)/π) from the χ₄ zero density,
   δ(m) − ½ ~ 1/√(2π·Var(m)) as m → ∞.
   Three-way confirmation at m = 100: Monte Carlo 0.51370 ± 0.00035,
   Gaussian Φ(1/σ) 0.51379, closed-form law 0.51380. (The law is
   genuinely asymptotic: its log is negative below m ≈ 1.07.)
   Full curve computed at 15 values of m ∈ [−0.3, 100] (race_curve.py);
   δ → 1 rapidly as m → −½⁺ (δ(−0.3) = 1.000000 at 2×10⁶ samples) —
   the weight-aspect instance of the Fiorilli "highly biased" and
   Humphries δ_α → 1 phenomena.

4. **An interpolation theorem (GRH + LI), doubly red-teamed.** For
   m ∈ (−1/2, 0]: the limiting logarithmic distribution of the normalized
   race exists (Akbary–Ng–Shahabi framework, Cor 1.3(a)+Thm 1.9, applied
   to the shifted explicit formula); δ(m) ∈ (1/2, 1); m ↦ δ(m) is
   **continuous** (Lévy continuity + arcsine absolute continuity ⇒ no atom
   at 0); and 1 − δ(m) ≤ min{C(2m+1)², exp(−1/(2C(2m+1)²))} with
   C = Σ_γ 2/γ² = 0.156033 — so δ(m) → 1 as m → −1/2⁺, matching the
   Aoki–Koyama/Sheth/Hayani single-sign regime at m = −1/2. Stated for
   the θ-form race; a proposition transfers everything verbatim to the
   unlogged race D_m. NEW: the prime-race statement, the continuity in
   the weight, the explicit rate with computable constant. NOT new: the
   method (Humphries 2013 proved the Liouville analogue of the limit;
   our mechanism is his transposed — variance collapse at fixed mean
   instead of mean divergence at fixed variance; the paper says so).
   NEVER claim this answers Problem 12: it exhibits the two definitions
   as the two ends of one continuous, quantitatively controlled family —
   a conditional structural connection, not a logical inclusion; the
   problem remains open.

5. **Numerical completion of the m ≤ 0 boundary** (confirming, not
   discovering): at m = −1/2 our zero-free-parameter prediction
   D = ½·log log x + C*, C* = (M − log2 − ½)/2 + K₃ − log L(½,χ₄)
   = −0.07153, hits the exact sieve value at 10¹⁰ within 0.63σ
   (measured 1.50775 vs predicted 1.4968 ± 0.0172), with the refinement
   that the log-stripped fluctuation *decays* like √Σ/log x
   (Σ = Σ_γ 2/γ² = 0.156033) — visible decade-by-decade in the data.
   Neither race with m ∈ {−1/2, −3/4, −1} flips even once on [3, 10¹⁰]:
   the 3-side leads from the first odd prime; minimum margin
   1/√3−1/√5 ≈ 0.13014 at p = 5 (attained by the m=−½ race; the m=−1
   margin there is 2/15). Frozen limits identified with published constants:
   D_{−1}(∞) = M(4,3) − M(4,1) = 0.334981325299993181… (our independent
   Möbius-over-log-L computation agrees with Languasco–Zaccagnini/OEIS
   values to all compared digits).

## The phase diagram (attribution per regime)

| regime | behavior | status |
|---|---|---|
| m < −1/2 | frozen: sign constant, limit = Mertens-AP constant difference | classical/L–Z constants; never-flips scan + identification: this work |
| m = −1/2 | ½ log log x drift, decaying fluctuation | theorem: Aoki–Koyama/Sheth; constant C*, decay refinement + 10¹⁰ test: this work |
| −1/2 < m | delicate race, density δ(m) ∈ (½, 1) | existence: ANS/Devin-type machinery; **δ(m) values: this work, first** |
| m → ∞ | δ(m) → ½ at rate 1/√(2π·2(m+½)log(2(m+½)/π)) | **this work** (method: Fiorilli–Martin paradigm) |

## Reproduce

race_scan.c (exact races to 10¹⁰, ~40s) · race_density.py / race_curve.py
(densities; anchor δ(0)) · race_critical.py + race_critical_scan.c
(critical point) · race_frozen.py (constants + verification) — all under
prototype/explore/, every headline number independently re-run.

## Key citations for the write-up

Rubinstein–Sarnak 1994 · Aoki–Koyama JNT 2023 (arXiv:2203.12266) · Sheth
2024 (arXiv:2405.01512) · Shimada–Koyama, Mathematics 13(16):2564 (2025) ·
Humphries JNT 2013 (arXiv:1108.1524) · Fiorilli ANT 2014 (arXiv:1210.6946)
· Fiorilli–Martin (density asymptotics) · Meng 2018 · Devin MPCPS 2020
(arXiv:1706.06394) · Akbary–Ng–Shahabi QJM 2014 · Aymone IJNT 2022
(arXiv:2001.00764) · Languasco–Zaccagnini Exp. Math. 2010 (arXiv:0906.2132)
· OEIS A368645/A086239 · Hamieh–Kadiri–Martin–Ng problem list
(arXiv:2407.03530), Problem 12 · Lamzouri IJNT 2016 (Mertens race) ·
Lichtman–Martin–Pomerance PAMS 2019 (Zhang race).

**Urgency note:** Shimada–Koyama published Aug 2025; Koyama posted again
July 2026; the δ(m) interpolation is the visible next step for that
group. The density computation and m > 0 regime are ours today; they
will not stay unclaimed long.

## Modulus universality (mod 3)

The structure is not a mod-4 accident. With 537 self-computed zeros of
L(s,χ₃) (phase derived from τ(χ₃)=i√3; Z real to 4×10⁻²⁷; RvM count
535.9 vs 537 found; anchor δ₃(0) = 0.99904 vs classical 0.9990):

| m | 0 | 1 | 2 | 3 | 8 | 20 | 60 |
|---|---|---|---|---|---|---|---|
| δ₃(m) | 0.99904 | 0.83679 | 0.72361 | 0.66695 | 0.57879 | 0.54094 | 0.51917 |

The dissolution law generalizes with the modulus entering through the
zero density: **Var_q(m) ~ 2(m+½)·log(q(m+½)/2π)** (reduces to the mod-4
form at q=4), confirmed at m=60 to 0.26% in variance. Predicted ordering
δ₃(m) > δ₄(m) holds at every m (χ₃'s first zero 8.04 > χ₄'s 6.02: fewer
low-frequency fluctuations, stronger bias). Sieve scans to 10¹⁰: the
classical mod-3 race never flips below 10¹⁰ (its famous first flip is at
~6.09×10¹¹ — beyond scan, consistent ✓) while the weighted races flip at
p=13 (m=1) and p=7 (m=2,3), hand-verified. Finite-x log-measures agree
with δ₃ to 9×10⁻⁴ (m=1) and 9×10⁻³ (m=3); the m=2 gap of 0.023 at 10¹⁰
is the weakest agreement in the study (plausibly a slow almost-periodic
oscillation phase; noted honestly as unresolved).
