# Session log — full state (anti-compaction record, updated 2026-08-15)

## Repo map (all under algorithms/prime-sum/)
- original.c, lucy.c (O(n^3/4)), fenwick.c (~O(n^2/3)), sieve.c — combinatorial programs, benchmarked in README.md
- prototype/analytic_sum.py — S(x)=Σp analytic from 2000 zeta zeros; EXACT to x=1e9 (24,739,512,092,254,535, resid +6e-3)
- prototype/proto_sharp.py, proto_smooth.py — validation ladder
- prototype/explore/pi_lifree.py — π(x) exact 1e6..1e8 (elementary-transforms variant; FKBJ/Büthe already li-free — cited, not claimed novel)
- prototype/explore/power_sums.py — Σp², Σp³ exact to 1e7 (40-digit Newton-refined zeros needed at m=3)
- prototype/explore/mertens.py — Σ1/p to 17 digits (1e6, 1e7)
- prototype/explore/ap_sums.py + chi4_zeros.txt — 511 self-computed L(s,χ₄) zeros; AP sums mod 4 exact 1e5..1e7
- prototype/explore/race_scan.c — exact weighted races mod 4 to 1e10 (results in race_1e10_results.txt)
- prototype/explore/race_density.py — δ(m) for m=0..3 (anchor δ(0)=0.99593 = classical RS ✓)
- prototype/explore/race_curve.py — FULL δ(m) curve; confirms both theoretical ends (numbers below)
- paper/analytic-prime-sum.tex — submission-format manuscript (claims calibrated by paper/prior-art-review.md)
- paper/weighted-races-note.md — race discovery write-up (needs phase-diagram update — in progress)
- explainer.html — visual explainer, published artifact f96eb43f-ea4e-46c9-b1a0-204acdb31202

## Zeros data (scratchpad — regenerate if lost)
- /tmp/claude-0/-home-user-hihi/482aec6c-4f00-58b8-b5df-df7d9a8314a0/scratchpad/hpzeros2000.txt: 2000 zeta zeros, 25 digits (mpmath zetazero, dps 30)
- chi4_zeros.txt (in repo): 511 L(s,χ₄) zeros

## Key verified numbers
- S(1e9)=24739512092254535; π(1e8)=5761455; Σp²(1e7)=21113978675102768574; Σp³(1e7)=157468033886449157634628898; Σ1/p(1e7)=3.0414493812797104945; S(1e7;4,1)=1601423376628; S(1e7;4,3)=1601901617726
- Races (kernel a_γ(m)=(2m+1)/√((m+½)²+γ²), bias normalized to 1):
  δ(0)=0.99593 ✓classical | δ(1)=0.79731 | δ(2)=0.69468 | δ(3)=0.64577 (MC ±3e-4)
  Exact 1e10 log-measures: 0.79380 / 0.69275 / 0.64900 — agree ~3e-3
  First 1-side lead: m=0 at 26,861 (Leech ✓); m≥1 at p=5. Lead changes to 1e10: 3082/125624/159942/199540
- PHASE DIAGRAM (new, this session):
  END m→∞: Var(m) ~ 2(m+½)log(2(m+½)/π) ⇒ δ(m)−½ ~ 1/√(2π·Var): CONFIRMED 3-way at m=100: MC 0.51370 / Gauss 0.51379 / law 0.51380
  END m→−½⁺: δ→1 super-fast (δ(−0.3)=1.000000 at 2e6 samples)
  END m<−½ (frozen regime): D_m(x) converges to constant −Σχ₄(p)p^m (= −P_χ₄(−m) via Möbius over log L); sign fixed forever — agents computing constants + sieve verification now

## Claims calibration (from prior-art sweep)
Novel-as-computation: analytic prime sums any weight + AP exact recovery + δ(m) family. NOT novel: underlying formulas (classical), li-free π(x) (FKBJ/Büthe). σ-device = Fubini-equiv of log ζ (operational framing only). Must-cite: FKBJ, Büthe×3, Galway, Riesel–Göhl, Bays–Hudson, Devin (analytic L Chebyshev bias), Zhang race, Ford–Sneed/Meng.

## In flight (parallel agents launched 2026-08-15)
A: frozen-regime constants (m=−1,−0.75) via log L + sieve verify + last flip
B: critical case m=−½ derivation + measurement
C: modulus universality: χ₃ zeros + mod-3 races + law constant test
D: literature check on dissolution law + phase diagram
Then: update weighted-races-note.md w/ phase diagram, explainer race section, push all.

## PR
raghavsharma2003/hihi #2, branch claude/prime-sum-algo-optimization-lkry0q, base claude/voice-notes-app-calendar-f0d541. PR monitoring/check-ins STOPPED at user request — do not re-arm.
