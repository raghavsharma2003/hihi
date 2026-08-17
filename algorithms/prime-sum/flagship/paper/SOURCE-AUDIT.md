# External theorem and normalization audit

Audit date: 2026-08-17

Scope: only the imported results used for (i) hyperelliptic monodromy and
quantitative Frobenius equidistribution, (ii) the maximal-Galois exceptional
set, (iii) the implication from maximal Galois group to angle--pi linear
independence over square fields, and (iv) the symplectic hard-edge and
determinantal-process steps.  This is not an audit of the prime-race explicit
formula, the heat estimate, or the marked-law appendix.

The statuses below distinguish a false or inconsistent normalization
(`FAIL`) from a citation whose exact advertised substatement could not be
checked in an accessible primary text (`UNRESOLVED`).  `PASS` means the
hypotheses and normalization were checked against the cited primary source or
were rederived from the source's stated formulas.

## Executive ledger

| Imported item | Status | Release consequence |
|---|---:|---|
| Katz--Sarnak full symplectic geometric monodromy and tameness for the pencil | PASS | The family and characteristic hypotheses match. |
| Half-Tate Frobenius normalization | **FAIL** | Correct arithmetic/geometric Frobenius orientation before release. |
| Exact attribution of the constant in the character bound to Katz--Sarnak, Theorem 9.2.6(4)--(5) | **UNRESOLVED** | The displayed estimate is nevertheless provable directly, with a stronger constant; either give that proof or inspect an authorized copy of the theorem. |
| Kowalski uniform maximal-Galois exceptional-set estimate, including erratum | PASS | The exponent and the additional factor `g^2` are correct. |
| Square-field maximal-Weyl-group implication to angle--pi LI | PASS | Proposition 2.4(2) applies with `m=1` and `g >= 2`. |
| Haar `USp(2g)` finite kernel and hard-edge scaling | PASS | The factor `4/(2g+1)` and limiting symplectic kernel are correct. |
| DPP existence, weak convergence, factorial moments, and projection variance | PASS WITH WORDING REPAIR | State the operator hypotheses used in Soshnikov's theorems instead of saying only that local kernel convergence suffices. |
| Bibliographic metadata | PARTIAL | Add four DOIs; do not assert a date for the undated Kowalski erratum without an archival source. |

## 1. Katz--Sarnak monodromy, tameness, and Frobenius conventions

### 1.1 Full symplectic monodromy and tameness: PASS

The family in the manuscript is

```text
y^2 = f_g(x)(x-t),     deg(f_g)=2g,
```

with `f_g` monic, split, and squarefree.  The assumption
`char(F_Q)>2g+1` makes the residues of `1,...,2g` distinct and in particular
puts the family in odd characteristic.  This is precisely the
one-parameter family treated in Katz--Sarnak, Theorem 10.1.16; Lemma
10.1.12 is the cited tameness input.  Kowalski's primary proof of his
Theorem 6.2 independently records the same application: in the author PDF,
page 25, the geometric mod-ell monodromy is `Sp(2g,F_ell)`, and equation
(8.1) is followed by the statement that all the sheaves are tame by
Katz--Sarnak, Lemma 10.1.12.

Primary/official sources:

