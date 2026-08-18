# Path to a peer-reviewed publication

What peer review demands here: a contribution over the *entire* published
literature, reviewed by people who know Legendre/Meissel, Lucy_Hedgehog,
Deléglise–Rivat, min_25, and Kim Walisch's implementations in detail. The code
in this directory — correct, benchmarked, orders of magnitude past the sieve —
is a *reimplementation study*. No journal accepts it as new research, because
every technique in it is published (see README.md's prior-art map).

Below are the research targets that could clear the bar, ranked by how
promising the gap looks after a literature check (August 2026).

## Candidate A — analytic computation of the sum of primes (strongest gap)

π(x) has been computed **analytically** — explicit formula over the zeros of
the Riemann zeta function, rigorous interval arithmetic, unconditional record
π(10²⁴): Platt, *Computing π(x) analytically*, Math. Comp. (arXiv:1203.5712);
see also Büthe's analytic π(x) work. The prime **sum** analog — the same
explicit-formula machinery applied to Σ_{p≤x} p (a Chebyshev-type weighted
sum, or Σ p^k generally) with rigorous error control — does **not** appear in
the literature. All published prime-sum records (primesum, 10²⁰⁺) are
combinatorial.

- Contribution: derive the truncated explicit formula for Σ p ≤ x with
  explicit error bounds; implement with interval arithmetic and a verified
  zeta-zeros database; validate against primesum's range; set an unconditional
  record (e.g. 10²⁴⁺).
- Complexity target: O(x^(1/2+ε)) — asymptotically *below* every combinatorial
  method, which answers "beat the sieve" in the strongest possible sense.
- Venue: Mathematics of Computation, LMS J. Comput. Math., or ANTS.
- Risk: a referee may call it a routine extension of Platt — mitigated by the
  record computation and by the technical work in the error analysis (the
  weight p makes the zero-sum converge more slowly than for π(x)).
- Effort: a 1–2 year project; realistically needs an advisor in analytic /
  computational number theory. This is a thesis topic, not a weekend.

## Candidate B — space-efficient prime sums

Staple (arXiv:1503.01839) got π(x) down to O(x^(1/3) log² x) memory and
computed π(10²⁶). The prime-sum analog is harder than it looks: sums need
128/256-bit accumulators, and the Fenwick/segment structures multiply that
cost. A prime-sum algorithm at O(x^(1/3+ε)) memory with matching records
would be publishable in the same venues. Risk: primesum's internals may
already effectively do this without a standalone paper claiming it — a close
reading of its implementation is the first step.

## Candidate C — new targets for the min_25 machinery

The min_25 sieve computes Σ f(p)-type quantities in ~x^(2/3) for many
multiplicative f. Picking a function with an *application* (primes in
residue classes feeding an equidistribution question, sums tied to a
conjecture that wants numerical evidence) makes the computation itself the
contribution. Venue: Experimental Mathematics, or Involve / Rose-Hulman UMJ
for an undergraduate-led paper. Lowest risk, moderate prestige, fastest.

## Candidate D — rigorous experimental study / hardware

GPU or SIMD implementations of the x^(2/3) class with a careful experimental
methodology fit ACM JEA (Journal of Experimental Algorithmics). Peer-reviewed,
respectable, but reads as engineering, not number theory.

## Recommended sequence

1. Read Platt (arXiv:1203.5712) and Büthe's analytic-π(x) paper; derive the
   explicit formula for Σ p ≤ x on paper. (Weeks; costs nothing.)
2. Prototype non-rigorously: truncated zero-sum with ~10⁴ zeros, compare
   against fenwick.c up to 10¹³. If the numbers converge as the error bound
   predicts, Candidate A is alive. (This directory's code is the oracle.)
3. Take the derivation + prototype to a computational number theorist as a
   thesis/collaboration proposal.
4. In parallel, publish the honest expository piece (README.md's benchmarks:
   rediscovery → n^(3/4) → n^(2/3)) as a blog post — it builds the public
   record that you do this work carefully, which matters when the real paper
   goes out.

## Step 2 executed: prototype results (see `prototype/`)

Both prototypes are implemented and run against the exact values from
`fenwick.c` (August 2026, this repo).

**Derived formulas** (non-rigorous constants, RH assumed in the zero range —
true for all zeros used):

- Sharp: `T(x) = sum_{p^k<=x} p^k/k = li(x^2) - sum_rho li(x^(rho+1)) + O(1)`,
  and `S(x) = T(x) - (exact prime-power correction)`. The li-terms are
  `Ei((rho+1) ln x)`, computed by the asymptotic series; the ±iπ branch
  constants cancel over conjugate zero pairs.
- Smoothed: for the log-Gaussian cutoff `c(t) = erfc(ln(t/x)/(sqrt(2)eps))/2`
  the Mellin transform is exactly `x^s/s * exp(s^2 eps^2/2)`, so
  `sum_n Lambda(n) n c(n) = (x^2/2)e^(2eps^2) - sum_rho x^(rho+1)/(rho+1) *
  exp((rho+1)^2 eps^2/2) - (tiny)`, and each zero term carries the damping
  `e^(-gamma^2 eps^2/2)`.

**Measured** (`proto_sharp.py`, Odlyzko's first 100k zeros, 9 decimals):
the sharp formula converges — relative error ~1e-5 at x=1e6 down to ~1e-7 at
x=1e10 with 1e5 zeros — but slowly and oscillating, exactly the classical
sharp-truncation behavior that motivates smoothing.

**Measured** (`proto_smooth.py`, x=1e8, target `sum Lambda(n) n c(n)` ≈ 5e15):

| zeros | precision | abs err | rel err |
|---|---|---|---|
| 100k (Odlyzko) | 3e-9 | ~934 | 1.9e-13 |
| 2k (Odlyzko) | 3e-9 | ~1237 | 2.5e-13 |
| 2k (mpmath, 25 digits) | 1e-24 | ~15 | 3.1e-15 |

Three things this establishes: (1) the smoothed formula beats the sharp one
by ~5 orders of magnitude at equal zero count; (2) with 9-digit zeros the
error sits exactly at the predicted zero-precision floor, independent of N —
truncation tail is ~1e-4, i.e. negligible; (3) swapping in 25-digit zeros
collapses the error another ~80x to the prototype's own float128 noise.
The accuracy chain behaves exactly as the theory predicts, which is the
evidence a proposal needs that a rigorous Platt-style computation of
S(x) = sum of primes would work.

**What remains for a paper** (in rough order): strip the log-weight
analytically (the T-route: smoothed li-type transforms, or quadrature over
the smoothed psi1), rigorous truncation/window error bounds replacing the
heuristic `12 eps` cutoffs, interval arithmetic end to end, a high-precision
zero database at scale (LMFDB, or computed as Platt did), and a record-scale
target x with independent combinatorial verification (primesum). None of
this is conceptually blocked; all of it is careful work.

Reproduce: `zeros1` from
https://www-users.cse.umn.edu/~odlyzko/zeta_tables/zeros1 (first 100k zeros);
high-precision zeros via mpmath `zetazero` (script header documents usage);
exact values from `../fenwick`.

## What not to do

Do not submit any variant of the current combinatorial pipeline as new. A
referee — or the first commenter — refutes it with one link, and withdrawn
claims follow you (Deléglise himself withdrew a 10²¹ prime-sum record in 2011
after a discrepancy was found; this field checks everything).
