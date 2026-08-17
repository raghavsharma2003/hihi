# All-order joint dissolution: an explicit Bell-polynomial expansion

Status: focused research note, 17 August 2026. This note does **not** modify
the frozen manuscript. It tests whether the manuscript's joint uniform
third-order theorem can be upgraded to a full fixed-order asymptotic
expansion, gives a proof from the existing Bessel-product machinery, and
assesses the result against Fiorilli--Martin.

## 1. Verdict

The upgrade is feasible. No new zero-density theorem is needed.

For each fixed integer `K >= 0`, the present hypotheses and the present
global Bessel-product tail lemma imply a joint `(q,m)`-uniform expansion

\[
 \delta_\chi(m)-\frac12
 =G\sum_{\ell=0}^{K}\frac{A_\ell(c_2,\ldots,c_{\ell+1})}
                              {\sigma^{2\ell}}
  +O_{K,\delta_0}\!\left(G\sigma^{-2K-2}\right),          \tag{1.1}
\]

uniformly over every real primitive character in hypothesis (H) and every
`M=m+1/2 >= delta_0 > 0`. Here

\[
 G=(2\pi\sigma^2)^{-1/2},\qquad
 c_r=\frac{\beta_r S_{2r}}{\sigma^2},                    \tag{1.2}
\]

`beta_r` is the positive coefficient of `z^(2r)` in `-log J_0(z)`, and
`A_ell` is an explicit complete-Bell-polynomial expression given below.
One may take

\[
 C_{K}(\delta_0)\le C_K\delta_0^{-(2K+4)}.               \tag{1.3}
\]

The cases `K=0,1,2` are exactly parts (i), (ii), and (iii) of the current
joint dissolution theorem. Thus this is a genuine all-order completion, not
a different approximation scheme.

The honest novelty verdict is less exciting. Fiorilli--Martin already prove
an arbitrary-order expansion for classical pairwise prime races in the
modulus aspect. The new content here would be simultaneous conductor and
growing-weight uniformity for the one-character weighted aggregate race,
together with an especially transparent cumulant/Bell coefficient formula.
That is publishable supporting mathematics, but by itself it is unlikely to
be the single high-value flagship result sought for a short paper. It is best
used as a component of a stronger theorem about the **actual finite-`x`
race**, a moving weight, or a general Mellin-kernel universality principle.

## 2. Exact notation

Retain hypothesis (H) and all notation from the joint dissolution section of
the manuscript. Thus `chi` is a real primitive character modulo `q >= 3`,
GRH holds for `L(s,chi)`, `L(1/2,chi) != 0`, and

\[
 b_\gamma:=2a_\gamma(m)=\frac{4M}{\sqrt{M^2+\gamma^2}},
 \qquad 0<b_\gamma\le4.                                  \tag{2.1}
\]

Put

\[
 Y_{m,\chi}=\sum_{\gamma>0}b_\gamma\cos\theta_\gamma,
 \qquad X_{m,\chi}=1+Y_{m,\chi},                         \tag{2.2}
\]

where the phases are independent and uniform, and define

\[
 S_{2r}=\sum_{\gamma>0}b_\gamma^{2r},\qquad
 \sigma^2=\frac12S_2.                                    \tag{2.3}
\]

The characteristic function of `Y` is

\[
 \Phi(t)=\prod_{\gamma>0}J_0(b_\gamma t).               \tag{2.4}
\]

Let `j_(0,n)` be the positive zeros of `J_0`. The canonical product for
`J_0` gives, for `|z|<j_(0,1)`,

\[
 -\log J_0(z)=\sum_{r\ge1}\beta_rz^{2r},\qquad
 \beta_r=\frac1r\sum_{n\ge1}j_{0,n}^{-2r}>0.            \tag{2.5}
\]

In particular

\[
 \beta_1=\frac14,\quad \beta_2=\frac1{64},\quad
 \beta_3=\frac1{576},                                   \tag{2.6}
\]

