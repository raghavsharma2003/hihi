# Submission-readiness audit

## Verdict

The manuscript is **not ready today for a prestige-journal submission**, and
it is not close to "100% Lean verified." It is, however, a substantially more
serious paper than the earlier numerical draft: it now has five coherent
headline blocks (interpolation, fixed-character dissolution, joint uniform
dissolution, critical zero-process transfer, and large-weight monotonicity),
explicit assumptions, certified zero lists, and a completed but deliberately
narrow Lean algebra layer.

The biggest risk is no longer that a named theorem disappeared. The biggest
risk is that the manuscript's breadth outruns the depth of independent
verification. A long AI-assisted proof can contain one subtle gap that survives
many internal passes. The only responsible route is to make every trust
boundary visible and obtain external expert review before making prestige or
"bulletproof" claims.

On a ten-point scale, the mathematical package is plausibly in the **7.5--8.0
range if the current proofs and Arb reductions survive independent review**.
Its present submission readiness is lower because external review and a
locked reproduction environment are missing. The density certificate has now
been repaired, rerun in all fourteen cases, re-audited by a second internal AI
agent, and reconciled with the manuscript.
A 9.5 rating cannot be manufactured by additional exposition or more decimal
places.

## Hard blockers

Every item in this table must be closed before submission.

| Gate | Current status | Required evidence to close |
|---|---|---|
| Independent proof audit | Internal/AI adversarial passes only | An analytic number theorist checks every headline statement, hypothesis, interchange of limits/sums/integrals, uniform constant, and cited input from first principles; corrections are logged |
| Density-method consistency | **Closed internally:** both implementation defects were repaired; all 14 cases reran successfully; a second internal AI-agent audit accepted the repairs; TeX and result file are synchronized | Preserve exact source/output hashes and obtain external replication before publication |
| Clean release build | **Closed internally:** final automatic build, log scan, 66-page visual inspection, synchronized PDF copies, and SHA-256 manifest completed | Rebuild from a clean checkout in release CI before public submission |
| Reproducible environment | Python verification packages and Lean/mathlib are pinned; Lean CI exists. Tectonic bundle, C compiler, and full Python certificate CI are not yet independently exercised | Add clean CI for the Arb and finite-sieve checks; archive compiler/tool hashes and logs |
| Formal-verification claim | **Narrow layers complete:** 61 supporting declarations compile; clean pinned builds and axiom audits pass; no full TeX theorem is covered | Keep every claim at declaration/fragment granularity; never call the paper fully Lean-verified |
| External numerical replication | Same repository and zero data drive the main computations | A second implementation by another person, preferably in a different language/library, independently reconstructs at least zero counts, selected density intervals, and monotonicity margins |
| Literature/priority audit | Recent close work is now cited, but priority language remains inherently fragile | A specialist confirms the search and the final novelty wording; use "we have not located" rather than categorical "first" claims |
| Archival package | **Partially closed:** synchronized local manifest and certificate transcripts exist; legacy instructions are marked superseded | Choose a license, add clean finite-sieve/CI logs, create a release tag, and synchronize the public archive |

## Major but nonfatal issues

1. **The critical theorem is a transfer principle, not yet a family theorem.**
   It assumes microscopic zero-process convergence and reciprocal-square tail
   tightness. Proving those hypotheses in a natural function-field or
   Dirichlet-character family would be a genuine flagship advance.

2. **The 66-page breadth is a referee risk.** Each new theorem creates another
   place where uniformity, parity, endpoints, or a hidden dependence on the
   conductor can fail. If an expert cannot audit it as one paper, split the
   analytic theorem paper from the computational/certificate companion.

3. **The numerical and theorem layers have different trust bases.** A rerun of
   an Arb program supports the implemented inequalities. It does not validate
   the manuscript lemma that reduces the theorem to those inequalities.

4. **The finite sieves are not globally "exact."** Integer-weight differences
   use `__int128`, but measures and fractional weights use floating point, and
   neither the sieve nor overflow safety is formally verified.

5. **The Lean supplement is useful but easy to oversell.** Its 61 supporting
declarations (34 algebraic and 27 exact post-processing) compile and pass axiom
audits, but zero complete TeX theorems are covered. They do not verify the
explicit formula, limiting laws, Bessel/Fourier analysis, or the analytic
source intervals behind the numerical certificates.

6. **The old publishing playbook is stale.** It is now marked prominently as
   legacy/superseded and must not be treated as authorization to upload, email,
   or advertise this version. Submission/public release is a separate decision
   after the hard blockers close.

7. **The corrected variance-shift threshold is now synchronized.** The
   executable assertion, docstring, comment, and TeX all use `4.3e-6` for the
   observed worst shift of about `4.23e-6`.

## First-principles referee checklist

The reviewer should sign off on each line, with a page/lemma reference and a
short reason. "Looks standard" is not enough for a load-bearing step.

### Arithmetic bridge

- The truncated explicit formula has the stated endpoint convention, parity,
  trivial-zero terms, and uniform error for every allowed `m`.
- Prime-power separation produces exactly the bias constant and remainder used
  in both logged and unlogged races.
- NCZ is used precisely where claimed; the unconditional arguments for
  `q=3,4` do not silently generalize to arbitrary real characters.
