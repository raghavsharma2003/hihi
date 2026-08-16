# Lean verification layer for *Weighted Prime Number Races*

This standalone Lean 4/mathlib project machine-checks a narrow but genuine
algebraic layer of the paper in 34 theorem declarations. The source is
[`Formal/WeightedRaces.lean`](Formal/WeightedRaces.lean).

Verified here:

- finite-zero amplitude, variance, and variance-derivative identities;
- the termwise fourth- and sixth-amplitude identities used to derive `S4` and
  `S6` from logarithmic derivatives;
- exact normalized second and fourth moments of a uniform cosine phase;
- fourth-cumulant arithmetic and finite amplitude-moment bounds;
- the squared critical-rescaling identity and one-zero threshold algebra;
- all rational coefficients in the displayed third-order Edgeworth formula.

Not verified here: GRH, LI, zero-list completeness, infinite series/products,
analytic continuation or explicit formulae for Dirichlet L-functions,
probabilistic convergence theorems, Fourier remainder estimates, numerical
quadrature, or Arb certificates. Those are logically separate obligations.
The proof file intentionally contains no `sorry`, `admit`, `unsafe`,
project-local `axiom`, or placeholder proof. As usual, real analysis in mathlib
uses Lean's foundational axioms such as quotient soundness and classical choice;
`Formal/Audit.lean` prints the exact dependency set for every theorem.

Build from this directory with:

```text
lake exe cache get
lake build
lake env lean Formal/Audit.lean
```

The exact Lean toolchain and mathlib revision are pinned by `lean-toolchain`
and `lake-manifest.json`.  Do not run `lake update` in a release build; it may
change the pinned dependency graph.
