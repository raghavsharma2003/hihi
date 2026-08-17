# Effective finite-x convergence for the weighted race

Status: proof draft for internal audit, 17 August 2026.  This note does not
modify the manuscript.  It proves a fixed-character, fixed-weight conditional
theorem and records exactly why GRH+LI alone cannot give a rate.  All uses of
recent literature below are to primary sources.

## 1. Normalization and the needed Diophantine hypothesis

Fix a real primitive character `chi` modulo `q>=3`, and put

\[
 M=m+\tfrac12>0,\qquad
 E_m(x)=2M x^{-M}\left(-\sum_{p\le x}\chi(p)p^{m}\log p\right).
\]

Assume GRH for `L(s,chi)` and `L(1/2,chi) != 0`.  Enumerate the positive
ordinates of its nontrivial zeros, with multiplicity, as
`gamma_1 <= gamma_2 <= ...`, and let `N(T)=#{j: gamma_j<=T}`.  The coefficients
in the manuscript's shifted explicit formula are

\[
 r_j(m)=\frac{4M}{M+i\gamma_j}.
\]

Thus the limiting random variable under LI is

\[
 X_m=1+\sum_{j\ge1}\Re\bigl(r_j(m)Z_j\bigr),                 \tag{1.1}
\]

where the `Z_j` are independent and uniform on the unit circle.  This is the
same variable as `1+sum 2 a_gamma(m) cos(theta_gamma)` in the manuscript,
because `|r_j|=2a_{gamma_j}=4M/(M^2+gamma_j^2)^(1/2)`.

For `A>1`, use the following single-character version of the effective-LI
hypothesis of Bailleul--Hayani--Untrau (BHU): there are specified constants
`c_ELI>0` and `T_ELI>=3` such that, for every `T>=T_ELI` and every nonzero
integer vector `k=(k_1,...,k_N)` with `|k_j|<=N=N(T)`,

\[
 \left|\sum_{j=1}^{N}k_j\gamma_j\right|
 \ge c_{\rm ELI}N^{-N^A}.                                  \tag{ELI_A}
\]

This implies ordinary LI.  Indeed, any fixed finite integer relation can be
padded by zeros and then tested at a sufficiently large height, where both
its support and its largest coefficient are at most `N(T)`.

The combined shifted explicit formula used below is stated in the manuscript
for `u>=2`.  Put `u_*:=2`.  For `U>u_*`, define the actual finite-log-time law

\[
 \mu_{m,U}:=\frac1{U-u_*}\int_{u_*}^{U}\delta_{E_m(e^u)}\,du, \tag{1.2}
\]

and write `nu_m=Law(X_m)`.  Wasserstein distance always means `W_1` on the
real line.

## 2. Candidate theorem (proved below)

**Theorem A (effective finite-log-time convergence).**  Fix `chi`, `m>-1/2`
and `A>1`.  Assume GRH, central nonvanishing, and `(ELI_A)` with specified
constants.  There are effective constants `K>0` and `U_0>e`, depending only
on `q, chi, m, A, c_ELI, T_ELI` and on effective constants in the standard
explicit formula, such that for every `U>=U_0`,

\[
 W_1(\mu_{m,U},\nu_m)
 \le K\,(\log\log U)^2(\log U)^{-1/(2A)}.                    \tag{2.1}
\]

The law `nu_m` has a bounded continuous density.  Consequently, with

\[
 \delta_\chi(m)=\Pr(X_m>0),
\]

one also has

\[
 \left|\frac1{U-u_*}\int_{u_*}^{U}
       1_{\{R_{m,\chi}(e^u)>0\}}\,du-\delta_\chi(m)\right|
 \le K\,(\log\log U)(\log U)^{-1/(4A)}.                    \tag{2.2}
\]

The second occurrence of `K` may be enlarged.  Replacing the lower endpoint
`u_*=2` in (2.2) by the conventional `log 2` changes that proportion by at
most `O(1/U)`, so the same bound holds after enlarging `K`.  If the largest
prime-scale argument is denoted by `Y=e^U`, (2.1) reads

