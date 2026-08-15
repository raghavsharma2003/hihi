#!/usr/bin/env python3
"""
race_density_certified.py -- rigorous enclosures [lo, hi] for the
Rubinstein-Sarnak logarithmic densities delta_q(m) of the weighted prime
races mod 4 and mod 3, replacing the estimated Gaussianized tail of
race_density_exact.py / race_density.py by a certified one.

Conditionality (stated once, applies to every number printed):
  * GRH(chi) + LI(chi) for the limiting-variable model (as everywhere in
    this literature);
  * completeness of the computed ordinate list up to its last entry
    Gamma (511 ordinates for chi_4, 537 for chi_3, 25 digits each,
    validated upstream by Riemann-von Mangoldt counts and Hardy Z-scans;
    a soft RvM count check is repeated below);
  * the closed-form variance sigma_m^2 = 4M (log Lambda)'(m+1) (proved
    under GRH in paper/v3/variance-identity.tex) evaluated by mpmath at
    40 digits -- high-precision floating point cross-checked by
    independent routes and closed-form anchors, not interval arithmetic;
    a defensive slack SLV = 1e-15 is budgeted for it and for the
    25-digit ordinate rounding (whose actual effect is < 1e-20).

Model. delta_q(m) = P(1 + V > 0), V = sum_{gamma>0} 2 a_gamma cos(theta_gamma),
a_gamma(m) = 2M/sqrt(M^2+gamma^2), M = m+1/2, phases iid uniform (LI).
Characteristic function Phi(t) = prod_{gamma>0} J0(2 a_gamma t)
                              = P(t) * Psi(t),
P over the computed ordinates, Psi over the unseen tail gamma > Gamma.
Since |Phi(t)| <= prod_{i<=K} min(1, sqrt(2/(pi 2 a_i t))) is integrable,
V has a continuous density and Gil-Pelaez gives exactly
  delta = 1/2 + (1/pi) int_0^inf Phi(t) sin(t)/t dt.

Certified pieces.
(1) Tail variance:  V_T = sigma_m^2 - sum_{computed} 2 a_gamma^2, with
    sigma_m^2 from the Hadamard identity (no zero-counting estimate).
    Abort if V_T <= 0.
(2) a_gamma is strictly decreasing in gamma (a'(gamma) < 0), so for
    t <= t_max := 1/(2 a(Gamma)) every tail argument obeys |2 a_gamma t| <= 1.
    For |z| <= 1,
        0 <= -log J0(z) - z^2/4 <= c4 z^4,
        c4 = -log J0(1) - 1/4 = 0.017621064...
    PROOF (sharp constant): J0(z) = prod_n (1 - z^2/j_{0,n}^2), so
    -log J0(z) = sum_{k>=1} (sigma_k/k) z^{2k} with sigma_k =
    sum_n j_{0,n}^{-2k} > 0 (Rayleigh sums), valid for |z| < j_{0,1} = 2.40...;
    sigma_1 = 1/4 (Rayleigh), and z^{2k} <= z^4 for k >= 2, |z| <= 1, so
    -log J0(z) - z^2/4 = sum_{k>=2}(sigma_k/k) z^{2k} lies in
    [0, c4 z^4] with c4 = sum_{k>=2} sigma_k/k = -log J0(1) - 1/4.
    We use the rounded-up constant C4 = 0.018 and verify the inequality
    numerically on a dense grid as well.
    Hence Psi(t) = exp(-V_T t^2/2 + eps(t)) for 0 <= t <= t_max with
        -C4 * S4 * t^4 <= eps(t) <= 0,
        S4 = sum_{gamma>Gamma} (2 a_gamma)^4 <= (2 a_Gamma)^2 * 2 V_T
    (since (2a)^4 <= (2 a_Gamma)^2 (2a)^2 for tail gammas and
    sum_{tail} (2a)^2 = 2 * sum_{tail} 2 a^2 = 2 V_T).  The sign
    information is exploited: with w := C4 S4 t^4, e^{eps} lies in
    [e^{-w}, 1], so it is enclosed by its midpoint,
        |e^{eps(t)} - (1+e^{-w})/2| <= (1-e^{-w})/2,
    which halves the tail-model radius relative to the symmetric
    bound e^{w}-1.
(3) Truncation: |J0(x)| <= min(1, B/sqrt(x)) with B = 0.8 > sqrt(2/pi)
    (classical envelope, numerically re-verified below), so for any K
        |int_{T1}^inf Phi sin(t)/t dt|
          <= (B^K / sqrt(prod_{i<=K} 2 a_i)) * T1^{-K/2} / (K/2)  =: E2*pi/pi,
    using |sin t/t| <= 1/t and |remaining factors| <= 1.

Enclosure.  delta = 1/2 + (1/pi)(I_main + R), where
  I_main = int_0^{T1} P(t) e^{-V_T t^2/2} ((1+e^{-w})/2) sin(t)/t dt (computed),
  |R| <= E1 + E2, with
  E1 = int_0^{T1} |P(t)| e^{-V_T t^2/2} ((1-e^{-w})/2) dt  (tail-model radius),
  E2 as above (truncation), T1 <= t_max.
Estimated (NOT certified) pieces, budgeted into the radius and stated
honestly: quadrature error E3 of I_main (composite Simpson, step-doubling
Richardson difference, floored at 1e-12); E1's own quadrature (inflated
by 1.5); double-precision rounding of the 511-fold J0 product and the
V_T slack sensitivity (E4 = 2e-11 + SLV * int (t^2/2)|P|G dt).

Output: for each modulus a table  m, delta_lo, delta_hi, width, plus a
comparison against the six-decimal values printed in the paper.
"""
import os
import sys
import math
import numpy as np
from scipy.special import j0 as J0f
from scipy.integrate import simpson
from mpmath import (mp, mpf, mpc, log, exp, pi, loggamma, digamma, sqrt,
                    fabs, diff, euler, stieltjes, besselj, workdps,
                    catalan, nsum, inf)

