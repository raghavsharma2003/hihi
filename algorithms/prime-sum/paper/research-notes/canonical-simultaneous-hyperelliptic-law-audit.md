# Adversarial audit of the canonical simultaneous hyperelliptic law

Date: 2026-08-17

Scope: line-by-line audit of canonical-simultaneous-hyperelliptic-law.md, from
the cited primary sources and direct calculations. This is an internal audit
record, not peer review and not a priority certificate.

Correction record: a subsequent independent novelty/source audit found that
the first version of this report miscomputed the base complexity as
`A(U_g)=2g-1`.  The correct compact-support Betti numbers give `A(U_g)=2g`.
The note and this report now use the correct value.  The sufficient hypothesis
`Q>16g^2` was already correct and the theorem is unaffected.

A later dedicated probability audit also found that vague convergence on
`(0,infinity)` was insufficient because points could escape to zero.  The
research note now places the processes on `[0,infinity)`, where local kernel
convergence through zero and a closed-hard-edge matching lemma repair the
argument.  Thus this first general audit should not be read as the final word
on the point-process step; the dedicated audit is the governing record there.

## Verdict

**Safe for development as the single theorem of a focused manuscript.**
I found no fatal mathematical blocker after correcting the proof-writing issues
listed below. It is **not yet safe to describe as submission-ready or
externally verified**: the heat-kernel bridge and marked-series lemma still
deserve an independent expert audit, and the novelty search is not exhaustive.

The result is a rigorous simultaneous large-field/large-genus bridge theorem,
not the fixed-field microscopic theorem. Its mathematical value is
checkability and a concrete arithmetic realization of the critical law. The
astronomical field growth and one-parameter pencil materially limit its claim
to being a breakthrough.

## Primary-source checks

1. **Pencil monodromy and varying characteristic: pass.** Katz--Sarnak,
   Theorem 10.1.16, proves geometric monodromy \(\operatorname{Sp}(2g)\) for
   \(y^2=f(x)(x-t)\) in every odd characteristic when \(f\) has \(2g\)
   distinct roots. The chosen \(p_g>2g+1\) makes
   \(1,\ldots,2g\) distinct, and connected monodromy is unchanged after
   base-change to \(\mathbb F_{Q_g}\).
2. **Large-sieve exceptional exponent: pass.** Kowalski, Theorem 6.2, gives
   \(\gamma_g=(4g^2+3g+5)^{-1}\) with an absolute implied constant for this
   split one-parameter pencil. Item 3 of the published erratum inserts the
   necessary factor \(g^2\). The note now uses exactly
   \(O(g^2Q^{1-\gamma_g}\log Q)\).
3. **Maximal \(W_{2g}\) implies angle-plus-\(\pi\) LI over square fields:
   pass.** The normalized inverse roots are the roots of
   \(s_g^{-2g}R_{g,t}(s_gX)\in\mathbb Q[X]\), where
   \(Q_g=s_g^2\) and \(R\) is the reciprocal characteristic polynomial.
   Kowalski, Proposition 2.4(2), with its \(m=1\), identifies the rational
   multiplicative-relation space with the reciprocal-pair space for \(g\ge2\).
   Squaring the exponential of an integral angle relation then forces every
   angle coefficient, and finally the \(\pi\) coefficient, to vanish. No
   saturation claim is needed.
4. **Katz--Sarnak character normalization: pass.** After base change to the
   square field, twisting arithmetic Frobenius by \(Q^{-1/2}=s^{-1}\) produces
   a weight-zero \(\mathbb Q_3\)-sheaf whose full arithmetic monodromy lies in
   \(\operatorname{Sp}(2g)\). For
   \(U_g=\mathbb A^1-\{2g\text{ points}\}\),
   \(A(U_g)=2g\). Theorem 9.2.6(5) therefore gives
   \[
   \left|\frac1{|U_g(\mathbb F_Q)|}\sum_t\chi_\rho(\Theta_{g,t})\right|
   \le \frac{2C_g\dim\rho}{\sqrt Q}
   \]
   once \(Q>16g^2\), exactly the note's displayed sufficient condition.
5. **Mod-\(3\) cover and Betti constant: pass.** The kernel cover has degree
   \(N_g\le|\operatorname{GL}(2g,\mathbb F_3)|<3^{4g^2}\).
   Katz--Sarnak, Lemma 10.1.12, gives tameness at all boundary points.
   Tame Euler-characteristic multiplicativity gives
   \(\chi_c(Y)=N_g(1-2g)\). If \(c\) is the number of components, affineness
   gives \(b_c^0=0\), duality gives \(b_c^2=c\), and hence
   \(b_c^1=c+N_g(2g-1)\). Therefore
   \(C_g\le(2g+1)3^{4g^2}\).
6. **Canonical growth rule: pass.** Bertrand's postulate controls the least
   prime, and minimality of \(n_g\) gives
   \[
   g^2\log^2(g+2)\le\log Q_g
   <g^2\log^2(g+2)+2\log p_g.
   \]
   This makes both the LI-exception probability and the heat-smoothed
   equidistribution error tend to zero.

## Direct analytic and arithmetic checks

1. **Race sign and normalization: pass.** From
   \(\Psi(k)=-\sum_j\alpha_j^k\), subtracting prime powers from the von
   Mangoldt sum gives \(-A(N)\) equal to the positive Frobenius spectral sum
   plus the prime-power correction. Thus inert primes and the square center
   have the signs stated in the note.
