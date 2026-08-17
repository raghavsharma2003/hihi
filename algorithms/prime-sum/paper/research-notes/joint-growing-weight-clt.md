# A moving-weight Gaussian theorem for the actual weighted prime race

Status: focused flagship-candidate note, 17 August 2026. This note does not
modify the manuscript and does not claim that the theorem below is ready for
submission. It identifies the strongest joint number-field theorem that the
present machinery appears able to prove, gives the proof architecture from
first principles, and isolates the one new uniform tail lemma that must be
written and refereed carefully.

## 1. Executive conclusion

There is a materially stronger target than the fixed-weight effective-ELI
adaptation:

> For a fixed real primitive character, the **actual**, sharply truncated
> weighted prime race is asymptotically Gaussian on a moving logarithmic
> window when the power weight tends to infinity, provided that its growth is
> subpower on the logarithmic-time scale and the zeros satisfy an all-order
> quantitative linear-independence hypothesis.

In the notation below, the natural range is

\[
 M=M(U)\longrightarrow\infty,
 \qquad \log M=o(\log U),                                 \tag{1.1}
\]

where `u` is averaged over `[U,2U]`, the prime-scale variable is `x=e^u`, and
`M=m+1/2`. Thus

\[
 M=(\log x)^{o(1)}.
\]

Examples covered by (1.1) include
`M=(log U)^B=(log log x)^B` for every fixed `B`, and
`M=exp((log U)^alpha)` for every fixed `alpha<1`. A fixed positive power
`M=U^eta=(log x)^eta` is not covered.

This is substantially stronger than a fixed-`m` convergence theorem. It also
has a simple probabilistic consequence: the proportion of logarithmic time in
`[U,2U]` for which the growing-weight race is positive tends to `1/2`.

The honest significance assessment is:

- the theorem would close the manuscript's explicit growing-weight/short-
  interval open direction;
- the proof has a real new uniformity problem, but its core moment mechanism
  is an exponential-Mellin-kernel adaptation of Leung's short-interval method;
- the power-race instance alone is likely a strong specialist result, not a
  prestige-journal flagship;
- a focused paper becomes substantially more attractive if it proves a
  general Mellin-kernel universality theorem and presents the power race as
  its sharp one-sided exponential-kernel application.

## 2. Exact formulation

Fix a real primitive nonprincipal character `chi` modulo `q`. Assume GRH for
`L(s,chi)` and

\[
 L(1/2,\chi)\ne0.                                         \tag{2.1}
\]

Write the positive ordinates, with multiplicity, as `gamma>0`. The LI
hypothesis below is understood for the indexed positive ordinates, so in
particular it implies simplicity.

For `M>0`, put `m=M-1/2` and

\[
 E_M(e^u)
 :=2M e^{-Mu}\left(-\sum_{p\le e^u}\chi(p)p^{M-1/2}\log p\right). \tag{2.2}
\]

The variance dictated by the explicit formula is

\[
 \sigma_M^2
 :=8M^2\sum_{\gamma>0}\frac1{M^2+\gamma^2}
 =4M\frac{\xi'}{\xi}(M+1/2,\chi).                         \tag{2.3}
\]

For fixed `q`, the manuscript proves

\[
 \sigma_M^2=2M\log\frac{qM}{2\pi}+O_q(1)\asymp_q M\log M. \tag{2.4}
\]

We need a Dirichlet-`L` version of Leung's quantitative LI hypothesis.

**Hypothesis QLI(chi).** For each integer `k>=2` there are `c_k>k` and a
nondecreasing function `g_k(T)`, with `g_k(T)->infinity` and
`g_k(T)<=log T`, such that, uniformly over
`epsilon=(epsilon_1,...,epsilon_k) in {+1,-1}^k`,

\[
 \#\left\{(\gamma_1,\ldots,\gamma_k)\in(0,T]^k:
 0<\left|\sum_{j=1}^k\epsilon_j\gamma_j\right|
 \le T^{-c_k}\right\}
 \ll_{k,\chi}\frac{N_\chi(T)^{k/2}}{g_k(T)}.              \tag{2.5}
\]

The `g_k` formulation is just the quantified form of an `o_k(N(T)^(k/2))`
statement. It makes every loss visible.

**Candidate Theorem (moving-weight Gaussian race).** Assume GRH, (2.1), LI,
and QLI(chi). Let `M=M(U)` satisfy (1.1), and choose `u` uniformly on
`[U,2U]`. Then

