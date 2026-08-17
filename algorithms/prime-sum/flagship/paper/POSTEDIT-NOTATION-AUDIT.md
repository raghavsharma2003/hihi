# Post-edit notation and logic audit

Audit date: 2026-08-17.  Scope: the current `main.tex` and all eight included
section files.  The TeX source was inspected read-only; this report is the only
file created by the audit.

## Verdict

**Conditional pass.**  I found no theorem-level regression, broken implication,
missing citation key, unresolved cross-reference, or editorial change that
altered the mathematical content.  The split into theorem, corollary, and
example preserves the earlier assertions and makes their logical dependence
clear.  Four localized release-grade fixes remain: three notation/ordering
repairs and one priority-wording repair.

## Mandatory fixes

1. **Make the first-use order literal in the introduction.**  In
   `sections/00-introduction.tex`, `\nu_{g,t,\lambda}\in\Ptwo` is used at
   current line 60 before `\Ptwo` is defined at lines 65--67.  Also, the
   two-randomness paragraph names `\PiSp` at line 70 before the process is
   introduced at lines 76--83.  Exact repair: move the sentence defining
   `\Ptwo` and `\Wtwo` to immediately before the paragraph beginning "For
   every parameter"; move the rest of the two-probability-layer paragraph to
   immediately after the definition of `\nu_\lambda(\xi)` and its phases.
   This changes no mathematics and makes every body-text use genuinely
   post-definition.

2. **Use the already defined Weyl-group notation consistently.**  Section 3
   defines
   `W_{2g}=(\mathbb Z/2\mathbb Z)^g\rtimes S_g`.  In
   `sections/03-transfer.tex`, current line 145 unexpectedly switches to
   `W(C_g)` in the affine-Weyl minimum.  Replace `W(C_g)` by `W_{2g}` (or write
   `W(C_g)=W_{2g}` there).  The groups intended are the same, but the current
   switch looks like a new undefined symbol.

3. **Bracket the falling factorial inside the expectation.**  In
   `sections/04-hard-edge.tex`, current lines 256--261 correctly define
   `(n)_N`, but the display `\E(\PiSp(I))_N` is visually ambiguous between the
   falling factorial of the count and a subscript outside the expectation.
   Write
   `\E\!\left[(\PiSp(I))_N\right]`.

4. **Remove unqualified priority implications.**  The fresh-search ledger
   explicitly says it is evidence, not a priority certificate.  In
   `sections/00-introduction.tex`, replace "the closest direct race precedent"
   by "a particularly close direct race precedent," "The new object here" by
   "The object studied here," and "The three new bridges" by "The three bridges
   established here."  The precise comparison that follows already carries
   the novelty argument; these edits avoid claiming an exhaustive literature
   priority that the search cannot prove.

## Checks that passed

- The abstract spells out `\mathcal P_2(\mathbb R)` and `W_2`; the body explains
  the quadratic Wasserstein topology and distinguishes phase/quenched
  randomness from the outer curve/process randomness before the theorem.
- `W_{2g}` is defined before its substantive use.  The falling factorial is
  defined before the factorial-moment identity.  `J_0` is defined at its first
  occurrence as the order-zero Bessel function of the first kind.
- Theorem 1.1 fixes `\lambda>0` in its own statement.  Corollary 1.2 follows by
  the almost-sure continuity of half-line evaluation at the absolutely
  continuous limit; boundedness in `[0,1]` justifies expectation convergence.
  Its natural-density clause is restricted to the density-one LI event.
  Example 1.3 invokes the separately proved field-growth estimate correctly.
- The Soshnikov edit does not strengthen the cited theorem: it now separates
  count-cylinder convergence from the manuscript's local-tightness and compact
  exhaustion argument.  The GOS, Deligne, and factorial-moment citation edits
  do not change proof meaning.
- Automatic numbering is coherent: equations run by section as 1.1--1.9,
  2.1--2.14, 3.1--3.8, 4.1--4.8, 5.1--5.18, A.1--A.12, and B.1--B.8.  `(LI)`
  is the sole deliberate manual tag.  Theorem/corollary/example numbering is
  1.1/1.2/1.3.
- A mechanical graph check found 104 unique labels, no duplicate labels, no
  missing reference targets, 19 cited bibliography keys, and no missing keys.
- A fresh Tectonic build of the edited source produced a 22-page PDF with no
  LaTeX warnings, undefined references/citations, overfull boxes, or missing
  characters.  PDF metadata and bookmarks are populated correctly.

## Bottom line

After the four fixes above, this notation/editorial gate passes.  This audit
does **not** upgrade the separate mathematical/source conclusion: independent
specialist review of the arithmetic and determinantal inputs remains required,
and the paper is not end-to-end Lean verified.

## Closeout re-audit after the four fixes (2026-08-17)

### Final verdict: PASS

All four mandatory items above are correctly applied in the current TeX:

1. `\Ptwo` and `\Wtwo` are defined before the first body-text membership use,
   and the two-probability-layer paragraph now follows the formal definition of
   `\PiSp` and `\nu_\lambda(\xi)`.
2. The affine-Weyl minimum uses the previously defined `W_{2g}` notation; no
   undefined `W(C_g)` remains.
3. The factorial moment is unambiguously written as
   `\E\bigl[(\PiSp(I))_N\bigr]`.
4. The literature paragraph now says "a particularly close direct race
   precedent," "the object studied here," and "the three bridges established,"
   removing the unsupported exhaustive-priority implications.

The theorem/corollary/example references were rechecked after automatic
numbering, both in source and in the compiled auxiliary records:

- `thm:main` resolves as **Theorem 1.1** with cleveref type `theorem`;
- `cor:prime-race-densities` resolves as **Corollary 1.2** with type
  `corollary`;
- `ex:explicit-fields` resolves as **Example 1.3** with type `example`.

The corollary's reference to Theorem 1.1, the example's joint reference to
Theorem 1.1 and Corollary 1.2, and the assembly references to all three labels
are present and correctly typed.  Their associated equations remain 1.6--1.9,
and the field-growth input remains equation 3.8.  There are still 104 unique
labels, zero duplicate labels, zero missing reference targets, and only the
intentional `(LI)` manual tag.

A fresh Tectonic build after these edits produced a 22-page PDF with populated
metadata/bookmarks and no LaTeX, citation, cross-reference, overfull-box, or
missing-character warnings.  No proof meaning changed.  There are no remaining
mandatory fixes within this notation/editorial audit's scope.
