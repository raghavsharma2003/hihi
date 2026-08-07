#!/usr/bin/env python3
"""
Analytic prime POWER sums  S_m(x) = sum_{p<=x} p^m  from zeros of zeta.

Generalizes ../analytic_sum.py (which is m=1) to weight n^m.  As far as we
can tell S_2, S_3 have never been computed analytically.

Pipeline:

  1. Same log-Gaussian cutoff c(t) = erfc(ln(t/x)/(sqrt(2) eps))/2 with
     Mellin transform M(s) = x^s/s * exp(s^2 eps^2/2).
  2. Weighted smoothed sums (Perron against -zeta'/zeta(s + sigma - m); the
     M-pole at s=0 contributes the -(zeta'/zeta)(sigma-m) term):
        psim(sigma) = sum_n Lambda(n) n^(m-sigma) c(n)
                    = M(m+1-sigma) - sum_rho M(rho+m-sigma)
                      - (zeta'/zeta)(sigma-m) - sum_{k>=1} M(m-2k-sigma).
  3. Log-stripping with 1/ln n = int_0^A n^(-sigma) dsigma + n^(-A)/ln n,
     A = m+3 (remainder weight p^(-3k) for every m):
        T_m := sum_{p^k} (p^(mk)/k) c(p^k)
             = int_0^A psim(sigma) dsigma + R_A,
        R_A  = sum_{p^k} (1/k) p^((m-A)k) c(p^k).
  4. S_m,smooth = T_m - sum_{k>=2} (1/k) p^(mk) c(p^k)  (exact correction).
  5. S_m(x) = S_m,smooth - sum_{p in window} p^m (c(p) - [p<=x]).
  6. Round to integer; verify against a sieve.

POLE STRUCTURE over sigma in [0, A] (this is where m>1 differs from m=1):

  * sigma = m+1: zeta-pole of -(zeta'/zeta)(sigma-m) cancels the M-pole of
    M(m+1-sigma) — same pair cancellation as the reference (sigma=2, m=1).
  * sigma = m-2k > 0 (odd m, e.g. m=3, k=1 -> sigma=1): the TRIVIAL-zero
    pole of zeta'/zeta at -2k is crossed INSIDE the integration range.  It
    cancels against the pole of the k-th trivial term M(m-2k-sigma) at the
    same sigma.  Both go in one bracket, quad split at that sigma.
  * sigma = 0 for EVEN m (m=2, k=m/2=1): the trivial-zero pole sits AT THE
    ENDPOINT sigma=0.  -(zeta'/zeta)(sigma-2) ~ -1/sigma cancels against
    the k=1 trivial term -M(-sigma) ~ +1/sigma.  Stable evaluation:
        -(z'/z)(sigma-m) - M(-sigma)
            = expm1(-sigma L + sigma^2 eps^2/2)/sigma
              - [ (z'/z)(sigma-m) - 1/sigma ],
    expm1 handles the first piece; the second piece is analytic at 0 and is
    evaluated for tiny sigma from the Taylor series of zeta about -m
    (zeta(u-m) = u*P(u), (z'/z)(u-m) - 1/u = P'(u)/P(u)).  The endpoint
    value is -(ln x + zeta''(-m)/(2 zeta'(-m))) for m=2.
    Equivalently: at sigma=0 the Perron integrand M(s)(-z'/z)(s-m) has a
    DOUBLE pole at s=0 (M-pole collides with the trivial-zero pole), and
    the finite bracket value is its residue.

PRECISION NOTES specific to m>=2 (targets: exact integers at x=1e6, 1e7):

  * Zero terms scale x^(m+1/2)/|rho| ~ 2e16 at x=1e7, m=2, while the final
    answer needs absolute error < 0.5.  float128 accumulation noise
    (1e-19 relative/op, ~1e6 ops) is ~0.3 — marginal.  The zero quadrature
    therefore runs the LARGE terms (float64-estimated |term| > MP_THRESH)
    through mpmath at dps 30 and only the small remainder vectorized in
    complex128 (their absolute errors are bounded by MP_THRESH * 1e-12).
  * numpy's leggauss returns float64 nodes/weights; using them as the rule
    injects ~1e-16 relative-to-integrand-scale errors (~1 absolute at
    x=1e7, m=2).  Nodes/weights are recomputed to 30 digits by Newton
    iteration on P_24.
  * Window correction weight is p^m ~ x^m: high-precision path is
    MANDATORY, exactly as documented in the reference — u = ln(p/x) via
    log1p on exact integers, erfc in mpmath (workdps 30 here).

Non-rigorous in the same ways as the reference (floating point, heuristic
truncation bounds); the structure is what a rigorous version would bound.

Usage:
  power_sums.py m x [zeros_file] [--psim-check] [--brute-T]
    --psim-check : verify psim(sigma) pointwise against a brute-force sum
                   at several sigma (including sigma ~ 0) and exit.
    --brute-T    : also brute-force T_m (exact bulk + mp window) for a
                   direct check of the analytic T_m.
"""
import sys, os, math
import numpy as np
import mpmath as mp

