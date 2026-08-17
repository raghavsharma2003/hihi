# Focused-paper release manifest

Manifest date: 2026-08-17

Status: internally verified release candidate; not yet cleared for journal
submission or advertised as externally verified.

## Artifact

- Title: *A simultaneous quenched hard-edge limit for weighted
  hyperelliptic prime races*
- File: `output/pdf/simultaneous-hard-edge-weighted-hyperelliptic-prime-races.pdf`
- Pages: 23, US Letter
- Bytes: 201820
- SHA-256:
  `72DBA8006CC101023D97BEA5A34952328E17ECFB1467C9531CC89B34C5767EC7`
- PDF metadata: title, author, subject, and keywords present
- PDF structure: 11 outline entries, 24 fonts, every font embedded, no page
  without extractable text

## Reproducible build

Run from the repository root:

```powershell
& ".\algorithms\prime-sum\flagship\paper\build-release.ps1"
```

The successful release build used Tectonic 0.17.0, ran TeX and BibTeX to a
fixed point in a fresh temporary directory, and exited zero.  The fail-closed
log gate found no TeX error, undefined control sequence, unresolved citation
or reference, or overfull box.  Tectonic emitted the host's nonfatal
Fontconfig configuration diagnostic; all fonts in the resulting PDF were
nevertheless embedded and rendered correctly.

The build input ledger is the following sorted list.  Its aggregate is the
SHA-256 of the UTF-8, LF-joined lines, including the terminal LF:

```text
8EEE18AC6447DBD1B80B5160278ABE13948BED282888176A1476565CC7868ED6  algorithms/prime-sum/flagship/paper/build-release.ps1
50D41565AA0E82D884ADEBD0B22BB17B8E352CE20A07955BA4C8881B0FE3FED9  algorithms/prime-sum/flagship/paper/main.tex
1C303DBB0DB97AAE1D5C52D4B5BCC60F6B82DEDDA3D785722D6E05EC283881D2  algorithms/prime-sum/flagship/paper/references.bib
E6C5DBDBE275F04397E2C1008C6F2612BB03F7B4B8B8168D2372E46C137F17BC  algorithms/prime-sum/flagship/paper/sections/00-introduction.tex
CDA509BB55B253F2650CDCB15DE0553DBE91EBBDDD5F703714B1A0C5A0B6CAB1  algorithms/prime-sum/flagship/paper/sections/01-race-law.tex
892FDAF424FC662D86E06733A3E40978693A6DA52C97815A94DFD7013EEE2504  algorithms/prime-sum/flagship/paper/sections/02-linear-independence.tex
BE6B09D3CD03C94AF4DE1F287384E0968FEE68A9A638718AE39CAFBD635130D3  algorithms/prime-sum/flagship/paper/sections/03-transfer.tex
893933310E136A1DFFD59B782D5E08523776BDB628E5437274CC9B8B2A447330  algorithms/prime-sum/flagship/paper/sections/04-hard-edge.tex
2739EBE7D5411EE0C62FB02EE9CC39C7A0C8D099282E6C3FEF40F5622D5A05F7  algorithms/prime-sum/flagship/paper/sections/05-assembly.tex
1C3A07AC58D7A37F025930BE0A6533DAEF251D38005D99752A0F880C92BD84E1  algorithms/prime-sum/flagship/paper/sections/A-heat-trace.tex
8493A73EBD4F176D5FC8E9956A5DC1A76E4FEB9545CB0F1AF64D2B3CD6A1E895  algorithms/prime-sum/flagship/paper/sections/B-marked-laws.tex
```

Aggregate SHA-256:
`5976085238FD23B7958AF9A52C0F798C247D7B233AB0DEBED9751A41E8F1AFB3`.

## Render and static QA

- Rendered all 23 pages at 140 dpi with Poppler and visually inspected every
  page, including full-resolution checks of the proof map and the
  disclosure/bibliography transition.
- No clipping, overlap, missing glyph, blank page, broken equation, or
  unreadable reference was found.
- Extracted-text scan found zero occurrences of `??`, `undefined`, `TODO`,
  `FIXME`, `PLACEHOLDER`, raw `\cite{`, raw `\ref{`, or `qquad`.
- Equation numbers are automatic and section-based: 1.1--1.9 through
  5.1--5.18, A.1--A.12, and B.1--B.8.  `(LI)` is the sole semantic manual tag.
- Theorem 1.1, Corollary 1.2, and Example 1.3 resolve with the correct
  `cleveref` types.  The post-edit audit found 104 unique labels and no
  duplicate or missing target.

## Mathematical and literature gates

- `EXACT-SOURCE-LEDGER.md`: aggregate PASS for the inspected Katz--Sarnak,
  Kowalski plus erratum, Raynaud, Deligne, and Soshnikov imports and for the
  inspected new bibliography metadata.
- `FRESH-NOVELTY-SEARCH.md`: no exact collision located through 2026-08-17;
  Bailleul--Devin--Keliher--Li and the relevant 2026 literature are now cited
  and distinguished.  This is a structured search, not proof of priority.
- `POSTEDIT-NOTATION-AUDIT.md`: PASS after the theorem/corollary/example split,
  first-use definitions, notation repairs, and automatic numbering.
- `REFEREE-RELEASE-REVIEW.md`: the post-revision internal delta review found no
  theorem regression; its final overfull-display finding was repaired and the
  fail-closed build then passed.

These are internal AI-agent audits, not external peer review.

## Lean boundary

The focused elementary layer rebuilt successfully on Lean 4.33.0/mathlib:

- `Formal/CanonicalHyperellipticCore.lean`: 10 declarations; SHA-256
  `FEA2ECDF1C64C6B543DCA80E6FB9C7998E4F582BFF4A4E9145C9A430548B0093`
- `Formal/CanonicalHyperellipticCoreAudit.lean`: SHA-256
  `29442C6668C2361E10BCD524FD8B1BAEA1A46C1860454B0D60E13165EEBB2112`
- anchored scan: no project `axiom`, `sorry`, `admit`, or `unsafe` declaration
- axiom report: only `propext`, `Classical.choice`, and `Quot.sound`

This formalization checks the geometric block, parity centers, elementary
limits, and critical-amplitude scaling.  It does **not** formalize the
headline theorem, the curves or Frobenius bridge, Katz--Sarnak or Kowalski,
the heat-kernel transfer, or determinantal-process convergence.  Complete
headline-theorem Lean coverage remains zero.

## Gates still open before submission

1. Independent human review by an arithmetic geometer of the monodromy,
   large-sieve, and cohomological bridge.
2. Independent human review by a random-matrix/DPP specialist of the hard-edge
   and marked-law passage.
3. Human-author verification and acceptance of responsibility for every proof,
   citation, and disclosure statement.
4. Author affiliation, postal address, and corresponding-author email for the
   target journal; these were not invented or replaced by placeholders.
5. A final database-level priority check immediately before public posting.

Accordingly, this manifest records a strong internal release candidate, not a
claim that the paper is bulletproof, 100% Lean verified, peer reviewed, or
guaranteed publishable.
