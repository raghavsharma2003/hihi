#!/usr/bin/env python3
"""
Verification script for paper/v3/variance-identity.tex
("The variance in closed form").

Checks, at 50 working digits (mpmath):
  A. root number of chi4: tau(chi4) = 2i, epsilon = tau/(i sqrt(4)) = +1
  B. evenness of Xi(z) = Lambda(1/2+z), Lambda = (4/pi)^{(s+1)/2}
     Gamma((s+1)/2) L(s,chi4)
  C. L(1/2,chi4) = beta(1/2) > 0
  D. sigma_m^2 = 4M (log Lambda)'(m+1) against the zero-sum
     sum_{gamma<=Gamma} 2 a_gamma^2 + RvM tail (511 ordinates)
  E. C = sum 2/gamma^2 = (log Lambda)''(1/2)
       = (1/4) psi'(3/4) + (log L)''(1/2)  [psi'(3/4) = pi^2 - 8G]
     vs the paper's old zero-sum value 0.156033
  F. asymptotics: sigma_m^2 - 2M log(4M/(2pi)) -> 1, and
     M*(sigma_m^2 - 2M log(4M/(2pi)) - 1) -> 1/12
  G. general q: even real primitive character mod 5 gives
     Var_5(m) - 2M log(5M/(2pi)) -> -1  (c0 = 2a-1 with a=0)
  H. table numbers for the tex file (sigma^2 exact, paper law, tail
     variance at Gamma = gamma_511)
  I. (needs numpy+scipy; skipped with a notice otherwise) the density
     shift quoted in Remark [certified tails]: replacing the estimated
     tail variance of race_density_exact.py by the exact one moves the
     Gil-Pelaez densities of tab:delta by < 4.3e-6, worst ~4.23e-6 at
     q=3, m=1 (spot-checked at (q,m) = (4,1), (4,100), (3,1))
"""
import os
from mpmath import mp, mpf, mpc, exp, log, pi, gamma, loggamma, digamma, \
    zeta, sqrt, catalan, diff, polygamma, cos, sin, fabs, euler, nsum, inf, \
    workdps

mp.dps = 50

HERE = os.path.dirname(os.path.abspath(__file__))
ZEROS = os.path.join(HERE, '..', '..', 'prototype', 'explore', 'chi4_zeros.txt')

# ---------- L(s, chi4) = Dirichlet beta via Hurwitz zeta ----------
# The two Hurwitz zetas share a pole at s=1 (residue 1 each); their
# difference is entire but suffers catastrophic cancellation when a
# numerical-derivative step lands near s=1.  Evaluate with 80 guard
# digits so every diff() below is safe at every s used.
def Lbeta(s):
    with workdps(mp.dps + 80):
        v = 4**(-s) * (zeta(s, mpf(1)/4) - zeta(s, mpf(3)/4))
    return +v

def logLambda(s):
    # completed L: (4/pi)^{(s+1)/2} Gamma((s+1)/2) L(s,chi4)
    return (s+1)/2 * log(4/pi) + loggamma((s+1)/2) + log(Lbeta(s))

def sigma2_closed(m):
    M = m + mpf(1)/2
    return 4*M * diff(logLambda, m+1)

def sigma2_decomposed(m):
    # independent route: (log Lambda)' = (1/2)log(4/pi) + (1/2)psi((s+2)/2) + L'/L
    M = m + mpf(1)/2
    s = m + 1
    LpL = diff(lambda t: log(Lbeta(t)), s)
    return 4*M * (log(4/pi)/2 + digamma((s+1)/2)/2 + LpL)

# ---------- A. root numbers ----------
i = mpc(0, 1)
tau = sum(mpc(cos(2*pi*n/4), sin(2*pi*n/4)) * (1 if n % 4 == 1 else -1)
          for n in (1, 3))
eps = tau / (i * sqrt(mpf(4)))
print("A. tau(chi4) =", tau, "  eps =", eps)
assert fabs(tau - 2*i) < mpf(10)**-45 and fabs(eps - 1) < mpf(10)**-45
# tau(chi3) = i*sqrt(3) (odd, a=1), tau(chi5) = sqrt(5) (even, a=0)
chi3 = {1: 1, 2: -1}
tau3 = sum(mpc(cos(2*pi*n/3), sin(2*pi*n/3)) * chi3[n] for n in (1, 2))
chi5 = {1: 1, 2: -1, 3: -1, 4: 1}
tau5 = sum(mpc(cos(2*pi*n/5), sin(2*pi*n/5)) * chi5[n] for n in (1, 2, 3, 4))
print("   tau(chi3) =", tau3, " (i*sqrt3 =", i*sqrt(mpf(3)), ")")
print("   tau(chi5) =", tau5, " (sqrt5  =", sqrt(mpf(5)), ")")
assert fabs(tau3 - i*sqrt(mpf(3))) < mpf(10)**-45   # eps = tau/(i sqrt q) = +1
assert fabs(tau5 - sqrt(mpf(5))) < mpf(10)**-45     # eps = tau/sqrt q = +1