mp.dps = 40
GUARD = 100          # guard digits inside the Hurwitz representation of L
HERE = os.path.dirname(os.path.abspath(__file__))

C4 = 0.018           # >= c4 = -log J0(1) - 1/4 = 0.01762106...  (proved sharp)
BENV = 0.8           # >= sqrt(2/pi) = 0.7978846  (J0 envelope constant)
SLV = mpf(10)**-15   # defensive slack on the certified tail variance
E2_TARGET = 1e-15
NFINE = 2**17        # Simpson intervals on [0, T1]

# ---------------------------------------------------------------- L-functions
def L_hurwitz(q, s):
    """L(s,chi_q) for the odd real primitive character mod q in {3,4},
    via Hurwitz zetas with guard digits (their shared pole at s=1 cancels
    catastrophically under numerical differentiation otherwise)."""
    with workdps(mp.dps + GUARD):
        if q == 4:
            v = 4**(-s) * (mp.zeta(s, mpf(1)/4) - mp.zeta(s, mpf(3)/4))
        elif q == 3:
            v = 3**(-s) * (mp.zeta(s, mpf(1)/3) - mp.zeta(s, mpf(2)/3))
        else:
            raise ValueError(q)
    return +v

def logLambda(q, s):
    """log of the completed L: Lambda = (q/pi)^{(s+1)/2} Gamma((s+1)/2) L
    (both characters are odd, a=1, root number +1)."""
    return (s+1)/2 * log(mpf(q)/pi) + loggamma((s+1)/2) + log(L_hurwitz(q, s))

def sigma2(q, m):
    """sigma_m^2 = 4M (log Lambda)'(m+1); two evaluation routes must agree."""
    M = mpf(m) + mpf(1)/2
    rA = 4*M*diff(lambda t: logLambda(q, t), mpf(m) + 1)
    rB = 4*M*(log(mpf(q)/pi)/2 + digamma((mpf(m)+2)/2)/2
              + diff(lambda t: log(L_hurwitz(q, t)), mpf(m) + 1))
    assert fabs(rA - rB) < mpf(10)**-25 * max(1, fabs(rA)), (q, m, rA, rB)
    return rA

