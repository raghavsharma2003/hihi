# Focused flagship project

Last updated: 2026-08-17

## Frozen reference

The 66-page manuscript remains preserved on branch
`codex/weighted-races-breakthrough` at commit
`342ed8cd24cc110a7a5b411c425697b6001aff6c`.  This project does not expand
that manuscript.  Verification fixes and exploratory notes live on
`codex/weighted-races-focused-flagship` until a separate focused theorem is
selected.

## Objective

Produce a self-contained paper of approximately 20--30 pages built around one
headline theorem.  Supporting lemmas, computations, and formalization are
included only when they are necessary to state, prove, or independently check
that theorem.

The target is not a numerical score.  The target is a result for which a
specialist can answer all three questions positively:

1. Is the theorem genuinely new and mathematically consequential?
2. Is the proof short enough, modular enough, and explicit enough to audit?
3. Does the theorem resolve a clearly stated obstruction rather than merely
   add another example or higher-order term?

## Non-negotiable proof standard

- Every imported result is checked against a primary source and quoted with
  its exact hypotheses and order of limits.
- Every asymptotic parameter and hidden constant has a dependency ledger.
- Conditional assumptions are theorem parameters, never project axioms.
- Numerical evidence is separated from proof.  A computational theorem needs
  a fail-closed certificate and an independent checker.
- Lean coverage is reported by exact declaration/theorem coverage.  No claim
  of full formal verification is permitted until the complete arithmetic and
  analytic bridge compiles.
- A hostile proof audit must pass before a result is promoted from a research
  note to the focused manuscript.

## Candidate directions

### A. Quantitative simultaneous hyperelliptic critical law

Goal: replace the noncanonical iterated limit by a concrete regime
`Q >= Q_0(g)` and prove convergence of the weighted degree-race density to a
functional of the symplectic hard-edge process.

Preferred strengthened formulation (under audit): make the whole quenched
limiting race law a random element of `P_2(R)` and prove its convergence in
the Wasserstein topology.  The sign density is then a continuous-mapping
corollary at the almost-surely atomless limit.  This formulation is both
stronger and analytically cleaner because the coefficient coupling gives a
direct `W_2` estimate and eliminates the global bounded-density Lipschitz
step.  Nondegeneracy should be certified through the random conditional
variance, not asserted from simulations.

Value: high if the genus dependence is explicit and substantially sharper
than a formal diagonalization.  Current status: active primary-source audit.

### B. Fixed-field hyperelliptic critical law

Goal: prove the critical race law with fixed finite field and genus tending to
infinity, possibly by proving convergence of the race functional directly
instead of the full microscopic point process.

Value: very high.  Current obstruction: known fixed-field low-zero density
results have restricted Fourier support, generic LI is unavailable, and full
hard-edge convergence would imply central-nonvanishing information beyond the
current literature.  This remains exploratory, not a claimed theorem.

### C. Joint finite-x/growing-weight number-field theorem

Goal: prove an actual-race convergence theorem for a nontrivial range
`m=m(x)`, going materially beyond the fixed-weight ELI adaptation.

Value: high if the range reaches a genuine short-interval transition.  Current
status: active audit of explicit-formula uniformity, small divisors, bounded
density, and short-interval prime estimates.

### D. All-order joint conductor--weight expansion

Goal: replace the existing third-order expansion by an explicit expansion to
every fixed order, with one remainder uniform in the conductor and growing
weight.

Value: technically clean and highly auditable.  Current assessment: the
theorem is valid, but Fiorilli--Martin already established the all-order
Bessel/cumulant mechanism in a closely related modulus-aspect race.  The new
joint uniformity is useful supporting mathematics, not a sufficient flagship
by itself.

## Current decision matrix

| Direction | Proof route | Main unresolved issue | Originality ceiling | Near-term role |
|---|---|---|---:|---|
| Canonical simultaneous hyperelliptic quenched law | Complete candidate proof; hostile proof, novelty, heat, and P2 audits passed internally after repairs | external expert checks | high | selected focused theorem |
| Fixed-field hyperelliptic law | blocked | microscopic hard-edge convergence and generic LI | very high | long-term open target |
| Moving-weight number-field CLT | credible architecture | uniform explicit formula and diagonal-aware high-zero lemma under all-order QLI | medium-high | do not promote yet |
| Mellin-kernel universality | credible architecture | same two analytic lemmas and strong QLI | high | future project |
| All-order joint expansion | complete candidate proof | novelty, not correctness | medium | safe supporting theorem |
| Third-order joint extraction | already proved in the frozen paper | limited theorem size | medium-low | fallback short paper |

## Selection rule

The selected theorem must have a complete proof route from current primary
literature plus new arguments.  If no candidate meets that standard, the
correct outcome is a rigorous no-go/roadmap and no new paper claim.  We do not
weaken the standard merely to produce a manuscript quickly.

## Existing supporting work (not the flagship)

- `paper/research-notes/effective-finite-x-convergence.md`: sound fixed-weight
  theorem under GRH, central nonvanishing, and effective LI; useful but mainly
  a Bailleul--Hayani--Untrau kernel-shift adaptation.