which recovers every coefficient used in the current third-order proof.
Formula (2.5) follows directly from the standard Bessel product; see DLMF
10.21.15 and Watson, Sections 15.4--15.41.

The even cumulants of `Y` are therefore

\[
 \kappa_{2r}(Y)=(-1)^{r+1}(2r)!\,\beta_rS_{2r},
 \qquad \kappa_{2r+1}(Y)=0,                              \tag{2.7}
\]

and `kappa_2=sigma^2`. It is convenient to normalize the higher cumulants
by

\[
 c_r:=\frac{\beta_rS_{2r}}{\sigma^2}
 =\frac{(-1)^{r+1}\kappa_{2r}(Y)}{(2r)!\,\sigma^2}
 \qquad(r\ge2).                                          \tag{2.8}
\]

These quantities are bounded uniformly in both parameters. Indeed (2.1)
implies

\[
 S_{2r}\le4^{2r-2}S_2=2\cdot4^{2r-2}\sigma^2,
 \qquad 0<c_r\le2\beta_r4^{2r-2}.                       \tag{2.9}
\]

This elementary inequality is the whole reason arbitrary fixed order can be
made joint-uniform.

## 3. The coefficient polynomials

Let `B_n(x_1,...,x_n)` denote the complete exponential Bell polynomial,
normalized by

\[
 \exp\!\left(\sum_{s\ge1}x_s\frac{z^s}{s!}\right)
 =\sum_{n\ge0}B_n(x_1,\ldots,x_n)\frac{z^n}{n!}.          \tag{3.1}
\]

Let `Z` be standard normal. For `s >= 1`, set

\[
 x_s(Z):=-s!\,c_{s+1}Z^{2s+2}.                           \tag{3.2}
\]

Define `A_0=1`, and for `ell >= 1` define

\[
 A_\ell(c_2,\ldots,c_{\ell+1})
 :=\sum_{j=0}^{\ell}\frac{(-1)^j}{(2j+1)!(\ell-j)!}
 \mathbb E\!\left[
 Z^{2j}B_{\ell-j}\bigl(x_1(Z),\ldots,x_{\ell-j}(Z)\bigr)
 \right].                                                \tag{3.3}
\]

Equivalently, without Bell notation,

\[
 A_\ell=
 \sum_{\substack{j,i_2,\ldots,i_{\ell+1}\ge0\\
 j+\sum_{r=2}^{\ell+1}(r-1)i_r=\ell}}
 \frac{(-1)^{j+\sum i_r}
 \bigl(2(j+\sum_{r=2}^{\ell+1}r i_r)-1\bigr)!!}
 {(2j+1)!\prod_{r=2}^{\ell+1}i_r!}
 \prod_{r=2}^{\ell+1}c_r^{i_r}.                         \tag{3.4}
\]

The partition formula (3.4) is the most direct form for verification. It is
a finite sum over the partitions of the weighted degree `ell`; (3.3) is the
same formula packaged by the exponential formula.

The first four polynomials are

\[
\begin{aligned}
 A_0={}&1,\\
 A_1={}&-\frac16-3c_2,\\
 A_2={}&\frac1{40}+\frac52c_2-15c_3+\frac{105}{2}c_2^2,\\
 A_3={}&-\frac1{336}-\frac78c_2+\frac{35}{2}c_3
          -\frac{315}{4}c_2^2-105c_4
          +945c_2c_3-\frac{3465}{2}c_2^3.
                                                               \tag{3.5}
\end{aligned}
\]

Substituting `c_2=S_4/(64 sigma^2)` and
`c_3=S_6/(576 sigma^2)` into `A_1/sigma^2` and
`A_2/sigma^4` reproduces term-for-term the current theorem:

\[
 \frac{A_1}{\sigma^2}
 =-\frac1{6\sigma^2}-\frac{3S_4}{64\sigma^4},            \tag{3.6}
\]

and

\[
 \frac{A_2}{\sigma^4}
 =\frac1{40\sigma^4}+\frac{5S_4}{128\sigma^6}
  -\frac{5S_6}{192\sigma^6}
  +\frac{105S_4^2}{8192\sigma^8}.                       \tag{3.7}
\]

