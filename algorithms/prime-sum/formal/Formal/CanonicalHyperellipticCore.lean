import Mathlib

set_option linter.style.header false

/-!
# Elementary core of the canonical hyperelliptic critical scaling

This file checks only the real algebra and asymptotic calculus used in the
critical normalization.  It deliberately does not formalize hyperelliptic
curves, Frobenius, linear independence, equidistribution, random matrices, or
the marked point-process limit.
-/

namespace CanonicalHyperellipticCore

open Filter Real
open scoped Topology

noncomputable section

/-- The critical radius `r = exp(lambda / d)`. -/
def criticalRadius (lambda d : ℝ) : ℝ :=
  Real.exp (lambda / d)

/-- Square-prime center on even degree endpoints. -/
def evenParityCenter (lambda d : ℝ) : ℝ :=
  2 * criticalRadius lambda d / (criticalRadius lambda d + 1)

/-- Square-prime center on odd degree endpoints. -/
def oddParityCenter (lambda d : ℝ) : ℝ :=
  2 / (criticalRadius lambda d + 1)

/-- The exact one-pair amplitude after substituting
`theta = 2 * pi * y / d` and `r = exp(lambda / d)` in equation (2.3). -/
def criticalAmplitude (lambda y d : ℝ) : ℝ :=
  let rho := Real.exp (-lambda / d)
  4 * (1 - rho) /
    Real.sqrt ((1 - rho) ^ 2 + 4 * rho * Real.sin (π * y / d) ^ 2)

/-- The limiting hard-edge coefficient. -/
def hardEdgeAmplitude (lambda y : ℝ) : ℝ :=
  4 * lambda / Real.sqrt (lambda ^ 2 + (2 * π * y) ^ 2)

/-! ## Exact finite algebra -/

/-- The geometric-series identity behind the endpoint normalization. -/
theorem geometric_block_identity (r : ℝ) (n : ℕ) :
    (r ^ 2 - 1) * (∑ k ∈ Finset.range n, (r ^ 2) ^ k) = (r ^ 2) ^ n - 1 := by
  simpa only [mul_comm] using mul_geom_sum (r ^ 2) n

/-- Exact trigonometric conversion from the cosine denominator in (2.3) to
the nonnegative sine-square form used in the limit proof. -/
theorem cosine_denominator_eq_sine (rho x : ℝ) :
    1 + rho ^ 2 - 2 * rho * Real.cos (2 * x) =
      (1 - rho) ^ 2 + 4 * rho * Real.sin x ^ 2 := by
  rw [Real.cos_two_mul]
  nlinarith [Real.sin_sq_add_cos_sq x]

/-- The two parity centers add to exactly two before taking any limit. -/
theorem parityCenters_add (lambda d : ℝ)
    (h : criticalRadius lambda d + 1 ≠ 0) :
    evenParityCenter lambda d + oddParityCenter lambda d = 2 := by
  unfold evenParityCenter oddParityCenter
  field_simp [h]

/-! ## Radius and parity-center limits -/

theorem tendsto_criticalRadius_atTop (lambda : ℝ) :
    Tendsto (criticalRadius lambda) atTop (nhds 1) := by
  change Tendsto (fun d : ℝ ↦ Real.exp (lambda / d)) atTop (nhds 1)
  have hinv : Tendsto (fun d : ℝ ↦ d⁻¹) atTop (nhds 0) := tendsto_inv_atTop_zero
  have harg : Tendsto (fun d : ℝ ↦ lambda / d) atTop (nhds 0) := by
    simpa only [div_eq_mul_inv, mul_zero] using tendsto_const_nhds.mul hinv
  convert Real.continuous_exp.continuousAt.tendsto.comp harg using 1
  · rfl
  · simp

