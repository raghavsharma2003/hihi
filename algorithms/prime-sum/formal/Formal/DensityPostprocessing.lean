import Mathlib.Analysis.Real.Pi.Bounds
import Mathlib.Analysis.Real.Sqrt
import Mathlib.Tactic.GCongr
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum

set_option linter.style.header false

/-!
# Kernel-checked post-processing for the weighted-races density table

This module is deliberately independent of the program that produced the
analytic input intervals.  Its theorems have those intervals as explicit
hypotheses and machine-check only the exact consequences:

* the fourteen claims about rounding to six decimal places;
* the two genuinely ambiguous half-unit rounding boundaries;
* square-root enclosures using mathlib's proved 20-decimal bounds on `Real.pi`;
* propagation of positive interval inputs through the leading and second-order
  relative-residual transformations.

No floating-point evaluation occurs in this file.  Every decimal literal is an
exact rational embedded in the reals.  This does **not** prove GRH, LI, zero
completeness, quadrature bounds, or that the density/variance/moment inputs are
valid; those obligations remain outside this post-processing layer.
-/

namespace WeightedPrimeRaces.DensityPostprocessing

open Real

noncomputable section

/-- A value lies in the half-open nearest-rounding bin for a six-decimal
representative.  None of the fixed rows touches a tie, so no tie convention is
needed. -/
def RoundsToSix (x shown : ℝ) : Prop :=
  shown - 1 / 2000000 ≤ x ∧ x < shown + 1 / 2000000

/-! ## The fourteen density rows -/

theorem q4_m0_rounds (x : ℝ)
    (hlo : 0.995927866782 ≤ x) (hhi : x ≤ 0.995927983908) :
    RoundsToSix x 0.995928 := by
  constructor <;> norm_num [RoundsToSix] at * <;> linarith

theorem q4_m1_rounds (x : ℝ)
    (hlo : 0.797630378395 ≤ x) (hhi : x ≤ 0.797630419780) :
    RoundsToSix x 0.797630 := by
  constructor <;> norm_num [RoundsToSix] at * <;> linarith

theorem q4_m2_rounds (x : ℝ)
    (hlo : 0.694521087360 ≤ x) (hhi : x ≤ 0.694521114910) :
    RoundsToSix x 0.694521 := by
  constructor <;> norm_num [RoundsToSix] at * <;> linarith

theorem q4_m3_rounds (x : ℝ)
    (hlo : 0.645851046701 ≤ x) (hhi : x ≤ 0.645851069409) :
    RoundsToSix x 0.645851 := by
  constructor <;> norm_num [RoundsToSix] at * <;> linarith

theorem q4_m8_rounds (x : ℝ)
    (hlo : 0.571870091125 ≤ x) (hhi : x ≤ 0.571870113448) :
    RoundsToSix x 0.571870 := by
  constructor <;> norm_num [RoundsToSix] at * <;> linarith

theorem q4_m20_rounds (x : ℝ)
    (hlo : 0.538455286605 ≤ x) (hhi : x ≤ 0.538455320880) :
    RoundsToSix x 0.538455 := by
  constructor <;> norm_num [RoundsToSix] at * <;> linarith

theorem q4_m100_rounds (x : ℝ)
    (hlo : 0.513778241424 ≤ x) (hhi : x ≤ 0.513778355623) :
    RoundsToSix x 0.513778 := by
  constructor <;> norm_num [RoundsToSix] at * <;> linarith

theorem q3_m0_rounds (x : ℝ)
    (hlo : 0.999063097443 ≤ x) (hhi : x ≤ 0.999063289012) :
    RoundsToSix x 0.999063 := by
  constructor <;> norm_num [RoundsToSix] at * <;> linarith

