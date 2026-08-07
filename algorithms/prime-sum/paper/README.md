# An analytic algorithm for the sum of primes below x — manuscript

`analytic-prime-sum.tex` is the submission-format LaTeX source (compiles on
Overleaf or any TeX Live; no exotic packages). This file is the readable
summary.

## The result

**S(x) = Σ_{p≤x} p computed from zeros of the Riemann zeta function**, exact
integer recovery for x up to 10⁹ using only the first 2,000 zeros:

| x | S(x) | residual before rounding |
|---|---|---|
| 10⁶ | 37,550,402,023 | +2.8×10⁻⁶ |
| 10⁷ | 3,203,324,994,356 | −2.0×10⁻⁵ |
| 10⁸ | 279,209,790,387,276 | +6.0×10⁻⁴ |
| 10⁹ | 24,739,512,092,254,535 | +6.0×10⁻³ |

Implementation: `../prototype/analytic_sum.py`. Reference values verified by
two independent combinatorial programs (`../lucy.c`, `../fenwick.c`) and
OEIS A046731.

## The algorithm in five lines

1. Smooth the counting with the log-Gaussian cutoff
   c(t) = erfc(ln(t/x)/(√2ε))/2, whose Mellin transform is exactly
   (x^s/s)·e^(s²ε²/2) — so every zeta zero's contribution is damped by
   e^(−γ²ε²/2), a hard effective truncation.
2. Explicit formula (Perron + contour shift) for the smoothed weighted sum
   ψ̃₁(σ) = Σ Λ(n)·n^(1−σ)·c(n) — main term, zero terms, a ζ′/ζ(σ−1) term
   from the transform's pole, trivial-zero dust.
3. **Strip the logarithmic weight** — the new step: 1/ln n = ∫₀^A n^(−σ)dσ +
   n^(−A)/ln n. Integrate the explicit formula over σ ∈ [0, A]; the
   ζ′/ζ pole at σ=2 cancels the main term's pole *exactly*; the truncation
   remainder R_A is a prime-zeta-like series converging in milliseconds.
4. Subtract exact prime-power and window corrections — sieves confined to
   [x·e^(−12ε), x·e^(12ε)] and up to √x.
5. Round. Heuristic total cost O(x^(1/2+ε)) with N ~ √x zeros — the same
   exponent as Lagarias–Odlyzko/Platt for π(x).

## Novelty claim (and its honest boundaries)

- π(x) has been computed analytically and rigorously (Platt, Math. Comp.
  2015, π(10²⁴)). **No published analytic computation of prime sums is known
  to us** — that gap is what this fills, at working-algorithm level.
- The smoothing and contour technology parallels Platt; the σ-integral
  log-stripping with prime-zeta remainder is the part we have not found in
  the literature (the π(x) line uses Riemann-style li terms instead).
- What this is NOT yet: rigorous. Floating point, heuristic truncation
  bounds. Section 7 of the paper lays out the path (interval arithmetic,
  quantitative contour lemmas, certified zeros, record-scale targets).
- A referee may judge it "Platt adapted to sums." The mitigations are the
  new log-stripping mechanism, the working code, and (in a full version) a
  record computation. An expert collaborator in computational number theory
  should be brought in before submission.

## A finding of independent interest

Evaluating the window correction in double precision produces a coherent
rounding bias ~x²·2⁻⁵² that **oscillates at the zeta-zero frequencies** —
perfectly impersonating a missing explicit-formula term (it inherits the
oscillation from the window's prime-count fluctuations). Diagnosed by
recomputing wholly in 40-digit arithmetic; fixed by computing ln(p/x) via
log1p((p−x)/x) from exact integers and using high-precision erfc in the
window. Any implementation of windowed analytic prime computations will face
this; the symptom is maximally misleading (§6.1 of the paper).

## Reproduce

```
gcc -O2 -o ../fenwick ../fenwick.c -lm
python3 ../prototype/analytic_sum.py 1e9        # ~8 min single-threaded
```
Zeros: first 2,000 from mpmath `zetazero` at 25 digits (generation script
documented in `../prototype/proto_smooth.py` header) or Odlyzko's tables.
