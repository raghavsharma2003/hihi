#!/usr/bin/env python3
"""
Analytic Mertens-type sum  sum_{p<=x} 1/p  from zeros of zeta.

Weight m = -1 member of the family psi_m(sigma) = sum_n Lambda(n) n^(m-sigma) c(n)
(m = 1 is S(x) = sum of primes, see ../analytic_sum.py); this file closes the
weight family m in {-1, 0, 1, 2} for the framework.

Pipeline (mirrors analytic_sum.py):

 1. Log-Gaussian cutoff c(t) = erfc(ln(t/x)/(sqrt2 eps))/2 with exact Mellin
    transform M(s) = x^s/s * exp(s^2 eps^2/2).
 2. Smoothed explicit formula, Perron against A(s) = -zeta'/zeta(s+sigma+1):
      psim1(sigma) = sum_n Lambda(n) n^(-1-sigma) c(n)
                   = M(-sigma) - sum_rho M(rho-1-sigma)
                     - (zeta'/zeta)(sigma+1) - sum_k M(-2k-1-sigma).
    The zeta pole at s+sigma+1 = 1 sits at s = -sigma and gives M(-sigma);
    M's own pole at s = 0 gives -(zeta'/zeta)(sigma+1); nontrivial zeros rho
    land at s = rho-1-sigma; trivial zeros -2k at s = -2k-1-sigma.
    ENDPOINT sigma = 0: M(-sigma) collides with M's pole AND zeta'/zeta(sigma+1)
    hits its pole at argument 1.  The pair [M(-sigma) - zeta'/zeta(sigma+1)]
    extends continuously: M(-sigma) = -1/sigma + ln x + O(sigma) and
    zeta'/zeta(1+sigma) = -1/sigma + gamma_E + O(sigma), so the limit is
    ln x - gamma_E.  Verified numerically by verify_limit(); main_pair()
    evaluates the bracket stably (extra working digits ~ log10(1/sigma) near 0,
    exact limit below sigma = 1e-30, where the O(sigma) term is < 1e-28).
 3. Log-stripping: 1/ln n = int_0^A n^(-sigma) dsigma + n^(-A)/ln n gives
      T := sum_{p^k} (1/k) p^(-k) c(p^k) = int_0^A psim1(sigma) dsigma + R_A,
      R_A = sum_{p^k} (1/k) p^(-(A+1)k) c(p^k)
    (prime-zeta-like, weights p^(-5k) for A = 4; truncation at p <= 1e6 costs
    ~1e-25).  The sigma-integral of [M(-sigma) - zeta'/zeta(sigma+1)] is finite
    because the sigma = 0 poles cancel inside the bracket (step 2).
 4. Strip prime powers k >= 2 exactly:
      PP2 = sum_{k>=2, p^k} (1/k) p^(-k) c(p^k)      (~450 primes, instant),
    leaving sum_p c(p)/p.
 5. Window correction with weight 1/p over the exactly sieved window
    [x e^(-12 eps), x e^(12 eps)]:  sum_p (c(p) - [p<=x])/p.
    DOUBLE PRECISION IS FINE HERE, unlike the weight-p window in
    analytic_sum.py: each weight is 1/p ~ 1/x, so a ~1e-16-absolute rounding
    error in c contributes ~1e-22 per term and < 1e-17 in total even if it
    were perfectly coherent across all ~1e4-1e5 window primes — far below the
    1e-13 target.  (With weight p ~ x the same rounding is amplified by x^2,
    which is why analytic_sum.py needs mpmath there.)  Terms are accumulated
    with math.fsum (exact for doubles).
 6. Result: sum_{p<=x} 1/p.  Validated against mpmath fsum of 1/p over sieved
    primes, and sanity-checked against ln ln x + M (Mertens constant).

Precision notes: zero terms have magnitude x^(-1/2-sigma) (vs x^(3/2-sigma)
for weight p), so float128 accumulation noise is ~1e-21 and the truncation
tail after 2000 zeros is driven below 1e-14 by choose_eps_m.  All prime/prime-
power sums with tiny weights (R_A ~ p^(-5k), PP2 ~ p^(-2k)) use double or
float128 cutoffs for the same weights-are-tiny reason.

Non-rigorous in the same ways as analytic_sum.py (floating point, heuristic
truncation bounds).

Usage: mertens.py [x] [zeros_file]
  no x: full validation suite — limit check, pointwise psim1 validation at
        x = 1e6, then the full pipeline vs brute at x = 1e6 and 1e7.
"""
import sys, os, math
import numpy as np
import mpmath as mp

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
from analytic_sum import (sieve_np, segmented_primes, u_of, cutoff_scalar,
                          A, KCUT, SCRATCH)

