# Gaussian white-noise universality for shrinking Mellin kernels

Status: proof-first flagship feasibility note, 17 August 2026. This file does
not modify or supplement the frozen manuscript. Nothing below should be
advertised as a proved theorem until the two promotion gates in Section 10
have been written in full and independently audited.

## 1. Bottom line

The strongest coherent single-result paper suggested by the moving-power
calculation is not a theorem about one more value of the exponent. It is a
finite-dimensional universality theorem for actual, shrinking, weighted prime
races.

Fix a real primitive nonprincipal Dirichlet character `chi`. For any fixed
finite family of admissible shapes `kappa_1,...,kappa_r`, shrink each shape to
logarithmic width `1/M` about `x=e^u` and form the corresponding signed prime
sum. Under GRH, NCZ, LI, and Leung's all-order QLI hypothesis for the zeros of
`L(s,chi)`, the centered vector should converge, as `M->infinity` and
`log M=o(log U)`, to a Gaussian vector whose covariance is exactly the
`L^2(R)` Gram matrix of the shapes.

Equivalently, the local prime-race noise tends to real Gaussian white noise in
the Mellin coordinate. The one-sided exponential shape

\[
 \kappa_{\rm exp}(y)=e^{-y}{\bf 1}_{[0,\infty)}(y)
\]

recovers the growing power-weight race exactly. Compact interval indicators
give sharp local races, and arbitrary finite linear combinations give joint
laws and correlations without a new proof.

This is a materially better flagship than the power-kernel theorem alone:

* it gives one organizing result rather than another isolated CLT;
* it solves the moving multivariate extension that Leung explicitly leaves
  open after Theorem 10.1;
* it identifies a universal covariance object, the `L^2` Gram matrix;
* it contains the actual growing power race as a clean corollary.

It remains a conditional specialist theorem, not a plausible 9.5/10
breakthrough. The moment mechanism is still Leung's QLI mechanism. The real
new work is the Dirichlet-race interpretation, the kernel class, the joint
white-noise formulation, and a corrected diagonal-aware high-zero theorem.

## 2. A precise admissible kernel class

Let `K` be the following class of real functions. A function
`kappa:R->R` belongs to `K` if:

1. `kappa` is right-continuous and of bounded variation;
2. there is an `A<infinity` such that `kappa(y)=0` for `y<-A`;
3. there are `a,C>0` such that, for `y>=0`,

\[
 |\kappa(y)|+|D\kappa|([y,\infty))\le C e^{-ay};          \tag{2.1}
\]

4. `kappa` is not zero in `L^2(R)`.

Here `D kappa` is the finite signed distributional derivative and `|D kappa|`
its total variation. This class contains finite-step kernels, compactly
supported BV kernels, splines, compact smooth kernels, and one-sided
exponentials. The lower-support condition makes every statistic below an
actual finite prime sum. The exponential tail controls the remote lower
endpoint in the explicit formula.

With the Fourier convention

\[
 \widehat\kappa(t)=\int_{\mathbb R}\kappa(y)e^{-ity}\,dy, \tag{2.2}
\]

bounded variation gives the two estimates used everywhere in the proof,

\[
 |\widehat\kappa(t)|\le \|\kappa\|_1,
 \qquad
 |\widehat\kappa(t)|\le {|D\kappa|(\mathbb R)\over |t|}
 \quad(t\ne0).                                           \tag{2.3}
\]

Thus `hat kappa` is continuous, square-integrable, and

\[
 \int_{\mathbb R}|\widehat\kappa(t)|^2dt
 =2\pi\int_{\mathbb R}|\kappa(y)|^2dy.                  \tag{2.4}
\]

The full exponentially weighted BV class is close to the broadest class that
the present proof can handle without changing its tail argument. It is safer
than merely assuming `kappa in L^1 cap L^2`: that weaker condition does not
give the uniform `1/|t|` decay needed to remove high zeros. A publication can
initially state the theorem for finite-jump, piecewise `C^1` members of this
class and then obtain the BV version by approximation. That ordering avoids
burying the main idea in Stieltjes technicalities.

Values at jumps are irrelevant to the distribution: the times for which a
transformed jump lands exactly on a prime or prime power form a countable,
hence measure-zero, set.

