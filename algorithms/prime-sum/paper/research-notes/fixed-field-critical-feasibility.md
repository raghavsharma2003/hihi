# Fixed-field hyperelliptic critical law: feasibility and obstruction ledger

Date: 2026-08-17

Status: internal research note.  This is a feasibility audit, not manuscript
text and not a theorem claim.

## 1. Question and verdict

Fix an odd prime power \(q\), let \(D\) be uniform among the monic squarefree
polynomials of degree \(d=2g+1\) over \(\mathbb F_q\), and scale the positive
Frobenius angles by

\[
 y_{D,j}=\frac{d\vartheta_{D,j}}{2\pi}.
\]

The desired fixed-field flagship would identify the \(g\to\infty\) law of the
critical weighted race at

\[
 m=-\frac12+\frac{\lambda}{d\log q},\qquad \lambda>0,
\]

with the symplectic hard-edge law already obtained in the iterated limit
\(q^n\to\infty\) first and \(g\to\infty\) second.

The conclusion of this audit is sharp:

1. **The reciprocal-square tail estimate is probably accessible now.**  It
   follows from the known fixed-\(q\) one-level density with restricted Fourier
   support and positive Beurling--Selberg majorants.  It is not the real
   obstruction.
2. **Full symplectic hard-edge convergence at fixed \(q\) is not accessible
   from the published trace, density, or mesoscopic theorems.**  It is the
   fixed-field microscopic Katz--Sarnak problem itself.
3. **Passing directly to the race functional does not evade the missing
   microscopic information at fixed \(\lambda\).**  The relevant Bessel
   multiplicative statistic has Fourier content at every multiple of the
   genus scale, whereas the rigorous density theorems see only bounded total
   Fourier support.
4. **The actual per-curve race density has a second independent obstruction:**
   density-one linear independence of the Frobenius angles is known in a
   large-field limit at fixed genus, not in the fixed-field large-genus limit.

Therefore a fixed-\(q\), fixed-\(\lambda\) theorem should not be advertised as
an ASAP extension of the present paper.  Proving it would be a major result,
but it would require a genuinely new microscopic or arithmetic-statistical
input, not a reassembly of current lemmas.

## 2. Exact fixed-field statistic

Put

\[
 a=e^{-\lambda/d}.
\]

The exact amplitude contributed by a positive Frobenius angle is

\[
 B_{g,\lambda}(\vartheta)
 =\frac{4(1-a)}{\sqrt{1-2a\cos\vartheta+a^2}}.
\tag{2.1}
\]

At \(\vartheta=2\pi y/d\), this converges locally uniformly to

\[
 b_\lambda(y)=\frac{4\lambda}
 {\sqrt{\lambda^2+(2\pi y)^2}}.
\tag{2.2}
\]

After the parity centers coalesce to \(1\), the independent-phase model has
conditional characteristic function

\[
 \Phi_{g,D}(t)
 =e^{it}\prod_{j=1}^g J_0\!\left(tB_{g,\lambda}
 (\vartheta_{D,j})\right).
\tag{2.3}
\]

When the conditional law has no atom at the threshold, its sign probability
can be recovered by the usual inversion formula

\[
 \delta_{g,D,\lambda}
 =\frac12+\frac1\pi\int_0^\infty
 \frac{\sin t}{t}\prod_{j=1}^g
 J_0\!\left(tB_{g,\lambda}(\vartheta_{D,j})\right)\,dt.
\tag{2.4}
\]

Thus even the **annealed** race law requires control of a local multiplicative
spectral statistic.  The distribution of the quenched quantity
\(\delta_{g,D,\lambda}\) requires more.

## 3. What is rigorously known at fixed field

### 3.1 One trace and products of traces

Rudnick computes the fixed-\(q\) mean of
\(\operatorname{tr}(\Theta_D^n)\) for powers nearly as large as \(4g\), with
the exceptional low-power arithmetic terms and the exceptional power
\(n=2g\) made explicit.  This yields one-level density for Fourier support
\((-2,2)\).

Roditty-Gershon proves agreement of products of high traces with Haar
\({\rm USp}(2g)\) in the range

\[
 \sum_j a_jk_j\leq 2g-1,
 \qquad \min_j k_j\gg\log_q g,
\tag{3.1}
\]

