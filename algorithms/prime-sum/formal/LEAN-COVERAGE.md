# Lean 4 verification coverage and feasibility audit

Audit date: 2026-08-16; live ledger updated 2026-08-17
Manuscript audited: `paper/weighted-races.tex` on branch
`codex/weighted-races-breakthrough` (base commit
`eed3942b4e43e4fe165cb58e4e89fad4cdf62e35`; the working copy was being edited
concurrently during the audit).

## Bottom line

**Initial compiled Lean coverage was exactly 0%.** At the start of the audit:

- `lean`, `lake`, and `elan` were not available on `PATH`;
- there was no `lakefile.toml`, `lean-toolchain`, or Lean source tree for this
  project;
- no theorem in the manuscript had a kernel-checked Lean proof.

That bootstrap state has now changed.  The project is pinned to Lean and
mathlib `v4.33.0`, and `lake build` completes successfully.  The module
`Formal.WeightedRaces` exports 34 compiled supporting theorems covering finite
amplitude/variance algebra, exact uniform-cosine moments, finite cumulant and
moment bounds, critical rescaling and one-zero threshold algebra, and the
rational coefficients in the third-order Edgeworth correction.  The full
axiom report is reproducible with `lake env lean Formal/Audit.lean`.

This does **not** make any complete TeX theorem Lean-verified: the analytic,
probabilistic-limit, arithmetic, Bessel, and certificate bridges listed below
remain open.  The current honest count is therefore 34 compiled support
theorems and 0 fully covered manuscript theorem items.

The manuscript contains mathematics that can ultimately be formalized, but
"100% Lean verified" is not an immediate polishing step. Mathlib already has
useful foundations for Dirichlet characters and their analytically continued
L-functions, complex analysis, infinite products, probability, characteristic
functions, infinite product probability spaces, and Levy convergence. It does
**not** currently provide the complete chain used by this manuscript:

- a Dirichlet-L explicit formula with the stated uniform truncation error;
- Riemann--von Mangoldt zero counting with the required uniform/explicit
  constants;
- the prime number theorem with the classical
  `exp(-c sqrt(log x))` error used in prime-power separation;
- the Akbary--Ng--Shahabi limiting-distribution theorem;
- Bessel `J_0`, `J_1`, their product/zero theory, and the explicit inequalities
  used here;
- a Lean-checkable bridge from the Arb zero and monotonicity certificates to
  the exact mathematical propositions in the paper.

Accordingly, an honest full formalization is a substantial research software
project, probably measured in person-years rather than days. The best first
formal target is the **abstract probability/zero-process layer**, especially
Theorem `thm:critical-transfer`, followed by the dissolution expansion. The
arithmetic bridge to actual Dirichlet L-functions is the longest critical path.

## Meaning of “100% Lean verified” in this project

A conditional theorem can be completely Lean-verified **as an implication**.
For example, Lean may prove

```text
GRH chi -> LinearIndependentOrdinates chi -> NCZ chi -> conclusion
```

without proving GRH or LI. That is not cheating, because GRH and LI are stated
hypotheses of the paper. They must be explicit parameters of the theorem, not
global `axiom` declarations.

A non-cheating certificate requires all of the following:

1. The theorem is stated using the actual `DirichletCharacter.LFunction` (or a
   definition proved equivalent to it), not only an abstract sequence called
   “the zeros.”
2. Any abstract probability theorem is connected to the arithmetic theorem by
   a separately proved bridge theorem.
3. No `sorry`, `admit`, `by_contra` followed by an oracle, user-declared
   `axiom`, or opaque theorem imported solely to assert a missing paper result.
4. `#print axioms` is recorded for every exported theorem. Standard logical
   principles already used by mathlib (for example classical choice and
   quotient soundness) are acceptable; any project-specific axiom is not.
5. Numerical claims are discharged from exact rational/integer certificates
   whose checker is proved correct in Lean. Calling Arb, Python, C, or an FFI
   and trusting its Boolean result is not a Lean proof.
6. CI pins exact Lean and mathlib revisions, rejects `sorry`, rebuilds from a
   clean checkout, and stores certificate hashes.
