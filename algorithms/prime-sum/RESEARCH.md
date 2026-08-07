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

## What not to do

Do not submit any variant of the current combinatorial pipeline as new. A
referee — or the first commenter — refutes it with one link, and withdrawn
claims follow you (Deléglise himself withdrew a 10²¹ prime-sum record in 2011
after a discrepancy was found; this field checks everything).
