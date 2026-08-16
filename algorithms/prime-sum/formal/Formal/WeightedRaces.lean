import Mathlib.Analysis.SpecialFunctions.Integrals.Basic
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.Ring

set_option linter.style.header false

/-!
# Machine-checked algebra for weighted prime races

This file formalizes a deliberately limited, auditable layer of the paper:

* the finite-zero amplitude, variance, and derivative identities;
* the termwise fourth- and sixth-amplitude identities;
* exact second and fourth moments of a uniform cosine phase;
* fourth-cumulant arithmetic and the finite-sum moment bounds used in the paper;
* the critical rescaling identity (at the level of squared amplitudes);
* the one-zero threshold and profile algebra; and
* the Gaussian-moment arithmetic behind the displayed third-order coefficients.

It does **not** formalize GRH, LI, zero completeness, infinite products or series,
limit theorems, Fourier inversion bounds, or interval-arithmetic certificates.
There are no axioms and no `sorry` declarations in this project.
-/

namespace WeightedPrimeRaces

open scoped Interval
open Real

noncomputable section

/-! ## Amplitude and variance algebra -/

/-- Contribution of one positive zero ordinate to the variance in the paper's
normalization, with `M = m + 1/2`. -/
def varianceTerm (M gamma : ℝ) : ℝ :=
  8 * M ^ 2 / (M ^ 2 + gamma ^ 2)

/-- Derivative of `varianceTerm` with respect to `M`. -/
def varianceDerivativeTerm (M gamma : ℝ) : ℝ :=
  16 * M * gamma ^ 2 / (M ^ 2 + gamma ^ 2) ^ 2

/-- Square of the doubled amplitude `2 a_gamma = 4M / sqrt(M^2+gamma^2)`. -/
def doubledAmplitudeSquared (M gamma : ℝ) : ℝ :=
  16 * M ^ 2 / (M ^ 2 + gamma ^ 2)

/-- The square-root definition of the doubled amplitude. -/
def doubledAmplitude (M gamma : ℝ) : ℝ :=
  4 * M / Real.sqrt (M ^ 2 + gamma ^ 2)

theorem doubledAmplitude_sq (M gamma : ℝ) (hden : 0 < M ^ 2 + gamma ^ 2) :
    doubledAmplitude M gamma ^ 2 = doubledAmplitudeSquared M gamma := by
  unfold doubledAmplitude doubledAmplitudeSquared
  rw [div_pow, Real.sq_sqrt hden.le]
  ring

theorem doubledAmplitudeSquared_nonneg (M gamma : ℝ) :
    0 ≤ doubledAmplitudeSquared M gamma := by
  unfold doubledAmplitudeSquared
  positivity

theorem doubledAmplitudeSquared_le_sixteen (M gamma : ℝ)
    (hden : 0 < M ^ 2 + gamma ^ 2) : doubledAmplitudeSquared M gamma ≤ 16 := by
  unfold doubledAmplitudeSquared
  rw [div_le_iff₀ hden]
  nlinarith [sq_nonneg gamma]

theorem varianceTerm_eq_half_doubledAmplitudeSquared (M gamma : ℝ) :
    varianceTerm M gamma = doubledAmplitudeSquared M gamma / 2 := by
  unfold varianceTerm doubledAmplitudeSquared
  ring

/-- Fourth power of the doubled amplitude `2 a_gamma`. -/
def fourthAmplitudeTerm (M gamma : ℝ) : ℝ :=
  256 * M ^ 4 / (M ^ 2 + gamma ^ 2) ^ 2

/-- Sixth power of the doubled amplitude `2 a_gamma`. -/
def sixthAmplitudeTerm (M gamma : ℝ) : ℝ :=
  4096 * M ^ 6 / (M ^ 2 + gamma ^ 2) ^ 3

/-- The summand in the second logarithmic derivative of the completed
L-function's Hadamard product. -/
def logXiSecondTerm (M gamma : ℝ) : ℝ :=
  2 * (gamma ^ 2 - M ^ 2) / (M ^ 2 + gamma ^ 2) ^ 2

