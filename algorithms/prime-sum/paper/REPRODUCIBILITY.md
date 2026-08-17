# Reproducibility and trust-boundary guide

This guide applies to `weighted-races.tex` on branch
`codex/weighted-races-breakthrough`. It is intentionally stricter than a
normal "run these scripts" note: reproducing an output is not the same as
proving that the algorithm which produced it is sound.

The paper studies conditional prime-race laws. No computation here proves
GRH or LI. The strongest honest numerical claim is therefore a rigorous
enclosure **conditional on the paper's mathematical hypotheses and on the
soundness of the stated analytic reduction**, not an unconditional theorem
about primes.

## Status vocabulary

Use these terms consistently in the paper, repository, and submission letter.

| Class | Meaning | What it does not mean |
|---|---|---|
| Analytic theorem | A pen-and-paper implication proved in the TeX source, often conditional on GRH, NCZ, LI, or zero-process hypotheses | Formally verified; independently refereed; unconditional |
| External interval certificate | A fail-closed FLINT/Arb calculation with outward-rounded balls, conditional on the proved reduction and on its software trust base | Lean-verified; a proof of GRH/LI; immune to implementation error |
| High-precision diagnostic | A numerical cross-check using mpmath, NumPy, or SciPy | A rigorous enclosure |
| Finite computation | A deterministic sieve or exact-integer calculation over a finite range | A theorem about the limiting density; formally verified software |
| Lean-checked algebra | A compiled kernel check of the exact Lean statement | Coverage of a stronger TeX theorem or its arithmetic/analytic bridge |

## Snapshot and prerequisites

Record the precise source state before every release:

```powershell
git branch --show-current
git rev-parse HEAD
git status --short
git diff --check
```

The development machine used Python 3.12.13 with `python-flint 0.9.0`,
`mpmath 1.4.1`, `numpy 2.5.2`, and `scipy 1.18.0`. They are pinned in
`requirements-verification.txt`; a clean-environment installation still needs
to be exercised in release CI. The existing environment can be checked with:

```powershell
$PY = ".\.venv-research\Scripts\python.exe"
& $PY --version
& $PY -c "import flint, mpmath, numpy, scipy; print(flint.__version__, mpmath.__version__, numpy.__version__, scipy.__version__)"
```

The local TeX build used Tectonic 0.17.0 at
`.tools/tectonic/tectonic.exe`. The executable and its downloaded TeX bundle
are workspace tooling, not release inputs. A release should either pin them
with hashes or document a clean Overleaf/TeX Live build as a second route.

## Build the manuscript

From the repository root:

```powershell
New-Item -ItemType Directory -Force output\pdf | Out-Null
& .\.tools\tectonic\tectonic.exe `
  algorithms\prime-sum\paper\weighted-races.tex `
  --outdir output\pdf --keep-logs --keep-intermediates
```

The expected primary artifact is `output/pdf/weighted-races.pdf`. Treat a PDF
as releasable only after all of the following are done:

```powershell
rg -n "undefined references|Citation .* undefined|Emergency stop|Fatal error" output\pdf\weighted-races.log
Get-FileHash output\pdf\weighted-races.pdf -Algorithm SHA256
```

The first command should return no matches. Overfull boxes are not necessarily
mathematical errors, but every reported box must be inspected in rendered page
images. A successful TeX exit code alone is not visual QA.

## Verification order

Run the checks in this order. A downstream script that consumes the zero lists
does not replace the zero-isolation and completeness check.

### 1. Record immutable input hashes

```powershell
Get-FileHash `
  algorithms\prime-sum\prototype\explore\chi3_zeros.txt, `
  algorithms\prime-sum\prototype\explore\chi4_zeros.txt, `
  algorithms\prime-sum\prototype\explore\certify_arb.py, `
  algorithms\prime-sum\prototype\explore\race_density_arb.py, `
  algorithms\prime-sum\paper\v3\verify_monotonicity_arb.py `
  -Algorithm SHA256
```