- `paper/research-notes/function-field-critical-family.md`: iterated
  large-field/large-genus realization; potentially a supporting theorem, but
  not by itself the desired single breakthrough.
- `prototype/independent_verifier/` and
  `formal/Formal/DensityPostprocessing.lean`: exact downstream verification
  layers for the frozen manuscript, not evidence for a new headline theorem.

## Decision log

- 2026-08-17: froze the broad manuscript; rejected adding both new theorem
  notes to it.
- 2026-08-17: adopted a one-theorem, 20--30 page companion-paper constraint.
- 2026-08-17: opened three parallel searches (A--C above).
- 2026-08-17: fixed-field audit found that the fixed-critical law crosses the
  unresolved microscopic Katz--Sarnak and fixed-field LI barriers; retained it
  as a long-term target, not the near-term paper.
- 2026-08-17: moving-weight number-field CLT survived a feasibility audit but
  still needs uniform explicit-formula and diagonal-aware high-zero lemmas and
  assumes all-order quantitative LI; it is not yet manuscript-ready.
- 2026-08-17: simultaneous function-field search produced a canonical
  one-parameter pencil with an explicit square-field growth rule; hostile
  audit is in progress.
- 2026-08-17: a safe fallback was identified: extract the existing joint
  weight--conductor dissolution expansion into a 24--28 page paper.  This is
  highly auditable but has a lower originality ceiling.
- 2026-08-17: opened two upgrade searches: arbitrary-order joint expansion and
  general shrinking-Mellin-kernel universality.
- 2026-08-17: the fixed-field search was closed as a near-term route: current
  restricted-support density theorems do not determine the fixed-critical
  Bessel statistic, and generic fixed-field LI is also unavailable.
- 2026-08-17: the moving-weight CLT and Mellin-kernel searches produced
  plausible conditional theorems but not complete proofs.  Both require a
  new uniform explicit-formula ledger and a diagonal-aware high-zero lemma;
  neither is eligible for the focused manuscript yet.
- 2026-08-17: completed the all-order joint expansion.  It is mathematically
  clean but, because the all-order mechanism has close precedent, retained it
  only as a supporting result or fallback.
- 2026-08-17: made the canonical simultaneous hyperelliptic law the provisional
  leader, conditional on two separate hostile audits: one of the proof and one
  of novelty/priority.  No manuscript will be opened until both audits close.
- 2026-08-17: the hostile proof audit closed without a fatal mathematical
  blocker after repairs to the normalized polynomial, LI deduction, half-Tate
  twist, level-cover Betti bound, heat metric, and marked-series lemma.  This
  is an internal audit, not external validation.  The independent
  novelty/priority audit remains open.
- 2026-08-17: the independent source/novelty audit found no prior statement of
  the full `P_2(R)`-valued quenched law or its actual-race density corollary.
  It also caught and repaired `A(U_g)=2g` (not `2g-1`); the already stated
  threshold `Q>16g^2` remains valid.  The result is selected as the focused
  theorem, subject to dedicated heat-kernel and point-process audits now in
  progress.  The honest target is a strong specialist bridge theorem, not a
  claimed solution of the fixed-field microscopic problem.
- 2026-08-17: the dedicated heat audit fixed the `K_{2s}(e)`/Haar-probability
  conventions and found no hidden rank loss.  The point-process audit found a
  real closed-hard-edge gap, repaired it by working on `[0,infinity)`, and
  supplied the missing Borel/`P_2` lemma.  It also proved scalar-density
  nonconstancy separately by DPP crowding and a uniform Bessel concentration
  bound.  These internal gates now pass; external specialist review remains.
- 2026-08-17: drafted the complete focused manuscript under `flagship/paper/`
  and ran an end-to-end hostile integration audit plus a separate primary-source
  audit.  The source audit caught an arithmetic/geometric Frobenius reversal in
  the half-Tate wording; it is now corrected exactly.  The manuscript also
  replaced the source-sensitive residual-cover bound by the direct identity
  `dim H_c^1=(2g-1) dim(rho)` from GOS and Deligne, defined the genuine
  orbit-Haar endpoint law on every parameter, expanded the Soshnikov, Brownian,
  quotient-metric, and Bessel bridges, and corrected the exceptional-set BL
  factor from one to two.
- 2026-08-17: Tectonic 0.17.0 completed an automatic three-pass TeX/BibTeX
  auxiliary build with exit code zero, and the 10-theorem focused Lean scaling
  core rebuilt with a clean axiom report.  This is not a rendered-PDF check and
  not an end-to-end formalization of the headline theorem.  External arithmetic
  geometry and DPP review remain mandatory before submission.
- 2026-08-17: a fresh post-repair audit rederived the current manuscript rather
  than inheriting the earlier verdict.  It found no fatal or high-priority
  mathematical error and requested no further TeX correction.  Status is
  `CONDITIONAL MATHEMATICAL PASS; NOT YET RELEASE-CLEARED`: exact source-page
  inspection, rendered-PDF QA, current novelty search, and independent human
  arithmetic-geometry/DPP review are still required.
