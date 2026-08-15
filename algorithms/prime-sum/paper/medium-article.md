# Medium article — FINAL (red-team cleared; all corrections applied)

Suggested title: **At 14 I Tried to Beat a 2,300-Year-Old Algorithm. This Year, With an AI, I Watched a 170-Year-Old Prime Mystery Dissolve.**
Subtitle: A nine-year story about a drawer, a heartbreak, the zeros of the Riemann zeta function, and Chebyshev's dissolving bias.

---

In 2017 I was fourteen, in 9th grade, and prime numbers had gotten into my
head the way songs do. Their randomness looked like a lie to me — surely
something so important couldn't just be *noise*. I spent months of evenings
being gloriously naive about it, filling pages, writing C programs, chasing a
pattern.

And I actually built something: an algorithm that added up all the primes
below a number without ever finding a single prime. My dream was concrete
and absurd — beat the Sieve of Eratosthenes, the 2,300-year-old champion.
I never told anyone. The algorithm went into a drawer, and I went back to
being a teenager.

## Part 1: The heartbreak

In my third year of college I finally decided to write it up properly. A few
searches in, I found a 2013 post on the Project Euler forums by a user called
Lucy_Hedgehog. It was my algorithm — cleaner, earlier, already beloved by
competitive programmers. The mathematics underneath it, I learned, went back
to Legendre in 1808.

Four years before my drawer, and two centuries before that. I abandoned the
whole thing. Honestly, it hurt in a way I didn't have words for at the time:
the discovery was real, but it wasn't *mine*.

This year, when AI models became seriously capable at mathematics, the old
love won. I handed my teenage algorithm to Claude (Anthropic's AI — the
honest details of that collaboration are below) and asked the only question
left: what's *beyond* this? What would it take to compute prime sums in a
way nobody ever has?

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
| p | 79.76% |
| p² | 69.45% |
| p³ | 64.59% |
| p^100 | 51.38% |

The first number is the known classical value — our calibration. The rest are,
to our knowledge, the first Rubinstein–Sarnak densities ever computed for a
weighted race between prime families. We verified them against reality by exactly racing every
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
the two definitions whose relationship Problem 12 of the comparative prime
number theory problem list (Hamieh–Kadiri–Martin–Ng, 2024) asks about. Our
contribution is computational evidence; the logical relation the problem
demands remains for the theorists.

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
