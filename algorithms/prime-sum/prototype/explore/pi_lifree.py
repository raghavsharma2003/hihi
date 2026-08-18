#!/usr/bin/env python3
"""
Analytic pi(x) from zeta zeros WITHOUT logarithmic-integral functions.

Methodological point (vs Riemann/Riesel-Gohl/Platt): the classical analytic
pi(x) route evaluates li(x^rho) for complex rho, which drags in the branch
cut / Ei continuation of the logarithmic integral.  Here NO li/Ei/Gamma-
incomplete function is ever evaluated.  The 1/log weight is stripped by a
real sigma-integral of entire objects, exactly as the accompanying
analytic_sum.py does for S(x) = sum of primes, but adapted to weight n^0:

  1. Log-Gaussian cutoff c(t) = erfc(ln(t/x)/(sqrt(2) eps))/2, exact Mellin
     transform M(s) = x^s/s * exp(s^2 eps^2 / 2)   (entire apart from s=0).
  2. Perron against A(s) = -zeta'/zeta(s+sigma) gives, for real sigma >= 0,
        psi0t(sigma) := sum_n Lambda(n) n^(-sigma) c(n)
                      = M(1-sigma) - sum_rho M(rho-sigma)
                        - (zeta'/zeta)(sigma) - sum_k M(-2k-sigma),
     where -(zeta'/zeta)(sigma) is the residue of the M-pole at s=0.
     The bracket [M(1-sigma) - zeta'/zeta(sigma)] extends continuously
     across sigma=1: M(1-sigma) = 1/(1-sigma) + ln x + O(1-sigma) and
     (zeta'/zeta)(sigma) = 1/(1-sigma) + gamma_E + O(sigma-1), so the poles
     cancel EXACTLY and the crossing value is ln x - gamma_E + O(eps^2).
     (Verified numerically in --validate before use.)
  3. Strip the log weight with 1/ln n = int_0^A n^(-sigma) dsigma
     + n^(-A)/ln n   (A = 4):
        T0t := sum_{p^k} (1/k) c(p^k) = int_0^A psi0t(sigma) dsigma + R_A,
        R_A  = sum_{p^k} (1/k) p^(-A k) c(p^k)
     (prime-zeta-like; truncating at p <= 1e6 costs < 1e-19).
     The sigma-integral of the main pair is finite by the pole cancellation
     above; its value plays the role li(x) plays for Riemann, but it is
     obtained by quadrature of elementary/zeta functions only.
  4. pi_smooth = T0t - sum_{k>=2} (1/k) c(p^k)   (exact prime powers,
     p <= sqrt(x e^(12 eps))).
  5. pi(x) = pi_smooth - sum_p (c(p) - [p<=x])   (window sieved exactly).
  6. Round.  Verified against a direct sieve count computed in this script.

Precision notes:
  * Every prime in the window carries weight 1 (not p as in analytic_sum),
    so DOUBLE-precision c(p) is fine there: each c has absolute error
    ~1e-16, u is fed in via float128 log1p so the argument error is
    negligible, and the worst coherent bias is ~1e-16..1e-13 per prime
    times the window count (~4e5 at x=1e8), i.e. <~1e-8 total -- far below
    the 0.5 rounding margin.  (Contrast analytic_sum.py, where the weight
    p ~ x forces mpmath erfc in the window.)
  * Zero terms are x^(1/2-sigma)-scale (<= 1e4 at x=1e8), so float128
    accumulation noise ~1e-19*scale*sqrt(ops) is harmless.
  * eps = 8/gamma_N (N = 2000 zeros): truncated-zero tail is suppressed by
    exp(-(gamma eps)^2/2) <= e^{-32} ~ 1.3e-14 per zero at x^(1/2) scale.

Usage:
  pi_lifree.py --validate            pointwise psi0t checks at x=1e6
  pi_lifree.py x [x2 x3 ...]         full pipeline + direct sieve check
Repro: python3 pi_lifree.py --validate && python3 pi_lifree.py 1e6 1e7 1e8
"""
import sys, os, math
from fractions import Fraction
import numpy as np
import mpmath as mp

ld = np.longdouble
cld = np.clongdouble
SCRATCH = "/tmp/claude-0/-home-user-hihi/482aec6c-4f00-58b8-b5df-df7d9a8314a0/scratchpad"
ZEROS_DEFAULT = os.path.join(SCRATCH, "hpzeros2000.txt")

