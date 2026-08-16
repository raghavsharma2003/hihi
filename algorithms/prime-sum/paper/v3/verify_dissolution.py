#!/usr/bin/env python3
"""
verify_dissolution.py -- every numeric and explicit constant used in
paper/v3/dissolution-theorem.tex, recomputed for this draft.

Checks, in order:
  [1] sigma_m^2 = 4M (log xi)'(m+1,chi) against the values quoted in the
      draft (q=4: m=0,1,2,3,8,20,100; q=3: m=60), via the Hurwitz-zeta
      representation of L(s,chi) at 50 working digits.
  [2] Bessel constants of Lemma (Bessel facts):
        |J0(z)| <= (8/pi) z^{-1/2}          (z>0, sampled densely),
        |log J0(z) + z^2/4|        <= z^4/17  (|z|<=1),
        |log J0(z) + z^2/4 + z^4/64| <= z^6/80 (|z|<=1),
        |log J0(z) + z^2/4 + z^4/64 + z^6/576| <= C8 z^8,
        rho(z*) = sup_{z>=z*}|J0(z)| < 1 at z* = 1/(2 sqrt 5),
        4*5^{1/4}/pi < 2  (the constant c3 of the large-t lemma).
  [3] The closed forms for S4(m) = sum (2a_gamma)^4 and
      S6(m) = sum (2a_gamma)^6, with a zeros+tail check for S4.
  [4] High-accuracy deterministic Gil-Pelaez densities delta_q(m) with
      the EXACT tail variance sigma_m^2 - (computed-zero sum) (certified
      by [1]), and comparison with the one-, two-, and three-term dissolution
      predictions
        pred1 = (2 pi sigma^2)^{-1/2}
        pred2 = pred1 * (1 - 1/(6 sigma^2) - 3 S4/(64 sigma^4)).
        pred3 = pred2 + pred1 * (1/(40 sigma^4)
                 + 5 S4/(128 sigma^6) - 5 S6/(192 sigma^6)
                 + 105 S4^2/(8192 sigma^8)).
      Also prints the Gaussianized-tail modelling error bound
      0.21 * S4_tail / sigma^4 (relative; rigorous on t <= 1/8 by the
      T3 estimate applied to the tail factors) PLUS the t > 1/8
      remainder, bounded numerically by inserting the computed |Phi|
      into the same integrand.  Their sum bounds the amount by which
      Gaussianizing the unseen zeros can bias these reference
      densities.
Run: python3 verify_dissolution.py     (needs mpmath, numpy, scipy)
"""
import os, math
import numpy as np
from scipy.special import j0
from mpmath import mp, mpf, psi, log as mlog, diff, zeta, pi as mpi, quad, besselj

mp.dps = 50
HERE = os.path.dirname(os.path.abspath(__file__))
EXPLORE = os.path.normpath(os.path.join(HERE, "..", "..", "prototype", "explore"))

CHARS = {4: {1: 1, 3: -1}, 3: {1: 1, 2: -1}}   # real nonprincipal chi mod q (odd: a=1)

def Lfun(s, q):
    return q**(-s) * sum(c * zeta(s, mpf(a) / q) for a, c in CHARS[q].items())

def LpL_q4_s1():
    """L'/L(1, chi4), pole-free: the classical closed form
    L'(1,chi4) = (pi/4)(gamma + 2 log 2 + 3 log pi - 4 log Gamma(1/4)),
    L(1,chi4) = pi/4.  Cross-checked (25 digits) against the accelerated
    alternating series sum (-1)^(k+1) log(2k+1)/(2k+1) via mpmath nsum
    with method='a'; both give L'(1) = 0.1929013167969124293631898."""
    from mpmath import euler, gamma as mgamma
    Lp = (mpi / 4) * (euler + 2 * mlog(2) + 3 * mlog(mpi) - 4 * mlog(mgamma(mpf(1) / 4)))
    return Lp / (mpi / 4)

