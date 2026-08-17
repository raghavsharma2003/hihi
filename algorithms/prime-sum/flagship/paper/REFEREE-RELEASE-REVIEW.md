# Hostile referee/editor release review

**Manuscript reviewed:** `main.tex` and all eight included section files in
the focused-paper tree, current snapshot on 2026-08-17.

**Editorial verdict:** **major revision; do not submit this snapshot.**

I did not find a mismatch in which the title or abstract promises a theorem
that the proof never addresses. The mathematical spine is unusually coherent:
one explicit pencil, one critical scaling, one outer random-measure limit, and
one scalar prime-race consequence. The paper is also commendably explicit
about the large-field limitation. But it is not release-ready. The scientific
statement is obscured by a theorem that bundles five logically different
outputs, central spaces and layers of randomness are not defined at first use,
the novelty contrast is too implicit for an editor, and the source uses a
mixed manual/automatic equation-numbering scheme that is unacceptable in a
journal submission. In addition, the two deepest imported arithmetic inputs
have not yet been checked against the exact source pages by a human expert.

This is a credible specialist paper after revision. It is not presently a
prestige-journal paper, a `9.5/10` paper, or a paper that should be advertised
as fully formally verified.

## 1. What the paper actually proves

For every fixed \(\lambda>0\), the manuscript considers the explicit pencil

\[
y^2=\prod_{a=1}^{2g}(x-a)(x-t)
\]

over odd square fields whose characteristic exceeds \(2g+1\). It first takes
the endpoint cutoff \(N\) to infinity for each fixed curve, obtaining a
genuine empirical law. It then lets the genus and field size grow together,
under

\[
\log Q_g/(g^2\log(g+2))\longrightarrow\infty,
\]

and proves convergence in distribution of the resulting random element of
\((\mathcal P_2(\mathbb R),W_2)\) to a conditional random-phase law marked by
the symplectic hard-edge determinantal process. It also proves that the random
conditional measure is nonconstant and absolutely continuous, and separately
that its mass on \((0,\infty)\) is nonconstant.

That statement matches the proof. The proof does **not** give a fixed-field
microscopic theorem, an optimal field-growth threshold, a result for the full
hyperelliptic ensemble, or end-to-end Lean verification. The current abstract
and scope paragraphs correctly disclaim all four.

## 2. Scorecard

| Criterion | Current score | Referee assessment |
|---|---:|---|
| One-result focus | 8/10 | The proof has one dependency chain, not a collection of unrelated results. |
| Main theorem clarity | 6/10 | Correct, but overloaded by secondary consequences and an explicit example. |
| Definitions before use | 5/10 | \(\mathcal P_2\), \(W_2\), the two randomness layers, \(W_{2g}\), and several local notations need earlier definitions. |
| Abstract/title fidelity | 8/10 | No substantive overpromise, but “quenched” should be in the title and “splitting-prime race” is imprecise. |
| Proof architecture | 8/10 | The arithmetic-to-Haar-to-hard-edge chain is visible and justified. |
| Length discipline | 9/10 | The rendered manuscript is 22 pages and has passed a separate visual-layout check; the remaining cuts are for clarity, not page count. |
| Novelty presentation | 5/10 | The paper says what it contributes but does not sharply distinguish quenched \(\mathcal P_2\)-valued convergence from antecedent scalar or annealed results. |
| Claim calibration | 9/10 | The large-field and formalization boundaries are honest. |
| Submission readiness | 4.5/10 | Exact-source, external-review, typography, metadata, and equation-numbering gates remain open. |
| Specialist-journal potential after revision | 7/10 | Credible for a solid specialist venue if the deep inputs survive human verification. |

## 3. Mandatory changes before external circulation

### M1. Check the deep imported results against the original sources

This is the only item that can still destroy the headline theorem rather than
merely improve exposition.

1. In `sections/03-transfer.tex`, lines 47--52 and 80--99, verify the exact
   hypotheses and conventions of Katz--Sarnak Theorem 10.1.16, Lemma 10.1.12,
   and the cited GOS theorem for this varying pencil, including tameness at
   every puncture and infinity, geometric versus arithmetic Frobenius, and
   the asserted full symplectic geometric monodromy.
2. In `sections/02-linear-independence.tex`, lines 41--62 and 69--103, verify
   Kowalski's relation-space statement, the large-sieve exponent, the erratum
   factor, and especially the uniformity of the constant as \(g\), the
   polynomial \(f_g\), and the characteristic all vary.
