#!/usr/bin/env python3
"""
Analytic computation of S(x) = sum of primes <= x from zeros of zeta.

Pipeline (all pieces derived in the accompanying paper):

  1. Log-Gaussian cutoff c(t) = erfc(ln(t/x)/(sqrt(2) eps))/2 with exact
     Mellin transform M(s) = x^s/s * exp(s^2 eps^2 / 2).
  2. Weighted, smoothed Chebyshev-type sums
        psi1t(sigma) = sum_n Lambda(n) n^(1-sigma) c(n)
                     = M(2-sigma) - sum_rho M(rho+1-sigma)
                       - (zeta'/zeta)(sigma-1) - sum_k M(1-2k-sigma).
     (Perron against -zeta'/zeta(s+sigma-1); the M-pole at s=0 contributes
      the -(zeta'/zeta)(sigma-1) term.)
  3. Strip the logarithmic weight with 1/ln n = int_0^A n^(-sigma) dsigma
     + n^(-A)/ln n:
        Tt := sum_{p^k} (p^k/k) c(p^k)
            = int_0^A psi1t(sigma) dsigma + R_A,
     where R_A = sum_{p^k} (1/k) p^(-(A-1)k) c(p^k) converges like a prime
     zeta value for A = 4 (truncating at p <= 1e6 costs < 1e-13).
     The sigma-integral of the main pair [M(2-sigma) - zeta'/zeta(sigma-1)]
     is finite: the zeta'/zeta pole at sigma=2 cancels M's pole exactly.
  4. S_smooth = Tt - (exact prime-power correction, k >= 2).
  5. S(x) = S_smooth - sum_{p in window} p (c(p) - [p<=x]); the window
     [x e^(-12eps), x e^(12eps)] is sieved exactly.
  6. Round. Verified against the combinatorial fenwick.c values.

Non-rigorous in this implementation: floating point instead of interval
arithmetic, heuristic truncation bounds. The structure mirrors Platt's
rigorous analytic pi(x) computation (Math. Comp. 2015); making each bound
explicit is the path to a rigorous version.

Usage: analytic_sum.py x [zeros_file] [--brute]
  --brute: additionally brute-force Tt and S for validation (slow; only
           sensible for x <= ~1e8).
"""
import sys, os, math, subprocess
import numpy as np
import mpmath as mp

ld = np.longdouble
HERE = os.path.dirname(os.path.abspath(__file__))
SCRATCH = "/tmp/claude-0/-home-user-hihi/482aec6c-4f00-58b8-b5df-df7d9a8314a0/scratchpad"

mp.mp.dps = 50
A = 4.0            # truncation of the 1/log integral representation
KCUT = 12.0        # cutoff half-width in units of eps (erfc(12/sqrt2)~1e-32)


def sieve_np(limit):
    is_c = np.zeros(limit + 1, dtype=bool)
    is_c[:2] = True
    for i in range(2, int(limit**0.5) + 1):
        if not is_c[i]:
            is_c[i * i :: i] = True
    return np.flatnonzero(~is_c)


