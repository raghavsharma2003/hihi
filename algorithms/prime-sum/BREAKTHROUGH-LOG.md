# Weighted prime races — breakthrough research log

Durable context for work on branch `codex/weighted-races-breakthrough`.
Update this file after every material mathematical, computational, literature,
or manuscript finding.  Treat earlier model conversations as hypotheses; only
items marked **verified** have been checked against source or computation.

## 2026-08-16 — project reconstruction

### Baseline

- Base branch: `claude/prime-sum-algo-optimization-lkry0q`.
- Base commit: `1b00bc2eabf2b34599204800275cb69bba11d273`.
- Main manuscript: `paper/weighted-races.tex` (v4, 4,753 lines; bundled PDF
  reported as 59 pages).
- Main numerical inputs: `prototype/explore/chi4_zeros.txt` (511 ordinates)
  and `prototype/explore/chi3_zeros.txt` (537 ordinates).
- Certification script: `prototype/explore/certify_arb.py`.
- Monotonicity verifier: `paper/v3/verify_monotonicity.py`.

### Objective

First make every existing claim theorem-grade or accurately qualified.  Then
seek a genuinely new contribution, with priority given to:

1. global monotonicity of `delta_chi(m)` on `m > -1/2` for chi_3 and chi_4;
2. the critical joint regime `M = m + 1/2 ~ lambda/log q`;
3. a higher joint Edgeworth expansion if it is both correct and not already
   present in the literature;
4. weaker-than-LI transfer or an effective finite-x convergence theorem.

No result enters the paper until its hypotheses and proof have been audited
against primary sources and a reproducible computation exists where needed.

### Verified artifact-level findings

1. **Serious completeness contradiction.**  The abstract (lines 83–85 of the
   baseline manuscript) says that the completeness of the zero lists
   underlying the numerics is machine-certified.  The methods section (lines
   4588–4592) says only 510 of 511 chi_4 zeros and 536 of 537 chi_3 zeros are
   covered by the winding-number count.  The final listed zero in each file is
   certified to exist but lies above the certified-completeness height.  Thus
   the full lists are not yet certified complete.
2. This gap matters to the finite-zero product used for the density tables and
   to the ordinate-dependent leg of the explicit monotonicity thresholds.  It
   does not by itself invalidate the analytic large-M theorem (`M >= 300`) or
   the abstract limiting-variable framework.
3. `paper/v3/verify_monotonicity.py` runs successfully in the current Windows
   environment.  It reproduces the quoted closed forms, Bessel constants,
   sampled/evaluated criterion on `M in [17.317,319.96]` for q=4 and
   `[19.119,349.89]` for q=3, and the analytic `M >= 300` inequalities.  This is
   a floating-point verifier, not an interval proof; passing it does not cure
   the zero-completeness or rounding rigor gap.
4. The current environment initially lacks `python-flint`, `mpmath`, and a TeX
   executable.  Consequently `certify_arb.py`, the validated-density script,
   and a fresh local PDF build have not yet been reproduced in this branch.

### Immediate proof/certification obligations

- Extend the winding-number count to a height strictly above each final listed
  ordinate and certify counts 511 and 537, or weaken every dependent claim.
- Audit `certify_arb.py` for contour placement, argument-principle assumptions,
  endpoint avoidance, and what its balls actually certify.
- Convert the finite-range monotonicity criterion and final density quadrature
  to ball/interval arithmetic before calling the explicit thresholds
  computer-assisted theorems.
- Standardize `delta_chi` notation outside the two concrete q=3,4 examples.
- Keep central nonvanishing prominent in every family-uniform statement.
- Describe the Fiorilli–Martin relation as an analogue, not a specialization.

### Current status

The repository context and theorem dependency graph are being reconstructed.
No mathematical or manuscript fix has yet been committed on this branch.

## 2026-08-16 — full zero-list completeness repaired

### Reproduction of the v4 behavior

Using an isolated Python 3.12 environment with `python-flint==0.9.0`, the
baseline command

```text
python certify_arb.py --K 0
```