\[
 W_1(\mu_{m,\log Y},\nu_m)
 \ll_{\chi,m,A}
 \frac{(\log\log\log Y)^2}{(\log\log Y)^{1/(2A)}}.          \tag{2.3}
\]

This translation is important: the theorem is effective but the guaranteed
rate is extremely slow on the ordinary `x` scale.

The following two-parameter inequality is the more informative result behind
Theorem A.  It displays the Diophantine input instead of hiding it in ELI.
For `N=N(T)`, `H>=1`, set

\[
 \mathcal D(T,H)^2=
 \sum_{0<\|k\|_\infty\le H}
 \frac1{\|k\|_2^2\,|k\cdot\gamma^{(T)}|^2},\qquad
 \gamma^{(T)}=(\gamma_1,\ldots,\gamma_N).                  \tag{2.4}
\]

Under LI all denominators in (2.4) are nonzero.

**Proposition B (finite-height master bound).**  Under GRH, central
nonvanishing, and LI, put `T_1(chi)=max(4,gamma_1(chi))`.  For fixed
`m>-1/2`, all `T>=T_1(chi)` (so `N(T)>=1`), all real `H>=1`, and all
`U>=max(4,log T)`,

\[
\begin{split}
 W_1(\mu_{m,U},\nu_m)\ \le\ &C_{\chi,m}\left(
       \frac{\log T}{\sqrt T}+U^{-1/2}\right)\\
 &+L_m\left(\frac{4\sqrt3\sqrt{N(T)}}H
       +\frac{2\mathcal D(T,H)}{U-u_*}\right),              \tag{2.5}
\end{split}
\]

where one may take

\[
 L_m=\left(\sum_{j\ge1}|r_j(m)|^2\right)^{1/2}
 \le 2\sqrt{2C(\chi)}\,M,\qquad
 C(\chi)=2\sum_{j\ge1}\gamma_j^{-2}.                      \tag{2.6}
\]

All constants in (2.5), except the displayed Diophantine sum, are effective
for fixed `chi,m`.  Formula (2.5) can therefore also be used with rigorously
certified finite lower bounds for zero linear forms, without assuming the
full asymptotic ELI conjecture.

## 3. Proof of Proposition B

### 3.1 The shifted explicit formula has the right uniformity in height

The manuscript's Lemmas `lem:trunc` and `lem:squares`, paired over conjugate
zeros, give for every `u>=2` and every `S>=2`

\[
 E_m(e^u)=1+\Re\sum_{0<\gamma_j\le S}r_j(m)e^{i\gamma_j u}
              +\mathcal E_m(u,S),                           \tag{3.1}
\]

with

\[
 |\mathcal E_m(u,S)|\ll_{q,m}
 \frac{e^{u/2}(u+\log S)^2}{S}
 +u^2e^{-\kappa_m u}+ue^{-u/6}+e^{-c\sqrt u},               \tag{3.2}
\]

where `kappa_m=min(M,1/2)>0`.  The four terms after the zero sum have the
following origins: truncating the weighted von Mangoldt formula, its
`(1+x^m)log x` floor together with the higher-prime-power floor, prime powers
of exponent at least three, and the PNT error in the prime-square main term.

For fixed `m`, the final three functions in (3.2) lie in both `L^1(2,infty)`
and `L^2(2,infty)`.  This is the exact point at which `m>-1/2` is required.
Choose `S=e^U`.  Since

\[
 \frac1{U-u_*}\int_{u_*}^{U}
 e^{u/2}(u+U)^2e^{-U}\,du\ll Ue^{-U/2}\ll U^{-1/2},          \tag{3.3}
\]

and every fixed integrable remainder contributes `O_{q,m}(U^{-1})`, the
average absolute contribution of `mathcal E_m(u,e^U)` is
`O_{q,m}(U^{-1/2})`.