def sigma2(m, q):
    """4 M (log xi)'(m+1) = 4M [ (1/2)log(q/pi) + (1/2)psi((s+a)/2) + L'/L(s) ], s=m+1, a=1.
    For (q,m)=(4,0) use the pole-free closed form for L'/L(1); for m>=1 the
    Hurwitz representation with guard digits is accurate (checked at m=1..100
    against the quoted 40-dps values, which trace to the same identity)."""
    with mp.workdps(mp.dps + 90):
        M = mpf(m) + mpf(1) / 2
        s = mpf(m) + 1
        if m == 0 and q == 4:
            LL = LpL_q4_s1()
        else:
            LL = diff(lambda z: mlog(Lfun(z, q)), s)
        return +(4 * M * (mlog(mpf(q) / mpi) / 2 + psi(0, (s + 1) / 2) / 2 + LL))

def S4_closed(m, q):
    """S4 = 16 sigma^2 - 64 M^2 (log xi)''(m+1)  (exact under GRH + L(1/2)!=0)."""
    with mp.workdps(mp.dps + 90):
        M = mpf(m) + mpf(1) / 2
        s = mpf(m) + 1
        LL2 = diff(lambda z: mlog(Lfun(z, q)), s, 2)
        xi2 = psi(1, (s + 1) / 2) / 4 + LL2
        return +(16 * sigma2(m, q) - 64 * M**2 * xi2)

def S6_closed(m, q):
    """S6 = 12 S4 + 256 M^3 (log xi)'''(m+1), exact under the same hypotheses."""
    with mp.workdps(mp.dps + 90):
        M = mpf(m) + mpf(1) / 2
        s = mpf(m) + 1
        LL3 = diff(lambda z: mlog(Lfun(z, q)), s, 3)
        xi3 = psi(2, (s + 1) / 2) / 8 + LL3
        return +(12 * S4_closed(m, q) + 256 * M**3 * xi3)

def zeros(q):
    f = {4: "chi4_zeros.txt", 3: "chi3_zeros.txt"}[q]
    return np.loadtxt(os.path.join(EXPLORE, f))

# ---------------------------------------------------------------- [1]
print("[1] sigma_m^2 = 4M (log xi)'(m+1):")
# (4,0): the value 0.155568715095 circulated in earlier notes is an artifact of
# differentiating the Hurwitz representation at its s=1 pole; three pole-free
# routes (closed-form L'(1,chi4) = (pi/4)(gamma+2log2+3logpi-4logGamma(1/4)),
# the accelerated alternating series for L'(1), and zeros+tail) agree on
# 0.1555679799235859, as recorded at variance-identity.tex line ~339.
quoted = {(4, 0): "0.1555679799235859", (4, 1): "1.36855505395", (4, 2): "3.64763501678",
          (4, 3): "6.77684634861", (4, 8): "29.7124677146", (4, 20): "106.325999646",
          (4, 100): "836.874383888"}
S2 = {}
for (q, m), want in sorted(quoted.items()):
    v = sigma2(m, q); S2[(q, m)] = v
    ok = abs(v - mpf(want)) < mpf(10) ** (-9) * max(1, abs(v))
    print(f"    q={q} m={m:>3}: {mp.nstr(v, 15):>20}  quoted {want}  {'OK' if ok else 'MISMATCH'}")
for (q, m) in [(3, 60), (3, 20), (3, 8)]:
    S2[(q, m)] = sigma2(m, q)
    print(f"    q={q} m={m:>3}: {mp.nstr(S2[(q,m)], 15):>20}  (no quoted value)")

