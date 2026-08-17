# A hyperelliptic function-field realization of the critical low-zero law

Status: proof draft for internal audit, not manuscript text.  The theorem below is
complete in the iterated limit \(Q\to\infty\) at fixed genus, followed by
\(g\to\infty\).  The fixed-field limit \(g\to\infty\), and an unrestricted
simultaneous limit, are not claimed.

## 1. Candidate family and exact normalization

Fix an odd prime power \(q_0\).  For \(n\geq 1\), put \(Q=q_0^n\).  For
\(g\geq 1\), put

\[
 d=2g+1,
 \qquad
 \mathcal H_d(Q)=\{D\in\mathbb F_Q[T]:D\text{ monic, squarefree},\ \deg D=d\}.
\]

For \(D\in\mathcal H_d(Q)\), let \(\chi_D\) be the primitive quadratic
character associated with the hyperelliptic curve \(C_D:y^2=D(T)\).  Its
\(L\)-polynomial has degree \(2g\):

\[
 L(u,\chi_D)=\prod_{j=1}^{2g}(1-\alpha_{D,j}u),
 \qquad
 \alpha_{D,j}=Q^{1/2}e^{i\vartheta_{D,j}}.
\]

The angles can be ordered as

\[
 0\leq\vartheta_{D,1}\leq\cdots\leq\vartheta_{D,g}\leq\pi,
 \qquad
 \vartheta_{D,g+j}=-\vartheta_{D,j}.
\]

The norm of the conductor is

\[
 \mathcal C_D=|D|=Q^d,
 \qquad \log\mathcal C_D=d\log Q.
\]

Writing a zero as \(s=\tfrac12+i\gamma\), one has

\[
 \gamma=\frac{\vartheta_{D,j}+2\pi k}{\log Q},\qquad k\in\mathbb Z.
\]

Thus the number-field microscopic coordinate attached to the fundamental
positive angle is exactly

\[
 y_{D,j}=\frac{\gamma\log\mathcal C_D}{2\pi}
          =\frac{d\vartheta_{D,j}}{2\pi}.
\]

The periodic copies in \(s\) must **not** be inserted as independent modes in a
degree race.  The race samples integer degrees \(N\), so angles differing by
\(2\pi\) give the same sequence \(e^{iN\vartheta}\).  The correct function-field
analogue is a finite Frobenius-angle sum.  Treating every vertical copy as a new
zero would double-count aliased modes.

Fix \(\lambda>0\), and choose the critical weight

\[
 M=M_{g,Q}:=m+\frac12=\frac{\lambda}{\log\mathcal C_D}
 =\frac{\lambda}{d\log Q}.
\]

Then

\[
 r:=Q^M=e^{\lambda/d}.
\]

This identity is the exact function-field version of \(M\log q\to\lambda\).
There is no asymptotic ambiguity about whether the scale is \(2g\) or \(2g+1\):
the conductor gives \(d=2g+1\), while replacing \(d\) by the \(L\)-degree \(2g\)
changes the microscopic coordinate by \(1+O(g^{-1})\) and hence has the same
limit.

## 2. The natural weighted splitting race

Let \(\Lambda(f)\) be the polynomial von Mangoldt function.  Consider the
log-weighted inert-versus-split prime race

\[
 \mathcal E_{D,\lambda}(N)
 :=2(1-Q^{-M})Q^{-MN}
 \left(-\sum_{\substack{P\ {m monic\ irreducible}\\ \deg P\leq N}}
       (\deg P)\chi_D(P)Q^{m\deg P}\right).
\]

The prefactor is positive, so it does not change the winner.  The minus sign
makes inert primes, for which \(\chi_D(P)=-1\), the positive side of the race.

The exact explicit formula is

\[
 \sum_{\deg f=k}\Lambda(f)\chi_D(f)
 =-\sum_{j=1}^{2g}\alpha_{D,j}^{k}.
\]

After multiplication by (Q^{mk}) and summation over (k\leq N), the spectral
part is a finite geometric series.  Since

\[
 r^{-N}\sum_{k=1}^N(re^{i\vartheta})^k
 =\frac{e^{iN\vartheta}}{1-r^{-1}e^{-i\vartheta}}+O(r^{-N}),
\]

the conjugate pair (\pm\vartheta), after applying the normalization in
\(\mathcal E_{D,\lambda}\), has amplitude

