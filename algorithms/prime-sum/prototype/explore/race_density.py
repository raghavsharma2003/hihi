#!/usr/bin/env python3
"""
Rubinstein-Sarnak logarithmic densities for WEIGHTED Chebyshev races mod 4.

The race (theta-form): R_m(x) = sum_{p<=x, p=3(4)} p^m log p - sum_{p=1(4)} p^m log p.
Explicit formula (L(s,chi4) entire, no main term; prime squares give the bias):
  R_m(x) = x^(m+1/2)/(2m+1) + sum_rho x^(rho+m)/(rho+m) + smaller,
so with u = ln x the normalized race E_m = (2m+1) x^(-(m+1/2)) R_m tends to the
almost-periodic function
  E_m(u) = 1 + (2m+1) * sum_{gamma>0} 2 Re( e^(i gamma u) / ((m+1/2) + i gamma) ).
Under GRH + linear independence of the gamma (the standard Rubinstein-Sarnak
assumptions) the logarithmic density of {x : 3-side leads} equals
  delta(m) = P( 1 + V_m > 0 ),   V_m = sum_gamma a_gamma(m) * 2 cos(theta_gamma),
with independent uniform phases theta_gamma and
  a_gamma(m) = (2m+1) / sqrt((m+1/2)^2 + gamma^2).
The bias term stays 1 while the fluctuation coefficients grow like (2m+1)/gamma:
heavier weights weaken the bias.

Anchor: m=0 must reproduce the classical 0.9959... (Rubinstein-Sarnak 1994).
Zeros: 511 ordinates of L(s,chi4) from chi4_zeros.txt (computed in ap_sums.py);
the tail gamma > gamma_N is added as an independent Gaussian with variance from
the Riemann-von Mangoldt density for modulus 4.

Usage: race_density.py [n_samples]
"""
import sys, os, math
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
NS = int(float(sys.argv[1])) if len(sys.argv) > 1 else 4_000_000

gammas = np.loadtxt(os.path.join(HERE, "chi4_zeros.txt"))
gN = gammas[-1]

def tail_variance(m):
    # var of sum over gamma > gN of (a_gamma * 2 cos(theta)) = sum 2 a^2,
    # zero density for modulus q=4: dN/dt ~ log(2 t / pi) / (2 pi)  (q t / (2 pi e) form)
    f = lambda g: 2.0 * ((2*m+1)**2 / ((m+0.5)**2 + g*g)) * (math.log(2*g/math.pi) / (2*math.pi))
    # integrate to effective infinity
    total, g, step = 0.0, gN, 2.0
    while g < 2e6:
        total += f(g + step/2) * step
        g += step
        if g > 2e4: step = 50.0
    return total

rng = np.random.default_rng(20260815)
print(f"{len(gammas)} chi4 zeros, gamma_max={gN:.1f}, samples={NS}")
print(f"{'m':>3} {'delta_log(m)':>14} {'+/-':>10} {'fluct sd':>9} {'tail sd':>8}")
for m in [0, 1, 2, 3]:
    a = (2*m+1) / np.sqrt((m+0.5)**2 + gammas**2)
    tv = tail_variance(m)
    # Monte Carlo in blocks to bound memory
    hits = 0
    block = 250_000
    done = 0
    while done < NS:
        n = min(block, NS - done)
        th = rng.uniform(0, 2*math.pi, size=(n, len(gammas)))
        V = (2.0 * np.cos(th) @ a) + rng.normal(0.0, math.sqrt(tv), size=n)
        hits += int(np.count_nonzero(1.0 + V > 0.0))
        done += n
    p = hits / NS
    se = math.sqrt(p*(1-p)/NS)
    sd = math.sqrt(float(np.sum(2*a*a)))
    print(f"{m:>3} {p:>14.5f} {se:>10.5f} {sd:>9.4f} {math.sqrt(tv):>8.4f}")