# ---------- B. evenness of Xi ----------
worst = mpf(0)
for z in (mpf('0.3'), mpf('1.7'), mpc('0.4', '2.1'), mpc('-1.2', '0.9')):
    d = fabs(exp(logLambda(mpf(1)/2 + z)) - exp(logLambda(mpf(1)/2 - z)))
    r = d / fabs(exp(logLambda(mpf(1)/2 + z)))
    worst = max(worst, r)
print("B. evenness of Xi: worst relative asymmetry =", worst)
assert worst < mpf(10)**-40

# ---------- C. central value ----------
L_half = Lbeta(mpf(1)/2)
print("C. L(1/2,chi4) = beta(1/2) =", L_half)
assert L_half > mpf('0.6')

# ---------- load zeros ----------
with open(ZEROS) as f:
    gammas = [mpf(line.strip()) for line in f if line.strip()]
print("   loaded", len(gammas), "ordinates; gamma_1 =", gammas[0])
G = gammas[-1]

# check first few ordinates really are zeros of Lambda (|Lambda| tiny)
for g in gammas[:3]:
    val = fabs(exp(logLambda(mpc(mpf(1)/2, g))))
    print("   |Lambda(1/2 + i*%.6f)| = %.3e" % (float(g), float(val)))
    assert val < mpf(10)**-20

# ---------- D0. anchor at m=0: closed form for L'/L(1,chi4) ----------
# beta'(1)/beta(1) = gamma_E + 2 log 2 + 3 log pi - 4 log Gamma(1/4),
# cross-checked against the accelerated alternating series
# beta'(1) = -sum_{k>=1} (-1)^k log(2k+1)/(2k+1).
bpb1_closed = euler + 2*log(2) + 3*log(pi) - 4*log(gamma(mpf(1)/4))
bpb1_series = -nsum(lambda k: (-1)**k * log(2*k+1)/(2*k+1), [1, inf]) / (pi/4)
bpb1_diff = diff(lambda t: log(Lbeta(t)), 1)
print("D0. beta'/beta(1): closed=%s series-agrees=%.1e diff-agrees=%.1e" % (
    mp.nstr(bpb1_closed, 20), float(fabs(bpb1_closed-bpb1_series)),
    float(fabs(bpb1_closed-bpb1_diff))))
assert fabs(bpb1_closed - bpb1_series) < mpf(10)**-40
assert fabs(bpb1_closed - bpb1_diff) < mpf(10)**-40
sigma2_0_anchor = 2*(log(4/pi)/2 + digamma(1)/2 + bpb1_closed)
print("    sigma^2(0) anchor =", mp.nstr(sigma2_0_anchor, 20),
      " (context file said 0.155568715095: off by %.1e)" %
      float(mpf('0.155568715095') - sigma2_0_anchor))

# ---------- D. identity vs zero-sum ----------
# m=0 target corrected: the 40-dps context value 0.155568715095 is an
# artifact of differentiating the Hurwitz representation at its s=1
# pole without guard digits; three independent pole-free routes give
# 0.15556797992358592886...
CONTEXT = {0: '0.15556797992358592886', 1: '1.36855505395', 2: '3.64763501678',
           3: '6.77684634861', 8: '29.7124677146', 20: '106.325999646',
           100: '836.874383888'}
print("D. sigma_m^2: closed form vs decomposed vs zero-sum+RvM-tail")
def a2sum(m):
    M = m + mpf(1)/2
    return sum(2 * (2*M)**2 / (M**2 + g**2) for g in gammas)
def rvm_tail_a2(m):
    # int_G^inf 2 (2M)^2/(M^2+t^2) dN(t), dN = (1/2pi) log(2t/pi) dt, numeric
    M = m + mpf(1)/2
    from mpmath import quad, inf
    return quad(lambda t: 2*(2*M)**2/(M**2+t**2) * log(2*t/pi)/(2*pi), [G, inf])
