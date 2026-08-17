# Adversarial audit of the quenched `P_2` upgrade

Status: independent probability/point-process audit, 2026-08-17.  This note
audits only `canonical-simultaneous-quenched-upgrade.md`.  It does not audit
the arithmetic equidistribution, LI, heat-kernel, or prime-race inputs.

## 1. Verdict

The quenched upgrade is mathematically viable, but Sections 4--5 are **not
correct as written**.  The point-process state space is taken to be
`(0,infinity)`.  Vague convergence on that space does not detect points that
escape to zero: for example, `delta_(1/n)` converges vaguely to the empty
measure there, although its critical coefficient converges to `4`, not to
zero.  The asserted passage from vague convergence plus a large-`y` tail
bound to full `ell^2` coefficient convergence therefore has a genuine missing
hard-edge argument.  The same choice of state space also makes "no point at
zero" vacuous and does not by itself imply the existence of a first point.

There is a clean repair.  Regard all rescaled processes as point measures on
`[0,infinity)`.  The finite kernels converge locally uniformly on this closed
half-line, the limiting process has no atom at zero, and vague convergence
then prevents loss of points through the hard edge.  With this correction,
the coefficient coupling proves convergence in `P_2(R)`.

The other probability claims pass after filling in measurability and
integrability details.  In particular:

- the conditional-law map is Borel as a `P_2(R)`-valued map;
- the displayed phase coupling has exactly the claimed mean-square cost,
  although it is an upper bound for `W_2`, not generally the optimal coupling;
- the hard-edge process has a first positive point almost surely;
- its conditional marked law is absolutely continuous;
- the projection-DPP variance formula has the correct factor `1/2` and is
  finite and strictly positive;
- the scalar sign functional `F_lambda(Pi_Sp)` can in fact be proved
  nonconstant.  It need not remain an open assertion.

Thus the probability/point-process half is **repairable pass**, not pass as
currently written.

## 2. Measurability of the random conditional law

Let `N_s([0,infinity))` carry its vague Borel structure, and Borel-enumerate
the atoms increasingly as

\[
 0\le e_1(\xi)\le e_2(\xi)\le\cdots,
\]

padding a finite configuration by `infinity`.  Set

\[
 a_\lambda(\infty)=0,\qquad
 A_\lambda(\xi)=
   \bigl(a_\lambda(e_j(\xi))\bigr)_{j\ge1}.
\]

Every coordinate is Borel, and

\[
 \mathcal D_\lambda
 =\left\{\xi:\sum_{j\ge1}a_\lambda(e_j(\xi))^2<\infty\right\}
\]

is Borel because its defining sum is the increasing limit of Borel partial
sums.  On `D_lambda`, the map `A_lambda` is Borel into the separable Hilbert
space `ell^2` (coordinate measurability suffices).

For `c in R` and `u in ell^2`, define

\[
 \mathscr L(c,u)
 =\mathcal L\left(c+\sum_{j\ge1}u_j\cos\Phi_j\right).
\]

The series converges in `L^2` and almost surely.  Coupling the same phases
gives the fundamental estimate

\[
 W_2\bigl(\mathscr L(c,u),\mathscr L(d,v)\bigr)^2
 \le |c-d|^2+\frac12\lVert u-v\rVert_2^2.                 \tag{2.1}
\]

Consequently `mathscr L:R times ell^2 -> P_2(R)` is continuous.  It follows
that

\[
 \xi\longmapsto \nu_\lambda(\xi)=
 \mathscr L\bigl(1,A_\lambda(\xi)\bigr)                 \tag{2.2}
\]

is Borel on `D_lambda`.  Assigning, say, `delta_1` on its Borel complement
makes (2.2) a globally Borel `P_2(R)`-valued map.  Moreover,

\[
 \int x\,d\nu_\lambda(\xi)=1,\qquad
 \int (x-1)^2\,d\nu_\lambda(\xi)
 =\frac12\lVert A_\lambda(\xi)\rVert_2^2,               \tag{2.3}
\]

so it really takes values in `P_2(R)`.  The finite-genus parity mixture is
Borel by the same argument (and is automatic on its finite parameter set).

**Verdict on audit gate 3:** fail by omission in the draft; pass with
(2.1)--(2.3).

## 3. The coupling constants and the finite-to-infinite passage

### 3.1 Exact cost of the displayed coupling

For equal parity centers and equal vector length, the shared-phase coupling
has mean-square cost

