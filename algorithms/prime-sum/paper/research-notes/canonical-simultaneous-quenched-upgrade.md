# Quenched-law upgrade for the canonical simultaneous theorem

Status: proof sketch for adversarial review, 2026-08-17.  This note strengthens
the candidate theorem in `canonical-simultaneous-hyperelliptic-law.md`.  It is
not yet manuscript text and makes no priority claim.

## 1. Why the full law is the right headline

For a curve satisfying LI, the normalized degree-race sequence has not only a
sign density but a complete limiting probability distribution.  Retaining
that distribution makes the simultaneous theorem stronger and shortens its
analytic bridge: coefficient coupling gives a direct Wasserstein estimate,
so the bounded-density estimate used only for the sign functional is no
longer needed.

Let `P_2(R)` be the probability measures on the real line with finite second
moment, equipped with `W_2`.  For the family and notation of the canonical
note, define

\[
 \nu_{g,t,\lambda}
 =\frac12\mathcal L_\Phi\!\left(
 c_{g,\lambda}^{(0)}+
 \sum_{j=1}^g b_{g,\lambda}(\vartheta_j)\cos\Phi_j\right)
 +\frac12\mathcal L_\Phi\!\left(
 c_{g,\lambda}^{(1)}+
 \sum_{j=1}^g b_{g,\lambda}(\vartheta_j)\cos\Phi_j\right).
\tag{1.1}
\]

Under LI this is exactly the natural limiting distribution of the normalized
race as the degree endpoint varies.  On the exceptional non-LI set, assign
any fixed element of `P_2(R)`.

For a locally finite point measure `xi` on `[0,infinity)`, put

\[
 a_\lambda(y)=\frac{4\lambda}
 {\sqrt{\lambda^2+(2\pi y)^2}},\qquad
 \nu_\lambda(\xi)=\mathcal L_\Phi\!\left(
 1+\sum_{y\in\xi}a_\lambda(y)\cos\Phi_y\right),
\tag{1.2}
\]

whenever the coefficient sequence is square summable.

## 2. Strengthened candidate theorem

**Theorem (simultaneous quenched critical law).**  Fix `lambda>0`.  Let
`p_g`, `Q_g`, and the pencil

\[
 C_{g,t}:y^2=\prod_{a=1}^{2g}(x-a)(x-t)
\]

be as in the canonical note, with `Q_g` an odd square and

\[
 \frac{\log Q_g}{g^2\log(g+2)}\longrightarrow\infty.
\tag{2.1}
\]

If `t_g` is uniform on the punctured parameter line, then, as random elements
of `P_2(R)`,

\[
 \nu_{g,t_g,\lambda}\ \Longrightarrow\
 \nu_\lambda(\Pi_{\rm Sp}).
\tag{2.2}
\]

The limiting random probability measure is not almost surely constant.
Moreover, it is almost surely absolutely continuous, its positive-half-line
mass is not almost surely constant, and consequently

\[
 \nu_{g,t_g,\lambda}((0,\infty))\ \Longrightarrow\
 \nu_\lambda(\Pi_{\rm Sp})((0,\infty)).
\tag{2.3}
\]

The expectation of the left side in (2.3) converges to the expectation of the
right side.

Equation (2.3) is the earlier race-density theorem.  Equation (2.2) is the
headline result.

## 3. Exact Wasserstein coupling

Let `theta=(theta_1,...,theta_g)` and `phi=(phi_1,...,phi_g)` be ordered
positive eigenangle vectors.  Couple the same parity Bernoulli variable and
the same independent phases in the two laws (1.1).  Since the parity centers
do not depend on the angles,

\[
 W_2\bigl(\nu_{g,\lambda}(\theta),
           \nu_{g,\lambda}(\phi)\bigr)^2
 \leq \frac12\sum_{j=1}^g
 \bigl(b_{g,\lambda}(\theta_j)
       -b_{g,\lambda}(\phi_j)\bigr)^2.
\tag{3.1}
\]

The derivative estimate already proved in the canonical note gives

\[
 \|b'_{g,\lambda}\|_\infty
 \leq \frac{2(2g+1+\lambda)}{\lambda}.
\tag{3.2}
\]

Hoffman--Wielandt angle matching for the fixed Hilbert--Schmidt metric then
shows that the central map

\[
 T_{g,\lambda}:{\rm USp}(2g)\longrightarrow P_2(\mathbb R),
 \qquad T_{g,\lambda}(U)=\nu_{g,\lambda}(\Theta_U),
\]

is `O_lambda(g)`-Lipschitz.  This replaces the weaker
`O_lambda(g^(5/2))` sign-functional estimate and removes the three-Bessel
density lemma from the main proof.

