# LinkedIn post — FINAL v3 (humanized per author edits; theorem included)

## Before posting (read once)
- DO NOT tag Prof. Martin, Prof. Koyama, or any researcher you haven't
  interacted with. Email first; tag only after a positive reply.
- SAFE to tag: @Anthropic, your school/university. Project Euler: name, don't tag.
- Hashtags at the end, max 5.
- ATTACH: the chart image `race-chart.png` (Claude prepared it) — NOT the
  paper PDF. One striking image beats a 15-page math PDF in the feed.
- The DOI link goes in the FIRST COMMENT, not the post body (LinkedIn
  reaches further without external links in the body). Post, then
  immediately comment the link text at the bottom of this file.
- LinkedIn cuts the preview after ~3 lines — the first two lines are the hook.

## The post

---

In 2017 I was 14, in 9th grade, and I genuinely believed I could beat a
2,300-year-old algorithm.

I was a kid. Nobody had told me the problem was hard, so I didn't know. I
had fallen in love with prime numbers — their randomness, their mystery —
and I spent months of school evenings filling a notebook, chasing a
pattern in them.

And I actually built something: a little algorithm that could add up all
the primes below a number without finding a single prime. My dream was to
beat the Sieve of Eratosthenes. I showed it to almost nobody. It went into
a drawer.

In my third year of college I finally tried to write it up properly.
That's when I found a 2013 post on a competitive programming forum
describing essentially the same method. Four years before my drawer.

I abandoned it.

This year, when AI models got seriously good at mathematics, I dug the
notebook back out. I handed my teenage algorithm to Claude (Anthropic's
AI) and said: let's find out what's beyond this.

We rebuilt the idea on the "hidden frequencies" of the primes — the zeros
of the Riemann zeta function. Counting primes from those frequencies is
famous. Computing prime sums exactly from them had never been done. Now it
has: the exact sum of every prime below a billion, from 2,000 zeta zeros
plus one thin, exactly-sieved window.

Then the real discovery. Chebyshev's bias is a 170-year-old curiosity:
primes of the form 4n+3 outnumber primes of the form 4n+1 about 99.6% of
the time. We asked something that appears in no paper: what if bigger
primes count for more? The bias dissolves — 99.6% → 79.8% → 69.5% → 64.6%
as the weight grows — following a law we derived, then checked against
every prime up to ten billion. Those numbers bear directly on an open
problem posed in 2024 (Problem 12 of the Comparative Prime Number Theory
problem list): the first computational evidence connecting the two
definitions it asks about. And in the last push it became a theorem —
under the field's standard hypotheses, the two competing definitions of
the bias are the two ends of one continuous curve, with an explicit bound
on how fast the bias becomes total. New for prime races, built on known
methods. The problem stays open; this is a bridge, not the answer.

Full transparency, because it's the best part: the AI didn't just help. It
derived, coded, and then attacked its own work. Twice its adversarial
literature reviews proved our "discoveries" already existed — we demoted
them and cited the real discoverers. A final hostile audit recomputed
every number and caught a real error before anyone outside saw it.
Everything that survived is verified two independent ways, and every
limitation is stated in the paper.

The preprint, all code, and all data are public — link in the first
comment.

I'm a learner, not an expert. People who know this field will find things
to correct, and that's exactly why it's public. If you know someone in
analytic number theory, I'd be grateful for an introduction.

To the 14-year-old with the drawer: it was worth keeping.

#NumberTheory #Mathematics #RiemannHypothesis #AIforScience #OpenScience

---

## First comment (post this immediately after publishing)

Preprint, all code, and all data (open access):
https://doi.org/10.5281/zenodo.21947101
GitHub: https://github.com/raghavs1729/weighted-prime-races
