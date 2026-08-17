# A canonical simultaneous hyperelliptic critical law

Status: focused internal research note, 2026-08-17.  This is a candidate
companion-paper theorem and proof architecture, not text for the frozen
66-page manuscript.  The cited arithmetic inputs below have been checked
against the primary-source statements.  An internal adversarial audit found no
fatal mathematical obstruction, but this is not external peer verification and
the priority search is not complete.  The metric normalization, level-cover
calculation, and marked-series lemma are made explicit below so that they do not
hide fixed-genus constants.

## 1. Executive verdict

There is a viable way to replace the noncanonical iterated limit

\[
  Q\to\infty\ \text{at fixed }g,\qquad g\to\infty,
\]

by one explicit simultaneous limit.  The right family is not the full
\(2g+1\)-parameter hyperelliptic ensemble.  It is the one-parameter pencil

\[
  C_{g,t}: y^2=f_g(x)(x-t),
  \qquad f_g(x)=\prod_{a=1}^{2g}(x-a).
\]

For this pencil, Katz--Sarnak's quantitative character equidistribution has an
explicit genus dependence because the base is a punctured affine line.  At the
same time, Kowalski's large-sieve theorem gives a genus-uniform estimate for the
curves whose Frobenius polynomial does not have maximal Weyl-group Galois
group.  If the ground field is a square, maximal Galois group already implies
the exact linear-independence condition needed by the degree race.

A concrete sufficient choice is

\[
 \boxed{
  \begin{aligned}
  p_g&=\text{the least prime greater than }2g+1,\\
  Q_g&=p_g^{2n_g},\quad
  n_g=\min\left\{n\geq1:p_g^{2n}\geq
  \exp\!\bigl(g^2\log^2(g+2)\bigr)\right\}.
  \end{aligned}}
\tag{1.1}
\]

The square-field condition is deliberate, not cosmetic.  It makes
\(\sqrt{Q_g}\in\mathbb Z\), so the normalized Frobenius polynomial remains a
rational polynomial with the same splitting field.  Kowalski's algebraic
criterion can then be applied without a trace-nonzero side condition.

The resulting theorem is much stronger than an existence diagonal: the family,
the characteristic, the extension degree, and the growth rule are canonical.
It is still not a fixed-field theorem.  The field size in (1.1) is astronomical,
so this is a rigorous bridge theorem rather than the final Katz--Sarnak
microscopic conjecture.

## 2. Exact family and race

Fix \(\lambda>0\).  For \(g\geq2\), take \(p_g,Q_g\) as in (1.1), regard
\(1,\ldots,2g\) as distinct elements of \(\mathbb F_{Q_g}\), and put

\[
 U_g=\mathbb A^1\setminus\{1,\ldots,2g\},\qquad
 D_{g,t}(x)=f_g(x)(x-t),\quad t\in U_g(\mathbb F_{Q_g}).
\]

The polynomial \(D_{g,t}\) is monic and squarefree of degree
\(d_g=2g+1\), and \(C_{g,t}:y^2=D_{g,t}(x)\) has genus \(g\).  Let
\(\chi_{g,t}\) be its quadratic Euler symbol, with \(+1\) on split primes and
\(-1\) on inert primes.  Define

\[
 M_g=m_g+\frac12=\frac{\lambda}{d_g\log Q_g},
 \qquad r_g=Q_g^{M_g}=e^{\lambda/d_g}.
\tag{2.1}
\]

For degree endpoint \(N\), use the normalized inert-minus-split race

\[
 \mathcal E_{g,t,\lambda}(N)
 =2(1-Q_g^{-M_g})Q_g^{-M_gN}
 \left(-\sum_{\substack{P\ \text{ monic irreducible}\\ \deg P\leq N}}
  (\deg P)\chi_{g,t}(P)Q_g^{m_g\deg P}\right).
\tag{2.2}
\]

If the positive Frobenius angles are
\(0\leq\vartheta_1\leq\cdots\leq\vartheta_g\leq\pi\), put