ld = np.longdouble
mp.mp.dps = 50


def load_zeros(zf):
    """Parse zeros with C strtold so float128 keeps ~18-19 digits."""
    with open(zf) as f:
        return np.array([ld(line.strip()) for line in f if line.strip()])


def choose_eps_m(x, gammas, target=1e-14):
    """Smallest eps whose zero-truncation tail stays below `target`.
    Zero terms here are |M(rho-1-sigma)| <= x^(-1/2) exp((re^2-g^2)eps^2/2)/g
    with |re| <= 1/2 + A; the (1+A) factor covers both the pointwise sum and
    the sigma-integral.  ~2e5 zeros past the table, asymptotic density."""
    gN = float(gammas[-1])
    n0 = len(gammas)
    ns = np.arange(n0 + 1, n0 + 200001, dtype=np.float64)
    gtail = 2 * math.pi * ns / np.log(ns + 10)  # conservative underestimate
    gtail = np.maximum(gtail, gN + (ns - n0) * 0.1)
    re2 = (0.5 + A) ** 2
    for mult in np.arange(6.0, 20.0, 0.25):
        eps = mult / gN
        tail = 2 * (1 + A) * np.sum(
            x ** -0.5 * np.exp((re2 - gtail ** 2) * eps ** 2 / 2) / gtail)
        if tail < target:
            return eps, tail
    return 20.0 / gN, tail


# ---------------------------------------------------------------- explicit formula

def main_pair(x, eps, sig):
    """[M(-sigma) - zeta'/zeta(1+sigma)], stable through sigma -> 0.

    Both terms are -1/sigma + O(1); the bracket is regular with value
    ln x - gamma_E at sigma = 0.  Near 0 each term is ~1/sigma, so we add
    ~log10(1/sigma) guard digits before subtracting (tanh-sinh quadrature
    pushes nodes to sigma ~ 1e-50, but their weights shrink like sigma, so
    the guarded evaluation keeps every node's contribution accurate)."""
    s = mp.mpf(sig)
    X, E = mp.mpf(x), mp.mpf(eps)
    if s < mp.mpf(10) ** -30:
        # bracket = ln x - gamma + O(sigma); O(sigma) coeff ~ (ln^2 x)/2 < 1e2,
        # so the truncation error here is < 1e-28.
        return mp.log(X) - mp.euler
    extra = int(max(0, -mp.floor(mp.log10(s)))) + 10
    with mp.workdps(mp.mp.dps + extra):
        w = -s
        Mterm = mp.e ** (w * mp.log(X) + w * w * E * E / 2) / w
        zpz = mp.zeta(1 + s, derivative=1) / mp.zeta(1 + s)
        val = Mterm - zpz
    return +val  # round back to ambient precision


def M_of(x, eps, w):
    """M(w) = x^w/w exp(w^2 eps^2/2) for real w != 0 (mpmath)."""
    X, E, W = mp.mpf(x), mp.mpf(eps), mp.mpf(w)
    return mp.e ** (W * mp.log(X) + W * W * E * E / 2) / W


def zero_sum_point(x, gammas, eps, sig):
    """sum over all nontrivial zeros of M(rho-1-sigma) = 2 Re sum_{gamma>0},
    vectorized float128.  Magnitude ~ x^(-1/2-sigma) per term."""
    g = gammas.astype(ld)
    L = np.log(ld(x))
    re = ld(-0.5) - ld(sig)
    E2 = ld(eps) ** 2
    mag = np.exp(re * L + (re * re - g * g) * E2 / 2)
    ph = g * L + g * re * E2
    num = mag * (np.cos(ph) + 1j * np.sin(ph))
    den = re + 1j * g.astype(np.complex256)
    return float(2 * np.sum((num / den).real))