This is a useful nontrivial consistency check on all signs and
normalizations.

## 4. Candidate theorem

**Theorem (all-order joint uniform dissolution).** Fix an integer `K >= 0`
and `delta_0 in (0,1]`. There is an effectively computable constant
`C_K(delta_0)` such that, for every pair `(chi,m)` satisfying (H) and
`M=m+1/2 >= delta_0`,

\[
 \left|\delta_\chi(m)-\frac12
 -G\sum_{\ell=0}^{K}
       \frac{A_\ell(c_2,\ldots,c_{\ell+1})}{\sigma^{2\ell}}
 \right|
 \le C_K(\delta_0)\frac{G}{\sigma^{2K+2}}.               \tag{4.1}
\]

No lower bound on `sigma` is needed for the inequality. The coefficient
polynomials are uniformly bounded:

\[
 |A_\ell(c_2,\ldots,c_{\ell+1})|\le C_\ell              \tag{4.2}
\]

with an absolute effectively computable `C_ell`. One may take

\[
 C_K(\delta_0)\le C_K\delta_0^{-(2K+4)}.                 \tag{4.3}
\]

Consequently, as `q*max(M,1) -> infinity`, uniformly on
`M >= delta_0`, (4.1) is a full Poincare expansion in inverse powers of
`sigma^2`, hence in inverse powers of `max(M,1) log(q max(M,1))` at the
level of remainder size.

The phrase "at the level of remainder size" matters. The bounded
coefficients `c_r` still depend on `(q,m)`. Turning every `c_r` into a closed
series solely in `M` and `log(qM)` is a separate arithmetic expansion and is
not needed for the uniform probabilistic theorem.

## 5. Proof from first principles

### 5.1 Inversion and rescaling

The global tail lemma in the current manuscript gives `Phi in L^1`, so
Gil--Pelaez inversion yields

\[
 \delta_\chi(m)-\frac12
 =\frac1\pi\int_0^\infty\Phi(t)\frac{\sin t}{t}\,dt.     \tag{5.1}
\]

For `0 <= t <= 1/8`, all `|b_gamma t| <= 1/2`, and (2.5) gives the exact
factorization

\[
 \Phi(t)=\exp\!\left(-\frac{\sigma^2t^2}{2}-H(t)\right),
 \qquad
 H(t)=\sum_{r\ge2}\beta_rS_{2r}t^{2r}\ge0.              \tag{5.2}
\]

After `u=sigma*t`, the formal integrand divided by the Gaussian is

\[
 \frac{\sin(u/\sigma)}{u/\sigma}
 \exp\!\left(-\sum_{s\ge1}
 c_{s+1}u^{2s+2}\sigma^{-2s}\right).                    \tag{5.3}
\]

Expanding (5.3) by weighted degree in `sigma^(-2)` gives (3.3)--(3.4).
Since the normalized half-Gaussian integral of an even function equals its
expectation under a standard normal, the monomial `u^(2n)` contributes
`(2n-1)!!`. This proves the coefficient formula formally. The next two
steps make the remainder uniform.

### 5.2 Uniform local remainder

Write

\[
 H_K(t)=\sum_{r=2}^{K+1}\beta_rS_{2r}t^{2r}.             \tag{5.4}
\]

Because the coefficients in (2.5) are positive and the series is analytic
on a disk strictly larger than `|z| <= 1/2`, its tail satisfies

\[
 0\le H(t)-H_K(t)
 \le C_KS_{2K+4}t^{2K+4}
 \le C_K\sigma^2t^{2K+4}.                               \tag{5.5}
\]

The last inequality is (2.9). Since `x -> exp(-x)` is 1-Lipschitz on the
positive half-line,

\[
 |e^{-H(t)}-e^{-H_K(t)}|
 \le C_K\sigma^2t^{2K+4}.                               \tag{5.6}
\]

