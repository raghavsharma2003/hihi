# Fresh novelty search for the focused hard-edge paper

Audit date: 2026-08-17.

Status: primary-source literature audit, not a priority certificate.  This
search was designed to test the exact conjunction in the focused manuscript,
not merely whether each ingredient is known.  Negative search results are
evidence, never proof of priority.

## 1. Exact statement tested

The target was the following assembled result:

1. the explicit one-parameter pencil
   \(C_{g,t}:y^2=\prod_{a=1}^{2g}(x-a)(x-t)\) over odd square fields;
2. the critically weighted inert-minus-split cumulative prime race with
   \(m_g+1/2=\lambda/((2g+1)\log Q_g)\);
3. the genuine endpoint limiting law for each curve;
4. a uniformly random parameter \(t_g\) and a simultaneous limit
   \(g,Q_g\to\infty\) under
   \(\log Q_g/(g^2\log(g+2))\to\infty\);
5. convergence of the *conditional endpoint laws*, as random elements of
   \((\mathcal P_2(\mathbb R),W_2)\), to a phase-marked symplectic
   hard-edge point-process law; and
6. nonconstancy/absolute continuity of the random limiting measure and a
   nonconstant limiting law for its positive-half-line mass.

No located paper states this full conjunction.  The exact assembly therefore
remains plausibly new.  Several individual pieces, including a piece much
closer to the race calculation than the present bibliography indicates, are
already known.

## 2. Search protocol and reproducible queries

The arXiv Atom API was searched in all fields, sorted by submission date, with
up to 100 results per query.  The following are the most diagnostic queries;
the numbers are the API result counts on the audit date.

| Query | Results | Relevant outcome |
|---|---:|---|
| `all:(hyperelliptic AND "prime race")` | 0 | No literal match |
| `all:("function field" AND "prime race")` | 1 | Bates--Jesubalan--Lee--Lu--Shim (2026), ties |
| `all:("prime number races" AND "function fields")` | 7 | Main race bibliography; see below |
| `all:(hyperelliptic AND "hard edge")` | 0 | No arithmetic literal match |
| `all:(hyperelliptic AND "prime races")` | 0 | No literal match |
| `all:(USp AND "prime race")` | 0 | No literal match |
| `all:(Wasserstein AND "prime race")` | 0 | No match |
| `all:("random probability measure" AND "prime races")` | 0 | No match |
| `all:("quenched law" AND "L-functions")` | 0 | No match |
| `all:("conditional law" AND hyperelliptic)` | 0 | No match |
| `all:("endpoint distribution" AND "L-function")` | 0 | No match |
| `all:(weighted AND "Chebyshev bias" AND "function field")` | 0 | No match |
| `all:("critical scaling" AND "prime race")` | 0 | No match |
| `all:(hyperelliptic AND "point process")` | 0 | No match |
| `all:(hyperelliptic AND determinantal)` | 1 | Unrelated to this arithmetic problem |
| `all:(hyperelliptic AND zeros AND symplectic)` | 7 | Relevant zero-statistics sources |
| `all:(hyperelliptic AND "L-functions")` | 40 | Checked recent 2023--2026 results |
| `all:("quadratic Dirichlet L-functions" AND "function fields")` | 36 | Checked recent 2023--2026 results |
| `all:("hard edge" AND symplectic)` | 14 | Random-matrix papers, no prime race |

Keyword searches were supplemented by the official bibliographies in the
primary papers closest to the target: Bailleul--Devin--Keliher--Li (2024),
Bates et al. (2026), Entin--Pirani (2024), Andrade--Shamesaldeen (2026), and
Lal\'in--Lee--Oliver--Pozdnyakov (2026).  Those bibliographies recovered the
older Cha, Kowalski, Katz--Sarnak, Perret--Gentil, Sedrati, Bailleul, low-zero,
and random-matrix lines listed below.

The search does not cover every non-arXiv preprint, thesis, translated title,
or paper indexed only in MathSciNet/zbMATH.  It also cannot detect a theorem
described with wholly different terminology.  A specialist bibliography
check remains mandatory before any priority statement.

## 3. Closest match: exceptional hyperelliptic biases

The most important fresh finding is:

**A. Bailleul, L. Devin, D. Keliher, W. Li, _Exceptional biases in counting
primes over function fields_, J. London Math. Soc. 109 (2024), e12876.**

- Primary preprint: <https://arxiv.org/abs/2302.13665>
- Version of record: <https://doi.org/10.1112/jlms.12876>

This paper is substantially closer than the generic `Bailleul2022` citation
now in the focused manuscript.  It studies quadratic characters attached to
hyperelliptic curves, split-versus-inert prime counts, fixed-curve endpoint
limiting distributions, linear independence, and the rarity of complete,
lower-order, and reversed biases in hyperelliptic families.  Its introduction
also records Kowalski's *same one-parameter pencil*
\(y^2=f(x)(x-t)\).  Its equation (2.2) gives the parity centers and Frobenius
oscillation for the exact-degree race, and Remark 2.8 gives an explicit
cumulative-degree formula.