/-- The first dagger is necessary: its input interval has points on both sides
of the boundary between 0.836880 and 0.836881.  The last two conjuncts prove
that no third six-decimal representative can occur. -/
theorem q3_m1_dagger :
    (0.836880448106 : ℝ) < 0.8368805 ∧
      (0.8368805 : ℝ) < 0.836880514652 ∧
      RoundsToSix (0.836880448106 : ℝ) 0.836880 ∧
      RoundsToSix (0.836880514652 : ℝ) 0.836881 := by
  norm_num [RoundsToSix]

theorem q3_m2_rounds (x : ℝ)
    (hlo : 0.723472889305 ≤ x) (hhi : x ≤ 0.723472932221) :
    RoundsToSix x 0.723473 := by
  constructor <;> norm_num [RoundsToSix] at * <;> linarith

theorem q3_m3_rounds (x : ℝ)
    (hlo : 0.666554247837 ≤ x) (hhi : x ≤ 0.666554281617) :
    RoundsToSix x 0.666554 := by
  constructor <;> norm_num [RoundsToSix] at * <;> linarith

theorem q3_m8_rounds (x : ℝ)
    (hlo : 0.578535581419 ≤ x) (hhi : x ≤ 0.578535607434) :
    RoundsToSix x 0.578536 := by
  constructor <;> norm_num [RoundsToSix] at * <;> linarith

theorem q3_m20_rounds (x : ℝ)
    (hlo : 0.540768194762 ≤ x) (hhi : x ≤ 0.540768228848) :
    RoundsToSix x 0.540768 := by
  constructor <;> norm_num [RoundsToSix] at * <;> linarith

/-- The second dagger is necessary, for the same exact half-unit reason. -/
theorem q3_m60_dagger :
    (0.519717445589 : ℝ) < 0.5197175 ∧
      (0.5197175 : ℝ) < 0.519717513972 ∧
      RoundsToSix (0.519717445589 : ℝ) 0.519717 ∧
      RoundsToSix (0.519717513972 : ℝ) 0.519718 := by
  norm_num [RoundsToSix]

/-- A single exact check of the manuscript's common width bound. -/
theorem all_density_widths_below_two_e_minus_seven :
    (0.995927983908 - 0.995927866782 : ℝ) < 0.0000002 ∧
    (0.797630419780 - 0.797630378395 : ℝ) < 0.0000002 ∧
    (0.694521114910 - 0.694521087360 : ℝ) < 0.0000002 ∧
    (0.645851069409 - 0.645851046701 : ℝ) < 0.0000002 ∧
    (0.571870113448 - 0.571870091125 : ℝ) < 0.0000002 ∧
    (0.538455320880 - 0.538455286605 : ℝ) < 0.0000002 ∧
    (0.513778355623 - 0.513778241424 : ℝ) < 0.0000002 ∧
    (0.999063289012 - 0.999063097443 : ℝ) < 0.0000002 ∧
    (0.836880514652 - 0.836880448106 : ℝ) < 0.0000002 ∧
    (0.723472932221 - 0.723472889305 : ℝ) < 0.0000002 ∧
    (0.666554281617 - 0.666554247837 : ℝ) < 0.0000002 ∧
    (0.578535607434 - 0.578535581419 : ℝ) < 0.0000002 ∧
    (0.540768228848 - 0.540768194762 : ℝ) < 0.0000002 ∧
    (0.519717513972 - 0.519717445589 : ℝ) < 0.0000002 := by
  norm_num

/-! ## Generic exact interval propagation -/

/-- Multiplicative correction in the paper's second-order approximation,
with `s = sigma^2`. -/
def correction2 (s S4 : ℝ) : ℝ :=
  1 - 1 / (6 * s) - 3 * S4 / (64 * s ^ 2)

def relativeLeadingResidual (density root : ℝ) : ℝ :=
  (density - 1 / 2) * root - 1

def relativeSecondResidual (density root correction : ℝ) : ℝ :=
  (density - 1 / 2) * root / correction - 1

/-- Symmetric displayed enclosure, interpreted with exact rational endpoints. -/
def InClaim (x center radius : ℝ) : Prop :=
  center - radius ≤ x ∧ x ≤ center + radius

