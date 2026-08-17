# Novelty and significance audit: simultaneous hyperelliptic race law

Status: independent adversarial audit, 2026-08-17. Literature was searched
through that date. This note audits
`canonical-simultaneous-hyperelliptic-law.md` and the strengthened formulation
in `canonical-simultaneous-quenched-upgrade.md`; it is not a proof certificate
or a priority guarantee. Only primary research sources are used for technical
comparisons.

## 1. Bottom line

No source located states the exact proposed result: an explicit one-parameter
hyperelliptic pencil over an explicit simultaneous sequence of square fields,
density-one linear independence obtained from maximal Weyl-group Galois group,
and convergence of the complete quenched weighted-race law as a random
\(\mathcal P_2(\mathbb R)\)-valued object to a nondegenerate law constructed
from the symplectic hard-edge process. The convergence of the **actual weighted
degree-race density** is then a threshold corollary.

The result is therefore plausibly new. It is not, however, a foundational
breakthrough on the scale suggested by a 9.5/10 rating. The arithmetic family,
full symplectic monodromy, genus-uniform maximal-Galois estimate, and the idea
of allowing the field and genus to grow simultaneously are already present in
Katz--Sarnak and Kowalski. The proposed paper's originality lies in assembling
those inputs with a new critical weighted-race calculation, a genus-explicit
nonlinear transfer, and a microscopic hard-edge marked-series limit.

The fairest classification is:

> a strong, focused new application/bridge theorem, assuming every analytic
> transfer step survives proof audit; not a solution of the fixed-field
> microscopic Katz--Sarnak problem.

It is not a routine one-line corollary. The exact prime-power decomposition,
the parity centers, the passage from character equidistribution to a nonsmooth
microscopic functional with genus-dependent constants, the marked
\(\ell^2\)-tail argument, and the bridge from maximal Galois group to the
actual race density all require real work. Conversely, the deliberately huge
field size imports Haar statistics in a regime designed to dominate those
costs, so the theorem should not be advertised as overcoming the central
fixed-field obstacle.

## 2. What is old and what appears new

| Component | Closest primary precedent | Audit classification |
|---|---|---|
| The exact pencil \(y^2=f(x)(x-t)\), with \(\deg f=2g\) | Katz--Sarnak, Chapter 10; Kowalski, Theorem 6.2 | Established input |
| Full geometric monodromy \({\rm Sp}(2g)\) and tameness for the pencil | Katz--Sarnak, Lemma 10.1.12 and Theorem 10.1.16 | Established input |
| Quantitative character equidistribution from a mod-\(3\) trivializing cover | Katz--Sarnak, Theorem 9.2.6 | Established theorem; the explicit genus bookkeeping is an application |
| Maximal Weyl-group Galois group for almost all members, with \(g,q\) varying | Kowalski, Theorem 6.2 and erratum | Established input; Kowalski explicitly notes simultaneous information |
| Maximal Galois group implies only reciprocal-pair multiplicative relations | Kowalski, Proposition 2.4 | Established algebraic input; the square-field LI specialization is a clean derivation |
| Limiting degree distribution and Bessel-product characteristic functions for a fixed function-field prime race | Cha; later Bailleul removes LI in a general Kronecker--Weyl framework | Established race technology |
| Generic LI plus family averaging and a \({\rm USp}\) functional in a hyperelliptic family | Cha, *The summatory function of the Möbius function in function fields* | Very close conceptual precedent |
| Hyperelliptic low-zero statistics in iterated or support-restricted regimes | Entin--Roditty-Gershon--Rudnick; Bui--Florea; Entin--Pirani | Established local-statistics background, but not the nonlinear sign law |
| Critical weight \(M_g=\lambda/((2g+1)\log Q_g)\), exact square-prime centers, and the resulting cosine coefficients | No exact precedent located | Apparently new calculation |
| An actual race-density law converging to \(F_\lambda(\Pi_{\rm Sp})\) along an explicit simultaneous sequence | No exact precedent located | Apparently new theorem-level assembly |
| A random conditional race law converging in \(\mathcal P_2(\mathbb R)\) | No prime-race precedent located | Apparently new and preferable flagship formulation |