3. In `sections/04-hard-edge.tex`, lines 45--59, quote the exact version of
   Soshnikov's convergence criterion and state explicitly how local trace
   convergence plus the operator statement supplies every hypothesis.
4. Add a precise theorem or corollary locator for the Deligne weight estimate
   used in `sections/03-transfer.tex`, lines 92--97. A book/article-level
   citation is too coarse at the proof's quantitative bottleneck.

Internal AI audits are not a substitute for this check. At least one
arithmetic geometer should sign off on items 1--2 and one determinantal-process
expert on item 3 before the paper is posted as a serious preprint.

### M2. Refactor the headline into one theorem plus one corollary and one example

`sections/00-introduction.tex`, lines 84--118, currently puts all of the
following into a single theorem:

- random-measure convergence;
- nonconstancy and absolute continuity of the limiting measure;
- convergence and expectation convergence of half-line masses;
- identification with the natural race density with probability \(1-o(1)\);
- a particular least-prime sequence of fields.

This makes the central contribution harder, not stronger, to see. Retain one
named main theorem with only:

1. the field/genus assumptions;
2. the random-measure convergence;
3. nonconstancy and absolute continuity of the limiting random measure.

Immediately follow it by a `Corollary (prime-race densities)` containing the
half-line convergence, explicit expectation formula, nonconstancy of the
limiting scalar, and the high-probability natural-density identification.
Put the least-prime construction in an `Example (an explicit admissible
sequence)` or a short remark. This is still a paper with one main theorem; it
merely stops treating an example as part of that theorem.

The phrase “the expectations of the two sides converge” at lines 105--106 is
ambiguous. Replace it by the displayed statement

\[
\mathbb E_{t_g}\,\nu_{g,t_g,\lambda}((0,\infty))
\longrightarrow
\mathbb E\,\nu_\lambda(\Pi_{\rm Sp})((0,\infty)).
\]

Also make the theorem itself begin “For every fixed \(\lambda>0\)” rather
than relying on a declaration 54 lines earlier.

### M3. Define the state space and the two levels of randomness before the theorem

The main statement uses \(\mathcal P_2(\mathbb R)\) and \(W_2\), but the
manuscript never explicitly says that \(\mathcal P_2(\mathbb R)\) is the
space of Borel probability measures with finite second moment, equipped with
the quadratic Wasserstein metric. Add this definition before
`sections/00-introduction.tex`, line 57.

The central “quenched” distinction also needs one explicit paragraph:

- the phases \(\Phi\) are integrated out to form a conditional probability
  measure;
- the curve parameter \(t_g\), or in the limit the configuration
  \(\Pi_{\rm Sp}\), is the outer randomness that makes this measure-valued
  object random;
- \(\Longrightarrow\) denotes weak convergence of the outer laws on the
  Polish space \((\mathcal P_2,W_2)\).

Without this paragraph, even a number theorist can misread (1.7) as ordinary
convergence of annealed scalar distributions.

Definitions to move or add at first use:

- define \(W_{2g}\) as the signed-permutation Weyl group before
  `sections/02-linear-independence.tex`, line 35, not in the proof at line 99;
- define \(\Theta_{g,t}\) by an explicit characteristic-polynomial equation
  near `sections/03-transfer.tex`, lines 21--24;
- define \(d_G\) and \(d_{\rm conj}\) before the metric lemma in
  `sections/03-transfer.tex`, lines 122--132;
- identify \(\rho_2\) as the second correlation function before
  `sections/04-hard-edge.tex`, line 186;
- define \((n)_N=n(n-1)\cdots(n-N+1)\) before the factorial-moment formula at
  `sections/04-hard-edge.tex`, line 256;
- identify \(J_0\) as the Bessel function of the first kind of order zero at
  its first use, line 270.

### M4. Rewrite the novelty paragraph as a precise contrast

`sections/00-introduction.tex`, lines 131--149, is cautious but editorially
weak. It lists antecedents and then states the contribution in one long
sentence. An editor needs to know why the result is not a routine composition
of Katz--Sarnak and an existing race law.

Use two short paragraphs with this logic:

1. Earlier function-field race work supplies fixed-curve endpoint laws and
   bias statistics; hyperelliptic family work supplies Frobenius
   equidistribution and low-zero statistics.