- Every Hadamard-product differentiation is justified by local uniform
  convergence, multiplicities are retained, and central zeros are handled.
- Every `O`, `asymp`, "absolute," "effective," and "uniform" has the correct
  quantifier order and parameter dependence.

### Probability and Fourier layer

- The random cosine series converges in the stated mode and its characteristic
  product is justified before Fourier inversion is invoked.
- LI is used only for the arithmetic-to-independent-phase bridge and is stated
  wherever a model probability is called a logarithmic race density.
- Absolute continuity, full support, boundary probabilities, and continuity in
  `m` are proved with domination tight enough for the stated domain.
- Every Taylor expansion of `log J_0` has the claimed sign, domain, and explicit
  remainder; all small- and large-`t` regions cover the whole integral with no
  gap or overlap dependency.
- The second- and third-order coefficients follow from a quantitative remainder
  at the required uniform scale, not only from formal power-series algebra.

### Joint and critical regimes

- The uniform Riemann--von Mangoldt estimate has constants independent of
  character, conductor, parity, `M`, and the chosen window wherever claimed.
- The `delta_0` degradation is tracked through all small-variance and
  large-`t` estimates.
- Weighted vague convergence handles repeated atoms, a possible limit atom at
  zero, compact-boundary atoms, and the reciprocal-square tails.
- Convergence of the critical density follows from a proved zero boundary mass;
  the non-Gaussian cumulant passage is justified in `L^4`.
- The conjectural random-matrix family law is visually and verbally separated
  from the deterministic transfer theorem.

### Computer-assisted monotonicity

- Every analytic inequality consumed by the script is proved on its complete
  domain, including Bessel envelopes and zero-count bounds.
- Every interval endpoint is outward-rounded; SciPy values are seeds only;
  interval Newton proves the stated uniqueness and no relevant extremum is
  skipped.
- The 285 finite cells cover the exact ranges without gaps, and the `M=300`
  bridge overlaps the analytic leg.
- Zero completeness exceeds every ordinate cutoff used by every cell.
- An independent implementation reproduces the worst margins with the same or
  stronger intervals.

### Density enclosures

- The complex-step derivative remainder for `sigma^2` follows from a valid
  holomorphic Cauchy bound over the entire disk used.
- The Gauss--Legendre nodes, weights, derivative bound, and exact remainder
  constant imply the implemented composite-quadrature radius.
- Interval subdivision encloses the unseen-tail modeling error rather than
  estimating it from sampled smoothness.
- The global Bessel envelope and chosen factors rigorously bound the entire
  infinite-`t` tail.
- All finite-product rounding, zero-ball uncertainty, and division by `pi` are
  included before decimal endpoints are directed outward.
- The two daggered six-decimal cases remain daggered if their final intervals
  straddle the rounding boundary.

## Lean gate: what would count

The formal supplement may be advertised only at the granularity actually
compiled. Before release:

- perform a clean build using the pinned `lean-toolchain` and
  `lake-manifest.json`;
- reject `sorry`, `admit`, `unsafe` proof oracles, and project-specific axioms;
- record `#print axioms` for each exported declaration;
- map each Lean theorem to the exact TeX equation or lemma fragment;
- label abstract zero-sequence results as abstract until a theorem connects
  them to the actual `DirichletCharacter.LFunction`;
- treat Arb/Python output as untrusted until a Lean-proved checker consumes an
  exact rational certificate.

Full paper formalization is a separate research-software project, likely
measured in person-years. GRH and LI can remain explicit hypotheses in a fully
formal conditional implication; they must not be introduced as hidden project
axioms. Literature priority and authorship disclosures are not propositions
Lean can verify.

## What would materially raise the paper toward 9.5

The highest-value paths are mathematical, not cosmetic:

1. Prove the critical point-process hypotheses for a natural function-field
   family and derive an actual family limit law.
2. Obtain effective convergence of weighted arithmetic races to their limiting
   laws, extending the recent quantitative unweighted framework.
3. Prove global monotonicity, or close a substantial part of the remaining
   bounded interval analytically rather than by a denser plot.
4. Turn the numerical programs into proof-producing certificate generators
   with a small independently verified checker, eventually Lean-checked.

Any one of the first two would change the paper's mathematical category. More
plots, more agents, a longer introduction, or additional sampled decimals will
not.

## Realistic publication route

After the blockers close, a journal such as *Journal of Number Theory* is a
realistic theory-first target; *Experimental Mathematics* is a strong fit if
the computational narrative and reproducibility package remain central.
*Mathematics of Computation* becomes plausible only after the numerical
enclosures and software trust story are independently rigorous. A top general
number-theory venue is not realistic on presentation alone.

The fastest credible sequence is:

1. freeze a release candidate and stop adding theorem scope;
2. archive the repaired density-certificate logs and synchronize code, TeX,
   and PDF;
3. obtain independent analytic and numerical reviews;
4. fix only issues found by those reviews;
5. rebuild, render, rerun, hash, and archive the release manifest;
6. post a clearly conditional preprint and submit to the chosen journal.

"ASAP" should mean removing avoidable delay, not skipping the only checks that
can distinguish a strong AI-assisted manuscript from a polished hallucination.
