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

## Phase-diagram program COMPLETE (all 4 agents verified 2026-08-15)
A frozen: D_-1(inf)=0.334981325299993... = M(4,3)-M(4,1) (matches Languasco-Zaccagnini/OEIS A368645/A086239 to 1e-10); D_-0.75(inf)=0.546437908...; ZERO flips ever on [3,1e9]; min 2/15 at p=5; convergence exponents fit GRH (-0.519 vs -0.5).
B critical m=-1/2: D = (1/2)loglog x + C*, C*=-0.07153 (M, log2, K3, log L(1/2,chi4)); fluctuation DECAYS ~ sqrt(0.156033)/log x; zero-free-param test at 1e10: pred 1.4968+-0.0172 vs measured 1.50775 (+0.63sigma); never flips; indep verified at 1e7 (1.31670 exact match).
C mod-3 universality: 537 chi3 zeros (gamma1=8.039737, RvM 535.9 ✓); anchor delta3(0)=0.99904 vs classical 0.9990 ✓; delta3(1)=0.83679 (indep re-MC 0.83696 ✓), delta3(2)=0.72361, delta3(3)=0.66695, delta3(60)=0.51917; LAW GENERALIZES: Var_q(m) ~ 2(m+1/2)log(q(m+1/2)/2pi) (agent corrected my drafted constant; 0.26% at m=60); ordering delta3>delta4 all m ✓; weighted flips p=13/p=7 hand-verified; caveat: m=2 finite-x gap 0.023 unresolved.
D literature: CRITICAL RECALIBRATION. m<=0 half is occupied: Aoki-Koyama 2023 proved the m=-1/2 (1/2)loglog x theorem (DRH), Sheth 2024 (GRH); Shimada-Koyama Aug 2025 has the w=1/2 threshold; Humphries 2013 has the full template for Liouville; frozen constants = Meissel-Mertens AP constants (L-Z 2010, OEIS). OURS: first RS densities for any weighted race; m>0 regime untouched; dissolution law novel (Fiorilli-Martin paradigm in weight aspect); ANSWERS PROBLEM 12 of arXiv:2407.03530 (Koyama). URGENT: Koyama group actively publishing on this seam (Aug 2025, Jul 2026) - write up fast. All framing recalibrated in paper/weighted-races-note.md.

## PR
raghavsharma2003/hihi #2, branch claude/prime-sum-algo-optimization-lkry0q, base claude/voice-notes-app-calendar-f0d541. PR monitoring/check-ins STOPPED at user request — do not re-arm.

## FINAL AUDIT (2026-08-15, pre-outreach) — PASSED
Numbers audit: 38/39 claims reproduced exactly (both 1e10 sieves regenerated; all density cells to last digit; kernel derivation verified analytically incl. theta-form->unlogged 1/log x cancellation; off-by-one kernel alternative excluded via m=0 anchor). ONE error found+fixed: min margin over m in {-1,-3/4,-1/2} is 1/sqrt3-1/sqrt5=0.13014 (m=-1/2 at x=5), not 2/15 (that's m=-1 only). Evidence gap closed: fresh 1e10 frozen-race scan (race_frozen_scan.c, archived) confirms zero flips for m=-1,-3/4 to 1e10.
Citations audit: Problem 12 VERIFIED (number, statement, Koyama attribution, quote obtained); fixes applied: problem-list title, authors-not-eds, Sheth MPCPS 179 (2025) 331-349, OEIS A086239=difference/A368645+A368646=constants. Martin: gerg@math.ubc.ca, Professor Emeritus, UBC.
Outreach package READY: paper/weighted-races.tex (audited), paper/outreach-email.md (to Greg Martin), bundle in scratchpad prime-sum-research.tar.gz.