\[
 Z_U(u):=\frac{E_{M(U)}(e^u)-1}{\sigma_{M(U)}}
 \ \xrightarrow[U\to\infty]{\ d\ }\ \mathcal N(0,1).    \tag{2.6}
\]

In fact the proof should give convergence in `W_1`:

\[
 W_1\bigl(\operatorname{Law}_{u\in[U,2U]}(Z_U(u)),
           \mathcal N(0,1)\bigr)\longrightarrow0.         \tag{2.7}
\]

Let

\[
 X_M=1+\Re\sum_{\gamma>0}\frac{4M}{M+i\gamma}U_\gamma,
                                                               \tag{2.8}
\]

where the `U_gamma` are independent and uniform on the unit circle. Then the
same argument plus the independent-sum Berry--Esseen estimate gives

\[
 W_1\left(\operatorname{Law}(Z_U),
 \operatorname{Law}\left(\frac{X_M-1}{\sigma_M}\right)\right)
 \longrightarrow0.                                        \tag{2.9}
\]

Finally, because `sigma_M->infinity` and the normal distribution is continuous
at zero,

\[
 \frac1U\operatorname{meas}\{u\in[U,2U]:R_{m(U),\chi}(e^u)>0\}
 \longrightarrow\frac12.                                  \tag{2.10}
\]

Equation (2.10) is a joint finite-`x` dissolution theorem for the actual race,
not merely for its fixed-weight limiting random model.

## 3. Why the normalization reveals the theorem

Pairing conjugate zeros in the shifted explicit formula gives

\[
 E_M(e^u)=1+\sum_{0<|\gamma|\le Z}c_M(\gamma)e^{i\gamma u}
              +\mathcal R_M(u,Z),                          \tag{3.1}
\]

where

\[
 c_M(\gamma)=\frac{2M}{M+i\gamma},\qquad
 c_M(-\gamma)=\overline{c_M(\gamma)}.                     \tag{3.2}
\]

These coefficients have the three decisive properties

\[
 |c_M(\gamma)|\le2,
 \qquad
 \sum_{\gamma\ne0}|c_M(\gamma)|^2=\sigma_M^2,
 \qquad
 \sigma_M^2\asymp_q M\log M.                             \tag{3.3}
\]

Thus no single zero contributes a nonnegligible fraction of the variance:

\[
 \frac{\max_\gamma|c_M(\gamma)|^2}{\sigma_M^2}
 \ll_q\frac1{M\log M}\longrightarrow0.                  \tag{3.4}
\]

The weight is simultaneously a short-interval kernel and a triangular-array
CLT kernel. In logarithmic distance `v=u-log p`, its envelope is
`exp(-Mv)1_(v>=0)`, of width `1/M`; on the zero side its Mellin transform is
exactly `M/(M+i gamma)`.

This also explains why normalizing before estimating is essential. The
Euclidean Lipschitz norm of all zero coefficients is `sigma_M`, not the crude
`O(M)` bound obtained from `|c_M(gamma)|<=2M/|gamma|`. After division by
`sigma_M`, the torus map has norm one.

## 4. Uniform explicit formula: the constants can be exposed

The current manuscript states the shifted explicit formula with fixed-`m`
constants, but its proof already contains the required uniform estimate for
large `M`.

Start with its classical formula, uniform in `T>=2`,

\[
 \psi(x,\chi)=-\sum_{|\gamma|\le Z}\frac{x^\rho}{\rho}
 +O_q\left(\frac{x\log^2(xZ)}Z+\log x\right).              \tag{4.1}
\]

Partial summation gives, for `m>=0`,

\[
 \psi_m(x)=-\sum_{|\gamma|\le Z}\frac{x^{m+\rho}}{m+\rho}
 +O_q\left(\frac{x^{m+1}\log^2(xZ)}Z+x^m\log x
            +m2^m\right).                                 \tag{4.2}
\]

Here the integral of the truncation error costs only
`m/(m+1)<=1`; the last term is the lower-endpoint zero sum and is bounded
using `sum gamma^(-2)<infinity`. This is the dependence hidden by the fixed-`m`
notation.

For `m>=0`, prime powers of exponent at least three satisfy the already
uniform bound

\[
 \sum_{k\ge3}\sum_{p^k\le x}p^{km}\log p
 \ll x^{m+1/3}\log x.                                    \tag{4.3}
\]