The closest conceptual warning is Cha's Möbius paper: generic hyperelliptic
LI, Katz--Sarnak family averaging, and a large-genus \({\rm USp}\) functional
have already been combined. A submission must distinguish its object sharply:
the present object is a conditional weighted-race probability law at the
hard edge, not a Mertens bound or a characteristic-polynomial moment.

## 3. Primary-source statement audit

### 3.1 Kowalski

Kowalski's Theorem 6.2 treats the same form
\(y^2=f(x)(x-u)\), for squarefree \(f\) of degree \(2g\). It bounds the
exceptional parameters by

\[
  \ll g^2 q^{1-\gamma_g}\log q,
  \qquad \gamma_g=(4g^2+3g+5)^{-1},
\]

after applying item 3 of the published erratum. The original displayed theorem
omits the factor \(g^2\); the erratum requires it. The paper states that the
implied constant is absolute in this setting and explicitly points out that the
bound carries information when \(q\) and \(g\) increase together. Therefore
"simultaneous large field and large genus" by itself is not a novelty claim.

Kowalski's Proposition 2.4(2) identifies the rational multiplicative-relation
space under maximal Weyl-group Galois group: apart from the product relation,
relations are forced by reciprocal pairs. For square \(Q=s^2\), normalizing by
the rational integer \(s\) preserves the rational splitting field. Applying
the proposition to a putative relation among
\(\theta_1,\ldots,\theta_g,\pi\) gives the required LI. This last square-field
specialization is a derivation from the proposition, not a theorem quoted
verbatim from the source; it should be written out completely.

### 3.2 Katz--Sarnak

For a pure weight-zero lisse sheaf whose arithmetic representation lands in
the geometric monodromy group, Katz--Sarnak Theorem 9.2.6(5) gives a normalized
irreducible-character error bounded by

\[
  \frac{2\,\dim(\rho)\,C(X,\mathcal F)}{\sqrt{|E|}},
  \qquad |E|>4A(X)^2.
\]

Part (4) permits \(C(X,\mathcal F)\) to be taken as the total compactly
supported Betti number of a finite étale cover trivializing the sheaf modulo
an auxiliary prime. Lemma 10.1.12 supplies tameness for this pencil, and
Theorem 10.1.16 supplies full geometric monodromy \({\rm Sp}(2g)\).

There is one concrete error in the candidate note. For

\[
 U_g=\mathbb A^1\setminus\{1,\ldots,2g\},
\]

one has

\[
 b_c^0(U_g)=0,\qquad b_c^1(U_g)=2g,\qquad b_c^2(U_g)=1,
\]

and hence Katz--Sarnak's
\(A(U_g)=\sum_{i<2}b_c^i(U_g)=2g\), not \(2g-1\). The candidate's sufficient
condition \(Q>16g^2\) remains exactly valid because
\(4A(U_g)^2=16g^2\); the arithmetic slip does not invalidate that step, but it
must be corrected before submission.

The proposed level-cover estimate is consistent with these theorems. If its
degree is \(N_g\leq |{\rm GL}(2g,\mathbb F_3)|<3^{4g^2}\), tameness and
multiplicativity of the compactly supported Euler characteristic give, for
\(c\) connected components,

\[
 b_c^1=c+N_g(2g-1),\qquad b_c^2=c,
\]

so the total Betti number is at most \(N_g(2g+1)\). The half-Tate twist over a
square field also needs to be stated explicitly: the constant \(3\)-adic
character taking Frobenius to \(s^{-1}\) is continuous because \(3\nmid s\),
and the twist makes arithmetic monodromy land in, and hence equal, the full
symplectic group.

### 3.3 What existing low-zero results do not provide

Entin--Pirani's trace-moment theorem reaches total Fourier degree at most
\(4g+1\). It controls fixed-complexity local statistics, not an arbitrary
microscopic sign functional whose approximation complexity must grow.
Entin--Roditty-Gershon--Rudnick prove the full random-matrix comparison in an
iterated large-field/large-genus regime and a fixed-field, large-genus
\(n\)-level result only under restricted Fourier support. Bui--Florea likewise
obtain support-restricted fixed-field one- and pair-density results. None of
these statements yields convergence of the complete hard-edge process or the
proposed nonlinear conditional law.

Recent ratios work of Andrade--Shamesaldeen is conjectural/ratios-derived and
concerns \(n\)-level densities, not this race law. It is relevant context, not
a precedence claim.

