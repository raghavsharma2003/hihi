# Lean verification layers for the weighted-races project

This standalone Lean 4/mathlib project machine-checks narrow but genuine
supporting layers in 71 theorem declarations.  The broad weighted-races
manuscript is supported by
[`Formal/WeightedRaces.lean`](Formal/WeightedRaces.lean) (34 algebraic
declarations) and
[`Formal/DensityPostprocessing.lean`](Formal/DensityPostprocessing.lean)
(27 exact post-processing declarations).  The separate focused
hyperelliptic project is supported by
[`Formal/CanonicalHyperellipticCore.lean`](Formal/CanonicalHyperellipticCore.lean)
(10 elementary critical-scaling declarations).

Verified here:

- finite-zero amplitude, variance, and variance-derivative identities;
- the termwise fourth- and sixth-amplitude identities used to derive `S4` and
  `S6` from logarithmic derivatives;
- exact normalized second and fourth moments of a uniform cosine phase;
- fourth-cumulant arithmetic and finite amplitude-moment bounds;
- the squared critical-rescaling identity and one-zero threshold algebra;
- all rational coefficients in the displayed third-order Edgeworth formula.
- the 14 density-table rounding/width claims, including both daggered rows;
- four square-root enclosures from mathlib's certified bounds for `Real.pi`;
- generic interval monotonicity and the four leading/second-order residual
  enclosures used in the dissolution tables.
- the exact geometric-block and trigonometric denominator identities for the
  focused hyperelliptic race;
- convergence of both parity centers and of the critical one-pair amplitude
  to its hard-edge coefficient.

Not verified here: GRH, LI, zero-list completeness, infinite series/products,
analytic continuation or explicit formulae for Dirichlet L-functions,
probabilistic convergence theorems, Fourier remainder estimates, numerical
quadrature, or Arb certificates.  The focused module also does not formalize
hyperelliptic curves, Frobenius, Katz--Sarnak or Kowalski inputs, compact-group
heat kernels, determinantal processes, or the quenched-law transfer.  Those
are logically separate obligations.
The proof file intentionally contains no `sorry`, `admit`, `unsafe`,
project-local `axiom`, or placeholder proof. As usual, real analysis in mathlib
uses Lean's foundational axioms such as quotient soundness and classical choice;
`Formal/Audit.lean`, `Formal/DensityPostprocessingAudit.lean`, and
`Formal/CanonicalHyperellipticCoreAudit.lean` print the exact dependency sets
for every theorem.

Build from this directory with:

```text
lake exe cache get
lake build
lake env lean Formal/Audit.lean
lake env lean Formal/DensityPostprocessingAudit.lean
lake env lean Formal/CanonicalHyperellipticCoreAudit.lean
```

The exact Lean toolchain and mathlib revision are pinned by `lean-toolchain`
and `lake-manifest.json`.  Do not run `lake update` in a release build; it may
change the pinned dependency graph.