Also, Taylor's theorem on the positive half-line gives

\[
 \left|e^{-H_K}-\sum_{n=0}^{K}\frac{(-H_K)^n}{n!}\right|
 \le\frac{H_K^{K+1}}{(K+1)!}.                           \tag{5.7}
\]

On `t <= 1/8`, (2.9) and analyticity give

\[
 0\le H_K(t)\le C_K\sigma^2t^4.                         \tag{5.8}
\]

Thus the integrated error in (5.7), relative to `G`, is at most a constant
times

\[
 \sigma^{2K+2}\,
 \mathbb E\left[(Z/\sigma)^{4K+4}\right]
 \ll_K\sigma^{-2K-2}.                                   \tag{5.9}
\]

When the finite powers in (5.7) are expanded, a monomial
`prod_(s=1)^K (beta_(s+1) S_(2s+2) t^(2s+2))^(i_s)` has weighted degree

\[
 w=\sum_{s=1}^{K}s i_s.                                  \tag{5.10}
\]

If `n=sum i_s`, its coefficient is `O_K(sigma^(2n))`, while its Gaussian
moment is `O_K(sigma^(-2(w+n)))`; hence its integrated size relative to `G`
is `O_K(sigma^(-2w))`. All discarded monomials have `w >= K+1` and
therefore contribute `O_K(sigma^(-2K-2))` when `sigma >= 1`.

Finally,

\[
 \left|\frac{\sin t}{t}-\sum_{j=0}^{K}
 \frac{(-1)^jt^{2j}}{(2j+1)!}\right|
 \le\frac{t^{2K+2}}{(2K+3)!}.                            \tag{5.11}
\]

Combining (5.5)--(5.11) under the Gaussian factor proves

\[
 \frac1\pi\int_0^{1/8}\Phi(t)\frac{\sin t}{t}\,dt
 =G\sum_{\ell=0}^{K}\frac{A_\ell}{\sigma^{2\ell}}
 +O_K(G\sigma^{-2K-2})                                  \tag{5.12}
\]

for `sigma >= 1`, apart from extending finitely many Gaussian moments from
`[0,1/8]` to `[0,infinity)`. Those extension errors are
`O_K(exp(-c sigma^2))` times a polynomial in `sigma`, and hence are absorbed
in the right side of (5.12).

### 5.3 The global Bessel-product tail

The current uniform superexponential-tail lemma already proves

\[
 \int_{1/8}^{\infty}|\Phi(t)|\frac{|\sin t|}{t}\,dt
 \le C\delta_0^{-1}e^{-c\delta_0^2\sigma^2}.             \tag{5.13}
\]

No strengthening is required as `K` grows. For `sigma >= 1`,

\[
 \delta_0^{-1}e^{-c\delta_0^2\sigma^2}
 \le C_K\delta_0^{-(2K+4)}
       \sigma^{-(2K+3)}
 \asymp C_K\delta_0^{-(2K+4)}G\sigma^{-2K-2}.           \tag{5.14}
\]

This proves both (4.1) and the stated `delta_0` dependence for `sigma >= 1`.
For `0 < sigma <= 1`, use `|delta-1/2| <= 1/2`, (2.9), and the finite
coefficient formula: the right side of (4.1) is of order
`sigma^(-2K-3)` and dominates every retained term. Thus the same inequality,
after enlarging `C_K`, holds for all positive `sigma`.

This completes the proof.

## 6. Exact conditions behind the argument

The proof separates cleanly into local and global inputs.

### Local all-order expansion

For a general triangular family of Bessel products

\[
 \Phi_n(t)=\prod_\nu J_0(b_{n,\nu}t),                    \tag{6.1}
\]

the local expansion through every fixed order needs only:

1. `sum b_(n,nu)^2 < infinity` and
   `sigma_n^2=(1/2) sum b_(n,nu)^2`;
2. a uniform amplitude bound `sup_(n,nu)|b_(n,nu)| <= B`;
3. a fixed local interval `|t| <= t_0 < j_(0,1)/B`.