ld = np.longdouble
HERE = os.path.dirname(os.path.abspath(__file__))
SCRATCH = "/tmp/claude-0/-home-user-hihi/482aec6c-4f00-58b8-b5df-df7d9a8314a0/scratchpad"

mp.mp.dps = 50
KCUT = 12.0        # cutoff half-width in units of eps (erfc(12/sqrt2)~1e-32)
MP_THRESH = 0.03   # zero-quadrature terms larger than this go through mpmath
ZDPS = 30          # working dps for the zero quadrature / window paths


# ---------------------------------------------------------------- sieves ----

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


# ---------------------------------------------------------------- cutoff ----

def u_of(t, x, eps):
    """u = ln(t/x)/eps without catastrophic cancellation: (t-x)/x is exact
    integer arithmetic over a float128 division, then log1p."""
    return float(np.log1p(ld(t - x) / ld(x)) / ld(eps))


def cutoff_scalar(t, x, eps):
    """c(t) at double precision — ONLY where t^m * delta_c is negligible
    (e.g. the p^(-3k)-weighted remainder R_A)."""
    u = u_of(t, x, eps)
    if u < -KCUT:
        return 1.0
    if u > KCUT:
        return 0.0
    return 0.5 * math.erfc(u / math.sqrt(2.0))


def cutoff_mp(t, x, eps):
    """c(t) as mpf: u computed entirely in mpmath from exact integers
    (t-x, x exact; eps embeds its binary double value exactly).
    MANDATORY wherever c is multiplied by ~x^m-sized weights."""
    ufast = float(np.log1p(ld(t - x) / ld(x)) / ld(eps))
    if ufast < -KCUT:
        return mp.mpf(1)
    if ufast > KCUT:
        return mp.mpf(0)
    u = mp.log1p(mp.mpf(t - x) / x) / mp.mpf(eps)
    return mp.erfc(u / mp.sqrt(2)) / 2


# ----------------------------------------------------------- eps choice ----

def choose_eps(x, gammas, m):
    """Smallest eps whose zero-truncation tail bound stays below 0.02.
    Same heuristic as the reference with x^1.5 -> x^(m+1/2)."""
    gN = float(gammas[-1])
    n0 = len(gammas)
    ns = np.arange(n0 + 1, n0 + 200001, dtype=np.float64)
    gtail = 2 * math.pi * ns / np.log(ns + 10)  # conservative underestimate
    gtail = np.maximum(gtail, gN + (ns - n0) * 0.1)
    a2 = (m + 0.5) ** 2
    for mult in np.arange(6.0, 16.0, 0.25):
        eps = mult / gN
        tail = 2 * np.sum(x**(m + 0.5)
                          * np.exp((a2 - gtail**2) * eps**2 / 2) / gtail)
        if tail < 0.02:
            return eps, tail
    return 16.0 / gN, tail


# -------------------------------------------------- Gauss-Legendre nodes ----