7. The formal statement is checked line-by-line against the TeX statement.
   Proving a weakened or abstract surrogate does not count as covering the TeX
   theorem.

Literature-priority claims (“first,” “no prior treatment”), authorship
disclosures, and empirical statements about Monte Carlo are not mathematical
propositions that Lean can establish. They require source review or
reproducibility evidence and should never be labelled Lean-verified.

## Mathlib capability snapshot

The audit used current official mathlib documentation. These are available:

- `Mathlib.NumberTheory.DirichletCharacter.*` for Dirichlet characters.
- `Mathlib.NumberTheory.LSeries.DirichletContinuation` for analytic
  continuation, completed L-functions, differentiability, and the primitive
  functional equation.
- `Mathlib.NumberTheory.LSeries.Nonvanishing` for nonvanishing on
  `Re(s) >= 1`.
- `Mathlib.NumberTheory.AbelSummation` for summation by parts.
- `Mathlib.NumberTheory.VonMangoldt` and
  `Mathlib.NumberTheory.LSeries.PrimesInAP` for von Mangoldt functions and
  Dirichlet's theorem in arithmetic progressions.
- `Mathlib.MeasureTheory.Measure.LevyConvergence` for Levy's continuity
  theorem.
- `Mathlib.Probability.Independence.CharacteristicFunction` and
  `Mathlib.Probability.Independence.InfinitePi` for characteristic functions
  and independent coordinate families.
- Gamma/digamma, Taylor series, improper integration, Gaussian integrals,
  asymptotics, meromorphic functions, and broad complex-analysis support.

Important gaps or uncertain areas that must be treated as absent until an
exact declaration is located and compiled:

- Bessel functions and the specific `J_0`/`J_1` API used by the manuscript;
- Perron inversion in the required number-theoretic form;
- the Riemann--von Mangoldt formula for Dirichlet L-functions;
- a Dirichlet-character PNT with the explicit error used here;
- Hadamard factorization specialized to completed Dirichlet L-functions and
  an enumeration of their zeros with multiplicity;
- Gil--Pelaez inversion in the exact form used;
- the cited ANS limiting-distribution framework;
- vague convergence of locally finite point measures in a directly reusable
  form.

Generic infrastructure may exist for parts of several gaps (for example
complex Hadamard theory and weak convergence), but “generic infrastructure” is
not the specialized theorem needed by this manuscript.

Official documentation checked:

- <https://leanprover-community.github.io/mathlib4_docs/Mathlib/NumberTheory/LSeries/DirichletContinuation.html>
- <https://leanprover-community.github.io/mathlib4_docs/Mathlib/MeasureTheory/Measure/LevyConvergence.html>
- <https://leanprover-community.github.io/mathlib4_docs/Mathlib/Probability/Independence/InfinitePi.html>
- <https://leanprover-community.github.io/mathlib4_docs/Mathlib/NumberTheory/AbelSummation.html>
- <https://leanprover-community.github.io/mathlib4_docs/Mathlib/NumberTheory/LSeries/PrimesInAP.html>

## Definitions that must be frozen before proving anything

These definitions are not bookkeeping. Ambiguity here can make a formally
proved theorem differ from the paper.

### Arithmetic layer

- `RealPrimitiveCharacter q`: a nontrivial primitive Dirichlet character with
  values in `{0, 1, -1}` (with the exact coercion to complex characters proved).
- completed L-function `Lambda chi s`, its parity and normalization, matched to
  the paper's `(q/pi)^((s+a)/2) Gamma((s+a)/2) L(s,chi)`.
- nontrivial zeros, including multiplicity, and positive ordinates.
- `GRH chi`: every nontrivial zero has real part `1/2`.
- `NCZ chi`: `LFunction chi (1/2) != 0`.
- `LI chi`: rational linear independence of the **distinct positive
  ordinates**. The multiplicity convention must be explicit: LI forces
  simplicity if it is instead imposed on a multiset.
- weighted prime and von-Mangoldt sums, with exact endpoint conventions.
- logarithmic density and limiting distribution, including the change of
  variables `x = exp u` and the irrelevance of a finite initial interval.