2. The new object here retains the Frobenius configuration as outer
   randomness and proves convergence of the **conditional law itself** in
   \(W_2\), at a critical moving weight for which the lowest angles remain of
   order one. State that the new work needed for this passage is the exact
   weighted-race reduction, a genus-explicit nonsmooth-test transfer, and
   closed-edge \(\ell^2\) stability of the marked law.

Do not use “first” unless a refreshed literature search supports it. The
current sentence “We do not claim that simultaneous large field and large
genus, by themselves, are new” should remain, perhaps in the scope paragraph.

### M5. Replace the mixed equation-numbering system

This is a release blocker, not a cosmetic preference. `main.tex` does not set
section-based equation numbering. Sections 1--4 and Appendix A manually apply
dozens of `\tag{1.1}`, `\tag{2.1}`, ..., `\tag{A.12}`, while Section 5 and
Appendix B use automatic `equation` numbering. An auxiliary TeX build confirms
the inconsistency: `eq:finite-sp-kernel` prints as `(1)` in Section 5,
`eq:conditional-variance-statistic` prints as `(11)`, and
`eq:basic-shared-phase-cost` prints as `(19)` in Appendix B, immediately after
earlier displays manually numbered `(4.8)` and `(A.12)`. The pages can look
visually clean while this numbering remains editorially wrong.

Add automatic section numbering in the preamble (for example,
`\numberwithin{equation}{section}`), remove the ordinary numerical `\tag`
commands, and retain only the semantic tag `(LI)`. Rebuild and verify every
cross-reference. The theorem/equation hierarchy should be generated by TeX,
not hand-maintained.

### M6. Fix submission metadata and move the AI disclosure

`main.tex`, lines 30--36, is draft metadata, not journal metadata.

- Add a verifiable affiliation, postal address, and corresponding-author
  email.
- Remove “Draft of August 2026, not yet submitted or externally peer
  reviewed” from the author footnote.
- Move the AI-use statement to a short unnumbered disclosure or
  acknowledgements paragraph and adapt it to the chosen journal's current
  policy. It should name the tools and their roles, say that they are not
  authors, and state exactly which checks the human author actually performed.
- Do not say that the author independently checked the final manuscript until
  that is true. At present the repository itself records missing exact-source
  and external-specialist checks.
- Remove the “Verification status” paragraph from
  `sections/05-assembly.tex`, lines 48--54. Put the Lean scope and repository
  link in a reproducibility/data statement, an acknowledgement, or the
  preprint landing page. It interrupts the mathematical conclusion and
  advertises incompleteness without supporting the theorem.

### M7. Repair the title and abstract

The present title is accurate but misses the paper's real distinguishing
word. Recommended title:

> **A quenched hard-edge limit for weighted hyperelliptic prime races**

“Quenched” matters more than “simultaneous”; the simultaneous regime belongs
in the abstract and theorem assumptions.

In the abstract, replace “weighted splitting-prime race” by “weighted
inert-versus-split prime race,” because the statistic in (1.3) has that sign
and comparison. Replace “has an endpoint distribution” by “has a Cesàro
empirical distribution over the degree cutoff,” which tells the reader what
an endpoint distribution is. The current 144-word length is good.

A compact replacement abstract could follow this structure (the final wording
must be checked against the revised theorem):

> We study a weighted inert-versus-split prime race in the explicit
> hyperelliptic pencil
> \(y^2=\prod_{a=1}^{2g}(x-a)(x-t)\) over finite fields. For each curve, the
> normalized race has a Cesàro endpoint law. At the critical scaling
> \(m+1/2=\lambda/((2g+1)\log Q)\), we prove convergence in distribution of
> these quenched laws, as random elements of
> \((\mathcal P_2(\mathbb R),W_2)\), to the conditional random-phase law
> marked by the symplectic hard-edge process. The limit is simultaneous in
> genus and field size for odd square prime powers satisfying
> \(\log Q/(g^2\log(g+2))\to\infty\). The limiting conditional measure is
> almost surely absolutely continuous and genuinely random; its
> positive-half-line mass is also nonconstant. The proof combines
> density-one Frobenius-angle independence, a genus-explicit
> arithmetic-to-Haar transfer, and direct \(\ell^2\)-to-\(W_2\) control of
> the marked hard-edge series.

The fixed-field disclaimer should remain in the introduction and scope
section rather than being the final sentence of the abstract.