# ---------------------------------------------------------------- [2]
print("[2] Bessel constants:")
zs = np.linspace(1e-4, 400.0, 4_000_000)
bad = np.abs(j0(zs)) - (8 / math.pi) / np.sqrt(zs)
print(f"    max |J0(z)| - (8/pi)z^-1/2 on (0,400]: {bad.max():.6f}  (must be <0)")
# the log J0 expansion bounds need multiprecision: near z=0 the remainders are
# below float64 cancellation noise (z^6/576 ~ 1e-21 at z=0.005).
e1m = mpf(0); e2m = mpf(0); e3m = mpf(0)
for i in range(1, 1001):
    z = mpf(i) / 1000
    l = mlog(besselj(0, z))
    e1m = max(e1m, abs(l + z**2 / 4) / z**4)
    e2m = max(e2m, abs(l + z**2 / 4 + z**4 / 64) / z**6)
    e3m = max(e3m, abs(l + z**2 / 4 + z**4 / 64 + z**6 / 576) / z**8)
print(f"    sup |log J0 + z^2/4|/z^4  on (0,1]: {mp.nstr(e1m, 6)}  (claim <= 1/17 = {1/17:.6f})")
print(f"    sup |log J0 + z^2/4 + z^4/64|/z^6 : {mp.nstr(e2m, 6)}  (claim <= 1/80 = {1/80:.6f}; "
      f"z->0 limit 1/576 = {1/576:.6f})")
print(f"    sup |log J0 + z^2/4 + z^4/64 + z^6/576|/z^8: {mp.nstr(e3m, 6)}  "
      "(finite absolute C8; sampled on (0,1])")
zstar = 1 / (2 * math.sqrt(5))
grid = np.linspace(zstar, 400, 4_000_000)
rho = np.abs(j0(grid)).max()
print(f"    rho(z*) = sup_(z>=1/(2 sqrt5))|J0| = {rho:.6f} = J0({zstar:.6f}) itself? "
      f"J0(z*)={j0(zstar):.6f}  (must be <1)")
print(f"    c3 = 4*5^(1/4)/pi = {4 * 5**0.25 / math.pi:.6f}  (claim < 2)")

# ---------------------------------------------------------------- [3]
def S4_parts(m, q):
    # a_gamma = 2M/sqrt(M^2+gamma^2); 2a_gamma = 4M/sqrt(M^2+gamma^2)
    g = zeros(q); M = m + 0.5
    twoa = 4 * M / np.sqrt(M**2 + g**2)
    head = (twoa**4).sum()
    G = float(g[-1])
    Mq = mpf(M); Gq = mpf(G)
    tail = quad(lambda t: 256 * Mq**4 / (Mq**2 + t**2)**2 * mlog(q * t / (2 * mpi)) / (2 * mpi),
                [Gq, 10 * Gq, 1000 * Gq, mp.inf])
    return head, float(tail)

print("[3] S4 = sum (2a)^4: closed form 16 sigma^2 - 64 M^2 (log xi)''(m+1)")
print("    vs zeros+tail vs asymptotic 32M(log(qM/2pi)-1) + 32(2a-1), a=1:")
S4 = {}
S6 = {}
for (q, m) in [(4, 100), (4, 20), (4, 8), (3, 60)]:
    h, t = S4_parts(m, q); M = m + 0.5
    closed = S4_closed(m, q)
    asym = 32 * M * (math.log(q * M / (2 * math.pi)) - 1) + 32
    S4[(q, m)] = float(closed)
    S6[(q, m)] = float(S6_closed(m, q))
    print(f"    q={q} m={m:>3}: closed {float(closed):12.4f}   zeros+tail {h+t:12.4f}"
          f"   asym {asym:12.4f}   (S4/sigma^2 = {float(closed)/float(S2[(q,m)]):.3f}; ->16)"
          f"   S6={S6[(q,m)]:12.4f}")

# ---------------------------------------------------------------- [4]
def delta(m, q, T=2.0, n=2_000_001):
    g = zeros(q); M = m + 0.5
    a = (2 * m + 1) / np.sqrt(M**2 + g**2)           # a_gamma
    s2_exact = float(S2[(q, m)])
    tv = s2_exact - float((2 * a**2).sum())          # exact tail variance
    t = np.linspace(1e-12, T, n)
    lg = np.zeros_like(t); sg = np.ones_like(t)
    for av in a:
        v = j0(2 * av * t)
        lg += np.log(np.abs(v) + 1e-300); sg *= np.sign(v)
    phi = sg * np.exp(lg - tv * t * t / 2)
    val = 0.5 + np.trapezoid(phi * np.sin(t) / t, t) / math.pi
    return val, tv, s2_exact