## 4. Closest prime-race precedents missing from the current discussion

The final paper should discuss at least the following distinctions.

1. Cha establishes the function-field Chebyshev-bias framework, natural degree
   densities under a grand-simplicity/LI hypothesis, and Bessel-product
   characteristic functions. This is the direct ancestor of the random-phase
   representation.
2. Cha--Kim study biases in function-field prime races and are a closer
   race-density citation than a general number-field analogy.
3. Bailleul gives a discrete Kronecker--Weyl treatment of prime-race densities
   without assuming LI. This does not provide a family hard-edge limit, but it
   prevents the paper from presenting the existence of fixed-race densities as
   new.
4. Perret-Gentil combines generic LI with bias questions in trace-function
   families. His families and limit objects differ, but the methodological
   overlap should be acknowledged.
5. Cha--Fiorilli--Jouve prove generic behavior and a central limit theorem for
   elliptic-curve prime races over function fields. This is another important
   family-random-race precedent, although not a quenched random-measure limit.

A search for "quenched" race laws, random probability-measure limits for
function-field races, critical weighted splitting races, and Bessel/hard-edge
prime-race functionals found no exact prior theorem. This negative result is
evidence only; an expert MathSciNet/Zentralblatt search and direct consultation
with specialists remain appropriate before a public priority claim.

## 5. Stronger and cleaner flagship theorem

The scalar density should be a corollary of convergence of the entire
conditional race law. For an LI curve, define

\[
 \nu_{g,t,\lambda}
 =\frac12\sum_{\epsilon=0}^1
   {\rm Law}\!\left(
      c_{g,\lambda}^{(\epsilon)}+
      \sum_{j=1}^g b_{g,\lambda}(\theta_j)\cos\Phi_j
   \right)
 \in\mathcal P_2(\mathbb R).
\]

The natural proposed limit is the random probability measure

\[
 \nu_{\lambda,\Pi_{\rm Sp}}
 = {\rm Law}\!\left(
       1+\sum_{y\in\Pi_{\rm Sp}}
       a_\lambda(y)\cos\Phi_y
       \;\middle|\;\Pi_{\rm Sp}
   \right),
 \qquad
 a_\lambda(y)=\frac{4\lambda}
 {\sqrt{\lambda^2+(2\pi y)^2}}.
\]

The desirable statement is

\[
 \nu_{g,t_g,\lambda}\Longrightarrow
 \nu_{\lambda,\Pi_{\rm Sp}}
 \quad\text{as random elements of }
 (\mathcal P_2(\mathbb R),W_2).
\]

This is stronger, more intrinsic, and easier to recognize as genuinely new
than convergence of one threshold probability. The proof should be accessible
from the existing marked-series architecture. Under shared phases,

\[
 W_2^2\!\left({\rm Law}(c+\sum a_j\cos\Phi_j),
                   {\rm Law}(c'+\sum a'_j\cos\Phi_j)\right)
 \leq |c-c'|^2+\frac12\sum_j|a_j-a'_j|^2.
\]

Thus convergence of the centers and the marked coefficients in \(\ell^2\),
with a uniform tail estimate, gives a direct continuity principle. The density
is then

\[
 \delta_{g,t,\lambda}=\nu_{g,t,\lambda}((0,\infty)),
\]

and follows by the continuous-mapping argument once atomlessness at zero is
proved. The current three-summand/Bessel or marked-series argument is aimed at
exactly that threshold issue.

No located prime-race source formulates convergence of the family-random
**conditional law** in \(\mathcal P_2\). Fixed-race limiting distributions are
known; a quenched random-law limit over a hyperelliptic family appears to be a
real conceptual addition.

## 6. Nondegeneracy: what can and cannot yet be claimed

The random probability-measure limit has a clean rigorous nondegeneracy route.
Its conditional mean is \(1\), while its conditional variance is

\[
 V_\lambda(\Pi_{\rm Sp})
 =\frac12\sum_{y\in\Pi_{\rm Sp}}a_\lambda(y)^2
 =\sum_{y\in\Pi_{\rm Sp}}f_\lambda(y).
\]

Put

\[
 f_\lambda(y)=\frac12a_\lambda(y)^2
 =\frac{8\lambda^2}{\lambda^2+4\pi^2y^2}.
\]