## 4. Mandatory cuts and relocations within the 22-page submission

The present source contains about 8,800 prose/math words before references.
The separately rendered manuscript is 22 pages and was reported visually
clean. Thus the 20--30-page target is already met. The following cuts are
still required because they improve focus and authority, not because the
paper is too long.

1. **Delete the verification-status paragraph** in Section 6 (7 lines), as
   required by M6.
2. **Remove the duplicate explicit-sequence calculation** in
   `sections/05-assembly.tex`, lines 28--39. It is already proved in
   `sections/02-linear-independence.tex`, lines 131--147. Section 6 should cite
   that calculation in one sentence.
3. **Remove the duplicate absolute-continuity proof** in
   `sections/04-hard-edge.tex`, lines 147--161, or remove the last clause and
   proof from Proposition B.1. Keep one complete proof, not both. The cleanest
   choice is to retain it in Appendix B and cite it after the Haar-limit
   proposition.
4. **Move the detailed Bessel inversion calculation** at
   `sections/04-hard-edge.tex`, lines 277--299, to a short lemma in Appendix B
   if Section 5 renders above five pages. Keep the crowding argument and the
   conclusion in the main line. This is a relocation, not an invitation to
   replace the proof with an unsupported “standard estimate.”
5. If the paper still exceeds 28 pages, **cite rather than prove the Brownian
   displacement lemma** in Appendix A, lines 117--142. Do not cut the
   type-\(C_g\) heat-trace derivation or the exact \(K_{2s}(e)\) normalization;
   those are the parts a referee will most want to audit.

Do **not** cut the parity centers, the square-field angle--\(\pi\) argument,
the closed-half-line/no-escape repair, the projection-DPP variance, or the
separate scalar-nondegeneracy argument. Each prevents a natural but incorrect
shortcut.

## 5. Presentation improvements that are important but not release blockers

### O1. Add a one-line proof diagram

The introduction promises a four-stage bridge but only describes it in prose.
After the main result, add one displayed chain:

\[
\text{endpoint race}
\longrightarrow \text{quenched Frobenius law}
\longrightarrow \text{Haar }\mathrm{USp}(2g)\text{ law}
\longrightarrow \text{marked hard-edge law}.
\]

Annotate the three arrows by LI, the heat bridge, and marked \(W_2\) stability.
This is the only visual the paper needs.

### O2. Explain why the topology is \(W_2\)

Add one sentence: the cosine coefficients are naturally square-summable and
the shared-phase coupling controls second moments exactly, making \(W_2\)
the topology carried by the proof. This turns an apparently fashionable
metric choice into a necessary one.

### O3. Give each technical section a one-sentence contract

Sections 2--5 already do this informally. Make the statements parallel:
input, output, and where the output is next used. This will help a referee
separate imported theorems from new arguments.

### O4. Tighten a few defensive sentences

Sentences such as “All factors in this formula are essential, including
\(1/2\)” and “For clarity, the last assertion does not rest only on the formal
stability lemma” reveal the history of internal debugging. Convert them into
positive mathematical prose or footnotes. A final paper should display the
correct normalization without narrating earlier mistakes.

## 6. Proof-length assessment

The proof length is fundamentally justified. The paper has three genuinely
nonstandard bridges, each of which needs visible constants or topology:

1. the exact endpoint law with parity centers;
2. the genus-explicit transfer from arithmetic Frobenius classes to Haar
   measure for a nonsmooth measure-valued functional;
3. the closed-hard-edge, square-summable marked-law passage in \(W_2\).

The appendices are not generic padding. Appendix A protects the metric,
Casimir, heat-time, Haar-volume, and \(K_{2s}\) normalizations. Appendix B
protects measurability, the endpoint zero, and the exact shared-phase
coupling. Those are precisely the places a hostile referee would probe.

The least economical part is the proof of nonconstancy of the scalar
half-line mass. It consumes substantial space, but it is also the result that
turns a random conditional law into a concrete prime-race statement. Keep it
unless the target editor explicitly asks for a shorter pure convergence
paper. If it is kept, advertise it in the corollary rather than enlarging the
main theorem.

## 7. Claim calibration

The current manuscript is appropriately restrained. Preserve these points:

- “large-field/large-genus bridge,” not fixed-field microscopic theorem;
- conservative sufficient growth condition, not an optimal threshold;
- explicit one-parameter pencil, not the full hyperelliptic ensemble;
- elementary scaling core Lean-checked, not headline theorem Lean-verified;
- no unqualified claim of priority.