/-- The summand in the third logarithmic derivative of the completed
L-function's Hadamard product. -/
def logXiThirdTerm (M gamma : ℝ) : ℝ :=
  -12 * M / (M ^ 2 + gamma ^ 2) ^ 2 +
    16 * M ^ 3 / (M ^ 2 + gamma ^ 2) ^ 3

theorem fourth_amplitude_term_identity (M gamma : ℝ)
    (h : M ^ 2 + gamma ^ 2 ≠ 0) :
    16 * varianceTerm M gamma - 64 * M ^ 2 * logXiSecondTerm M gamma =
      fourthAmplitudeTerm M gamma := by
  unfold varianceTerm logXiSecondTerm fourthAmplitudeTerm
  field_simp [h]
  ring

theorem sixth_amplitude_term_identity (M gamma : ℝ)
    (h : M ^ 2 + gamma ^ 2 ≠ 0) :
    12 * fourthAmplitudeTerm M gamma + 256 * M ^ 3 * logXiThirdTerm M gamma =
      sixthAmplitudeTerm M gamma := by
  unfold fourthAmplitudeTerm logXiThirdTerm sixthAmplitudeTerm
  field_simp [h]
  ring

theorem hasDerivAt_varianceTerm (M gamma : ℝ)
    (h : M ^ 2 + gamma ^ 2 ≠ 0) :
    HasDerivAt (fun x : ℝ => varianceTerm x gamma)
      (varianceDerivativeTerm M gamma) M := by
  unfold varianceTerm varianceDerivativeTerm
  have hnum : HasDerivAt (fun x : ℝ => 8 * x ^ 2) (16 * M) M := by
    convert! (hasDerivAt_const M (8 : ℝ)).mul ((hasDerivAt_id M).pow 2) using 1
    simp only [id_eq]
    ring
  have hden : HasDerivAt (fun x : ℝ => x ^ 2 + gamma ^ 2) (2 * M) M := by
    convert! ((hasDerivAt_id M).pow 2).add (hasDerivAt_const M (gamma ^ 2)) using 1
    simp only [id_eq]
    ring
  convert! hnum.div hden h using 1
  field_simp [h]
  ring

theorem varianceDerivativeTerm_pos (M gamma : ℝ) (hM : 0 < M)
    (hgamma : gamma ≠ 0) : 0 < varianceDerivativeTerm M gamma := by
  unfold varianceDerivativeTerm
  positivity

/-- Squared critical-scaling identity. Taking `c = log q` and
`gamma * c = 2 * pi * y` is the algebraic content of equation
`critical-amplitude` without introducing square-root side conditions. -/
theorem critical_squared_amplitude_rescaling (M gamma c : ℝ) (hc : c ≠ 0) :
    (4 * M) ^ 2 / (M ^ 2 + gamma ^ 2) =
      (4 * (M * c)) ^ 2 / ((M * c) ^ 2 + (gamma * c) ^ 2) := by
  have hc2 : c ^ 2 ≠ 0 := pow_ne_zero 2 hc
  by_cases hden : M ^ 2 + gamma ^ 2 = 0
  · have hM : M = 0 := by nlinarith [sq_nonneg M, sq_nonneg gamma]
    simp [hM]
  · field_simp [hden, hc2]

/-! ## Uniform cosine moments and fourth cumulants -/

/-- Normalized Lebesgue moment of a uniform phase on `[0, 2*pi]`. -/
def uniformCosMoment (n : ℕ) : ℝ :=
  (∫ theta in (0 : ℝ)..2 * π, Real.cos theta ^ n) / (2 * π)

theorem uniformCosMoment_zero : uniformCosMoment 0 = 1 := by
  simp [uniformCosMoment, Real.pi_ne_zero]

theorem uniformCosMoment_one : uniformCosMoment 1 = 0 := by
  simp [uniformCosMoment, integral_cos]

theorem uniformCosMoment_two : uniformCosMoment 2 = 1 / 2 := by
  simp [uniformCosMoment, integral_cos_sq]
  field_simp [Real.pi_ne_zero]