## 3. The actual statistic and its deterministic center

Let `M=M(U)>0`, let `u` be chosen uniformly from `[U,2U]`, and define

\[
 \mathcal P_{\kappa,M}(u)
 :=-2M\sum_p \chi(p){\log p\over\sqrt p}\,
       \kappa\!\left(M(u-\log p)\right).                 \tag{3.1}
\]

This is a genuine prime-race statistic. It is finite because `kappa` is
supported in `[-A,infinity)`, so only
`p<=exp(u+A/M)` occurs. Its deterministic prime-square center is

\[
 \mu_\kappa:=\int_{\mathbb R}\kappa(y)\,dy.              \tag{3.2}
\]

The factor `2M` is a convenient convention: it makes the square center equal
to `mu_kappa`. Multiplying (3.1) by any positive deterministic scalar does
not alter the standardized CLT or its sign.

To see (3.2) from first principles, insert prime powers and then remove them.
For a real primitive nonprincipal character, `chi(p)^2=1` away from the
finitely many primes dividing `q`. The square contribution is

\[
 2M\sum_p{\log p\over p}\,
       \kappa\!\left(M(u-2\log p)\right).
\]

Replacing `d theta(t)` by `dt` and putting
`y=M(u-2 log t)` gives

\[
 2M\int_0^\infty {1\over t}\kappa(M(u-2\log t))dt
 =\int_{-\infty}^{Mu}\kappa(y)dy
 =\mu_\kappa+O_\kappa(e^{-aMU}).                         \tag{3.3}
\]

The classical PNT error and BV partial summation make (3.3) uniform on the
moving window, with error `o(sqrt(M log M))` when
`log M=o(log U)`. Powers `p^k`, `k>=3`, are exponentially smaller, with the
largest scale coming from `k=3`, namely `exp(-u/6)` after normalization. The
primes dividing fixed `q` are also exponentially negligible.

## 4. The zero transform and the exact covariance

Assume GRH for `L(s,chi)` and NCZ,

\[
 L(1/2,\chi)\ne0.                                        \tag{4.1}
\]

Write the indexed nonzero ordinates as `gamma`. Applying the explicit formula
to the von Mangoldt version of (3.1), a zero
`rho=1/2+i gamma` contributes

\[
 2M\int_0^\infty t^{\rho-3/2}
       \kappa(M(u-\log t))dt
 =2\widehat\kappa(\gamma/M)e^{i\gamma u}.               \tag{4.2}
\]

Thus the natural zero polynomial is

\[
 S_{\kappa,M}^{(Z)}(u)
 =\sum_{0<|\gamma|\le Z}
     2\widehat\kappa(\gamma/M)e^{i\gamma u}.             \tag{4.3}
\]

Because `kappa` is real,
`hat kappa(-t)=overline{hat kappa(t)}`, so (4.3) is real.

For two kernels define the exact zero covariance

\[
 \mathcal C_{\kappa,\lambda}(M)
 :=4\sum_{\gamma\ne0}
   \widehat\kappa(\gamma/M)
   \overline{\widehat\lambda(\gamma/M)}
 =8\sum_{\gamma>0}\Re\!\left(
   \widehat\kappa(\gamma/M)
   \overline{\widehat\lambda(\gamma/M)}\right).         \tag{4.4}
\]

In particular,

\[
 \sigma_\kappa^2(M):=\mathcal C_{\kappa,\kappa}(M)
 =8\sum_{\gamma>0}|\widehat\kappa(\gamma/M)|^2.         \tag{4.5}
\]

Zero counting, (2.3), and Plancherel give

\[
 \mathcal C_{\kappa,\lambda}(M)
 =4M\log {qM\over2\pi}\,
       \langle\kappa,\lambda\rangle_{L^2(\mathbb R)}
   +O_{q,\kappa,\lambda}(M),                             \tag{4.6}
\]

and hence

\[
 \sigma_\kappa^2(M)
 \sim4M\log M\,\|\kappa\|_2^2.                         \tag{4.7}
\]