The only needed strengthening is a **precise novelty comparison**, not a
larger novelty claim. A paper can be publishable because the object and bridge
are new even when all four surrounding theories are established.

Avoid the words “groundbreaking,” “bulletproof,” “impossible to be wrong,” or
“100% verified” in the paper, cover letter, arXiv comments, or correspondence.
They would lower rather than raise editorial confidence.

## 8. Venue assessment

The best current fit is a specialist number-theory/finite-field journal, not
a general top-tier journal.

- **Finite Fields and Their Applications:** strong subject fit because finite
  fields and arithmetic geometry are essential, not cosmetic. Its official
  scope explicitly includes number theory and algebraic geometry over finite
  fields: <https://www.sciencedirect.com/journal/finite-fields-and-their-applications>.
- **Journal of Number Theory:** broad and realistic if the introduction makes
  the number-theoretic novelty legible. Its official scope welcomes detailed
  contemporary number-theory articles:
  <https://www.sciencedirect.com/journal/journal-of-number-theory>.
- **Research in Number Theory** or **Acta Arithmetica:** plausible specialist
  alternatives. The latter's official scope is simply number theory:
  <https://www.impan.pl/en/publishing-house/journals-and-series/acta-arithmetica>.
- **Forum of Mathematics, Sigma / IMRN:** stretch targets. The current theorem
  is technically broad but its very rapid field-growth regime and reliance on
  an explicit pencil weaken the case for a leading general/specialist venue.
  Sigma describes itself as an open-access alternative to leading specialist
  journals: <https://www.cambridge.org/core/journals/forum-of-mathematics-sigma>.

My honest rating is **6.5--7/10 for mathematical contribution**, **4.5/10 for
release readiness today**, and **about 7/10 for specialist-journal readiness
after the mandatory edits and two expert checks**. There is no honest path to
`9.5/10` by polishing alone. Reaching that level would require a materially
stronger theorem, most plausibly a fixed-field microscopic result or a much
broader family theorem, not a longer introduction.

## 9. Release decision checklist

Do not submit until all boxes are true:

- [ ] exact Katz--Sarnak hypotheses and Frobenius convention checked from the
  original source;
- [ ] exact Kowalski theorem, erratum, exponent, and uniformity checked from
  the original source;
- [ ] Soshnikov convergence criterion matched hypothesis by hypothesis;
- [ ] main theorem split from its corollary and explicit example;
- [ ] \(\mathcal P_2\), \(W_2\), quenched/outer randomness, and first-use
  notation defined;
- [ ] novelty paragraph rewritten as a precise comparison with prior work;
- [ ] equation numbering made fully automatic and all references rebuilt;
- [ ] author affiliation, correspondence data, and policy-compliant AI
  disclosure supplied;
- [ ] duplicate proof/calculation passages cut;
- [x] rendered PDF inspected separately, reported visually clean, and
  confirmed at 22 pages;
- [ ] arithmetic-geometry expert report received and answered;
- [ ] random-matrix/DPP expert report received and answered;
- [ ] literature search refreshed immediately before public release;
- [ ] cover letter describes a quenched \(\mathcal P_2\)-valued bridge theorem,
  without prestige or full-formal-verification rhetoric.

**Bottom line:** the manuscript has a real paper inside it, and the proof
length is defensible. The next gain will come from sharpening the statement,
definitions, novelty contrast, and external verification—not from adding more
theorems.

---

## POST-REVISION DELTA REVIEW (2026-08-17)

### Delta verdict

**The major editorial revision passes, subject to one remaining TeX release
blocker.** The current manuscript now states one main theorem, separates its
prime-race consequence and explicit field sequence, defines the Wasserstein
state space and the two probability layers before the theorem, gives a
specific novelty comparison rather than a priority slogan, and uses coherent
automatic numbering. The exact-source ledger closes both its deep-theorem and
new-bibliography gates as `PASS`.

I found no mathematical statement lost or strengthened incorrectly during the
revision. Excluding the already acknowledged needs for independent human
specialist review and author affiliation/contact details, the only remaining
submission blocker is the overfull proof diagram described below.

### Mandatory delta checklist