To transfer from arithmetic Frobenius classes to Haar measure, test against
bounded 1-Lipschitz functions `H:P_2(R)->R`.  The composite `H o T` is a
bounded central `O_lambda(g)`-Lipschitz function on `USp(2g)`.  Heat smoothing,
the Katz--Sarnak character estimate, the explicit level-cover Betti bound, and
the heat-trace estimate from the canonical note therefore give

\[
 d_{\rm BL}\bigl((T_{g,\lambda})_*\mu_{g,Q_g},
                 (T_{g,\lambda})_*\mu_{{\rm Haar},g}\bigr)
 \longrightarrow0.
\tag{3.3}
\]

For example, taking heat time `s=g^(-8)` makes the smoothing term
`O_lambda(g^(-2))`; the field growth (2.1) absorbs the heat trace and level
cover.  The density-one LI estimate permits replacing the model law by the
actual race law.

## 4. Haar-to-hard-edge convergence in `P_2`

Put the finite and limiting processes on the **closed** half-line
`[0,infinity)`.  This is essential: vague convergence on `(0,infinity)` would
not detect a point escaping to zero.  The finite kernels converge locally
uniformly through the hard edge, the limit has no point at zero, and
`K_g(y,y)<2` gives

\[
 \sup_g\mathbb E\Xi_g([0,\epsilon])\leq2\epsilon.
\tag{4.1}
\]

The canonical note also proves local coefficient convergence and the uniform
large-`y` tail estimate

\[
 \lim_{R\to\infty}\sup_g
 \mathbb P\left(\sum_{y\in\Xi_g,\,y>R}
 a_{g,\lambda}(y)^2>\eta\right)=0.
\tag{4.2}
\]

On a Skorokhod realization, choose a deterministic `R` at which the limiting
process has no atom.  Vague convergence on the closed half-line, simplicity,
and local uniform coefficient convergence match all points in `[0,R]` and
make their finite squared difference tend to zero.  After padding the two
tails by zeros, their remaining squared difference is at most

\[
 2\sum_{y\in\Xi_g,\,y>R}a_{g,\lambda}(y)^2
 +2\sum_{y\in\Pi_{\rm Sp},\,y>R}a_\lambda(y)^2.
\tag{4.3}
\]

Take `R` large using (4.2) and the almost-sure square summability of the limit,
and then let `g` tend to infinity.  Thus the matched coefficient vectors
converge in `ell^2` in probability.  Couple the same phases and parity.  Since
both parity centers tend to one,

\[
 W_2\bigl(\nu_{g,\lambda}(\Xi_g),
           \nu_\lambda(\Pi_{\rm Sp})\bigr)^2
 \leq \max_{\epsilon=0,1}|c_{g,\lambda}^{(\epsilon)}-1|^2
 +\frac12\sum_j|a_{g,j}-a_j|^2
 \longrightarrow0.
\tag{4.4}
\]

This proves Haar convergence of the random probability measures.  Combining
(3.3) and (4.4) proves (2.2).

For measurability, Borel-enumerate the atoms increasingly, pad a finite
configuration by infinity, and put `a_lambda(infinity)=0`.  The square-sum
domain is Borel and the coefficient map into the separable space `ell^2` is
Borel.  The map

\[
 (c,u)\longmapsto\mathcal L\left(c+\sum_j u_j\cos\Phi_j\right)
\]

is continuous from `R times ell^2` to `P_2(R)` by the coupling estimate (3.1).
Assigning a fixed fallback law on the nonsquare-summable complement makes the
conditional-law map globally Borel.

## 5. Absolute continuity and the density corollary

The symplectic hard-edge process has no point at zero, is locally finite on the
closed half-line, is almost surely infinite, and has a square-summable
coefficient sequence.  It therefore has a first positive point.  Conditional
on the point configuration, the first term
`a_lambda(y_1) cos Phi_1` has an absolutely continuous arcsine law and is
independent of the remaining `L^2`-convergent series.  Their convolution is
absolutely continuous.  Thus

\[
 \nu_\lambda(\Pi_{\rm Sp})(\{0\})=0
 \quad\hbox{almost surely}.
\tag{5.1}
\]

The map `mu -> mu((0,infinity))` is continuous for weak convergence at every
measure satisfying (5.1).  Since `W_2` convergence implies weak convergence,
the continuous-mapping theorem proves (2.3).  Boundedness in `[0,1]` proves
the expectation statement.

## 6. Nondegeneracy of the limiting random law

Every conditional law in (1.2) has mean one and conditional variance

\[
 V_\lambda(\xi)
 =\frac12\sum_{y\in\xi}a_\lambda(y)^2
 =\sum_{y\in\xi}f_\lambda(y),\qquad
 f_\lambda(y)=\frac{8\lambda^2}
 {\lambda^2+4\pi^2y^2}.
\tag{6.1}
\]

The kernel

\[
 K_{\rm Sp}(x,y)=S(x-y)-S(x+y)
\]

has the exact representation

\[
 K_{\rm Sp}(x,y)=\frac2\pi\int_0^\pi\sin(tx)\sin(ty)\,dt.
\]