### Probability layer

- probability space `Omega = (circle)^Nat` with product Haar measure;
- independent uniform phases and coordinate cosines;
- amplitude `a gamma M = 2*M / sqrt(M^2 + gamma^2)`;
- partial sums, their `L2` limit, `X = 1 + V`, variance, moments, and
  characteristic functions;
- two separate names for `modelDensity chi m = P(X > 0)` and
  `raceLogDensity chi m`. They coincide only after the interpolation/LI bridge.
  The TeX presently overloads `delta_chi`/`delta_q`, which Lean should not do.

### Point-process layer

- locally finite counting measures on `[0,infinity)`, with multiplicity;
- vague convergence as convergence against continuous compactly supported
  functions;
- reciprocal-square tail tightness;
- the weighted random series associated to a point measure.

## Dependency graph

```text
Dirichlet character + completed L-function
        |
        +--> explicit formula --> shifted formula --> prime-power separation
        |        |                                      |
        |        +--> ANS/Besicovitch limiting law ------+--> interpolation
        |                                                  +--> unlogged transfer
        |
        +--> zeros/Hadamard --> variance identity --> S4/S6 identities
        |                         |                 +--> dissolution expansions
        |                         +--> variance asymptotic +--> joint theorem
        |
        +--> Riemann--von Mangoldt --> zero windows --> Fourier tails
        |                                  |              +--> dissolution/joint
        |                                  +--> monotonicity tails
        |
        +--> explicit zero-count bounds --> analytic monotonicity leg

Independent probability route:
square-summable amplitudes --> random series --> characteristic products
   --> Levy/Portmanteau --> critical zero-process transfer
   --> Bessel inversion/differentiation --> monotonicity criterion

Finite certificates:
zero enclosures + completeness --> exact Bessel/rational bounds
   --> cellwise MAIN > TAIL --> explicit q=3,4 monotonicity thresholds
```

## Theorem-by-theorem coverage map

Difficulty scale:

- **S**: small once definitions exist (days to two weeks).
- **M**: substantial but supported by mathlib (weeks).
- **L**: major new library development (months).
- **XL**: research-scale formalization or several large upstream results.

Every full TeX item in the tables below currently has status **UNFORMALIZED**;
the 34 compiled declarations discharge only supporting algebraic obligations.

### Interpolation and the arithmetic-to-probability bridge