- [x] **Headline structure:** Theorem 1.1 now contains the random-measure
  convergence, nonconstancy, and absolute continuity; Corollary 1.2 contains
  the half-line race-density consequences; Example 1.3 contains the explicit
  field sequence.
- [x] **Self-contained theorem parameter:** Theorem 1.1 explicitly begins
  “For every fixed \(\lambda>0\).”
- [x] **State space:** \(\mathcal P_2(\mathbb R)\) and \(W_2\) are defined
  before the endpoint law is placed in that space.
- [x] **Quenched meaning:** The inner phase randomness and outer
  curve/configuration randomness are distinguished before the main theorem;
  the meaning of \(\Longrightarrow\) is stated.
- [x] **Topology motivation:** The square-summable coefficients and
  shared-phase second-moment coupling explain why \(W_2\) is used.
- [x] **Novelty calibration:** The introduction now contrasts the result with
  Bailleul--Devin--Keliher--Li, Bates et al., and Lal\'{i}n et al., and says
  “particularly close,” “the object studied here,” and “bridges established
  here,” avoiding an unproved priority claim.
- [x] **Deep-source gate:** The Katz--Sarnak, Raynaud/GOS, Deligne, Kowalski,
  and Soshnikov statements and locators have been repaired and re-audited.
- [x] **Bibliography metadata:** The Bailleul--Devin--Keliher--Li and Bates et
  al. author/volume metadata corrections recorded in the exact-source ledger
  are present.
- [x] **First-use notation:** \(W_{2g}\), the falling factorial, and \(J_0\)
  are defined before use; the affine-Weyl formula now uses the already defined
  \(W_{2g}\).
- [x] **Equation numbering:** A fresh auxiliary build gives equations
  1.1--1.9, 2.1--2.14, 3.1--3.8, 4.1--4.8, 5.1--5.18, A.1--A.12, and
  B.1--B.8. `(LI)` is the sole deliberate manual tag. Theorem/corollary/example
  numbers are 1.1/1.2/1.3.
- [x] **Manuscript disclosure:** The draft disclaimer was removed from the
  author field; the generative-AI statement is now a separate declaration and
  does not claim end-to-end formal verification.
- [x] **Cuts:** The verification-status paragraph and duplicate explicit-field
  calculation were removed from Section 6.
- [x] **Source integration:** The final TeX pass resolves citations and
  cross-references and remains 22 pages.
- [ ] **TeX log gate:** The newly added proof-chain display in
  `sections/00-introduction.tex`, lines 199--206, is 90.48846 pt too wide. A
  fresh three-pass Tectonic run reports
  `Overfull \hbox ... at line 206`. The display must be split across two
  lines (for example with `aligned`), shortened, or otherwise reflowed. Then
  rerun `build-release.ps1`; its `Overfull \hbox` pattern should reject the
  current snapshot and pass only after the warning is gone.

### Remaining nonblocking polish

These items should be cleaned up but do not justify delaying mathematical
submission after the overfull display and the two excluded human gates are
resolved:

1. Define \(d_G\) and \(d_{\rm conj}\) in words immediately before the
   conjugacy-quotient lemma rather than relying on conventional interpretation.
2. The abstract could replace “endpoint distribution” by “Ces\`aro endpoint
   law,” matching the body more precisely.
3. Update `README.md` to the new title and make `build-release.ps1` the primary
   documented release command; its present working title omits “quenched.”
4. Once a target journal is chosen, adapt the generative-AI declaration to
   that journal's exact policy and move it if the journal requires a different
   submission field.
5. The chronological source ledger begins with its pre-fix `FAIL` verdict and
   ends with the authoritative `PASS`. Add a one-line status banner at its top
   if it will be distributed with the preprint, so readers do not stop at the
   superseded verdict.

### Updated readiness assessment

- **Mathematical contribution:** unchanged at **6.5--7/10**.
- **Editorial/source readiness after this revision:** **8/10**.
- **Submission readiness today:** **7/10**, held below release only by the
  overfull proof diagram plus the separately excluded human-review and contact
  gates.
- **Submission readiness after those gates:** **8/10 for an appropriate
  specialist venue**. Finite Fields and Their Applications and Journal of
  Number Theory remain the most natural first targets; Sigma/IMRN remain
  stretches rather than realistic “publish quickly” choices.

**Post-revision bottom line:** the revision successfully converted the draft
from “major editorial revision required” to “release candidate with one local
TeX failure.” No further theorem or section should be added before submission.