What it does **not** provide is the manuscript's tunable exponent \(m_g\), the
critical scaling at \(-1/2\), a microscopic hard-edge coefficient profile, a
simultaneous \(Q_g,g\) point-process limit, a random
\(\mathcal P_2\)-valued family limit, or the resulting random density law.

Classification: a direct and mandatory race precedent, but not the exact
theorem.  The current introduction should not be released without citing and
distinguishing it.

## 4. Other close prime-race sources

### Fixed-race distributions and biases

- B. Cha, _Chebyshev's bias in function fields_ (2008): the foundational
  function-field limiting-distribution and bias framework.
  <https://doi.org/10.1112/S0010437X08003631>
- A. Bailleul, _Explicit Kronecker--Weyl theorems and applications to prime
  number races_ (2022): fixed-race densities without an LI assumption and
  effective Kronecker--Weyl technology.
  <https://arxiv.org/abs/2007.05763>
- Y. Sedrati, _Inequities in the Shanks--R\'enyi prime number race over
  function fields_ (2022): asymptotic density formulas for many-way races as
  the modulus degree grows, under LI.
  <https://arxiv.org/abs/2110.06669>
- B. Cha, D. Fiorilli, F. Jouve, _Prime number races for elliptic curves over
  function fields_ (2016): family-generic behavior and a central limit theorem
  for a different arithmetic race.
  <https://arxiv.org/abs/1502.05295>
- I. Kaneko, S. Koyama, _A New Aspect of Chebyshev's Bias for Elliptic Curves
  over Function Fields_ (2023): rank-sensitive bias via partial Euler products,
  not a hyperelliptic hard-edge law.
  <https://arxiv.org/abs/2206.05445>
- G. Bates, R. Jesubalan, S. Lee, J. Lu, H. Shim, _Ties in Function Field
  Prime Races_ (2026): exact-degree congruence-class ties from explicit
  formulas and \(\mathrm{GL}_2\)-bijections.  It is current race literature,
  but it has no hyperelliptic family limit, critical weight, hard edge, or
  random-measure convergence.
  <https://arxiv.org/abs/2603.21005>

These sources make the following claims unsafe: that fixed function-field
race laws are new; that existence of endpoint densities is new; or that
family averaging and generic LI in function-field races are new.

### Generic independence and the exact pencil

- E. Kowalski, _The large sieve, monodromy, and zeta functions of algebraic
  curves, II: independence of the zeros_ (2008): density-one independence and
  simultaneous information for the pencil \(y^2=f(x)(x-t)\).
  <https://arxiv.org/abs/0807.2118>
- E. Kowalski, preceding large-sieve paper and author erratum:
  <https://people.math.ethz.ch/~kowalski/large-sieve-monodromy.pdf> and
  <https://people.math.ethz.ch/~kowalski/erratum-large-sieve-monodromy.pdf>.
- C. Perret--Gentil, _Roots of L-functions of characters over function fields,
  generic linear independence and biases_ (2020): generic LI and bias
  applications in trace-function families.
  <https://arxiv.org/abs/1903.05491>
- B. Cha, D. Fiorilli, F. Jouve, _Independence of the zeros of elliptic curve
  L-functions over function fields_ (2017): quantitative family-generic LI in
  elliptic-curve families.
  <https://arxiv.org/abs/1502.05294>

Thus neither the pencil, maximal-Galois/LI mechanism, nor simultaneous
large-field/large-genus information is itself a novelty claim.

## 5. Closest symplectic low-zero and double-limit sources

- A. Entin, E. Roditty-Gershon, Z. Rudnick, _Low-lying zeros of quadratic
  Dirichlet L-functions, hyper-elliptic curves and Random Matrix Theory_
  (2013): hyperelliptic zero statistics and an iterated large-field then
  large-genus comparison with \(\mathrm{USp}\).
  <https://arxiv.org/abs/1208.5962>
- H. Bui, A. Florea, _Zeros of quadratic Dirichlet L-functions in the
  hyperelliptic ensemble_ (2018): support-restricted low-zero densities in the
  fixed-field conductor limit.
  <https://arxiv.org/abs/1605.07092>
- A. Entin, N. Pirani, _Moments of traces of random symplectic matrices and
  hyperelliptic L-functions_ (2024): trace moments through total Fourier degree
  \(4g+1\) and narrow-band linear statistics.  It does not give the target
  quenched race law.
  <https://arxiv.org/abs/2409.04844>
- J. Andrade, A. Shamesaldeen, _Correlations of zeros of a family of
  L-functions in function fields with symplectic symmetry_ (2026): ratios-based
  formulas for \(n\)-level densities, not a proved complete hard-edge process
  or conditional prime-race measure.
  <https://arxiv.org/abs/2607.06022>
