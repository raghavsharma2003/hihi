# Post-repair end-to-end mathematical audit

Audit date: 2026-08-17

Scope: the current repaired `main.tex` and all files under `sections/`. This
pass rederived the proof chain after the orbit-Haar, cohomology, operator,
heat, quotient-metric, and Bessel repairs. It did not edit any TeX source.

## Strict verdict

**No fatal or high-priority mathematical error remains in the current
files.** The headline theorem now has a mutually consistent proof chain.

The release status is nevertheless:

> **CONDITIONAL MATHEMATICAL PASS; NOT YET RELEASE-CLEARED.**

The pass is conditional on the cited deep inputs: Katz--Sarnak monodromy and
tameness, Kowalski's large-sieve and relation-space theorems, Deligne's weight
theorem, and Soshnikov's DPP results. These are not proved from first
principles or formalized in Lean here. A claim of 100% first-principles or
end-to-end Lean verification would be false.

During the final audit window, the root pass also applied the only two minor
clarifications I had identified:

- `sections/02-linear-independence.tex`, lines 97--101, now spells out the
  functional-equation embedding in the signed permutation group and the
  equivalence between full splitting-field degree and full Weyl group.
- `sections/03-transfer.tex`, lines 80--84, now gives the precise
  connected-nonproper/lisse-section reason for compactly supported
  degree-zero vanishing.

I found no remaining TeX correction to request.

## 1. Genuine endpoint law and LI replacement: PASS

The endpoint calculation in `sections/01-race-law.tex`,
`lem:endpoint-decomposition` and `eq:endpoint-cosine` (lines 61--153), has
the correct sign, normalization, parity centers, and critical coefficient.
For `r=Q^M`, a conjugate root pair contributes exactly

```text
4(1-r^(-1)) Re[(exp(i N theta)-r^(-N))
                 /(1-r^(-1) exp(-i theta))].
```

The square main term gives `2r/(r+1)` on even endpoints and `2/(r+1)` on
odd endpoints. Its error exponent is at most
`-min(M,1/4)N+O(1)`. The three cases following
`eq:higher-power-exponent` give exponential decay for every `M>0`.

Lines 164--177 construct the genuine endpoint law for every parameter by
pushing Haar measure on the closed cyclic angle-parity orbit. The remainder
tends to zero, hence has vanishing Cesaro second moment, so the empirical
measures converge in `W_2`. Under `eq:LI`, lines 179--222 correctly identify
the orbit with full phases times fair parity and obtain
`eq:finite-quenched-law`. The law is atomless, so the positivity density
follows.

In `sections/05-assembly.tex`, lines 4--19, the independent-phase model is
now substituted for the genuine law only on the LI event. For a bounded test
of sup norm at most one, the exact loss is at most twice the non-LI
probability. This closes the former model-versus-actual-law gap.

## 2. Square-field Galois criterion and density-one LI: PASS

In `sections/02-linear-independence.tex`,
`eq:normalized-rational-polynomial` (lines 19--30), square `Q=s^2` makes the
normalized reciprocal roots the roots of a rational polynomial without
changing the splitting field. Pair products are one. Under maximal Weyl
group, Kowalski's rational relation-space theorem forces equal exponents in
each reciprocal pair. Exponentiating an angle--pi relation twice gives pair
coordinates `(2a_j,0)`, hence all coefficients vanish (lines 40--63). No
integral saturation assertion is used.

The exceptional estimate `eq:kowalski-exceptional` includes the erratum
factor `g^2` and exponent `1/(4g^2+3g+5)`. Lines 97--101 now explicitly
explain why Kowalski's full-degree formulation is equivalent to full Weyl
group. Division by `Q-2g` gives `eq:LI-probability-bound`.

At lines 117--128, putting `x_g=(log Q_g)/g^2` is sufficient:
`x_g/log(g+2)` tends to infinity, while `log log Q_g=o(x_g)`. Thus the
exceptional probability tends to zero.