\[
 b_{g,\lambda}(\vartheta)
 =\frac{4(1-e^{-\lambda/d_g})}
 {\sqrt{1+e^{-2\lambda/d_g}
       -2e^{-\lambda/d_g}\cos\vartheta}},
\tag{2.3}
\]

and

\[
 c_{g,\lambda}^{(0)}=\frac{2r_g}{r_g+1},\qquad
 c_{g,\lambda}^{(1)}=\frac{2}{r_g+1}.
\tag{2.4}
\]

For completeness, write
\[
 \Psi_{g,t}(k)=\sum_{\deg F=k}\Lambda(F)\chi_{g,t}(F)
             =-\sum_{j=1}^{2g}\alpha_j^k
\]
and let \(A_{g,t}(N)\) denote the prime sum inside (2.2), without its
minus sign.  Euler-product expansion gives the exact identity
\[
 -A_{g,t}(N)=
 \sum_{k\leq N}\sum_{j=1}^{2g}\alpha_j^k+
 \sum_{\substack{a\geq2,\ a\deg P\leq N}}
 (\deg P)\chi_{g,t}(P)^aQ_g^{m_ga\deg P}.
\]
After the normalization in (2.2), one conjugate Frobenius pair has limiting
amplitude (2.3); the fixed denominator argument is absorbed into its uniform
phase.  The \(a=2\) term uses
\(\sum_{\deg P=\ell}\deg P=Q_g^\ell+O(Q_g^{\ell/2})\) and yields, for even
and odd \(N\), respectively,
\[
 2(1-r_g^{-1})r_g^{-N}\sum_{\ell\leq N/2}r_g^{2\ell}
 \longrightarrow
 \frac{2r_g}{r_g+1},\quad \frac{2}{r_g+1}.
\]
The prime-polynomial-theorem error is summable for \(M_g<1/4\).
For \(a\geq3\), the degree-\(\ell\) majorant is a geometric series with
exponent \(1+3m_g=-\tfrac12+3M_g<0\) when \(M_g<1/6\), so its normalized
contribution tends to zero.  Primes dividing \(D_{g,t}\) also contribute only
a finite term before endpoint normalization.  Thus, under LI,

\[
 \delta_{g,t,\lambda}=F_{g,\lambda}(\Theta_{g,t})
 :=\frac12\sum_{\epsilon=0}^1
 \mathbb P\left(
 c_{g,\lambda}^{(\epsilon)}+
 \sum_{j=1}^g b_{g,\lambda}(\vartheta_j)\cos\Phi_j>0
 \right),
\tag{2.5}
\]

where the \(\Phi_j\) are independent uniform phases.  Higher prime powers are
summable once \(M_g<1/6\), which holds for every sufficiently large \(g\).
The two square-prime centers in (2.4) both tend to \(1\).

## 3. Candidate theorem

**Theorem (canonical simultaneous hyperelliptic critical law).**
Fix \(\lambda>0\), and choose \(p_g,Q_g,f_g,U_g\) by (1.1)--(2.1).
Let \(t_g\) be uniform in \(U_g(\mathbb F_{Q_g})\).  When
\(C_{g,t_g}\) satisfies LI, let \(\delta_{g,t_g,\lambda}\) be the natural
degree density of the event \(\mathcal E_{g,t_g,\lambda}(N)>0\); give the
density any value in \([0,1]\) on the exceptional non-LI set.  Then

\[
 \delta_{g,t_g,\lambda}\ \Longrightarrow\
 F_\lambda(\Pi_{\rm Sp}),
\tag{3.1}
\]

where \(\Pi_{\rm Sp}\) is the symplectic hard-edge determinantal process with

\[
 K_{\rm Sp}(x,y)=
 \frac{\sin\pi(x-y)}{\pi(x-y)}-
 \frac{\sin\pi(x+y)}{\pi(x+y)},
\tag{3.2}
\]

and

\[
 F_\lambda(\mu)=
 \mathbb P\left(
 1+\sum_{y\in\mu}
 \frac{4\lambda}{\sqrt{\lambda^2+(2\pi y)^2}}
 \cos\Phi_y>0\ \middle|\ \mu\right).
\tag{3.3}
\]

Moreover,

