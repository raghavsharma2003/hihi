# Medium article — FINAL (links live; ready to publish)

Suggested title: **I Started With a School Algorithm. I Ended Up Answering an Open Problem About Prime Numbers.**
Subtitle: How a wrong C program, an AI collaborator, and the zeros of the Riemann zeta function led to the first "weighted density" computations for Chebyshev's famous prime race.

---

In school I wrote a small C program to add up prime numbers without listing them
all. It had a clever recursive idea, a 32-bit overflow bug, and no idea what it
was about to start.

This month, that idea grew into something I never expected: a computational
answer to a formally posed open problem in number theory — Problem 12 of the
2024 Comparative Prime Number Theory problem list — with every number verified
twice, a preprint, and open-source code. This is the story, including the parts
where we were wrong.

## Part 1: My algorithm already existed

When I dusted off my school program this year, the first discovery was
humbling: fixed and optimized, my recursion turned out to be a method posted on
the Project Euler forums in 2013, known to competitive programmers as
Lucy_Hedgehog's algorithm. The mathematics behind it goes back to Legendre in
1808.

That could have been the end. Instead it became the entry fee. Working with an
AI collaborator (Anthropic's Claude — more on that honestly below), I asked:
what would it take to compute prime sums in a way *nobody* has?

## Part 2: Hearing the primes instead of counting them

Since Riemann in 1859, mathematicians have known that the primes' apparent
randomness is controlled by a fixed set of hidden frequencies — the zeros of
the Riemann zeta function. Know the frequencies, and you can reconstruct facts
about primes without touching a single one.

Prime *counting* had been done this way, famously, up to 10^24. Prime *sums*
never had — by anyone, as far as a deliberately hostile literature search could
find. We built it: a program that computes the exact sum of every prime below a
billion — 24,739,512,092,254,535 — from just 2,000 zeta zeros plus a thin
verification window. Then the same machinery computed sums of squares of
primes, cubes, reciprocals, and — the key step — sums of primes split into
families, using zeros of Dirichlet L-functions the program computed for
itself.

Getting there was not smooth. At one point the computation was off by exactly
the kind of oscillating error a missing mathematical term would produce. We
spent hours hunting the "missing term." It was floating-point rounding,
conspiring coherently at precisely the frequencies of the zeta zeros — the
most misleading numerical artifact I hope to ever meet. (It's documented in
the paper; anyone who builds this after us would have hit it too.)

## Part 3: The race

In 1853, Chebyshev noticed that primes leaving remainder 3 when divided by 4
seem to outnumber those leaving remainder 1. It's now a classic result
(Rubinstein–Sarnak, 1994) that under standard conjectures, "team 3" leads
about **99.59%** of the time — and doesn't lose the lead even once until
x = 26,861.

We asked a question that, as far as we and our literature search can tell,
nobody had asked: **what if bigger primes count for more?** Let each prime
score p points instead of 1. Or p². Or p³. Does the famous bias survive?

It dissolves — and we computed exactly how fast:

| weight per prime | how often team 3 leads |
|---|---|
| 1 (classical) | 99.59% |
| p | 79.73% |
| p² | 69.47% |
| p³ | 64.58% |
| p^100 | 51.37% |

The first number is the known classical value — our calibration. The rest are,
to our knowledge, the first Rubinstein–Sarnak densities ever computed for a
weighted prime race. We verified them against reality by exactly racing every
prime up to ten billion (the measured values agree to about 3 parts in 1,000),
and we derived a closed-form law for how the bias decays to a coin flip as the
weight grows — confirmed in two different moduli.

There's a full phase diagram: give primes slightly *negative* weight and the
bias becomes total (team 3 leads forever, with a final margin computable to 30
digits); at exactly weight p^(-1/2) sits a critical point where the race grows
at the slowest unbounded rate in analysis, ½·log log x — a regime where our
role was confirming beautiful recent theorems of Aoki–Koyama and Sheth, not
discovering them.

## Part 4: What's actually new, and what isn't

Research lives or dies on this distinction, so here it is plainly.

**Not new:** the underlying explicit formulas (classical); the critical-point
theorem (Aoki–Koyama 2023, Sheth 2025); the frozen-race constants (they're
differences of Meissel–Mertens constants, computed to 100 digits in 2010); the
existence machinery for limiting distributions (Akbary–Ng–Shahabi, Devin).

**New, to the best of a determined search:** the analytic prime-sum
computations themselves; the weighted-race densities δ(m); the entire
growing-weight regime; and the dissolution law. Together they connect the
"weighted" school of Chebyshev's bias with the classical "density" school —
which is precisely what Problem 12 of the comparative prime number theory
problem list (Hamieh–Kadiri–Martin–Ng, 2024) asks for.

## Part 5: About the AI

I want to be completely transparent: this work was done *with* an AI, deeply.
Claude derived formulas, wrote code, ran literature searches, and — this
mattered most — attacked its own results: parallel verification agents
re-computed every claim from scratch, an adversarial literature review tried
to prove our "discoveries" already existed (twice, it succeeded — we demoted
those claims and cited the real discoverers), and a final hostile audit
re-derived every number in the paper before anyone outside saw it. One audit
caught a real error in a stated constant; it was fixed before, not after.

I believe this is what honest AI-assisted mathematics looks like: the AI's
role fully disclosed, every claim verified independently of the tool that
produced it, and the human responsible for what gets claimed. The paper says
all of this on page one.

## What happens next

The preprint, code, and data are public: https://doi.org/10.5281/zenodo.21947102 and
https://github.com/raghavs1729/weighted-prime-races. I've written to the authors of the problem list. The
results are conditional on the standard conjectures of this field (GRH and
linear independence — the same assumptions the classical 99.59% rests on),
and turning the demonstrated error bounds into formally proven ones is the
natural next step, ideally with a professional collaborator.

If you work in analytic number theory and see something wrong — or something
worth pushing further — my inbox is open. That's what the preprint is for.

*The primes were never random. We just needed to learn to listen.*

---
END — ready to publish. Read once aloud first; publish after the email to Prof. Martin is sent.
