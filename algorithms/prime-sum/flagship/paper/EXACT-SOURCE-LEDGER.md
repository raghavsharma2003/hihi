# Exact-source release ledger

Date checked: 2026-08-17

Manuscript commit checked: `dfdfe18171ae70b8c78f6d1caa01a05631fc7038`

Scope: only the deep imported statements named below, against accessible
primary/author-hosted source text. No claim was accepted from a search snippet,
secondary paper, or remembered theorem statement.

## Gate verdict

**FAIL pending mandatory citation/wording corrections.**

The principal arithmetic inputs are supported: the Katz--Sarnak monodromy and
tameness results, Kowalski's exceptional-set estimate with the erratum factor,
Kowalski's relation-space theorem, and Deligne's weight bound all match the
manuscript hypotheses and constants. Soshnikov supports DPP existence and
count-cylinder convergence, as well as the correlation formulas used later.

The gate nevertheless fails for the current TeX for three exact-source reasons:

1. `sections/03-transfer.tex:86` cites **Katz--Sarnak, Theorem 9.2.5** as the
   Grothendieck--Ogg--Shafarevich formula. There is no such theorem: 9.2.5 is an
   unlabelled introductory paragraph on equidistribution, followed by Theorem
   9.2.6. It is not the claimed GOS result.
2. `sections/04-hard-edge.tex:53-59` says Soshnikov's criterion directly gives
   vague convergence. The exact conclusion of Soshnikov's Theorem 5 is weak
   convergence "on the cylinder sets." The manuscript's first-moment bound can
   supply local tightness, but that cylinder-to-vague step must be stated rather
   than attributed verbatim to Theorem 5.
3. `sections/04-hard-edge.tex:254` attributes the determinant factorial-moment
   identity only to Definition 2 and (1.5). Those give the factorial-moment
   integral in terms of `rho_N`; the substitution `rho_N = det(K(x_i,x_j))`
   additionally comes from Definition 3 and (1.20).

These are repairable source/citation defects. The first is mandatory. The second
is a mandatory exact-wording clarification. The third is a mandatory citation
completion under this release gate. No contradiction to the headline theorem was
found in the checked sources.

## 1. Katz--Sarnak: family, tameness, monodromy, and GOS

Primary text inspected: Nicholas M. Katz and Peter Sarnak, *Random Matrices,
Frobenius Eigenvalues, and Monodromy*, author-hosted full book PDF:
<https://web.math.princeton.edu/~nmk/RMFEM.pdf>.

Inspected file SHA-256:
`39BEB011E5FAB2737BB131611F054221108128FBEBBB7F62BA2DE9A56F755DD5`.

### 1.1 Applicability to the pencil -- PASS

- Exact location: section 10.1.1, printed p. 293 (PDF p. 302), and section
  10.1.2, printed p. 293.
- Source hypotheses: odd characteristic; `g > 1`; `f` has degree `2g` and all
  roots are distinct in the ground field; parameter space is the affine line
  with the roots of `f` removed; family `Y^2=f(X)(X-T)`.
- Manuscript match: `f_g(X)=prod_{a=1}^{2g}(X-a)`, and `p>2g+1` makes the
  residues `1,...,2g` distinct; the main regime has `g>=2`; `U_g` removes
  exactly those roots. The book's Lemma 10.1.11, printed p. 296 (PDF p. 305),
  identifies the affine `R^1 pr_!` sheaf with `R^1 pi_*` for the proper family,
  matching the manuscript's sheaf model.

### 1.2 Tameness -- PASS

- Exact location: Lemma 10.1.12, printed pp. 296--297 (PDF pp. 305--306).
- Exact conclusion: the lisse sheaf on `U` is everywhere tame, including the
  points at infinity of `U`.
- Manuscript match: `sections/03-transfer.tex:50-52` cites this exact lemma for
  the same one-parameter family. Twisting by a geometrically trivial constant
  character does not change geometric local inertia, and applying an algebraic
  representation preserves tameness. The cited result supports the input used
  in the GOS calculation.

### 1.3 Full geometric monodromy -- PASS

- Exact location: Theorem 10.1.16, printed pp. 299--300 (PDF pp. 308--309).
- Exact conclusion: the geometric monodromy group of the one-parameter family
  `Y^2=f(X)(X-T)` is `Sp(2g)`.
- Manuscript match: same family and hypotheses as in section 10.1.1. The
  citation at `sections/03-transfer.tex:52` is exact.

