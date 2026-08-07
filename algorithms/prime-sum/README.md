# Sum of primes ≤ n — from the school recurrence to beating the sieve

Three programs, same answer, very different speed:

| file | algorithm | time | memory |
|---|---|---|---|
| `original.c` | the school recurrence, top-down recursion | exponential-ish (and overflows past ~10⁵) | O(√n) stack |
| `sieve.c` | segmented sieve of Eratosthenes (the baseline to beat) | O(n log log n) | O(√n) |
| `lucy.c` | the same recurrence, memoized over `floor(n/i)` | **O(n^(3/4))** | O(√n) |

Build: `gcc -O2 -o lucy lucy.c -lm` (same for the others). Run: `./lucy 1000000000000`.

## Benchmarks (this container, single thread, gcc -O2)

| n | sieve.c | lucy.c | speedup |
|---|---|---|---|
| 10⁹ | 2.15 s | 0.038 s | 57× |
| 10¹⁰ | 22.2 s | 0.17 s | 128× |
| 10¹² | ~40 min (extrapolated) | 5.0 s | ~480× |

All outputs cross-checked against published values (e.g. 2 220 822 432 581 729 238 at 10¹⁰,
18 435 588 552 550 705 911 377 at 10¹² — OEIS A046731). `original.c` is already
**wrong** at n = 10⁵ (prints 4 749 363 833 instead of 454 396 537) because `R()`
accumulates into a 32-bit `int`.

## What the recurrence actually is

The identity behind `R()` — remove each composite once, charged to its *smallest*
prime factor, over primes p ≤ √n — is a Legendre-style inclusion–exclusion. It is
the same mathematics behind Legendre's 1808 prime-counting formula, Meissel's
1870 refinement, and (for prime *sums*) the method posted by **Lucy_Hedgehog on
the Project Euler problem-10 thread in 2013** — almost certainly the write-up you
found. Rediscovering it independently in school is genuinely impressive; it just
isn't unpublished.

## The one idea that changes the complexity class

`R(k, n)` only ever gets called with second argument `floor(n/something)` — and
`floor(n/i)` takes just ~2√n **distinct values**. The original recursion recomputes
those few subproblems exponentially many times. Store one table `S` indexed by the
distinct values, sweep primes 2…√n bottom-up, and each prime p updates only the
keys ≥ p²:

```
S[v] -= p * (S[v/p] - sum_of_primes_below_p)
```

That's the whole of `lucy.c`. Total work: O(n^(3/4)), asymptotically below the
sieve's O(n log log n), with O(√n) memory instead of the flat sieve's O(n) bits.
This is why the benchmark table looks the way it does: the goal "make this
algorithm beat the sieve" is achieved — but that property is exactly what was
published in 2013.

Other fixes folded in: 128-bit accumulators (the sum of primes ≤ 10¹¹ already
overflows int64), primality detected for free from the table itself
(`S[p] > S[p-1]`) instead of O(n) trial division, careful update order so every
read sees the previous prime's value.

## Where real innovation space still exists

Honest map of the frontier, so effort goes where novelty is possible:

1. **O(n^(2/3)) is the practical state of the art**, not n^(3/4): Deléglise–Rivat
   style balancing plus a Fenwick tree over the small keys. Kim Walisch's
   `primesum` implements it (records up to the sum of primes below 10²⁵) and
   `primecount` does the counting analog. Reproducing it is education;
   *improving its constants, parallel scaling, or porting it to GPU* would be a
   real, publishable engineering contribution — ideally as PRs to those projects.
2. **Generalize, don't re-derive**: the min_25 sieve (2018) computes sums of any
   reasonably nice multiplicative function in ~O(n^(2/3)). Applying that
   framework to a function nobody has computed at scale is where competitive
   programmers still produce genuinely new blog posts.
3. **Theory**: the analytic Lagarias–Odlyzko method promises O(x^(1/2+ε)) but has
   never been made practically competitive. Anything below n^(2/3) *in practice*
   is a genuine research result — a serious analytic-number-theory project, not a
   weekend of optimization.
4. **The realistic publication today**: an expository post — "I rediscovered
   Lucy_Hedgehog's algorithm in school; here is the derivation, the bugs, and the
   benchmarks" — citing Legendre/Meissel/Lucy_Hedgehog. Rediscovery + honest
   benchmarks is a legitimate and well-liked genre. Claiming novelty for the
   recurrence itself would get corrected in the first comment.