This verifies that the extra weighted prime-power terms do **not** obstruct
the BHU argument.  They are absent in the unweighted BHU normalization, but
after the present normalization all are integrable in logarithmic time.

### 3.2 The high-zero mean-square estimate survives the shifted denominator

Define

\[
 F_{m,T}(u)=1+\Re\sum_{0<\gamma_j\le T}r_j(m)e^{i\gamma_j u}.
\]

By (3.1) with `S=e^U`, the difference `E_m(e^u)-F_{m,T}(u)` is the zero sum
over `T<gamma_j<=e^U` plus the remainder just bounded.  For every positive
ordinate,

\[
 |r_j(m)|=\frac{4M}{\sqrt{M^2+\gamma_j^2}}\le\frac{4M}{\gamma_j}. \tag{3.4}
\]

To track the conjugate pairing without suppressing a frequency, write the
real part as a sum over the signed ordinates `alpha=+/-gamma`, with
coefficients `r_gamma/2` and `conj(r_gamma)/2`.  Expanding its square and
integrating in `u` therefore produces both the `gamma-lambda` and
`gamma+lambda` frequencies.  The latter are harmless because, for positive
`gamma,lambda`,

\[
 \min(U,(\gamma+\lambda)^{-1})
 \le \min(U,|\gamma-\lambda|^{-1}),
\]

with the right side interpreted as `U` on the diagonal.  Equivalently one
can apply BHU Corollary 5.2(iii) directly to the signed ordinates.  Thus the
integrated square is bounded, up to a fixed absolute factor, by

\[
 M^2\sum_{\gamma,\lambda>T}
 \frac1{\gamma\lambda}
 \min\left(U,\frac1{|\gamma-\lambda|}\right).               \tag{3.5}
\]

When `gamma=lambda`, the minimum is interpreted as `U`.  (The coefficients
of the signed sum are bounded by `2M/|alpha|`; this is consistent with the
displayed factor `M^2` after absorbing an absolute constant.)  The
zero-counting argument in BHU, Corollary 5.2(iii) and its appendix proof, uses only
`N(t+1)-N(t)<<_q log(t+2)` and gives

\[
 \sum_{\gamma,\lambda>T}\frac1{\gamma\lambda}
 \min\left(U,\frac1{|\gamma-\lambda|}\right)
 \ll_q U\frac{(\log T)^2}{T}+\frac{(\log T)^3}{T}.           \tag{3.6}
\]

No lower bound for zero spacings is used in (3.6), and multiplicities are
included in every zero count: pairs at distance at most one are bounded by
the number of zeros in a unit interval.  More explicitly,
use

\[
 \min(U,|\gamma-\lambda|^{-1})
 \le \frac{2U}{1+U|\gamma-\lambda|}.
\]

For `|lambda-gamma|<=1`, one has `lambda asymp gamma` and there are
`O_q(log gamma)` such ordinates, giving after summing over `gamma>T` the
term `U(log T)^2/T`; this includes `lambda=gamma`.  For
`1<|lambda-gamma|<=gamma/2`, unit-shell summation contributes a harmonic
factor and gives `(log T)^3/T`.  The two ranges
`lambda<gamma/2` and `lambda>3gamma/2` (including the negative-ordinate
range, which represents the `gamma+lambda` frequencies above) have
`|lambda-gamma|` comparable to the larger ordinate and are smaller.  This is
the complete five-range argument in the BHU appendix and also verifies the
diagonal and multiplicity conventions directly.  Divide the resulting
mean-square estimate by `U-u_*` and use Cauchy--Schwarz only for the
high-zero sum; add the truncation and integrable remainders with their
`L^1` bounds from Section 3.1.  Since `U>=log T`, this yields

\[
 \frac1{U-u_*}\int_{u_*}^{U}|E_m(e^u)-F_{m,T}(u)|\,du
 \ll_{q,m}\frac{\log T}{\sqrt T}+O_{q,m}(U^{-1/2}).          \tag{3.7}
\]