### 1.4 Claimed GOS theorem number -- FAIL

- Current citation: `sections/03-transfer.tex:85-86`,
  `\cite[Theorem~9.2.5]{KatzSarnak1999}`.
- Exact source check: at printed p. 276 (PDF p. 285), **9.2.5 is a paragraph**
  beginning the statement of a version of Deligne equidistribution. The next
  numbered result is Theorem 9.2.6. Neither is the cited tame GOS formula.
- Relevant text actually present in the book: the proof of Lemma 10.1.12,
  printed pp. 296--297, explicitly writes the Euler--Poincare/GOS formula
  `chi_c(U,F)=rank(F) chi_c(U,Q_l)-sum_x Swan_x(F)` and cites Raynaud.
- Mathematical consequence: for the manuscript's tame `rho(F_g)`, all Swan
  terms vanish; with `chi_c(A^1-{2g points})=1-2g` and the separately proved
  vanishing of `H_c^0,H_c^2`, the identity
  `dim H_c^1=(2g-1)dim rho` follows. Thus the calculation is supported, but the
  current theorem-number citation is false.
- Mandatory repair: replace the nonexistent theorem citation by an exact
  primary citation to Raynaud, Part I, Theorem 1 and equations (2), (2 bis),
  (2 ter), printed pp. 133--134, as pinned immediately below. Do not rename
  9.2.5 as a theorem.

### 1.5 Exact primary GOS replacement -- PASS

Primary text inspected: Michel Raynaud, *Caractéristique d'Euler--Poincaré
d'un faisceau et cohomologie des variétés abéliennes*, Séminaire N. Bourbaki,
Exposé 286, vol. 9 (1964/65; published 1966), pp. 129--147:
<https://www.numdam.org/item/SB_1964-1966__9__129_0.pdf>.

Inspected SHA-256:
`FD0CF10B653F40E43F2EF7211FED427B7C5C80022C42BEDECBF1544B050BAA40`.

- Exact locations: Proposition 1(b), printed p. 131 (PDF p. 4), states that the
  wild correction is zero for tame ramification. Part I, Theorem 1 and
  equations (2), (2 bis), and (2 ter), printed pp. 133--134 (PDF pp. 6--7),
  give the Euler--Poincare formula for constructible prime-to-characteristic
  torsion sheaves on a smooth projective curve and its open-curve form.
- Application: apply the torsion formula to stable lattices modulo powers of
  `ell` and pass to the associated lisse `Q_ell`-sheaf. For a tame sheaf the
  local wild/Swan corrections vanish, yielding exactly
  `chi_c(U,F)=rank(F) chi_c(U,Q_ell)`. This is also the source cited as `[Ray]`
  in Katz--Sarnak's proof of Lemma 10.1.12.
- BibTeX-ready metadata:

```bibtex
@article{Raynaud1966,
  author  = {Michel Raynaud},
  title   = {Caract\'eristique d'{{E}}uler--Poincar\'e d'un faisceau et
             cohomologie des vari\'et\'es ab\'eliennes},
  journal = {S\'eminaire N. Bourbaki},
  volume  = {9},
  pages   = {129--147},
  year    = {1966},
  note    = {Expos\'e no. 286},
  url     = {https://www.numdam.org/item/SB_1964-1966__9__129_0/}
}
```

- Exact manuscript citation to use:
  `\cite[Part~I, Theorem~1 and (2 bis), pp.~133--134]{Raynaud1966}`.

## 2. Kowalski: exceptional parameters and erratum

Primary texts inspected:

- Emmanuel Kowalski, *The large sieve, monodromy and zeta functions of
  curves*, author PDF:
  <https://people.math.ethz.ch/~kowalski/large-sieve-monodromy.pdf>.
- Author erratum:
  <https://people.math.ethz.ch/~kowalski/erratum-large-sieve-monodromy.pdf>.

Inspected SHA-256 values:

- article: `A55CCF3F0F9BF5FE97D49ACE2DC9C4625BDA37CD2C9C34CBF18B29EBAA52323D`
- erratum: `A1696709F3BD9A0CAF2283C5C50A19D54C86ADE93AB58CCFFFFF78FBE0D2BCD1`

### 2.1 Theorem 6.2 hypotheses, exponent, and constant -- PASS

- Exact location: Theorem 6.2, author PDF p. 19; published-page location p. 54
  is confirmed by erratum item [3].