\[
 \mathbb E\delta_{g,t_g,\lambda}
 \longrightarrow \mathbb E F_\lambda(\Pi_{\rm Sp}).
\tag{3.4}
\]

The proof separates into three quantitative statements: maximal-Galois LI,
arithmetic-to-Haar equidistribution, and Haar-to-hard-edge convergence.

## 4. Quantitative LI: why square fields close the algebra

Kowalski's Theorem 6.2 for the pencil \(y^2=f(x)(x-t)\), together with his
published erratum, gives an absolute constant \(A\) such that the number of
parameters whose Frobenius polynomial is reducible or has splitting field
smaller than the Weyl group \(W_{2g}\) is at most

\[
 A g^2 Q^{1-\gamma_g}\log Q,
 \qquad
 \gamma_g=\frac1{4g^2+3g+5}.
\tag{4.1}
\]

The factor \(g^2\), absent from the displayed theorem in the original paper,
is required by item 3 of the erratum.  The implied constant is absolute for
this one-parameter hyperelliptic pencil.

Now use that \(Q_g=s_g^2\) with \(s_g=p_g^{n_g}\in\mathbb Z\).  If

\[
 P_{g,t}(T)=\prod_{j=1}^{2g}(1-\alpha_jT)\in\mathbb Z[T],
\]

form the reciprocal characteristic polynomial
\[
 R_{g,t}(X)=X^{2g}P_{g,t}(1/X)=\prod_j(X-\alpha_j)\in\mathbb Z[X].
\]
Then
\[
 s_g^{-2g}R_{g,t}(s_gX)=\prod_j(X-\alpha_j/s_g)\in\mathbb Q[X].
\]
Scaling by the nonzero rational number \(s_g\) leaves the splitting field and
its Galois action unchanged.  Kowalski's Proposition 2.4(2), with its parameter
\(m=1\), says that for \(g\geq2\) and Galois group \(W_{2g}\), the rational
vector space of multiplicative relations among the normalized inverse roots is
exactly the reciprocal-pair space.  Consequently

\[
 \{\vartheta_1,\ldots,\vartheta_g,\pi\}
 \quad\hbox{is linearly independent over }\mathbb Q.
\tag{4.2}
\]

Indeed, clear denominators in a relation
\(\sum_j a_j\vartheta_j+b\pi=0\), with \(a_j,b\in\mathbb Z\), and square its
exponential to obtain \(\prod_j e^{2ia_j\vartheta_j}=1\).  In the relation
vector on the \(2g\) normalized roots, the coefficient of the positive member
of the \(j\)-th reciprocal pair is \(2a_j\), while that of the negative member
is \(0\).  Membership in the reciprocal-pair space forces \(a_j=0\) for every
\(j\), and then \(b=0\).  No assertion about saturation of the integral
relation lattice is needed.

Since \(|U_g(\mathbb F_{Q_g})|=Q_g-2g\), (4.1) gives

\[
 \mathbb P(t_g\hbox{ is non-LI})
 \ll g^2 Q_g^{-\gamma_g}\log Q_g=o(1).
\tag{4.3}
\]

For (1.1), the logarithm of the right side is at most

\[
 O(\log g+\log\log Q_g)
 -\frac{\log Q_g}{4g^2+3g+5}
 =-\frac14\log^2(g+2)+O(\log g),
\]

which tends to \(-\infty\).
Here the final equality is justified without an unstated prime-gap estimate:
Bertrand's postulate gives \(2g+1<p_g<2(2g+1)\), while minimality of \(n_g\)
gives
\[
 g^2\log^2(g+2)\leq\log Q_g
 <g^2\log^2(g+2)+2\log p_g.
\]

## 5. Quantitative equidistribution with an explicit genus constant

Katz and Sarnak prove, in every odd characteristic, that the geometric
monodromy of the pencil \(y^2=f_g(x)(x-t)\) is \({\rm Sp}(2g)\).  Base-change
this pencil to \(\mathbb F_Q\), where \(Q=s^2\), and twist the weight-one
cohomology sheaf by the constant character sending arithmetic Frobenius to
\(s^{-1}\).  The twist is defined over \(\mathbb Q_3\), is pure of weight zero,
has unchanged geometric monodromy, and takes the full arithmetic monodromy
into \({\rm Sp}(2g)\).  Its Frobenius classes are exactly
\(\Theta_{g,t}\).  For