def psim1_analytic(x, gammas, eps, sig):
    """psim1(sigma) from the explicit formula (trivial zeros k = 1, 2)."""
    zsum = zero_sum_point(x, gammas, eps, sig)
    triv = sum(M_of(x, eps, -2 * k - 1 - sig) for k in (1, 2))
    return main_pair(x, eps, sig) - mp.mpf(repr(zsum)) - triv


def psim1_brute(x, eps, sig, ps=None):
    """sum_n Lambda(n) n^(-1-sigma) c(n) by brute force, float128.
    Per-term rel. error ~1e-19, transition-band c error 1e-16 * (ln p / p)
    ~ 1e-21 abs — supports ~16-digit validation."""
    xmax = int(x * math.exp(KCUT * eps)) + 1
    if ps is None:
        ps = sieve_np(xmax)
    lo = x * math.exp(-KCUT * eps)
    pl = ps.astype(ld)
    lg = np.log(pl)
    terms = lg * np.exp(-(1 + ld(sig)) * lg)          # k = 1 terms
    mask = ps < lo                                     # c = 1 (error < 1e-33)
    total = np.sum(terms[mask])
    for p, t in zip(ps[~mask], terms[~mask]):
        total += ld(cutoff_scalar(int(p), x, eps)) * t
    for p in map(int, ps[ps <= int(xmax ** 0.5) + 1]):  # k >= 2
        lgp = np.log(ld(p))
        pk, k = p * p, 2
        while pk <= xmax:
            c = cutoff_scalar(pk, x, eps)
            if c:
                total += ld(c) * lgp * np.exp(-(1 + ld(sig)) * k * lgp)
            pk *= p
            k += 1
    return total


# ---------------------------------------------------------------- sigma-integrals

def main_pair_integral(x, eps):
    """int_0^A [M(-sigma) - zeta'/zeta(sigma+1)] dsigma (finite: the
    sigma = 0 poles cancel inside the bracket, handled by main_pair)."""
    return mp.quad(lambda s: main_pair(x, eps, s), [0, 1, A])


def zero_integrals_m(x, gammas, eps):
    """sum over conjugate zero pairs of int_0^A M(rho-1-sigma) dsigma,
    Gauss-Legendre in u = sigma ln x, vectorized over zeros (float128).
    Integrand magnitude x^(-1/2) e^(-u); beyond u = 60 it is < 1e-29."""
    L = float(np.log(ld(x)))
    umax = min(A * L, 60.0)
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
            re = ld(-0.5 - sig)
            mag = np.exp(re * ld(L) + (re * re - g * g) * ld(eps) ** 2 / 2)
            ph = g * ld(L) + g * re * ld(eps) ** 2
            num = mag * (np.cos(ph) + 1j * np.sin(ph))
            den = re + 1j * g.astype(np.complex256)
            total += ld(wj) * 2 * np.sum((num / den).real)
    return total


def trivial_integrals_m(x, eps):
    """int_0^A M(-2k-1-sigma) dsigma, k = 1, 2 (magnitude ~ x^-3, x^-5)."""
    tot = mp.mpf(0)
    for k in (1, 2):
        tot += mp.quad(lambda s, k=k: M_of(x, eps, -2 * k - 1 - s), [0, A])
    return tot


def R_A_m(x, eps):
    """R_A = sum_{p^k} (1/k) p^(-(A+1)k) c(p^k), truncated at p <= 1e6
    (tail ~ 1e-25 for A = 4).  Positive terms with weight p^(-5k): float128
    accumulation (rel 1e-19) and double-precision c are both harmless."""
    xmax = x * math.exp(KCUT * eps)
    lo = x * math.exp(-KCUT * eps)
    cap = min(10 ** 6, int(xmax) + 1)
    ps = sieve_np(cap)
    tot = ld(0)
    e = -ld(A + 1)
    for p in map(int, ps):
        pk, k = p, 1
        while pk <= xmax:
            c = 1.0 if pk < lo else cutoff_scalar(pk, x, eps)
            if c:
                tot += ld(c) * ld(pk) ** e / k
            pk *= p
            k += 1
    return mp.mpf(repr(float(tot)))