for fixed multiplicities \(a_j\).  This is powerful but is a
**total-frequency budget**, not arbitrary joint control of all genus-scale
traces.

Primary sources:

- Z. Rudnick, *Traces of high powers of the Frobenius class in the
  hyperelliptic ensemble*, Acta Arith. 143 (2010),
  [arXiv:0811.3649](https://arxiv.org/abs/0811.3649).
- E. Roditty-Gershon, *Statistics for products of traces of high powers of the
  Frobenius class of hyperelliptic curves*,
  [arXiv:1105.4476](https://arxiv.org/abs/1105.4476), Theorem 1.1.

### 3.2 All \(n\)-level densities, but only in a fixed Fourier window

Entin--Roditty-Gershon--Rudnick prove, for every fixed \(n\), the symplectic
\(n\)-level density at fixed \(q\) for test functions satisfying

\[
 \operatorname{supp}\widehat f
 \subset\left\{(u_1,\ldots,u_n):
 \sum_{j=1}^n|u_j|<2\right\}.
\tag{3.2}
\]

Their hyperelliptic estimate has error \(O_f(\log g/g)\), uniform in \(q\).
This is an all-\(n\) theorem, but (3.2) is not convergence-determining for a
microscopic point process.  For example, when \(n\) grows, a product test has
individual bandwidth below roughly \(2/n\).  A fixed bandwidth class cannot
approximate arbitrary compactly supported continuous tests to arbitrarily
small error.

Primary source: A. Entin, E. Roditty-Gershon and Z. Rudnick, *Low-lying zeros
of quadratic Dirichlet L-functions, hyper-elliptic curves and Random Matrix
Theory*, GAFA 23 (2013), [arXiv:1208.5962](https://arxiv.org/abs/1208.5962),
Theorem 1.2 and Corollary 1.3.

### 3.3 Mesoscopic statistics stop just before the needed scale

Faifman--Rudnick prove a Gaussian counting law for an interval of angular
length \(\beta\) when

\[
 g\beta\longrightarrow\infty.
\tag{3.3}
\]

They explicitly distinguish the unresolved microscopic regime
\(\beta\asymp 1/g\), where the limiting count is non-Gaussian.  The critical
race is precisely in this excluded regime: the first \(O(1)\) scaled angles
have \(O(1)\) amplitudes in (2.2).

This is also the order-of-limits boundary stated by Katz--Sarnak: their
large-field-then-large-genus low-zero law is equation (41), while the
fixed-field large-genus analogue is posed as equation (42), not proved.

Primary source: D. Faifman and Z. Rudnick, *Statistics of the zeros of zeta
functions in families of hyperelliptic curves over a finite field*, Compos.
Math. 146 (2010), [arXiv:0803.3534](https://arxiv.org/abs/0803.3534).

Original conjectural source: N. Katz and P. Sarnak, *Zeroes of zeta functions
and symmetry*, Bull. AMS 36 (1999),
[DOI 10.1090/S0273-0979-99-00766-1](https://doi.org/10.1090/S0273-0979-99-00766-1),
equations (41)--(42).

### 3.4 The apparent 2026 full-correlation formula is conjectural

The recent Andrade--Shamesaldeen formulas are derived from the Andrade--Keating
Ratios Conjecture.  They are useful predictions, but they do not provide a
rigorous fixed-field microscopic theorem and cannot be used in a
first-principles proof.

Primary source: J. Andrade and A. Shamesaldeen, *Correlations of zeros of a
family of L-functions in function fields with symplectic symmetry*,
[arXiv:2607.06022](https://arxiv.org/abs/2607.06022), especially Conjecture 1.1
and the statements explicitly conditional on it.

## 4. Why the direct characteristic-function route still needs microscopic data

Let

\[
 u_t(y)=J_0(t b_\lambda(y))-1.
\]

The annealed version of (2.3) has the factorial expansion

\[
 \mathbb E_D\prod_j(1+u_t(y_{D,j}))
 =\sum_{k\geq0}\frac1{k!}
 \mathbb E_D\sum_{j_1,\ldots,j_k}^{\ne}
 \prod_{r=1}^ku_t(y_{D,j_r}).
\tag{4.1}
\]

The function \(u_t(y)=O_{t,\lambda}(y^{-2})\), so (4.1) is exactly the right
Fredholm-type expansion.  But \(u_t\) is not band-limited.  Its Fourier
transform decays exponentially because the nearest complex singularities are
at distance proportional to \(\lambda\), but it is nonzero at arbitrarily high
frequencies.  Cutting each factor to bandwidth below \(2/k\) leaves a
nonzero error depending on \(t,\lambda,k\); that error does not disappear as
\(g\to\infty\).

The obstruction can already be seen in the quadratic coefficient.  From the
Poisson-kernel identity,

\[
 B_{g,\lambda}(\vartheta)^2
 =16\frac{1-a}{1+a}
 \left(1+2\sum_{n\geq1}a^n\cos(n\vartheta)\right),
 \qquad a=e^{-\lambda/d}.
\tag{4.2}
\]

The coefficient of the \(n\)-th angular mode is therefore of size

\[
 \frac{\lambda}{d}e^{-\lambda n/d}.
\tag{4.3}
\]

For fixed \(\lambda\), modes \(n=cd\) for every fixed \(c>0\) remain relevant.
A cutoff at \(n\leq Cd\) leaves a tail of natural size \(e^{-C\lambda}\), a
constant independent of \(g\).  To drive the error to zero one needs
\(C\to\infty\), while the existing trace theorems only give a fixed finite
multiple of \(g\), and product moments have the stricter total budget (3.1).

Taking logarithms does not repair this.  For small \(t\),

\[
 \log\prod_jJ_0(tB_j)
 =-\sum_{r\geq1}c_r t^{2r}\sum_jB_j^{2r}.
\tag{4.4}
\]

The local linear statistics \(\sum_jB_j^{2r}\) have nonvanishing fluctuations;
they do not concentrate to deterministic constants.  Their joint law, not
only their means, is needed.

This explains why the fixed-field direct method succeeds for global smooth
statistics such as \(\log\#J_C\), but not here.  In
Xiong--Zaharescu the trace expansion has coefficients \(q^{-n/2}/n\), so it
can be truncated far below the conductor with exponentially small error.  In
(4.3), the decay scale itself is \(d\).

Primary comparison: M. Xiong and A. Zaharescu, *Statistics of the Jacobians of
hyperelliptic curves over finite fields*, Math. Res. Lett. 19 (2012),
[arXiv:1007.4621](https://arxiv.org/abs/1007.4621), especially their tail bound
and Theorem 3.

## 5. Two hard consequences that expose the size of the target

### 5.1 Full hard-edge convergence would imply density-one central nonvanishing

If the fixed-\(q\) point measures converged to the symplectic hard-edge process,
then

\[
 \mathbb P_D\bigl(L(1/2,\chi_D)=0\bigr)\longrightarrow0.
\tag{5.1}
\]

Indeed, an exact central zero gives a point at \(y=0\).  For every
\(\varepsilon>0\), its probability is bounded by the probability of a point in
\([0,\varepsilon]\).  Point-process convergence sends the limsup to the
corresponding hard-edge probability, which tends to zero with \(\varepsilon\).

Current fixed-field results do not prove (5.1).  Bui--Florea prove more than
\(94.27\%\) nonvanishing.  Ellenberg--Li--Shusterman give a bound uniform in
genus which tends to zero when the field grows; their result deliberately does
not give density-one nonvanishing for each fixed \(q\) as \(g\to\infty\).

Primary sources:

- H. Bui and A. Florea, *Zeros of quadratic Dirichlet L-functions in the
  hyperelliptic ensemble*, Trans. AMS 370 (2018),
  [arXiv:1605.07092](https://arxiv.org/abs/1605.07092).
- J. Ellenberg, W. Li and M. Shusterman, *Nonvanishing of hyperelliptic zeta
  functions over finite fields*, Algebra & Number Theory 14 (2020),
  [arXiv:1901.08202](https://arxiv.org/abs/1901.08202), Theorem 1.2.

Thus the full point-process theorem would settle, as a corollary, a recognized
fixed-field nonvanishing problem not resolved by current methods.

### 5.2 The arithmetic race also needs fixed-field LI

For a single curve, independent uniform phases in (2.3) come from rational
independence of

\[
 \{\vartheta_{D,1},\ldots,\vartheta_{D,g},\pi\}.
\]

Kowalski's sieve and Cha's application give density-one independence when the
field extension grows at fixed genus.  They do not establish density-one LI
for a fixed field as the genus grows.  Spectral point-process convergence by
itself would not imply LI: discrete spectra supported on rationally dependent
angles can converge weakly to a continuous point process.

Primary sources:

- E. Kowalski, *The large sieve, monodromy and zeta functions of algebraic
  curves, II: independence of the zeros*, IMRN (2008),
  [arXiv:0807.2118](https://arxiv.org/abs/0807.2118).
- B. Cha, *The summatory function of the Moebius function in function fields*,
  Acta Arith. 179 (2017), [arXiv:1008.4711](https://arxiv.org/abs/1008.4711),
  Theorem 3.1.

One can avoid LI only by changing the target to an annealed model with
auxiliary independent phases.  That is a legitimate statistic, but it is not
the per-curve arithmetic race density.

## 6. Reciprocal-square uniform integrability is not the bottleneck

The needed tail statement is

\[
 \lim_{R\to\infty}\limsup_{g\to\infty}
 \mathbb E_D\sum_{y_{D,j}>R}\frac1{y_{D,j}^2}=0.
\tag{6.1}
\]

A candidate direct route uses only the fixed-\(q\) one-level trace formula.
Decompose
\([R,\infty)\) into dyadic intervals
\(I_k=[2^kR,2^{k+1}R]\).  For each \(I_k\), take a nonnegative
Beurling--Selberg majorant \(M_k\geq1_{I_k}\) with Fourier support in
\((-1,1)\) and

\[
 \int_{\mathbb R}M_k(x)\,dx\ll |I_k|+1.
\]

Then the positive band-limited function

\[
 M_R(x)=\sum_{k\geq0}(2^kR)^{-2}M_k(x)
\]

majorizes \(1_{x>R}x^{-2}\), has Fourier support inside \((-1,1)\), and

\[
 \int_{\mathbb R}M_R(x)\,dx\ll R^{-1}+R^{-2}.
\tag{6.2}
\]

There is one uniformity point which must not be hidden.  The published
asymptotic theorem is stated for a fixed test function, whereas the infinite
dyadic sum requires a bound uniform in the interval translate and length up to
the full scaled spectrum.  The explicit trace proof should yield

\[
 \mathbb E_D N_D([A,B])\ll (B-A)+1
 \tag{6.3}
\]

uniformly for \(0\leq A<B\leq d/2\), because translation only inserts
unit-modulus phases in the Fourier coefficients; however, (6.3) must be
extracted and checked from Rudnick's exact mean-trace estimates rather than
quoted from fixed-test convergence.  Once (6.3) is established, summing the
dyadic intervals proves (6.1) immediately.  Together with the elementary
amplitude bound

\[
 B_{g,\lambda}(2\pi y/d)\ll_\lambda y^{-1}
 \qquad (0<y\leq d/2),
\]

this yields the required \(\ell^2\)-tail control.

This uniform counting lemma appears substantially easier than microscopic
convergence, but it is a real integration gate, not a completed citation.  It
does not supply compact hard-edge convergence.

## 7. The smallest genuinely major fixed-field target

The right reduced target is not a vague claim of "using trace moments".  It is
the following precise multiplicative-statistic theorem:

> **Bessel-statistic target.**  For every fixed \(\lambda>0\) and every fixed
> \(t\in\mathbb R\), prove
> \[
> \lim_{g\to\infty}\mathbb E_D
> \prod_{j=1}^gJ_0(tB_{g,\lambda}(\vartheta_{D,j}))
> =\det\!\left(I+\bigl(J_0(tb_\lambda)-1\bigr)K_{\rm Sp}\right).
> \tag{7.1}
> \]

With locally uniform control in \(t\), (7.1) would prove convergence of the
**annealed independent-phase race law**.  It is strictly weaker than full
point-process convergence because it tests one special one-parameter family
of multiplicative functionals.  It is still a major new fixed-field theorem.

No published theorem found in this audit implies (7.1).  Plausible attack
routes are:

1. an arithmetic Fredholm expansion with new unrestricted estimates for the
   special product tests in (4.1);
2. a symplectic-character expansion of the multiplicative class function,
   followed by fixed-field bounds for the corresponding growing-weight local
   systems on the hyperelliptic moduli space;
3. a new trace-moment theorem whose total-frequency range grows beyond every
   fixed multiple of \(g\), with summable bounds strong enough to use (4.2).

Each route requires a new theorem.  The third makes the barrier especially
transparent: algebraic determination of high traces by the first \(2g\)
traces does not control the high-degree polynomials in those traces that occur
in the multiplicative statistic.

Even (7.1) does **not** prove the distribution over \(D\) of the quenched race
density.  That would require joint convergence of products of (7.1)-type
functionals, or a stronger process theorem, as well as an arithmetic
phase-equidistribution statement.

## 8. A feasible but lower-value regime

If \(\lambda=\lambda_g\to\infty\) while \(\lambda_g=o(g)\), the relevant
spectral window becomes mesoscopic and the omitted Fourier tail in (4.3)
shrinks rapidly.  Existing mesoscopic/trace methods may then prove a Gaussian
independent-phase law after variance normalization.  Formally,

\[
 \frac12\sum_j b_{\lambda_g}(y_{D,j})^2\sim 2\lambda_g,
 \qquad
 \frac{\max_j b_{\lambda_g}(y_{D,j})}
 {\sqrt{\sum_j b_{\lambda_g}(y_{D,j})^2}}\to0,
\]

so Lindeberg predicts a Gaussian and

\[
 \delta_{g,D,\lambda_g}
 =\frac12+\frac{1}{2\sqrt{\pi\lambda_g}}+o(\lambda_g^{-1/2})
\tag{8.1}
\]

for the independent-phase model, provided the variance concentration is
proved.  This is potentially publishable as a mesoscopic theorem, but it
deliberately leaves the non-Gaussian fixed-\(\lambda\) law and tends toward the
unbiased value \(1/2\).  It is not a substitute for the flagship target.

## 9. Prime-conductor subfamily: a useful refinement, not a solution

There is one natural fixed-field subfamily worth separating.  Restrict \(D\)
to monic irreducible polynomials of degree \(2g+1\).  Ellenberg--Li--Shusterman
show that, for irreducible conductor of degree not divisible by \(4\), the
central value is nonzero; their Frobenius-cycle criterion also gives simplicity
of all zeros in this odd prime-degree case.  Thus this subfamily removes the
central-vanishing and repeated-zero obstructions exactly, not statistically.

It does **not** presently remove either decisive barrier:

1. no rigorous full microscopic symplectic point-process theorem is known for
   the fixed-\(q\), degree-\(2g+1\) prime-conductor family;
2. simplicity of the angles is much weaker than rational linear independence
   of the angles with \(\pi\);
3. the available 2026 higher-correlation formulas for prime characters are
   again conditional on a Ratios Conjecture.

The prime-conductor analogue of (7.1) is nevertheless a sensible alternate
high-risk target.  It has the advantage that any failure can no longer be
blamed on exact central zeros.  A successful proof would still require new
prime-polynomial character-sum estimates at unrestricted microscopic Fourier
range.

## 10. Recommendation

- Preserve the iterated-limit arithmetic realization as the rigorous natural
  family theorem after its remaining proof-writing audit.
- Do not choose fixed-\(q\) hard-edge convergence as the "fast focused paper"
  unless the project is explicitly recast as a long-term attempt on the
  Katz--Sarnak microscopic conjecture.
- If a high-risk fixed-field project is desired, target (7.1), not the full
  process.  It is the minimal theorem that would give a new annealed critical
  race law, and its exact missing estimates are now identifiable.
- For an ASAP paper, the fixed-field route is the wrong risk profile.  The
  available \(\lambda\to\infty\) regime is more feasible but less
  groundbreaking; it should be pursued only if a clean quantitative theorem
  emerges, not to manufacture an inflated claim.

The honest bottom line is that the fixed-field fixed-critical law is valuable
precisely because it crosses a known microscopic barrier.  That makes it a
real flagship problem, not a currently completed contribution.