- N. Katz and P. Sarnak, *Random Matrices, Frobenius Eigenvalues, and
  Monodromy*, AMS Colloquium Publications 45 (1999), Theorem 10.1.16 and
  Lemma 10.1.12, [DOI 10.1090/coll/045](https://doi.org/10.1090/coll/045).
- E. Kowalski, *The large sieve, monodromy and zeta functions of curves*,
  author PDF, Theorem 6.2 and proof on pp. 25--28,
  [author PDF](https://people.math.ethz.ch/~kowalski/large-sieve-monodromy.pdf).

The manuscript's rank (`2g`), base (`A^1` minus the `2g` roots), and compact
group (`USp(2g)`) agree with these sources.

### 1.2 Half-Tate character: FAIL AS WRITTEN

The manuscript simultaneously uses the following two conventions:

1. the cohomological Frobenius has eigenvalues `alpha_j` satisfying
   `alpha_j alpha_{j+g}=Q`, and the cup-product similitude multiplier is
   `Q`; and
2. the constant character sends **arithmetic** Frobenius to `s^{-1}` for
   `Q=s^2`, after which the manuscript computes the multiplier as
   `Q(s^{-1})^2=1` and the eigenvalues as `alpha_j/s`.

These are inconsistent labels.  The zeta-function/cohomological Frobenius
with multiplier `Q` is geometric Frobenius.  Arithmetic Frobenius is its
inverse.  Therefore the required character must satisfy

```text
eta_s(geometric Frobenius)  = s^{-1},
eta_s(arithmetic Frobenius) = s.
```

This convention is explicit in the primary source already used for the
large-sieve input.  Kowalski defines `Fr_{u,q^n}` to be the **geometric**
Frobenius conjugacy class in Section 2 (p. 2 of the author PDF).  In Section 6
(pp. 17--18, equations (6.1)--(6.2)), he then writes the zeta numerator as the
characteristic polynomial of that geometric Frobenius on `H^1` and records
that the cup-product pairing has multiplier `q`.  Thus this is not merely a
choice of terminology: the manuscript's displayed roots and multiplier use
Kowalski's geometric-Frobenius convention.

Primary source: E. Kowalski, *The large sieve, monodromy and zeta functions of
curves*, Section 2, p. 2, and Section 6, pp. 17--18, equations (6.1)--(6.2),
[author PDF](https://people.math.ethz.ch/~kowalski/large-sieve-monodromy.pdf).

With this repair, the new eigenvalues are `alpha_j/s`, the pairing multiplier
is `Q s^{-2}=1`, and the twisted sheaf is pure of weight zero.  No theorem
statement or limiting law changes.

Required wording repairs:

- In Section 2, replace "sending arithmetic Frobenius to `s^{-1}`" by
  "sending geometric Frobenius to `s^{-1}` (equivalently arithmetic
  Frobenius to `s`)".
- In Section 3, identify every `Fr_Q` in (4.1)--(4.2) as geometric
  Frobenius, and construct the character on the arithmetic generator with
  value `s`.
- The sentence saying the half-Tate character "has weight zero" is also
  wrong literally: the character itself has weight `-1`; the **twisted
  rank-`2g` sheaf** has weight zero.

This is a normalization error, not a gap in the existence of the character:
the map from the procyclic arithmetic quotient sending its arithmetic
generator to the 3-adic unit `s` is continuous, and `3` is invertible because
`char(F_Q)>2g+1>=5`.

### 1.3 Quantitative character estimate: citation unresolved, claim repairable

The official AMS record confirms the book and chapter metadata, but the exact
text of Katz--Sarnak, Theorem 9.2.6(4)--(5), was not accessible in this audit.
I therefore did not verify from the primary theorem that its constant is
literally the total compactly supported Betti number of the particular full
mod-3 cover used in Section 3.  Mark that exact attribution `UNRESOLVED`.

The displayed character estimate itself is safe and can be proved more
directly, avoiding this source ambiguity and the mod-3 cover entirely.  After
the Frobenius repair above, let `rho` be a nontrivial irreducible algebraic
representation of `Sp(2g)`.  The associated sheaf is lisse, tame, pure of
weight zero, of rank `dim(rho)`, and has no geometric invariants.  On the
affine curve

```text
U_g = A^1 - {1,...,2g},     chi_c(U_g)=1-2g,
```

compactly supported `H^0` and `H^2` vanish.  Grothendieck--Ogg--Shafarevich
therefore gives exactly

```text
dim H_c^1(U_bar, rho(F_g)) = (2g-1) dim(rho).
```

Deligne's weight bound and the trace formula then give

```text
| average_t chi_rho(Theta_{g,t}) |
 <= (2g-1) dim(rho) sqrt(Q)/(Q-2g)
 <= 2(2g-1) dim(rho)/sqrt(Q)       (Q>4g).
```

This is stronger than (4.3), hence also proves (4.3) with the manuscript's
much larger `C_g`.  Recommended release repair: insert this two-paragraph
argument and cite Katz--Sarnak only for monodromy/tameness and the standard
trace-formula framework.  If the mod-3-cover route is retained, inspect an
authorized copy of Theorem 9.2.6(4)--(5) and quote its hypotheses verbatim.

The separate base-complexity calculation is correct:

```text
h_c^0(U_g)=0,  h_c^1(U_g)=2g,  h_c^2(U_g)=1,
A(U_g)=sum_{i<2} h_c^i(U_g)=2g.
```

Thus the stated sufficient threshold `Q>4A(U_g)^2=16g^2` is arithmetically
correct.  The earlier value `2g-1` would have been wrong.

## 2. Kowalski maximal-Galois exceptional set

### 2.1 Theorem and exponent: PASS

Kowalski, Theorem 6.2, assumes `g>=2`, odd characteristic, and a monic
degree-`2g` polynomial with `2g` distinct roots in the base field.  It treats
exactly

```text
C_u: y^2=f(x)(x-u),  u in A^1 - zeros(f).
```

It bounds the number of parameters for which the Frobenius polynomial is
reducible or its splitting field has degree less than `2^g g!` by

```text
O(q^(1-gamma_g) log q),
gamma_g = 1/(4g^2+3g+5),
```

with an absolute implied constant.  The proof concludes with this exponent
on pp. 27--28 of the author PDF; the theorem itself is stated on p. 19.

Item 3 of the author's erratum changes the right side on the published page
54 to

```text
g^2 q^(1-gamma_g) log q.
```

The manuscript includes exactly this missing `g^2` factor.  Its stronger
assumption `char(F_Q)>2g+1` guarantees that `f_g` is split and squarefree.
Dividing by `|U_g(F_Q)|=Q-2g` gives the stated probability bound when
`Q>4g`.

Primary sources:

- Kowalski, Theorem 6.2 and pp. 27--28,
  [author PDF](https://people.math.ethz.ch/~kowalski/large-sieve-monodromy.pdf),
  [DOI 10.1515/CRELLE.2006.094](https://doi.org/10.1515/CRELLE.2006.094).
- Kowalski, item 3 of
  [the author's erratum](https://people.math.ethz.ch/~kowalski/erratum-large-sieve-monodromy.pdf).

One explanatory sentence should be added.  Theorem 6.2 phrases the bad set
as "reducible or splitting-field degree less than `2^g g!`".  To obtain the
manuscript's formulation `Gal not isomorphic to W_{2g}`, explicitly recall
that the functional equation embeds the Galois action in the signed
permutation group `W_{2g}`, whose order is `2^g g!`; full degree is therefore
equivalent to the full Weyl group.

The 2006 proof notes that its full mod-ell monodromy input was then quoted
from unpublished work of J.-K. Yu.  A subsequent published proof is available
in C. Hall, *Big symplectic or orthogonal monodromy modulo ell*, Duke Math.
J. 141 (2008), 179--203,
[DOI 10.1215/S0012-7094-08-14115-8](https://doi.org/10.1215/S0012-7094-08-14115-8).
Adding this citation would make the provenance chain more robust.

## 3. Square-field maximal Galois group implies LI

Status: **PASS**.

For `Q=s^2`, the normalized roots `beta_j=alpha_j/s` are roots of a
polynomial in `Q[X]`, have the same splitting field and Galois permutation
action as the `alpha_j`, and occur in inverse pairs.  Hence their pair product
is the positive rational number `m=1`.

Kowalski, Proposition 2.4(2), states for `g>=2` that under full `W_{2g}`
Galois group and `m=1`, the rationalized multiplicative relation space is
exactly `1 direct-sum G(M)`.  In the paper's notation this is the trivial
inverse-pair relation space: relation coordinates are equal on the two roots
in every inverse pair.  See also equations (1.6)--(1.7), where Kowalski
identifies this condition with rational independence of
`1,theta_1,...,theta_g`.

Given an additive relation

```text
sum_j a_j theta_j + b pi = 0,
```

clearing denominators and exponentiating twice gives a multiplicative
relation with pair coordinates `(2a_j,0)`.  Equality of the two coordinates
forces every `a_j=0`; then `b=0`.  The manuscript correctly uses only the
rationalized relation space and does not need an integral saturation claim.

Primary source:

- E. Kowalski, *The Large Sieve, Monodromy, and Zeta Functions of Algebraic
  Curves, 2: Independence of the Zeros*, equations (1.6)--(1.7) and their
  angle-independence explanation on pp. 3--4, and Proposition 2.4(2) with
  equation (2.5) on pp. 11--13 of the
  [author PDF](https://people.math.ethz.ch/~kowalski/relations-roots.pdf).
  See also the
  [institutional copy of the published article](https://www.research-collection.ethz.ch/bitstreams/59b37028-1616-4669-9a47-f17206f0942f/download);
  [DOI 10.1093/imrn/rnn091](https://doi.org/10.1093/imrn/rnn091).

## 4. Haar symplectic hard edge

### 4.1 Finite kernel and normalization: PASS

Weyl integration for Haar `USp(2g)` on the positive eigenangles gives the
rank-`g` projection with orthonormal functions

```text
(2/pi)^(1/2) sin(k theta),   1<=k<=g,   0<theta<pi.
```

The normalization can be checked without importing a random-matrix limit.
The type-`C_g` Weyl denominator reduces, up to a constant, to

```text
det[sin(k theta_j)]_(k,j=1)^g
 = 2^(g(g-1)/2) product_j sin(theta_j)
   product_(i<j) (cos(theta_i)-cos(theta_j)).
```

Squaring this identity gives the Haar joint density relative to
`dtheta_1...dtheta_g`.  Since
`integral_0^pi sin(k theta)sin(l theta)dtheta=(pi/2)delta_(k,l)`, its
correlation kernel is exactly the projection displayed above.

Under `y=(2g+1)theta/(2pi)`, the Jacobian multiplies the kernel by
`2pi/(2g+1)`, giving exactly

```text
K_g(x,y) = 4/(2g+1) sum_{k=1}^g
           sin(2pi kx/(2g+1)) sin(2pi ky/(2g+1)).
```

Writing `d=2g+1`, this is a Riemann sum:

```text
K_g(x,y) -> 4 integral_0^(1/2) sin(2pi ux)sin(2pi uy) du
          = (2/pi) integral_0^pi sin(tx)sin(ty) dt
          = sinc_pi(x-y)-sinc_pi(x+y).
```

Thus both the scale `d/(2pi)` and the limiting kernel in (1.4) are correct.
The diagonal envelope `K_g(y,y)<=4g/(2g+1)<2` is also correct.

### 4.2 Point-process convergence: PASS WITH WORDING REPAIR

Soshnikov's Theorem 5 does not literally say that local uniform kernel
convergence plus a diagonal bound, by themselves, imply weak convergence.
It assumes weak-operator convergence and convergence of local traces.  The
manuscript's kernels do satisfy those hypotheses, but the missing bridge
should be stated:

1. extend the finite kernels by zero off `[0,d/2]`, and if desired extend
   both finite and limiting kernels by zero to the negative half-line;
2. local uniform convergence on every compact set gives convergence on
   compactly supported `L^2` test functions;
3. all operators are orthogonal projections/contractions, so density of
   compactly supported functions upgrades this to weak-operator convergence;
4. local uniform diagonal convergence together with the common bound `2`
   gives convergence of `Tr(1_B K_g 1_B)` for every bounded Borel `B`.

Soshnikov, Theorem 5, then gives weak convergence of the DPPs.  The estimate
`sup_g E Xi_g([0,eta])<=2eta` correctly prevents escape through zero, and
the limiting intensity at the singleton `{0}` is zero.

Primary source:

- A. Soshnikov, *Determinantal Random Point Fields*, Theorem 5 (weak
  convergence), arXiv version pp. 15--16,
  [arXiv:math/0002099v4](https://arxiv.org/pdf/math/0002099).

## 5. Projection-DPP facts

Status: **PASS**.

The limiting kernel is the orthogonal projection, under the unitary sine
transform, onto frequencies `[0,pi]`.  Consequently

```text
integral_0^infinity |K(x,y)|^2 dy = K(x,x).
```

Soshnikov's Theorem 3 gives existence and uniqueness of the DPP because the
kernel is Hermitian, locally trace class, and `0<=K<=1`.  Definition 2,
equation (1.5), gives factorial moments; Definition 3, equation (1.20), gives
the determinantal correlations.  From the one- and two-point correlations,
for a compactly supported real `f`,

```text
Var(sum f(x))
 = integral f(x)^2 K(x,x) dx
   - double_integral f(x)f(y)|K(x,y)|^2 dxdy.
```

Using the projection identity symmetrizes this to

```text
1/2 double_integral (f(x)-f(y))^2 |K(x,y)|^2 dxdy.
```

The factor `1/2` in the manuscript is therefore correct.  The truncation
argument for the noncompact `f_lambda` is justified by its `L^1` and `L^2`
tails and the diagonal bound.

The crowding claim is also correct.  Equation (1.5) gives

```text
E (N_I)_N = integral_{I^N} det(K(x_i,x_j)) dx_1...dx_N.
```

For distinct positive `x_i`, this determinant is the Gram determinant of
`sqrt(2/pi) sin(t x_i)` in `L^2(0,pi)`.  These functions are linearly
independent: differentiating an identity at zero yields a Vandermonde system
in the distinct numbers `x_i^2`.  The determinant is therefore positive off
the diagonals, its integral is positive, and `P(N_I>=N)>0`.

Primary source locations:

- Soshnikov, Definition 2 and equation (1.5), pp. 3--4;
- Definition 3 and equation (1.20), pp. 7--8;
- Theorem 3 (`0<=K<=1` existence/uniqueness), p. 12;
- Theorem 5 (weak convergence), pp. 15--16;
- [arXiv:math/0002099v4](https://arxiv.org/pdf/math/0002099).

Recommended wording repair: cite these theorem/equation numbers at the first
use of existence, convergence, factorial moments, and the projection
variance formula.  A single unlocated citation to Soshnikov at the convergence
step is too imprecise for a proof whose selling point is verifiability.

## 6. Bibliographic metadata audit

The following records were checked against publisher or institutional
metadata.

1. `KatzSarnak1999`: title, authors, series, volume 45, publisher, and the
   conventional bibliographic year 1999 are correct.  Add
   `doi = {10.1090/coll/045}`.  The official AMS record also lists ISBN
   978-0-8218-1017-0 for the original edition.
2. `Kowalski2006`: journal, issue/volume 601, pages 29--69, and year 2006 are
   correct.  Add `doi = {10.1515/CRELLE.2006.094}`.
3. `Kowalski2008`: the robust journal form is *International Mathematics
   Research Notices*, volume 2008, article ID `rnn091`, 57 pages.  Add
   `doi = {10.1093/imrn/rnn091}`; the existing note `Art. ID rnn091` is
   acceptable.
4. `Soshnikov2000`: journal, volume 55, number 5, pages 923--975, and year
   2000 are correct.  Add
   `doi = {10.1070/RM2000v055n05ABEH000321}`.
5. `KowalskiErratum`: the PDF itself is undated.  The current `year={2008}`
   was not verified from the document or a publisher record.  Prefer an
   undated `@misc` entry with the author URL and a note such as
   `Undated author errata, item 3`, unless an archived timestamp is supplied.
6. Add a Hall record if the manuscript wants a fully published provenance
   chain for the mod-ell monodromy input:

```bibtex
@article{Hall2008Monodromy,
  author  = {Chris Hall},
  title   = {Big symplectic or orthogonal monodromy modulo $\ell$},
  journal = {Duke Math. J.},
  volume  = {141},
  number  = {1},
  pages   = {179--203},
  year    = {2008},
  doi     = {10.1215/S0012-7094-08-14115-8}
}
```

## Release decision for this ledger

Do not call the focused paper source-verified until the half-Tate Frobenius
orientation is corrected.  After that repair, the large-sieve, square-field
LI, hard-edge normalization, and projection-DPP imports pass this audit.  The
only remaining source-specific uncertainty is the exact wording of
Katz--Sarnak, Theorem 9.2.6(4)--(5); the cleanest resolution is to replace that
one imported constant by the direct tame-curve cohomology calculation above,
which is both stronger and easier for a referee to verify.

## Post-audit repair disposition

The root integration pass corrected the failed Frobenius convention exactly
as prescribed: `eta_s(Fr_geom)=s^{-1}` and
`eta_s(Fr_arith)=s`.  It now states that `eta_s` has weight `-1` and that the
twisted rank-`2g` sheaf has weight zero.  The unresolved attribution to
Katz--Sarnak Theorem 9.2.6 was eliminated rather than assumed: the manuscript
now proves the stronger character estimate directly from tameness, absence of
geometric invariants, Grothendieck--Ogg--Shafarevich, the trace formula, and
Deligne's weight bound.  The Soshnikov operator hypotheses and the recommended
bibliographic DOI/erratum repairs were also inserted.  Thus the original
`FAIL` and `UNRESOLVED` items in this dated audit have concrete dispositions;
external specialist review remains separate and undone.