For the square term, write `y=sqrt x` and
`theta(y)=y+O(y exp(-2c sqrt(log y)))`. Splitting the partial-summation
integral at `sqrt y`, but retaining the parameter, gives

\[
 \sum_{p\le y}p^{2m}\log p
 =\frac{y^{2M}}{2M}
 +O\left(y^{2M}e^{-c\sqrt{\log y}}+y^M+M2^{2M}\right).    \tag{4.4}
\]

The finitely many primes dividing `q` add `O_q(q^(2m)log q)`, harmless in
the moving window.

Take `x=e^u`, `u in [U,2U]`, and `Z=e^(3U)`. Combining (4.2)--(4.4) yields
the following auditable target bound:

\[
 \sup_{U\le u\le2U}|\mathcal R_M(u,e^{3U})|
 \ll_q MU^2e^{-2U}+MUe^{-U/2}+MUe^{-U/6}
       +Me^{-c\sqrt U}+Me^{-MU/2}+M^2e^{-M(U-C_q)}.       \tag{4.5}
\]

Every term in (4.5) is `o(sigma_M)` under (1.1). No short-interval prime
theorem beyond the classical PNT error is needed for this step.

This lemma should be written formally before claiming the candidate theorem,
but there is no remaining conceptual obstruction in its constant ledger.

## 5. The finite zero cutoff and Gaussian moments

Choose

\[
 T=Mh,\qquad h=h(U)\longrightarrow\infty                 \tag{5.1}
\]

so slowly that

\[
 \log h=o(\log M),\qquad \log T=o(\log U),               \tag{5.2}
\]

and, for each fixed `k`,

\[
 \frac{h^{k/2}}{g_k(T)}\longrightarrow0.                 \tag{5.3}
\]

Such a diagonal choice exists because `M->infinity`, every `g_k->infinity`,
and `log M=o(log U)`. Define

\[
 S_{M,T}(u)=\sum_{0<|\gamma|\le T}c_M(\gamma)e^{i\gamma u},
 \qquad
 V_{M,T}=\sum_{0<|\gamma|\le T}|c_M(\gamma)|^2.          \tag{5.4}
\]

Zero counting and partial summation give

\[
 \sigma_M^2-V_{M,T}
 \ll_q M^2\frac{\log(qT)}T,
 \qquad
 \frac{\sigma_M^2-V_{M,T}}{\sigma_M^2}
 \ll_q\frac{M}{T}\frac{\log(qT)}{\log(qM)}=o(1).         \tag{5.5}
\]

Use a nonnegative smooth time weight `W(u/U)` with unit mass. Expanding the
`k`th moment of `S_(M,T)` produces signed sums

\[
 \sum_{\boldsymbol\epsilon,\boldsymbol\gamma}
 c_M^{\boldsymbol\epsilon}(\boldsymbol\gamma)
 \widehat W\left(U\sum_j\epsilon_j\gamma_j\right).       \tag{5.6}
\]

There are three classes.

1. **Exact relations.** LI says that every exact relation is balanced at each
   distinct ordinate. Pairings with distinct ordinates give the Gaussian
   moment. Repeated-ordinate collisions cost

   \[
   O_k\left(\frac{\max|c_M|^2}{V_{M,T}}\right)
   =O_{k,q}\left(\frac1{M\log M}\right)                  \tag{5.7}
   \]

   relative to the main moment.

2. **Near nonzero relations.** QLI bounds their number by
   `N(T)^(k/2)/g_k(T)`. Since `|c_M|<=2`, `N(T)asymp_q T log T`, and
   `V_(M,T)asymp_q M log M`, their normalized contribution is

   \[
   \ll_{k,q}\frac1{g_k(T)}
       \left(\frac{T\log T}{M\log M}\right)^{k/2}
   \ll_{k,q}\frac{h^{k/2}}{g_k(T)}=o_k(1).               \tag{5.8}
   \]

3. **Far relations.** For
   `|sum epsilon_j gamma_j|>T^(-c_k)`, Schwartz decay gives an arbitrary
   power of `(U T^(-c_k))^(-1)`. The coefficient `ell^1` bound

   \[
   \sum_{0<|\gamma|\le T}|c_M(\gamma)|
   \ll_q M(\log(qT))^2                                  \tag{5.9}
   \]

   and `log T=o(log U)` make this contribution `o_k(V_(M,T)^(k/2))`.