reproduced all v4 balls and sign changes, but its winding contours returned
exactly 510 zeros through `T=639.5622457728018` for chi_4 and 536 through
`T=699.4645875200972` for chi_3.  The reason was mechanical: whole-list mode
set `K_d=len(zeros)-1` so that it could place `T` between the final two stored
ordinates.

### Fix and certification result

`certify_arb.py` now handles a contour above the final stored ordinate.  In
whole-list mode it sets `K_d=len(zeros)` and places the top edge at
`gamma_K + --top-offset` (default `0.25`).  This is rigorous without knowing
`gamma_{K+1}`: `winding_number` covers every contour segment by an input ball,
requires the corresponding L-value ball to exclude zero, and subdivides or
fails otherwise.  Thus a successful run certifies the new top edge as
zero-free as part of the argument-principle calculation.

The repaired full run passed:

- chi_4: exactly 511 zeros in
  `(-1/2,3/2) x (-1/2,640.1657072529865)`, winding ball
  `[511.0000000 +/- 3e-12]`;
- chi_3: exactly 537 zeros in
  `(-1/2,3/2) x (-1/2,700.0247478100384)`, winding ball
  `[537.0000000 +/- 3e-11]`;
- all 511 and 537 disjoint `1e-20` sign-change intervals were independently
  re-certified in the same run.

Combined with the standard zero-free regions stated in the script, this proves
that every listed interval contains exactly one simple zero and that there is
no missing nontrivial zero below the two new heights.  The concrete v4
last-zero completeness objection is therefore fixed at the computational
source, not merely reworded.  The manuscript still needs its old heights and
counts updated.

## 2026-08-16 — literature and critical-regime checkpoint

### Primary-source checks

- The current HTML of the *Comparative Prime Number Theory Problem List*
  (arXiv:2407.03530, page marked updated 2026-08-11) still states Problem 12 as
  asking for the logical inclusion or relation between the Aoki–Koyama
  `p^{-1/2}` asymptotic formulation and the conventional logarithmic-density
  formulation.  The manuscript is right not to claim that Problem 12 is
  solved: its continuous `m>-1/2` family supplies a structural bridge under
  GRH+LI but does not prove a logical inclusion between the endpoint notions.
- Aoki–Koyama arXiv:2203.12266 is now at v6 (2026-06-10); its abstract still
  frames the weighted central-point result through DRH.  Sheth
  arXiv:2405.01512 obtains central-point Euler-product/ Chebyshev-bias results
  under GRH off a finite-log-measure exceptional set.
- Shimada–Koyama (Mathematics 13 (2025), 2564) treats weights `p^{-w}` with
  `0 <= w < 1/2` and sign changes, not the growing weights `p^m`, `m>0`, or the
  Rubinstein–Sarnak density-as-a-function-of-weight developed here.
- Direct primary-literature searches have not yet found an earlier
  Rubinstein–Sarnak treatment of growing `p^m` weights.  This is evidence, not
  an exhaustive novelty proof; the literature audit remains open.

### Critical scaling: corrected conceptual target

Let `M=m+1/2=lambda/log q` and scale ordinates by
`y_gamma = gamma log q/(2 pi)`.  Then each phase amplitude becomes

```text
2 a_gamma = 4 lambda / sqrt(lambda^2 + (2 pi y_gamma)^2).
```

Therefore the critical regime is controlled by the *microscopic low-zero
configuration*, not solely by the scalar lambda.  The formal variance scale is
order one (`2M log(qM/(2pi)) -> 2 lambda` away from low-zero fluctuations), so
there is no central-limit mechanism forcing a deterministic Gaussian profile
for fixed lambda.  A universal function `F(lambda)` for individual characters
is therefore not the right default conjecture.

A defensible new theorem target is instead:

> If the rescaled positive-zero counting measures of a sequence of real
> primitive characters converge, with a uniform reciprocal-square tail bound,
> then the critical weighted-race variables converge to the Bessel-product law
> determined by that limiting zero measure.  The density limit follows at
> continuity points.

This would identify the previously excluded corner and explain why any
family-averaged universal profile should be a Katz–Sarnak/random-matrix
functional, while an individual-character profile can retain low-zero data.
The exact hypotheses, proof, novelty, and whether a useful family theorem can
be made unconditional are still under investigation.