/-- Convert rational square certificates to a square-root enclosure.  The
pi hypotheses are discharged below by `Real.pi_gt_d20` and `Real.pi_lt_d20`.
-/
theorem sqrt_two_pi_s_bounds
    {s sLo sHi rootLo rootHi piLo piHi : ℝ}
    (hsLoPos : 0 ≤ sLo) (hsLo : sLo ≤ s) (hsHi : s ≤ sHi)
    (hpiLo : piLo ≤ π) (hpiHi : π ≤ piHi)
    (hrootHi : 0 ≤ rootHi)
    (hrootLoSq : rootLo ^ 2 ≤ 2 * piLo * sLo)
    (hrootHiSq : 2 * piHi * sHi ≤ rootHi ^ 2) :
    rootLo ≤ √(2 * π * s) ∧ √(2 * π * s) ≤ rootHi := by
  have hpiNonneg : 0 ≤ π := Real.pi_pos.le
  have hsNonneg : 0 ≤ s := hsLoPos.trans hsLo
  have hLowerMul : piLo * sLo ≤ π * s := by
    exact mul_le_mul hpiLo hsLo hsLoPos hpiNonneg
  have hUpperMul : π * s ≤ piHi * sHi := by
    have hpiHiNonneg : 0 ≤ piHi := hpiNonneg.trans hpiHi
    exact mul_le_mul hpiHi hsHi hsNonneg hpiHiNonneg
  constructor
  · apply Real.le_sqrt_of_sq_le
    nlinarith
  · rw [Real.sqrt_le_iff]
    exact ⟨hrootHi, by nlinarith [hrootHiSq, hUpperMul]⟩

/-- The correction is increasing in `s` and decreasing in `S4` on the
positive region.  This lemma records the endpoint rule used by both checkers.
-/
theorem correction2_bounds
    {s sLo sHi S4 S4Lo S4Hi : ℝ}
    (hsLoPos : 0 < sLo) (hsLo : sLo ≤ s) (hsHi : s ≤ sHi)
    (hS4Lo : S4Lo ≤ S4) (hS4Hi : S4 ≤ S4Hi) (hS4LoNonneg : 0 ≤ S4Lo) :
    correction2 sLo S4Hi ≤ correction2 s S4 ∧
      correction2 s S4 ≤ correction2 sHi S4Lo := by
  have hsPos : 0 < s := hsLoPos.trans_le hsLo
  have hsHiPos : 0 < sHi := hsPos.trans_le hsHi
  have hS4Nonneg : 0 ≤ S4 := hS4LoNonneg.trans hS4Lo
  have hS4HiNonneg : 0 ≤ S4Hi := hS4Nonneg.trans hS4Hi
  constructor
  · unfold correction2
    have hrecip : 1 / (6 * s) ≤ 1 / (6 * sLo) := by
      gcongr
    have hfourth : S4 / s ^ 2 ≤ S4Hi / sLo ^ 2 := by
      gcongr
    have hscaled : 3 * S4 / (64 * s ^ 2) ≤ 3 * S4Hi / (64 * sLo ^ 2) := by
      calc
        3 * S4 / (64 * s ^ 2) = (3 / 64) * (S4 / s ^ 2) := by
          field_simp [ne_of_gt hsPos, ne_of_gt hsLoPos]
        _ ≤ (3 / 64) * (S4Hi / sLo ^ 2) :=
          mul_le_mul_of_nonneg_left hfourth (by norm_num)
        _ = 3 * S4Hi / (64 * sLo ^ 2) := by
          field_simp [ne_of_gt hsPos, ne_of_gt hsLoPos]
    linarith
  · unfold correction2
    have hrecip : 1 / (6 * sHi) ≤ 1 / (6 * s) := by
      gcongr
    have hfourth : S4Lo / sHi ^ 2 ≤ S4 / s ^ 2 := by
      gcongr
    have hscaled : 3 * S4Lo / (64 * sHi ^ 2) ≤ 3 * S4 / (64 * s ^ 2) := by
      calc
        3 * S4Lo / (64 * sHi ^ 2) = (3 / 64) * (S4Lo / sHi ^ 2) := by
          field_simp [ne_of_gt hsHiPos, ne_of_gt hsPos]
        _ ≤ (3 / 64) * (S4 / s ^ 2) :=
          mul_le_mul_of_nonneg_left hfourth (by norm_num)
        _ = 3 * S4 / (64 * s ^ 2) := by
          field_simp [ne_of_gt hsHiPos, ne_of_gt hsPos]
    linarith

