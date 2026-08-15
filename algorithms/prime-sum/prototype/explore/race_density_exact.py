#!/usr/bin/env python3
"""
Deterministic Rubinstein-Sarnak densities for weighted races via
Gil-Pelaez Fourier inversion (no Monte Carlo, no seeds).

V = sum_gamma 2 a_gamma cos(theta_gamma) with independent uniform phases
(LI) has characteristic function  phi(t) = prod_gamma J0(2 a_gamma t),
times exp(-Var_tail t^2/2) for the Gaussianized unseen-zero tail. Then
  delta = P(1 + V > 0) = 1/2 + (1/pi) int_0^inf phi(t) sin(t)/t dt.
The integrand decays under the tail Gaussian; we integrate on a fine
grid to T where the envelope < 1e-12.

Usage: race_density_exact.py [q]   (q = 4 or 3; default both)
"""
import sys, os, math
import numpy as np
from scipy.special import j0

HERE = os.path.dirname(os.path.abspath(__file__))

def tail_var(m, gN, q):
    f = lambda g: 2.0*((2*m+1)**2/((m+0.5)**2+g*g))*(math.log(q*g/(2*math.pi))/(2*math.pi))
    tot, g, step = 0.0, gN, 2.0
    while g < 5e6:
        tot += f(g+step/2)*step
        g += step
        if g > 2e4: step = 100.0
    return tot

def delta(m, gammas, q):
    a = (2*m+1)/np.sqrt((m+0.5)**2+gammas**2)
    tv = tail_var(m, gammas[-1], q)
    # integration grid: phi damped by exp(-tv t^2/2); also J0 products decay
    T = max(60.0, 12.0/math.sqrt(tv) if tv > 0 else 400.0)
    T = min(T, 4000.0)
    n = 400000
    t = np.linspace(1e-9, T, n)
    lg = np.zeros_like(t)
    for av in a:               # log of product of J0's, chunked over zeros
        lg += np.log(np.abs(j0(2*av*t)) + 1e-300)
    sgn = np.ones_like(t)
    for av in a:
        sgn *= np.sign(j0(2*av*t))
    phi = sgn*np.exp(lg - tv*t*t/2)
    integ = phi*np.sin(t)/t
    return 0.5 + np.trapezoid(integ, t)/math.pi

def main():
    for q, zf, ms in [(4, "chi4_zeros.txt", [0,1,2,3,8,20,100]),
                      (3, "chi3_zeros.txt", [0,1,2,3,8,20,60])]:
        g = np.loadtxt(os.path.join(HERE, zf))
        print(f"q={q} ({len(g)} zeros):")
        for m in ms:
            print(f"  delta_{q}({m}) = {delta(float(m), g, q):.6f}")

if __name__ == "__main__":
    main()