# ---------------------------------------------------------------- exact strips

def prime_power_strip(x, eps):
    """PP2 = sum_{k>=2, p^k <= xmax} (1/k) p^(-k) c(p^k), exact mpmath ints.
    Transition-band weight is p^(-k) ~ 1/x, so double-precision c (abs error
    ~1e-16) contributes ~1e-23 per term — negligible."""
    xmax = int(x * math.exp(KCUT * eps)) + 1
    ps = sieve_np(int(xmax ** 0.5) + 2)
    tot = mp.mpf(0)
    for p in map(int, ps):
        pk, k = p * p, 2
        while pk <= xmax:
            c = cutoff_scalar(pk, x, eps)
            if c:
                tot += mp.mpf(c) / (k * mp.mpf(pk))
            pk *= p
            k += 1
    return tot


def window_correction_m(x, eps):
    """sum_p (c(p) - [p<=x])/p over the sieved window.  Double precision:
    weight 1/p ~ 1/x makes c's ~1e-16 rounding contribute ~1e-22 per term,
    < 1e-17 total even coherently (see module docstring, step 5); math.fsum
    adds the double terms exactly.  u comes from float128 log1p (u_of), so
    no cancellation in ln(p/x)."""
    lo = int(x * math.exp(-KCUT * eps))
    hi = int(x * math.exp(KCUT * eps)) + 1
    ps = segmented_primes(lo, hi)
    s2 = math.sqrt(2.0)
    terms = []
    for p in map(int, ps):
        u = u_of(p, x, eps)
        if abs(u) > KCUT:
            continue
        if p <= x:
            terms.append(-math.erfc(-u / s2) / 2 / p)  # -(1 - c(p))/p
        else:
            terms.append(math.erfc(u / s2) / 2 / p)    # c(p)/p
    return math.fsum(terms), len(ps)


# ---------------------------------------------------------------- brute forces

def brute_T(x, eps):
    """T = sum_{p^k} (1/k) p^(-k) c(p^k) by brute force (float128)."""
    xmax = int(x * math.exp(KCUT * eps)) + 1
    lo = x * math.exp(-KCUT * eps)
    ps = sieve_np(xmax)
    mask = ps < lo
    tot = np.sum(1 / ps[mask].astype(ld))
    for p in map(int, ps[~mask]):
        tot += ld(cutoff_scalar(p, x, eps)) / p
    for p in map(int, ps[ps <= int(xmax ** 0.5) + 1]):
        pk, k = p * p, 2
        while pk <= xmax:
            c = cutoff_scalar(pk, x, eps)
            if c:
                tot += ld(c) / (ld(k) * pk)
            pk *= p
            k += 1
    return tot


def brute_mertens(x):
    """sum_{p<=x} 1/p, mpmath fsum over sieved primes (30 digits)."""
    ps = sieve_np(x)
    with mp.workdps(30):
        val = mp.fsum(mp.mpf(1) / p for p in map(int, ps))
    return +val


def digits_match(a, b):
    d = abs(mp.mpf(a) - mp.mpf(b))
    if d == 0:
        return 99
    return int(mp.floor(-mp.log10(d / abs(mp.mpf(b)))))


# ---------------------------------------------------------------- validations

def verify_limit(x, eps):
    """Numerical check: [M(-sigma) - zeta'/zeta(sigma+1)] -> ln x - gamma_E."""
    lim = mp.log(x) - mp.euler
    print(f"-- limit check at x={x:.0e}: ln x - gamma_E = {mp.nstr(lim, 20)}")
    for sig in (1e-2, 1e-4, 1e-8, 1e-16, 1e-40):
        v = main_pair(x, eps, sig)
        print(f"   sigma={sig:8.0e}   pair = {mp.nstr(v, 20)}   "
              f"pair - limit = {mp.nstr(v - lim, 5)}")