Thus BHU Lemma 5.6 adapts: replacing `1/2+i gamma` by `M+i gamma` merely
introduces the fixed factor `M` in (3.4).

Let `mu_{m,U}^{(T)}` be the pushforward of normalized Lebesgue measure on
`[u_*,U]` by `F_{m,T}`.  Coupling values at the same `u` in (3.7) gives

\[
 W_1(\mu_{m,U},\mu_{m,U}^{(T)})
 \ll_{q,m}\frac{\log T}{\sqrt T}+U^{-1/2}.                  \tag{3.8}
\]

### 3.3 Quantitative Kronecker--Weyl for the truncated sum

Let `lambda_N` be Haar probability measure on `(S^1)^N`.  Under LI, the map

\[
 u\longmapsto(e^{i\gamma_1u},\ldots,e^{i\gamma_Nu})
\]

is equidistributed in the full torus.  BHU Theorem 3.4 (their quantitative
continuous Kronecker--Weyl theorem) states that its finite-time law
`sigma_U^(T)` satisfies

\[
 W_1(\sigma_U^{(T)},\lambda_N)
 \le\frac{4\sqrt3\sqrt N}{H}
 +\frac{2\mathcal D(T,H)}{U-u_*}.                            \tag{3.9}
\]

The map

\[
 g_{m,T}(z_1,\ldots,z_N)=1+\Re\sum_{j\le N}r_j(m)z_j
\]

is Lipschitz, for the Euclidean product of arc-length metrics, with constant

\[
 \left(\sum_{j\le N}|r_j(m)|^2\right)^{1/2}\le L_m.          \tag{3.10}
\]

The last inequality in (2.6) follows from (3.4) and the definition of
`C(chi)`.  Wasserstein distance contracts under an `L`-Lipschitz map by at
most the factor `L`; hence (3.9)--(3.10) give

\[
 W_1(\mu_{m,U}^{(T)},\nu_m^{(T)})
 \le L_m\left(\frac{4\sqrt3\sqrt N}{H}
 +\frac{2\mathcal D(T,H)}{U-u_*}\right),                    \tag{3.11}
\]

where `nu_m^(T)` is the law of the first `N(T)` terms of (1.1).

### 3.4 Passing from the truncated model to the full model

Couple `nu_m^(T)` and `nu_m` with the same independent phases.  Orthogonality
and (3.4) give

\[
\begin{split}
 W_1(\nu_m^{(T)},\nu_m)
 &\le \left(\frac12\sum_{\gamma_j>T}|r_j(m)|^2\right)^{1/2}\\
 &\ll_{q,m}\left(\sum_{\gamma_j>T}\gamma_j^{-2}\right)^{1/2}
 \ll_{q,m}\sqrt{\frac{\log T}{T}}.                          \tag{3.12}
\end{split}
\]

The last estimate is partial summation from `N(t)<<_q t log(t+2)`.  It is
smaller than the first term in (3.8).  The triangle inequality applied to
(3.8), (3.11), and (3.12) proves Proposition B.

## 4. From Proposition B to Theorem A

Put `N=N(T)` and take `H=N`.  Under `(ELI_A)`, for sufficiently large `T`,

\[
 \mathcal D(T,N)^2
 \le c_{\rm ELI}^{-2}(2N+1)^N N^{2N^A}
 \le c_{\rm ELI}^{-2}N^{3N^A}.                              \tag{4.1}
\]

Therefore, if

\[
 U-u_*\ge 4c_{\rm ELI}^{-1}N(T)^{2N(T)^A},                  \tag{4.2}
\]

the parenthesis in (3.11) is `O_A(N(T)^(-1/2))`.  Proposition B becomes

\[
 W_1(\mu_{m,U},\nu_m)
 \ll_{q,m,A,c_{\rm ELI}}
 \frac{\log T}{\sqrt T}+U^{-1/2}+N(T)^{-1/2}.               \tag{4.3}
\]