Then

\[
 S_{2r,n}\le 2B^{2r-2}\sigma_n^2,                       \tag{6.2}
\]

and the complete local proof above is uniform. This is the analytic core of
an all-order Edgeworth expansion for bounded rotational summands.

### Global inversion and tail

Local cumulant control alone is not enough for a distribution-function
expansion. A lattice-like family can retain large Fourier mass away from the
origin. A sufficient global condition is a uniform Cramer window:

- at least `N_n >= c sigma_n^2` amplitudes obey
  `b_0 <= |b_(n,nu)| <= B`, with fixed `b_0,c>0`;
- at least three of those amplitudes are retained when the large-argument
  envelope `|J_0(x)| <= C|x|^(-1/2)` is applied.

Indeed, on a bounded interval away from zero,

\[
 \sup_{x\ge b_0t_0}|J_0(x)|=\rho<1,                     \tag{6.3}
\]

so the window contributes `rho^(N_n)`; at infinity, three retained Bessel
factors make the product integrable, while the remaining factors preserve
the exponential window gain. The manuscript uses seven retained factors,
which is more than sufficient and gives (5.13).

For the weighted prime-race family, the uniform Riemann--von Mangoldt window
provides

\[
 N_0\gg\max(M,1)\log(q\max(M,1))\gg\sigma^2,             \tag{6.4}
\]

and every amplitude in that window is bounded below by a constant times
`min(M,1) >= delta_0`. Thus the global condition is already proved in the
manuscript. There is no hidden arbitrary-order obstruction.

## 7. Computing the coefficients without listing zeros

The higher moment sums have a simple exact differential recurrence. Let

\[
 \Xi(z)=\xi(1/2+z,\chi),\qquad
 F_r(M)=\sum_{\gamma>0}(M^2+\gamma^2)^{-r}.              \tag{7.1}
\]

The Hadamard product gives

