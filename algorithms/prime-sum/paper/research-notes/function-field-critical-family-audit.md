# Adversarial audit: hyperelliptic critical family

Date: 2026-08-17

Scope: first-principles audit of `function-field-critical-family.md`.  This is
an internal audit record, not a claim of external peer verification.

## Verdict

I found no fatal arithmetic or random-matrix obstruction to the stated
**iterated** limit (first `Q=q_0^n -> infinity` at fixed genus, then
`g -> infinity`).  The geometric kernel, critical scaling, parity centers,
generic-LI bridge, and order of limits are mutually consistent.

The draft is nevertheless **not safe to paste unchanged into the manuscript**.
The convergence of the random *quenched sign-probability functional* is only
sketched and needs a stated lemma in an `ell^2` coefficient topology.  Two
elementary proof errors were corrected in the source note during this audit.
Novelty/priority also remains an external literature-review question.

## Corrections made

1. In (5.2), `int_R^{d/2}` was replaced by `int_R^infinity`; the former is
   negative when `R>d/2` and therefore cannot be an upper bound for a
   nonnegative expectation.
2. The original void-probability argument established nonemptiness, not
   infinitude.  It was replaced by the determinantal estimate
   `Var N_L = Tr(K_L-K_L^2) <= Tr K_L` and Chebyshev, using
   `E N_L = L+O(1)`.
3. The note now explicitly records
   `M=lambda/(d log Q)=lambda/(dn log q_0)`.  Thus `M<1/6` does hold after
   discarding finitely many inner-limit values of `n`.  The quantity independent
   of `n` is `M log Q=lambda/d`, not `M`.  The proposed objection that `M` is
   independent of `n` was itself incorrect.

## Exact arithmetic calculation

Let

```text
A_D(N) = sum_{deg P <= N} (deg P) chi_D(P) Q^{m deg P},
Psi_D(k) = sum_{deg f=k} Lambda(f) chi_D(f).
```

Then

```text
sum_{k<=N} Q^{mk} Psi_D(k)
  = A_D(N) + sum_{a>=2, a deg P<=N} (deg P) chi_D(P)^a Q^{ma deg P},
Psi_D(k) = -sum_j alpha_{D,j}^k.
```

Hence `-A_D(N)` is the Frobenius spectral sum **plus** the prime-power
correction.  This confirms the sign: inert primes are positive, and squares
give a positive center.

With `r=Q^M=e^{lambda/d}` and `M=m+1/2`, one conjugate pair contributes

```text
4(1-r^{-1}) / |1-r^{-1}e^{-i theta}|
```

after absorbing the fixed denominator argument into the uniform phase.  In
the coordinate `y=d theta/(2 pi)`, this converges locally uniformly to

```text
4 lambda / sqrt(lambda^2 + (2 pi y)^2).
```

For `N=2L` and `N=2L+1`, respectively, the square main term is

```text
2(1-r^{-1})r^{-N} sum_{ell<=N/2} r^{2 ell}
  -> 2r/(r+1),  2/(r+1).
```

Both centers tend to `1` as `g -> infinity`.  The polynomial prime-number
theorem error is summable for `M<1/4`.  All powers `a>=3` are summable for
`1+3m<0`, equivalently `M<1/6`.  Primes dividing `D` contribute only a finite
term before endpoint normalization.  Thus the prime-square and higher-power
analysis is correct.

The race should define `chi_D(P)` explicitly as the Euler/Kronecker symbol
whose value is `+1` for split and `-1` for inert primes of
`F_Q(T)(sqrt D)`.  This avoids a quadratic-reciprocity convention ambiguity
between `(D/P)` and `(P/D)`.

## LI and the family average

The needed LI condition is rational independence of
`{theta_1,...,theta_g,pi}`.  It implies Kronecker--Weyl equidistribution on
each parity subsequence because `N=2k+epsilon` replaces the frequencies by
`2 theta_j`, while fixed phase shifts do not change Haar measure.

Cha's Theorem 3.1 states exactly that, for fixed odd `q_0` and fixed `g`, the
proportion of LI curves in
`H_{2g+1}(F_{q_0^n})` tends to one as `n -> infinity`.  The stronger-looking
condition `p>2g+1` is only used for the quantitative estimate in Cha's
subsequent remark, not for the qualitative density-one theorem.  Assigning
arbitrary values in `[0,1]` to non-LI curves changes the inner distribution by
at most the exceptional proportion.  It is therefore legitimate; one does
not need equidistribution conditional on the LI set.

For fixed `g`, Katz--Sarnak/Deligne equidistribution sends the full Frobenius
conjugacy class to Haar `USp(2g)`.  This is the correct input.  Equation (41)
of the Katz--Sarnak survey only states ordered-low-zero marginal limits; the
full point-process claim in the note should be presented as a consequence of
fixed-genus conjugacy-class equidistribution followed by the explicit Haar
kernel calculation, not attributed to (41) alone.