\[
 A(U_g)=\sum_{i<2}h_c^i(U_g,\mathbb Q_3)=2g,
\]

Katz--Sarnak's Theorem 9.2.6(5) then says
that for every nontrivial irreducible representation \(\rho\) of
\({\rm USp}(2g)\),

\[
 \left|\frac1{|U_g(\mathbb F_Q)|}
 \sum_{t\in U_g(\mathbb F_Q)}\chi_\rho(\Theta_{g,t})\right|
 \leq \frac{2C_g\dim\rho}{\sqrt Q},
\tag{5.1}
\]

provided \(Q>4A(U_g)^2\); the displayed sufficient condition \(Q>16g^2\)
is therefore safe.  Here \(C_g\) is the total compactly supported mod-\(3\)
Betti number of a finite etale cover of
\(U_g\otimes\overline{\mathbb F}_Q\) that trivializes the mod-\(3\)
geometric local system.

For this pencil, \(C_g\) is elementary to bound.  The mod-\(3\) cover has
degree

\[
 N_g\leq |{\rm GL}(2g,\mathbb F_3)|<3^{4g^2}.
\tag{5.2}
\]

Katz--Sarnak's Lemma 10.1.12 says that the local system is everywhere tame;
the mod-3 trivializing cover is therefore tame above all \(2g+1\) boundary
points (the deleted finite points and infinity) of the smooth
compactification.  The base \(U_g=\mathbb A^1-\{2g\text{ points}\}\) has
\(\chi_c(U_g)=1-2g\).  If the cover has \(c\leq N_g\) connected components,
then \(H_c^0=0\), \(b_c^2=c\), and multiplicativity of the etale Euler
characteristic gives

\[
 b_c^1=c+N_g(2g-1),\qquad
 C_g=b_c^1+b_c^2\leq(2g+1)N_g.
\]

Here multiplicativity
\(\chi_c(Y_g)=N_g\chi_c(U_g)\) is the tame Euler-characteristic formula;
equivalently it follows componentwise from tame Riemann--Hurwitz.  Since a
finite morphism over the affine curve \(U_g\) is affine, every component of
the cover is nonproper, which justifies \(H_c^0=0\).

Thus the completely explicit bound

\[
 \boxed{C_g\leq(2g+1)3^{4g^2}}
\tag{5.3}
\]

is sufficient in (5.1).  This is the decisive simplification supplied by the
one-parameter pencil.  For the full universal hyperelliptic family, the same
Katz--Sarnak theorem contains a Betti constant, but a comparably clean uniform
genus bound has not been verified here.

## 6. Passing from characters to the nonlinear race functional

The input (5.1) is a character bound, while (2.5) is a nonlinear sign
probability.  A heat-kernel smoothing argument bridges them with only an
\(\exp(O(g^2\log g))\) loss.

### 6.1 A uniform Lipschitz bound for the race functional

Put \(d=2g+1\), \(a=1-e^{-\lambda/d}\), and
\(\rho=e^{-\lambda/d}\).  From (2.3),

\[
 b_{g,\lambda}(\vartheta)
 =\frac{4a}{\sqrt{a^2+4\rho\sin^2(\vartheta/2)}}.
\]

The minimum and derivative satisfy

\[
 b_{\min}=4\tanh\frac{\lambda}{2d}
 \geq \frac{2\lambda}{d+\lambda/2},
 \qquad
 \|b'_{g,\lambda}\|_\infty
 \leq \frac{2(d+\lambda)}{\lambda}.
\tag{6.1}
\]

For \(g\geq3\), use any three random-phase summands.  The elementary Bessel
bound \(|J_0(u)|\leq\min(1,2|u|^{-1/2})\) shows that their convolution has a
bounded density, and hence the full sum has density at most

\[
 B_{g,\lambda}\leq \frac{10}{b_{\min}}
 \leq\frac{5(d+\lambda/2)}{\lambda}.
\tag{6.2}
\]