| TeX item | Main prerequisites | Existing support | Missing proof work | Difficulty | Non-cheating completion condition |
|---|---|---|---|---:|---|
| `lem:classical`, truncated explicit formula | Perron kernel; `-L'/L` Dirichlet series; contour shift; residues at nontrivial/trivial zeros; local log-derivative bound; Riemann--von Mangoldt short-interval bound | L-function continuation, functional equation, meromorphic and contour foundations | Nearly the entire specialized explicit-formula argument, zero enumeration with multiplicity, horizontal/vertical estimates, parity at zero, all uniform constants | XL | Lean theorem about the actual weighted von-Mangoldt sum and actual zeros of `DirichletCharacter.LFunction`, valid for every `x,T` in the stated ranges |
| `lem:trunc`, shifted formula | `lem:classical`; Stieltjes/Abel summation; summability of endpoint terms | Abel summation and integration | Bridge the paper's step functions/Stieltjes integral to mathlib, formalize complex powers and all `O_{m,chi}` estimates | L after `lem:classical` | Exact theorem with the same floor `(1+x^m) log x`; no stronger hidden restriction such as `T <= x` |
| `lem:squares`, prime-power separation | prime-power decomposition of von Mangoldt; PNT with `exp(-c sqrt(log x))`; partial summation | von Mangoldt definitions, prime-power facts, Abel summation | Classical PNT error at the strength used; all uniform case splits for negative `m`; endpoint conventions | XL | Both displays, including the `log^2 x` exceptional range, proved for the manuscript definitions |
| `thm:interp` (i), limiting distribution | preceding two lemmas; Besicovitch `B^2` almost periodicity/ANS theorem; zero counts | general measure/probability tools | Formalize the ANS theorem or prove the needed special case; verify its error hypothesis from the explicit formula | XL | Limiting distribution of the actual normalized race; an abstract theorem for a supplied frequency sequence is only an intermediate result |
| `thm:interp` (ii), random law, absolute continuity, full support, strict bias, continuity | LI/Kronecker--Weyl bridge; infinite independent phases; arcsine law; divergent `sum 1/gamma`; Levy/Portmanteau | infinite product spaces, independence, char functions, Levy convergence, convolution/absolute continuity tools | Formal arcsine component, full-support block argument, RvM-based divergence, and actual LI-to-random-law bridge | L/XL | Every clause proved; especially `raceLogDensity = modelDensity`, support `R`, and continuity on the whole open interval |
| `thm:interp` (iii), Chebyshev and Chernoff bounds | square-summable independent cosines; `I0(x) <= exp(x^2/4)` | probability inequalities, series, exponential | Define/prove modified-Bessel MGF or prove the integral inequality directly; pass finite Chernoff bounds to the `L2` limit | M | Symbolic bounds with `C(chi)=sum 2/gamma^2`; numerical constants are separate certificates |
| `thm:interp` (iv), endpoint synthesis | parts (i)--(iii) plus external results RS94, AK23, Sheth24, Hay25, FM13 | none of those paper-specific theorems | Formalize every imported endpoint theorem, or rewrite this clause explicitly as a literature comparison rather than an internally proved theorem | XL | No citation-only theorem is counted as Lean coverage |
| `cor:mod3rate` | interpolation (iii); certified value of `C(chi_3)` | real arithmetic | identify `chi_3`; prove NCZ; certify derivative/series evaluation and decimal thresholds | L | Rational intervals implying every printed decimal and threshold, checked in Lean |
| `prop:unlogged` | shifted explicit formula; prime-power separation; partial summation; negligible-error transfer of limiting laws | Abel summation, asymptotics | exact normalization, zero-term summability, Cesaro-negligibility of every remainder | L/XL | Same limiting measure for actual logged and unlogged races, not merely matching formal series |

### Variance and moment identities

| TeX item | Main prerequisites | Existing support | Missing proof work | Difficulty | Non-cheating completion condition |
|---|---|---|---|---:|---|
| `prop:varid` | completed L functional equation; genus-zero Hadamard product under GRH; logarithmic derivative | completed L-function and functional equation; generic complex analysis | order/growth of completed Dirichlet L, zero multiset, specialized Hadamard factorization and legal termwise differentiation | XL | Identity derived from the actual completed L-function; taking the partial-fraction identity as an assumption does not cover this proposition |
| `cor:Cexact` | variance identity at `M=0`; trigamma identity; Catalan constant; certified L-derivative value | Gamma/digamma basics | boundary limit, trigamma identity `psi'(3/4)=pi^2-8G`, exact definition of Catalan constant, certified numerical interval | L | symbolic equality plus Lean-proved rational enclosure containing every printed decimal |
| `prop:varasymp` | variance identity; Stirling bounds for digamma; exponentially small Dirichlet series | Gamma/digamma and asymptotic framework | explicit uniform remainder through `1/(12M)`; parity normalization; uniform-in-`q` coefficient bounds | L | Both q=4 and general-character displays, with exact meaning of the absolute `O` constant |
| `lem:S4mom` | differentiated partial fractions/log derivatives; variance asymptotic | calculus and series | second/third log derivatives, justified termwise differentiation, asymptotic and global moment inequalities | M/L after `prop:varid` | S4 and S6 closed forms, asymptotic, and inequalities all checked; no numerical differentiation |

### Bessel/Fourier layer and fixed-q dissolution

