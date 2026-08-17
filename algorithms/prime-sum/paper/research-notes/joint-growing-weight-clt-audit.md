# Independent adversarial audit of the moving-weight CLT candidate

Date: 17 August 2026.

Scope: `joint-growing-weight-clt.md`, checked from the definitions through the
sign consequence. This audit does not promote the candidate to a theorem and
does not modify the long manuscript.

## Verdict

The proposed theorem is **mathematically credible but not yet proved in the
repository**. I found no first-principles contradiction in the claimed range

\[
M\to\infty,\qquad \log M=o(\log U),
\]

under the stated all-order QLI hypothesis. The normalization, cutoff
arithmetic, moment comparison, model CLT, and sign transfer all close. The
large-zero argument also appears to close after restoring the diagonal that is
missing from the proof of Leung's Lemma 10.2, but the repository currently has
only a proof sketch of that repair. Consequently:

- **fatal for submission now:** the uniform high-zero lemma and the uniform
  large-`M` explicit formula are not written as complete lemmata with all
  dyadic and endpoint details;
- **serious but routine:** the passage from smooth time weights to the sharp
  interval and the `W_1` upgrade need explicit measure-normalization and
  uniform-integrability arguments;
- **not fatal:** the remaining probabilistic and moment steps can be completed
  with standard, correctly scaled estimates;
- **novelty warning:** the result is an exponential-Mellin-kernel analogue of
  Leung's Theorem 10.1, not a wholly new CLT mechanism. A paper based only on
  this specialization is likely publishable in a specialist venue if the two
  missing lemmata are completed, but it is not presently a prestige-journal
  flagship.

## 1. Statement and hypotheses

The theorem must state QLI for the multiset of indexed positive ordinates of
the single fixed `L(s,chi)`. With multiplicities retained, indexed LI implies
simplicity because two copies of an ordinate would give the forbidden relation
`gamma_i-gamma_j=0`. QLI must be stated separately: its exclusion of exact
zero does not imply LI.

Leung's actual formulation is Conjecture 10.1 of arXiv:2401.04000v4: for every
fixed `k>=2`, some `c_k>k` makes the number of nonzero signed sums of size at
most `T^{-c_k}` be `o_k(N(T)^{k/2})`. Replacing the little-oh by a
nondecreasing `g_k(T)->infinity`, with `g_k(T)<=log T`, is legitimate. One
constructs a monotone minorant from the little-oh estimate and truncates it by
`log T`. The constants and functions are allowed to depend on `k` and the
fixed character.

The hypotheses are extremely strong and unproved. The result must always be
advertised as conditional on GRH + NCZ + LI + all-order QLI, not as a GRH
theorem.

Primary-source check: Leung, Conjecture 10.1 and Theorem 10.1,
<https://arxiv.org/html/2401.04000v4#S10>.

## 2. Normalization and variance

Writing `M=m+1/2`, partial summation of the zero term gives

\[
c_M(\gamma)=\frac{2M}{M+i\gamma}.
\]

The signed-zero trigonometric sum has variance

\[
\sum_{\gamma\ne0}|c_M(\gamma)|^2
=8M^2\sum_{\gamma>0}\frac1{M^2+\gamma^2}=\sigma_M^2.
\]

This agrees with the independent-phase model, since
`Var(Re(aU))=|a|^2/2` and its positive-zero coefficient is
`a=4M/(M+i gamma)`. The completed-function identity in the manuscript gives

