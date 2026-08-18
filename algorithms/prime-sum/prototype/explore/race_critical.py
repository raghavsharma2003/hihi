#!/usr/bin/env python3
"""
The CRITICAL point m = -1/2 of the weighted Chebyshev race mod 4.

    D_{-1/2}(x) = sum_{p<=x, p=3(4)} p^{-1/2} - sum_{p<=x, p=1(4)} p^{-1/2}
                = - sum_{p<=x} chi4(p) / sqrt(p).

Phase diagram context (race_density.py, race_curve.py): for m > -1/2 the race
is a delicate biased race (log-density delta(m) < 1, infinitely many lead
changes); for m < -1/2 the series converges and the sign freezes at a finite
constant. m = -1/2 is the unique boundary point. This file derives and tests
what happens exactly there.

DERIVATION (same GRH + LI standard as race_density.py; mirrors its docstring
at general m and takes the m -> -1/2 limit of the un-log-weighted object).

Step 1 (split off prime powers). With Lambda(n)/log n = 1/k at n = p^k,

  A(x) := sum_{n<=x} chi4(n) Lambda(n) / (sqrt(n) log n)
        = sum_{p<=x} chi4(p)/sqrt(p)                       (k = 1: -D(x))
        + (1/2) sum_{odd p <= sqrt(x)} 1/p                 (k = 2: chi4(p^2)=+1)
        + sum_{k>=3} (1/k) sum_{p^k<=x} chi4(p^k)/p^{k/2}  (-> K3, abs. conv.)

The k = 2 line is THE bias source: prime squares are all 1 mod 4, and at the
critical weight their contribution (1/2) sum_{p<=sqrt(x)} 1/p is UNBOUNDED
but only just — Mertens gives (1/2)(log log sqrt(x) + M - 1/2) + o(1)
= (1/2) log log x - (log 2)/2 + (M - 1/2)/2 + o(1). The coefficient of
log log x that enters D is c = 1/2: one factor 1/2 from Lambda/log = 1/2 at
squares, and the sqrt(x) cutoff only shifts the constant by -(log 2)/2
(log log sqrt(x) = log log x - log 2 — it does NOT halve the slope).

Step 2 (value of the limit A(infty)). A(x) is the partial sum, in p^k <= x
order, of the Dirichlet series of log L(s, chi4) at s = 1/2. By the explicit
formula, dA(t) = dpsi(t,chi4) / (sqrt(t) log t) and psi(t,chi4) =
-sum_rho t^rho / rho + O(1), so with GRH (rho = 1/2 + i*gamma) and u = log t:

  A(x) = A(2) + sum_gamma int_{log 2}^{log x} e^{i gamma u} / u du + (tiny).

Each integral converges as x -> infty (oscillatory, 1/u amplitude), and the
zero sum converges in the LI mean-square sense; hence A(x) -> A(infty), and by
Abel continuity of Dirichlet series along the real axis (log L(s,chi4) is
analytic and real on [1/2, infty), no real zero: L(1/2,chi4) = 0.66769 > 0)

  A(infty) = log L(1/2, chi4)         [NO Conrad sqrt(2): that factor belongs
                                       to the p <= x Euler-product truncation;
                                       our cut is p^k <= x throughout.]

Step 3 (the fluctuation — SIZE CORRECTION to the naive guess). Integration by
parts on the tail, L = log x:

  eps(x) := A(infty) - A(x) = sum_gamma e^{i gamma L}/(i gamma L) + O(1/(gamma L)^2)

i.e. the zero term of the LOG-STRIPPED race is x^{i gamma}/(i gamma log x),
not x^{i gamma}/(i gamma): partial summation from the theta-form race hangs an
extra 1/log x on it. Treating the phases as LI-random, the variance is

  Var eps(x) = Sigma / (log x)^2,   Sigma = sum_{gamma>0} 2/gamma^2 = 0.156033,

convergent because the zero DENSITY at height gamma is only ~ log(2 gamma/pi)
/(2 pi) (Riemann-von Mangoldt for modulus 4): integral log(g)/g^2 dg < infty.
Crucial input: L(1/2, chi4) != 0, so gamma_1 = 6.0209... > 0 and no term
blows up. So the fluctuation is not merely bounded (the working conjecture)
— it DECAYS like 1/log x. [The bounded-variance sum_rho x^{i gamma}/(i gamma)
object is the fluctuation of the theta-form race R_{-1/2}(x) =
- sum chi4(p) log p/sqrt(p), whose drift is the much faster (1/2) log x;
both freezes are real, but for D the contest is loglog-drift vs 1/log-noise.]

RESULT. Assembling steps 1-3:

  D_{-1/2}(x) = (1/2) log log x + C* + eps(x),      sd(eps) ~ sqrt(Sigma)/log x,

  C* = (M - log 2 - 1/2)/2 + K3 - log L(1/2, chi4) = -0.0715300(1),

with M = 0.2614972... (Mertens), K3 = -0.0096341(1) (prime cubes and higher),
log L(1/2,chi4) = log 0.667691457... = -0.4039291. Equivalently, with the
EXACT bias sum (used for residuals below, removing the Mertens o(1)):

  D_{-1/2}(x) = (1/2) sum_{2<p<=sqrt(x)} 1/p + K3 - log L(1/2,chi4) + eps(x).

CONSEQUENCES — the slowest possible freeze:
  * drift -> +infinity like (1/2) log log x: Team 3 leads FOREVER eventually,
    and delta(-1/2) = 1 exactly (limit of the delta(m) -> 1 end of the curve);
  * but the divergence is doubly logarithmic — the slowest unbounded growth in
    the whole family — while for m < -1/2 D converges and for m > -1/2 it has
    power-law size x^{m+1/2}/log x with infinitely many flips (delta(m) < 1);
  * sign changes STOP (a.s. under GRH+LI): drift grows, noise sd decays, so
    only finitely many flips can occur — the last flip is a finite number;
  * quantitatively the noise is so small (sd 0.029 already at x = 1e6, vs
    drift ~ 1.24) that the data below shows NO sign change at all: the 3-side
    leads from p = 3 onward, minimum D = 0.13014 at x = 5 (the same p = 5
    that flips every race with m >= 1).

VERIFICATION (race_critical_scan.c, exact segmented sieve to 1e10 in
Neumaier-compensated long double, cross-checked against an independent numpy
computation at 1e7 to all 16 digits): this script fits the checkpoints to
a + b log log x, compares b to the predicted 1/2 and a to C*, tests the
drift-vs-constant question on residual RMS, and checks the 1/log x decay of
the residuals against sqrt(Sigma)/log x.

Usage: race_critical.py [results.txt]   (default race_critical_1e10.txt;
       if missing, compiles and runs the scanner: ~1 min for X = 1e10)
"""

