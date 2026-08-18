#!/usr/bin/env python3
"""30-point deterministic delta_q(m) grid (Gil-Pelaez, same kernel as
race_density_exact.py, plus the exact closed-form tail remainder beyond
G=5e6), to test strict monotonicity of m -> delta_q(m).
"""
import os, math, sys
import numpy as np
from scipy.special import j0

HERE = "/home/user/hihi/algorithms/prime-sum/prototype/explore"

def tail_var(m, gN, q):
    f = lambda g: 2.0*((2*m+1)**2/((m+0.5)**2+g*g))*(math.log(q*g/(2*math.pi))/(2*math.pi))
    tot, g, step = 0.0, gN, 2.0
    while g < 5e6:
        tot += f(g+step/2)*step
        g += step
        if g > 2e4: step = 100.0
    # exact remainder beyond G=5e6 (audit-verified closed form)
    tot += ((2*m+1)**2/math.pi)*(math.log(q*g/(2*math.pi))+1.0)/g
    return tot

def delta(m, gammas, q, n=400000):
    a = (2*m+1)/np.sqrt((m+0.5)**2+gammas**2)
    tv = tail_var(m, gammas[-1], q)
    T = max(60.0, 12.0/math.sqrt(tv) if tv > 0 else 400.0)
    T = min(T, 4000.0)
    t = np.linspace(1e-9, T, n)
    lg = np.zeros_like(t)
    sgn = np.ones_like(t)
    for i in range(0, len(a), 24):
        J = j0(2.0*np.outer(a[i:i+24], t))
        lg += np.log(np.abs(J) + 1e-300).sum(axis=0)
        sgn *= np.prod(np.sign(J), axis=0)
    phi = sgn*np.exp(lg - tv*t*t/2)
    return 0.5 + np.trapezoid(phi*np.sin(t)/t, t)/math.pi

MS = [-0.2, -0.15, -0.1, -0.05, 0.0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5,
      2.0, 2.5, 3.0, 4.0, 5.0, 6.0, 8.0, 10.0, 12.0, 15.0, 20.0, 25.0,
      30.0, 40.0, 50.0, 60.0, 75.0, 90.0, 100.0]
assert len(MS) == 30

for q, zf in [(4, "chi4_zeros.txt"), (3, "chi3_zeros.txt")]:
    g = np.loadtxt(os.path.join(HERE, zf))
    print(f"q={q} ({len(g)} zeros), 30-point grid:")
    prev = None
    mono = True
    vals = []
    for m in MS:
        d = delta(float(m), g, q)
        vals.append(d)
        dec = "" if prev is None else ("  OK(dec)" if d < prev else "  VIOLATION")
        if prev is not None and d >= prev: mono = False
        print(f"  delta_{q}({m:g}) = {d:.9f}{dec}")
        prev = d
    print(f"  STRICTLY DECREASING on all 30 points: {mono}")
    sys.stdout.flush()