Only (4.7) is needed for the theorem. A refined second term is shape
dependent and involves
`int_0^infinity Re(hat kappa overline{hat lambda}) log t dt`; it should not be
stated until the Stieltjes error in the zero-counting formula is written
carefully. The leading constant in (4.6) is fixed unambiguously by (2.4).

The coefficient bounds and the diverging variance imply the Lindeberg ratio

\[
 {\max_\gamma|2\widehat\kappa(\gamma/M)|^2
   \over \sigma_\kappa^2(M)}
 \ll_\kappa {1\over M\log M}\longrightarrow0.           \tag{4.8}
\]

## 5. Flagship candidate theorem

Use the following precise hypotheses on the indexed positive ordinates of
`L(s,chi)`.

* **LI:** the positive ordinates are linearly independent over `Q`. With
  indexed multiplicities this implies simplicity.
* **QLI:** for every integer `k>=2`, there are `c_k>k` and a nondecreasing
  `g_k(T)` with `g_k(T)->infinity` and `g_k(T)<=log T` such that, uniformly in
  `epsilon in {+1,-1}^k`,

\[
 \#\left\{(\gamma_1,\ldots,\gamma_k)\in(0,T]^k:
 0<\left|\sum_{j=1}^k\epsilon_j\gamma_j\right|
 \le T^{-c_k}\right\}
 \ll_{k,\chi}{N_\chi(T)^{k/2}\over g_k(T)}.              \tag{5.1}
\]

This is Leung's Conjecture 10.1, with its little-oh written using a monotone
minorant `g_k`.

**Candidate theorem (shrinking Mellin-kernel white noise).** Fix a real
primitive nonprincipal character `chi` and a finite family
`kappa_1,...,kappa_r in K`. Assume GRH, NCZ, LI, and QLI for `L(s,chi)`. Let

\[
 M=M(U)\longrightarrow\infty,
 \qquad \log M=o(\log U).                                \tag{5.2}
\]

If `u` is uniform on `[U,2U]`, then

\[
 {1\over\sqrt{4M\log(qM/(2\pi))}}
 \bigl(\mathcal P_{\kappa_j,M}(u)-\mu_{\kappa_j}\bigr)_{j=1}^r
 \ \Longrightarrow\ \mathcal N_r(0,G),                \tag{5.3}
\]

where

\[
 G_{j\ell}=\int_{\mathbb R}\kappa_j(y)\kappa_\ell(y)dy. \tag{5.4}
\]

The Gaussian may be degenerate. For one nonzero kernel, exact-variance
normalization gives

\[
 {\mathcal P_{\kappa,M}(u)-\mu_\kappa
   \over\sigma_\kappa(M)}
 \Longrightarrow\mathcal N(0,1).                        \tag{5.5}
\]

The same argument should give convergence in `W_1` for every fixed finite
dimension, because the normalized vectors have uniformly bounded second
moments. No rate is asserted: qualitative QLI supplies no usable universal
rate.

The multivariate statement costs essentially nothing after the scalar proof.
For any fixed `a in R^r`, Cramer--Wold replaces the family by the single
admissible kernel `sum a_j kappa_j`; its variance limit is `a^T G a`.

## 6. Uniform explicit formula: exact promotion lemma needed

The first promotion gate is the following lemma.

**Required Lemma A (uniform kernel explicit formula).** Let `W` be a fixed
smooth time weight supported in a fixed compact subset of `(0,infinity)`.
Uniformly for `u` in the corresponding `U`-window, `M` satisfying (5.2), and
`Z=e^{4U}`,

\[
 \mathcal P_{\kappa,M}(u)
 =\mu_\kappa+S_{\kappa,M}^{(Z)}(u)
   +\mathcal R_{\kappa,M}(u,Z),
 \qquad
 \sup_u|\mathcal R_{\kappa,M}(u,Z)|
 =o_\kappa(\sqrt{M\log M}).                              \tag{6.1}
\]

There is no conceptual short-interval barrier here. A direct BV-Stieltjes
proof starts from the classical truncated formula

\[
 \psi(t,\chi)
 =-\sum_{|\gamma|\le Z}{t^{1/2+i\gamma}\over1/2+i\gamma}
 +O_q\!\left({t\log^2(tZ)\over Z}+\log t\right),         \tag{6.2}
\]

