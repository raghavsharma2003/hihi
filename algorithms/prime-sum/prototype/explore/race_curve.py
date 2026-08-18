#!/usr/bin/env python3
"""
The full delta(m) curve for weighted Chebyshev races mod 4, pushed to both
theoretical ends.

Kernel (from the uniform explicit formula, races normalized by the
prime-square bias term): E_m = 1 + V_m,
  V_m = sum_{gamma>0} a_gamma(m) * 2 cos(theta_gamma),
  a_gamma(m) = (2m+1)/sqrt((m+1/2)^2 + gamma^2),
delta(m) = P(E_m > 0) under GRH + LI (independent uniform phases).

Theoretical ends this script tests:

END 1 (m -> infinity): substituting gamma = (m+1/2)u and using the zero
density (1/2pi) log(2 gamma / pi) for chi4 gives
  Var(m) ~ 2 (m+1/2) log(2(m+1/2)/pi),
growing without bound while the bias term stays 1. CLT applies (many
comparable coefficients), so
  delta(m) - 1/2  ~  1 / sqrt(2 pi Var(m))  -> 0:
the bias dissolves at an explicit 1/sqrt(m log m) rate. The script
compares Monte Carlo delta(m) against the Gaussian law Phi(1/sigma).

END 2 (m -> -1/2 from above): a_gamma -> 0 like (2m+1), fluctuations
vanish against the fixed bias, delta(m) -> 1 faster than any power
(Gaussian tail in 1/(2m+1)).

END 3 (m < -1/2, handled in race_frozen.py): x^(m+1/2) -> 0, the race
FREEZES: D_m(x) converges to the constant -sum_p chi4(p) p^m, computable
via log L; the sign is decided forever.

Usage: race_curve.py [n_samples]
"""
import sys, os, math
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
NS = int(float(sys.argv[1])) if len(sys.argv) > 1 else 2_000_000

gammas = np.loadtxt(os.path.join(HERE, "chi4_zeros.txt"))
gN = gammas[-1]

def tail_variance(m):
    f = lambda g: 2.0 * ((2*m+1)**2 / ((m+0.5)**2 + g*g)) * (math.log(2*g/math.pi) / (2*math.pi))
    total, g, step = 0.0, gN, 2.0
    while g < 5e6:
        total += f(g + step/2) * step
        g += step
        if g > 2e4: step = 100.0
    return total

def Phi(z):
    return 0.5 * math.erfc(-z / math.sqrt(2))

rng = np.random.default_rng(20260815)
MS = [-0.3, -0.2, -0.1, 0.0, 0.5, 1.0, 2.0, 3.0, 5.0, 8.0, 12.0, 20.0, 35.0, 60.0, 100.0]
print(f"{len(gammas)} chi4 zeros (gamma_max={gN:.0f}), {NS} samples per m")
print(f"{'m':>6} {'delta_MC':>10} {'+/-':>8} {'sigma':>8} {'Gauss Phi(1/s)':>14} {'asympt law':>11}")
for m in MS:
    a = (2*m+1) / np.sqrt((m+0.5)**2 + gammas**2)
    tv = tail_variance(m)
    var = float(np.sum(2*a*a)) + tv
    sd = math.sqrt(var)
    hits, done, block = 0, 0, 200_000
    while done < NS:
        n = min(block, NS - done)
        th = rng.uniform(0, 2*math.pi, size=(n, len(gammas)))
        V = (2.0 * np.cos(th) @ a) + rng.normal(0.0, math.sqrt(tv), size=n)
        hits += int(np.count_nonzero(1.0 + V > 0.0))
        done += n
    p = hits / NS
    se = math.sqrt(max(p*(1-p), 1e-12)/NS)
    gauss = Phi(1.0/sd)
    # asymptotic law with the derived variance 2(m+1/2)log(2(m+1/2)/pi)
    v_as = 2*(m+0.5)*math.log(2*(m+0.5)/math.pi) if 2*(m+0.5) > math.pi else float('nan')
    law = 0.5 + 1.0/math.sqrt(2*math.pi*v_as) if v_as == v_as and v_as > 0 else float('nan')
    print(f"{m:>6.1f} {p:>10.5f} {se:>8.5f} {sd:>8.4f} {gauss:>14.5f} {law:>11.5f}")