theorem tendsto_evenParityCenter_atTop (lambda : ℝ) :
    Tendsto (evenParityCenter lambda) atTop (nhds 1) := by
  change Tendsto
    (fun d : ℝ ↦ 2 * criticalRadius lambda d / (criticalRadius lambda d + 1))
    atTop (nhds 1)
  have hr := tendsto_criticalRadius_atTop lambda
  convert
    ((tendsto_const_nhds : Tendsto (fun _ : ℝ ↦ (2 : ℝ)) atTop (nhds 2)).mul hr).div
      (hr.add tendsto_const_nhds) (by norm_num : (1 : ℝ) + 1 ≠ 0) using 1
  · rfl
  · norm_num

theorem tendsto_oddParityCenter_atTop (lambda : ℝ) :
    Tendsto (oddParityCenter lambda) atTop (nhds 1) := by
  change Tendsto (fun d : ℝ ↦ 2 / (criticalRadius lambda d + 1)) atTop (nhds 1)
  have hr := tendsto_criticalRadius_atTop lambda
  convert
    (tendsto_const_nhds : Tendsto (fun _ : ℝ ↦ (2 : ℝ)) atTop (nhds 2)).div
      (hr.add tendsto_const_nhds) (by norm_num : (1 : ℝ) + 1 ≠ 0) using 1
  · rfl
  · norm_num

/-! ## First-order analytic inputs -/

/-- First-order normalization of `1 - exp (-lambda t)` from the right. -/
theorem tendsto_one_sub_exp_neg_div (lambda : ℝ) :
    Tendsto (fun t : ℝ ↦ (1 - Real.exp (-lambda * t)) / t)
      (nhdsWithin 0 (Set.Ioi 0)) (nhds lambda) := by
  have hderiv : HasDerivAt (fun t : ℝ ↦ 1 - Real.exp (-lambda * t)) lambda 0 := by
    convert! (((hasDerivAt_id (0 : ℝ)).const_mul (-lambda)).exp.const_sub 1) using 1
    all_goals simp
  simpa [smul_eq_mul, div_eq_mul_inv, mul_comm] using hderiv.tendsto_slope_zero_right

/-- First-order normalization of `sin (pi y t)` from the right. -/
theorem tendsto_sin_pi_mul_div (y : ℝ) :
    Tendsto (fun t : ℝ ↦ Real.sin (π * y * t) / t)
      (nhdsWithin 0 (Set.Ioi 0)) (nhds (π * y)) := by
  have hderiv : HasDerivAt (fun t : ℝ ↦ Real.sin (π * y * t)) (π * y) 0 := by
    convert! ((hasDerivAt_id (0 : ℝ)).const_mul (π * y)).sin using 1
    all_goals simp
  simpa [smul_eq_mul, div_eq_mul_inv, mul_comm] using
    hderiv.tendsto_slope_zero_right

/-! ## Critical amplitude limit -/