Therefore every fixed normalized moment tends to the corresponding Gaussian
moment. Since the normal law is moment-determinate,

\[
 S_{M,T}(u)/\sqrt{V_{M,T}}\Rightarrow\mathcal N(0,1).     \tag{5.10}
\]

The second-moment case also supplies the uniform integrability needed to
upgrade weak convergence to `W_1` after the tail step below.

## 6. The critical new lemma: uniform high-zero removal

The actual prime sum cannot be replaced directly by the low-zero sum at
height `T=Mh`: the pointwise explicit-formula remainder at that height is far
too large. One must first use height `e^(3U)` in (4.5), then remove the zeros
between `T` and `e^(3U)` in mean square.

The required statement is:

**Uniform high-zero lemma.** Under QLI(chi) for `k=2`, if (1.1)--(5.2) hold,
then

\[
 \frac1U\int
 \left|\sum_{T<|\gamma|\le e^{3U}}c_M(\gamma)e^{i\gamma u}\right|^2
 W(u/U)\,du=o(\sigma_M^2).                                \tag{6.1}
\]

A safe proof splits at

\[
 Y_0=U^\eta,\qquad 0<\eta<1/c_2.                         \tag{6.2}
\]

For `T<|gamma|<=Y_0`, use dyadic blocks.

- The diagonal contributes

  \[
  \sum_{|\gamma|>T}|c_M(\gamma)|^2
  \ll_q M^2\frac{\log(qT)}T=o(\sigma_M^2).                \tag{6.3}
  \]

- Off-diagonal pairs with
  `0<|gamma-lambda|<=Y^(-c_2)` are bounded by QLI on each block. Their total
  is

  \[
  \ll_q M^2\frac{\log(qT)}{Tg_2(T)}.                     \tag{6.4}
  \]

- On the remaining pairs, rapid decay of `hat W` and
  `U Y_0^(-c_2)>=U^(1-eta c_2)` beat the squared `ell^1` coefficient norm.

For `|gamma|>Y_0`, no small-divisor hypothesis is needed. The unit-interval
zero count `N(t+1)-N(t)<<_q log(q(t+2))`, with the decay of `hat W`, gives the
deliberately crude but sufficient bound

\[
 \ll_q M^2\frac{(\log(qY_0))^2}{Y_0}.                    \tag{6.5}
\]

After division by `sigma_M^2 asymp M log M`, (6.5) tends to zero because
`M=U^(o(1))` and `Y_0=U^eta`. Equations (6.3)--(6.5) prove (6.1).

This split is essential. A direct unit-interval bound starting at `T=Mh`
would lose an extra logarithm and would not close against the very slowly
growing `h` allowed by QLI.

### A concrete source issue that must not be copied

Leung's arXiv v4, Lemma 10.2, displays a high-zero mean-square bound of size

\[
 \frac{(\log T)^2}{TU}+U^3e^{-U/2}.                       \tag{6.6}
\]

As written, the proof of (6.6) does not account for the diagonal contribution
`sum_(|gamma|>T)|w(rho)|^2`, whose natural upper scale is `log T/T` and whose
individual terms carry no factor `1/U`, since `hat W(0)=1`. It also replaces a
discrete close-pair sum by a continuous double integral without first
separating the diagonal. Off-diagonal cancellation sufficient to erase that
term is not established in the displayed argument. Thus the quoted bound is
not presently justified by that argument. The theorem can still close after
restoring `O(log T/T)`, because Leung assumes `delta T->infinity`, but Lemma
9.3 should not be cited verbatim as the tail input for the present project.

The proof above repairs the diagonal explicitly and uses QLI only where
sub-unit zero spacing is genuinely relevant.

## 7. Completion of the theorem

Combine:

- the uniform explicit formula (4.5);
- the high-zero lemma (6.1);
- the low-zero moment limit (5.10); and
- the variance comparison (5.5).

Chebyshev's inequality removes the high-zero tail, and Slutsky's theorem gives
(2.6) for a smooth time weight. Smooth majorants and minorants of
`1_[1,2]`, followed by a limit in their boundary width, give the uniform time
average. The second moments remain bounded throughout, so the same
approximation supplies uniform integrability of the absolute value and hence
the `W_1` conclusion (2.7).

For the limiting model (2.8), a standard Berry--Esseen inequality for
independent summands gives