The Riemann--von Mangoldt formula gives `N(T) asymp_q T log T`.  As in BHU
Theorem 5.13, choose a sufficiently large fixed constant `D_q` and determine
`T=T(U)` through

\[
 P=D_qT\log(qT),\qquad U=P^{P^A}.                            \tag{4.4}
\]

Increasing `D_q` and the lower threshold if necessary makes (4.2) hold.  The
relations

\[
 P\asymp_A\left(\frac{\log U}{\log\log U}\right)^{1/A},
 \qquad T\asymp_q\frac{P}{\log P}                            \tag{4.5}
\]

then imply, with room to spare,

\[
 \frac{\log T}{\sqrt T}+N(T)^{-1/2}
 \ll_{q,A}(\log\log U)^2(\log U)^{-1/(2A)}.                 \tag{4.6}
\]

The monotonicity of the functions in (4.4) lets one make this choice for
every sufficiently large real `U`, not just a sequence.  Equations
(4.3)--(4.6) prove (2.1).

## 5. Passing from Wasserstein distance to the sign density

The characteristic function of `nu_m` is

\[
 e^{it}\prod_{j\ge1}J_0(|r_j(m)|t).                         \tag{5.1}
\]

For fixed `m`, the first three coefficients `|r_j(m)|` are positive.  The
standard bound `|J_0(t)|<<min(1,|t|^(-1/2))`, applied to those first three
factors, shows that (5.1) lies in `L^1(R)`.  Fourier inversion therefore gives
a bounded continuous density `f_m`; write `B_m=||f_m||_infinity<infinity`.

For any probability law `eta` and any law `nu` with density bounded by `B`,
approximating `1_(0,infinity)` above and below by ramps of width `1/L` gives

\[
 |\eta(0,\infty)-\nu(0,\infty)|
 \le 2\sqrt{B\,W_1(\eta,\nu)}.                              \tag{5.2}
\]

Apply (5.2) to `eta=mu_{m,U}` and `nu=nu_m`, then use (2.1).  Since the
normalizing factor in `E_m` is positive, `E_m(e^u)>0` if and only if the
weighted race `R_{m,chi}(e^u)>0`.  This proves (2.2).

## 6. What is and is not uniform in the weight

The proof above is complete for each fixed `m>-1/2`.  It does **not** yet
justify a joint limit `m=m(U)`:

1. The manuscript's shifted explicit formula and prime-power separation are
   stated with `O_{q,m}` constants.  The proof shows integrability for each
   fixed `m`, but it does not provide an audited global dependence on `m`.
2. The elementary coefficient bound is explicit,
   `L_m<=2 sqrt(2 C(chi)) M`, so the Kronecker--Weyl part loses at most a
   factor linear in `M`.  This alone suggests the possible range
   `M=o((log U)^(1/(2A))/(log log U)^2)`, but that range is **not a theorem**
   until the explicit-formula and prime-power constants are uniformized.
3. The bounded-density constant `B_m` used for signs also varies with `m`.
   For Wasserstein convergence this is irrelevant; for a uniform sign result
   it must be controlled.
4. When `m` grows with `x`, the prime weight localizes near the endpoint in a
   short interval of relative width about `1/m`.  A genuinely strong joint
   theorem therefore meets the short-interval prime problem, rather than
   being a formal parameter-uniform version of the fixed-weight proof.

Uniformity on a fixed compact interval of weights should be obtainable by
redoing Lemmas `lem:trunc` and `lem:squares` with a locally uniform constant
ledger, and by using the first three Bessel factors uniformly.  It is not
claimed here because that ledger is absent from the current manuscript.

## 7. The no-go result under ordinary LI

The obstruction to an effective rate under GRH+LI is exactly
`mathcal D(T,H)` in (2.5).  Qualitative LI says every individual denominator
is nonzero, but gives no lower bound for it.  Quantitative equidistribution of
a torus flow necessarily depends on such small divisors: rationally
independent frequency vectors can have arbitrarily small integer linear
forms and hence arbitrarily slow discrepancy along selected time scales.