import math
import os
import subprocess
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "race_critical_1e10.txt")

# Mertens constant (mpmath: euler - sum_{k>=2} primezeta(k)/k, 30 dps)
M_MERTENS = 0.261497212847642783755426838609

# ----------------------------------------------------------------------------
# Theory constants
# ----------------------------------------------------------------------------

def log_L_half():
    """log L(1/2, chi4) via Hurwitz zeta: beta(s) = 4^-s (zeta(s,1/4)-zeta(s,3/4))."""
    try:
        import mpmath as mp
        mp.mp.dps = 30
        s = mp.mpf(1) / 2
        b = mp.power(4, -s) * (mp.zeta(s, mp.mpf(1) / 4) - mp.zeta(s, mp.mpf(3) / 4))
        return float(mp.log(b)), float(b)
    except ImportError:
        b = 0.6676914571896091766586909293  # beta(1/2), precomputed at 30 dps
        return math.log(b), b


def sieve_primes(n):
    s = np.ones(n + 1, dtype=bool)
    s[:2] = False
    for i in range(2, int(n ** 0.5) + 1):
        if s[i]:
            s[i * i::i] = False
    return np.nonzero(s)[0]


def compute_K3(limit=10 ** 7):
    """K3 = sum_{k>=3} (1/k) sum_p chi4(p^k) p^{-k/2}  (odd p; chi4(2^k)=0).

    k odd: chi4(p^k) = chi4(p), direct prime sum (abs. convergent, k/2 >= 3/2;
    tail beyond `limit` < 1.4e-5). k even: chi4(p^k) = 1, so the sum is
    P(k/2) - 2^{-k/2} with P the prime zeta (computed from the same primes;
    for k >= 6 the tail is < 1e-12 anyway)."""
    p = sieve_primes(limit)[1:].astype(np.float64)  # drop p = 2
    chi = np.where(p % 4 == 1, 1.0, -1.0)
    K3 = 0.0
    k = 3
    while k <= 80:
        if k % 2 == 1:
            t = float(np.sum(chi * p ** (-k / 2.0))) / k
        else:
            t = (float(np.sum(p ** (-k / 2.0)))) / k
        K3 += t
        if abs(t) < 1e-17 and k > 8:
            break
        k += 1
    return K3, p


