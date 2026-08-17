# Independent density post-processing verifier

This directory contains a deliberately small verification layer that shares
no numerical library or code path with `race_density_arb.py`.

## What is checked

`check_density_postprocess.py` uses only Python's standard library. Every JSON
decimal is parsed as an exact `fractions.Fraction`; no binary floating-point
operation is used. It checks:

1. all 14 density interval widths are strictly below `2e-7`;
2. 12 six-decimal table entries are forced by their intervals;
3. the two daggered rows cross exactly the asserted half-unit boundary and
   permit no third rounded value;
4. four enclosures for `sqrt(2*pi*sigma^2)`, by squaring exact rational
   endpoints and using the same 20-decimal pi interval proved in mathlib;
5. leading, second-order, and third-order relative residual enclosures for all
   four dissolution rows; and
6. the three displayed `sigma^4`-scaled second-order residual enclosures.

The parser rejects duplicate JSON fields, unknown nested fields, substituted
row keys, and any missing required claim.  In particular, the success counts
are derived only after the exact 14-row and 4-row manuscript schemas have been
matched; they are not permissions to omit checks.

`Formal/DensityPostprocessing.lean` independently kernel-checks the 14 rounding
claims, the 4 square-root certificates (using `Real.pi_gt_d20` and
`Real.pi_lt_d20`), generic positive interval propagation, and the manuscript's
leading/second-order residual enclosures for all four rows. The Python checker
also covers the more cumbersome third-order and scaled residual arithmetic.

## Trust boundary

This verifier treats the source density, `sigma^2`, `S4`, and `S6` intervals
as hypotheses. It does **not** establish that the analytic quantities are in
those intervals. In particular, it does not verify the zero lists, GRH/LI,
FLINT/Arb, Bessel products, quadrature, or tail estimates. Its purpose is to
make every downstream rounding and residual transformation independently
reproducible and fail-closed.

The density endpoints were transcribed from
`prototype/explore/race_density_arb_results.txt`. The `sigma^2`, `S4`, and
`S6` intervals are outward decimal widenings of the closed-form evaluations
used by `paper/v3/verify_dissolution.py`. Neither provenance statement is used
as a proof by this checker: the JSON values are explicit assumptions, and a
future fully independent analytic implementation should replace that input
side of the trust boundary.

The exact certificate SHA-256 printed by a release run must match
`expected_output.txt`.  This detects accidental edits to the explicit input
hypotheses; it does not make those hypotheses analytically rigorous.  The
Lean file duplicates the density, variance, and `S4` endpoints used in its
theorems instead of importing this JSON, providing an independent
transcription check for the core layer.

Thus the assurance chain is:

```text
analytic interval generator  ->  exact JSON hypotheses
                              ->  stdlib Fraction checker
                              ->  independent Lean theorems for the core layer
```

The last two arrows detect transcription, directed-rounding, formula, and
error-propagation mistakes; they cannot repair an invalid analytic input.

## Reproduce

From the repository root:

```text
python algorithms/prime-sum/prototype/independent_verifier/check_density_postprocess.py
python algorithms/prime-sum/prototype/independent_verifier/test_fail_closed.py
```

From `algorithms/prime-sum/formal`, with the pinned Lean toolchain:

```text
lake env lean Formal/DensityPostprocessing.lean
lake env lean Formal/DensityPostprocessingAudit.lean
```

Also run a source scan anchored at the start of a Lean command:

```text
rg -n '^\s*(axiom|sorry|admit|unsafe)\b' Formal/DensityPostprocessing*.lean
```

The scan must return no matches. Foundational dependencies printed by the
audit are expected to be limited to Lean/mathlib's standard `propext`,
`Classical.choice`, and `Quot.sound` where real analysis requires them.
