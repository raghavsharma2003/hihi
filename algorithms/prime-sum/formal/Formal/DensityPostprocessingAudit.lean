import Formal.DensityPostprocessing

/-!
Run with

`lake env lean Formal/DensityPostprocessingAudit.lean`

to print the kernel axiom dependencies of the independent post-processing
layer.  No project-local axiom, `sorry`, or `admit` is permitted.
-/

open WeightedPrimeRaces.DensityPostprocessing

#print axioms all_density_widths_below_two_e_minus_seven
#print axioms q4_m0_rounds
#print axioms q4_m1_rounds
#print axioms q4_m2_rounds
#print axioms q4_m3_rounds
#print axioms q4_m8_rounds
#print axioms q4_m20_rounds
#print axioms q4_m100_rounds
#print axioms q3_m0_rounds
#print axioms q3_m1_dagger
#print axioms q3_m2_rounds
#print axioms q3_m3_rounds
#print axioms q3_m8_rounds
#print axioms q3_m20_rounds
#print axioms q3_m60_dagger
#print axioms sqrt_two_pi_s_bounds
#print axioms correction2_bounds
#print axioms relativeLeadingResidual_bounds
#print axioms relativeSecondResidual_bounds
#print axioms q4_m8_sqrt_certificate
#print axioms q4_m20_sqrt_certificate
#print axioms q4_m100_sqrt_certificate
#print axioms q3_m60_sqrt_certificate
#print axioms q4_m8_residual_claims
#print axioms q4_m20_residual_claims
#print axioms q4_m100_residual_claims
#print axioms q3_m60_residual_claims