/-- Monotone propagation through the leading relative residual. -/
theorem relativeLeadingResidual_bounds
    {d dLo dHi root rootLo rootHi : ℝ}
    (hdHalf : 1 / 2 ≤ dLo) (hdLo : dLo ≤ d) (hdHi : d ≤ dHi)
    (hrootNonneg : 0 ≤ rootLo) (hrootLo : rootLo ≤ root)
    (hrootHi : root ≤ rootHi) :
    relativeLeadingResidual dLo rootLo ≤ relativeLeadingResidual d root ∧
      relativeLeadingResidual d root ≤ relativeLeadingResidual dHi rootHi := by
  unfold relativeLeadingResidual
  have hdLoNonneg : 0 ≤ dLo - 1 / 2 := by linarith
  have hdNonneg : 0 ≤ d - 1 / 2 := by linarith
  have hdHiNonneg : 0 ≤ dHi - 1 / 2 := by linarith
  have hrootNonneg' : 0 ≤ root := hrootNonneg.trans hrootLo
  have hrootHiNonneg : 0 ≤ rootHi := hrootNonneg'.trans hrootHi
  constructor
  · gcongr
  · gcongr

/-- Monotone propagation through the second-order relative residual. -/
theorem relativeSecondResidual_bounds
    {d dLo dHi root rootLo rootHi c cLo cHi : ℝ}
    (hdHalf : 1 / 2 ≤ dLo) (hdLo : dLo ≤ d) (hdHi : d ≤ dHi)
    (hrootNonneg : 0 ≤ rootLo) (hrootLo : rootLo ≤ root)
    (hrootHi : root ≤ rootHi)
    (hcLoPos : 0 < cLo) (hcLo : cLo ≤ c) (hcHi : c ≤ cHi) :
    relativeSecondResidual dLo rootLo cHi ≤ relativeSecondResidual d root c ∧
      relativeSecondResidual d root c ≤ relativeSecondResidual dHi rootHi cLo := by
  unfold relativeSecondResidual
  have hdLoNonneg : 0 ≤ dLo - 1 / 2 := by linarith
  have hdNonneg : 0 ≤ d - 1 / 2 := by linarith
  have hdHiNonneg : 0 ≤ dHi - 1 / 2 := by linarith
  have hrootNonneg' : 0 ≤ root := hrootNonneg.trans hrootLo
  have hrootHiNonneg : 0 ≤ rootHi := hrootNonneg'.trans hrootHi
  have hnumLoNonneg : 0 ≤ (dLo - 1 / 2) * rootLo := mul_nonneg hdLoNonneg hrootNonneg
  have hnumNonneg : 0 ≤ (d - 1 / 2) * root := mul_nonneg hdNonneg hrootNonneg'
  have hnumHiNonneg : 0 ≤ (dHi - 1 / 2) * rootHi := mul_nonneg hdHiNonneg hrootHiNonneg
  have hcPos : 0 < c := hcLoPos.trans_le hcLo
  have hcHiPos : 0 < cHi := hcPos.trans_le hcHi
  constructor
  · gcongr
  · gcongr

/-! ## Instantiated square-root certificates

These are the four irrational steps in the post-processing table.  The
variance intervals remain hypotheses; the pi bounds and all rational square
comparisons are discharged inside Lean.
-/

