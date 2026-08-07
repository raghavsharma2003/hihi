# Sum of primes ≤ n — from the school recurrence to O(n^(2/3))

Four programs, same answer, three complexity classes apart:

| file | algorithm | time | memory |
|---|---|---|---|
| `original.c` | the school recurrence, top-down recursion | exponential-ish (and overflows past ~10⁵) | O(√n) stack |
| `sieve.c` | segmented sieve of Eratosthenes (the baseline to beat) | O(n log log n) | O(√n) |
| `lucy.c` | the same recurrence, memoized over `floor(n/i)` | O(n^(3/4)) | O(√n) |
| `fenwick.c` | hybrid: Fenwick-tree sieve on [1, B≈n^(2/3)] + Lucy table for the n/B large keys | **~O(n^(2/3))** | O(n^(2/3)) |

Build: `gcc -O2 -o fenwick fenwick.c -lm` (same pattern for the others).
Run: `./fenwick 10000000000000` (optional second argument overrides the sieve bound B).

## Benchmarks (4-core container, single thread, gcc -O2)

| n | sieve.c | lucy.c | fenwick.c |
|---|---|---|---|
| 10⁹ | 2.15 s | 0.038 s | — |
| 10¹⁰ | 22.2 s | 0.17 s | — |
| 10¹¹ | ~4 min* | 0.90 s | 0.63 s |
| 10¹² | ~40 min* | 4.8 s | 2.7 s |
| 10¹³ | ~7 h* | 25.1 s | 14.6 s |

\* extrapolated from the 10¹⁰ measurement.

Every output cross-checked: all four programs agree on n up to 10¹⁰, and the
large values match OEIS A046731 (e.g. 18 435 588 552 550 705 911 377 at 10¹²,
1 699 246 443 377 779 418 889 494 at 10¹³). `original.c` is already **wrong** at
n = 10⁵ (prints 4 749 363 833 instead of 454 396 537) because `R()` accumulates
into a 32-bit `int`.

## What the recurrence actually is

The identity behind `R()` — remove each composite once, charged to its *smallest*
prime factor, over primes p ≤ √n — is a Legendre-style inclusion–exclusion, the
same mathematics behind Legendre's 1808 prime-counting formula and Meissel's 1870
refinement. For prime *sums* specifically it is the method posted by
**Lucy_Hedgehog on the Project Euler problem-10 thread in 2013** — almost
certainly the write-up you found. Rediscovering it independently in school is
genuinely impressive; it just isn't unpublished.

## The ideas, in order of appearance

**lucy.c (n^(3/4)):** `R(k, n)` only ever gets called with second argument
`floor(n/something)`, and `floor(n/i)` takes just ~2√n distinct values. The
original recursion recomputes those few subproblems exponentially many times.
Store one table `S` indexed by the distinct values, sweep primes 2…√n bottom-up,
and each prime p updates only the keys ≥ p²:

```
S[v] -= p * (S[v/p] - sum_of_primes_below_p)
```

Also folded in: 128-bit accumulators (the sum of primes ≤ 10¹¹ already overflows
int64), primality read off the table itself (`S[p] > S[p-1]`), and a careful
update order so every read sees the previous prime's state.

**fenwick.c (~n^(2/3)):** lucy.c's cost is dominated by re-updating the ~√n
small keys for every prime. Instead, sieve [1, B] with B ≈ n^(2/3)/8 directly,
maintaining a Fenwick tree over surviving values so `sum of survivors ≤ x` is a
query, not a stored table. Only the n/B large keys stay as an explicit Lucy
table. Each composite ≤ B is removed from the tree exactly once (enumerated by
smallest prime factor from a linear sieve), and the p = 2 round is done in
closed form so the tree starts odd-only — halving tree-update work. Balancing
the two halves gives the ~n^(2/3) total.

## Prior art — the honest map

Everything above is published:

- **n^(3/4), O(√n) memory:** Lucy_Hedgehog, Project Euler forum, 2013.
- **Lucy + Fenwick hybrid (~n^(2/3)):** described in detail by gbroxey,
  ["Lucy's Algorithm + Fenwick Trees"](https://gbroxey.github.io/blog/2023/04/09/lucy-fenwick.html), 2023 —
  including the sharper O(x^(2/3)/(log x)^(2/3))-type balancing.
- **n^(2/3) at record scale:** [Kim Walisch's primesum](https://github.com/kimwalisch/primesum)
  (Deléglise–Rivat adapted to sums, multithreaded, 128/256-bit), used for the
  published record values; its sibling [primecount](https://github.com/kimwalisch/primecount)
  holds the π(x) records.
- **Generalizations:** the min_25 sieve (2018) computes sums of many
  multiplicative functions in ~n^(2/3); Deléglise–Rivat (1996) is the
  counting ancestor.
- **Theory below n^(2/3):** the analytic Lagarias–Odlyzko method promises
  O(x^(1/2+ε)) but has never been made practically competitive.

## So where is novelty actually possible?

1. **Constants and hardware, not asymptotics.** Making the n^(2/3) class
   faster in practice — SIMD Fenwick layouts, cache-blocked trees, GPU ports,
   better parallel scaling — is real, welcome work. The natural venue is PRs to
   `primesum`/`primecount` plus a write-up with measurements.
2. **New targets for the same machinery.** Sums of primes in residue classes,
   prime k-th-power sums, or another multiplicative function nobody has computed
   at scale via min_25 — pick a function with an application and the write-up is
   genuinely new.
3. **Record computations.** With verified code and enough cores, extending a
   published table (or independently verifying one) is a citable contribution.
4. **Theory.** Anything below n^(2/3) *in practice* would be a real research
   result — an analytic-number-theory project, not a weekend of optimization.
5. **The realistic publication today:** an expository post — "I rediscovered
   Lucy_Hedgehog's algorithm in school: the derivation, the bugs, the
   benchmarks" — citing Legendre/Meissel/Lucy_Hedgehog/gbroxey. Honest
   rediscovery with good measurements is a well-liked genre. Claiming the
   recurrence or the Fenwick hybrid as new would be refuted by a single link.