| TeX item | Main prerequisites | Existing support | Missing proof work | Difficulty | Non-cheating completion condition |
|---|---|---|---|---:|---|
| `lem:J0facts` (J1--J5) | definition of `J0`; integral representation; asymptotics; Taylor/log remainders | general power series, integrals, Taylor | build Bessel `J0`; prove strict modulus, global `z^-1/2` bound, positivity, and explicit rational remainders through degree 8 | L | All five inequalities proved for their complete stated domains with exact rational constants |
| `lem:window` | fixed-q Riemann--von Mangoldt | none specialized | RvM and extraction of an effective threshold | XL/L | Lean constructs or proves existence of computable `M0(q)` and the displayed lower bound |
| `lem:invert` | random series; Bessel characteristic factor; Fourier inversion/Gil--Pelaez | finite independent char-function products, Fourier/measure theory | infinite-product convergence, integrable char-function inversion at threshold `-1` | M/L | Absolute convergence and the exact `1/pi` formula, including sign convention, are kernel checked |
| `lem:bigt` | Bessel global bounds; zero window | general integration | product decay split into finite and infinite ranges with constants 17 and exponent | M after prerequisites | Exact integral bound, not only asymptotic decay |
| `thm:dissolution` | inversion; small-t log expansion; Gaussian moments; S4 bounds; superexponential tail | Gaussian integrals/Taylor/asymptotics | rigorous remainder bookkeeping for first and second order, all `O_q` dependencies | L after prerequisites | All three parts and exact coefficients `-1/6`, `-3/64` proved |
| `cor:dissolution-race` | interpolation bridge plus dissolution | none beyond parents | compose the two formal theorems | S after parents | Lean equality of race and model densities under LI |
| `cor:secondorder` | dissolution plus variance/S4 asymptotics | asymptotic algebra | controlled substitution of asymptotic expansions | S/M after parents | exact `-11/24` coefficient with the stated error scale |

### Joint uniform theorem

| TeX item | Main prerequisites | Existing support | Missing proof work | Difficulty | Non-cheating completion condition |
|---|---|---|---|---:|---|
| `lem:rvm-joint` | uniform explicit RvM for primitive characters | no specialized theorem located | formalize a source with absolute constants, including symmetry and exclusion of zero ordinate | XL | Absolute constants exist in Lean and are independent of `q,chi,T` as stated |
| `lem:window-joint` | uniform RvM | elementary inequalities | choose an explicit `A1`, prove both the count and amplitude bound in all small/large `M` cases | M after RvM | An actual natural/rational `A1`, not an opaque existential backed by a citation |
| `lem:rho-rate` | strict Bessel bound and local Taylor control | none for Bessel | compactness plus explicit small-argument lower bound | M after `J0` | Positive explicit or constructively extractable `kappa` |
| `lem:bigt-joint` | joint window, Bessel rate, sigma comparison | integration | all delta dependence and exponential-to-polynomial conversions | M/L | `C11(delta)<=C/delta` and absolute `c10` proved, not suppressed in notation |
| `prop:sigcomp` | zero counts and partial summation | Abel summation/integration | Stieltjes sum identities and uniform constants in head/tail split | M/L after RvM | upper/lower comparisons and Lindeberg ratio exactly as stated |
| `thm:joint` (i)--(ii) | all preceding Bessel/joint lemmas; Gaussian moments | Taylor/Gaussian foundations | uniform small-sigma and large-sigma case handling; exponential tails; explicit dependence on `delta0` | L | inequalities for every admissible pair, including small sigma; no asymptotic-only surrogate |
| `thm:joint` (iii) | eighth-order Bessel-log remainder; cross-term bookkeeping | Taylor and integrals | prove the displayed seven retained terms and bound every omitted term; certify `delta0^-8` degradation | L | exact seven coefficients and `G/sigma^6` remainder checked from a formal remainder lemma |
| `cor:joint-asymp` | joint (i), sigma comparison | asymptotic algebra | equivalence of growth conditions in every aspect | S/M | all three aspect statements formalized with correct filters |
| `cor:joint-second` | joint (ii), uniform Stirling and Dirichlet-series errors | asymptotic algebra | uniform substitutions under `M>=16`, `L>=2` | M | same absolute constant works over the whole stated region |

### Critical zero-process theorem