theorem q4_m8_sqrt_certificate (s : ℝ)
    (hlo : 29.7124677146037 ≤ s) (hhi : s ≤ 29.7124677146038) :
    (13.6634161388887 : ℝ) ≤ √(2 * π * s) ∧
      √(2 * π * s) ≤ (13.6634161388889 : ℝ) := by
  apply sqrt_two_pi_s_bounds (sLo := 29.7124677146037)
    (sHi := 29.7124677146038) (piLo := 3.14159265358979323846)
    (piHi := 3.14159265358979323847)
  · norm_num
  · exact hlo
  · exact hhi
  · exact Real.pi_gt_d20.le
  · exact Real.pi_lt_d20.le
  · norm_num
  · norm_num
  · norm_num

theorem q4_m20_sqrt_certificate (s : ℝ)
    (hlo : 106.3259996464375 ≤ s) (hhi : s ≤ 106.3259996464376) :
    (25.8469719454654 : ℝ) ≤ √(2 * π * s) ∧
      √(2 * π * s) ≤ (25.8469719454655 : ℝ) := by
  apply sqrt_two_pi_s_bounds (sLo := 106.3259996464375)
    (sHi := 106.3259996464376) (piLo := 3.14159265358979323846)
    (piHi := 3.14159265358979323847)
  · norm_num
  · exact hlo
  · exact hhi
  · exact Real.pi_gt_d20.le
  · exact Real.pi_lt_d20.le
  · norm_num
  · norm_num
  · norm_num

theorem q4_m100_sqrt_certificate (s : ℝ)
    (hlo : 836.8743838883749 ≤ s) (hhi : s ≤ 836.8743838883750) :
    (72.5137010005861 : ℝ) ≤ √(2 * π * s) ∧
      √(2 * π * s) ≤ (72.5137010005862 : ℝ) := by
  apply sqrt_two_pi_s_bounds (sLo := 836.8743838883749)
    (sHi := 836.8743838883750) (piLo := 3.14159265358979323846)
    (piHi := 3.14159265358979323847)
  · norm_num
  · exact hlo
  · exact hhi
  · exact Real.pi_gt_d20.le
  · exact Real.pi_lt_d20.le
  · norm_num
  · norm_num
  · norm_num

theorem q3_m60_sqrt_certificate (s : ℝ)
    (hlo : 407.9701181293456 ≤ s) (hhi : s ≤ 407.9701181293457) :
    (50.6295551234516 : ℝ) ≤ √(2 * π * s) ∧
      √(2 * π * s) ≤ (50.6295551234517 : ℝ) := by
  apply sqrt_two_pi_s_bounds (sLo := 407.9701181293456)
    (sHi := 407.9701181293457) (piLo := 3.14159265358979323846)
    (piHi := 3.14159265358979323847)
  · norm_num
  · exact hlo
  · exact hhi
  · exact Real.pi_gt_d20.le
  · exact Real.pi_lt_d20.le
  · norm_num
  · norm_num
  · norm_num

/-! ## Instantiated leading and second-order residual enclosures -/