mp.mp.dps = 50
A = 4.0        # truncation of the 1/log integral representation
KCUT = 12.0    # cutoff half-width in units of eps (erfc(12/sqrt2)/2 ~ 1.8e-33)


# ----------------------------------------------------------------- sieves
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


def pi_count_sieve(x):
    """Direct sieve count of primes <= x (the ground truth used below --
    computed here, not a memorized constant)."""
    is_c = np.zeros(x + 1, dtype=bool)
    is_c[:2] = True
    for i in range(2, int(x**0.5) + 1):
        if not is_c[i]:
            is_c[i * i :: i] = True
    return int(np.count_nonzero(~is_c))


# ----------------------------------------------------------------- cutoff
def u_of(t, x, eps):
    """u = ln(t/x)/eps without catastrophic cancellation: (t-x) is exact
    integer arithmetic, the division is float128, then log1p."""
    return float(np.log1p(ld(t - x) / ld(x)) / ld(eps))


def cutoff_scalar(t, x, eps):
    """c(t) at double precision.  Fine everywhere in THIS script: the
    largest weight multiplying c anywhere here is 1 (window primes), so the
    ~1e-16 absolute error per evaluation cannot accumulate past ~1e-8 even
    over ~4e5 window primes (see module docstring)."""
    u = u_of(t, x, eps)
    if u < -KCUT:
        return 1.0
    if u > KCUT:
        return 0.0
    return 0.5 * math.erfc(u / math.sqrt(2.0))


def cutoff_mp(t, x, eps):
    """c(t) as mpf, for the (cheap) prime-power band where we keep extra
    headroom anyway."""
    ufast = u_of(t, x, eps)
    if ufast < -KCUT:
        return mp.mpf(1)
    if ufast > KCUT:
        return mp.mpf(0)
    u = mp.log1p(mp.mpf(t - x) / x) / mp.mpf(eps)
    return mp.erfc(u / mp.sqrt(2)) / 2


# ------------------------------------------------- pointwise psi0t (check)
def psi0t_analytic(x, sigma, gammas, eps):
    """psi0t(sigma) = M(1-sigma) - (zeta'/zeta)(sigma)
                      - sum_rho M(rho-sigma) - sum_{k=1,2} M(-2k-sigma).
    Main terms in mpmath, zero sum vectorized in float128 (x^(1/2-sigma)
    scale).  sigma != 1 (use the continuous pair near 1)."""
    X, E = mp.mpf(x), mp.mpf(eps)
    w = 1 - mp.mpf(sigma)
    Mterm = mp.e ** (w * mp.log(X) + w * w * E * E / 2) / w
    zpz = mp.zeta(mp.mpf(sigma), derivative=1) / mp.zeta(mp.mpf(sigma))

    g = gammas.astype(ld)
    L = ld(np.log(ld(x)))
    re = ld(0.5) - ld(sigma)
    mag = np.exp(re * L + (re * re - g * g) * ld(eps) ** 2 / 2)
    ph = g * L + g * re * ld(eps) ** 2
    num = mag * (np.cos(ph) + 1j * np.sin(ph))
    den = re + 1j * g.astype(cld)
    zsum = 2 * np.sum((num / den).real)

    triv = mp.mpf(0)
    for k in (1, 2):
        wk = mp.mpf(-2 * k) - mp.mpf(sigma)
        triv += mp.e ** (wk * mp.log(X) + wk * wk * E * E / 2) / wk
    return Mterm - zpz - mp.mpf(repr(float(zsum))) - triv


def psi0t_brute(x, sigma, eps):
    """Brute force sum_n Lambda(n) n^(-sigma) c(n), float128 accumulation."""
    xmax = int(x * math.exp(KCUT * eps)) + 1
    ps = sieve_np(xmax)
    tot = ld(0)
    for p in map(int, ps):
        lp = np.log(ld(p))
        pk = p
        while pk <= xmax:
            c = cutoff_scalar(pk, x, eps)
            if c:
                tot += lp * np.power(ld(pk), ld(-sigma)) * ld(c)
            pk *= p
    return tot