\[
 \mathbb E\left|\sum_j(u_j-v_j)\cos\Phi_j\right|^2
 =\frac12\sum_j(u_j-v_j)^2.                              \tag{3.1}
\]

Thus equation (3.1) of the upgrade is correct.  It should be called an exact
cost calculation for a particular coupling, not an exact formula for the
optimal `W_2` distance.

When the finite law has the two equiprobable centers `c_g^(0),c_g^(1)` and
the limiting law has center one, couple the same parity Bernoulli and phases.
The exact cost of this coupling is

\[
 \frac12\sum_{\epsilon=0}^1|c_g^{(\epsilon)}-1|^2
 +\frac12\sum_{j\ge1}|u_{g,j}-u_j|^2.                    \tag{3.2}
\]

The `max` used in equation (4.2) of the upgrade is therefore a valid, slightly
weaker upper bound.

### 3.2 Correct coefficient-matching lemma

The following is the needed replacement for the argument around (4.1)--(4.2).

**Lemma (closed-hard-edge `ell^2` matching).**  Let `Xi_n,Xi` be random
simple locally finite point measures on `[0,infinity)`, with
`Xi_n => Xi` vaguely and `Xi({0})=0` almost surely.  Let `a_n,a` extend
continuously to zero, with `a_n -> a` locally uniformly.  Suppose

\[
 \lim_{R\to\infty}\sup_n
 \mathbb P\left(\sum_{x\in\Xi_n,\ x>R}a_n(x)^2>\eta\right)=0
 \quad(\eta>0),                                          \tag{3.3}
\]

and `sum_(x in Xi) a(x)^2<infinity` almost surely.  Enumerate increasingly
and pad finite vectors by zero.  On a Skorokhod realization of the vague
convergence,

\[
 \sum_{j\ge1}|a_n(e_j(\Xi_n))-a(e_j(\Xi))|^2
 \longrightarrow0                                      \tag{3.4}
\]

in probability.

**Proof.**  Choose a deterministic `R` at which `Xi({R})=0` almost surely;
all but countably many `R` have this property.  Vague convergence on the
closed half-line, simplicity of the limit, and `Xi({0,R})=0` imply that the
points in `[0,R]` eventually have the same cardinality and match in increasing
order.  Local uniform coefficient convergence makes the squared difference
on this compact interval tend to zero almost surely.  After padding the two
tails, their contribution is bounded by

\[
 2\sum_{x\in\Xi_n,\ x>R}a_n(x)^2
 +2\sum_{x\in\Xi,\ x>R}a(x)^2.                           \tag{3.5}
\]

First choose `R` so that the two tail terms are small in probability, using
(3.3) and almost-sure square summability of the limit, and then let `n` tend
to infinity.  This proves (3.4).  Notice that no unjustified conversion of a
uniform-in-probability bound into an almost-sure bound is required.  A further
subsequence may be taken if an almost-sure conclusion is desired.  \(\square\)


For the symplectic kernels, local uniform convergence holds on
`[0,infinity)^2`, not merely away from zero.  Also
`K_tilde_g(y,y)<2`, so for every `epsilon>0`,

\[
 \sup_g\mathbb E\Xi_g([0,\epsilon])\le2\epsilon,          \tag{3.6}
\]

which is an alternative direct no-escape estimate.  Applying the lemma,
(3.2), and the convergence of the two centers proves the required `P_2`
convergence under Haar measure.

**Verdict on Section 4:** fail on `(0,infinity)`; pass after changing the
state space to `[0,infinity)` and using the lemma above.

## 4. First point, convergence of the marked series, and atomlessness

For the limiting kernel,

\[
 K_{\rm Sp}(x,x)=1-\frac{\sin(2\pi x)}{2\pi x},
 \qquad 0\le K_{\rm Sp}(x,x)<2.                          \tag{4.1}
\]

Hence the number of points in `[0,L]` is finite almost surely, and the
process has no point at zero.  On the other hand,

\[
 \mathbb E N_L=L+O(1),\qquad
 \operatorname {Var}N_L\le\mathbb E N_L.                \tag{4.2}
\]

For fixed `K`, Chebyshev gives

\[
 \mathbb P(N_L\le K)
 \le\frac{\mathbb E N_L}{(\mathbb E N_L-K)^2}
 \longrightarrow0.                                     \tag{4.3}
\]

Monotone convergence in `L`, followed by a union over `K`, proves that the
total number of points is infinite almost surely.  Local finiteness at zero
then implies that this nonempty configuration has a least point
`y_1>0`.  This supplies the step missing from the draft's use of "the first
term."