- Source family: odd characteristic, `q=p^k`, monic `f in F_q[X]` of degree
  `2g` with distinct roots in `F_q`, `U=A^1-{f=0}`, and
  `C_u:y^2=f(x)(x-u)` completed at infinity.
- Source exceptional event: `P_u` is reducible or its splitting-field degree is
  strictly below `2^g g!`.
- Source exponent: `gamma=(4g^2+3g+5)^{-1}`; the uncorrected displayed theorem
  has an absolute implied constant and `q^{1-gamma} log q`.
- Manuscript match: `f_g` is monic of degree `2g` and is split squarefree under
  `p>2g+1`; the manuscript uses the same exceptional event and exponent. The
  functional equation embeds the action in `W_{2g}`, whose order is
  `2^g g!`, so full splitting-field degree is equivalent to full `W_{2g}`.

### 2.2 Erratum factor `g^2` -- PASS

- Exact location: erratum item [3], PDF p. 1, correcting published p. 54,
  line 4.
- Exact correction: the right side is `g^2 q^{1-gamma} log q`, because the
  proof must ensure `L>1`.
- Manuscript match: Proposition 3.4 has `A g^2 Q^{1-gamma_g} log Q` with an
  absolute `A`, exactly the corrected uniform form.

No extra condition `p>2g+1` is imposed by Theorem 6.2 itself; the manuscript's
stronger condition is legitimate and is used to make the explicit integer-root
polynomial squarefree after reduction.

## 3. Kowalski: multiplicative relation space

Primary text inspected: Emmanuel Kowalski, *The large sieve, monodromy, and
zeta functions of algebraic curves, II: independence of the zeros*, author
preprint PDF: <https://arxiv.org/pdf/0807.2118>.

Inspected SHA-256:
`2F12C458B013E98ACC682C153BA2CBA01A400D36517766EF37BB4345DBB3450D`.

### Proposition 2.4(2), `m=1` -- PASS

- Exact locations: equation (2.5), PDF p. 11; Proposition 2.4 and its hypotheses,
  PDF p. 12; conclusion and proof, PDF pp. 12--14.
- Source hypotheses relevant here: `g>=2`; splitting field has Galois group
  `W_{2g}` in its natural action on the roots; reciprocal-pair products are the
  same positive rational `m`; for `m=1`, the conclusion is valid already for
  `g>=2`.
- Exact conclusion: for one polynomial and `m=1`, the rational multiplicative
  relation space is `1 plus G(M)`, which equation (2.5) identifies with the
  vectors having equal coordinates on the two members of every reciprocal pair.
- Manuscript match: because `Q=s^2`, normalizing the inverse roots by the
  rational number `s` produces a polynomial over `Q`; the pair products become
  one; scaling does not change the splitting field; the maximal group hypothesis
  is exactly `W_{2g}`. The vector `(2a_j,0)` arising after exponentiating twice
  can lie in the source relation space only when every `a_j=0`; the remaining
  `b pi` coefficient is then zero. The manuscript does not require an integral
  saturation claim, consistently with the proposition's rational conclusion.

## 4. Deligne: weight bound on compactly supported cohomology

Primary text inspected: Pierre Deligne, *La conjecture de Weil II*, author/IAS
PDF: <https://publications.ias.edu/sites/default/files/Number40.pdf>.

Inspected SHA-256:
`99D3C62A83FD9FB41AF17D165E4A63D7120A7EDF3C5C4A409FA50F2E64B1CD20`.

### Theorem 3.3.1 -- PASS

- Exact location: Theorem 3.3.1, printed p. 204 (PDF p. 68).
- Exact statement used: if a sheaf is mixed of weights at most `n`, then
  `R^i f_!` is mixed of weights at most `n+i`.
- Manuscript specialization: apply `f:U_g -> Spec(F_Q)` to the weight-zero
  lisse sheaf `rho(F_g)`. Eigenvalues on `H_c^1` then have weights at most one,
  hence every complex absolute value is at most `Q^{1/2}`. With the GOS
  dimension identity and the trace formula this gives
  `(2g-1) dim(rho) sqrt(Q)`, exactly as written.
- Citation quality: `sections/03-transfer.tex:92-93` cites the correct work but
  not the exact theorem. For release-grade precision, change it to
  `\cite[Theorem~3.3.1]{Deligne1980}`. This is a precision improvement, not a
  mathematical failure.

## 5. Soshnikov: DPP existence, convergence, and moment identities

