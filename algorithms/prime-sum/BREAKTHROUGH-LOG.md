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

## 2026-08-16 — general-character race-transfer seam

The general interpolation theorem defines
`R_{m,chi}=-sum_{p<=x} chi(p)p^m log p` and proves under LI(chi) that its
logarithmic density equals `P(X_{m,chi}>0)` for every real primitive chi.
The fixed-character dissolution scope paragraph states this correctly.  The
later joint-uniformity remarks had stale text saying the race transfer existed
only for q=3,4 and that no transfer was stated for other moduli.  That was a
direct internal contradiction.  The joint section now states the proved
generality: q=3,4 are the computed examples; for any real primitive chi the
joint theorem transfers to the aggregate chi=-1 versus chi=+1 weighted race
under LI(chi), while without LI it is only a limiting-variable statement.

## 2026-08-16 — Fiorilli–Martin overlap and normalization audit

The primary arXiv source of Fiorilli–Martin (arXiv:0912.4908), not a
secondary description, was inspected. Section 3.6 explicitly treats
`pi(x;q,N)-pi(x;q,R)` for odd prime `q` through the unique quadratic
character, including the influence of the lowest zero. Therefore v4's claim
that the comparison is only with an all-character pairwise race, and “an
analogue, not a specialization,” was materially wrong: the present `m=0`
unlogged race is exactly their aggregate quadratic race. The genuinely new
scope must be the continuous/growing weight, the joint `(q,m)` uniformity, and
the quantitative refinements—not the existence of the one-character modulus
aspect itself.

There is also an apparent factor-two typo in the two displayed formulas of
their Section 3.6. From their definition
`E(x;N,R)=log(x)/sqrt(x)*(pi_N-pi_R)` and their own residue-class explicit
formula, character orthogonality gives the limiting variable

```text
1 + 2 sum_{gamma>0} cos(theta_gamma)/sqrt(1/4+gamma^2),
```

whereas their display prints constant `2` with the same noise, then prints a
leading density correction twice as large. This can be checked immediately
at `q=3`, where the aggregate race is the ordinary race `2 mod 3` versus
`1 mod 3`; it also agrees exactly with the `m=0` case of the manuscript's
partial-summation transfer. The manuscript now states the overlap honestly,
derives the corrected normalization, and does not rely on the affected
Fiorilli–Martin displays.

## 2026-08-16 — critical regime promoted from question to theorem

The manuscript previously called the double limit
`M=m+1/2 -> 0`, `q -> infinity` open.  The genuinely critical scale is
`M log q -> lambda in (0,infinity)`.  With scaled ordinates

```text
y_gamma = gamma log(q)/(2 pi),
b_lambda(y) = 4 lambda/sqrt(lambda^2+(2 pi y)^2),
```

the exact phase amplitudes converge to `b_lambda(y)`: microscopic low zeros
retain order-one influence.  A new critical zero-process transfer theorem has
now been added.  If the scaled positive-zero point measures converge vaguely
and their reciprocal-square tails are uniformly tight, then:

- the full limiting variables converge in law to the explicit Bessel-product
  variable `1 + sum b_lambda(y) cos(theta_y)`;
- the variances converge to the corresponding point-measure integral;
- the bias probabilities, hence under LI the logarithmic race densities,
  converge without an extra boundary hypothesis (the limit is atomless unless
  the zero measure is empty, in which case it is the point mass at 1);
- every nonempty limit is provably non-Gaussian, with fourth cumulant
  `-(3/8) sum b_lambda(y)^4 < 0`.

This classifies the critical corner conditionally on precisely the low-zero
input that conductor-uniform Riemann–von Mangoldt estimates cannot supply.  It
also changes the conjectural target: quadratic-character families should yield
a *distribution* of critical densities obtained by applying the explicit
functional to the symplectic Katz–Sarnak point process, not a deterministic
Gaussian profile for each character.

## 2026-08-16 — third-order uniform density expansion

The Bessel/Fourier argument was pushed one full order past v4.  With
`S_6=sum_gamma (2a_gamma)^6`, the new term inside the leading Gaussian factor
is

```text
  1/(40 sigma^4)
+ 5 S4/(128 sigma^6)
- 5 S6/(192 sigma^6)
+ 105 S4^2/(8192 sigma^8),
```

and the joint theorem now has remainder `O_delta(G/sigma^6)`, uniformly for
`M>=delta>0`.  The proof uses the exact sixth-order coefficient
`log J0(z) = -z^2/4-z^4/64-z^6/576+O(z^8)`, Gaussian moments through the
eighth, and the absolute amplitude bounds `S_{2k+2}<=16 S_{2k}`.  The sixth
moment also has a new closed form

```text
S6 = 12 S4 + 256 M^3 (log xi)'''(m+1,chi).
```

`paper/v3/verify_dissolution.py` was extended and completed successfully.  It
found `sup |remainder|/z^8 = 0.000259954` on a 1000-point multiprecision grid
and independently evaluated the new prediction.  Relative residuals after the
third-order term were:

- `(q,m)=(4,8)`: `-2.04e-4` (second order `-7.40e-4`);
- `(4,20)`: `-6.18e-6` (second order `-7.88e-5`);
- `(3,60)`: `+7.74e-7` (second order `-4.90e-6`);
- `(4,100)`: `+2.14e-6`, below the reference density's `9.9e-6`
  Gaussian-tail modelling floor (so the apparent worsening from the already
  sub-floor second-order residual is not statistically meaningful).

The common explicit dependence in the joint theorem was conservatively
updated from `C delta^-6` to `C delta^-8` because absorbing the large-`t` tail
at third order uses the supremum of `sigma^7 exp(-c delta^2 sigma^2)`.