\[
 B_{g,\lambda}(\vartheta)
 =\frac{4(1-r^{-1})}{|1-r^{-1}e^{-i\vartheta}|}.
\]

In microscopic coordinates this is

\[
 b_{g,\lambda}(y)
 =\frac{4(1-e^{-\lambda/d})}
 {\sqrt{1+e^{-2\lambda/d}-2e^{-\lambda/d}\cos(2\pi y/d)}}.
\tag{2.1}
\]

For every compact set of (y\)'s,

\[
 b_{g,\lambda}(y)\longrightarrow
 b_\lambda(y):=\frac{4\lambda}{\sqrt{\lambda^2+(2\pi y)^2}}
\tag{2.2}
\]

uniformly as (g\to\infty).  This is exactly the amplitude in the manuscript's
critical transfer theorem.

### Prime squares and parity

The von Mangoldt sum contains prime powers, whereas the race contains primes.
The only surviving correction comes from squares.  Indeed,

\[
 \sum_{\deg P=\ell}\deg P=Q^\ell+O(Q^{\ell/2}),
\]

and (1+2m=2M), so the square contribution is

\[
 \sum_{2\ell\leq N}\sum_{\deg P=\ell,\,P\nmid D}
 (\deg P)Q^{2m\ell}
 =\sum_{\ell\leq N/2}r^{2\ell}+O_{D,Q,M}(1)
\]

when (M<1/4).  Consequently its normalized limits are

\[
 c_{g,\lambda}^{(0)}=\frac{2r}{r+1}\quad(N\ {m even}),
 \qquad
 c_{g,\lambda}^{(1)}=\frac{2}{r+1}\quad(N\ {m odd}).
\tag{2.3}
\]

Both tend to (1) as (g\to\infty).  Prime powers (P^k), (k\geq3), are
uniformly summable before the endpoint normalization once
(1+3m<0), equivalently (M<1/6):

\[
 \sum_P(\deg P)\sum_{k\geq3}Q^{mk\deg P}<\infty.
\]

Their contribution is therefore (O(r^{-N})).  Primes dividing (D) make only
a finite correction and also disappear after multiplication by (r^{-N}).

Hence the two parity subsequences have limiting zero-model variables

\[
 X_{D,g,\lambda}^{(\epsilon)}
 =c_{g,\lambda}^{(\epsilon)}
  +\sum_{j=1}^g b_{g,\lambda}(y_{D,j})\cos\Theta_j,
 \qquad \epsilon\in\{0,1\},
\tag{2.4}
\]

where the \(\Theta_j\)'s are independent uniform phases when the Frobenius
angles satisfy LI.

## 3. The arithmetic-to-random-phase bridge

For this family, LI means that

\[
 \{\vartheta_{D,1},\ldots,\vartheta_{D,g},\pi\}
\]

is linearly independent over \(\mathbb Q\).  Under LI, Kronecker--Weyl on each
parity subsequence makes the phases in (2.4) independent and uniform.  Therefore
the natural density

\[
 \delta_{D,g,\lambda}
 :=\lim_{X\to\infty}\frac1X
 \#\{1\leq N\leq X:\mathcal E_{D,\lambda}(N)>0\}
\]

exists and equals

\[
 \frac12\sum_{\epsilon=0}^1
 \mathbb P\!\left(
 c_{g,\lambda}^{(\epsilon)}+
 \sum_{j=1}^g b_{g,\lambda}(y_{D,j})\cos\Theta_j>0
 \right).
\tag{3.1}
\]

This use of LI is not conjectural in the geometric limit.  Kowalski's
independence theorem, in the universal hyperelliptic form recorded and proved by
Cha, gives, for each fixed (g) and (q_0),