## 3. Half-Tate twist and direct character estimate: PASS conditional on import

The convention in `sections/03-transfer.tex`,
`eq:frob-convention`--`eq:half-tate-character` (lines 12--49), is consistent.
Geometric Frobenius has root-pair product `Q`; the constant character sends
arithmetic Frobenius to `s` and geometric Frobenius to `s^(-1)`. The twisted
roots are `alpha_j/s`, the pairing multiplier is `Q s^(-2)=1`, the character
has weight `-1`, and the twisted rank-`2g` sheaf has weight zero. Since the
characteristic is greater than `2g+1>=5`, `s` is a 3-adic unit, so the
constant character exists continuously. It is geometrically trivial and does
not change geometric monodromy.

The direct proof of `prop:character-equidistribution` (lines 59--99) is
sound. For a nontrivial irreducible algebraic representation `rho`, the
associated sheaf is lisse, tame, pure of weight zero, has rank `dim rho`, and
has no geometric invariants. On
`U_g=A^1-{1,...,2g}`, `chi_c(U_g)=1-2g`. Compactly supported degrees zero and
two vanish. The compact-support GOS formula has no tame-drop term, hence

```text
dim H_c^1(U_g_bar, rho(F_g)) = (2g-1) dim rho.
```

The trace formula and Deligne's weight bound give
`(2g-1)(dim rho)sqrt(Q)`. Division by `Q-2g` gives exactly
`eq:character-bound`. No residual lattice, mod-3 cover, or hidden
genus-exponential Betti factor remains.

## 4. Quotient metric, Brownian lemma, and heat bridge: PASS

`lem:conjugacy-quotient-metric`, `sections/03-transfer.tex` lines 122--155,
now displays the affine-Weyl minimization. For the metric
`-Tr(XY)/2`, torus angles are Euclidean. On the closed type-C alcove, signs
and `2pi` translations cannot improve ordinary nonnegative-angle matching;
the rearrangement inequality selects increasing order. Thus both the equality
and `d_conj<=d_G` are correct.

The same-phase coupling in `lem:T-lipschitz` has the correct factor `1/2`
from `E cos(Phi)^2=1/2`. Direct differentiation gives the displayed global
`O_lambda(g)` Lipschitz constant, including at eigenvalue collisions.

In `sections/A-heat-trace.tex`, `lem:brownian-displacement` (lines 117--142)
uses the correct heat convention: `P_s=exp(s Delta)` has local coordinate
variance `2s`. Nonnegative Ricci curvature gives the distributional bound
`Delta d(x,.)^2<=2D`, hence expected squared displacement at most `2Ds`.
The cut-locus singular part has the favorable sign.

The type-C Casimir and dimension-shell estimate in
`lem:uniform-heat-trace` have the correct metric normalization.
`prop:heat-bridge` correctly produces `K_(2s)(e)^(1/2)`, relative to Haar
probability, and two smoothing errors give `2L sqrt(2D_g s)`.

With `s=g^(-8)`, `D_g=2g^2+g`, and `L=O_lambda(g)`,
`prop:arithmetic-haar-transfer` gives `O_lambda(g^(-2))` plus

```text
Q^(-1/2) exp(C g^2 log(g+2)),
```

which vanishes under `eq:growth`.

## 5. Operator hard edge and marked W_2 stability: PASS

The finite kernel in `sections/04-hard-edge.tex`,
`eq:finite-sp-kernel` (lines 16--43), has the correct Jacobian factor `4/d`.
Its compact-uniform Riemann-sum limit is the symplectic sine kernel, including
zero. After zero extension, compactly supported matrix elements converge;
the projection operators are contractions, so density gives weak-operator
convergence. Local diagonal convergence and the common bound below two give
all bounded local traces. These are the Soshnikov hypotheses used at lines
45--59. `eq:no-escape-zero` and zero limiting intensity at the singleton
exclude a hidden hard-edge atom.