# ------------------------------------------------------------------- anchors
def run_anchors():
    print("== anchors and sanity checks ==")
    # exact special values (the Hurwitz form has a pole at s=1, so anchor
    # at the regular point s=2: L(2,chi4) = Catalan's constant; L(2,chi3)
    # summed directly from its absolutely convergent Dirichlet series)
    L2_4 = L_hurwitz(4, mpf(2))
    assert fabs(L2_4 - catalan) < mpf(10)**-35, "L(2,chi4) != Catalan"
    L2_3_series = nsum(lambda k: 1/(3*k+1)**2 - 1/(3*k+2)**2, [0, inf])
    L2_3 = L_hurwitz(3, mpf(2))
    assert fabs(L2_3 - L2_3_series) < mpf(10)**-30, "L(2,chi3) series mismatch"
    print("  L(2,chi4)=Catalan ok;  L(2,chi3)=direct-series ok")
    # central values positive (chi4: alternating series; chi3: positive
    # 3-blocks 1/sqrt(3k+1) - 1/sqrt(3k+2) of the conditionally convergent
    # Dirichlet series -- both unconditional)
    Lh4 = L_hurwitz(4, mpf(1)/2); Lh3 = L_hurwitz(3, mpf(1)/2)
    assert Lh4 > mpf('0.6') and Lh3 > mpf('0.4')
    print("  L(1/2,chi4) = %s   L(1/2,chi3) = %s  (both > 0)" %
          (mp.nstr(Lh4, 20), mp.nstr(Lh3, 20)))
    # L'/L(1) by generalized Stieltjes constants (independent of diff())
    lpl4_st = -log(mpf(4)) - (stieltjes(1, mpf(1)/4) - stieltjes(1, mpf(3)/4))/pi
    lpl4_cf = euler + 2*log(mpf(2)) + 3*log(pi) - 4*loggamma(mpf(1)/4)
    lpl4_df = diff(lambda t: log(L_hurwitz(4, t)), mpf(1))
    assert fabs(lpl4_st - lpl4_cf) < mpf(10)**-30
    assert fabs(lpl4_st - lpl4_df) < mpf(10)**-25
    lpl3_st = -log(mpf(3)) - (stieltjes(1, mpf(1)/3) - stieltjes(1, mpf(2)/3))/(pi/sqrt(mpf(3)))
    lpl3_df = diff(lambda t: log(L_hurwitz(3, t)), mpf(1))
    assert fabs(lpl3_st - lpl3_df) < mpf(10)**-25
    print("  L'/L(1) anchors: chi4 stieltjes/closed-form/diff agree to >=25 dg;"
          " chi3 stieltjes/diff agree to >=25 dg")
    # sigma^2(0) anchors
    s2_4 = sigma2(4, 0)
    anchor4 = 2*(log(mpf(4)/pi)/2 + digamma(mpf(1))/2 + lpl4_cf)
    assert fabs(s2_4 - anchor4) < mpf(10)**-25
    assert fabs(s2_4 - mpf('0.15556797992358592886')) < mpf(10)**-18, s2_4
    s2_3 = sigma2(3, 0)
    anchor3 = 2*(log(mpf(3)/pi)/2 + digamma(mpf(1))/2 + lpl3_st)
    assert fabs(s2_3 - anchor3) < mpf(10)**-25
    print("  sigma^2(0): chi4 = %s (matches corrected v3 value)" % mp.nstr(s2_4, 20))
    print("              chi3 = %s" % mp.nstr(s2_3, 20))
    # context values from the v3 verification run (12 digits)
    ctx = {1: '1.36855505395', 2: '3.64763501678', 3: '6.77684634861',
           8: '29.7124677146', 20: '106.325999646', 100: '836.874383888'}
    for m, v in ctx.items():
        s2 = sigma2(4, m)
        assert fabs(s2 - mpf(v)) < mpf(10)**-9 * max(1, fabs(s2)), (m, s2)
    print("  sigma^2(m), q=4, m=1..100: matches 12-digit reference values")
    # c4 constant: sharp value and grid verification of the bound
    c4_true = -log(besselj(0, 1)) - mpf(1)/4
    assert C4 > float(c4_true), (C4, c4_true)
    # (-log J0(z) - z^2/4)/z^4 = sum_{k>=2}(sigma_k/k) z^{2k-4} has positive
    # coefficients, hence is increasing on (0,1] with sup = c4 at z=1; the
    # grid check below confirms this on [0.05, 1] (below 0.05 the double-
    # precision difference cancels catastrophically, and the series bound
    # ratio in [1/64, c4] applies analytically).
    z = np.linspace(0.05, 1.0, 20001)
    ratio = (-np.log(J0f(z)) - z*z/4)/z**4
    assert np.all(ratio > 1/64 - 1e-6) and ratio.max() <= float(c4_true) + 1e-9
    assert np.all(np.diff(ratio) > -1e-12)
    print("  c4 = -log J0(1) - 1/4 = %s; grid max of (-log J0 - z^2/4)/z^4 = %.9f;"
          " using C4 = %.3f" % (mp.nstr(c4_true, 12), ratio.max(), C4))
    # J0 envelope constant
    x = np.linspace(1e-4, 500.0, 2_000_001)
    env = np.sqrt(x)*np.abs(J0f(x))
    assert env.max() < 0.7989, env.max()
    x2 = np.linspace(500.0, 1e5, 10_000_001)
    env2 = np.sqrt(x2)*np.abs(J0f(x2))
    assert env2.max() < 0.7979, env2.max()
    print("  sup sqrt(x)|J0(x)| on (0,500] = %.6f, on [500,1e5] = %.12f,"
          " both < sqrt(2/pi) = %.12f; using B = %.2f"
          % (env.max(), env2.max(), math.sqrt(2/math.pi), BENV))
    # (beyond: the Hankel asymptotic modulus is sqrt(2/(pi x))(1 - 1/(8x^2)
    #  + O(x^-4)) < sqrt(2/(pi x)); the classical envelope is not re-proved
    #  here -- see the stated-gaps list.)