theorem uniformCosMoment_four : uniformCosMoment 4 = 3 / 8 := by
  rw [uniformCosMoment, show 4 = 2 + 2 by norm_num, integral_cos_pow]
  simp [integral_cos_sq]
  field_simp [Real.pi_ne_zero]
  norm_num

/-- Exact second moment of the scaled cosine `b cos(theta)`. -/
theorem scaled_uniform_cos_second_moment (b : ℝ) :
    (∫ theta in (0 : ℝ)..2 * π, (b * Real.cos theta) ^ 2) / (2 * π) =
      b ^ 2 / 2 := by
  simp_rw [mul_pow]
  rw [intervalIntegral.integral_const_mul, integral_cos_sq]
  simp
  field_simp [Real.pi_ne_zero]

/-- Exact fourth moment of the scaled cosine `b cos(theta)`. -/
theorem scaled_uniform_cos_fourth_moment (b : ℝ) :
    (∫ theta in (0 : ℝ)..2 * π, (b * Real.cos theta) ^ 4) / (2 * π) =
      3 * b ^ 4 / 8 := by
  simp_rw [mul_pow]
  rw [intervalIntegral.integral_const_mul, show 4 = 2 + 2 by norm_num, integral_cos_pow]
  simp [integral_cos_sq]
  field_simp [Real.pi_ne_zero]
  ring

/-- Fourth cumulant expressed from the second and fourth central moments. -/
def fourthCumulant (secondMoment fourthMoment : ℝ) : ℝ :=
  fourthMoment - 3 * secondMoment ^ 2

theorem scaled_uniform_cos_fourthCumulant (b : ℝ) :
    fourthCumulant (b ^ 2 / 2) (3 * b ^ 4 / 8) = -3 * b ^ 4 / 8 := by
  unfold fourthCumulant
  ring

theorem scaled_uniform_cos_fourthCumulant_neg {b : ℝ} (hb : b ≠ 0) :
    fourthCumulant (b ^ 2 / 2) (3 * b ^ 4 / 8) < 0 := by
  rw [scaled_uniform_cos_fourthCumulant]
  have hb4 : 0 < b ^ 4 := by positivity
  nlinarith

/-! ## Finite amplitude moment bookkeeping -/

section FiniteMoments

variable {Index : Type*}

def finiteVariance (s : Finset Index) (b : Index → ℝ) : ℝ :=
  (∑ i ∈ s, b i ^ 2) / 2

def finiteFourthMomentSum (s : Finset Index) (b : Index → ℝ) : ℝ :=
  ∑ i ∈ s, b i ^ 4

def finiteSixthMomentSum (s : Finset Index) (b : Index → ℝ) : ℝ :=
  ∑ i ∈ s, b i ^ 6

def finiteEighthMomentSum (s : Finset Index) (b : Index → ℝ) : ℝ :=
  ∑ i ∈ s, b i ^ 8

/-- Variance contributed by a finite list of zero ordinates. -/
def finiteZeroVariance (s : Finset Index) (gamma : Index → ℝ) (M : ℝ) : ℝ :=
  ∑ i ∈ s, varianceTerm M (gamma i)

/-- Derivative of the finite-zero variance. -/
def finiteZeroVarianceDerivative (s : Finset Index) (gamma : Index → ℝ) (M : ℝ) : ℝ :=
  ∑ i ∈ s, varianceDerivativeTerm M (gamma i)

theorem hasDerivAt_finiteZeroVariance (s : Finset Index) (gamma : Index → ℝ) (M : ℝ)
    (hden : ∀ i ∈ s, M ^ 2 + gamma i ^ 2 ≠ 0) :
    HasDerivAt (finiteZeroVariance s gamma) (finiteZeroVarianceDerivative s gamma M) M := by
  unfold finiteZeroVariance finiteZeroVarianceDerivative
  convert! (HasDerivAt.sum fun i hi =>
    hasDerivAt_varianceTerm M (gamma i) (hden i hi)) using 1
  funext x
  simp

