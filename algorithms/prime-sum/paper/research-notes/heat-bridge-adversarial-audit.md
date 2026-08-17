# Adversarial audit of the compact-group heat bridge

Status: independent internal audit, 2026-08-17. This note checks only the
compact-Lie-group step used in canonical-simultaneous-hyperelliptic-law.md and
canonical-simultaneous-quenched-upgrade.md. It does not re-audit the arithmetic
construction of the Frobenius measure or the claimed level-cover Betti bound.

## 1. Verdict

**PASS, with two wording/normalization repairs and no change to the field-growth
condition.** With probability Haar measure, the metric

\[
  \langle X,Y\rangle=-\frac12\operatorname{Tr}(XY),
\]

and the positive Laplace--Beltrami operator specified below, the heat bridge is
valid uniformly in \(g\). There is no missing group-volume factor, no missing
power of the representation dimension, and no hidden exponential worse than
\(\exp(O(g^2\log g))\) at polynomial heat time.

The two repairs are:

1. The sum
   \(\sum_\rho(\dim\rho)^2e^{-2s\kappa_\rho}\) is the heat kernel
   \(K_{2s}(e)\), not \(K_s(e)\).
2. The manuscript should state that the heat kernel is a density relative to
   **Haar probability measure**. If one instead writes it relative to
   unnormalized Riemannian volume, a volume factor appears in the density, but
   it cancels after normalization. The proof below never uses that convention.

These are not mathematical failures of (6.5)--(6.7). They are exact repairs
needed to make the convention audit-proof.

## 2. Repaired heat-transfer proposition

Let \(G_g={\rm USp}(2g)\), let \(m_g\) be Haar probability measure, and give
\(G_g\) the bi-invariant metric above. Put

\[
  D_g=\dim G_g=2g^2+g.
\]

Let

\[
  \mathcal A_g=-\sum_{j=1}^{D_g}X_j^2
\]

be the positive Laplace--Beltrami operator, where the \(X_j\) are an
orthonormal basis of left-invariant vector fields, and put
\(P_s=e^{-s\mathcal A_g}\). For an irreducible representation \(\rho\), write
\(d_\rho=\dim\rho\) and

\[
  \mathcal A_g\chi_\rho=\kappa_\rho\chi_\rho.
\]

Suppose that \(\mu\) is a conjugation-invariant probability measure on \(G_g\)
and that, for every nontrivial irreducible \(\rho\),

\[
  \left|\int_{G_g}\chi_\rho\,d\mu\right|
  \leq \varepsilon_g d_\rho.
\tag{2.1}
\]

Then every bounded central \(L\)-Lipschitz function \(h\), with
\(\lVert h\rVert_\infty\leq1\), satisfies for \(0<s\leq1\)

\[
 \boxed{
  \left|\int h\,d\mu-\int h\,dm_g\right|
  \leq 2L\sqrt{2D_gs}
   +\varepsilon_g
    \left(\sum_\rho d_\rho^2e^{-2s\kappa_\rho}\right)^{1/2}.}
\tag{2.2}
\]

If \(\lVert h\rVert_\infty\leq M\) instead, the last term in (2.2) is
multiplied by \(M\).

There is an absolute constant \(C\) such that

\[
 \boxed{
  \sum_\rho d_\rho^2e^{-2s\kappa_\rho}
  \leq
  \exp\!\bigl(Cg^2\log(g+2)\bigr)
  s^{-(2g^2+g+1)/2}}
  \qquad(0<s\leq1).
\tag{2.3}
\]

In particular, the weaker form used in the canonical note,

\[
  \sum_\rho d_\rho^2e^{-2s\kappa_\rho}
  \leq \exp\!\bigl(Cg^2\log(g+2)\bigr)s^{-Cg^2},
\]

is correct.

## 3. Metric and Casimir normalization from first principles

Use the maximal torus

\[
 T(\theta)=\operatorname{diag}
 (e^{i\theta_1},\ldots,e^{i\theta_g},
  e^{-i\theta_1},\ldots,e^{-i\theta_g}).
\]

For