Consequences:

- The current assumptions GRH+LI prove the limiting density but do not imply
  any stated numerical rate by this method.
- A finite list of rigorously enclosed zeros is not a proof of global LI or
  ELI.  It can certify finitely many bounded-coefficient linear forms and be
  inserted in (2.5), but the number of vectors is `(2H+1)^N-1`.
- Taking `H=N`, as needed for the clean `N^(-1/2)` torus term, is
  computationally impossible for the present 500-plus-zero lists by direct
  enumeration.
- Neither Dirichlet simultaneous approximation nor the classical
  noneffective Kronecker theorem removes this obstruction; both fail to give
  a lower bound for all the small divisors appearing in (2.4).

Thus a theorem advertised as effective under GRH+LI alone would currently be
wrong.  The honest extra hypothesis is ELI (or an explicit finite collection
of certified lower bounds appearing in Proposition B).

## 8. Novelty and likely significance

BHU already prove the unweighted `1/2+i gamma` theorem in much greater
generality in the residue-class variable.  The result above is a rigorous
kernel-shift adaptation to the growing power weight, including the extra
prime-power terms.  A targeted arXiv search found no primary paper stating
this weighted version, but that is not a definitive priority search.

Realistic assessment:

- As an added theorem in the present paper, this is meaningful: it answers an
  explicitly identified open direction and connects the actual finite race
  to the random model with a quantitative metric.
- It is conditional on the substantially stronger and wholly unproved ELI
  hypothesis, not merely on GRH+LI.
- Because the main argument is a careful adaptation of BHU rather than a new
  equidistribution mechanism, the fixed-`m` theorem is not a prestige-journal
  flagship by itself.
- A genuinely stronger contribution would be one of: an audited theorem
  uniform in an unbounded weight range; a joint `m=m(x)` result reaching the
  short-interval transition; or a practical finite-zero theorem with
  non-enumerative, rigorously certified small-divisor bounds.

## 9. Primary sources

1. A. Bailleul, M. Hayani, T. Untrau, *A Wasserstein metric approach to
   generalized Skewes' numbers. I. Prime number races*, arXiv:2603.20093v2
   (2026), especially Theorem 3.4, Corollary 5.2(iii), Lemma 5.6,
   and Theorems 5.13 and 5.17:
   <https://arxiv.org/abs/2603.20093>.
2. Y. Lamzouri, *An effective Linear Independence conjecture for the zeros
   of the Riemann zeta function and applications*, arXiv:2311.04860v2,
   for the effective-LI heuristic that BHU extend to Dirichlet `L`-functions:
   <https://arxiv.org/abs/2311.04860>.
3. A. Akbary, N. Ng, M. Shahabi, *Limiting distributions of the classical
   error terms of prime number theory*, Q. J. Math. 65 (2014), 743--780,
   arXiv:1306.1657, for the qualitative limiting-distribution framework used
   by the manuscript: <https://arxiv.org/abs/1306.1657>.
4. A. Bailleul, *Explicit Kronecker--Weyl theorems and applications to prime
   number races*, Res. Number Theory 8 (2022), article 43,
   arXiv:2007.05763v3, for the subtorus formulation without LI:
   <https://arxiv.org/abs/2007.05763>.

## 10. Integration recommendation

Do not insert Theorem A into the main manuscript until two independent
checks are completed:

1. have an independent analytic-number-theory referee check the shifted
   high-zero expansion and the five-range derivation of (3.6); and
2. rewrite the fixed-`m` `O_{q,m}` constants in the manuscript's shifted
   explicit formula as an explicit lemma, so the word *effective* has a
   documented constant dependency rather than only an in-principle meaning.

After those checks, the safest manuscript statement is the fixed-`m`
Theorem A plus Proposition B.  Do not currently claim uniformity in `m` or a
new unconditional/GRH+LI rate.