Primary text inspected: Alexander Soshnikov, *Determinantal Random Point
Fields*, author preprint version 4:
<https://arxiv.org/pdf/math/0002099>.

Inspected SHA-256:
`73FEA6B802F7EC00DCB281438904AE89108412CE469BE7E5CA651903B4806D0B`.

### 5.1 Existence from a projection kernel -- PASS

- Exact location: Theorem 3, PDF p. 13.
- Exact statement: a Hermitian locally trace-class operator defines a unique
  DPP exactly when `0<=K<=1`.
- Manuscript match: every finite kernel and the limiting sine-band kernel are
  locally trace-class orthogonal projections, hence Hermitian contractions.
  To match Soshnikov's `E=R^d` setting literally, extend the half-line kernels
  by zero to the negative half-line; the resulting process is supported on
  `[0,infinity)`.

### 5.2 Operator convergence criterion -- PASS for cylinder laws; FAIL as a
verbatim citation for vague convergence

- Exact location: Theorem 5, PDF p. 16.
- Exact hypotheses: weak-operator convergence `K_n -> K` and convergence of
  every bounded local trace `Tr(chi_B K_n chi_B) -> Tr(chi_B K chi_B)`.
- Exact conclusion: the corresponding probability measures converge weakly
  **on the cylinder sets**.
- Manuscript hypotheses: local uniform kernel convergence gives convergence on
  compactly supported test functions; projection/contraction bounds extend it
  to weak-operator convergence. Local uniform convergence of the diagonal plus
  the common diagonal bound gives every bounded local-trace convergence. Thus
  Theorem 5 applies.
- Exactness defect: the displayed conclusion in the manuscript is vague point-
  process convergence, which is not the literal conclusion printed in Theorem
  5. The following manuscript estimate `sup_g E Xi_g([0,L])<=2L` supplies the
  required local tightness, so the upgrade is standard and plausible, but it is
  a separate step.
- Mandatory repair: say explicitly that Theorem 5 gives convergence of the
  local count-cylinder laws and that the displayed first-moment bound gives
  local tightness, which upgrades this to weak convergence for the vague
  topology. Alternatively provide a direct compactly supported Laplace-
  functional/Fredholm-determinant argument.

### 5.3 Determinantal covariance identity -- PASS as a derivation

- Exact location: Definition 3 and equation (1.20), PDF p. 8.
- Exact source content: `rho_n(x_1,...,x_n)=det(K(x_i,x_j))`.
- Manuscript use: combining the `n=1,2` cases with the factorial-moment
  definition yields
  `Var(sum f)=int f^2 K(x,x)-doubleint f(x)f(y)|K(x,y)|^2`. For a projection,
  `int |K(x,y)|^2dy=K(x,x)`, and symmetrization gives the manuscript's exact
  factor `1/2` in equation `eq:projection-dpp-variance`. The source citation is
  sufficient because the manuscript displays the derivation and justifies the
  noncompact limit by `L^2` truncation.

### 5.4 Factorial-moment crowding formula -- mathematical PASS, citation
incomplete

- Exact locations: Definition 2 and equation (1.5), PDF p. 3; Definition 3 and
  equation (1.20), PDF p. 8.
- Source consequence: for a single bounded interval `I`, Definition 2 gives
  `E(N_I)_N=int_{I^N} rho_N`, and Definition 3 gives
  `rho_N=det(K(x_i,x_j))`. This is exactly the manuscript formula.
- Citation defect: `sections/04-hard-edge.tex:254` cites only Definition 2 and
  (1.5), omitting the second half of the displayed determinant identity.
- Mandatory repair: cite `Definitions 2 and 3, equations (1.5) and (1.20)`.

## Required TeX actions before this gate can pass

1. Correct the false Katz--Sarnak GOS citation at
   `sections/03-transfer.tex:86`.
2. Separate Soshnikov Theorem 5's cylinder-law conclusion from the local-
   tightness upgrade to vague convergence at `sections/04-hard-edge.tex:53-60`.
3. Complete the Soshnikov factorial-moment citation at
   `sections/04-hard-edge.tex:254` by adding Definition 3 and (1.20).
4. Recommended exactness: attach Deligne Theorem 3.3.1 to the weight bound.

After those edits, this exact-source gate should be rerun against the new lines.

## Post-fix re-audit addendum (2026-08-17)

### Deep-source theorem gate -- PASS

The three mandatory source repairs were rechecked in the current TeX.