This nonconstant function lies in \(L^1(0,\infty)\cap L^2(0,\infty)\). The
symplectic hard-edge kernel is a Hermitian projection kernel on
\(L^2(0,\infty)\). The projection-DPP variance identity gives

\[
 {\rm Var}\!\left(\sum_{y\in\Pi_{\rm Sp}}f_\lambda(y)\right)
 =\frac12\int_0^\infty\!\int_0^\infty
   (f_\lambda(x)-f_\lambda(y))^2
   |K_{\rm Sp}(x,y)|^2\,dx\,dy>0.
\]

Strict positivity follows because \(f_\lambda\) is nonconstant and the kernel
is nonzero on a set of positive two-dimensional measure. Hence
\(V_\lambda(\Pi_{\rm Sp})\) is not almost surely constant. If the conditional
law itself were deterministic, every continuous moment functional, including
its variance, would be deterministic. Therefore
\(\nu_{\lambda,\Pi_{\rm Sp}}\) is a genuinely nondegenerate random element of
\(\mathcal P_2(\mathbb R)\).

This does **not** prove that the scalar
\(F_\lambda(\Pi_{\rm Sp})\) is nonconstant. Conditional symmetry and
atomlessness give

\[
 F_\lambda(\Pi_{\rm Sp})
 =\frac12+\frac12\,
   \mathbb P\!\left(
      \left|\sum_y a_\lambda(y)\cos\Phi_y\right|<1
      \;\middle|\;\Pi_{\rm Sp}
   \right).
\]

Different symmetric laws can have different variances but the same mass in
\((-1,1)\). No primary source located proves nonconstancy of this exact
small-ball functional, and the DPP linear-statistic calculation alone is
insufficient. A proof would require, for example, a support/conditional
configuration lemma for the hard-edge process together with strict variation
of this small-ball probability under a controlled coefficient perturbation,
or a direct positive-variance/covariance computation for \(F_\lambda\).

Until such a proof is supplied, the manuscript may claim convergence to a
well-defined functional, but it should not call the scalar limiting density
"nontrivial" or "nondegenerate." The stronger random-law theorem avoids this
presentation weakness because its nondegeneracy is already accessible through
the conditional-variance statistic.

## 7. Publication and significance assessment

These scores assume the candidate proof is completed and independently checked:

| Criterion | Honest score |
|---|---:|
| Exact-statement novelty | 7/10 |
| Conceptual originality | 6/10 |
| Potential technical execution | 7.5/10 |
| Broad mathematical significance | 5.5--6/10 |
| Focus and verifiability | 8/10 |
| Overall as a completed focused paper | about 7/10 |

Current readiness is closer to 4--5/10: the heat-kernel smoothing bound and
marked-law transfer still need theorem-quality proofs, the Betti-number
arithmetic error must be corrected, scalar nondegeneracy is open, and no
external specialist has audited the argument.

Realistic venues after a complete proof and a compact rewrite include *Journal
of Number Theory*, *Finite Fields and Their Applications*, *Research in Number
Theory*, and *Acta Arithmetica*. *International Mathematics Research Notices*
is a stretch target if the paper proves the full random-law convergence,
nondegeneracy, and useful quantitative bounds with an exceptionally clean
presentation. On the theorem presently proposed, *Compositio Mathematica*,
*Algebra & Number Theory*, and the very top general journals are not realistic.
A fixed-field microscopic theorem would materially change that assessment.

For a fast, credible submission, the best shape is roughly 20--30 pages:

1. a general theorem for any odd square sequence satisfying
   \(\log Q_g/(g^2\log(g+2))\to\infty\);
2. the least-prime construction as an explicit corollary, not the headline;
3. convergence of the quenched law in \(\mathcal P_2\) as the main result;
4. the scalar density and mean density as corollaries;
5. a short section stating exactly which inputs are Katz--Sarnak/Kowalski and
   which lemmas are new.

A descriptive title such as *A simultaneous large-field/large-genus limit for
weighted quadratic prime races* is stronger than emphasizing "canonical."

## 8. Mandatory gates before a novelty claim or submission

1. Correct \(A(U_g)=2g\) and recheck every Katz--Sarnak hypothesis, including
   the half-Tate twist and the meaning of arithmetic versus geometric
   monodromy.