def load_zeros(fname, q):
    path = os.path.join(HERE, fname)
    with open(path) as f:
        gam_mpf = [mpf(line.strip()) for line in f if line.strip()]
    gam_f = np.array([float(g) for g in gam_mpf])
    assert np.all(np.diff(gam_f) > 0) and gam_f[0] > 0
    # first ordinates really are zeros of Lambda
    for g in gam_mpf[:3]:
        s = mpc(mpf(1)/2, g)
        val = fabs((mpf(q)/pi)**((s+1)/2) * mp.gamma((s+1)/2) * L_hurwitz(q, s))
        assert val < mpf(10)**-19, (q, g, val)
    # soft Riemann-von Mangoldt completeness check (both-signs count)
    T = gam_f[-1] + 0.5
    smooth = (T/math.pi)*math.log(q*T/(2*math.pi*math.e))
    dev = smooth - 2*len(gam_f)
    assert abs(dev) < 8, dev
    print("  %s: %d ordinates in (0, %.4f]; RvM smooth count %.1f vs %d"
          " (deviation %+.1f, within S(T) fluctuation)" %
          (fname, len(gam_f), gam_f[-1], smooth, 2*len(gam_f), dev))
    return gam_mpf, gam_f

# ------------------------------------------------------------- the enclosure
def enclose(q, m, gam_mpf, gam_f, s2):
    M = mpf(m) + mpf(1)/2
    # certified tail variance
    Sfin = mpf(0)
    for g in gam_mpf:
        Sfin += 8*M*M/(M*M + g*g)
    VT = s2 - Sfin
    if not VT > 10*SLV:
        raise SystemExit("V_T <= 0 at (q,m)=(%d,%d): %s" % (q, m, mp.nstr(VT, 10)))
    Gam = gam_mpf[-1]
    twoaG = 4*M/sqrt(M*M + Gam*Gam)               # 2 a(Gamma)
    tmax = float(1/twoaG)
    S4b = float(twoaG**2 * 2 * (VT + SLV))        # >= sum_tail (2a)^4
    VTf = float(VT)
    c4S4 = C4 * S4b

    a_f = (2*m + 1)/np.sqrt((m + 0.5)**2 + gam_f**2)
    assert np.all(np.diff(a_f) < 0)               # a_gamma decreasing

    # choose K and T1: E2(T1) = A * T1^{-K/2} / (pi K/2) with
    # A = B^K / sqrt(prod_{i<=K} 2 a_i)
    best = None
    for K in (24, 32, 40, 56, 72):
        K = min(K, len(a_f))
        logA = K*math.log(BENV) - 0.5*np.sum(np.log(2*a_f[:K]))
        # T needed for E2 = E2_TARGET
        logT_req = (logA - math.log(math.pi*(K/2)*E2_TARGET)) * (2.0/K)
        T1_K = min(tmax, math.exp(logT_req))
        logE2 = logA - (K/2)*math.log(T1_K) - math.log(math.pi*K/2)
        cand = (logE2, T1_K, K)
        if best is None or cand[0] < best[0]:
            best = cand
    logE2, T1, K = best
    E2 = math.exp(logE2)*math.pi   # raw-integral convention; radius divides by pi
    # (logE2 above already divided by pi; undo so that all E_i share the
    #  convention "radius = (E1+E2+E3+E4)/pi")
    assert E2 <= math.pi*E2_TARGET*(1 + 1e-9), (q, m, E2)

    # quadrature grid
    t = np.linspace(0.0, T1, NFINE + 1)
    dx = T1/NFINE
    logabs = np.zeros_like(t)
    sgn = np.ones_like(t)
    for av in a_f:
        v = J0f(2*av*t)
        sgn *= np.where(v >= 0, 1.0, -1.0)
        logabs += np.log(np.abs(v) + 1e-300)
    absP = np.exp(logabs)
    G = np.exp(-VTf*t*t/2)
    # one-sided tail model: Psi = G e^{eps}, eps in [-w, 0], w = c4S4 t^4;
    # enclose e^{eps} by its midpoint (1+e^{-w})/2 with radius (1-e^{-w})/2
    w = c4S4 * t**4
    emw = np.exp(-w)
    main = sgn*absP*G*((1.0 + emw)/2.0)*np.sinc(t/np.pi)
    I_fine = simpson(main, dx=dx)
    I_half = simpson(main[::2], dx=2*dx)
    E3 = abs(I_fine - I_half) + 1e-12

    # E1: tail-model (quartic) radius, |Psi/G - (1+e^{-w})/2| <= (1-e^{-w})/2
    E1 = 1.5*simpson(absP*G*(-np.expm1(-w))/2.0, dx=dx)

    # E4: slack sensitivity + double-precision product rounding
    EVsens = float(SLV)*simpson(absP*G*t*t/2, dx=dx)
    E4 = 2e-11 + EVsens

    R = (E1 + E2 + E3 + E4)/math.pi
    center = 0.5 + I_fine/math.pi
    return dict(q=q, m=m, VT=VT, tmax=tmax, T1=T1, K=K, S4b=S4b,
                E1=E1, E2=E2, E3=E3, E4=E4, R=R,
                center=center, lo=center - R, hi=center + R, width=2*R)

