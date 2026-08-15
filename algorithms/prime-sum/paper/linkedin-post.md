# LinkedIn post — FINAL (red-team cleared; all corrections applied)

## Tagging rules (unchanged — read before posting)
- DO NOT tag Prof. Martin, Prof. Koyama, or any researcher you haven't
  interacted with. Email first; tag only after a positive reply.
- SAFE to tag: @Anthropic, your school/university. Project Euler: name, don't tag.
- Hashtags at the end, max 5. Attach ONE image (the δ(m) table or race chart).
- LinkedIn cuts the preview after ~3 lines — the first two lines are the hook.

## The post

---

In 2017 I was 14, in 9th grade, and I genuinely believed I could beat a
2,300-year-old algorithm.

I had fallen in love with prime numbers — their randomness, their mystery.
I spent months of evenings chasing a pattern in them, and I actually built
something: a little algorithm that could add up all the primes below a
number *without finding a single prime*. My dream was to beat the Sieve of
Eratosthenes. I never showed it to anyone. It went into a drawer.

In my third year of college, I finally decided to write it up properly.
That's when I found out someone had published essentially the same method
on a competitive programming forum… in 2013. Four years before my drawer.

I abandoned it. Honestly, it hurt.

This year, when AI models got seriously good at mathematics, my undying
love for primes won. I handed my teenage algorithm to Claude (Anthropic's
AI) and said: let's find out what's actually beyond this.

What followed was months compressed into days. We rebuilt the idea on top
of the "hidden frequencies" of the primes — the zeros of the Riemann zeta
function — and found that while *counting* primes from those frequencies
was famous, nobody had ever used them to compute prime *sums* exactly. So
we built the first program that does: the exact sum of every prime below a
billion, from 2,000 zeta zeros plus one thin, exactly-sieved window.

Then came the real discovery. There's a 170-year-old curiosity called
Chebyshev's bias: primes of the form 4n+3 outnumber primes of form 4n+1
about 99.6% of the time. We asked a question that appears in no paper:
what if bigger primes count for more? The famous bias dissolves — 99.6% →
79.8% → 69.5% → 64.6% as the weight grows — following a law we derived and
then confirmed against every single prime up to ten billion. It turned out our
numbers bear directly on an open problem posed by researchers in 2024
(Problem 12 of the Comparative Prime Number Theory problem list) — the
first computational evidence connecting the two definitions it asks about.

Full transparency, because it's the most interesting part: the AI didn't
just help — it derived, coded, and then *attacked its own work*. Twice its
adversarial literature reviews proved our "discoveries" already existed,
and we demoted them and cited the real discoverers. A final hostile audit
re-computed every number in the paper and caught one real error before
anyone outside saw it. Every claim that survived is verified two
independent ways, and every limitation is stated in the paper.

The preprint, all code, and all data are public:
https://doi.org/10.5281/zenodo.21947102

I'm a student. The experts of this field will find things to correct —
that's exactly why it's public. If you know someone in analytic number
theory, I'd be grateful for an introduction.

To the 14-year-old with the drawer: it was worth keeping.

#NumberTheory #Mathematics #RiemannHypothesis #AIforScience #OpenScience