integrates against
`t^{-1/2} kappa(M(u-log t))`, and uses (2.1) to remove the remote lower
endpoint. The total variation of the scaled test function introduces at most
two extra powers of `M`. With `Z=e^{4U}` and `M=U^{o(1)}`, the truncation
and endpoint errors are exponentially below the scale in (6.1).

The prime-square calculation (3.3) follows by the same BV partial summation
from

\[
 \vartheta(t)=t+O(t e^{-c\sqrt{\log t}}),                 \tag{6.3}
\]

and costs at worst `O_kappa(M^2 e^{-c sqrt U})` on the window. Higher prime
powers cost `O_kappa(M^2 U^C e^{-U/6})`. These deliberately nonoptimal bounds
are already enough under (5.2).

What still has to be written, rather than waved away, is:

1. the integration-by-parts formula including every jump of `kappa`;
2. the lower endpoint and the finite set of primes dividing `q`;
3. uniformity on the enlarged support used by smooth majorants/minorants;
4. the exact separation of prime squares from powers `k>=3`;
5. approximation from finite-jump piecewise `C^1` kernels to the full BV
   class.

Until this lemma exists in full, (5.3) remains a candidate.

## 7. Low zeros and the QLI moment engine

Choose

\[
 T=Mh,\qquad h=h(U)\to\infty,                             \tag{7.1}
\]

diagonally so slowly that, for every fixed `k`,

\[
 \log h=o(\log M),\qquad
 {h^{k/2}\over g_k(Mh)}\to0,
 \qquad T\le U^{1/(2c_k)}                                \tag{7.2}
\]

eventually. Such a single `h` exists by a standard staged diagonal
construction, because every `g_k` tends to infinity and (5.2) makes
`T=U^{o(1)}`.

For a fixed scalar linear combination `kappa`, set

\[
 V_{\kappa,M,T}
 =\sum_{0<|\gamma|\le T}|2\widehat\kappa(\gamma/M)|^2.
\]

Equations (2.3) and zero counting give

\[
 \sigma_\kappa^2(M)-V_{\kappa,M,T}
 \ll_{q,\kappa}M^2{\log(qT)\over T},
 \qquad
 {\sigma_\kappa^2-V_{\kappa,M,T}\over\sigma_\kappa^2}
 =o(1).                                                   \tag{7.3}
\]

Expand a fixed `k`th moment against a nonnegative smooth time density. The
three classes of signed frequency sums are controlled as follows.

1. LI makes every exact relation balanced at each distinct ordinate. The
   distinct pairings give the Gaussian moment. Repeated-ordinate collisions
   are relatively

\[
 O_k\!\left({\max_\gamma|\widehat\kappa(\gamma/M)|^2
                   \over V_{\kappa,M,T}}\right)
 =O_{k,\kappa}((M\log M)^{-1}).                           \tag{7.4}
\]

2. QLI bounds near nonzero relations. After normalization their total is

\[
 \ll_{k,q,\kappa}{1\over g_k(T)}
 \left({T\log(qT)\over M\log(qM)}\right)^{k/2}
 =o_k(1),                                                 \tag{7.5}
\]

by (7.2).

3. For far relations, (2.3) and zero counting give

\[
 \sum_{0<|\gamma|\le T}|\widehat\kappa(\gamma/M)|
 \ll_{q,\kappa}M(\log(qT))^2.                            \tag{7.6}
\]

Schwartz decay of the time transform, together with
`UT^{-c_k}=U^{1-o(1)}`, beats this fixed-moment `ell^1` loss.

This proves all Gaussian moments for the low-zero polynomial once the
pairing/collision combinatorics are written without suppression. It is the
same engine as Leung's Proposition 10.1, now stable under every fixed
admissible Mellin shape and every fixed scalar combination of shapes.

## 8. High zeros: the central technical lemma

The second and genuinely delicate promotion gate is a complete proof of the
following statement.

**Required Lemma B (diagonal-aware high-zero removal).** Under QLI for
`k=2`, with `T=Mh` as above and `Z=e^{4U}`,

\[
 {1\over U}\int
 \left|\sum_{T<|\gamma|\le Z}
 2\widehat\kappa(\gamma/M)e^{i\gamma u}\right|^2
 W(u/U)du=o_\kappa(M\log M).                             \tag{8.1}
\]