Indeed, Fourier inversion bounds the density by
\((2\pi)^{-1}\int_{\mathbb R}\prod_{j=1}^3|J_0(b_jt)|\,dt\); splitting at
\(|t|=4/b_{\min}\) gives the displayed constant \(10/b_{\min}\).

Couple the same phases for two coefficient vectors.  Their random sums differ
pointwise by at most the \(\ell^1\) distance between the vectors, so (6.2) gives

\[
 |F_{g,\lambda}(\vartheta)-F_{g,\lambda}(\varphi)|
 \leq 2B_{g,\lambda}\|b(\vartheta)-b(\varphi)\|_1.
\]

Equip \({\rm USp}(2g)\) with the bi-invariant metric induced at the identity by
\(\langle X,Y\rangle=-\tfrac12\operatorname{Tr}(XY)\).  Its restriction to a
maximal torus gives the Euclidean norm
\((\sum_jd\vartheta_j^2)^{1/2}\).  Hoffman--Wielandt matching of the positive
angles and (6.1) therefore give

\[
 {\rm Lip}(F_{g,\lambda})\leq C_\lambda g^{5/2}.
\tag{6.3}
\]

This polynomial loss is negligible compared with (5.3).

### 6.2 Heat smoothing

Let \(G_g={\rm USp}(2g)\), let Haar measure have total mass one, let
\(D_g=\dim G_g=2g^2+g\), and let \(P_s\) be the heat semigroup for the metric
fixed above, normalized so that the character
\(\chi_\rho\) has multiplier \(e^{-s\kappa_\rho}\).  The standard Brownian
coupling (or the radial comparison inequality, since a compact group with a
bi-invariant metric has nonnegative Ricci curvature) gives an absolute
constant \(C_0\) such that, for every \(0<s\leq1\), if \(h\) is a central
\(L\)-Lipschitz function bounded by one, then

\[
 \|P_sh-h\|_\infty\leq C_0L\sqrt{D_gs}.
\tag{6.4}
\]

Writing the central Fourier expansion in irreducible characters, applying
(5.1), and then Cauchy--Schwarz gives

\[
 \left|\mathbb E_{\rm arith}h-\mathbb E_{\rm Haar}h\right|
 \leq 2C_0L\sqrt{D_gs}
 +\frac{2C_g}{\sqrt Q}
 \left(\sum_\rho(\dim\rho)^2e^{-2s\kappa_\rho}\right)^{1/2}.
\tag{6.5}
\]

The last sum is the heat-kernel density \(K_{2s}(e)\) at the identity, relative
to Haar probability measure.  The Weyl dimension formula
for type \(C_g\) gives, uniformly for \(0<s\leq1\),

\[
 \sum_\rho(\dim\rho)^2e^{-2s\kappa_\rho}
 \leq \exp\!\bigl(Cg^2\log(g+2)\bigr)s^{-Cg^2}
\tag{6.6}
\]

for an absolute \(C\).  One direct proof is to group dominant highest weights
by \(R=\lambda_1\), use at most \((R+1)^g\) weights in the shell,
\(\dim V_\lambda\leq[2(R+g+1)]^{g^2}\), and
\(\kappa_\lambda\geq cR^2\) for an absolute \(c>0\) under the displayed
metric, then compare the resulting Gaussian sum with an integral.  (Under a
Killing-form normalization one instead gets \(cR^2/g\); the extra power of
\(g\) is absorbed by the prefactor
\(\exp(Cg^2\log(g+2))\).)  Thus no fixed-genus constant is hidden in (6.6).

Apply (6.5) to \(h=\phi\circ F_{g,\lambda}\), where \(\phi:[0,1]\to\mathbb R\)
is 1-Lipschitz and is normalized by \(\phi(0)=0\).  Then \(|h|\leq1\), and
(6.3) applies.  Taking \(s=g^{-10}\), (6.4)--(6.6) yield