The coefficient in `eq:finite-critical-coefficient` is exact, converges
locally uniformly on the closed half-line, and obeys the displayed `1/y`
envelope. Integrating against the diagonal bound gives the uniform `O(1/R)`
squared-tail estimate. Also `integral a_lambda(y)^2 dy=4 lambda`, so the
limiting coefficient sequence is square-summable almost surely.

Appendix B, `prop:marked-stability` (lines 70--148), correctly matches points
on the closed half-line and uses the two tails to obtain `ell^2` coefficient
matching in probability. The exact shared parity/shared phase cost in
`eq:parity-shared-coupling-cost` then gives `W_2` convergence. The Borel
enumeration supplies measurability, and splitting off the least point gives
absolute continuity.

## 6. Both nondegeneracy statements: PASS

For the random conditional measure, `eq:conditional-variance-statistic` is an
integrable DPP linear statistic. Since the limiting kernel is a projection,
the covariance identity symmetrizes to `eq:projection-dpp-variance` with the
essential factor `1/2`. Lines 174--205 separately verify tail convergence,
finiteness, and strict positivity. A fixed conditional law would have fixed
variance, proving `prop:random-law-nondegenerate`.

The scalar proof does not reuse that variance. In
`prop:scalar-nondegenerate` (lines 219--313), symmetry, absolute continuity,
and a direct small-ball event give `F_lambda(xi)>1/2`. For every `N`, the
factorial-moment Gram determinant is positive for `N` distinct points in a
fixed interval near zero, so the crowding event has positive probability.

On that event the selected coefficients lie in `[a_0,4]`, with `a_0>2`.
The expanded Bessel proof is complete: it uses `exp(-cNt^2)` near zero,
`r^N` on a compact annulus with `r<1`, and an integrable large-frequency
bound with ratio below one. Thus the characteristic function is in `L^1`
with norm `O(N^(-1/2))`, and Fourier inversion gives the uniform density
bound. Convolution with all remaining independent marks cannot increase it.
Positive-probability values of the scalar therefore occur arbitrarily close
to `1/2`, contradicting any almost-sure constant greater than `1/2`.

## 7. Assembly and explicit fields: PASS

The three comparisons in `sections/05-assembly.tex`, lines 4--19, combine by
the bounded--Lipschitz triangle inequality on the Polish `P_2` space.
Absolute continuity makes evaluation on `(0,infinity)` almost surely
continuous, giving scalar convergence; boundedness gives expectation
convergence.

For the explicit fields, Bertrand's postulate and minimality of `n_g` give

```text
g^2 log^2(g+2) <= log Q_g
                 < g^2 log^2(g+2)+2 log p_g.
```

Thus `Q_g` is an odd square, its characteristic exceeds `2g+1`, and the
required growth ratio tends to infinity. No iterated limit is used.

## 8. Static checks and remaining release gates

The current tree passed these non-rendering checks:

- 102 labels, with no duplicate;
- 96 reference targets, with none missing;
- 24 citation uses, with none missing and no bibliography key unused;
- brace and begin/end count scans balanced in every TeX file;
- no TODO, FIXME, placeholder proof, stale half-Tate orientation, or known
  malformed command pattern;
- `git diff --check`, with no whitespace error.

This audit did not generate a new PDF. Hard release gates remain:

1. compile the focused manuscript and inspect every rendered page;
2. independently inspect the exact Katz--Sarnak and Kowalski source text
   against the final wording;
3. obtain review from an arithmetic geometer and a random-matrix/DPP expert;
4. rerun the novelty search immediately before posting;
5. retain the honest formalization boundary: elementary scaling lemmas are
   Lean-checked, but the headline theorem is not end-to-end Lean formalized.

Subject to those gates, the repaired proof is coherent and suitable for
serious external circulation. It is not defensible to call it impossible to
be wrong, 100% first-principles, or 100% Lean verified.