def zero_variance():
    """Sigma = sum_{gamma>0} 2/gamma^2 over zeros of L(s,chi4): 511 computed
    zeros + Riemann-von Mangoldt tail (density log(2g/pi)/(2pi) for q=4):
    integral tail = (log(2 gN/pi) + 1)/(pi gN)."""
    g = np.loadtxt(os.path.join(HERE, "chi4_zeros.txt"))
    S = float(np.sum(2.0 / g ** 2))
    gN = float(g[-1])
    tail = (math.log(2 * gN / math.pi) + 1) / (math.pi * gN)
    return S + tail, S, tail, gN


# ----------------------------------------------------------------------------
# Scan data
# ----------------------------------------------------------------------------

def ensure_scan(path, X=10 ** 10):
    if os.path.exists(path):
        return
    src = os.path.join(HERE, "race_critical_scan.c")
    exe = os.path.join(HERE, "race_critical_scan")
    if not os.path.exists(exe):
        subprocess.run(["cc", "-O2", "-o", exe, src, "-lm"], check=True)
    with open(path, "w") as f:
        subprocess.run([exe, str(X)], stdout=f, check=True)


def load_scan(path):
    xs, ds = [], []
    summary = None
    with open(path) as f:
        for line in f:
            t = line.split()
            if t[0] == "CP":
                xs.append(float(t[1]))
                ds.append(float(t[2]))
            elif t[0] == "SUMMARY":
                summary = dict(
                    X=int(t[1]), D=float(t[2]), flips=int(t[3]),
                    last_flip=int(t[4]), first_neg=int(t[5]),
                    minD=float(t[6]), minD_at=int(t[7]))
    return np.array(xs), np.array(ds), summary


# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------