\[
 W_1\bigl((F_{g,\lambda})_*\mu_{g,Q},
           (F_{g,\lambda})_*\mu_{{\rm Haar},g}\bigr)
 \leq C_\lambda g^{-3/2}
 +Q^{-1/2}\exp\!\bigl(C_\lambda g^2\log(g+2)\bigr).
\tag{6.7}
\]

Together with (5.3), the second term is absorbed into the exponential on the
right.  The choice (1.1) makes it tend to zero because

\[
 -\frac12\log Q_g+C_\lambda g^2\log(g+2)
 \leq-\frac12g^2\log^2(g+2)+C_\lambda g^2\log(g+2)
 \longrightarrow-\infty.
\]

## 7. Haar low-edge limit and the quenched functional

For Haar \(U_g\in{\rm USp}(2g)\), scale its positive angles by
\(y=d_g\vartheta/(2\pi)\).  Their determinantal kernel is

\[
 \widetilde K_g(x,y)=\frac4{d_g}\sum_{k=1}^g
 \sin\frac{2\pi kx}{d_g}\sin\frac{2\pi ky}{d_g},
\tag{7.1}
\]

which converges locally uniformly to (3.2).  Also

\[
 0\leq\widetilde K_g(y,y)<2,
 \qquad
 \mathbb E\sum_{y_j>R}y_j^{-2}\leq\frac2R.
\tag{7.2}
\]

On compact \(y\)-sets,

\[
 b_{g,\lambda}(2\pi y/d_g)
 \longrightarrow
 \frac{4\lambda}{\sqrt{\lambda^2+(2\pi y)^2}},
\tag{7.3}
\]

and globally the left side is \(O_\lambda(y^{-1})\).  Hence the coefficient
tails vanish in \(\ell^2\), in expectation and therefore in probability.

The remaining functional step can be isolated as follows.

**Closed-hard-edge marked-sign stability lemma.**  Let \(\Xi_n,\Xi\) be
simple, locally finite point measures on \([0,\infty)\), with
\(\Xi_n\Rightarrow\Xi\) vaguely and \(\Xi(\{0\})=0\) almost surely.  Enumerate
points increasingly (a Borel enumeration on the space of simple locally
finite measures).  Let \(a_n,a\) be continuous coefficient functions on the
closed half-line, with \(a_n\to a\) locally uniformly, and suppose

\[
 \lim_{R\to\infty}\sup_n
 \mathbb P\!\left(\sum_{x\in\Xi_n,\ x>R}a_n(x)^2>\eta\right)=0
 \quad(\eta>0).
\]

Suppose also that \(\sum_{x\in\Xi}a(x)^2<\infty\) almost surely, and let
deterministic centers \(c_n\to c\).  Mark the enumerated points by i.i.d.
uniform phases.  Then the matched coefficient vectors converge in \(\ell^2\)
in probability.  If, for almost every limiting point configuration,
\(c+\sum_{x\in\Xi}a(x)\cos\Phi_x\) has no atom at zero, the conditional sign
probabilities converge in law.

**Proof.**  The ordered-point and coefficient maps are Borel.  On a Skorokhod
realization, choose a deterministic \(R\) with
\(\Xi(\{0,R\})=0\) almost surely.  Vague convergence on the **closed**
half-line, simplicity, and local uniform coefficient convergence imply that
the points in \([0,R]\) eventually match and their coefficient differences
tend to zero.  After padding the two tails by zeros, their squared difference
is at most

\[
 2\sum_{x\in\Xi_n,\,x>R}a_n(x)^2
 +2\sum_{x\in\Xi,\,x>R}a(x)^2.
\]

First take \(R\) large, using the uniform tail hypothesis and almost-sure
square summability, and then let \(n\to\infty\).  This proves full
\(\ell^2\) convergence in probability and, after a further subsequence,
almost surely.  Coupling the same phases gives conditional \(L^2\) convergence
because

\[
 \mathbb E_\Phi\left|\sum_j(a_{n,j}-a_j)\cos\Phi_j\right|^2
 =\frac12\sum_j(a_{n,j}-a_j)^2.
\]