for m in (0, 1, 2, 3, 8, 20, 100):
    s2 = sigma2_closed(m)
    s2b = sigma2_decomposed(m)
    zs = a2sum(m)
    tl = rvm_tail_a2(m)
    print("   m=%3d  closed=%s  |closed-decomp|=%.1e  zerosum+tail=%.9f  "
          "(diff %.2e)  context=%s" % (m, mp.nstr(s2, 15), float(fabs(s2-s2b)),
          float(zs+tl), float(zs+tl-s2), CONTEXT[m]))
    assert fabs(s2 - mpf(CONTEXT[m])) < mpf(10)**-9 * max(1, fabs(s2))
    assert fabs(s2 - s2b) < mpf(10)**-35 * max(1, fabs(s2))
    # RvM-smoothed zero sum agrees to the fluctuation scale (~1e-4 rel.)
    assert fabs(zs + tl - s2) < mpf('2e-3') * max(1, fabs(s2))

# ---------- D2. Hadamard product against the real zero list ----------
# log(Xi(z)/Xi(0)) - sum_{gamma<=G} log(1+z^2/gamma^2) should equal the
# unseen-zero tail, approximated by the RvM density integral.
from mpmath import quad
for zv in (mpf(1), mpf(3)):
    lhs = logLambda(mpf(1)/2 + zv) - logLambda(mpf(1)/2)
    fin = sum(log(1 + zv**2/g**2) for g in gammas)
    tail_est = quad(lambda t: log(1 + zv**2/t**2) * log(2*t/pi)/(2*pi),
                    [G, mp.inf])
    print("D2. z=%s: log Xi ratio - finite product = %.8f ; RvM tail est = %.8f"
          % (mp.nstr(zv, 3), float(lhs - fin), float(tail_est)))
    assert fabs((lhs - fin) - tail_est) < mpf('1e-4') * max(1, fabs(lhs))

# ---------- E. the constant C ----------
C_exact = polygamma(1, mpf(3)/4)/4 + diff(lambda t: log(Lbeta(t)), mpf(1)/2, 2)
C_direct = diff(logLambda, mpf(1)/2, 2)
psi1_34 = pi**2 - 8*catalan
print("E. C =", mp.nstr(C_exact, 25))
print("   (log Lambda)''(1/2)      =", mp.nstr(C_direct, 25))
print("   psi'(3/4) check: |polygamma - (pi^2-8G)| =",
      float(fabs(polygamma(1, mpf(3)/4) - psi1_34)))
assert fabs(C_exact - C_direct) < mpf(10)**-38
assert fabs(C_exact - mpf('0.15602964988964488')) < mpf(10)**-16
zsC = sum(2/g**2 for g in gammas)
tailC = (log(2*G/pi) + 1) / (pi*G)          # (1/pi) int_G^inf t^-2 log(2t/pi) dt
print("   zero-sum 511 terms = %.6f ; RvM tail = %.6f ; sum = %.6f "
      "(paper printed 0.156033; exact %.6f; discrepancy %.1e)"
      % (float(zsC), float(tailC), float(zsC+tailC), float(C_exact),
         float(zsC + tailC - C_exact)))

# ---------- F. asymptotics, c0 = 1 and next term 1/12 ----------
print("F. d(m) = sigma_m^2 - 2M log(4M/(2pi));  M*(d-1) -> 1/12 = 0.08333...")
for m in (1, 3, 8, 20, 100, 400, 1000):
    M = m + mpf(1)/2
    d = sigma2_closed(m) - 2*M*log(4*M/(2*pi))
    print("   m=%5d  d=%.10f   d-1=% .3e   M*(d-1)=% .6f" %
          (m, float(d), float(d-1), float(M*(d-1))))
m = 1000; M = m + mpf(1)/2
assert fabs(sigma2_closed(m) - 2*M*log(4*M/(2*pi)) - 1) < mpf('1e-4')
assert fabs(M*(sigma2_closed(m) - 2*M*log(4*M/(2*pi)) - 1) - mpf(1)/12) < mpf('1e-3')

# ---------- G. general q: even character mod 5 ----------
def L5(s):   # Legendre symbol mod 5: +1 at 1,4; -1 at 2,3 — even, a=0
    return 5**(-s) * (zeta(s, mpf(1)/5) - zeta(s, mpf(2)/5)
                      - zeta(s, mpf(3)/5) + zeta(s, mpf(4)/5))
def logLambda5(s):
    return s/2 * log(5/pi) + loggamma(s/2) + log(L5(s))
print("G. q=5 (even, a=0): L(1/2,chi5) =", mp.nstr(L5(mpf(1)/2), 10))
for m in (8, 100, 1000):
    M = m + mpf(1)/2
    v = 4*M*diff(logLambda5, m+1)
    d = v - 2*M*log(5*M/(2*pi))
    print("   m=%5d  Var_5=%.6f  d=% .8f  (-> -1)  M*(d+1)=% .6f" %
          (m, float(v), float(d), float(M*(d+1))))