\[
 X(x)=\operatorname{diag}(ix_1,\ldots,ix_g,-ix_1,\ldots,-ix_g)
\]

and similarly \(X(y)\), direct matrix multiplication gives

\[
 -\frac12\operatorname{Tr}(X(x)X(y))=\sum_{j=1}^gx_jy_j.
\tag{3.1}
\]

Thus the torus-angle metric is exactly Euclidean; there is no factor \(2\),
\(g\), or \(2\pi\). The type-\(C_g\) roots in this normalization are
\(e_i\pm e_j\) and \(2e_i\), and

\[
  \varrho=(g,g-1,\ldots,1).
\]

Irreducibles are indexed by partitions

\[
  \lambda=(\lambda_1\geq\cdots\geq\lambda_g\geq0),
\]

and the Casimir eigenvalue is exactly

\[
 \boxed{
  \kappa_\lambda
  =\lVert\lambda+\varrho\rVert^2-\lVert\varrho\rVert^2
  =\sum_{i=1}^g\lambda_i
    \bigl(\lambda_i+2(g-i+1)\bigr).}
\tag{3.2}
\]

As a normalization check, for \(g=1\), \(G_1={\rm SU}(2)\). The three
matrices \(i\sigma_1,i\sigma_2,i\sigma_3\) are orthonormal for (3.1), and on
the defining representation

\[
  -\sum_{j=1}^3(i\sigma_j)^2=3I.
\]

Formula (3.2) gives \(\kappa_{(1)}=3\), so there is no factor-of-two
discrepancy in the heat time. If the negative Killing form were used instead,
the metric would be larger by a factor proportional to \(g+1\), and the
Casimir would be smaller by that factor. That convention is not used here.

If \(R=\lambda_1\), (3.2) immediately gives

\[
  \kappa_\lambda\geq R^2.
\tag{3.3}
\]

## 4. Type-\(C_g\) dimension estimate and heat trace

The Weyl dimension formula in the same coordinates is

\[
\begin{split}
 d_\lambda={}&
 \prod_{i=1}^g
 \frac{\lambda_i+g-i+1}{g-i+1}\\
 &\times\prod_{1\leq i<j\leq g}
 \frac{\lambda_i-\lambda_j+j-i}{j-i}
 \frac{\lambda_i+\lambda_j+2g-i-j+2}{2g-i-j+2}.
\end{split}
\tag{4.1}
\]

There are \(g^2\) factors in (4.1). Every denominator is at least one and,
when \(\lambda_1=R\), every numerator is at most \(2(R+g+1)\). Hence

\[
  d_\lambda\leq[2(R+g+1)]^{g^2}.
\tag{4.2}
\]

The number of partitions with largest part \(R\) is at most \((R+1)^g\).
Combining (3.3)--(4.2) and
\(R+g+1\leq(g+1)(R+1)\) gives, with
\(N=2g^2+g\),

\[
\begin{split}
 K_{2s}(e)
 &=\sum_\lambda d_\lambda^2e^{-2s\kappa_\lambda}\\
 &\leq[2(g+1)]^{2g^2}
   \sum_{R=0}^\infty(R+1)^N e^{-2sR^2}.
\end{split}
\tag{4.3}
\]

The last sum is bounded by its maximum plus its Gaussian integral. Using

\[
 \int_0^\infty x^Ne^{-2sx^2}\,dx
 =\frac12(2s)^{-(N+1)/2}
   \Gamma\!\left(\frac{N+1}{2}\right)
\]

and the elementary maximum of \(x^Ne^{-2sx^2}\), one obtains

\[
 \sum_{R=0}^\infty(R+1)^Ne^{-2sR^2}
 \leq \exp\!\bigl(CN\log(N+2)\bigr)s^{-(N+1)/2}
\tag{4.4}
\]

for \(0<s\leq1\). Equations (4.3)--(4.4) prove (2.3). This derivation
also shows exactly where the \(g^2\log g\) loss enters; it is not a suppressed
fixed-rank heat-kernel constant.

## 5. Peter--Weyl insertion and absence of a volume factor