Furthermore,

\[
 \mathbb E\sum_{y\in\Pi_{\rm Sp}}a_\lambda(y)^2
 =\int_0^\infty a_\lambda(y)^2K_{\rm Sp}(y,y)\,dy<\infty. \tag{4.4}
\]

Thus the squared coefficient sum is finite almost surely.  Conditional on a
configuration, Kolmogorov's convergence theorem gives almost-sure and `L^2`
convergence of the centered independent series.  The first summand
`a_lambda(y_1) cos(Phi_1)` has an absolutely continuous arcsine law and is
independent of the convergent remainder.  Convolution with an absolutely
continuous probability measure is absolutely continuous.  Therefore the
whole conditional law is absolutely continuous, not merely atomless at zero.

**Verdict:** pass after the closed-hard-edge/local-finiteness repair.

## 5. The density corollary

If `mu_n -> mu` weakly and `mu({0})=0`, the portmanteau theorem gives

\[
 \mu_n((0,\infty))\longrightarrow\mu((0,\infty)).        \tag{5.1}
\]

The evaluation map in (5.1) is Borel on `P_2(R)` and continuous at every
measure with no atom at zero.  Since `W_2` convergence implies weak
convergence and the limiting conditional law is almost surely absolutely
continuous, the continuous-mapping theorem proves the density convergence.
The identity function is bounded and continuous on `[0,1]`, so convergence
in distribution of these density values also gives convergence of their
expectations.  No separate uniform-integrability argument is needed.

**Verdict:** pass.

## 6. Projection-DPP variance: normalization, integrability, positivity

The kernel has the exact representation

\[
 K_{\rm Sp}(x,y)
 =\frac2\pi\int_0^\pi\sin(tx)\sin(ty)\,dt,               \tag{6.1}
\]

so it is the kernel of the orthogonal projection under the unitary sine
transform onto frequencies in `[0,pi]`.  In particular,

\[
 \int_0^\infty |K_{\rm Sp}(x,y)|^2\,dy=K_{\rm Sp}(x,x).  \tag{6.2}
\]

The conditional variance of the marked law is exactly

\[
 \frac12\sum_y a_\lambda(y)^2=\sum_y f_\lambda(y),
 \qquad
 f_\lambda(y)=\frac{8\lambda^2}{\lambda^2+4\pi^2y^2}.   \tag{6.3}
\]

Thus all factors in Section 6 of the upgrade are correct.  Here
`f_lambda in L^1 cap L^2`, and, for example,

\[
 \mathbb E\sum_y f_\lambda(y)
 =\int_0^\infty f_\lambda(x)K_{\rm Sp}(x,x)\,dx
 \le2\lVert f_\lambda\rVert_1<\infty.                   \tag{6.4}
\]

The random sum is consequently finite almost surely.  Approximation by
compactly supported functions, the standard DPP covariance identity, and
(6.2) give

\[
 \begin{aligned}
 \operatorname {Var}\!\left(\sum_yf_\lambda(y)\right)
 &=\int f_\lambda(x)^2K_{\rm Sp}(x,x)\,dx
   -\iint f_\lambda(x)f_\lambda(y)|K_{\rm Sp}(x,y)|^2\,dx\,dy\\
 &=\frac12\iint
   (f_\lambda(x)-f_\lambda(y))^2
   |K_{\rm Sp}(x,y)|^2\,dx\,dy.                         \tag{6.5}
 \end{aligned}
\]

The integrals are finite because the right side is at most
`2 integral f_lambda(x)^2 K_Sp(x,x) dx`, which is finite.  They are strictly
positive: `f_lambda` is strictly decreasing on `(0,infinity)`, while the
real-analytic kernel is nonzero on an open set off the diagonal (for example
near any off-diagonal point where (6.1) is nonzero).  Hence the integrand is
positive on a set of positive two-dimensional measure.

It follows that the conditional variance is genuinely random.  Since every
conditional law has mean one, a deterministic `P_2`-valued conditional law
would have deterministic variance, contradicting (6.5).

**Verdict on audit gate 4 and Section 6:** pass, including the factor `1/2`,
after adding the displayed integrability justification.

## 7. The scalar functional is also nonconstant

Randomness of the full conditional measure does not logically imply
randomness of the single number

\[
 F_\lambda(\xi)=\nu_\lambda(\xi)((0,\infty)).
\]