\[
 W_1\left(\operatorname{Law}\left(\frac{X_M-1}{\sigma_M}\right),
 \mathcal N(0,1)\right)
 \ll\frac{\sum_{\gamma>0}|4M/(M+i\gamma)|^3}{\sigma_M^3}
 \ll_q\frac1{\sqrt{M\log M}}.                             \tag{7.1}
\]

The numerator bound follows by partial summation:

\[
 \sum_{\gamma>0}\frac{M^3}{(M^2+\gamma^2)^{3/2}}
 \ll_q M\log(qM).                                        \tag{7.2}
\]

Equations (2.7) and (7.1) imply (2.9) by the triangle inequality.

Finally, `E_M(e^u)>0` if and only if the race is positive, while

\[
 E_M(e^u)>0\quad\Longleftrightarrow\quad Z_U(u)>-1/\sigma_M.
\]

Since `1/sigma_M->0`, (2.6) proves (2.10).

## 8. Exact bottlenecks and no-go statements

### 8.1 Ordinary LI gives no explicit joint range

LI identifies exact relations, but gives no uniform bound on near relations
in (5.6). A rationally independent frequency vector can have arbitrarily
small integer linear forms and arbitrarily slow finite-time equidistribution.
Thus GRH+LI alone cannot justify (1.1) or any other explicit `M=M(U)` range by
this method.

Under GRH+LI one can diagonalize non-effectively and obtain the existence of
some extremely slowly growing admissible `M_*(U)->infinity`, but that statement
has no usable scale and is not a flagship result.

### 8.2 GRH alone is not a Gaussian hypothesis

GRH controls the real parts of zeros. It does not control their additive
relations, multiplicities, pair correlations, or higher correlations. Those
data enter the second and all higher finite-time moments. A GRH-only normal
law for the sharp growing-weight race would therefore require a genuinely new
mechanism, not a sharper version of the present explicit formula.

### 8.3 Classical short-interval estimates do not supply a distribution

The PNT and GRH short-interval bounds control the size or mean of a prime sum;
they do not prove a CLT. On the physical side, Montgomery--Soundararajan's
normal law for primes in much shorter intervals uses a uniform Hardy--Littlewood
prime-tuples conjecture. On the Fourier side, Leung uses LI plus QLI. There is
no known unconditional theorem that can simply be imported to prove (2.6) for
this fixed-character sharp race.

### 8.4 The theorem does not give the first bias term

Convergence in (2.6) implies only (2.10). It does **not** imply

\[
 \mathbb P_U(R_{m(U),\chi}>0)-\frac12
 \sim\frac1{\sqrt{2\pi}\,\sigma_M}.                      \tag{8.1}
\]

To prove (8.1), one needs a quantitative normal approximation whose
Kolmogorov error is `o(1/sigma_M)`. The qualitative QLI hypothesis supplies no
such rate. Claiming the fixed-model dissolution asymptotic for the actual
finite window would therefore be unjustified.

### 8.5 Why the range stops at subpower `M`

For the `k`th moment the zero cutoff must satisfy both `T/M->infinity` and
`T<=U^(1/c_k-o(1))`. Because the method needs every fixed `k`, and the QLI
exponents `c_k>k` grow with `k`, a fixed power `M=U^eta` cannot be retained
for all moments. The condition `log M=o(log U)` is exactly what permits a
diagonal cutoff for every fixed `k`.

## 9. A second, narrower route under effective LI

The fixed-weight Wasserstein note can also be uniformized after standardizing.
At a finite zero height `T`, its master inequality should become, for
`1<<M<<T`,

\[
 W_1(\operatorname{Law}(Z_U),\operatorname{Law}((X_M-1)/\sigma_M))
 \ll_q
 \sqrt{\frac{M}{T}}\frac{\log T}{\sqrt{\log M}}
 +\frac{\sqrt{N(T)}}H+\frac{\mathcal D(T,H)}U+o(1).       \tag{9.1}
\]

The crucial improvement over the unnormalized fixed-`m` statement is that the
torus Lipschitz constant is exactly `sqrt(2)` after division by `sigma_M`.
Under BHU's effective-LI hypothesis, optimizing `T=T(U)` gives a nontrivial
explicit growing-weight range roughly

\[
 M\log T=o(T).                                             \tag{9.2}
\]

This route gives a rate but permits much smaller `M` than (1.1). It is best
viewed as a quantitative supplement, not the main theorem. Obtaining the
first bias term (8.1) from a Wasserstein estimate and bounded-density smoothing
would require, conservatively,

