# Weighted Chebyshev races: exact data and the density curve δ(m)

**The new object.** For weight m ≥ 0 and the classical mod-4 race, define
D_m(x) = Σ_{p≤x, p≡3(4)} p^m − Σ_{p≤x, p≡1(4)} p^m. The case m=0 is
Chebyshev's classical bias (3-side leads with logarithmic density
0.9959…, Rubinstein–Sarnak 1994; first 1-side lead at x=26,861, Leech).
The cases m ≥ 1 — races weighted by the primes themselves — appear never
to have been computed, either exactly or in density.

**The mechanism (from our uniform explicit formula).** In θ-form the race
satisfies R_m(x) = x^{m+1/2}/(2m+1) + Σ_ρ x^{ρ+m}/(ρ+m) + …, ρ over
zeros of L(s,χ₄). The bias term (from prime squares, all ≡1 mod 4)
normalizes to the constant 1 while the zero-fluctuation coefficients
grow like (2m+1)/γ: heavier weights amplify the oscillation against a
fixed bias, so **Chebyshev's bias weakens as the weight grows** — a
single heavy prime (already p=5 vs p=3) can flip the race that counting
could not flip before 26,861.

**Results (all in this repo, independently anchored).**

Asymptotic logarithmic densities δ(m) = P(3-side leads), computed by
Monte Carlo from the 511 zeros of L(s,χ₄) in `prototype/explore/chi4_zeros.txt`
with kernel a_γ(m) = (2m+1)/√((m+½)²+γ²), Gaussian tail correction, 4×10⁶
samples (`race_density.py`), under the standard GRH + linear-independence
assumptions of this literature:

| m | δ(m) (asymptotic) | exact log-measure at 10¹⁰ | first 1-lead | lead changes to 10¹⁰ |
|---|---|---|---|---|
| 0 | 0.99593 ± 0.00003 (matches classical 0.9959 ✓) | 0.99905* | 26,861 ✓ Leech | 3,082 |
| 1 | 0.79731 ± 0.00020 | 0.79380 | 5 | 125,624 |
| 2 | 0.69468 ± 0.00023 | 0.69275 | 5 | 159,942 |
| 3 | 0.64577 ± 0.00024 | 0.64900 | 5 | 199,540 |

\* the m=0 log-measure converges notoriously slowly (classical); for
m ≥ 1 the exact scans already agree with the asymptotic densities to
~3×10⁻³ at 10¹⁰.

Exact scans by segmented sieve with signed __int128 accumulators
(`race_scan.c`, ~40 s to 10¹⁰); densities cross-validated by the double
anchor (Leech's 26,861 and Rubinstein–Sarnak's 0.9959 both reproduced).

**Placement in the literature.** The limiting-distribution framework is
Rubinstein–Sarnak (1994) as generalized by Devin ("Chebyshev's bias for
analytic L-functions"); weighted races have precedent (the "Mertens
race", the "Zhang race" Σ1/(p log p)); products-of-primes biases are
Ford–Sneed and Meng. The p^m family, its closed-form kernel, the δ(m)
curve, and the exact large-x data appear new. Our exact analytic AP
machinery (`ap_sums.py`) can evaluate these races at isolated large x
beyond sieve range — the capability that motivated this study.

**Honest scale.** This is a computational-phenomenon paper-section, not
a theorem: densities are conditional on GRH+LI exactly as in the parent
literature, and the derivation of the kernel is at the same
heuristic-plus-numerical-validation standard as the rest of this
project. It is, to our knowledge, the first quantification of how
Chebyshev's bias dissolves under polynomial weighting.