The proof is kernel-uniform because (2.3) is exactly the bound used for the
exponential kernel. Put `Y_0=U^eta` with `0<eta<1/c_2` and split the sum
before squaring.

For `T<|gamma|<=Y_0`, dyadic decomposition gives:

\[
 \text{diagonal}\ll_{q,\kappa}
 M^2{\log(qT)\over T},                                   \tag{8.2}
\]

\[
 \text{QLI-close pairs}\ll_{q,\kappa}
 M^2{\log(qT)\over T g_2(T)},                            \tag{8.3}
\]

while the remaining pairs cost, for arbitrary fixed `A`,

\[
 \ll_{A,q,\kappa}
 (U Y_0^{-c_2})^{-A}M^2(\log(qY_0))^4.                   \tag{8.4}
\]

For `Y_0<|gamma|<=Z`, group ordinates into unit intervals. Same and adjacent
intervals cost

\[
 \ll_{q,\kappa}M^2{(\log(qY_0))^2\over Y_0};             \tag{8.5}
\]

nonadjacent intervals are absorbed by arbitrary Schwartz decay. The crude
`ell^1` coefficient norm through `Z=e^{4U}` is only
`O(MU^2)`, so a sufficiently large decay exponent wins. Opposite-sign
ordinates are easier because the relevant frequency is the sum of their
absolute values.

Dividing (8.2)--(8.5) by `M log M` gives `o(1)`: use `T=Mh`, (7.2),
`M=U^{o(1)}`, and `eta c_2<1`.

The diagonal (8.2) must remain visible. Leung's displayed Lemma 10.2 gives a
smaller bound with an additional `1/U`, but the proof as written appears to
replace a discrete close-pair sum by a continuous integral without first
retaining the terms `gamma=lambda`, for which the time transform equals one.
The natural diagonal is of order `log T/T` for his coefficients. The present
argument needs only that natural bound and therefore does not depend on the
stronger display. This source issue must receive external expert review before
being asserted publicly.

## 9. Completion and the power-race corollary

Assuming Lemmas A and B, the low-zero moment limit, Chebyshev, and Slutsky
give the scalar theorem for every fixed linear combination of kernels and
every fixed smooth time weight. Smooth majorants and minorants of
`1_[1,2]`, followed by a limit in their boundary width, give the sharp
uniform window. The normalized second moments stay bounded, so the absolute
values are uniformly integrable and weak convergence upgrades to `W_1`.
Cramer--Wold then proves (5.3).

Now take

\[
 \kappa_{\rm exp}(y)=e^{-y}{\bf1}_{[0,\infty)}(y).
\]

Then

\[
 \widehat\kappa_{\rm exp}(t)={1\over1+it},\qquad
 \mu_{\kappa_{\rm exp}}=1,\qquad
 \|\kappa_{\rm exp}\|_2^2={1\over2}.                   \tag{9.1}
\]

Writing `M=m+1/2`, (3.1) becomes exactly

\[
 \mathcal P_{\kappa_{\rm exp},M}(u)
 =2M e^{-Mu}\left(-\sum_{p\le e^u}
       \chi(p)p^{M-1/2}\log p\right)=E_M(e^u),           \tag{9.2}
\]

and its zero coefficient is

\[
 2\widehat\kappa_{\rm exp}(\gamma/M)
 ={2M\over M+i\gamma}.                                  \tag{9.3}
\]

Consequently (5.5) gives the candidate moving-weight theorem

\[
 {E_M(e^u)-1\over\sigma_M}\Longrightarrow\mathcal N(0,1),
 \qquad
 \sigma_M^2=8M^2\sum_{\gamma>0}{1\over M^2+\gamma^2}
 \sim2M\log M.                                          \tag{9.4}
\]

The multiplier in (9.2) is positive, so its sign is the sign of the original
power race. Since `sigma_M->infinity`, (9.4) implies

\[
 {1\over U}\operatorname{meas}\{u\in[U,2U]:
 R_{m(U),\chi}(e^u)>0\}\longrightarrow{1\over2}.         \tag{9.5}
\]