def pole_cancellation_check(x, eps):
    """Numerically verify the SIGN of the sigma=1 cancellation in the pair
    f(sigma) = M(1-sigma) - (zeta'/zeta)(sigma) before integrating across
    it: f must stay finite and approach ln x - gamma_E (+O(eps^2))."""
    X, E = mp.mpf(x), mp.mpf(eps)

    def f(sig):
        w = 1 - sig
        Mterm = mp.e ** (w * mp.log(X) + w * w * E * E / 2) / w
        return Mterm - mp.zeta(sig, derivative=1) / mp.zeta(sig)

    limit = mp.log(X) - mp.euler
    print(f"pole-cancellation check at sigma=1 (expect ~ ln x - gamma_E "
          f"= {mp.nstr(limit, 12)}):")
    ok = True
    for d in (1e-3, 1e-6, 1e-9):
        lo, hi = f(mp.mpf(1) - mp.mpf(d)), f(mp.mpf(1) + mp.mpf(d))
        print(f"  f(1-{d:g}) = {mp.nstr(lo, 12)}   f(1+{d:g}) = {mp.nstr(hi, 12)}")
        ok &= abs(lo - limit) < 1 and abs(hi - limit) < 1
    print(f"  -> poles cancel with the signs as written: {'YES' if ok else 'NO'}")
    return ok


# --------------------------------------------------- sigma-integral pieces
def zero_integrals(x, gammas, eps):
    """sum over conjugate zero pairs of int_0^A M(rho-sigma) dsigma,
    Gauss-Legendre in u = sigma * ln x, vectorized over zeros (float128).
    Integrand magnitude is x^(1/2-sigma) = e^(0.5 L - u): cut once it is
    below e^(-60) of the sigma=0 value."""
    L = float(np.log(ld(x)))
    umax = min(A * L, 0.5 * L + 60.0)
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
            re = ld(0.5 - sig)
            mag = np.exp(re * ld(L) + (re * re - g * g) * ld(eps) ** 2 / 2)
            ph = g * ld(L) + g * re * ld(eps) ** 2
            num = mag * (np.cos(ph) + 1j * np.sin(ph))
            den = re + 1j * g.astype(cld)
            total += ld(wj) * 2 * np.sum((num / den).real)
    return total


def main_pair_integral(x, eps):
    """int_0^A [ M(1-sigma) - (zeta'/zeta)(sigma) ] dsigma  (mpmath quad;
    the sigma=1 poles cancel inside the bracket -- verified by
    pole_cancellation_check).  This finite number is the li-free stand-in
    for the li(x) main term."""
    X, E = mp.mpf(x), mp.mpf(eps)

    def f(sig):
        w = 1 - sig
        Mterm = mp.e ** (w * mp.log(X) + w * w * E * E / 2) / w
        zpz = mp.zeta(sig, derivative=1) / mp.zeta(sig)
        return Mterm - zpz

    return mp.quad(f, [0, 1, A])


def trivial_integrals(x, eps):
    """int_0^A M(-2k-sigma) dsigma for k=1,2 (x^(-2k-sigma) scale, tiny)."""
    X, E = mp.mpf(x), mp.mpf(eps)
    tot = mp.mpf(0)
    for k in (1, 2):
        def f(sig, k=k):
            w = -2 * k - sig
            return mp.e ** (w * mp.log(X) + w * w * E * E / 2) / w
        tot += mp.quad(f, [0, A])
    return tot


def R_A_term(x, eps):
    """R_A = sum_{p^k} (1/k) p^(-A k) c(p^k), truncated at p <= 1e6.
    Weights p^(-4k) <= 1/16; truncation tail sum_{p>1e6} p^-4 < 3e-20.
    Double-precision c is harmless under these weights."""
    ps = sieve_np(10**6)
    tot = mp.mpf(0)
    xmax = x * math.exp(KCUT * eps)
    for p in map(int, ps):
        pk, k = p, 1
        while pk <= xmax:
            c = cutoff_scalar(pk, x, eps)
            if c:
                tot += mp.mpf(c) / (k * mp.mpf(pk) ** A)
            pk *= p
            k += 1
    return tot


# ------------------------------------------------------ exact corrections
def prime_power_correction(x, eps):
    """sum_{k>=2} (1/k) c(p^k) for p^k <= x e^(12 eps), i.e.
    p <= sqrt(x e^(12 eps)).  Exact rationals where c=1 (below the window),
    mpmath erfc in the transition band."""
    xmax = int(x * math.exp(KCUT * eps)) + 1
    ps = sieve_np(int(xmax**0.5) + 2)
    frac = Fraction(0)
    fl = mp.mpf(0)
    lo_c1 = x * math.exp(-KCUT * eps)
    for p in map(int, ps):
        pk, k = p * p, 2
        while pk <= xmax:
            if pk < lo_c1:
                frac += Fraction(1, k)
            else:
                fl += cutoff_mp(pk, x, eps) / k
            pk *= p
            k += 1
    return frac, fl