theorem q4_m8_residual_claims
    (density s S4 : ℝ)
    (hdLo : 0.571870091125 ≤ density) (hdHi : density ≤ 0.571870113448)
    (hsLo : 29.7124677146037 ≤ s) (hsHi : s ≤ 29.7124677146038)
    (hS4Lo : 219.8279681583051 ≤ S4) (hS4Hi : S4 ≤ 219.8279681583052) :
    InClaim (relativeLeadingResidual density (√(2 * π * s)))
        (-0.018008885) 0.00000016 ∧
      InClaim (relativeSecondResidual density (√(2 * π * s)) (correction2 s S4))
        (-0.0007403203) 0.00000016 := by
  have hroot := q4_m8_sqrt_certificate s hsLo hsHi
  have hcorr := correction2_bounds (s := s) (S4 := S4)
    (sLo := 29.7124677146037) (sHi := 29.7124677146038)
    (S4Lo := 219.8279681583051) (S4Hi := 219.8279681583052)
    (by norm_num) hsLo hsHi hS4Lo hS4Hi (by norm_num)
  have hlead := relativeLeadingResidual_bounds
    (d := density) (dLo := 0.571870091125) (dHi := 0.571870113448)
    (root := √(2 * π * s)) (rootLo := 13.6634161388887)
    (rootHi := 13.6634161388889) (by norm_num) hdLo hdHi (by norm_num) hroot.1 hroot.2
  have hsecond := relativeSecondResidual_bounds
    (d := density) (dLo := 0.571870091125) (dHi := 0.571870113448)
    (root := √(2 * π * s)) (rootLo := 13.6634161388887)
    (rootHi := 13.6634161388889) (c := correction2 s S4)
    (cLo := correction2 29.7124677146037 219.8279681583052)
    (cHi := correction2 29.7124677146038 219.8279681583051)
    (by norm_num) hdLo hdHi (by norm_num) hroot.1 hroot.2
    (by norm_num [correction2]) hcorr.1 hcorr.2
  constructor
  · constructor <;> norm_num [InClaim, relativeLeadingResidual] at * <;> linarith
  · constructor <;> norm_num [InClaim, relativeSecondResidual, correction2] at * <;> linarith

theorem q4_m20_residual_claims
    (density s S4 : ℝ)
    (hdLo : 0.538455286605 ≤ density) (hdHi : density ≤ 0.538455320880)
    (hsLo : 106.3259996464375 ≤ s) (hsHi : s ≤ 106.3259996464376)
    (hS4Lo : 1061.3175563225463 ≤ S4) (hS4Hi : S4 ≤ 1061.3175563225464) :
    InClaim (relativeLeadingResidual density (√(2 * π * s)))
        (-0.006046843) 0.00000045 ∧
      InClaim (relativeSecondResidual density (√(2 * π * s)) (correction2 s S4))
        (-0.00007925247) 0.00000045 := by
  have hroot := q4_m20_sqrt_certificate s hsLo hsHi
  have hcorr := correction2_bounds (s := s) (S4 := S4)
    (sLo := 106.3259996464375) (sHi := 106.3259996464376)
    (S4Lo := 1061.3175563225463) (S4Hi := 1061.3175563225464)
    (by norm_num) hsLo hsHi hS4Lo hS4Hi (by norm_num)
  have hlead := relativeLeadingResidual_bounds
    (d := density) (dLo := 0.538455286605) (dHi := 0.538455320880)
    (root := √(2 * π * s)) (rootLo := 25.8469719454654)
    (rootHi := 25.8469719454655) (by norm_num) hdLo hdHi (by norm_num) hroot.1 hroot.2
  have hsecond := relativeSecondResidual_bounds
    (d := density) (dLo := 0.538455286605) (dHi := 0.538455320880)
    (root := √(2 * π * s)) (rootLo := 25.8469719454654)
    (rootHi := 25.8469719454655) (c := correction2 s S4)
    (cLo := correction2 106.3259996464375 1061.3175563225464)
    (cHi := correction2 106.3259996464376 1061.3175563225463)
    (by norm_num) hdLo hdHi (by norm_num) hroot.1 hroot.2
    (by norm_num [correction2]) hcorr.1 hcorr.2
  constructor
  · constructor <;> norm_num [InClaim, relativeLeadingResidual] at * <;> linarith
  · constructor <;> norm_num [InClaim, relativeSecondResidual, correction2] at * <;> linarith