theorem finite_fourth_le_thirty_two_variance (s : Finset Index) (b : Index → ℝ)
    (hb : ∀ i ∈ s, b i ^ 2 ≤ 16) :
    finiteFourthMomentSum s b ≤ 32 * finiteVariance s b := by
  have hterm : ∀ i ∈ s, b i ^ 4 ≤ 16 * b i ^ 2 := by
    intro i hi
    calc
      b i ^ 4 = b i ^ 2 * b i ^ 2 := by ring
      _ ≤ 16 * b i ^ 2 := mul_le_mul_of_nonneg_right (hb i hi) (sq_nonneg (b i))
  calc
    finiteFourthMomentSum s b ≤ ∑ i ∈ s, 16 * b i ^ 2 :=
      Finset.sum_le_sum hterm
    _ = 32 * finiteVariance s b := by
      unfold finiteVariance
      rw [show 32 * ((∑ i ∈ s, b i ^ 2) / 2) = (∑ i ∈ s, b i ^ 2) * 16 by ring]
      rw [Finset.sum_mul]
      apply Finset.sum_congr rfl
      intro i hi
      ring

theorem finite_sixth_le_sixteen_fourth (s : Finset Index) (b : Index → ℝ)
    (hb : ∀ i ∈ s, b i ^ 2 ≤ 16) :
    finiteSixthMomentSum s b ≤ 16 * finiteFourthMomentSum s b := by
  have hterm : ∀ i ∈ s, b i ^ 6 ≤ 16 * b i ^ 4 := by
    intro i hi
    calc
      b i ^ 6 = b i ^ 2 * b i ^ 4 := by ring
      _ ≤ 16 * b i ^ 4 := mul_le_mul_of_nonneg_right (hb i hi) (by positivity)
  calc
    finiteSixthMomentSum s b ≤ ∑ i ∈ s, 16 * b i ^ 4 :=
      Finset.sum_le_sum hterm
    _ = 16 * finiteFourthMomentSum s b := by
      simp [finiteFourthMomentSum, Finset.mul_sum]

theorem finite_eighth_le_sixteen_sixth (s : Finset Index) (b : Index → ℝ)
    (hb : ∀ i ∈ s, b i ^ 2 ≤ 16) :
    finiteEighthMomentSum s b ≤ 16 * finiteSixthMomentSum s b := by
  have hterm : ∀ i ∈ s, b i ^ 8 ≤ 16 * b i ^ 6 := by
    intro i hi
    calc
      b i ^ 8 = b i ^ 2 * b i ^ 6 := by ring
      _ ≤ 16 * b i ^ 6 := mul_le_mul_of_nonneg_right (hb i hi) (by positivity)
  calc
    finiteEighthMomentSum s b ≤ ∑ i ∈ s, 16 * b i ^ 6 :=
      Finset.sum_le_sum hterm
    _ = 16 * finiteSixthMomentSum s b := by
      simp [finiteSixthMomentSum, Finset.mul_sum]

/-- Finite-sum version of the critical law's fourth-cumulant formula. -/
def finiteCosineFourthCumulant (s : Finset Index) (b : Index → ℝ) : ℝ :=
  -3 / 8 * finiteFourthMomentSum s b