- M. Lal\'in, K.-H. Lee, T. Oliver, A. Pozdnyakov, _Murmurations of quadratic
  and cubic characters over function fields_ (2026): high-power trace
  asymptotics, lower-order one-level-density terms, and arbitrarily wide fixed
  Fourier support when \(q\) is sufficiently large relative to the support.
  Its final nonvanishing statement is an iterated
  \(\lim_{q\to\infty}\liminf_{g\to\infty}\) result.  It does not prove a
  quenched prime-race law, a full hard-edge point-process limit, or
  \(\mathcal P_2\)-valued convergence.
  <https://arxiv.org/abs/2608.01337>
- F. \c{C}i\c{c}ek, P. Darbar, A. Lumley, _Linear Combinations of Logarithms of
  L-functions over Function Fields at Microscopic Shifts and Beyond_ (2025):
  microscopic-shift distribution estimates under a low-lying-zero hypothesis,
  for a different observable.
  <https://arxiv.org/abs/2511.14563>

The 2026 murmurations paper is especially important for wording.  It further
weakens any broad claim that bringing large fields, large genus, and
microscopic/large-Fourier-degree statistics together is new.  It does not,
however, duplicate the manuscript's nonlinear marked conditional law.

## 6. Random-matrix/DPP component

The limiting kernel

\[
K_{\mathrm{Sp}}(x,y)=\frac{\sin\pi(x-y)}{\pi(x-y)}-
\frac{\sin\pi(x+y)}{\pi(x+y)}
\]

is the standard symplectic scaling kernel at the origin; it and the general
determinantal-process variance/continuity technology are established random
matrix inputs, not arithmetic novelties.  Relevant primary references include
Katz--Sarnak's monograph and Soshnikov's DPP survey:

- <https://doi.org/10.1090/coll/045>
- <https://arxiv.org/abs/math/0002099>

No source located attaches independent phase marks with the manuscript's
coefficient
\(4\lambda/\sqrt{\lambda^2+(2\pi y)^2}\), interprets the result as a
conditional weighted prime-race law, and proves convergence in \(W_2\).
The marked series and its random \(\mathcal P_2\)-valued interpretation are
therefore the clearest candidate conceptual contribution.

## 7. Component-by-component verdict

| Component of the manuscript | Fresh classification |
|---|---|
| Hyperelliptic pencil and full symplectic monodromy | Established input |
| Density-one LI/maximal Galois group | Established input |
| Fixed-curve endpoint limiting distribution | Established race technology |
| Split-versus-inert hyperelliptic prime race and parity centers | Closely preceded by Bailleul--Devin--Keliher--Li |
| Simultaneous large-field/large-genus information | Established in other forms; not independently new |
| Symplectic hard-edge kernel/DPP | Established random-matrix input |
| Tunable critical weight and resulting coefficient profile | No exact precedent located |
| Genus-explicit transfer of the full conditional law to Haar | No exact precedent located |
| Marked hard-edge conditional law as a random element of \(\mathcal P_2\) | No precedent located |
| \(W_2\) convergence of actual endpoint laws | No precedent located |
| Random limiting half-line density law | No precedent located |

The novelty is therefore an **exact theorem-level assembly plus the critical
observable**, not a new monodromy theorem, a new LI theorem, a new prime-race
limiting-distribution theory, or a new hard-edge process.

## 8. Safe novelty language

Safe, subject to specialist confirmation:

> We have not located a prior result proving convergence of the complete
> conditional laws of a weighted hyperelliptic prime race, as random elements
> of \(\mathcal P_2(\mathbb R)\), to a phase-marked symplectic hard-edge law.
> The contribution is the critical weighted-race calculation and a
> genus-explicit transfer to that quenched limit in one simultaneous
> large-field/large-genus regime.

Unsafe:

- "the first simultaneous large-field/large-genus theorem";
- "the first limiting distribution for hyperelliptic prime races";
- "the first generic hyperelliptic race theorem";
- "a new symplectic hard-edge process";
- "we solve the hyperelliptic microscopic Katz--Sarnak problem";
- any unqualified "first" or exhaustive priority claim.

## 9. Release verdict

**Exact-statement verdict:** no duplicate located; plausible novelty survives.

**Title/abstract impact:** no located collision requires changing the current
descriptive title, and the abstract's factual theorem summary contains no
unsafe priority claim.  The necessary repair is in the introduction's
literature comparison and bibliography.  If the abstract is later changed to
say "first", that word should be removed.

**Current release verdict:** **hold for literature repair, not for theorem
abandonment**.  Before public release, the introduction and bibliography must
at minimum add and explicitly distinguish:

1. Bailleul--Devin--Keliher--Li (2024), because it is the closest existing
   hyperelliptic split/inert race and fixed-law precedent;
2. Bates--Jesubalan--Lee--Lu--Shim (2026), as current function-field
   prime-race literature; and
3. Lal\'in--Lee--Oliver--Pozdnyakov (2026), as current large-genus/high-trace
   hyperelliptic literature relevant to any broad bridge claim.

Sedrati (2022) is also a reasonable addition to the race context.  The final
paper should use the cautious sentence above and should invite an arithmetic
geometer/prime-race specialist to challenge the bibliography before posting.

This audit supports a focused, apparently new specialist bridge theorem.  It
does not support an exhaustive priority claim or a "groundbreaking" label.
