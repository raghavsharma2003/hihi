# Outreach email — FINAL, SEND-READY (audits passed; links live)

**To:** gerg@math.ubc.ca (Prof. Greg Martin, University of British Columbia)
**Secondary option:** Prof. Shin-ya Koyama (Toyo University) — via the contact
form at researchmap.jp/koyama (no public email found)
**Attachment:** weighted-races.pdf (the recompiled version with the DOI in the footnote)

---

**Subject:** A computational answer to Problem 12 of the comparative prime
number theory list

Dear Professor Martin,

I am an independent student researcher. Working with substantial AI
assistance (Anthropic's Claude), I have been computing weighted analogues of
the classical prime number races, and I believe the results amount to a
computational answer to Problem 12 of your comparative prime number theory
problem list (arXiv:2407.03530): they connect the weighted (Aoki–Koyama)
formulation of Chebyshev's bias with the classical logarithmic-density
formulation.

For the races D_m(x) = Σ_{p≤x, p≡3(4)} p^m − Σ_{p≡1(4)} p^m we computed
what appear to be the first Rubinstein–Sarnak densities for any weighted
prime race: δ(1) = 0.79731, δ(2) = 0.69468, δ(3) = 0.64577, with
δ(0) = 0.99593 reproducing the classical value as calibration — under the
usual GRH + LI hypotheses, from 511 zeros of L(s,χ₄) computed for the
purpose, and likewise for modulus 3. Exact segmented-sieve computations to
10^10 agree with the densities to about 3×10⁻³. We also derive, and confirm
numerically in both moduli, a dissolution law
δ_q(m) − 1/2 ~ (2π·2(m+½)·log(q(m+½)/2π))^(−1/2) as m → ∞ — an analogue in
the weight aspect of the Fiorilli–Martin density asymptotics.

The preprint is archived at https://doi.org/10.5281/zenodo.21947102 with all code and
data (https://github.com/raghavs1729/weighted-prime-races); a PDF is attached for
convenience. It carries full attribution to the existing literature
(Aoki–Koyama, Sheth, Shimada–Koyama, Humphries, Devin, Akbary–Ng–Shahabi,
Languasco–Zaccagnini) and an explicit statement of what is and is not new.
I want to be fully transparent that the derivations and code were
AI-produced; every headline number was then verified by two independent
routes, and the draft discloses all of this.

If you find the note credible, I would also be grateful for an arXiv
endorsement for math.NT, so it can reach the community properly.

May I ask for your opinion: is this worth writing up properly, and might
you or a student be interested in taking a look? I am aware the existence
arguments and error terms need a professional hand, and I would welcome a
collaborator.

Thank you for your time,

Raghav Sharma
raghavsharma1729@gmail.com
Preprint: https://doi.org/10.5281/zenodo.21947102
Code and data: https://github.com/raghavs1729/weighted-prime-races