\[
 T\gg M^3(\log M)^3,                                      \tag{9.3}
\]

so the usable weight range would shrink by about a cube root.

## 10. Best focused-paper design

The strongest honest compact paper is not "another theorem added to the
66-page manuscript." It is a separate paper organized around one statement:

**Gaussian universality for shrinking Mellin kernels in prime races.**

A clean 20--30 page design would be:

1. state a general one-sided Mellin-kernel triangular-array theorem under
   QLI;
2. prove the corrected high-zero lemma, with the diagonal shown explicitly;
3. specialize to the exponential kernel `c_M(gamma)=2M/(M+i gamma)` arising
   from power weights;
4. derive the actual-race dissolution consequence (2.10);
5. include a short section proving that ordinary LI and GRH alone cannot give
   the advertised explicit range by the same mechanism.

That paper would be far easier to read and verify than the current long
manuscript. The existing manuscript can remain frozen as the source of the
fixed-weight explicit formula, variance identity, and limiting-model
dissolution law.

## 11. Verification plan before promotion to theorem

The candidate should not enter a submission until all of the following are
done.

1. Write the large-`M` version of the shifted explicit formula with every
   constant displayed and independently check (4.5).
2. Prove the uniform high-zero lemma (6.1) in full dyadic detail, including
   signed ordinates, cross-block pairs, multiplicities, and the exact use of
   QLI for `k=2`.
3. Write the `k`th-moment combinatorics without suppressing repeated
   ordinates, and check the `h^(k/2)/g_k(T)` exponent.
4. Make the diagonal construction of `h(U)` explicit for the countable family
   `{g_k,c_k}`.
5. Verify the passage from smooth time weights to normalized Lebesgue measure
   on `[U,2U]`, including uniform integrability for `W_1`.
6. Have an analytic-number-theory expert audit the corrected reading of
   Leung's Lemma 10.2 before mentioning the apparent omission publicly.
7. Search the literature specifically for CLTs for general Mellin kernels;
   the targeted searches recorded here found no direct statement, but that is
   not a priority proof.

## 12. Primary sources

1. S.-K. Leung, *Joint distribution of primes in multiple short intervals*,
   arXiv:2401.04000v4 (2026), to appear in Advances in Mathematics. Theorem
   10.1 and Proposition 10.1 provide the QLI/moment template; Lemma 10.2 requires
   the diagonal correction discussed in Section 6.
   <https://arxiv.org/abs/2401.04000>
2. A. Bailleul, M. Hayani, T. Untrau, *A Wasserstein metric approach to
   generalized Skewes' numbers. I. Prime number races*, arXiv:2603.20093v2
   (2026), especially their quantitative Kronecker--Weyl theorem and
   high-zero mean-square estimates.
   <https://arxiv.org/abs/2603.20093>
3. Y. Lamzouri, *An effective Linear Independence conjecture for the zeros of
   the Riemann zeta function and applications*, arXiv:2311.04860v2 (2024).
   <https://arxiv.org/abs/2311.04860>
4. H. L. Montgomery, K. Soundararajan, *Primes in short intervals*,
   arXiv:math/0409258 (2004), for the physical-side conditional Gaussian law
   under a uniform Hardy--Littlewood prime-tuples conjecture.
   <https://arxiv.org/abs/math/0409258>
5. A. Akbary, N. Ng, M. Shahabi, *Limiting distributions of the classical
   error terms of prime number theory*, arXiv:1306.1657 (2013), for the
   qualitative Besicovitch-almost-periodic limiting-distribution framework.
   <https://arxiv.org/abs/1306.1657>

## 13. Recommendation

Promote the moving-weight Gaussian theorem, not the fixed-`m` effective rate,
as the next mathematical target. Freeze the long paper. Build a short companion
around (2.6)--(2.10), but describe it initially as a candidate until the uniform
high-zero lemma and the large-`M` explicit-formula ledger have survived an
independent proof audit.

If those two lemmata close exactly as above, this is a real, focused, and
publishable advance. It is not yet a 9.5/10 breakthrough: its central moment
strategy has a clear predecessor in Leung. The path to a higher-impact result
is to prove the kernel theorem in genuine generality or to obtain the first
finite-window bias asymptotic (8.1), not to add more medium-sized results to
the existing manuscript.