| TeX item | Main prerequisites | Existing support | Missing proof work | Difficulty | Non-cheating completion condition |
|---|---|---|---|---:|---|
| `thm:critical-transfer` (i) | locally finite point measures; vague convergence; weighted `l2` random series; char functions; Levy | Levy theorem and infinite product probability spaces | counting-measure configuration matching on compacts; reciprocal-square tail transfer; convergence of infinite random series/products | M/L | Actual theorem for counting measures with multiplicity, including possible limit atom at zero |
| `thm:critical-transfer` (ii) | same plus moment/variance interchange | integration and `L2` tools | compact-plus-tail convergence for squared amplitudes | M | product, variance formula, and variance convergence all proved |
| `thm:critical-transfer` (iii) | weak convergence; absence of atom at zero; interpolation bridge only for race interpretation | Portmanteau/Levy | scaled arcsine absolute continuity and boundary-set argument | M | model density convergence proved unconditionally on the theorem hypotheses; race-density sentence separately depends on formalized LI bridge |
| `thm:critical-transfer` (iv) | fourth moments/cumulants of infinite independent sums | moments and independence foundations | convergence of fourth moments/cumulants; rule out Gaussian via fourth cumulant | M | negative cumulant derived, with finite sum/infinite-limit justification; `mu=0` branch proved |

This is the most independent major result. A fully formal **abstract** version can
be valuable early. It still does not verify the arithmetic claim until
`mu_n` is proved to be the scaled zero-counting measure of the actual completed
Dirichlet L-function and `X_{m_n,chi_n}` is connected to that enumeration.

### Monotonicity and the computer-assisted theorem

| TeX item | Main prerequisites | Existing support | Missing proof work | Difficulty | Non-cheating completion condition |
|---|---|---|---|---:|---|
| `lem:phi` | Hadamard product for `J0`, Bessel zeros, Rayleigh sums | no reusable Bessel-zero API located | construct zeros/order; product; positive log-series coefficients; exact bounds and `j01>2.4` | L | all domains and decimal/rational constants certified |
| `lem:J0env` | Bessel differential identities, alternating/asymptotic bounds, zeros of `J1` | general calculus only | define `J1`; prove derivative identities, monotonic energy, global `0.446` and `0.733` bounds, critical-point maximum rule | L | the suprema are mathematical bounds in Lean, not imported floating-point evaluations |
| `lem:binet` | digamma/trigamma integral or series bounds | digamma exists | prove both two-sided explicit inequalities | M | exact rational coefficients for every `x>0` |
| `lem:Nplus` | variance identity; Binet; nonvanishing Dirichlet series bounds | L-function nonvanishing at `Re>=1`, log/digamma | formal zero-count conversion and all constants, including `0.57` | L/XL | exact theorem over actual zero count for every `T>=3/2` |
| `lem:Nall` | joint uniform zero-count upper bound | elementary order facts after `lem:rvm-joint` | handle `0<T<1` by monotonicity and preserve a single absolute constant across both parities | S after RvM | exact all-parity bound for every `T>0`; it inherits, and therefore cannot outrun, the formal status of `lem:rvm-joint` |
| `lem:Nlow` | S4/variance closed forms and termwise comparisons | elementary sums after bridge | derive count inequality; prove explicit `q=3,4`, `Y>=20` simplification | M/L | both exact and explicit lower counts checked |
| `lem:Dprop` | differentiated variance series; closed L-function forms; Binet bounds | calculus/series | termwise derivatives, positivity, logarithmic Lipschitz bound, q=3/4 explicit constants | L | all three parts including `3.1`, `8/M`, and `100` |
| `lem:diffint` | differentiated infinite Bessel product; zero count; integrable dominance | differentiation/integration frameworks | uniform convergence of log derivatives; product rule with a removed factor; global dominant; parameter differentiation under integral | L | exact derivative formula and all bounds, not an informal “standard theorem” invocation |
| `lem:negstruct` | positive Bessel log derivative; Gaussian lower envelope | elementary integration/erf | exact `0.9973`, `1088`, and closed integral | M | rational comparisons and erf identity proved |
| `lem:tailexp` | per-cell Bessel suprema; zero counts; improper power-log integrals | finite products/integration | formal maximum/sorting argument, all cutoff cases, tail integral | M/L | criterion accepts exact rational certificate data; no floating-point `sup` oracle |
| `thm:monotone-large` | all preceding monotonicity lemmas plus asymptotics | asymptotic framework | turn eventual comparisons and constants `0.18`, `[0.90,1.14]` into explicit effective thresholds | L/XL | Lean proves existence/effectivity and strict derivative sign for the model density |
| `prop:criterion-eval` | analytic criterion plus zero/completeness/Bessel cell certificates | integer/rational normalization | replace Arb trust with a proof-producing certificate format and verified checker; certify all zero enclosures and completeness | XL | Lean checks every interval, special-function enclosure, list count, cutoff, and strict margin from exact serialized data |
| `lem:analytic-leg` | explicit counts and bounds; real transcendental inequalities on `[300,infinity)` | calculus and real arithmetic | prove endpoint ratios and global logarithmic-derivative signs `<=-0.14,-0.08` | L | exact rational inequalities imply the whole infinite interval, not sampled points |
| `cor:monotone-explicit` | finite certificate to 300 plus analytic leg thereafter | composition | join closed intervals with no gaps; convert `M=m+1/2`; LI bridge for race interpretation | S after very hard parents | exact thresholds `16.82`, `18.62` proved; certificate hashes recorded |