2. **One-pair amplitude: pass.** The exact geometric series, after multiplying
   by \(2(1-r^{-1})r^{-N}\), gives
   \[
   \frac{4(1-r^{-1})}{|1-r^{-1}e^{-i\vartheta}|}.
   \]
   With \(r=e^{\lambda/(2g+1)}\) and
   \(y=(2g+1)\vartheta/(2\pi)\), this tends locally uniformly to
   \(4\lambda/\sqrt{\lambda^2+(2\pi y)^2}\).
3. **Prime powers and parity centers: pass.** The square main term gives
   \(2r/(r+1)\) on even endpoints and \(2/(r+1)\) on odd endpoints. The
   prime-polynomial-theorem error is summable for \(M<1/4\); all powers
   \(a\ge3\) are summable for \(M<1/6\). Both centers tend to \(1\).
4. **Lipschitz estimate: pass after metric repair.** Three Bessel factors give
   a density bound \(O(1/b_{\min})\). Coupling phases, the derivative bound,
   and eigenangle matching give
   \(\operatorname{Lip}(F_{g,\lambda})=O_\lambda(g^{5/2})\) for the explicitly
   specified Hilbert--Schmidt bi-invariant metric.
5. **Heat bridge: pass at proof-architecture level.** Character expansion,
   Katz--Sarnak's bound, and Cauchy--Schwarz reduce the error to the heat trace.
   The type-\(C_g\) Weyl dimension formula and the Casimir lower bound give
   \[
   k_s(e)\le
   \exp(Cg^2\log(g+2))s^{-Cg^2}.
   \]
   Taking \(s=g^{-10}\) yields an \(O_\lambda(g^{-3/2})\) smoothing error and
   an arithmetic error
   \(Q^{-1/2}\exp(O_\lambda(g^2\log g))\). The original note's undefined
   “standard metric” and exact constant \(1\) in the Brownian estimate were
   unsafe; they were replaced by a fixed metric and an absolute constant.
6. **Hard-edge kernel and tails: pass.** Rescaling the finite
   \(\operatorname{USp}(2g)\) sine kernel gives exactly
   \(S(x-y)-S(x+y)\). The diagonal is \(<2\), so
   \(\mathbb E\sum_{y>R}y^{-2}\le2/R\), and the coefficients have a uniform
   \(O_\lambda(1/y)\) envelope.
7. **Marked-sign functional: pass after measurable formulation.** The note
   now uses Borel increasing enumeration, includes the converging deterministic
   centers, proves full \(\ell^2\) convergence by compact convergence plus
   uniform tails, and couples phases in conditional \(L^2\). The limiting
   process is infinite by the determinantal variance bound, and one arcsine
   summand convolved with the independent remainder makes the threshold
   atomless.

## Corrections made to the research note

- Replaced the ambiguous normalized-polynomial sentence by the exact reciprocal
  polynomial \(s^{-2g}R(sX)\).
- Removed an unnecessary integral-lattice saturation claim and wrote the
  \(W_{2g}\)-to-LI argument coefficient by coefficient.
- Specified the square-field half-Tate twist and the exact
  \(A(U_g)=2g\) threshold in Katz--Sarnak.
- Expanded the tame mod-\(3\) level-cover Euler-characteristic calculation.
- Added the exact von Mangoldt/prime-power decomposition and parity limits.
- Fixed the bi-invariant metric, Brownian constant, and Casimir normalization
  in the heat argument.
- Replaced the informal marked-sign lemma by a measurable-enumeration version
  and proved infinitude/atomlessness.
- Added the close-prior-work warning and explicitly declined a novelty claim.

## Fatal blockers and remaining gates

**Fatal mathematical blockers found: none.**

Remaining nonfatal but mandatory gates before submission:

1. have an independent expert in compact Lie-group heat kernels check the
   uniform form of the heat-trace lemma;
2. have a probability/point-process expert check the measurable marked-series
   lemma;
3. perform a database-level priority review and contact a function-field
   expert, because a web/arXiv search is not a priority certificate;
4. present this as a simultaneous large-field theorem, never as the fixed-field
   Katz--Sarnak microscopic conjecture;
5. do not promise “100% Lean verification” of the complete theorem with the
   present library: formalizing Katz--Sarnak's l-adic monodromy and
   equidistribution and Kowalski's large sieve would be a major independent
   formalization project. Elementary algebraic, analytic, and limit-transfer
   lemmas can be formalized separately without pretending the cited arithmetic
   theorems are Lean-checked.

## Sources checked directly

- N. Katz and P. Sarnak, *Random Matrices, Frobenius Eigenvalues, and
  Monodromy*, Theorem 9.2.6 and Sections 10.1.12--10.1.16:
  <https://web.math.princeton.edu/~nmk/RMFEM.pdf>.
- E. Kowalski, *The large sieve, monodromy and zeta functions of curves*,
  Theorem 6.2:
  <https://people.math.ethz.ch/~kowalski/large-sieve-monodromy.pdf>.
- E. Kowalski, published erratum, item 3:
  <https://people.math.ethz.ch/~kowalski/erratum-large-sieve-monodromy.pdf>.
- E. Kowalski, *The large sieve, monodromy, and zeta functions of algebraic
  curves, II*, Proposition 2.4:
  <https://arxiv.org/abs/0807.2118>.
- A. Entin, E. Roditty-Gershon, and Z. Rudnick, *Low-lying zeros of quadratic
  Dirichlet L-functions, hyper-elliptic curves and Random Matrix Theory*:
  <https://arxiv.org/abs/1208.5962>.
- M. Aoki and S. Koyama, *Chebyshev's Bias against Splitting and Principal
  Primes in Global Fields*:
  <https://arxiv.org/abs/2203.12266>.