/-- For positive scale `t`, division by `t` removes the common vanishing
factor from the exact amplitude. -/
theorem criticalAmplitude_inv_eq_normalized {lambda y d : ℝ} (hd : 0 < d) :
    criticalAmplitude lambda y d =
      4 * ((1 - Real.exp (-lambda / d)) / d⁻¹) /
        Real.sqrt
          (((1 - Real.exp (-lambda / d)) / d⁻¹) ^ 2 +
            4 * Real.exp (-lambda / d) *
              (Real.sin (π * y / d) / d⁻¹) ^ 2) := by
  have ht : 0 < d⁻¹ := inv_pos.mpr hd
  have hbase :
      0 ≤ (1 - Real.exp (-lambda / d)) ^ 2 +
        4 * Real.exp (-lambda / d) * Real.sin (π * y / d) ^ 2 := by
    positivity
  have hinside :
      ((1 - Real.exp (-lambda / d)) / d⁻¹) ^ 2 +
          4 * Real.exp (-lambda / d) *
            (Real.sin (π * y / d) / d⁻¹) ^ 2 =
        ((1 - Real.exp (-lambda / d)) ^ 2 +
          4 * Real.exp (-lambda / d) * Real.sin (π * y / d) ^ 2) /
          (d⁻¹) ^ 2 := by
    field_simp [ht.ne']
  unfold criticalAmplitude
  rw [hinside, Real.sqrt_div hbase, Real.sqrt_sq_eq_abs, abs_of_pos ht]
  rw [← mul_div_assoc, div_div_div_cancel_right₀ ht.ne']

/-- The exact critical one-pair amplitude converges to the symplectic
hard-edge coefficient for fixed `lambda > 0` and fixed `y ≥ 0`. -/
theorem tendsto_criticalAmplitude_atTop {lambda y : ℝ}
    (hlambda : 0 < lambda) (_hy : 0 ≤ y) :
    Tendsto (criticalAmplitude lambda y) atTop
      (nhds (hardEdgeAmplitude lambda y)) := by
  have hinvWithin :
      Tendsto (fun d : ℝ ↦ d⁻¹) atTop (nhdsWithin 0 (Set.Ioi 0)) := by
    rw [tendsto_nhdsWithin_iff]
    refine ⟨tendsto_inv_atTop_zero, ?_⟩
    filter_upwards [eventually_gt_atTop (0 : ℝ)] with d hd
    exact inv_pos.mpr hd
  have hA :
      Tendsto
        (fun d : ℝ ↦ (1 - Real.exp (-lambda / d)) / d⁻¹)
        atTop (nhds lambda) := by
    convert (tendsto_one_sub_exp_neg_div lambda).comp hinvWithin using 1
    rfl
  have hS :
      Tendsto (fun d : ℝ ↦ Real.sin (π * y / d) / d⁻¹)
        atTop (nhds (π * y)) := by
    convert (tendsto_sin_pi_mul_div y).comp hinvWithin using 1
    rfl
  have hRho :
      Tendsto (fun d : ℝ ↦ Real.exp (-lambda / d)) atTop (nhds 1) := by
    convert tendsto_criticalRadius_atTop (-lambda) using 1
    rfl
  have hdenSq :
      Tendsto
        (fun d : ℝ ↦
          ((1 - Real.exp (-lambda / d)) / d⁻¹) ^ 2 +
            4 * Real.exp (-lambda / d) *
              (Real.sin (π * y / d) / d⁻¹) ^ 2)
        atTop (nhds (lambda ^ 2 + (2 * π * y) ^ 2)) := by
    convert (hA.pow 2).add
      (((tendsto_const_nhds : Tendsto (fun _ : ℝ ↦ (4 : ℝ)) atTop (nhds 4)).mul hRho).mul
        (hS.pow 2)) using 1
    ring_nf
  have hden :
      Tendsto
        (fun d : ℝ ↦ Real.sqrt
          (((1 - Real.exp (-lambda / d)) / d⁻¹) ^ 2 +
            4 * Real.exp (-lambda / d) *
              (Real.sin (π * y / d) / d⁻¹) ^ 2))
        atTop (nhds (Real.sqrt (lambda ^ 2 + (2 * π * y) ^ 2))) := by
    convert Real.continuous_sqrt.continuousAt.tendsto.comp hdenSq using 1
    rfl
  have hlimitDenPos : 0 < Real.sqrt (lambda ^ 2 + (2 * π * y) ^ 2) := by
    apply Real.sqrt_pos.2
    nlinarith [sq_pos_of_pos hlambda, sq_nonneg (2 * π * y)]
  have hnormalized :
      Tendsto
        (fun d : ℝ ↦
          4 * ((1 - Real.exp (-lambda / d)) / d⁻¹) /
            Real.sqrt
              (((1 - Real.exp (-lambda / d)) / d⁻¹) ^ 2 +
                4 * Real.exp (-lambda / d) *
                  (Real.sin (π * y / d) / d⁻¹) ^ 2))
        atTop (nhds (hardEdgeAmplitude lambda y)) := by
    unfold hardEdgeAmplitude
    convert
      ((tendsto_const_nhds : Tendsto (fun _ : ℝ ↦ (4 : ℝ)) atTop (nhds 4)).mul hA).div
        hden hlimitDenPos.ne' using 1
    rfl
  apply hnormalized.congr'
  filter_upwards [eventually_gt_atTop (0 : ℝ)] with d hd
  exact (criticalAmplitude_inv_eq_normalized hd).symm

end

end CanonicalHyperellipticCore
