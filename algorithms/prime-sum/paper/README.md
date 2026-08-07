# Computing weighted prime sums from zeros of ζ and Dirichlet L-functions — manuscript

`analytic-prime-sum.tex` is the submission-format LaTeX source (compiles on
Overleaf; standard packages only). `prior-art-review.md` is the adversarial
literature sweep that shaped the claims. This file is the readable summary.

## The results (all independently re-verified)

One framework, from the first 2,000 zeta zeros (plus 511 self-computed
L(s,χ₄) zeros for progressions):

| quantity | largest verified x | value | residual |
|---|---|---|---|
| S₁(x) = Σp | 10⁹ | 24,739,512,092,254,535 | +6.0×10⁻³ |
| π(x) | 10⁸ | 5,761,455 | +6.0×10⁻¹² |
| S₂(x) = Σp² | 10⁷ | 21,113,978,675,102,768,574 | −6.8×10⁻⁶ |
| S₃(x) = Σp³ | 10⁷ | 157,468,033,886,449,157,634,628,898 | +2.3×10⁻³ |
| Σ 1/p | 10⁷ | 3.0414493812797104945 (17 digits) | −3×10⁻¹⁸ |
| Σp, p≡1 mod 4 | 10⁷ | 1,601,423,376,628 | −6.0×10⁻⁶ |
| Σp, p≡3 mod 4 | 10⁷ | 1,601,901,617,726 | −6.2×10⁻⁶ |

Every quantity also verified at smaller powers of 10; every exact-integer
row rounds correctly. Scripts: `../prototype/analytic_sum.py` (m=1) and
`../prototype/explore/{pi_lifree,power_sums,mertens,ap_sums}.py`.

## Claims, calibrated by the prior-art sweep

- **Novel (as computation):** no published implementation recovering exact
  prime sums — any weight, or in progressions — was found. The underlying
  explicit formulas are classical (Riesz means; Montgomery–Vaughan), and the
  paper says so.
- **Operational, not mechanistic:** the σ-integral log-stripping is
  Fubini-equivalent to the classical log ζ representation (Lagarias–Odlyzko,
  Platt). Its value: elementary erfc/exp integrands, one pair-cancellation
  lemma for every pole collision, no li(x^ρ), no kernel special functions
  (FKBJ/Büthe), no branch tracking (Platt), and one code path for every
  weight m ∈ {−1,0,1,2,3} and every character.
- **Li-free π(x) is NOT claimed as new** — FKBJ (2017) and Büthe already
  compute π(x) li-free on the Weil–Barner side; our π(x) run demonstrates
  uniformity of the framework, nothing more.
- **AP sums:** exact integer recovery from Dirichlet L-zeros appears new
  (Bays–Hudson 2000 computed approximate irregularities); presented as an
  engineering consequence of uniformity.

## Two measured phenomena of independent interest

1. **Coherent rounding at zero frequencies** (§6.1): double-precision window
   sums develop a bias ~x^{m+1}·2⁻⁵² oscillating at zeta-zero frequencies —
   perfectly impersonating a missing explicit-formula term. Remedy:
   log1p((p−x)/x) on exact integers + high-precision erfc.
2. **Zero-ordinate precision floor** (§6.2): phase error δγ·ln x enters at
   amplitude ~x^{m+1/2}; 25-digit ordinates already fail at m=3, x=10⁷
   (−16.9 off). Newton-refining the leading zeros to 40 digits restores
   10⁻³ residuals. The floor formula reproduces observed residuals at every
   (m, x).

## Status and path to submission

Floating-point with heuristic (numerically validated) truncation bounds —
NOT yet rigorous. Before submission: quantitative contour lemmas, interval
arithmetic, certified zero enclosures, and ideally a record-scale flagship
(S₁(10²²) cross-checked against primesum). Take this draft plus the code to
a computational number theorist; the AI-assistance disclosure is already in
the manuscript.

## Reproduce

```
gcc -O2 -o ../fenwick ../fenwick.c -lm
python3 ../prototype/analytic_sum.py 1e9          # S1, ~8 min
python3 ../prototype/explore/pi_lifree.py 1e6 1e7 1e8
python3 ../prototype/explore/power_sums.py 2 1e7
python3 ../prototype/explore/mertens.py
python3 ../prototype/explore/ap_sums.py run 1e6
```
