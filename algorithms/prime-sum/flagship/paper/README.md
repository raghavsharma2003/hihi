# Focused-paper source

Working title: *A simultaneous quenched hard-edge limit for weighted
hyperelliptic prime races*.

This is a new companion manuscript on branch
`codex/weighted-races-focused-flagship`.  It does not replace or extend the
frozen 66-page manuscript on `codex/weighted-races-breakthrough`.

## Build

The main source is `main.tex`; section files are under `sections/` and the
bibliography is `references.bib`.  From the repository root, the fail-closed
release build is:

```powershell
& ".\algorithms\prime-sum\flagship\paper\build-release.ps1"
```

It uses the repository-pinned Tectonic executable, builds in a fresh temporary
directory, rejects TeX errors, unresolved references/citations, and overfull
boxes, and writes the named PDF plus its SHA-256 digest to `output/pdf/`.
A conventional local build is also possible:

```text
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

No PDF is a release artifact until it has been rendered page by page, checked
for clipping, overlap, and unresolved references, and recorded in
`RELEASE-MANIFEST.md`.  The current draft has several internal AI-agent audits
but no external human specialist review.

On 2026-08-17, Tectonic 0.17.0 completed a TeX/BibTeX release build from the
repository root with exit code zero.  The exact command used by the script is:

```text
.tools/tectonic/tectonic.exe --outfmt aux --keep-logs --outdir <temporary-dir> algorithms/prime-sum/flagship/paper/main.tex
```

That check produced no TeX errors, undefined references or citations, or
overfull boxes.  Rendered-PDF inspection is a separate gate.

The audit trail is preserved in `SOURCE-AUDIT.md`, `INTEGRATION-AUDIT.md`,
`COHOMOLOGY-BRIDGE-AUDIT.md`, `POST-REPAIR-AUDIT.md`,
`EXACT-SOURCE-LEDGER.md`, `FRESH-NOVELTY-SEARCH.md`,
`POSTEDIT-NOTATION-AUDIT.md`, and `REFEREE-RELEASE-REVIEW.md`.  The exact-source
and post-edit gates pass on the current source.  The hostile referee report
separately records the remaining human-review and submission-metadata gates.

## Proof and formalization boundary

The main theorem imports deep arithmetic results of Katz--Sarnak and Kowalski.
The new elementary scaling core has a no-placeholder Lean 4 module at
`../../formal/Formal/CanonicalHyperellipticCore.lean`; that module does not
formalize the imported arithmetic geometry, heat-kernel bridge, or
determinantal-process convergence.  The manuscript must never be described as
fully Lean verified unless those missing bridges are actually formalized.

On 2026-08-17, the 10 focused declarations and their axiom audit rebuilt on
Lean 4.33.0/mathlib.  The audit reported only mathlib's standard foundations
(`propext`, `Classical.choice`, and `Quot.sound`) and the source contains no
project `axiom`, `sorry`, `admit`, or `unsafe` declaration.