Nevertheless, for this process the scalar nonconstancy has a direct proof.

First let

\[
 S_\xi=\sum_{y\in\xi}a_\lambda(y)\cos\Phi_y.
\]

For every nonempty square-summable coefficient sequence,
`P(|S_xi|<1)>0`.  Indeed, choose a finite head so that the variance of the
tail is small; Chebyshev gives positive probability that the tail lies in
`(-1/2,1/2)`, while requiring every cosine in the head to be sufficiently
close to zero has positive probability and puts the head in the same
interval.  By symmetry and absolute continuity,

\[
 F_\lambda(\xi)
 =\frac12\left(1+\mathbb P_\Phi(|S_\xi|<1)\right)
 >\frac12.                                               \tag{7.1}
\]

Next choose a compact interval `I` sufficiently close to, but bounded away
from, zero that

\[
 a_\lambda(y)\ge a_0>2\qquad(y\in I).                   \tag{7.2}
\]

For every integer `N`,

\[
 \mathbb P\bigl(\Pi_{\rm Sp}(I)\ge N\bigr)>0.            \tag{7.3}
\]

To see this, the factorial-moment formula gives

\[
 \mathbb E(\Pi_{\rm Sp}(I))_N
 =\int_{I^N}\det(K_{\rm Sp}(x_i,x_j))_{i,j\le N}
   \,dx_1\cdots dx_N>0.                                 \tag{7.4}
\]

The determinant is positive for distinct points because (6.1) realizes it as
the Gram determinant of the linearly independent functions
`t -> sin(tx_i)` in `L^2(0,pi)`.

On the event in (7.3), select any `N` of those points and write their marked
contribution as `X_1+...+X_N`.  Its characteristic function is

\[
 \prod_{j=1}^N J_0(a_jt),\qquad a_j\in[a_0,4].
\]

This product has an elementary uniform Fourier bound.  For sufficiently
small `|t|`, the power series for `J_0` gives
`|J_0(a_jt)| <= exp(-c_I t^2)`.  On any fixed annulus away from zero,
compactness and `|J_0(u)|<1` for `u != 0` give a uniform bound `r_I<1`.
For large `|t|`, use `|J_0(u)| <= 2|u|^(-1/2)`.  Splitting the Fourier
integral into these three regions yields, for `N>=3`,

\[
 \left\|p_{X_1+\cdots+X_N}\right\|_\infty
 \le\frac1{2\pi}\int_{\mathbb R}
       \prod_{j=1}^N|J_0(a_jt)|\,dt
 \le \frac{C_{\lambda,I}}{\sqrt N}.                    \tag{7.5}
\]

Convolution with the independent contribution of all remaining points cannot
increase this density bound.  Combining (7.1) and (7.5), on the positive
probability event (7.3),

\[
 \frac12<F_\lambda(\Pi_{\rm Sp})
 \le\frac12+\frac{C_{\lambda,I}}{\sqrt N}.               \tag{7.6}
\]

If `F_lambda(Pi_Sp)` were almost surely equal to a constant `c`, then (7.1)
would give `c>1/2`, while choosing `N` large enough in (7.6) would give
`F_lambda(Pi_Sp)<c` on an event of positive probability.  This is impossible.
In fact the
argument shows that the essential infimum of the scalar functional is
`1/2`, although the value `1/2` is not attained almost surely.

**Verdict:** scalar nonconstancy is provable, but it requires the crowding and
concentration argument above; it does not follow from random conditional
variance alone.

## 8. Required manuscript repairs

Before using the quenched theorem, make the following changes.

1. Put the finite and limiting point processes on `[0,infinity)`, and state
   explicitly that the limit has no atom at zero.
2. Replace the subsequence sentence in Section 4 by the closed-hard-edge
   `ell^2` matching lemma in Section 3.2 above.
3. State the Borel `P_2`-valued conditional-law lemma and define a fixed
   fallback law on the nonsquare-summable Borel complement.
4. Call (3.1)--(3.2) exact costs of the displayed couplings, not exact
   formulas for `W_2` itself.
5. Prove local finiteness at zero before splitting off the first point.
6. Add `f_lambda in L^1 cap L^2` and the projection identity (6.2) to justify
   every use of the DPP variance formula.
7. If the paper claims the scalar limiting density is nondegenerate, include
   the separate crowding/concentration lemma in Section 7.  The conditional
   variance argument proves only nondegeneracy of the full random law.

With these changes, no unresolved probability or point-process obstruction
remains in the quenched upgrade.