Normalize Haar measure by \(m_g(G_g)=1\). Irreducible characters are then an
orthonormal basis of the central subspace of \(L^2(G_g,m_g)\). Write

\[
  h=\sum_\rho\widehat h(\rho)\chi_\rho,
  \qquad
  \sum_\rho|\widehat h(\rho)|^2=\lVert h\rVert_2^2.
\]

Heat smoothing gives the uniformly convergent expansion

\[
  P_sh=\sum_\rho e^{-s\kappa_\rho}
       \widehat h(\rho)\chi_\rho.
\tag{5.1}
\]

The trivial character cancels between \(\mu\) and \(m_g\). Applying (2.1),
Cauchy--Schwarz, and \(\lVert h\rVert_2\leq\lVert h\rVert_\infty\) gives

\[
\begin{split}
 \left|\int P_sh\,d(\mu-m_g)\right|
 &\leq\varepsilon_g
   \sum_{\rho\ne1}e^{-s\kappa_\rho}
       |\widehat h(\rho)|d_\rho\\
 &\leq\varepsilon_g\lVert h\rVert_\infty
   \left(\sum_\rho d_\rho^2e^{-2s\kappa_\rho}\right)^{1/2}.
\end{split}
\tag{5.2}
\]

The final sum is \(K_{2s}(e)\), the group heat-kernel density at the identity
relative to Haar probability measure. It also equals the full Peter--Weyl
spectral trace because an irreducible of dimension \(d_\rho\) contributes
\(d_\rho^2\) matrix coefficients. No extra \(d_\rho\) is missing.

If \(dv\) denotes Riemannian volume and \(V_g=\int_Gdv\), then
\(dm_g=dv/V_g\), and the numerical value of a heat-kernel *density* changes by
\(V_g\). Formula (5.2) is written relative to \(dm_g\), where the exact
spectral identity is the displayed one. The Markov semigroup and (2.2) are
independent of this density convention. Thus there is no hidden \(V_g\) in the
arithmetic comparison.

## 6. Uniform Brownian smoothing

A compact group with a bi-invariant metric has nonnegative sectional, hence
nonnegative Ricci, curvature. The distributional Laplacian comparison

\[
  \Delta d(e,\cdot)^2\leq2D_g
\]

for the Markov generator corresponding to \(P_s=e^{-s\mathcal A_g}\) implies

\[
  \int_{G_g}d(e,x)^2K_s(x)\,dm_g(x)\leq2D_gs.
\tag{6.1}
\]

The convention is visible already in Euclidean space: this generator has
coordinate variance \(2s\). Therefore, for every \(L\)-Lipschitz \(h\),

\[
\begin{split}
 |P_sh(x)-h(x)|
 &\leq L\int d(e,y)K_s(y)\,dm_g(y)\\
 &\leq L\sqrt{2D_gs}.
\end{split}
\tag{6.2}
\]

Using (6.2) once for \(\mu\) and once for \(m_g\), then (5.2), proves (2.2).
The constant in the manuscript's (6.4) may therefore be taken to be
\(C_0=\sqrt2\), uniformly in \(g\). Cut-locus nonsmoothness causes no
additional constant: the squared-distance comparison holds in the
barrier/distributional sense and can equivalently be obtained by smooth
approximation before applying the heat semigroup.

## 7. Insertion of the Katz--Sarnak character bound

Katz--Sarnak, Theorem 9.2.6(5), states with normalized counting measure and
normalized Haar measure that

\[
 \left|\int\chi_\rho\,d\mu_{g,Q}
       -\int\chi_\rho\,dm_g\right|
 \leq\frac{2C_gd_\rho}{\sqrt Q}
\tag{7.1}
\]

for nontrivial irreducible \(\rho\), under the theorem's size hypotheses. Thus
(2.1) holds with

\[
  \varepsilon_g=\frac{2C_g}{\sqrt Q}.
\]

Assuming the separately audited level-cover estimate

\[
  C_g\leq(2g+1)3^{4g^2},
\tag{7.2}
\]

(2.2)--(2.3) give