theorem q4_m100_residual_claims
    (density s S4 : ℝ)
    (hdLo : 0.513778241424 ≤ density) (hdHi : density ≤ 0.513778355623)
    (hsLo : 836.8743838883749 ≤ s) (hsHi : s ≤ 836.8743838883750)
    (hS4Lo : 10190.01548744683 ≤ S4) (hS4Hi : S4 ≤ 10190.01548744684) :
    InClaim (relativeLeadingResidual density (√(2 * π * s)))
        (-0.0008845806) 0.0000042 ∧
      InClaim (relativeSecondResidual density (√(2 * π * s)) (correction2 s S4))
        (-0.000003412243) 0.0000042 := by
  have hroot := q4_m100_sqrt_certificate s hsLo hsHi
  have hcorr := correction2_bounds (s := s) (S4 := S4)
    (sLo := 836.8743838883749) (sHi := 836.8743838883750)
    (S4Lo := 10190.01548744683) (S4Hi := 10190.01548744684)
    (by norm_num) hsLo hsHi hS4Lo hS4Hi (by norm_num)
  have hlead := relativeLeadingResidual_bounds
    (d := density) (dLo := 0.513778241424) (dHi := 0.513778355623)
    (root := √(2 * π * s)) (rootLo := 72.5137010005861)
    (rootHi := 72.5137010005862) (by norm_num) hdLo hdHi (by norm_num) hroot.1 hroot.2
  have hsecond := relativeSecondResidual_bounds
    (d := density) (dLo := 0.513778241424) (dHi := 0.513778355623)
    (root := √(2 * π * s)) (rootLo := 72.5137010005861)
    (rootHi := 72.5137010005862) (c := correction2 s S4)
    (cLo := correction2 836.8743838883749 10190.01548744684)
    (cHi := correction2 836.8743838883750 10190.01548744683)
    (by norm_num) hdLo hdHi (by norm_num) hroot.1 hroot.2
    (by norm_num [correction2]) hcorr.1 hcorr.2
  constructor
  · constructor <;> norm_num [InClaim, relativeLeadingResidual] at * <;> linarith
  · constructor <;> norm_num [InClaim, relativeSecondResidual, correction2] at * <;> linarith

theorem q3_m60_residual_claims
    (density s S4 : ℝ)
    (hdLo : 0.519717445589 ≤ density) (hdHi : density ≤ 0.519717513972)
    (hsLo : 407.9701181293456 ≤ s) (hsHi : s ≤ 407.9701181293457)
    (hS4Lo : 4607.562686389960 ≤ S4) (hS4Hi : S4 ≤ 4607.562686389961) :
    InClaim (relativeLeadingResidual density (√(2 * π * s)))
        (-0.001712771) 0.0000018 ∧
      InClaim (relativeSecondResidual density (√(2 * π * s)) (correction2 s S4))
        (-0.000006610401) 0.0000018 := by
  have hroot := q3_m60_sqrt_certificate s hsLo hsHi
  have hcorr := correction2_bounds (s := s) (S4 := S4)
    (sLo := 407.9701181293456) (sHi := 407.9701181293457)
    (S4Lo := 4607.562686389960) (S4Hi := 4607.562686389961)
    (by norm_num) hsLo hsHi hS4Lo hS4Hi (by norm_num)
  have hlead := relativeLeadingResidual_bounds
    (d := density) (dLo := 0.519717445589) (dHi := 0.519717513972)
    (root := √(2 * π * s)) (rootLo := 50.6295551234516)
    (rootHi := 50.6295551234517) (by norm_num) hdLo hdHi (by norm_num) hroot.1 hroot.2
  have hsecond := relativeSecondResidual_bounds
    (d := density) (dLo := 0.519717445589) (dHi := 0.519717513972)
    (root := √(2 * π * s)) (rootLo := 50.6295551234516)
    (rootHi := 50.6295551234517) (c := correction2 s S4)
    (cLo := correction2 407.9701181293456 4607.562686389961)
    (cHi := correction2 407.9701181293457 4607.562686389960)
    (by norm_num) hdLo hdHi (by norm_num) hroot.1 hroot.2
    (by norm_num [correction2]) hcorr.1 hcorr.2
  constructor
  · constructor <;> norm_num [InClaim, relativeLeadingResidual] at * <;> linarith
  · constructor <;> norm_num [InClaim, relativeSecondResidual, correction2] at * <;> linarith

end

end WeightedPrimeRaces.DensityPostprocessing