\[
 F_1(M)=\frac{(\log\Xi)'(M)}{2M},\qquad
 F_{r+1}(M)=-\frac{F_r'(M)}{2rM}.                        \tag{7.2}
\]

Hence

\[
 S_{2r}=(4M)^{2r}F_r(M).                                 \tag{7.3}
\]

Equations (7.2)--(7.3), followed by the finite partition sum (3.4), are an
exact coefficient generator at every fixed order. At `r=2,3` they reproduce
the manuscript's displayed formulas for `S_4` and `S_6`. This recurrence is
also well suited to formal verification: it reduces coefficient generation
to differentiation, finite sums over integer partitions, and Gaussian
double-factorial moments.

What it does **not** provide automatically is a numerically sharp error
constant in (4.1). Making `C_K(delta_0)` practical would require retaining
explicit constants in the analytic Taylor tail and in the global zero
window; the theorem is effective in principle but the current window
constants are intentionally wasteful.

## 8. Comparison with Fiorilli--Martin

Fiorilli--Martin, *J. reine angew. Math.* 676 (2013), Theorem 1, already
prove for every fixed `K` an expansion of the form

\[
 \delta(q;a,b)=\frac12+
 \frac{\rho(q)}{\sqrt{2\pi V(q;a,b)}}
 \sum_{\ell=0}^{K}\frac1{V(q;a,b)^\ell}
 \sum_{j=0}^{\ell}\rho(q)^{2j}s_{q;a,b}(\ell,j)
 +O_K\!\left(\frac{\rho(q)^{2K+3}}
 {V(q;a,b)^{K+3/2}}\right).                              \tag{8.1}
\]

Their coefficients are finite partition sums built from the coefficients of
`log J_0`, and are uniformly bounded. Their paper also sketches the aggregate
quadratic-nonresidue versus quadratic-residue race and proves its leading
formula, but does not state the present weighted, joint-parameter theorem.

The relationship is therefore precise:

- **Already known mechanism:** arbitrary-order Bessel/cumulant expansion,
  partition coefficients, Gaussian moment integration, and modulus-aspect
  uniformity are all present in Fiorilli--Martin.
- **New theorem if written carefully:** one estimate valid simultaneously
  for all real primitive characters and all `M >= delta_0`, including the
  growing-weight interior; a uniform Cramer window at height comparable to
  `max(M,1)`; and coefficient functions generated from the weight-dependent
  moments `S_(2r)(m,chi)`.
- **Not new:** the existence of an all-order Edgeworth-type series as an
  abstract phenomenon.

Calling (4.1) "the first all-order prime-race expansion" would be false.
Calling it "an all-order joint conductor--weight expansion for the weighted
one-character race" appears defensible, subject to a fresh literature check
and expert review.

## 9. Publishability assessment

On its own, (4.1) is a rigorous and attractive completion of the current
theorem, but it is not a breakthrough-sized single result.

Reasons it is useful:

- it replaces an arbitrary stopping point at third order by a canonical full
  expansion;
- its coefficient formula is exact, finite, and independently checkable;
- its uniformity genuinely joins two regimes, `q -> infinity` and
  `M -> infinity`;
- it provides a compact theorem around which a shorter exposition can be
  organized.

Reasons it is not enough for a prestige flagship:

- the proof adds no new arithmetic input beyond the manuscript's existing
  uniform zero window;
- Fiorilli--Martin already supply the all-order blueprint in a closely
  related prime-race problem;
- for any fixed `K`, the extension is mostly disciplined Taylor bookkeeping;
- the expansion still concerns the limiting random model unless LI is used
  to transfer it to the limiting logarithmic density.

The highest-value way to use this result is one of the following:

1. prove a quantitative finite-`x` theorem whose limiting target is the full
   expansion (4.1);
2. prove the expansion uniformly for a genuinely moving weight in the actual
   race;
3. formulate and prove a general Mellin-kernel theorem, with power weights as
   one application and (4.1) as its universal coefficient calculus;
4. pair the theorem with a machine-checked coefficient generator and sharp,
   usable certified remainder bounds.

Options 1--3 would change the mathematical value. Option 4 would change the
verification and computational value, but probably not the journal tier by
itself.

## 10. Recommendation

Do not expand the frozen 66-page manuscript merely to insert another long
technical section. Preserve (4.1) as a proved candidate and use it in one of
two ways:

- as a concise theorem in a shorter, redesigned paper if a stronger
  finite-`x` or moving-weight result closes; or
- as an appendix/companion note showing that the third-order theorem is the
  beginning of a full joint expansion.

Before promoting it to a submitted theorem, obtain two independent checks:

1. a line-by-line audit of the weighted-degree remainder in Section 5.2;
2. a symbolic verification that (3.4) reproduces the manuscript through
   `K=2` and generates `A_3` as displayed.

The theorem is very likely correct. Its main risk is not mathematical
failure; it is overstating novelty.

## Primary references checked

- D. Fiorilli and G. Martin, *Inequities in the Shanks--Renyi prime number
  race: an asymptotic formula for the densities*, J. reine angew. Math. 676
  (2013), 121--212; arXiv:0912.4908. Theorem 1 and the derivation in Section
  3 give arbitrary-order partition/cumulant coefficients; Section 3.6 treats
  the aggregate quadratic race at leading order.
- NIST Digital Library of Mathematical Functions, Section 10.21(iii),
  equation 10.21.15: the canonical product for `J_nu`, specialized here to
  `J_0`.
- G. N. Watson, *A Treatise on the Theory of Bessel Functions*, 2nd ed.,
  Cambridge University Press, 1944, Sections 15.4--15.41.
- C. S. Withers and S. Nadarajah, *Charlier and Edgeworth expansions for
  distributions and densities in terms of Bell polynomials*, Probability and
  Mathematical Statistics 29 (2009), 271--280. This is the direct statistical
  precedent for packaging cumulant expansions by complete Bell polynomials;
  the proof above is nevertheless specialized and proved directly for the
  Bessel product rather than imported from a generic Edgeworth theorem.