print("[4] densities vs dissolution predictions:")
print("    (q,m)      delta            d-1/2      pred1      pred2      pred3      rel.err1   rel.err2   rel.err3  tailmodel")
for (q, m) in [(4, 8), (4, 20), (4, 100), (3, 60)]:
    d, tv, s2 = delta(m, q)
    dd = d - 0.5
    pred1 = 1 / math.sqrt(2 * math.pi * s2)
    s4 = S4[(q, m)]
    s6 = S6[(q, m)]
    pred2 = pred1 * (1 - 1 / (6 * s2) - 3 * s4 / (64 * s2 * s2))
    pred3 = pred2 + pred1 * (1 / (40 * s2**2) + 5 * s4 / (128 * s2**3)
                             - 5 * s6 / (192 * s2**3)
                             + 105 * s4**2 / (8192 * s2**4))
    # Gaussian-tail modelling error of the REFERENCE density (relative): the
    # unseen zeros gamma > gamma_511 enter as exp(-sigma_tail^2 t^2/2) instead of
    # prod J0.  On t <= 1/8 the T3 estimate applied to the tail factors gives the
    # rigorous relative bound 0.21 * S4_tail / sigma^4.  On t > 1/8 that estimate
    # does not apply (the head factors' arguments exceed 1); there we bound the
    # bias by (1/pi) int |Phi_model| (t^4 S4_tail/17) e^{t^4 S4_tail/17} dt with
    # the COMPUTED |Phi_model| -- a numerical evaluation on the same footing as
    # the reference density itself.  Valid while 2 a_tail_max * t <= 1; where
    # that fails (only (4,100) near t=2.5) |Phi_model| < 1e-100 and the factor
    # is irrelevant.
    gg = zeros(q); M = m + 0.5
    s4_head = ((4 * M / np.sqrt(M**2 + gg**2))**4).sum()
    s4t = s4 - s4_head
    smallt = 0.21 * s4t / s2**2
    aa = (2 * m + 1) / np.sqrt(M**2 + gg**2)
    tt = np.linspace(0.125, 2.5, 400001)
    lgt = np.zeros_like(tt)
    for av in aa:
        lgt += np.log(np.abs(j0(2 * av * tt)) + 1e-300)
    integ = (np.exp(lgt - tv * tt**2 / 2) * (tt**4 * s4t / 17)
             * np.exp(np.minimum(tt**4 * s4t / 17, 200.0)))
    bigt = np.trapezoid(integ, tt) / math.pi / pred1
    print(f"    ({q},{m:>3})  {d:.9f}  {dd:.7f}  {pred1:.7f}  {pred2:.7f}  {pred3:.7f}  "
          f"{dd/pred1-1:+.2e}  {dd/pred2-1:+.2e}  {dd/pred3-1:+.2e}  "
          f"{smallt:.1e}+{bigt:.1e}={smallt+bigt:.1e}")
print("    rel.err2 should be << rel.err1 and shrink roughly like (M log M)^-2 (constants unknown);")
print("    rel.err3 is the new O(sigma^-6) residual, subject to the printed tail-model floor;")
print("    'tailmodel' (small-t rigorous + large-t computed = total) bounds the relative bias of the reference delta from Gaussianizing unseen zeros.")

# convergence sanity: halve the grid, widen T
d1, _, _ = delta(100, 4, T=2.0, n=1_000_001)
d2, _, _ = delta(100, 4, T=3.0, n=3_000_001)
d3, _, _ = delta(100, 4)
print(f"    grid sanity delta_4(100): n/2 -> {d1:.10f}, T=3 -> {d2:.10f}, ref -> {d3:.10f}")