PRINTED = {(4, 0): 0.995928, (4, 1): 0.797628, (4, 2): 0.694520,
           (4, 3): 0.645850, (4, 8): 0.571869, (4, 20): 0.538455,
           (4, 100): 0.513778,
           (3, 0): 0.999063, (3, 1): 0.836877, (3, 2): 0.723470,
           (3, 3): 0.666552, (3, 8): 0.578534, (3, 20): 0.540767,
           (3, 60): 0.519716}

def main():
    run_anchors()
    # the constant C = sum 2/gamma^2 for both moduli (paper cross-reference)
    C4const = diff(lambda t: logLambda(4, t), mpf(1)/2, 2)
    C3const = diff(lambda t: logLambda(3, t), mpf(1)/2, 2)
    print("  C(chi4) = (log Lambda_4)''(1/2) = %s" % mp.nstr(C4const, 25))
    print("  C(chi3) = (log Lambda_3)''(1/2) = %s" % mp.nstr(C3const, 25))
    print()

    for q, fname, ms in [(4, "chi4_zeros.txt", [0, 1, 2, 3, 8, 20, 100]),
                         (3, "chi3_zeros.txt", [0, 1, 2, 3, 8, 20, 60])]:
        print("== modulus %d ==" % q)
        gam_mpf, gam_f = load_zeros(fname, q)
        rows = []
        for m in ms:
            s2 = sigma2(q, m)
            r = enclose(q, m, gam_mpf, gam_f, s2)
            rows.append(r)
            print("  m=%3d  sigma^2=%-16s V_T=%-13s tmax=%8.3f T1=%8.3f K=%d"
                  % (m, mp.nstr(s2, 12), mp.nstr(r['VT'], 8),
                     r['tmax'], r['T1'], r['K']))
            print("         E1=%.2e E2=%.2e E3=%.2e E4=%.2e" %
                  (r['E1'], r['E2'], r['E3'], r['E4']))
        print()
        print("  %-4s %-14s %-14s %-9s %-10s %s" %
              ("m", "delta_lo", "delta_hi", "width", "paper", "delta-paper"))
        for r in rows:
            p = PRINTED.get((q, r['m']))
            d = r['center'] - p
            flag = "  <-- DISCREPANCY > 1e-6" if abs(d) > 1e-6 else ""
            print("  %-4d %.10f  %.10f  %.2e  %8.6f  %+.2e%s" %
                  (r['m'], r['lo'], r['hi'], r['width'], p, d, flag))
        print()

if __name__ == "__main__":
    main()