1. **GOS and Deligne -- PASS.** `sections/03-transfer.tex:85-94` now cites
   Raynaud, Part I, Theorem 1 and (2 bis), printed pp. 133--134, for the tame
   Euler--Poincare formula, and Deligne Theorem 3.3.1 for the weight bound.
   These locators and the specialization used in the displayed dimension and
   square-root estimates match the inspected source text.
2. **Soshnikov convergence wording -- PASS.**
   `sections/04-hard-edge.tex:45-61` now separates the source conclusions
   correctly: Theorem 3 gives DPP existence; Theorem 5 gives the local
   count-cylinder laws; the manuscript's own uniform first-moment bound gives
   tightness on every compact interval; and a diagonal compact exhaustion is
   identified as the additional upgrade to weak convergence for the vague
   topology. The vague conclusion is no longer attributed verbatim to
   Soshnikov Theorem 5.
3. **Factorial-moment locator -- PASS.**
   `sections/04-hard-edge.tex:256-261` now cites Definitions 2 and 3 together
   with equations (1.5) and (1.20). Those are exactly the two source ingredients
   needed to replace the factorial moment by the determinant integral.

Accordingly, the deep imported-statement gate covered by this ledger is now
**PASS**.

### New bibliography metadata gate -- FAIL pending two corrections

The three newly highlighted records were checked against publisher metadata or
the first page of the current author preprint.

#### `BailleulDevinKeliherLi2024` -- FAIL

Primary publisher record:
<https://doi.org/10.1112/jlms.12876>.

Two fields in `references.bib:118-126` are wrong:

- first author is **Alexandre Bailleul**, not `Romain Bailleul`;
- the article is in **volume 109, issue 3**, not issue 2.

The title, year 2024, article number `e12876`, DOI, and other three authors are
correct. Required corrected core:

```bibtex
author  = {Alexandre Bailleul and Lucile Devin and Daniel Keliher and Wanlin Li},
volume  = {109},
number  = {3},
note    = {Article e12876},
doi     = {10.1112/jlms.12876}
```

#### `BatesEtAl2026` -- FAIL

Primary author preprint, arXiv:2603.21005v3, first page:
<https://arxiv.org/pdf/2603.21005>. Inspected PDF SHA-256:
`830C006B126357DC43A6968BFAA9C71D4A6D8A5C94AE713C86A6C3DD55CB4838`.

The title in the manuscript record, *Ties in Function Field Prime Races*, and
the arXiv identifier/year are correct against the current PDF, but every given
name in `references.bib:130-131` is wrong. The exact author line is:

```bibtex
author = {Graeme Bates and Ryan Jesubalan and Seewoo Lee and Jane Lu and
          Hyewon Shim},
```

The current hallucinated line `Grace Bates and Roshni Jesubalan and Sun Woo Lee
and Jasmine Lu and Hannah Shim` must not remain in a release bibliography.

#### `LalinEtAl2026` -- PASS

Primary author preprint, arXiv:2608.01337v1, first page:
<https://arxiv.org/pdf/2608.01337>. Inspected PDF SHA-256:
`0254FD4308BFEC8505D40B1CAB767548261AFAC42F44D5693E64745DEFF2ED3F`.

The authors Matilde Lalin, Kyu-Hwan Lee, Thomas Oliver, and Alexey Pozdnyakov;
the title *Murmurations of quadratic and cubic characters over function
fields*; year 2026; and arXiv identifier 2608.01337 all match. The TeX accent in
`Lal\'{i}n` correctly represents `Lalín`.

### Current aggregate verdict

- Exact deep-source claims: **PASS**.
- New bibliography metadata: **FAIL** until the BDKL and Bates records are
  corrected as above.
- No new mathematical source contradiction was found in the repaired theorem
  passages.

## Final aggregate closeout (2026-08-17)

**PASS.** The corrected records in `references.bib` were checked again:

- `BailleulDevinKeliherLi2024` now has Alexandre Bailleul as first author and
  Journal of the London Mathematical Society volume 109, issue 3, article
  e12876, matching DOI `10.1112/jlms.12876`.
- `BatesEtAl2026` now lists Graeme Bates, Ryan Jesubalan, Seewoo Lee, Jane Lu,
  and Hyewon Shim, matching the author line of arXiv:2603.21005v3.
- `LalinEtAl2026` remains correct against arXiv:2608.01337v1.

Both components of this ledger now pass: the exact deep-source theorem gate and
the inspected bibliography-metadata gate. No unresolved item remains within the
scope of this audit.
