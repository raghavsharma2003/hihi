# LinkedIn post — DRAFT (publish AFTER Zenodo DOI exists; same day as Medium is fine)

## Tagging rules (read before posting)
- DO NOT tag Prof. Martin, Prof. Koyama, or any researcher you haven't
  interacted with. Email first; tag only after a positive reply, and even then
  ask ("may I mention you in a post?").
- SAFE to tag: @Anthropic (the AI's role is public and central), your own
  school/university, @Project Euler cannot be tagged but can be named.
- Hashtags at the end, max 5.

## The post

---

A school project I wrote years ago had a bug and a dream. This month it turned
into a math preprint.

The short version:

🔹 My old C program tried to sum prime numbers cleverly. Fixed and optimized,
it turned out to reinvent a method already known since 2013. Humbling start.

🔹 So we went further: built what appears to be the first program that computes
exact prime sums from the zeros of the Riemann zeta function — the "hidden
frequencies" of the primes. Sum of every prime below a billion, computed
without touching a single prime, verified exactly.

🔹 Then we used it to ask a question nobody had asked about a 170-year-old
phenomenon (Chebyshev's bias: primes of form 4n+3 outnumber 4n+1 ~99.6% of the
time): what if bigger primes count for more? Answer: the bias dissolves —
99.6% → 79.7% → 69.5% → 64.6% as the weight grows — following a law we derived
and confirmed against every prime up to ten billion.

🔹 It turns out this connects two schools of research and computationally
answers Problem 12 of the 2024 Comparative Prime Number Theory problem list.

Full transparency: I did this with AI — Anthropic's Claude derived, coded, and
(most importantly) attacked its own work: adversarial literature reviews
demoted two of our "discoveries" to rediscoveries, and a hostile final audit
re-computed every number in the paper, catching one real error before anyone
else could. Every claim is verified twice and every limitation is stated in
the paper.

Preprint + all code and data: [ZENODO DOI LINK]

I'm a student, this field's experts will find things to correct, and that's
exactly why it's public. If you know someone in analytic number theory, I'd
be grateful for the connection.

#NumberTheory #Mathematics #RiemannHypothesis #AIforScience #OpenScience

---
END OF DRAFT. Before posting: replace the DOI placeholder, decide on tagging
per the rules above, attach ONE image (suggestion: screenshot of the δ(m)
table from the paper, or the race chart from explainer.html).