This is an actual finite-`x`, joint-limit dissolution theorem, not a statement
only about a fixed-`m` limiting random model.

For comparison, the sharp local kernel
`kappa_box=1_[-1/2,1/2]` gives a signed prime race in the multiplicative
window

\[
 e^{u-1/(2M)}\le p\le e^{u+1/(2M)}.                      \tag{9.6}
\]

Joint choices of translated or overlapping box kernels have limiting
correlations equal to their normalized overlap lengths. This is the concrete
white-noise content of (5.4).

## 10. What is proved, what is not, and the shortest paper

### Current classification

The theorem is **feasible and structurally consistent, but not yet proved in
the repository**.

Already checked from first principles:

* the physical scaling and prime-square center;
* the Fourier coefficient and every factor of two;
* the leading variance and covariance normalization;
* the QLI cutoff arithmetic for all fixed moments;
* the reduction of the multivariate result by Cramer--Wold;
* the high-zero estimates at the level of a complete dyadic blueprint;
* the exact recovery of the power-weight statistic.

Still fatal for submission:

1. Lemma A must be written line by line, first for finite-jump piecewise
   `C^1` kernels and then by BV approximation.
2. Lemma B must be written with signed ordinates, adjacent dyadic blocks,
   all cross terms, and the finite upper cutoff.
3. The pairing/collision combinatorics and the staged construction of `h(U)`
   must be explicit.
4. The sharp-window and vector `W_1` passages need complete measure
   normalization.
5. An independent analytic-number-theory expert must audit the apparent
   diagonal omission in Leung before it is mentioned in a paper.

### Honest novelty assessment

Leung's Theorem 10.1 already proves a moving univariate Gaussian theorem for
a shrinking sharp interval under RH, LI, and QLI. His Proposition 10.1 is the
moment template used here, and his paper explicitly says that a moving
multidimensional analogue is plausible but is not pursued. Therefore:

* a theorem only for the exponential kernel is mostly a nontrivial
  specialization/adaptation and is not a flagship;
* a theorem for one arbitrary scalar kernel is a useful abstraction, but may
  still be judged as repackaging;
* the finite-dimensional white-noise theorem, with actual Dirichlet prime
  races, a broad checkable BV class, the Gram covariance law, and a correct
  diagonal-aware tail theorem, is a genuine focused contribution;
* it is nevertheless built on an unproved all-order QLI assumption and does
  not introduce a fundamentally new CLT mechanism.

If the two lemmata close and an independent expert confirms them, a realistic
assessment is a strong specialist paper, roughly 8/10 in mathematical value
and substantially easier to read and verify than the 66-page manuscript. It
is not honestly a 9.5/10 prestige result. Reaching that level would require
removing or sharply weakening QLI, obtaining a new explicit range such as
`M=U^eta`, or proving a genuinely functional (tight process) limit rather
than only finite-dimensional convergence.

### Focused paper design

A self-contained paper can be about 22--28 pages:

1. one-page statement of the white-noise theorem and the power corollary;
2. admissible Mellin kernels and the uniform explicit formula;
3. covariance asymptotics and prime-square centering;
4. QLI moments, including exact collision combinatorics;
5. the diagonal-aware high-zero lemma;
6. sharp-window completion and two applications: exponential and boxes;
7. a short limitations section explaining why ordinary LI gives no explicit
   joint range.

The long weighted-races manuscript should remain frozen and be cited only for
motivation. The focused paper must reproduce every analytic input it uses, so
a reader never has to verify a 66-page dependency.

## 11. Primary-source ledger

* S.-K. Leung, *Joint distribution of primes in multiple short intervals*,
  arXiv:2401.04000v4, especially Conjecture 10.1, Theorem 10.1,
  Proposition 10.1, and Lemma 10.2:
  <https://arxiv.org/html/2401.04000v4#S10>.
* The source itself states after Theorem 10.1 that a multidimensional moving
  analogue under QLI is plausible but is not pursued.
* The current literature search found no arXiv paper stating the
  finite-dimensional Mellin-kernel/Dirichlet-race white-noise theorem above.
  That negative search is not proof of novelty; MathSciNet/Zentralblatt and
  an expert literature check remain mandatory before making a priority claim.