2. Write a complete proof of the exact prime-power decomposition, including
   signs, endpoint normalization, both parity centers, ramified primes, and all
   uniform error terms.
3. Prove the heat-kernel/character smoothing estimate with explicit metric,
   dimension, Casimir, and Sobolev normalizations; this is presently the most
   technically vulnerable bridge.
4. State and prove the \(\mathcal P_2\)-valued marked-series continuity lemma,
   including measurable enumeration and uniform \(\ell^2\) tails.
5. Either prove scalar \(F_\lambda\) nondegeneracy or deliberately make the
   nondegenerate random-law theorem the flagship and avoid the scalar claim.
6. Obtain external review from experts in function-field races, monodromy, and
   determinantal processes. Lean can verify finite algebraic/formal
   sublemmas, but it cannot certify the cited deep theorems, the priority
   search, or informal analytic estimates unless those are themselves fully
   formalized.

## 9. Primary sources checked

1. N. M. Katz and P. Sarnak, *Random Matrices, Frobenius Eigenvalues, and
   Monodromy*, AMS Colloquium Publications 45 (1999), especially Theorem 9.2.6,
   Lemma 10.1.12, and Theorem 10.1.16.
   <https://web.math.princeton.edu/~nmk/RMFEM.pdf>
2. E. Kowalski, "The large sieve, monodromy and zeta functions of curves,"
   *J. Reine Angew. Math.* 601 (2006), especially Proposition 2.4 and Theorem
   6.2. <https://people.math.ethz.ch/~kowalski/large-sieve-monodromy.pdf>
3. E. Kowalski, erratum to the preceding paper.
   <https://people.math.ethz.ch/~kowalski/erratum-large-sieve-monodromy.pdf>
4. E. Kowalski, "The large sieve, monodromy, and zeta functions of algebraic
   curves, II: independence of the zeros," 2008.
   <https://arxiv.org/abs/0807.2118>
5. B. Cha, "Chebyshev's bias in function fields," *Compositio Mathematica*
   144 (2008).
   <https://www.cambridge.org/core/services/aop-cambridge-core/content/view/01EF9B80CEA21A3C07C48957AD559EBE/S0010437X08003631a.pdf/chebyshevs_bias_in_function_fields.pdf>
6. B. Cha and S. Kim, "Biases in the prime number race of function fields,"
   *Journal of Number Theory* 130 (2010), 1048--1055.
   <https://doi.org/10.1016/j.jnt.2009.09.015>
7. B. Cha, "The summatory function of the Möbius function in function
   fields." <https://arxiv.org/abs/1008.4711>
8. B. Cha, D. Fiorilli, and F. Jouve, "Prime number races for elliptic curves
   over function fields." <https://arxiv.org/abs/1502.05295>
9. C. Perret-Gentil, "Roots of \(L\)-functions of characters over function
   fields, generic linear independence and biases," 2019.
   <https://arxiv.org/abs/1903.05491>
10. R. Bailleul, "Explicit Kronecker--Weyl theorems and applications to prime
   number races," 2020. <https://arxiv.org/abs/2007.05763>
11. A. Entin, E. Roditty-Gershon, and Z. Rudnick, "Low-lying zeros of quadratic
    Dirichlet \(L\)-functions, hyper-elliptic curves and Random Matrix Theory."
    <https://arxiv.org/abs/1208.5962>
12. H. M. Bui and A. Florea, "Zeros of quadratic Dirichlet \(L\)-functions in
    the hyperelliptic ensemble." <https://arxiv.org/abs/1605.07092>
13. A. Entin and N. Pirani, "Moments of traces of random symplectic matrices
    and hyperelliptic \(L\)-functions," 2024.
    <https://arxiv.org/abs/2409.04844>
14. Y. Aoki and S. Koyama, "Chebyshev's bias against splitting and principal
    primes in global fields," 2022. <https://arxiv.org/abs/2203.12266>
15. J. C. Andrade and A. Shamesaldeen, "Correlations of zeros of a family of
    \(L\)-functions in function fields with symplectic symmetry," 2026.
    <https://arxiv.org/abs/2607.06022>
16. A. Soshnikov, "Determinantal random point fields," *Russian Mathematical
    Surveys* 55 (2000), 923--975. <https://arxiv.org/abs/math/0002099>