theorem finiteCosineFourthCumulant_eq_sum (s : Finset Index) (b : Index → ℝ) :
    finiteCosineFourthCumulant s b = ∑ i ∈ s, (-3 * b i ^ 4 / 8) := by
  unfold finiteCosineFourthCumulant finiteFourthMomentSum
  rw [Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro i hi
  ring

theorem finiteCosineFourthCumulant_neg (s : Finset Index) (b : Index → ℝ)
    {i : Index} (hi : i ∈ s) (hbi : b i ≠ 0) :
    finiteCosineFourthCumulant s b < 0 := by
  have hs4 : 0 < finiteFourthMomentSum s b := by
    unfold finiteFourthMomentSum
    refine Finset.sum_pos' (fun j _ => by positivity) ⟨i, hi, ?_⟩
    positivity
  unfold finiteCosineFourthCumulant
  nlinarith

end FiniteMoments

/-! ## One-zero critical profile algebra -/

/-- The paper's one-zero profile, stated as an explicit real function. -/
noncomputable def oneZeroProfile (b : ℝ) : ℝ :=
  if b ≤ 1 then 1 else 1 - Real.arccos (1 / b) / π

theorem oneZeroProfile_of_le_one {b : ℝ} (hb : b ≤ 1) :
    oneZeroProfile b = 1 := by
  simp [oneZeroProfile, hb]

theorem oneZeroProfile_of_one_lt {b : ℝ} (hb : 1 < b) :
    oneZeroProfile b = 1 - Real.arccos (1 / b) / π := by
  simp [oneZeroProfile, not_le.mpr hb]

/-- Algebraic reduction of the sign event to a cosine threshold. -/
theorem oneZero_sign_threshold {b x : ℝ} (hb : 0 < b) :
    1 + b * x > 0 ↔ x > -1 / b := by
  constructor <;> intro h
  · exact (div_lt_iff₀ hb).2 (by nlinarith)
  · have := (div_lt_iff₀ hb).1 h
    nlinarith

theorem oneZero_nonnegative_when_small {b x : ℝ} (hb0 : 0 ≤ b) (hb1 : b ≤ 1)
    (hx0 : -1 ≤ x) : 0 ≤ 1 + b * x := by
  by_cases hx : 0 ≤ x
  · positivity
  · have hbx : -b ≤ b * x := by
      nlinarith [mul_nonneg hb0 (sub_nonneg.mpr hx0)]
    nlinarith

/-! ## Gaussian/Edgeworth coefficient arithmetic -/

/-- Standard Gaussian moment of order `2k`, recursively as `(2k-1)!!`. -/
def gaussianEvenMoment : ℕ → ℕ
  | 0 => 1
  | k + 1 => (2 * k + 1) * gaussianEvenMoment k

theorem gaussianEvenMoment_0 : gaussianEvenMoment 0 = 1 := by rfl
theorem gaussianEvenMoment_2 : gaussianEvenMoment 1 = 1 := by norm_num [gaussianEvenMoment]
theorem gaussianEvenMoment_4 : gaussianEvenMoment 2 = 3 := by norm_num [gaussianEvenMoment]
theorem gaussianEvenMoment_6 : gaussianEvenMoment 3 = 15 := by norm_num [gaussianEvenMoment]
theorem gaussianEvenMoment_8 : gaussianEvenMoment 4 = 105 := by norm_num [gaussianEvenMoment]

/-- Coefficient expression obtained by integrating the seven displayed terms
of the polynomial `Q` against a centered Gaussian kernel. -/
def edgeworthFromGaussianMoments (variance S4 S6 : ℝ) : ℝ :=
  1
    - gaussianEvenMoment 1 / (6 * variance)
    + gaussianEvenMoment 2 / (120 * variance ^ 2)
    - S4 * gaussianEvenMoment 2 / (64 * variance ^ 2)
    + S4 * gaussianEvenMoment 3 / (384 * variance ^ 3)
    - S6 * gaussianEvenMoment 3 / (576 * variance ^ 3)
    + S4 ^ 2 * gaussianEvenMoment 4 / (8192 * variance ^ 4)

/-- Exact machine check of all rational coefficients in the paper's
third-order correction. Here `variance` denotes `sigma^2`. -/
theorem edgeworth_third_order_coefficients (variance S4 S6 : ℝ) :
    edgeworthFromGaussianMoments variance S4 S6 =
      1 - 1 / (6 * variance)
        - 3 * S4 / (64 * variance ^ 2)
        + 1 / (40 * variance ^ 2)
        + 5 * S4 / (128 * variance ^ 3)
        - 5 * S6 / (192 * variance ^ 3)
        + 105 * S4 ^ 2 / (8192 * variance ^ 4) := by
  norm_num [edgeworthFromGaussianMoments, gaussianEvenMoment]
  ring

/-- The three nontrivial polynomial coefficients in `Q` after writing
`A = S4/64` and `B = S6/576`. -/
theorem q_polynomial_coefficient_arithmetic (S4 S6 : ℝ) :
    (S4 / 64) / 6 = S4 / 384 ∧
      S6 / 576 = 5 * S6 / (192 * 15) ∧
      (S4 / 64) ^ 2 / 2 = S4 ^ 2 / 8192 := by
  constructor
  · ring
  constructor <;> ring

end

end WeightedPrimeRaces