## Numerical and computational claims outside the theorem environments

These cannot be called Lean-verified merely because the analytic theorems are
formalized.

### Zero lists

For each q=3,4 list, Lean must verify:

1. every stored interval contains a zero of the actual completed L-function;
2. the interval contains the claimed multiplicity (normally exactly one);
3. intervals are ordered, positive, and disjoint;
4. no zero is missing up to the claimed completeness height;
5. the serialized certificate and source zero file hashes match.

The present Arb procedure is independent evidence, not a Lean proof. A
non-cheating route is a rational interval/argument-principle certificate with a
Lean theorem proving the checker sound. Simply importing decimal ordinates as
hypotheses is not acceptable.

### Density table

The fourteen printed density intervals are now externally enclosed by the
repaired Arb verifier.  It proves a finite Bessel-product enclosure, an
explicit Gauss--Legendre remainder, the unseen-product replacement error, an
analytic infinite tail, and outward decimal rounding.  The verifier was rerun
for all fourteen cases after an internal adversarial AI-agent audit found and prompted repairs
to its adaptive-sum bookkeeping and decimal formatter.  This is strong
external interval evidence conditional on GRH, LI, the certified zero-list
completeness, and the manuscript's analytic reduction; it is **not** a Lean
proof.  Lean certification still requires the following chain:

1. finite Bessel-product enclosure on every integration cell;
2. rigorous quadrature error (or a proof-producing interval integrator);
3. rigorous unseen-zero tail replacement error;
4. rigorous infinite integration tail;
5. exact rounding lemmas for each printed digit;
6. a proved parser/checker for the exported interval certificate and hashes.

Monte Carlo can remain a reproducibility cross-check, never a proof input.

### Monotonicity Arb run

The Arb run establishes strong evidence if its implementation and inputs are
correct. For Lean coverage, export a compact certificate containing rational
interval endpoints and the rational bounds needed on each cell. Lean must prove
the special-function enclosure scheme once and then reduce each cell to exact
rational inequalities. The Python script should become a **certificate
generator**, not a trusted verifier.

### Exact sieves to `10^10`

Formal verification needs:

- a Lean specification of lead changes and finite logarithmic measure;
- a proved-correct segmented sieve/accumulator algorithm or a proof certificate
  independently checked by Lean;
- proof of absence of overflow and of exact endpoint conventions;
- exact result hashes.

Re-running the C program is reproducibility, not formal verification.

## First-principles audit gates

Before a TeX theorem receives a “Lean verified” badge, all gates below must be
green.

### Statement gate

- exact hypotheses, quantifier order, parameter ranges, parity, and endpoint
  conventions match TeX;
- every occurrence of `O`, `asymp`, “effective,” and “uniform” is expanded into
  explicit quantifiers in Lean;
- the model density and the logarithmic race density are not conflated;
- multiplicities of zeros are preserved;
- every printed decimal used in a theorem is implied by a rational interval.

### Proof gate