\[
\sigma_M^2=4M\frac{\xi'}{\xi}(M+1/2,\chi)
=2M\log\frac{qM}{2\pi}+O_q(1).
\]

Thus `max |c_M|^2/sigma_M^2 << 1/(M log M)`. These factors are consistent;
no missing factor of two was found.

## 3. Uniform explicit formula

The proposed dependence on `M` can be recovered from the manuscript's proof,
but it is not already a theorem there because that theorem fixes `m`.
Starting from the uniform truncated formula for `psi(x,chi)`, Stieltjes partial
summation gives, for `m>=0`,

\[
\psi_m(x)=-\sum_{|\gamma|\le Z}\frac{x^{m+\rho}}{m+\rho}
+O_q\left(\frac{x^{m+1}\log^2(xZ)}Z+x^m\log x+m2^m\right).
\]

The three dependencies have independent origins: the integrated truncation
error costs `m/(m+1)<=1`; the floor integral is at most `x^m log x`; and the
lower endpoint of each zero term sums absolutely to `O_q(m2^m)`.

For prime squares, splitting the PNT-error integral at `sqrt(y)` gives

\[
\sum_{p\le y}p^{2m}\log p
=\frac{y^{2M}}{2M}
+O\left(y^{2M}e^{-c\sqrt{\log y}}+y^M+M2^{2M}\right).
\]

For powers `k>=3`, Chebyshev's bound gives the uniform estimate
`O(x^{m+1/3} log x)`. After multiplication by `2M x^{-M}`, these reproduce
the six error types in (4.5), and all are `o(sigma_M)` when
`log M=o(log U)`.

Two details must be corrected in the final proof:

1. the smooth weight later used is supported on a fixed enlargement such as
   `[U/2,5U/2]`, whereas (4.5) is stated only on `[U,2U]`; the same calculation
   works with altered exponential constants and `Z=e^{3U}`;
2. primes dividing fixed `q` contribute a term bounded after normalization by
   `O_q(M exp(-M(U-C_q)))`, which should be displayed rather than hidden.

Classification: **repairable but currently incomplete**.

## 4. Finite cutoff and all fixed moments

Let `T=Mh`. A single diagonal function `h(U)->infinity` can be selected so
slowly that, for every fixed `k`,

\[
\log h=o(\log M),\qquad
\frac{h^{k/2}}{g_k(Mh)}\to0,\qquad
T\le U^{1/(2c_k)}
\]

eventually. One explicit construction is by stages: at stage `n`, constrain
`h` by the minimum of fixed fractional powers of
`M,g_2(M),...,g_n(M),U^{1/c_2},...,U^{1/c_n}` and let the stage increase only
after this minimum exceeds `n`. Monotonicity of each `g_k` transfers the
bound from `M` to `Mh`.

The zero tail satisfies

\[
\sigma_M^2-V_{M,T}\ll_q M^2\frac{\log(qT)}T,
\qquad
\frac{\sigma_M^2-V_{M,T}}{\sigma_M^2}
\ll_q\frac1h\frac{\log(qT)}{\log(qM)}=o(1).
\]

For the `k`th moment:

- LI makes every exact signed relation balanced at each distinct ordinate;
- the distinct pairings yield the Gaussian moment;
- collisions are relatively
  `O_k(sum |c|^4/V^2)=O_k(max|c|^2/V)=O_k((M log M)^{-1})`;
- QLI makes the normalized near-relation contribution

\[
\ll_{k,q}\frac1{g_k(T)}
\left(\frac{T\log(qT)}{M\log(qM)}\right)^{k/2}
=o_k(1);
\]

- for far relations, the coefficient `ell^1` norm is
  `O_q(M(log(qT))^2)`, while `U T^{-c_k}=U^{1-o(1)}`; Schwartz decay
  defeats every fixed moment.

This is the same architecture as Leung's Proposition 10.1, with `1/M` in the
role of the shrinking interval parameter `delta`. The exponents and cutoff
conditions in the candidate note are consistent.

Classification: **valid architecture; full collision combinatorics still must
be written**.

## 5. High-zero mean square

This is the decisive step. Let `Y_0=U^eta`, where `0<eta<1/c_2`, and first
split the zero sum itself at `Y_0`; the inequality
`|S_medium+S_high|^2<=2|S_medium|^2+2|S_high|^2` removes cross terms between
the two ranges.

For the medium range `T<|gamma|<=Y_0`, dyadically group pairs by the larger
ordinate `Y`. Since `T/M=h->infinity`, one has
`|c_M(gamma)|<<M/|gamma|` throughout this range.

- The diagonal is

\[
\sum_{|\gamma|>T}|c_M(\gamma)|^2
\ll_q M^2\frac{\log(qT)}T.
\]

- If `0<|gamma-lambda|<=(2Y)^{-c_2}`, the ordinates are comparable.
  QLI counts `O_q(Y log(qY)/g_2(Y))` such pairs in the block, so summing
  dyadically gives

\[
O_q\left(M^2\frac{\log(qT)}{Tg_2(T)}\right).
\]

- Every remaining medium pair has separation at least `Y_0^{-c_2}`. Its
  total is bounded by

\[
C_A(UY_0^{-c_2})^{-A}
\left(\sum_{T<|\gamma|\le Y_0}|c_M(\gamma)|\right)^2,
\]

  and the `ell^1` sum is `O_q(M(log(qY_0))^2)`. This is negligible for large
  fixed `A`, since `eta c_2<1` and `M=U^{o(1)}`.

For the high range `|gamma|>Y_0`, group ordinates into unit intervals.
The local zero count is `O_q(log(q(n+2)))`, and hence the contribution of the
same and neighboring unit intervals is

\[
O_q\left(M^2\sum_{n\ge Y_0}\frac{\log^2(qn)}{n^2}\right)
=O_q\left(M^2\frac{\log^2(qY_0)}{Y_0}\right).
\]

Non-neighboring intervals are negligible by the rapid decay of `hat W`; with
the actual truncation at `e^{3U}`, their crude `ell^1` loss is only polynomial
in `U`, which an arbitrarily high Schwartz exponent absorbs. Opposite-sign
ordinates are even easier because their frequency difference is the sum of
their absolute values.

Dividing these estimates by `sigma_M^2 asymp M log M` gives `o(1)`. Thus the
claimed lemma is consistent. A submission proof still needs to write the
signed-ordinate, adjacent-block, and upper-truncation sums explicitly.

### Source discrepancy

The original candidate note called the relevant result "Leung's Lemma 9.3";
that reference has now been corrected. In
arXiv:2401.04000v4 it is **Lemma 10.2**. Its displayed bound is

\[
\mathbb E^W |E-E^{(T)}|^2
\ll \frac{(\log T)^2}{TU}+U^3e^{-U/2}.
\]

The proof's close-pair sum includes `gamma_1=gamma_2`, for which
`hat W(0)=1`; the ensuing continuous double-integral estimate does not include
this discrete diagonal. The natural upper bound for that diagonal is
`O(log T/T)`, without a factor `1/U`. Bailleul--Hayani--Untrau's independent
high-zero estimate retains the diagonal through a term of size
`Y(log T)^2/T` before division by the averaging length. Therefore Leung's
displayed Lemma 10.2 should not be imported as written. The repaired argument
above does not require that stronger bound.

Primary-source checks:

- Leung, Lemma 10.2 and its proof:
  <https://arxiv.org/html/2401.04000v4#S10>.
- Bailleul--Hayani--Untrau, Corollary 5.2(iii) and Lemma 5.6:
  <https://arxiv.org/html/2603.20093v2#S5.SS1> and
  <https://arxiv.org/html/2603.20093v2#S5.SS2>.

Classification: **the current note has a fatal proof-writing gap, but the
proposed repair is quantitatively viable**.

## 6. Weak convergence, `W_1`, and the sharp window

Moment convergence for the low-zero sum, the normalized `L^2` tail estimate,
and the uniform explicit-formula error imply weak convergence for each fixed
smooth time density. To transfer to uniform measure on `[U,2U]`, choose
smooth nonnegative `W_-` and `W_+` satisfying

\[
W_-\le 1_{[1,2]}\le W_+,
\qquad \int(W_+-W_-)\le\varepsilon.
\]

The moment proof applies to either weight after dividing by its total mass.
Sandwich probabilities of continuity intervals, take `U->infinity`, and then
`epsilon->0`. This proves weak convergence for the sharp window.

For `W_1`, weak convergence alone is insufficient. Here the second-moment
calculation gives a uniform `L^2` bound for the normalized low-zero sum, the
high-zero lemma is `o(1)` in normalized `L^2`, and the explicit remainder is
uniformly `o(1)`. A smooth majorant also gives this bound for the sharp
window. Hence the absolute values are uniformly integrable, their first
moments converge, and the standard characterization of `W_1` convergence
applies.

Classification: **correct but underexplained in the candidate note**.

## 7. Independent-phase model

For

\[
Y_\gamma=\Re\left(\frac{4M}{M+i\gamma}U_\gamma\right),
\]

the variables are independent, centered, and have total variance
`sigma_M^2`. A Wasserstein Berry--Esseen/Stein bound gives

\[
d_{W_1}\left(\frac{\sum Y_\gamma}{\sigma_M},N(0,1)\right)
\ll\sigma_M^{-3}\sum_\gamma \mathbb E|Y_\gamma|^3.
\]

Since `E|Re(aU)|^3` is an absolute constant times `|a|^3`, zero counting and
partial summation give

\[
\sum_{\gamma>0}\frac{M^3}{(M^2+\gamma^2)^{3/2}}
\ll_q M\log(qM).
\]

The resulting error is `O_q((M log M)^{-1/2})`. Applying the finite-sum
bound and passing to the `L^2` limit justifies the infinite series. The factor
and order in (7.1) are correct.

Classification: **valid**.

## 8. Sign transfer

The normalizing factor in `E_M(e^u)` is positive, so `E_M(e^u)>0` exactly
when the original race is positive. Also

\[
E_M>0\iff Z_U>-1/\sigma_M,
\]

and `sigma_M->infinity`. If `Z_U` converges weakly to a distribution
continuous at zero, moving-threshold probabilities at
`-1/sigma_M->0` converge to the corresponding probability at zero. Thus the
limit `1/2` follows. No Berry--Esseen rate is needed. Conversely, the note is
right that this does not prove the first bias asymptotic of order
`1/sigma_M`.

Classification: **valid**.

## 9. Manuscript-readiness and value

Current proof status: **candidate, not manuscript-ready**.

The minimum promotion gate is:

1. turn Sections 3 and 5 of this audit into formal lemmata with complete
   proofs and exact quantifiers;
2. write the diagonal construction of `h(U)`;
3. write the exact-pairing collision argument;
4. give the sharp-window and `W_1` passage in full;
5. obtain an external analytic-number-theory audit, especially before
   publicly asserting an omission in Leung's to-appear paper.

If those gates close, the theorem is real and useful. It solves one focused
joint-limit question for the actual prime race. It does not by itself justify
"groundbreaking" or a 9.5/10 assessment: Leung's Theorem 10.1 already proves
the corresponding shrinking-short-interval CLT with the same all-order QLI
moment engine. The strongest paper design would formulate and prove a genuine
class of shrinking Mellin kernels, state checkable kernel hypotheses, recover
both Leung-type compact-window kernels and the present one-sided exponential
kernel, and make the corrected diagonal-aware high-zero theorem the central
technical contribution.
