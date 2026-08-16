# Release-candidate manifest

Generated 2026-08-17 (Asia/Calcutta) for the commit containing this file.
This is a synchronized local release candidate, not a journal acceptance or a
claim of external review. The public GitHub/Zenodo copies were intentionally
not cited as current because they had not yet been updated to this tree.

## Toolchain

- Python 3.12.13
- python-flint 0.9.0; FLINT 3.6.0
- mpmath 1.4.1; NumPy 2.5.2; SciPy 1.18.0
- Tectonic 0.17.0
- Lean 4.33.0, commit `d8b18978322de05a8f3dba51ef03cf5461676c17`
- Lake 5.0.0; mathlib v4.33.0 at
  `db584cd6d46c92f209a44c0f1c829460d327499d`

## Final checks

- Tectonic automatic rerun: exit 0; 66 pages; no undefined reference,
  undefined citation, overfull box, or PDF-bookmark warning. Four harmless
  underfull-box diagnostics remain.
- Structural PDF check: 66/66 pages have extractable text; no empty pages.
- Visual check: every page inspected in six contact sheets; pages 1, 34, 44,
  59--61, 63--64, and 66 additionally inspected at high resolution.
- Zero/variance certificate: exit 0; all 511 and 537 balls localized, simple,
  and complete by winding counts.
- Density certificate: exit 0 for q=3 and q=4; all fourteen outward intervals
  exactly match the manuscript.
- Monotonicity certificate: exit 0; all 145 and 140 finite cells plus both
  analytic bridges passed.
- Lean: full 2,718-job pinned build and all 34 axiom-audit entries passed; no
  project `sorry`, `admit`, `unsafe`, or `axiom` command. This covers supporting
  algebra only; zero complete TeX theorems are fully Lean-formalized.

Terminal transcripts are in `release-logs/`. The assumptions and exact trust
boundaries are recorded in `REPRODUCIBILITY.md` and
`SUBMISSION-READINESS.md`.

## SHA-256

```text
e9b5e358b5821fe9004eadf916d4264cca95ec384948baebff32cec9c5e0688c  algorithms/prime-sum/paper/weighted-races.tex
aa1d3ee9a87e37067f1840deacb4bd094803cb8fe815637d6b17da3cced7e27a  algorithms/prime-sum/paper/weighted-races.pdf
aa1d3ee9a87e37067f1840deacb4bd094803cb8fe815637d6b17da3cced7e27a  output/pdf/weighted-races.pdf
45d6352281aa9240b62e2546bc61af6463e068681ef8f8bca22fea007bbed854  algorithms/prime-sum/prototype/explore/certify_arb.py
21ad06951b41cc9ca544dbddba231a06348184af4fb103f13569c48bd2519236  algorithms/prime-sum/prototype/explore/race_density_arb.py
3d1d456bf4d22c1a6776bda11013f51423231c8c968494e07ffe3818822dfca2  algorithms/prime-sum/paper/v3/verify_monotonicity_arb.py
f7ac9418b4ee481dd0589f2143ecf967866d3fb669c11ecee6ebb4ae34fc6cb6  algorithms/prime-sum/prototype/explore/chi4_zeros.txt
dba9101f9371b74a7d3747e8ffe2e431081dee2edfdb5224c105ff9bf9740f9a  algorithms/prime-sum/prototype/explore/chi3_zeros.txt
b520ec6194ef213db1030b0b78223ef513628ff5f22f158f69901fd779309891  algorithms/prime-sum/formal/Formal/WeightedRaces.lean
32490c05d4c0a40838a295fd3d29c529fe089154928e8d95a6e5754f604d03b1  algorithms/prime-sum/formal/Formal/Audit.lean
dc363249f5730e496c29d39dbbecd64aa86fcee17eb115c9830b89f0afe92cbe  algorithms/prime-sum/formal/lake-manifest.json
```

## Deliberately unresolved before public submission

- No external human proof audit or independent numerical reimplementation has
  yet been completed.
- No project license was chosen. Do not infer an open-source license from the
  presence of the source; the author must select one before public release.
- The public archive/repository must be synchronized to the commit containing
  this manifest, then its immutable URL/DOI inserted in the manuscript.
- The finite-sieve C programs still need a clean compiler/overflow audit and
  archived raw runs in the release environment.