- no `sorry`, `admit`, or project axiom;
- no theorem whose only hypothesis is the conclusion under another name;
- abstract zero-data theorems have an arithmetic bridge;
- every exchange of limit/sum/product/derivative/integral has a formal
  summability, domination, or uniform-convergence proof;
- every cited external mathematical theorem is either already in trusted
  mathlib under a matching statement or formalized locally.

### Build gate

- exact `lean-toolchain` and `lake-manifest.json` committed;
- clean `lake build` succeeds in CI;
- a script rejects `sorryAx`, `admit`, declarations named `axiom`, and
  unexpected `#print axioms` output;
- generated numerical certificates are immutable inputs with SHA-256 hashes;
- the report lists theorem names, source TeX labels, compiled module names, and
  axiom output.

## Recommended formalization order

The order below produces useful, honest milestones without pretending the
arithmetic bridge already exists.

1. **Bootstrap (several days).** Install/pin Lean and mathlib, add CI, define
   the trust policy, and create a machine-generated coverage report. This
   changes coverage from 0% only when an actual theorem compiles.
2. **Probability core (3--8 weeks).** Infinite uniform phases, square-summable
   cosine series, variance, absolute continuity, full support, Chernoff bound,
   characteristic products, and Levy/Portmanteau lemmas.
3. **Critical transfer (another 4--10 weeks).** Formalize
   `thm:critical-transfer` as an abstract counting-measure theorem. This is the
   shortest path to a complete formal proof of a headline original theorem.
4. **Bessel core and Fourier inversion (2--5 months).** Define `J0/J1`, prove
   J1--J5 and the inversion lemmas, then formalize dissolution and the
   third-order joint expansion at the abstract zero-sequence level.
5. **Dirichlet-L arithmetic bridge (6--18+ months).** Explicit formula,
   zero-counting, PNT error, completed-L Hadamard identities, ANS limiting law,
   and transfer to actual prime races. This is the main bottleneck and is large
   enough to merit upstream mathlib collaboration.
6. **Proof-producing numerics (3--9 months, parallelizable).** Rational
   certificate formats for Bessel bounds, zero isolation/completeness,
   monotonicity cells, density quadrature, and exact sieve outputs.
7. **Full paper closure.** Formalize or remove theorem-level reliance on
   external endpoint papers; reconcile every TeX claim with the compiled
   theorem ledger; have an independent Lean expert review both statements and
   the trust boundary.

These estimates are planning ranges, not promises. Parallel work can reduce
calendar time but not the amount of new mathematics and library engineering.

## Publication recommendation

Do **not** delay an ordinary conditional preprint until the entire project is
Lean-formalized, and do **not** claim “100% Lean verified” now. A credible staged
claim would be:

1. current submission: analytic paper plus rigorous external certificates,
   clearly separating certified and heuristic numerics;
2. formal supplement milestone A: kernel-checked abstract critical-transfer and
   dissolution theorems;
3. milestone B: kernel-checked arithmetic bridge to actual prime races;
4. milestone C: kernel-checked finite certificates and complete theorem ledger.

Even after milestone C, GRH and LI remain hypotheses. The correct phrase would
be “the conditional implications and stated numerical certificates are
formally verified in Lean 4,” not “the prime-race conclusions are
unconditionally proved.”

## Live coverage ledger

This table must be updated only from successful clean builds.

| Layer | Exported compiled theorems | TeX items fully covered | Status |
|---|---:|---:|---|
| Algebraic support layer | 34 | 0 | compiled and axiom-audited |
| Probability core | 0 | 0 | not started |
| Bessel/Fourier | 0 | 0 | not started |
| Critical transfer | 0 | 0 | not started |
| Dirichlet-L bridge | 0 | 0 | not started |
| Dissolution/joint theorem | 0 | 0 | not started |
| Monotonicity analytic proof | 0 | 0 | not started |
| Numerical certificate checker | 0 | 0 | not started |
| **Total** | **34 support theorems** | **0** | **bootstrap complete; no full TeX theorem yet** |

No future file, theorem name, or work estimate in this ledger is a proof. Only a
successful pinned Lean build and matching `#print axioms` audit may change the
last table.