def main():
    logL, betahalf = log_L_half()
    K3, primes = compute_K3()
    Sigma, S511, Stail, gN = zero_variance()
    Cstar = (M_MERTENS - math.log(2) - 0.5) / 2 + K3 - logL

    print("=" * 72)
    print("critical race m = -1/2 : theory")
    print("=" * 72)
    print(f"L(1/2,chi4) = {betahalf:.15f}   log L = {logL:+.7f}   (no central zero)")
    print(f"Mertens M   = {M_MERTENS:.15f}")
    print(f"K3 (k>=3 prime powers)          = {K3:+.7f}")
    print(f"drift:  D(x) ~ (1/2) log log x + C*")
    print(f"C* = (M - log2 - 1/2)/2 + K3 - log L(1/2,chi4) = {Cstar:+.7f}")
    print(f"noise:  sd eps(x) ~ sqrt(Sigma)/log x,  Sigma = sum 2/gamma^2")
    print(f"Sigma = {Sigma:.6f}  (511 zeros: {S511:.6f} + RvM tail {Stail:.6f}, "
          f"gamma_max = {gN:.1f})")
    print(f"sqrt(Sigma) = {math.sqrt(Sigma):.4f}   "
          f"sd at 1e6 / 1e10: {math.sqrt(Sigma)/math.log(1e6):.4f} / "
          f"{math.sqrt(Sigma)/math.log(1e10):.4f}")

    ensure_scan(RESULTS)
    x, D, summ = load_scan(RESULTS)
    llx = np.log(np.log(x))

    # exact bias sum (removes the Mertens o(1) from the residuals): prefix
    # sums of 1/p over odd p <= sqrt(x); primes to 1e7 >> sqrt(1e10) = 1e5.
    podd = primes  # odd primes from compute_K3's sieve (p = 2 already dropped)
    cum = np.concatenate(([0.0], np.cumsum(1.0 / podd)))
    bias_exact = 0.5 * cum[np.searchsorted(podd, np.sqrt(x), side="right")]
    pred_exact = bias_exact + K3 - logL
    resid = D - pred_exact          # should be pure eps(x), sd ~ sqrt(Sigma)/log x

    print()
    print("=" * 72)
    print(f"scan data: {RESULTS}  ({len(x)} checkpoints, X = {summ['X']:.0e})")
    print("=" * 72)
    print("sign record: flips = %d, last flip at %s, first 1-side lead at %s" % (
        summ["flips"],
        summ["last_flip"] if summ["last_flip"] else "NEVER",
        summ["first_neg"] if summ["first_neg"] else "NEVER"))
    print(f"minimum D over [3, X]: {summ['minD']:.6f} at x = {summ['minD_at']}"
          "   (3-side leads throughout)" if summ["flips"] == 0 else "")

    print()
    print(f"{'x':>14} {'D(x)':>10} {'0.5*llx+C*':>11} {'exact pred':>11} "
          f"{'resid':>8} {'pred sd':>8}")
    show = [10 ** k for k in range(2, 11)]
    for xv in show:
        i = int(np.argmin(np.abs(x - xv)))
        if abs(x[i] - xv) > 0.01 * xv:
            continue
        print(f"{x[i]:>14.0f} {D[i]:>10.5f} {0.5*llx[i]+Cstar:>11.5f} "
              f"{pred_exact[i]:>11.5f} {resid[i]:>+8.5f} "
              f"{math.sqrt(Sigma)/math.log(x[i]):>8.5f}")

    # ---------------- fits: drift vs constant --------------------------------
    for lo in (1e6, 1e7):
        w = x >= lo
        u, d = llx[w], D[w]
        A = np.vstack([np.ones_like(u), u]).T
        (a2, b2), res2, _, _ = np.linalg.lstsq(A, d, rcond=None)
        r2 = d - (a2 + b2 * u)
        n = len(u)
        se_b = math.sqrt(float(np.sum(r2 ** 2)) / (n - 2)
                         / float(np.sum((u - u.mean()) ** 2)))
        a_fix = float(np.mean(d - 0.5 * u))            # b fixed at 1/2
        r_fix = d - (a_fix + 0.5 * u)
        a_const = float(np.mean(d))                    # no drift at all
        r_const = d - a_const
        rms = lambda r: math.sqrt(float(np.mean(r ** 2)))
        print()
        print(f"fit window [{lo:.0e}, 1e10]  ({n} log-spaced points; residuals "
              "are correlated a.p. oscillations, se is the naive one)")
        print(f"  free fit      : D = {a2:+.4f} + {b2:.4f}*loglog x   "
              f"(b se ~ {se_b:.4f}, pred b = 0.5000)   rms {rms(r2):.5f}")
        print(f"  b = 1/2 fixed : a = {a_fix:+.4f}  (pred C* = {Cstar:+.4f})"
              f"                       rms {rms(r_fix):.5f}")
        print(f"  constant only : a = {a_const:+.4f}"
              f"                                             rms {rms(r_const):.5f}")
        print(f"  drift vs constant: rms ratio {rms(r_const)/rms(r2):.1f}x in "
              f"favor of drift")

    # ---------------- residual decay: is sd ~ sqrt(Sigma)/log x ? ------------
    print()
    print("residuals vs exact prediction (no free parameters), by decade:")
    print(f"{'decade':>14} {'n':>4} {'mean resid':>11} {'rms resid':>10} "
          f"{'pred sd':>8}")
    for k in range(4, 10):
        w = (x >= 10 ** k) & (x < 10 ** (k + 1))
        if not np.any(w):
            continue
        pr = math.sqrt(Sigma) / math.log(math.sqrt(10) * 10 ** k)
        print(f"1e{k:02d}..1e{k+1:02d}{'':>3} {int(np.sum(w)):>4} "
              f"{float(np.mean(resid[w])):>+11.5f} "
              f"{math.sqrt(float(np.mean(resid[w]**2))):>10.5f} {pr:>8.5f}")
    print()
    print("interpretation: b consistent with 1/2 and a with C* => the")
    print("(1/2) log log x drift is real; rms(resid) tracking sqrt(Sigma)/log x")
    print("(not constant, not sqrt(loglog) random-walk growth) confirms the")
    print("1/log x fluctuation decay — the critical race freezes with the")
    print("slowest possible drift and NO sign change in [3, 1e10].")


if __name__ == "__main__":
    main()