def segmented_primes(lo, hi):
    """primes in [lo, hi] as int64 array."""
    base = sieve_np(int(hi**0.5) + 2)
    n = hi - lo + 1
    mark = np.zeros(n, dtype=bool)
    for p in map(int, base):
        start = max(p * p, ((lo + p - 1) // p) * p)
        if start <= hi:
            mark[start - lo :: p] = True
    if lo <= 1:
        mark[: 2 - lo] = True
    return np.flatnonzero(~mark) + lo


def u_of(t, x, eps):
    """u = ln(t/x)/eps without catastrophic cancellation: (t-x)/x is exact
    integer arithmetic over a float128 division, then log1p."""
    return float(np.log1p(ld(t - x) / ld(x)) / ld(eps))


def cutoff_scalar(t, x, eps):
    """c(t) at double precision — ONLY for uses where t*delta_c is small.
    Window sums multiply c by t ~ x and MUST use cutoff_mp instead:
    coherent double rounding across a window sums to x^2 * 1e-16-scale."""
    u = u_of(t, x, eps)
    if u < -KCUT:
        return 1.0
    if u > KCUT:
        return 0.0
    return 0.5 * math.erfc(u / math.sqrt(2.0))


def cutoff_mp(t, x, eps):
    """c(t) as mpf: u computed entirely in mpmath from exact integers
    (t-x, x exact; eps embeds its binary double value exactly)."""
    ufast = float(np.log1p(ld(t - x) / ld(x)) / ld(eps))
    if ufast < -KCUT:
        return mp.mpf(1)
    if ufast > KCUT:
        return mp.mpf(0)
    u = mp.log1p(mp.mpf(t - x) / x) / mp.mpf(eps)
    return mp.erfc(u / mp.sqrt(2)) / 2


def choose_eps(x, gammas):
    """Smallest eps whose zero-truncation tail bound stays below 0.02,
    using the asymptotic zero density for ~2e5 zeros past the table."""
    gN = float(gammas[-1])
    n0 = len(gammas)
    ns = np.arange(n0 + 1, n0 + 200001, dtype=np.float64)
    gtail = 2 * math.pi * ns / np.log(ns + 10)  # conservative underestimate
    gtail = np.maximum(gtail, gN + (ns - n0) * 0.1)
    for mult in np.arange(6.0, 14.0, 0.25):
        eps = mult / gN
        tail = 2 * np.sum(x**1.5 * np.exp((2.25 - gtail**2) * eps**2 / 2) / gtail)
        if tail < 0.02:
            return eps, tail
    return 14.0 / gN, tail


def zero_integrals(x, gammas, eps):
    """sum over conjugate zero pairs of int_0^A M(rho+1-sigma) dsigma,
    Gauss-Legendre in u = sigma * ln x, vectorized over zeros (float128)."""
    L = float(np.log(ld(x)))
    umax = min(A * L, 1.5 * L + 50.0)
    nodes, weights = np.polynomial.legendre.leggauss(24)
    total = ld(0)
    g = gammas.astype(ld)
    npanels = max(8, int(umax / 5.0))
    edges = np.linspace(0.0, umax, npanels + 1)
    for a, b in zip(edges[:-1], edges[1:]):
        u = (a + b) / 2 + (b - a) / 2 * nodes
        w = (b - a) / 2 * weights / L  # du = L dsigma
        for uj, wj in zip(u, w):
            sig = uj / L
            re = ld(1.5 - sig)
            mag = np.exp(re * ld(L) + (re * re - g * g) * ld(eps) ** 2 / 2)
            ph = g * ld(L) + g * re * ld(eps) ** 2
            num = mag * (np.cos(ph) + 1j * np.sin(ph))
            den = re + 1j * g.astype(np.complex256)
            total += ld(wj) * 2 * np.sum((num / den).real)
    return total


def main_pair_integral(x, eps):
    """int_0^A [ M(2-sigma) - zeta'/zeta(sigma-1) ] dsigma  (mpmath quad;
    the sigma=2 pole cancels inside the bracket)."""
    X, E = mp.mpf(x), mp.mpf(eps)

    def f(sig):
        w = 2 - sig
        Mterm = mp.e ** (w * mp.log(X) + w * w * E * E / 2) / w
        zpz = mp.zeta(sig - 1, derivative=1) / mp.zeta(sig - 1)
        return Mterm - zpz

    return mp.quad(f, [0, 2, A])


def trivial_integrals(x, eps):
    X, E = mp.mpf(x), mp.mpf(eps)
    tot = mp.mpf(0)
    for k in (1, 2):
        def f(sig, k=k):
            w = 1 - 2 * k - sig
            return mp.e ** (w * mp.log(X) + w * w * E * E / 2) / w
        tot += mp.quad(f, [0, A])
    return tot


def R_A_term(x, eps):
    """sum_{p^k} (1/k) p^(-(A-1)k) c(p^k), truncated at p <= 1e6.
    Weights p^(-3k) are tiny, so double-precision c is harmless here."""
    ps = sieve_np(10**6)
    tot = mp.mpf(0)
    xmax = x * math.exp(KCUT * eps)
    for p in map(int, ps):
        pk, k = p, 1
        while pk <= xmax:
            c = cutoff_scalar(pk, x, eps)
            if c:
                tot += mp.mpf(c) / (k * mp.mpf(pk) ** (A - 1))
            pk *= p
            k += 1
    return tot


def prime_power_correction(x, eps):
    """sum_{k>=2} (1/k) p^k c(p^k) — exact rationals where c=1, mpmath
    erfc in the transition band (p^k there is ~x, so precision matters)."""
    xmax = int(x * math.exp(KCUT * eps)) + 1
    ps = sieve_np(int(xmax**0.5) + 2)
    from fractions import Fraction
    frac = Fraction(0)
    fl = mp.mpf(0)
    lo_c1 = x * math.exp(-KCUT * eps)
    for p in map(int, ps):
        pk, k = p * p, 2
        while pk <= xmax:
            if pk < lo_c1:
                frac += Fraction(pk, k)
            else:
                fl += cutoff_mp(pk, x, eps) * pk / k
            pk *= p
            k += 1
    return frac, fl


def window_correction(x, eps):
    """sum_p p*(c(p) - [p<=x]) over the transition window (exact sieve).
    All in mpmath: p is ~x here, so double-precision c would inject
    coherent x^2*1e-16-scale rounding bias (measured, not hypothetical)."""
    lo = int(x * math.exp(-KCUT * eps))
    hi = int(x * math.exp(KCUT * eps)) + 1
    ps = segmented_primes(lo, hi)
    tot = mp.mpf(0)
    with mp.workdps(25):
        E = mp.mpf(eps)
        s2 = mp.sqrt(2)
        for p in map(int, ps):
            ufast = float(np.log1p(ld(p - x) / ld(x)) / ld(eps))
            if abs(ufast) > KCUT:
                continue
            u = mp.log1p(mp.mpf(p - x) / x) / E
            if p <= x:
                tot -= mp.erfc(-u / s2) / 2 * p   # -(1 - c(p)) * p
            else:
                tot += mp.erfc(u / s2) / 2 * p    # c(p) * p
    return tot, len(ps)


def brute_check(x, eps):
    xmax = int(x * math.exp(KCUT * eps)) + 1
    ps = sieve_np(xmax)
    Tt = ld(0)
    for p in map(int, ps):
        pk, k = p, 1
        while pk <= xmax:
            Tt += ld(cutoff_scalar(pk, x, eps)) * ld(pk) / ld(k)
            pk *= p
            k += 1
    S = int(np.sum(ps[ps <= x].astype(object)))
    return Tt, S


def exact_S(x):
    out = subprocess.run([os.path.join(HERE, "..", "fenwick"), str(x)],
                         capture_output=True, text=True).stdout
    return int(out.strip().split(">")[-1])


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    x = int(float(args[0]))
    zf = args[1] if len(args) > 1 else os.path.join(SCRATCH, "hpzeros2000.txt")
    gammas = np.loadtxt(zf, dtype=ld)
    eps, tailb = choose_eps(x, gammas)
    print(f"x={x:.0e}  N={len(gammas)} zeros  eps={eps:.3e}  "
          f"window=±{KCUT*eps*100:.2f}%  tail_bound={tailb:.2e}")

    Iz = zero_integrals(x, gammas, eps)          # float128 (fast path)
    Im = main_pair_integral(x, eps)              # mpf
    It = trivial_integrals(x, eps)               # mpf
    Ra = R_A_term(x, eps)                        # mpf
    Tt_analytic = Im - mp.mpf(repr(float(Iz))) - It + Ra
    # repr(float(Iz)) rounds Iz to double: Iz itself carries float128
    # accumulation noise ~x^1.5*1e-19*sqrt(ops), well above double eps.

    ppf, ppl = prime_power_correction(x, eps)
    Wc, nwin = window_correction(x, eps)
    pp_total = mp.mpf(ppf.numerator) / ppf.denominator + ppl
    S_analytic = Tt_analytic - pp_total - Wc

    print(f"T~ analytic        = {mp.nstr(Tt_analytic, 25)}")
    print(f"prime-power corr   = {mp.nstr(pp_total, 25)}")
    print(f"window corr        = {mp.nstr(Wc, 25)}  ({nwin} primes sieved)")
    print(f"S analytic         = {mp.nstr(S_analytic, 25)}")
    Sr = int(mp.nint(S_analytic))
    Sx = exact_S(x)
    print(f"S rounded          = {Sr}")
    print(f"S exact (fenwick)  = {Sx}")
    print(f"difference         = {mp.nstr(S_analytic - Sx, 8)}   "
          f"{'*** EXACT INTEGER RECOVERED ***' if Sr == Sx else '(off)'}")

    if "--brute" in sys.argv:
        Tb, Sb = brute_check(x, eps)
        print(f"[brute] T~ = {float(Tb):.6f}   "
              f"T~ analytic err = {mp.nstr(Tt_analytic - mp.mpf(repr(float(Tb))), 8)}")


if __name__ == "__main__":
    main()
