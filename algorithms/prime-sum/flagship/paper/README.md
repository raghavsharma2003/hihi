# Focused-paper source

Working title: *A simultaneous hard-edge limit for weighted hyperelliptic
prime races*.

This is a new companion manuscript on branch
`codex/weighted-races-focused-flagship`.  It does not replace or extend the
frozen 66-page manuscript on `codex/weighted-races-breakthrough`.

## Build

The main source is `main.tex`; section files are under `sections/` and the
bibliography is `references.bib`.  A normal local build is:

```text
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

No PDF from this directory is a release artifact until it has been rendered
page by page, checked for clipping/overlap/unresolved references, and recorded
in a release manifest.  The current draft has internal AI-agent audits but no
external human specialist review.

On 2026-08-17, Tectonic 0.17.0 completed a three-pass TeX/BibTeX auxiliary
build from the repository root with exit code zero:

```text
.tools/tectonic/tectonic.exe --outfmt aux --keep-logs --outdir <temporary-dir> algorithms/prime-sum/flagship/paper/main.tex
```

That check produced no undefined references or citations.  It is a source
integration check, not the required rendered-PDF inspection.

The audit trail is preserved in `SOURCE-AUDIT.md`, `INTEGRATION-AUDIT.md`,
`COHOMOLOGY-BRIDGE-AUDIT.md`, and `POST-REPAIR-AUDIT.md`.  The last of these
audits the repaired snapshot and records the current verdict: conditional
mathematical pass, not release-cleared.

## Proof and formalization boundary

The main theorem imports deep arithmetic results of Katz--Sarnak and Kowalski.
The new elementary scaling core has a no-placeholder Lean 4 module at
`../../formal/Formal/CanonicalHyperellipticCore.lean`; that module does not
formalize the imported arithmetic geometry, heat-kernel bridge, or
determinantal-process convergence.  The manuscript must never be described as
fully Lean verified unless those missing bridges are actually formalized.