def window_correction(x, eps):
    """sum_p (c(p) - [p<=x]) over the transition window (exact sieve).
    Weight is 1 per prime, so double-precision c is fine here: u comes from
    float128 log1p (argument error negligible), each erfc carries ~1e-16
    absolute error, and even a fully coherent bias is <= ~1e-13 * count
    (~4e-8 at x=1e8) -- far below the 0.5 rounding margin.  math.fsum makes
    the accumulation itself exact."""
    lo = int(x * math.exp(-KCUT * eps))
    hi = int(x * math.exp(KCUT * eps)) + 1
    ps = segmented_primes(lo, hi)
    s2 = math.sqrt(2.0)
    terms = []
    for p in map(int, ps):
        u = u_of(p, x, eps)
        if abs(u) > KCUT:
            continue
        c = 0.5 * math.erfc(u / s2)
        terms.append(c - 1.0 if p <= x else c)
    return math.fsum(terms), len(ps)


# ---------------------------------------------------------------- driver
def load_zeros(path):
    return np.loadtxt(path, dtype=ld)


def validate(zeros_file):
    x = 10**6
    gammas = load_zeros(zeros_file)
    eps = 8.0 / float(gammas[-1])
    print(f"[validate] x={x}  N={len(gammas)} zeros  eps={eps:.6e}")
    ok = pole_cancellation_check(x, eps)
    print("pointwise psi0t(sigma) analytic vs brute at x=1e6:")
    worst = 0.0
    for sigma in (0.0, 0.5, 1.001, 2.0):
        ana = psi0t_analytic(x, sigma, gammas, eps)
        bru = psi0t_brute(x, sigma, eps)
        diff = ana - mp.mpf(repr(float(bru)))
        worst = max(worst, abs(float(diff)))
        print(f"  sigma={sigma:<6}  analytic={mp.nstr(ana, 18):<24}  "
              f"brute={float(bru):.12f}  diff={mp.nstr(diff, 4)}")
    ok &= worst < 1e-6
    print(f"[validate] worst |diff| = {worst:.3e}  ->  "
          f"{'PASS' if ok else 'FAIL'}")
    return ok


def compute_pi(x, gammas, eps):
    Iz = zero_integrals(x, gammas, eps)          # float128 (fast path)
    Im = main_pair_integral(x, eps)              # mpf
    It = trivial_integrals(x, eps)               # mpf
    Ra = R_A_term(x, eps)                        # mpf
    # repr(float(Iz)) rounds Iz to double: Iz carries float128 accumulation
    # noise ~x^0.5*1e-19*sqrt(ops), below double eps at these scales.
    T0t = Im - mp.mpf(repr(float(Iz))) - It + Ra

    ppf, ppl = prime_power_correction(x, eps)
    pp_total = mp.mpf(ppf.numerator) / ppf.denominator + ppl
    Wc, nwin = window_correction(x, eps)
    pi_analytic = T0t - pp_total - mp.mpf(repr(Wc))
    return pi_analytic, T0t, pp_total, Wc, nwin


def main():
    if "--validate" in sys.argv:
        sys.exit(0 if validate(ZEROS_DEFAULT) else 1)

    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        print(__doc__)
        sys.exit(2)
    xs = [int(float(a)) for a in args]
    gammas = load_zeros(ZEROS_DEFAULT)
    eps = 8.0 / float(gammas[-1])
    allok = True
    for x in xs:
        print(f"x={x:.0e}  N={len(gammas)} zeros  eps={eps:.6e}  "
              f"window=±{KCUT*eps*100:.2f}%")
        pi_a, T0t, pp, Wc, nwin = compute_pi(x, gammas, eps)
        print(f"  T0~ analytic       = {mp.nstr(T0t, 22)}")
        print(f"  prime-power corr   = {mp.nstr(pp, 18)}")
        print(f"  window corr        = {Wc:.15f}  ({nwin} primes sieved)")
        print(f"  pi analytic        = {mp.nstr(pi_a, 22)}")
        pr = int(mp.nint(pi_a))
        px = pi_count_sieve(x)
        resid = pi_a - px
        ok = pr == px
        allok &= ok
        print(f"  pi rounded         = {pr}")
        print(f"  pi exact (sieve)   = {px}")
        print(f"  residual           = {mp.nstr(resid, 6)}   "
              f"{'*** EXACT INTEGER RECOVERED ***' if ok else '(OFF)'}")
    sys.exit(0 if allok else 1)


if __name__ == "__main__":
    main()