def gl_rule_mp(n=24, dps=40):
    """(nodes, weights) of n-point Gauss-Legendre on [-1,1] to `dps` digits.
    float64 nodes would cap the zero quadrature at ~1e-16 relative to the
    x^(m+1/2)-scale integrand — not enough for m>=2."""
    seeds, _ = np.polynomial.legendre.leggauss(n)
    xs, ws = [], []
    with mp.workdps(dps + 10):
        for s in seeds:
            r = mp.mpf(float(s))
            for _ in range(80):
                P = mp.legendre(n, r)
                dP = n * (r * P - mp.legendre(n - 1, r)) / (r * r - 1)
                dr = P / dP
                r -= dr
                if abs(dr) < mp.mpf(10) ** (-(dps + 5)):
                    break
            dP = n * (r * P - mp.legendre(n - 1, r)) / (r * r - 1)
            # refresh dP at converged r
            P = mp.legendre(n, r)
            dP = n * (r * P - mp.legendre(n - 1, r)) / (r * r - 1)
            xs.append(+r)
            ws.append(2 / ((1 - r * r) * dP * dP))
    return xs, ws


# ----------------------------------------------------- zero quadrature -----

def zero_integrals(x, g_np, g_mp, eps, m):
    """int_0^A  sum_rho M(rho+m-sigma) dsigma  summed over conjugate pairs
    (2 Re over the gamma>0 zeros).  Gauss-Legendre in u = sigma ln x.

    Hybrid precision: per node, terms with float64-estimated magnitude
    > MP_THRESH are evaluated in mpmath (workdps ZDPS) with 30-digit nodes;
    the rest vectorized in complex128 (absolute error per term
    < MP_THRESH*1e-12; coherent worst case << 1e-4)."""
    A = m + 3
    L = float(np.log(ld(x)))
    umax = min(A * L, (m + 0.5) * L + 50.0)
    nodes_mp, weights_mp = gl_rule_mp(24, dps=ZDPS + 10)
    npanels = max(8, int(umax / 5.0))
    edges = np.linspace(0.0, umax, npanels + 1)

    g64 = g_np.astype(np.float64)
    tot_small = 0.0
    n_mp_terms = 0
    with mp.workdps(ZDPS):
        Lmp = mp.log(mp.mpf(x))
        logX = Lmp
        E2h = mp.mpf(eps) ** 2 / 2
        tot_mp = mp.mpf(0)
        for a, b in zip(edges[:-1], edges[1:]):
            amp, bmp = mp.mpf(a), mp.mpf(b)
            for r, wgt in zip(nodes_mp, weights_mp):
                u_node = (amp + bmp) / 2 + (bmp - amp) / 2 * r
                w_node = (bmp - amp) / 2 * wgt / Lmp     # du = L dsigma
                sig = u_node / Lmp
                re = m + mp.mpf('0.5') - sig
                # float64 magnitude estimate of each zero's term
                re64 = float(re)
                mag64 = np.exp(np.minimum(
                    re64 * L + (re64 * re64 - g64 * g64) * eps * eps / 2,
                    700.0)) / g64
                big = np.flatnonzero(mag64 > MP_THRESH)
                # -- large terms: mpmath --
                for i in big:
                    w = mp.mpc(re, g_mp[i])
                    term = mp.e ** (w * logX + w * w * E2h) / w
                    tot_mp += 2 * w_node * term.real
                n_mp_terms += len(big)
                # -- small terms: complex128 --
                sml = mag64 <= MP_THRESH
                if np.any(sml):
                    g = g64[sml]
                    mag = mag64[sml]
                    ph = g * L + g * re64 * eps * eps
                    num = mag * (np.cos(ph) + 1j * np.sin(ph))
                    den = re64 + 1j * g
                    tot_small += float(w_node) * 2 * float(
                        np.sum((num / den).real))
        total = tot_mp + mp.mpf(tot_small)
    return +total, n_mp_terms


# ------------------------------------- main bracket + trivial integrals ----

def zeta_taylor_at(z0, nterms=8):
    """coefficients c_n = zeta^(n)(z0)/n!, n=1..nterms (z0 a trivial zero)."""
    return [mp.zeta(mp.mpf(z0), derivative=n) / mp.factorial(n)
            for n in range(1, nterms + 1)]