Store this output beside the release artifact. Do not copy hashes into the
paper by hand; regenerate them from the exact release commit.

### 2. Certify constants, variances, zero localization, and completeness

```powershell
$PY = ".\.venv-research\Scripts\python.exe"
& $PY algorithms\prime-sum\prototype\explore\certify_arb.py `
  --K 0 --prec 200
```

`--K 0` is essential: the default checks only 50 zeros per character. A full
successful run must certify all 511 mod-4 and 537 mod-3 ordinate balls and a
winding count above each final ordinate. `--skip-winding` is useful for a
smoke test but is not a completeness certificate.

Trust boundary: this is a FLINT/Arb certificate plus classical zero-free and
functional-equation inputs described in the script. It is not a Lean proof.

### 3. Enclose the fourteen density values

```powershell
& $PY algorithms\prime-sum\prototype\explore\race_density_arb.py
```

For a quicker diagnostic, select a published case, for example:

```powershell
& $PY algorithms\prime-sum\prototype\explore\race_density_arb.py --q 4 --m 1
```

The script uses Arb enclosures for the variance, Gauss--Legendre
nodes and weights, a Cauchy quadrature remainder, adaptive interval integration
of the unseen-zero model error, and an analytic infinite-tail bound. The
fourteen-case output currently recorded in
`prototype/explore/race_density_arb_results.txt` was regenerated from the
repaired source on 2026-08-17: both modulus runs exited with status zero and
all printed endpoints passed directed-rounding postconditions.

An internal adversarial AI-agent audit on 2026-08-16 found two implementation
defects:

1. the adaptive `E1` sum adds `clo`/`chi`, stores a widened hull, and later
   subtracts the hull endpoints; because those are not the same balls, the
   running upper bound can become smaller than the quantity it should enclose;
2. the printed endpoints pass through binary64 and then another rounded
   multiply/divide, so one `nextafter` does not guarantee outward decimal
   rounding.

The source was repaired more conservatively: it recomputes the
active-leaf sums instead of using subtractive interval bookkeeping, formats
decimals by Arb/integer floor and ceiling, and reparses every printed endpoint
to assert the outward inequalities. A second internal AI-agent audit exercised the
repaired E1 sum on an exact toy integral and the formatter on counterexamples
that broke the former code; it found both blockers closed. It also rederived
the variance remainder, Gauss remainder, quartic tail inequality, E1
majorant, and analytic infinite-tail bound. The TeX methods section and table
have been reconciled with the rerun. These are therefore valid external
interval certificates, conditional on GRH, LI, certified zero completeness,
and the stated analytic reduction; they are not Lean-verified.

### 4. Certify the explicit monotonicity ranges

```powershell
& $PY algorithms\prime-sum\paper\v3\verify_monotonicity_arb.py
```

The expected coverage is 145 closed cells on `17.32 <= M <= 300` for `q=4`
and 140 cells on `19.12 <= M <= 300` for `q=3`, followed by a verified overlap
with the analytic `M >= 300` leg. This is a fail-closed external certificate
for the inequalities implemented by the script. It depends on the separately
certified zero lists and on the analytic lemmas in the manuscript, and it is
not Lean-verified.

The optional `--ratio`, `--stop`, and `--only` switches change the certified
domain. Results from a shortened run must not be reported as the full theorem.

### 5. Run high-precision diagnostics

```powershell
& $PY algorithms\prime-sum\paper\v3\verify_variance_identity.py
& $PY algorithms\prime-sum\paper\v3\verify_dissolution.py
```

`verify_variance_identity.py` contains assertion-based consistency checks and
must end with `ALL CHECKS PASSED`. Its optional density-shift check is skipped
if NumPy or SciPy cannot be imported, so inspect the output rather than relying
only on exit status. Its executable check, documentation, and the TeX use the
correct `4.3e-6` ceiling (observed shift about `4.23e-6`).

`verify_dissolution.py` is a diagnostic table generator. It samples several
Bessel inequalities and prints asymptotic comparisons, but it does not provide
a fail-closed proof of every statement it discusses. It must never be cited as
the proof of Theorems `thm:dissolution` or `thm:joint`.

### 6. Reproduce the finite sieves

The C scans require a compiler with `__int128` and `long double` support. No
such compiler is currently installed in the Windows development environment,
so these commands belong in Linux CI or a documented MinGW environment:

```bash
mkdir -p output/bin output/repro
gcc -O3 -std=c11 algorithms/prime-sum/prototype/explore/race_scan.c -lm -o output/bin/race_scan
gcc -O3 -std=c11 algorithms/prime-sum/prototype/explore/race_scan3.c -lm -o output/bin/race_scan3
gcc -O3 -std=c11 algorithms/prime-sum/prototype/explore/race_critical_scan.c -lm -o output/bin/race_critical_scan
gcc -O3 -std=c11 algorithms/prime-sum/prototype/explore/race_frozen_scan.c -lm -o output/bin/race_frozen_scan
output/bin/race_scan 1e10 | tee output/repro/race_mod4_1e10.txt
output/bin/race_scan3 1e10 | tee output/repro/race_mod3_1e10.txt
output/bin/race_critical_scan 1e10 | tee output/repro/race_critical_1e10.txt
output/bin/race_frozen_scan 1e10 | tee output/repro/race_frozen_1e10.txt
```

For integer weights `m=0,1,2,3`, the race difference uses signed `__int128`.
The reported natural/logarithmic measures and all fractional-weight scans use
floating-point arithmetic. The sieve code has not been formally verified and
does not itself prove absence of overflow. Calling the whole scan "exact" is
therefore acceptable only with the qualifier "exact integer accumulation for
the integer-weight difference," not as a blanket formal-verification claim.

### 7. Independently verify density post-processing

The following checker shares no numerical library or code path with the Arb
density generator.  It parses every decimal as an exact rational, requires the
exact manuscript row/claim schema, and verifies widths, six-decimal rounding,
both dagger boundaries, and the displayed residual transformations.  Its
mutation tests check that missing, substituted, narrowed, duplicated, and
unknown claims fail closed.

~~~powershell
Push-Location algorithms\prime-sum\prototype\independent_verifier
python check_density_postprocess.py
python -m unittest -v test_fail_closed.py
Pop-Location
~~~

The output must match `expected_output.txt`.  This layer assumes the analytic
density, variance, `S4`, and `S6` input intervals.  It independently verifies
their downstream arithmetic; it does not prove the Arb quadrature, zero
completeness, GRH, or LI.

## Theorem and assumption matrix

The matrix records the logical status of the headline results, not a referee's
endorsement of the proofs.

| TeX result | Main hypotheses | LI needed? | Computational input | Present Lean coverage |
|---|---|---:|---|---|
| `thm:interp` (interpolation) | real primitive character; GRH; NCZ; `m > -1/2` | For random-series identification, density, strict bias, continuity, and bounds; not for existence of the limiting distribution | None for the abstract statement | No complete coverage |
| `prop:unlogged` | GRH; NCZ; `m > -1/2` | For density consequences | None | No complete coverage |
| `prop:varid`, `cor:Cexact`, `prop:varasymp` | GRH, with central nonvanishing where the general-character factorization requires it | No | Decimal values have Arb enclosures; identities are analytic | Compiled finite-summand algebra only; no complete coverage |
| `thm:dissolution`, `cor:secondorder` | fixed real primitive character; GRH; NCZ; `m -> infinity` | No for the model law; yes to identify it with the prime race | Diagnostics only | Compiled coefficient and finite-moment fragments; no complete coverage |
| `thm:joint` | hypothesis (H) = real primitive, GRH, NCZ; `M >= delta_0 > 0` | No for the model law; yes for the race | Diagnostics only | Compiled third-order coefficient arithmetic; no complete coverage |
| `thm:critical-transfer` | (H) for the arithmetic sequence; `q_n -> infinity`; `M_n log q_n -> lambda`; vague zero-process convergence; reciprocal-square tail tightness | Only for the race-density interpretation | No family is proved to satisfy the point-process hypotheses | Compiled squared-rescaling and finite-cumulant algebra; no complete coverage |
| `thm:monotone-large` | GRH; NCZ; sufficiently large `M` | No for the model density; yes for the race | None for eventual qualitative result | Compiled finite derivative-summand algebra; no complete coverage |
| `cor:monotone-explicit` | GRH for `q=3,4`; NCZ is proved separately there | Only for the race interpretation | Complete zero lists; Arb cells to `M=300`; analytic leg thereafter | No complete coverage |
| Fourteen density intervals | GRH; LI; zero completeness; sound Fourier/tail reduction | Yes | Repaired Arb source; full 14-case rerun; directed printed endpoints; second audit | None |

The critical theorem is a conditional transfer principle. The manuscript does
not prove that a natural family of Dirichlet characters satisfies the required
microscopic point-process convergence and reciprocal-square tightness.

## Lean 4: exact present scope

The standalone project is under `algorithms/prime-sum/formal`. It contains
61 compiled supporting theorem declarations: 34 for finite algebraic
identities, cosine moments, finite moment inequalities, derivative identities,
critical rescaling, one-zero profiles, and Edgeworth coefficients; and 27 for
exact density-table rounding, square-root enclosures, and interval propagation.
A full pinned build on Lean 4.33.0/mathlib v4.33.0
(mathlib commit `db584cd6d46c92f209a44c0f1c829460d327499d`) completed
2,718 jobs successfully. The audit
file checks all exported declarations; a source scan found no `sorry`,
`admit`, `unsafe`, or project `axiom` commands. Reported axioms are only
standard Lean foundations (`propext`, `Classical.choice`, `Quot.sound`).

Those declarations do not formalize the
paper's explicit formula, Dirichlet-L zero theory, limiting distributions,
Bessel analysis, Fourier remainders, zero completeness, density quadrature, or
monotonicity certificate.

Install Lean through `elan`, open a shell in which `lake` is on `PATH`, and
confirm that `Get-Command lake` succeeds. The repository pins the toolchain but
does not vendor the `elan` launcher. Build and audit the pinned project without
updating the manifest:

```powershell
$LAKE = (Get-Command lake -ErrorAction Stop).Source
Push-Location algorithms\prime-sum\formal
& $LAKE exe cache get
& $LAKE build
& $LAKE env lean Formal/Audit.lean
& $LAKE env lean Formal/DensityPostprocessingAudit.lean
Pop-Location
```

The exact toolchain is in `lean-toolchain`; the mathlib revision is in
`lake-manifest.json`. Do not run `lake update` in a release build because it
can change the dependency graph.

`formal/LEAN-COVERAGE.md` is the governing gap analysis. The count of compiled
supporting declarations is 61, while the count of **fully covered TeX theorems
remains zero**. Consequently these phrases are false:

- "the paper is 100% Lean verified";
- "all theorems are machine checked";
- "the numerical certificates are checked by Lean".

CI now performs the pinned build with Lean's official action, uses `nanoda`
with `nanoda-allow-sorry: false`, and emits the axiom report. The coverage
ledger maps every declaration to its exact manuscript fragment; static text
search is retained only as a second guard, not as the kernel audit.

## Minimum release manifest

Archive these together, with SHA-256 hashes generated from the release commit:

- the TeX source and rendered PDF;
- the two zero files;
- all three Arb scripts named above;
- stdout/stderr and exit status from the full zero, density, and monotonicity runs;
- Python, FLINT/Arb, Tectonic, Lean, and mathlib versions;
- the Lean build log and axiom report;
- the four finite-sieve sources, compiler version/flags, and output logs;
- a statement of GRH, NCZ, LI, and point-process hypotheses;
- the generative-AI disclosure and a revision-specific independent-review log.

Until this manifest can be regenerated from a clean checkout, the repository
is a development record, not an archival reproducibility package.