Thus the conditional half-line probabilities converge whenever the limiting
conditional law has no atom at the threshold.  Finite partial-sum
probabilities are Borel functions of the point configuration, and their
pointwise limit at continuity configurations is the infinite-series
probability; hence the conditional probability itself is measurable.  Since
every subsequence has a further subsequence with the asserted limit, the
original sequence converges in law.  \(\square\)

The finite kernels converge locally uniformly on \([0,\infty)^2\), and
\(\widetilde K_g(y,y)<2\) also gives
\(\sup_g\mathbb E\Xi_g([0,\epsilon])\leq2\epsilon\); thus no point can escape
undetected through the hard edge.  The limiting process has no atom at zero
because \(K_{\rm Sp}(0,0)=0\).  It is almost surely infinite.  Indeed, for
\(N_L=\Pi_{\rm Sp}([0,L])\),
\[
 \mathbb E N_L=\int_0^LK_{\rm Sp}(x,x)\,dx=L+O(1),
 \qquad
 \operatorname{Var}N_L
 =\operatorname{Tr}(K_L-K_L^2)\leq\mathbb E N_L.
\]
For each fixed \(K\), Chebyshev therefore gives
\(\mathbb P(N_L\leq K)\to0\), and monotonicity in \(L\) proves infinitude.
Equation (7.2) makes the squared coefficient sum finite.  Local finiteness on
the closed half-line, absence of a point at zero, and infinitude give a first
positive point.  Conditional on the point configuration, split off its
nonzero arcsine summand; it is
independent of the remainder, so convolution makes the limiting marked sum
absolutely continuous and hence atomless.  The lemma,
(7.1)--(7.3), and \(c_{g,\lambda}^{(\epsilon)}\to1\) prove

\[
 F_{g,\lambda}(U_g)\Longrightarrow F_\lambda(\Pi_{\rm Sp})
 \quad(U_g\text{ Haar}).
\tag{7.4}
\]

## 8. Assembly

Equation (6.7) transfers the arithmetic model functional to the Haar functional.
Equation (4.3) permits replacing the model functional by the actual degree-race
density, because both take values in \([0,1]\).  Equation (7.4) supplies the
Haar limit.  This proves (3.1).  Boundedness in \([0,1]\) then gives (3.4).

The weakest quantitative inputs actually used are:

1. character equidistribution with
   \(C_g\leq\exp(O(g^2))\);
2. a nonlinear smoothing cost at most \(\exp(O_\lambda(g^2\log g))\);
3. an LI-exception estimate
   \(\ll g^2Q^{-1/(4g^2+3g+5)}\log Q\).

Thus the broad sufficient condition is

\[
 \frac{\log Q_g}{g^2\log(g+2)}\longrightarrow\infty,
 \qquad Q_g\text{ an odd square with characteristic }>2g+1.
\tag{8.1}
\]

The explicit rule (1.1) is a convenient canonical instance, not an optimized
threshold.

## 9. What is proved, what is not, and why the trace-moment route is weaker

### Supported by the argument above

- A canonical simultaneous large-field/large-genus theorem for a natural
  one-parameter hyperelliptic pencil.
- The full nonlinear race-density functional, not only one-level density or
  finitely many moments.
- Density-one LI in the same simultaneous regime.
- An explicit sufficient field-growth rule.

### Not established here

- Fixed \(Q\) with \(g\to\infty\).  That remains the genuinely difficult
  microscopic Katz--Sarnak direction.
- A comparable explicit simultaneous theorem for the full universal ensemble
  \(\mathcal H_{2g+1}(Q)\).  It should follow from a sufficiently explicit
  genus-uniform bound for the relevant level-cover Betti numbers, but that bound
  has not been verified.
- Any claim that (3.1) is new in the literature.  The ingredients are classical;
  the particular critical weighted-race functional and their assembly appear
  new, but a serious priority search and expert review are mandatory.
- A practical field-size threshold.  The regime (1.1) is intentionally
  conservative and far outside computation.

Entin--Pirani's trace-moment formula reaches total Fourier degree
\(\sum j a_j\leq4g+1\).  This is powerful for fixed-order local statistics but is
not, by itself, enough for (3.1): approximating a microscopic sign functional to
arbitrary accuracy and controlling all moments of its random value requires
unbounded Fourier complexity.  The Katz--Sarnak character estimate (5.1), which
is valid for every irreducible representation, is the correct weak sufficient
theorem.