m = 1000; M = m + mpf(1)/2
assert fabs(4*M*diff(logLambda5, m+1) - 2*M*log(5*M/(2*pi)) + 1) < mpf('1e-4')

# ---------- H. tex table ----------
print("H. table for the tex file (6 decimals):")
print("   m      sigma^2         2Mlog(4M/2pi)   +1(new law)     "
      "sigma^2-law-1     tail var at G")
for m in (1, 3, 8, 20, 100):
    M = m + mpf(1)/2
    s2 = sigma2_closed(m)
    law = 2*M*log(4*M/(2*pi))
    tailvar = s2 - a2sum(m)
    print("   %-4d  %-14s  %-14s  %-14s  % .6f   %s" %
          (m, mp.nstr(s2, 9), mp.nstr(law, 9), mp.nstr(law+1, 9),
           float(s2-law-1), mp.nstr(tailvar, 6)))
print("   L'/L(m+1,chi4) magnitude (odd-prime decay):")
for m in (1, 8, 20):
    print("     m=%2d  |L'/L| = %.3e   3^-(m+1) log3 = %.3e" %
          (m, float(fabs(diff(lambda t: log(Lbeta(t)), m+1))),
           float(3**(-(m+1))*log(3))))

# ---------- I. density shift from exact vs estimated tail variance ----------
# Reproduces the "at most 4.3e-6, worst at q=3, m=1" claim of the
# certified-tails remark by re-running the Gil-Pelaez inversion of
# race_density_exact.py with both tail variances, at the worst and the
# extreme-m cases.  Requires numpy+scipy (the density code's stack).
try:
    import math
    import numpy as np
    from scipy.special import j0
    import sys
    EXPL = os.path.join(HERE, '..', '..', 'prototype', 'explore')
    sys.path.insert(0, EXPL)
    from race_density_exact import tail_var

    def L3(s):
        with workdps(mp.dps + 80):
            v = 3**(-s) * (zeta(s, mpf(1)/3) - zeta(s, mpf(2)/3))
        return +v

    def var_exact(q, m):
        if q == 4:
            return sigma2_closed(m)
        M = m + mpf(1)/2
        f = lambda s: (s+1)/2*log(3/pi) + loggamma((s+1)/2) + log(L3(s))
        return 4*M*diff(f, m+1)

    def gp_delta(m, gam, tv):
        a = (2*m+1)/np.sqrt((m+0.5)**2+gam**2)
        T = min(max(60.0, 12.0/math.sqrt(tv) if tv > 0 else 400.0), 4000.0)
        t = np.linspace(1e-9, T, 400000)
        lg = np.zeros_like(t); sgn = np.ones_like(t)
        for av in a:
            v = j0(2*av*t)
            lg += np.log(np.abs(v) + 1e-300); sgn *= np.sign(v)
        phi = sgn*np.exp(lg - tv*t*t/2)
        return 0.5 + np.trapezoid(phi*np.sin(t)/t, t)/math.pi

    print("I. density shift, estimated -> exact tail variance:")
    worst = 0.0
    for q, zf, m in ((4, 'chi4_zeros.txt', 1), (4, 'chi4_zeros.txt', 100),
                     (3, 'chi3_zeros.txt', 1)):
        gam = np.loadtxt(os.path.join(EXPL, zf))
        tv_est = tail_var(float(m), gam[-1], q)
        zsum = float(np.sum(2*(2*m+1)**2/((m+0.5)**2+gam*gam)))
        tv_ex = float(var_exact(q, m)) - zsum
        d_est = gp_delta(float(m), gam, tv_est)
        d_ex = gp_delta(float(m), gam, tv_ex)
        shift = d_ex - d_est
        worst = max(worst, abs(shift))
        print("   q=%d m=%3d  tv est=%.6f exact=%.6f  delta %.7f -> %.7f  "
              "shift=%+.2e" % (q, m, tv_est, tv_ex, d_est, d_ex, shift))
    # This compares the two *Gaussian-tail* inversions before the proved
    # quartic tail correction is applied.  The largest shift is at (3,1).
    # An older 3.3e-6 threshold mistakenly compared this unrounded value
    # with the rounded six-decimal table entry.
    assert worst < 4.3e-6
    print("   worst |shift| = %.2e < 4.3e-6" % worst)
except ImportError as e:
    print("I. SKIPPED (numpy/scipy not available: %s) -- the density-shift"
          " numbers in the certified-tails remark are then unverified" % e)

print("ALL CHECKS PASSED")