def bracket_integral(x, eps, m):
    """int_0^A [ M(m+1-sigma) - (zeta'/zeta)(sigma-m)
                 - sum_{k: m-2k>=0} M(m-2k-sigma) ] dsigma.

    Every pole of every member in [0, A] cancels inside the bracket:
      sigma=m+1        M-pole vs zeta-pole of z'/z          (interior)
      sigma=m-2k>0     trivial term vs trivial zero of z'/z (interior)
      sigma=0, m even  trivial term k=m/2 vs trivial zero   (ENDPOINT;
                       stable expm1/Taylor branch, see module docstring)."""
    A = m + 3
    X, E = mp.mpf(x), mp.mpf(eps)
    L = mp.log(X)

    def Mw(w):
        return mp.e ** (w * L + w * w * E * E / 2) / w

    ks = list(range(1, m // 2 + 1))          # trivial ks inside the bracket
    even_endpoint = (m % 2 == 0) and m >= 2  # k0 = m/2 pairs at sigma = 0
    if even_endpoint:
        cs = zeta_taylor_at(-m, 8)           # zeta(u-m) = u * P(u)
        ks_reg = [k for k in ks if k != m // 2]
    else:
        ks_reg = ks
    SMALL = mp.mpf('1e-6')

    def zpz_minus_pole(sig):
        """(zeta'/zeta)(sig-m) - 1/sig, stable for sig near 0 (even m)."""
        if sig > SMALL:
            return (mp.zeta(sig - m, derivative=1) / mp.zeta(sig - m)
                    - 1 / sig)
        P = mp.mpf(0)
        dP = mp.mpf(0)
        for n, c in enumerate(cs):           # P = sum c_{n+1} sig^n
            P += c * sig ** n
            if n >= 1:
                dP += n * c * sig ** (n - 1)
        return dP / P

    def f(sig):
        tot = Mw(m + 1 - sig)
        if even_endpoint:
            h = -sig * L + sig * sig * E * E / 2
            em = mp.expm1(h) / sig if sig != 0 else -L
            tot += em - zpz_minus_pole(sig)
        else:
            tot -= mp.zeta(sig - m, derivative=1) / mp.zeta(sig - m)
        for k in ks_reg:
            tot -= Mw(m - 2 * k - sig)
        return tot

    splits = sorted({m - 2 * k for k in ks if m - 2 * k > 0} | {m + 1})
    return mp.quad(f, [0] + splits + [A]), f


def trivial_rest_integrals(x, eps, m):
    """int_0^A M(m-2k-sigma) dsigma for the first two trivial ks NOT in the
    bracket (m-2k < 0; poles all lie left of sigma=0, integrand regular)."""
    A = m + 3
    X, E = mp.mpf(x), mp.mpf(eps)
    L = mp.log(X)
    k0 = m // 2 + 1
    tot = mp.mpf(0)
    for k in (k0, k0 + 1):
        def f(sig, k=k):
            w = m - 2 * k - sig
            return mp.e ** (w * L + w * w * E * E / 2) / w
        tot += mp.quad(f, [0, A])
    return tot


# --------------------------------------------------------- small pieces ----

def R_A_term(x, eps, m):
    """sum_{p^k} (1/k) p^((m-A)k) c(p^k) = sum (1/k) p^(-3k) c(p^k) since
    A = m+3.  Truncated at p <= 1e6 (tail < 1e-13).  Weights are tiny, so
    double-precision c is harmless here."""
    ps = sieve_np(10 ** 6)
    tot = mp.mpf(0)
    xmax = x * math.exp(KCUT * eps)
    for p in map(int, ps):
        pk, k = p, 1
        while pk <= xmax:
            c = cutoff_scalar(pk, x, eps)
            if c:
                tot += mp.mpf(c) / (k * mp.mpf(pk) ** 3)
            pk *= p
            k += 1
    return tot


def prime_power_correction(x, eps, m):
    """sum_{k>=2} (1/k) p^(mk) c(p^k) — exact rationals where c=1, mpmath
    erfc in the transition band (p^k ~ x there, weight p^(mk) ~ x^m)."""
    from fractions import Fraction
    xmax = int(x * math.exp(KCUT * eps)) + 1
    ps = sieve_np(int(xmax ** 0.5) + 2)
    frac = Fraction(0)
    lo_c1 = x * math.exp(-KCUT * eps)
    with mp.workdps(ZDPS):
        fl = mp.mpf(0)
        for p in map(int, ps):
            pk, k = p * p, 2
            while pk <= xmax:
                if pk < lo_c1:
                    frac += Fraction(pk ** m, k)
                else:
                    fl += cutoff_mp(pk, x, eps) * pk ** m / k
                pk *= p
                k += 1
        fl = +fl
    return frac, fl


def window_correction(x, eps, m):
    """sum_p p^m (c(p) - [p<=x]) over the transition window (exact sieve).
    All in mpmath: weight p^m ~ x^m, so double-precision c would inject
    coherent x^(m+1)*2^-52-scale rounding bias (the documented trap)."""
    lo = int(x * math.exp(-KCUT * eps))
    hi = int(x * math.exp(KCUT * eps)) + 1
    ps = segmented_primes(lo, hi)
    tot = mp.mpf(0)
    with mp.workdps(ZDPS):
        E = mp.mpf(eps)
        s2 = mp.sqrt(2)
        for p in map(int, ps):
            ufast = float(np.log1p(ld(p - x) / ld(x)) / ld(eps))
            if abs(ufast) > KCUT:
                continue
            u = mp.log1p(mp.mpf(p - x) / x) / E
            pm = mp.mpf(p ** m)
            if p <= x:
                tot -= mp.erfc(-u / s2) / 2 * pm   # -(1 - c(p)) * p^m
            else:
                tot += mp.erfc(u / s2) / 2 * pm    # c(p) * p^m
        tot = +tot
    return tot, len(ps)


# ------------------------------------------------------------- checks ------

def exact_Sm(x, m):
    ps = sieve_np(x)
    return sum(int(p) ** m for p in ps)


def brute_T(x, eps, m):
    """T_m by direct summation: exact integers where c=1, mpmath in the
    window band.  Accurate to ~1e-12 absolute — independent check of the
    analytic T_m (zero quadrature + bracket + R_A)."""
    hi = int(x * math.exp(KCUT * eps)) + 1
    lo_c1 = x * math.exp(-KCUT * eps)
    ps = sieve_np(hi)
    bulk = 0
    with mp.workdps(ZDPS):
        band = mp.mpf(0)
        for p in map(int, ps):
            pk, k = p, 1
            while pk <= hi:
                if pk < lo_c1:
                    if k == 1:
                        bulk += pk ** m
                    else:
                        band += mp.mpf(pk ** m) / k
                else:
                    band += cutoff_mp(pk, x, eps) * pk ** m / k
                pk *= p
                k += 1
        band = +band
    return mp.mpf(bulk) + band


def psim_brute(x, eps, m, sigmas, g_mp):
    """Brute-force psim(sigma) = sum Lambda(n) n^(m-sigma) c(n) for several
    sigma.  Bulk (c=1) in mpmath dps 25 with cached ln p; window band and
    prime powers via cutoff_mp."""
    hi = int(x * math.exp(KCUT * eps)) + 1
    lo_c1 = x * math.exp(-KCUT * eps)
    ps = sieve_np(hi)
    out = []
    with mp.workdps(25):
        plist = [int(p) for p in ps]
        lnp = [mp.log(p) for p in plist]
        cwin = {}
        for p in plist:
            pk, k = p, 1
            while pk <= hi:
                if pk >= lo_c1:
                    cwin[(p, k)] = cutoff_mp(pk, x, eps)
                pk *= p
                k += 1
        for sig in sigmas:
            smp = mp.mpf(repr(sig))
            tot = mp.mpf(0)
            for p, l in zip(plist, lnp):
                pk, k = p, 1
                while pk <= hi:
                    w = cwin.get((p, k), mp.mpf(1))
                    if w:
                        tot += l * mp.e ** (k * (m - smp) * l) * w
                    pk *= p
                    k += 1
            out.append(+tot)
    return out


def psim_formula(x, eps, m, sigmas, g_mp, fbracket):
    """psim(sigma) from the explicit formula, using the SAME bracket
    integrand f that bracket_integral integrates, plus the 2000-zero sum
    (mpmath dps ZDPS) and the regular trivial terms."""
    out = []
    X, E = mp.mpf(x), mp.mpf(eps)
    L = mp.log(X)
    k0 = m // 2 + 1
    for sig in sigmas:
        smp = mp.mpf(repr(sig))
        tot = fbracket(smp)
        with mp.workdps(ZDPS):
            zsum = mp.mpf(0)
            re = m + mp.mpf('0.5') - smp
            for g in g_mp:
                w = mp.mpc(re, g)
                zsum += 2 * (mp.e ** (w * L + w * w * E * E / 2) / w).real
        tot -= zsum
        for k in (k0, k0 + 1):
            w = m - 2 * k - smp
            tot -= mp.e ** (w * L + w * w * E * E / 2) / w
        out.append(+tot)
    return out


# --------------------------------------------------------------- driver ----

def load_zeros(zf):
    g_np = np.loadtxt(zf, dtype=ld)
    with open(zf) as fh:
        g_mp = [mp.mpf(line.strip()) for line in fh if line.strip()]
    return g_np, g_mp


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    m = int(args[0])
    x = int(float(args[1]))
    zf = args[2] if len(args) > 2 else os.path.join(SCRATCH, "hpzeros2000.txt")
    A = m + 3
    g_np, g_mp = load_zeros(zf)
    eps, tailb = choose_eps(x, g_np, m)
    print(f"m={m}  x={x:.0e}  N={len(g_np)} zeros  A={A}  eps={eps:.3e}  "
          f"window=±{KCUT*eps*100:.2f}%  tail_bound={tailb:.2e}")

    if "--psim-check" in sys.argv:
        splits = {m + 1} | {m - 2 * k for k in range(1, m // 2 + 1)
                            if m - 2 * k > 0}
        sigmas = [0.0, 1e-6, 1e-3, 0.01, 0.1, 0.5]
        sigmas += [s / 2 for s in range(1, 2 * A + 1)
                   if min(abs(s / 2 - t) for t in splits) > 0.26]
        _, fbr = bracket_integral(x, eps, m)
        print("brute-forcing psim at", len(sigmas), "sigma values ...")
        br = psim_brute(x, eps, m, sigmas, g_mp)
        fo = psim_formula(x, eps, m, sigmas, g_mp, fbr)
        print(f"{'sigma':>8}  {'psim brute':>28}  {'formula-brute':>13}")
        worst = 0.0
        for s, b, f_ in zip(sigmas, br, fo):
            d = float(f_ - b)
            worst = max(worst, abs(d))
            print(f"{s:8.3g}  {mp.nstr(b, 22):>28}  {d:13.3e}")
        print(f"worst |formula - brute| = {worst:.3e}  "
              f"(zero-truncation tail bound {tailb:.1e})")
        return

    Iz, nmpt = zero_integrals(x, g_np, g_mp, eps, m)
    print(f"zero integrals      = {mp.nstr(Iz, 25)}   ({nmpt} mp terms)")
    Ibr, _ = bracket_integral(x, eps, m)
    Itr = trivial_rest_integrals(x, eps, m)
    Ra = R_A_term(x, eps, m)
    T_analytic = Ibr - Iz - Itr + Ra

    ppf, ppl = prime_power_correction(x, eps, m)
    Wc, nwin = window_correction(x, eps, m)
    pp_total = mp.mpf(ppf.numerator) / ppf.denominator + ppl
    S_analytic = T_analytic - pp_total - Wc

    print(f"T_{m} analytic       = {mp.nstr(T_analytic, 30)}")
    print(f"prime-power corr    = {mp.nstr(pp_total, 25)}")
    print(f"window corr         = {mp.nstr(Wc, 25)}  ({nwin} primes sieved)")
    print(f"S_{m} analytic       = {mp.nstr(S_analytic, 30)}")
    Sr = int(mp.nint(S_analytic))
    Sx = exact_Sm(x, m)
    print(f"S_{m} rounded        = {Sr}")
    print(f"S_{m} exact (sieve)  = {Sx}")
    print(f"difference          = {mp.nstr(S_analytic - Sx, 8)}   "
          f"{'*** EXACT INTEGER RECOVERED ***' if Sr == Sx else '(off)'}")

    if "--brute-T" in sys.argv:
        Tb = brute_T(x, eps, m)
        print(f"[brute] T_{m} = {mp.nstr(Tb, 30)}   "
              f"analytic - brute = {mp.nstr(T_analytic - Tb, 8)}")


if __name__ == "__main__":
    main()