def validate_pointwise(x, gammas, eps, sigmas=(0.001, 0.5, 1.0, 2.0)):
    """psim1(sigma) analytic vs brute, before any integration."""
    print(f"-- pointwise psim1 validation at x={x:.0e}")
    xmax = int(x * math.exp(KCUT * eps)) + 1
    ps = sieve_np(xmax)
    ok = True
    for sig in sigmas:
        an = psim1_analytic(x, gammas, eps, sig)
        br = psim1_brute(x, eps, sig, ps)
        brm = mp.mpf(repr(float(br)))
        dm = digits_match(an, brm)
        ok &= dm >= 12
        print(f"   sigma={sig:<6}  analytic = {mp.nstr(an, 18):<22}  "
              f"brute = {mp.nstr(brm, 18):<22}  diff = {mp.nstr(an - brm, 3)}"
              f"   [{dm} digits]")
    return ok


def run_x(x, gammas, do_brute=True):
    eps, tailb = choose_eps_m(x, gammas)
    print(f"== x={x:.0e}  N={len(gammas)} zeros  eps={eps:.3e}  "
          f"window=±{KCUT*eps*100:.2f}%  zero_tail_bound={tailb:.2e}")

    Iz = zero_integrals_m(x, gammas, eps)      # float128 (fast path)
    Im = main_pair_integral(x, eps)            # mpf
    It = trivial_integrals_m(x, eps)           # mpf
    Ra = R_A_m(x, eps)                         # mpf
    T = Im - mp.mpf(repr(float(Iz))) - It + Ra

    PP2 = prime_power_strip(x, eps)
    W, nwin = window_correction_m(x, eps)
    mert = T - PP2 - mp.mpf(repr(W))

    print(f"  int main pair      = {mp.nstr(Im, 20)}")
    print(f"  int zeros          = {mp.nstr(mp.mpf(repr(float(Iz))), 15)}")
    print(f"  int trivial        = {mp.nstr(It, 8)}")
    print(f"  R_A                = {mp.nstr(Ra, 20)}")
    print(f"  T analytic         = {mp.nstr(T, 20)}")
    print(f"  prime-power strip  = {mp.nstr(PP2, 20)}")
    print(f"  window corr        = {mp.nstr(mp.mpf(repr(W)), 15)}"
          f"  ({nwin} primes sieved)")
    print(f"  sum_(p<=x) 1/p     = {mp.nstr(mert, 20)}   [analytic]")

    sanity = mp.log(mp.log(x)) + mp.mpf(
        "0.26149721284764278375542683860869585905156664826120")
    print(f"  ln ln x + M        = {mp.nstr(sanity, 12)}   "
          f"(sanity, diff = {mp.nstr(mert - sanity, 3)})")

    if do_brute:
        Tb = brute_T(x, eps)
        print(f"  T brute            = {float(Tb):.18f}   "
              f"diff = {mp.nstr(T - mp.mpf(repr(float(Tb))), 3)}")
        mb = brute_mertens(x)
        dm = digits_match(mert, mb)
        print(f"  sum 1/p brute      = {mp.nstr(mb, 20)}")
        print(f"  analytic - brute   = {mp.nstr(mert - mb, 3)}   "
              f"*** {dm} matching digits ***")
    return mert


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    zf = args[1] if len(args) > 1 else os.path.join(SCRATCH, "hpzeros2000.txt")
    gammas = load_zeros(zf)
    xs = [int(float(args[0]))] if args else [10 ** 6, 10 ** 7]

    eps6, _ = choose_eps_m(10 ** 6, gammas)
    verify_limit(10 ** 6, eps6)
    if not validate_pointwise(10 ** 6, gammas, eps6):
        print("   WARNING: pointwise validation below 12 digits")
    for x in xs:
        run_x(x, gammas)


if __name__ == "__main__":
    main()