Primary-source checks:

- B. Cha, *The summatory function of the Moebius function in function
  fields*, Theorem 3.1 and its proof:
  <https://arxiv.org/abs/1008.4711>.
- E. Kowalski, *The large sieve, monodromy and zeta functions of algebraic
  curves, II: independence of the zeros*:
  <https://arxiv.org/abs/0807.2118>.
- N. Katz and P. Sarnak, *Zeroes of zeta functions and symmetry*, especially
  (40)--(42): <https://doi.org/10.1090/S0273-0979-99-00766-1>.
- B. Cha, *Chebyshev's bias in function fields*, for the discrete
  Kronecker--Weyl/parity mechanism:
  <https://doi.org/10.1112/S0010437X08003631>.

## USp kernel and tail check

The positive Haar-`USp(2g)` eigenangles form a determinantal process relative
to `d theta` with

```text
K_g(theta,phi)=(2/pi) sum_{k=1}^g sin(k theta)sin(k phi).
```

Under `y=d theta/(2 pi)`, `d=2g+1`, the kernel relative to `dy` is

```text
Ktilde_g(x,y)=(4/d) sum_{k=1}^g
  sin(2 pi kx/d)sin(2 pi ky/d),
```

and its Riemann-sum limit is

```text
S(x-y)-S(x+y),  S(t)=sin(pi t)/(pi t).
```

The normalization has unit bulk intensity and agrees asymptotically with the
Katz--Sarnak scale `g theta/pi`.

The diagonal bound `Ktilde_g(y,y)<2` gives

```text
E sum_{y>R} y^{-2} <= 2/R.
```

Moreover

```text
b_{g,lambda}(y) <= lambda exp(lambda/2)/y
```

follows from `sin(pi y/d)>=2y/d`.  Thus the expected discarded conditional
variance is `O_lambda(1/R)`, uniformly in `g`.  Local finiteness and the fact
that the process has no atom at `0` handle the compact part of the
reciprocal-square sum.

## Major proof completion still required

The sentence invoking truncation, Chebyshev, and absence of an atom does not
yet fully prove convergence in law of the **conditional** probabilities
`F_g(Pi_g)`.  Convergence of the annealed marked sums alone is weaker.

A clean repair is to state and prove this lemma:

> If random locally finite point measures converge vaguely in law, their
> coefficient vectors (points ordered increasingly and mapped through
> `b_{g,lambda}`) have uniformly vanishing `ell^2` tails in probability, and
> the limiting random-phase sum has no atom at the threshold almost surely,
> then the corresponding conditional sign probabilities converge in law.

Proof route: compact convergence gives convergence of every finite coefficient
block; the expectation bound above makes the `ell^2` tails vanish in
probability; use a subsequence/Skorokhod argument to obtain `ell^2`
convergence; couple the same i.i.d. phases to get `L^2` convergence of the
series; and use threshold continuity to pass sign probabilities.  The
symplectic limit is almost surely nonempty (indeed infinite), so splitting off
one arcsine summand proves the required atomlessness.

This is a proof-writing gap, not evidence that the theorem is false, but it is
large enough that the theorem should not enter the main paper before the lemma
is written and independently checked.

## Quenched law

For a fixed limiting configuration,
`sum b_lambda(y)^2<infinity`; the independent centered series therefore
converges almost surely and in `L^2`.  Since the process is nonempty, one
arcsine summand convolved with the independent remainder makes the law
absolutely continuous.  Also `sum b_lambda(y)^4<infinity`, and `L^4`
convergence permits termwise cumulants:

```text
kappa_4 = -(3/8) sum_y b_lambda(y)^4 < 0.
```

Thus the quenched non-Gaussian assertion is correct.  No conclusion about
the annealed fourth cumulant follows without a separate Fredholm-determinant
calculation, as the source note correctly warns.

## Integration gate

Before manuscript integration:

1. add the `ell^2` quenched-functional convergence lemma and a full proof;
2. state the Euler/Kronecker convention for `chi_D`;
3. cite Cha's density-one theorem and Katz--Sarnak equidistribution at their
   exact hypotheses;
4. keep the iterated order of limits in the theorem title, abstract, and every
   interpretation paragraph;
5. do not call the fixed-field or canonical simultaneous limit proved;
6. obtain an external function-field expert proof audit and a serious
   priority search before making a novelty claim.

Subject to these gates, the iterated theorem appears mathematically viable and
would be a substantive realization of the paper's conditional critical
transfer principle.  It is not, by itself, a 9.5/10 breakthrough: the inner
large-field limit imports Haar `USp` through established equidistribution.
