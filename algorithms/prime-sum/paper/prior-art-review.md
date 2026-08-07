# Adversarial prior-art review (August 2026)

Summary of a deep literature sweep run before submission. Full links inline.

## Verdicts per claim

1. **Analytic computation of S(x) = Σp — NOVEL as a computation.** No published
   explicit-formula implementation with exact integer recovery found. The
   underlying first-Riesz-mean formula Σ(x−n)Λ(n) = x²/2 − Σ_ρ x^{ρ+1}/(ρ(ρ+1)) − …
   is classical (Montgomery–Vaughan ch. on explicit formulae) — novelty rests on
   the algorithm/implementation and must be phrased that way. Cite-and-distinguish
   arXiv:2506.22634 (TG-kernel π(x) preprint; claims look dubious but a referee
   may surface it). Cite Axler arXiv:1409.1777 for S(x) bounds.

2. **σ-integral log-stripping — vulnerable to "reparametrization" objection.**
   ∫₀^A −(ζ′/ζ)(s+σ−1)dσ = log ζ(s−1) − log ζ(s+A−1): the device is
   Fubini-equivalent to the classical log ζ Perron representation used since
   Lagarias–Odlyzko/Platt. Unpublished as a mechanism, but must be presented as
   an *operational* contribution: elementary erfc/exp integrands, finite
   Gauss–Legendre quadrature, no branch tracking — not a new analytic identity.

3. **"Li-free analytic π(x)" — REFUTED as headlined.** FKBJ (Math. Comp. 86,
   2017, π(10²⁴) under RH) and Büthe (arXiv:1410.7008, π(10²⁵)) work on the
   Weil–Barner (ζ′/ζ) side: no li(x^ρ), no branch cuts. Platt also never
   evaluates li per zero (constructs the antiderivative with branch management).
   Surviving narrow claim: *all transforms in elementary closed form* (erfc/exp
   only; no Logan/Bessel kernels, no numerically constructed antiderivatives).
   MUST cite FKBJ, Büthe (1410.7008, 1410.7015), Galway (2004 thesis),
   Riesel–Göhl (1970).

4. **AP prime sums from L-zeros — lean novel-as-engineering.** Bays–Hudson
   (Math. Comp. 69, 2000) computed π_{4,3}−π_{4,1} irregularities from L-zeros to
   x≈10³⁰⁰ (approximate, GRH-conditional); Hutama (2017) has demo-level ψ(x,χ)
   plots. Exact integer recovery appears uncomputed. Claim as "we carry out",
   not "we introduce".

5. **Σp², Σ1/p — novel as computation, low surprise.** For Σ1/p, Büthe
   (arXiv:1503.01277, Mertens sign change) is the close antecedent — uses zero
   data + explicit formula to control Σ1/p − ln ln x − M beyond sieving range.
   Drop "exact recovery" framing for the non-integer target; position as
   certified enclosure, complementary to Möbius/prime-zeta methods.

## Required bibliography additions

Galway (2004 thesis); Franke–Kleinjung–Büthe–Jost (Math. Comp. 86, 2017);
Büthe (arXiv:1410.7008, 1410.7015, 1503.01277); Riesel–Göhl (Math. Comp. 24,
1970); Bays–Hudson (Math. Comp. 69, 2000); Axler (arXiv:1409.1777);
Brent–Platt–Trudgian (arXiv:2009.13791); Montgomery–Vaughan explicit-formulae
chapter; distinguish arXiv:2506.22634.

## Bottom line

Headline (S(x) implementation + unified weighted family + AP extension as
engineering) survives with softened phrasing. The two sentences a referee would
attack — "no direct analogue in the π(x) literature" for the σ-device, and any
li-free-novelty claim for π(x) — must be rewritten per above.