It is therefore the orthogonal projection kernel obtained from the sine
transform with band `[0,pi]`, and
`integral |K_Sp(x,y)|^2 dy=K_Sp(x,x)`.  Since
`f_lambda` lies in both `L^1` and `L^2`, approximation by compactly supported
functions and the projection-DPP variance identity give

\[
 {\rm Var}\,V_\lambda(\Pi_{\rm Sp})
 =\frac12\int_0^\infty\!\int_0^\infty
   (f_\lambda(x)-f_\lambda(y))^2
   |K_{\rm Sp}(x,y)|^2\,dx\,dy.
\tag{6.2}
\]

The integral is finite; for example, it is at most
`2 integral f_lambda(x)^2 K_Sp(x,x) dx`.  It is strictly positive:
`f_lambda` is strictly
decreasing and the real-analytic kernel is not zero on a set of positive
two-dimensional measure.  Therefore the conditional variance is genuinely
random.  If `nu_lambda(Pi_Sp)` were almost surely a fixed probability measure,
its variance would be constant, contradicting (6.2).  This proves the
nondegeneracy assertion without numerical evidence.

## 7. Nondegeneracy of the scalar density functional

The preceding conditional-variance argument does not by itself show that the
single number

\[
 F_\lambda(\xi)=\nu_\lambda(\xi)((0,\infty))
\]

varies with `xi`.  A separate crowding argument does.

Write `S_xi=sum_y a_lambda(y) cos Phi_y`.  For every nonempty square-summable
coefficient sequence,

\[
 \mathbb P_\Phi(|S_\xi|<1)>0.
\tag{7.1}
\]

Indeed, take a finite head whose tail has sufficiently small variance.  The
tail lies in `(-1/2,1/2)` with positive probability by Chebyshev, while all
head cosines lie sufficiently close to zero with positive probability.  By
symmetry and absolute continuity,

\[
 F_\lambda(\xi)=\frac12\left(1+
 \mathbb P_\Phi(|S_\xi|<1)\right)>\frac12.
\tag{7.2}
\]

Choose a compact interval `I` close to, but bounded away from, zero so that
`a_lambda(y)>=a_0>2` on `I`.  For every integer `N`,

\[
 \mathbb P(\Pi_{\rm Sp}(I)\geq N)>0.
\tag{7.3}
\]

The factorial-moment integral is strictly positive: its integrand is the Gram
determinant of the linearly independent functions
`t -> sin(t x_j)` in `L^2(0,pi)` for distinct points `x_j` in `I`.

On the event in (7.3), select `N` points.  Their marked sum has characteristic
function `prod_(j<=N) J_0(a_j t)`, with every `a_j` in `[a_0,4]`.  Splitting
the Fourier integral into a small neighborhood of zero, a compact annulus,
and the large-`t` region gives uniformly

\[
 \left\|p_{\sum_{j=1}^N a_j\cos\Phi_j}\right\|_\infty
 \leq \frac{C_{\lambda,I}}{\sqrt N}.
\tag{7.4}
\]

For small `t`, use the power series bound
`|J_0(a_jt)|<=exp(-c_I t^2)`; on the compact annulus use
`sup |J_0|<1`; at infinity use `|J_0(u)|<=2|u|^(-1/2)`.
Convolution with the independent contribution from all other points cannot
increase the density norm.  Consequently, on the positive-probability event
(7.3),

\[
 \frac12<F_\lambda(\Pi_{\rm Sp})
 \leq\frac12+\frac{C_{\lambda,I}}{\sqrt N}.
\tag{7.5}
\]

If the scalar functional were almost surely the constant `c`, (7.2) would
give `c>1/2`, while (7.5) with sufficiently large `N` would make it strictly
smaller than `c` on an event of positive probability.  Thus the scalar race
density limit is nonconstant.  In fact its essential infimum is `1/2`, though
that value is not attained almost surely.

## 8. Audit gates

Before this upgrade enters a manuscript, independently check:

1. the `O_lambda(g)` group-metric Lipschitz constant in (3.1)--(3.2);
2. the bounded-Lipschitz heat transfer in (3.3), including the harmless
   normalization of bounded tests;
3. measurability of `xi -> nu_lambda(xi)` as a `P_2(R)`-valued map;
4. the projection normalization and factor `1/2` in (6.2);
5. the closed-hard-edge matching lemma, including the no-escape estimate at
   zero;
6. the crowding and uniform Fourier bounds in (7.3)--(7.5);
7. the literature for quenched random probability-measure limits, not only
   sign-density limits.

This upgrade does not change the honest formalization boundary.  The coupling,
parity-center algebra, coefficient limits, and determinantal variance identity
are plausible Lean targets.  The Katz--Sarnak and Kowalski arithmetic inputs
are not presently available in mathlib and must remain explicitly imported
theorems rather than silently assumed formal facts.