\[
 \left|\int h\,d\mu_{g,Q}-\int h\,dm_g\right|
 \leq2L\sqrt{2D_gs}
 +Q^{-1/2}\exp\!\bigl(Cg^2\log(g+2)\bigr)s^{-Cg^2}.
\tag{7.3}
\]

All absolute factors, including the \(2\) in (7.1), have been absorbed only
after the exact bound (2.2) was established.

## 8. The two heat-time choices

For the sign functional, the independently stated Lipschitz estimate is

\[
  L_{g,\lambda}\leq C_\lambda g^{5/2}.
\]

Taking \(s=g^{-10}\) in (7.3) gives

\[
  2L_{g,\lambda}\sqrt{2D_gs}=O_\lambda(g^{-3/2})
\]

and

\[
 Q^{-1/2}\exp\!\bigl(C_\lambda g^2\log(g+2)\bigr).
\tag{8.1}
\]

For the quenched \(P_2(\mathbb R)\)-valued map, the same-phase coupling gives
\(L_{g,\lambda}\leq C_\lambda g\). Taking \(s=g^{-8}\) gives

\[
  2L_{g,\lambda}\sqrt{2D_gs}=O_\lambda(g^{-2})
\]

with the same form (8.1) for the character term. Thus in both cases the exact
sufficient condition is

\[
 \boxed{
   \frac{\log Q_g}{g^2\log(g+2)}\longrightarrow\infty.}
\tag{8.2}
\]

Indeed, the logarithm of the second term in (8.1) is at most

\[
  -\frac12\log Q_g+C_\lambda g^2\log(g+2).
\]

The canonical choice
\(\log Q_g\geq g^2\log^2(g+2)\) therefore has ample margin. Neither
\(s=g^{-10}\) nor \(s=g^{-8}\) requires a stronger field-growth rule.

## 9. What this audit does and does not certify

Certified within the stated hypotheses:

- the exact torus metric and Casimir normalization;
- the Peter--Weyl coefficient normalization;
- the factor \(d_\rho\), rather than \(d_\rho^2\), in the character input and
  the resulting \(d_\rho^2\) heat trace after Cauchy--Schwarz;
- a uniform-in-\(g\) Brownian smoothing constant;
- the type-\(C_g\) heat-trace bound and both polynomial heat-time choices;
- the field-growth conclusion (8.2).

Not certified by this note:

- the construction of the weight-zero arithmetic sheaf;
- the level-cover degree, tameness, or Betti estimate (7.2);
- the Lipschitz estimates for the two race functionals, except for using their
  stated orders in Section 8;
- any other part of the arithmetic-to-hard-edge theorem.

## 10. Primary and standard sources checked

1. N. M. Katz and P. Sarnak, *Random Matrices, Frobenius Eigenvalues, and
   Monodromy*, Theorem 9.2.6(5), especially the exact
   \(2C\dim(\rho)/\sqrt Q\) character bound and normalized Haar convention:
   <https://web.math.princeton.edu/~nmk/RMFEM.pdf>.
2. B. C. Hall, "A new form of the Segal--Bargmann transform for Lie groups of
   compact type," *Canadian Journal of Mathematics* 51 (1999), 816--834,
   for the heat semigroup on a compact group and the dependence of heat-kernel
   density on Haar normalization:
   <https://www.cambridge.org/core/services/aop-cambridge-core/content/view/C14D1AB283C5A9A3BF7BCC83D837AD73/S0008414X00007999a.pdf/a-new-form-of-the-segal-bargmann-transform-for-lie-groups-of-compact-type.pdf>.
3. W. Fulton and J. Harris, *Representation Theory: A First Course*, Chapters
   16--24, for the type-\(C_g\) root data, Casimir formula, and Weyl dimension
   formula. The formulas needed here are reproduced and bounded explicitly in
   Sections 3--4, so no rank-dependent constant is imported from the reference.
4. The standard Laplacian comparison theorem under nonnegative Ricci curvature,
   in the form \(\Delta r^2\leq2D\). Section 6 gives the complete one-line
   semigroup consequence and fixes the Brownian generator convention.