A targeted search located close antecedents that must be discussed in any
submission: Cha's function-field prime-race framework; Aoki--Koyama's weighted
splitting-prime bias over global fields; Entin--Roditty-Gershon--Rudnick's
iterated hyperelliptic low-zero limits; and Katz--Sarnak's quantitative
equidistribution itself.  None of those sources, in the versions checked,
states the quenched nonlinear sign-functional limit (3.1) with an explicit
simultaneous \(Q_g,g\) rule.  That negative search result is evidence, not a
priority proof.

## 10. Publication assessment and audit gates

If the new steps survive independent audit and the priority search is clean,
this is a plausible focused companion paper: one arithmetic family, one theorem,
one explicit simultaneous regime, and one limiting non-Gaussian functional.  It
would convert the current paper's conditional critical transfer into an actual
canonical arithmetic theorem.

It is not yet a 9.5/10 breakthrough.  The large-field hypothesis imports Haar
symplectic statistics, and the required \(Q_g\) is extremely large.  A fixed-field
microscopic theorem would be much deeper.  The realistic value of this result is
that it is narrow, checkable, and apparently provable now.

Before promotion to a submission draft:

1. independently audit the normalization and prime-power decomposition in
   (2.2)--(2.5);
2. check the mod-3 level-cover argument and every hypothesis of Katz--Sarnak
   Theorem 9.2.6 in the varying-characteristic setup;
3. rederive the corrected Kowalski bound from the theorem plus erratum and check
   that the absolute constant remains uniform for the chosen split \(f_g\);
4. formally write and independently audit the heat-kernel estimate (6.6),
   including metric/Casimir normalizations;
5. turn the marked-sign stability lemma into a standalone lemma with full
   measurable-enumeration details;
6. conduct an expert-level priority search specifically for simultaneous
   hyperelliptic low-edge functionals and weighted splitting races.

## 11. Primary sources

1. N. M. Katz and P. Sarnak, *Random Matrices, Frobenius Eigenvalues, and
   Monodromy*, AMS Colloquium Publications 45 (1999), especially Theorem
   9.2.6, Theorem 9.6.10, Lemma 10.1.12, Theorem 10.1.16, and Variant
   10.1.18.  Author-hosted PDF:
   <https://web.math.princeton.edu/~nmk/RMFEM.pdf>.
2. E. Kowalski, "The large sieve, monodromy and zeta functions of curves,"
   *J. Reine Angew. Math.* 601 (2006), 29--69, especially Theorem 6.2.
   Author-hosted PDF:
   <https://people.math.ethz.ch/~kowalski/large-sieve-monodromy.pdf>.
3. E. Kowalski, "Errata for `The large sieve, monodromy and zeta functions of
   curves'," especially item 3:
   <https://people.math.ethz.ch/~kowalski/erratum-large-sieve-monodromy.pdf>.
4. E. Kowalski, "The large sieve, monodromy, and zeta functions of algebraic
   curves, II: independence of the zeros," *IMRN* (2008), especially
   Proposition 2.4:
   <https://arxiv.org/abs/0807.2118>.
5. A. Entin and N. Pirani, "Moments of traces of random symplectic matrices and
   hyperelliptic L-functions," arXiv:2409.04844, especially Theorems 1 and 3:
   <https://arxiv.org/abs/2409.04844>.
6. A. Entin, E. Roditty-Gershon, and Z. Rudnick, "Low-lying zeros of quadratic
   Dirichlet \(L\)-functions, hyper-elliptic curves and random matrix theory,"
   arXiv:1208.5962:
   <https://arxiv.org/abs/1208.5962>.
7. M. Aoki and S. Koyama, "Chebyshev's bias against splitting and principal
   primes in global fields," arXiv:2203.12266:
   <https://arxiv.org/abs/2203.12266>.
8. B. Cha, "Chebyshev's bias in function fields," *Compositio Mathematica*
   144 (2008), 1351--1374:
   <https://doi.org/10.1112/S0010437X08003631>.