\[
 \lim_{n\to\infty}
 \frac{\#\{D\in\mathcal H_d(q_0^n):C_D\text{ satisfies LI}\}}
      {\#\mathcal H_d(q_0^n)}=1.
\tag{3.2}
\]

Thus the exceptional non-LI curves have no effect on the inner family limit.

## 4. The zero point process actually available

Let (U_g\) be Haar distributed in \({\rm USp}(2g)\), and write its positive
eigenangles as (0<\vartheta_1<\cdots<\vartheta_g<\pi\).  Put

\[
 \Pi_g=\sum_{j=1}^g\delta_{d\vartheta_j/(2\pi)}.
\]

The Weyl integration formula makes the positive eigenangles a determinantal
process on \((0,\pi)\) with kernel, relative to (d\vartheta),

\[
 K_g^{\vartheta}(\vartheta,\varphi)
 =\frac2\pi\sum_{k=1}^g\sin(k\vartheta)\sin(k\varphi).
\]

After the scaling (y=d\vartheta/(2\pi)), the kernel relative to (dy) is

\[
 \widetilde K_g(x,y)
 =\frac4d\sum_{k=1}^g
 \sin\!\left(\frac{2\pi kx}{d}\right)
 \sin\!\left(\frac{2\pi ky}{d}\right).
\tag{4.1}
\]

The sum in (4.1) is a Riemann sum.  Locally uniformly on
\([0,\infty)^2\),

\[
 \widetilde K_g(x,y)\longrightarrow
 K_{\rm Sp}(x,y):=S(x-y)-S(x+y),
 \qquad
 S(t)=\frac{\sin\pi t}{\pi t}.
\tag{4.2}
\]

Convergence of the determinantal Laplace functionals on compact intervals then
gives

\[
 \Pi_g\Rightarrow\Pi_{\rm Sp}
\tag{4.3}
\]

in the vague topology, where \(\Pi_{\rm Sp}\) is the determinantal point
process on \([0,\infty)\) with kernel (4.2).

For the arithmetic ensemble, Katz--Sarnak equidistribution says that for each
fixed (g), as (n\to\infty), the Frobenius conjugacy classes attached to
(D\in\mathcal H_d(q_0^n)) become Haar distributed in \({\rm USp}(2g)\).
Consequently the arithmetic point measure

\[
 \mu_D=\sum_{j=1}^g\delta_{d\vartheta_{D,j}/(2\pi)}
\]

converges in distribution to \(\Pi_g\) in the inner limit.  Combining this
with (4.3) proves the full point-process statement in the order

\[
 \lim_{g\to\infty}\lim_{n\to\infty}.
\]

Katz and Sarnak explicitly identify this iterated low-zero limit.  They also
explicitly state the fixed-(Q), (g\to\infty) analogue as a conjecture and say
that their equidistribution method gives no proof of it.

## 5. Reciprocal-square tightness from first principles

The diagonal of (4.1) is the scaled one-point intensity.  The elementary bound

\[
 0\leq\widetilde K_g(y,y)
 =\frac4d\sum_{k=1}^g\sin^2\!\left(\frac{2\pi ky}{d}\right)
 \leq\frac{4g}{2g+1}<2
\tag{5.1}
\]

implies, uniformly in (g),

\[
 \mathbb E\int_{(R,\infty)}\frac{d\Pi_g(y)}{y^2}
 \leq\int_R^{\infty}\frac{2\,dy}{y^2}
 \leq\frac2R.
\tag{5.2}
\]

The same bound passes to the iterated arithmetic limit by fixed-genus
equidistribution.  In particular, the reciprocal-square tails vanish in
expectation and hence in probability.  This is stronger than merely postulating
the tail condition.

The exact amplitudes also obey the needed tail envelope.  From

\[
 |1-e^{-\lambda/d}e^{-2\pi i y/d}|^2
 =(1-e^{-\lambda/d})^2
 +4e^{-\lambda/d}\sin^2(\pi y/d)
\]

and \(\sin(\pi y/d)\geq2y/d\) for (0\leq y\leq d/2\), one obtains

\[
 b_{g,\lambda}(y)\leq\frac{\lambda e^{\lambda/2}}{y}
 \qquad(0<y\leq d/2).
\tag{5.3}
\]

Equations (5.2)--(5.3) give uniform (L^2) control of all discarded modes.

## 6. Exact theorem

**Theorem (iterated hyperelliptic critical family law).**
Fix an odd prime power (q_0) and \(\lambda>0\).  For (Q=q_0^n),
(D\in\mathcal H_{2g+1}(Q)), and

\[
 m=-\frac12+\frac{\lambda}{(2g+1)\log Q},
\]

let \(\delta_{D,g,\lambda}\) be the weighted inert-versus-split prime-race
density above whenever (D) satisfies LI.  In the inner limit we may, and do,
discard the finitely many (n) for which (M\geq1/6).  Here
\(M=\lambda/(d\log Q)=\lambda/(dn\log q_0)\), so for fixed \(g\) the
condition \(M<1/6\) holds for all sufficiently large \(n\).  The
\(n\)-independent quantity is \(M\log Q=\lambda/d\), not \(M\) itself.
Give the density any value in \([0,1]\) on the exceptional non-LI set.  If
(D) is uniform in \(\mathcal H_{2g+1}(q_0^n)\), then

\[
 \lim_{g\to\infty}\lim_{n\to\infty}
 \delta_{D,g,\lambda}
 \ \stackrel{d}{=}\ 
 F_\lambda(\Pi_{\rm Sp}),
\tag{6.1}
\]

where

\[
 F_\lambda(\mu)=
 \mathbb P\!\left(
 1+\sum_{y\in\mu}
 \frac{4\lambda}{\sqrt{\lambda^2+(2\pi y)^2}}
 \cos\Theta_y>0\ \middle|\ \mu
 \right)
\tag{6.2}
\]

and the marks \(\Theta_y\) are independent and uniform on \([0,2\pi)\).
Moreover,

\[
 \lim_{g\to\infty}\lim_{n\to\infty}
 \mathbb E_D\delta_{D,g,\lambda}
 =\mathbb E F_\lambda(\Pi_{\rm Sp}).
\tag{6.3}
\]

Conditionally on \(\Pi_{\rm Sp}\), the random series in (6.2) converges almost
surely and in (L^2), its law is absolutely continuous, and it is non-Gaussian
almost surely.

### Proof

For fixed (g), (3.2) removes the non-LI exception, the explicit formula and
prime-power calculation give (3.1), and Katz--Sarnak equidistribution sends the
Frobenius angles to the Haar \({\rm USp}(2g)\) angles.  The finite-genus density
functional is continuous in the eigenangles: couple the uniform phases, use
continuity of the amplitudes, and note that a nontrivial finite sum containing
one arcsine summand has no atom at the threshold zero.  Hence the continuous
mapping theorem gives the inner limit.

For (g\to\infty), truncate at (y\leq R).  Equations (2.2) and (4.3) give
convergence of every truncated marked sum and of its conditional sign
probability.  By (5.2)--(5.3), the mean conditional variance of the discarded
tail is (O_\lambda(R^{-1})), uniformly in (g).  Chebyshev's inequality and
the absence of an atom at zero for the truncated limit allow (R\to\infty).
The parity centers in (2.3) both tend to (1), so the two subsequential laws
coalesce.  This proves (6.1).  Since every density is in \([0,1]\), weak
convergence also gives (6.3).

The limiting point process has finite reciprocal-square sum almost surely by
(5.2) and monotone convergence.  It is infinite almost surely.  Indeed, if
\(N_L=\Pi_{\rm Sp}([0,L])\), then
\(\mathbb E N_L=\operatorname{Tr}K_L=L+O(1)\), while the determinantal
variance identity gives
\(\operatorname{Var}N_L=\operatorname{Tr}(K_L-K_L^2)\leq\operatorname{Tr}K_L\).
Consequently, for every fixed integer \(K\), Chebyshev's inequality gives
\(\mathbb P(N_L\leq K)\to0\); hence the total number of points is almost
surely infinite.  Thus the marked series converges almost surely and in
\(L^2\), and it contains an arcsine summand, proving absolute continuity.
Finally, conditionally on a
configuration \(\mu\), the fourth cumulant of the centered series is

\[
 -\frac38\sum_{y\in\mu}b_\lambda(y)^4<0.
\]

The (L^4) passage is justified by \(\sum b_\lambda(y)^2<\infty\), exactly as
in the manuscript's transfer theorem.  Therefore every quenched limiting law
is non-Gaussian.  This proves the theorem.  \(\square\)

## 7. What “non-Gaussian” does and does not mean

The theorem proves the strongest statement naturally parallel to the
manuscript: for almost every limiting zero configuration, the conditional
(quenched) race law has a strictly negative fourth cumulant.  The annealed law,
obtained by also averaging over \(\Pi_{\rm Sp}\), is the mixture with
characteristic function

\[
 e^{it}\,\mathbb E_{\Pi_{\rm Sp}}
 \prod_{y\in\Pi_{\rm Sp}}J_0(t b_\lambda(y)),
\]

equivalently a Fredholm determinant.  A mixture of non-Gaussian laws is not
automatically non-Gaussian, because the randomness of the conditional variance
contributes to its fourth cumulant.  No annealed non-Gaussian claim is needed
for (6.1), and it should not be made without a separate Fredholm-determinant
calculation.

## 8. The precise obstruction beyond the theorem

The theorem is unconditional only in the order

\[
 Q=q_0^n\to\infty\quad\text{first, then}\quad g\to\infty.
\]

It also yields a one-parameter diagonal sequence (Q_g\to\infty) by a standard
diagonal argument, but that sequence is noncanonical unless the dependence on
(g) in geometric equidistribution is made explicit.

For fixed (Q) and (g\to\infty), the missing input is:

> **Missing microscopic theorem.**  Prove that the random point measures
> \(\sum_{j=1}^g\delta_{(2g+1)\vartheta_{D,j}/(2\pi)}\), for uniform
> \(D\in\mathcal H_{2g+1}(Q)\), converge vaguely to the determinantal
> symplectic hard-edge process (K_{\rm Sp}\), together with uniform
> integrability of \(\sum_{y>R}y^{-2}\).

Known fixed-field results on one-level density, restricted Fourier support, and
mesoscopic counting fluctuations do not imply this theorem.  The critical
functional depends nonlinearly on the entire (O(1))-scale low-zero
configuration, so finitely many moments or a mesoscopic central limit theorem
cannot replace point-process convergence.  Katz--Sarnak's 1999 paper explicitly
labels the fixed-field low-zero limit as conjectural.

## 9. Primary references

1. N. M. Katz and P. Sarnak, *Random Matrices, Frobenius Eigenvalues, and
   Monodromy*, AMS Colloquium Publications 45 (1999), especially Theorems
   10.1.18.3 and 10.8.2.  DOI:
   [10.1090/coll/045](https://doi.org/10.1090/coll/045).
2. N. M. Katz and P. Sarnak, “Zeroes of zeta functions and symmetry,” *Bull.
   Amer. Math. Soc.* 36 (1999), 1--26.  Equation (41) gives the iterated
   hyperelliptic low-zero limit; equation (42) is the fixed-field conjecture.
   DOI: [10.1090/S0273-0979-99-00766-1](https://doi.org/10.1090/S0273-0979-99-00766-1).
3. E. Kowalski, “The large sieve, monodromy and zeta functions of algebraic
   curves, II: independence of the zeros,” *Int. Math. Res. Not.* (2008).
   DOI: [10.1093/imrn/rnn091](https://doi.org/10.1093/imrn/rnn091).
4. B. Cha, “The summatory function of the Möbius function in function fields,”
   *Acta Arith.* 179 (2017), 375--395.  Theorem 3.1 records the density-one LI
   theorem for the universal family \(\mathcal H_{2g+1}(\mathbb F_{q^n})\).
   DOI: [10.4064/aa8590-1-2017](https://doi.org/10.4064/aa8590-1-2017).
5. B. Cha, “Chebyshev's bias in function fields,” *Compos. Math.* 144 (2008),
   1351--1374, for the function-field explicit-formula/prime-race framework and
   GSH. DOI:
   [10.1112/S0010437X08003631](https://doi.org/10.1112/S0010437X08003631).
6. D. Faifman and Z. Rudnick, “Statistics of the zeros of zeta functions in
   families of hyperelliptic curves over a finite field,” *Compos. Math.* 146
   (2010), 81--101.  This proves fixed-field mesoscopic statistics, not the
   microscopic point-process theorem required here.  DOI:
   [10.1112/S0010437X09004308](https://doi.org/10.1112/S0010437X09004308).

## 10. Feasibility verdict

- **Iterated family theorem:** feasible and, modulo expert line-by-line checking,
  proved above.  The key inputs are established primary theorems, and the new
  calculations (discrete amplitude, square parity, and reciprocal-square tail)
  are elementary and explicit.
- **Canonical simultaneous theorem:** not presently justified.  An existence
  diagonal is easy; a useful explicit growth condition (Q\geq Q_0(g)\) requires
  quantitative equidistribution uniform in genus.
- **Fixed-field theorem:** genuinely open at the required microscopic strength.
  This is the high-prestige target, but it is not an “ASAP” addition.
- **Likely impact on the paper:** the iterated theorem would turn the current
  abstract transfer principle into an actual natural arithmetic family law.  It
  is a substantial upgrade, but because the order of limits imports the full
  symplectic process through Katz--Sarnak equidistribution, it is not by itself a
  9.5/10 breakthrough.  The fixed-field or quantitatively simultaneous theorem
  would be much closer to that level.
