#!/usr/bin/env python3
"""
Prime sums in arithmetic progressions mod 4 from zeros of L(s, chi4).

chi4 = the nonprincipal (odd) character mod 4; L(s,chi4) = beta(s) =
sum_{n>=0} (-1)^n (2n+1)^(-s), computed two ways:
  * 4^(-s) [zeta(s,1/4) - zeta(s,3/4)]  (Hurwitz; fast at height, but the
    1/(s-1) poles of the two Hurwitz zetas only cancel analytically, so
    this form is unusable numerically near s=1), and
  * 2^(-s) Phi(-1, s, 1/2)              (Lerch; entire in s, used |s-1|<1/4).

STEP 1 -- zeros.  chi4 is odd (a=1), conductor q=4, Gauss sum tau=2i, so the
completed function Lambda(s) = (4/pi)^((s+1)/2) Gamma((s+1)/2) L(s,chi4)
satisfies Lambda(1-s) = Lambda(s) with root number  i^a sqrt(q)/tau = 2i/2i =
+1.  Coefficients are real, so conj Lambda(1/2+it) = Lambda(1/2-it) =
Lambda(1/2+it): Lambda is REAL on the critical line.  Dividing by the
positive factor (4/pi)^(3/4) |Gamma(3/4+it/2)| gives the Hardy Z analog
    Z(t) = exp(i theta(t)) L(1/2+it, chi4),
    theta(t) = Im log Gamma(3/4 + it/2) + (t/2) log(4/pi),
verified real to ~1e-40 relative before scanning.  Zeros: scan t in steps of
0.15, refine sign changes by Illinois iteration to width 1e-22.  Count
cross-check: n - theta(gamma_n)/pi must stay in a narrow band (a missed pair
would step it by 2).

STEP 2 -- twisted explicit formula.  With c(t) = erfc(ln(t/x)/(sqrt2 eps))/2
and M(s) = x^s/s exp(s^2 eps^2/2)  (c(n) = (1/2pi i) int M(s) n^-s ds),
Perron against -L'/L(s + sigma - 1) gives, for sigma in [0, A]:
    psi1t_chi(sigma) = sum_n Lambda(n) chi4(n) n^(1-sigma) c(n)
        = - sum_rho M(rho+1-sigma)        (nontrivial zeros, res -1 each)
          - (L'/L)(sigma-1)               (M's pole at s=0, residue 1)
          - sum_{k>=0} M(-2k-sigma)       (trivial zeros at -1,-3,-5,...)
NO main term: L(s,chi4) is entire.  The trivial-zero sum is truncated at
k<=2 (terms are ~x^(-2k-sigma); the shifted-contour remainder is far below
target).  SIGMA -> 0 BOOKKEEPING: s = -1 is itself a trivial zero of L, so
L'/L(sigma-1) = 1/sigma + h(sigma) with h analytic, while the k=0 trivial
term M(-sigma) = -1/sigma + ln x + O(sigma).  The two 1/sigma poles cancel
in the pair
    G(sigma) := -(L'/L)(sigma-1) - M(-sigma)
             -> -(ln x + L''(-1)/(2 L'(-1)))   as sigma -> 0.
G is evaluated by its Taylor expansion (coefficients from mp.taylor of L at
-1) for sigma < 1e-6 and directly (50 dps absorbs the 1/sigma cancellation)
otherwise, so the sigma-integral runs over the full [0, A].

STEP 3 -- combine.  Log-stripping (1/ln n = int_0^A n^-sigma dsigma +
n^-A/ln n) gives
    Tt_chi = sum_{p^k} chi4(p^k) (p^k/k) c(p^k)
           = -Iz_chi + int_0^A G + (-It_chi) + Ra_chi ,
then S_chi = Tt_chi - [exact chi-signed prime-power correction, k>=2], and
with S_odd from the reference all-primes pipeline (same eps!) minus 2*c(2):
    sum_{p<=x, p=1(4)} p = (S_odd + S_chi)/2 - W1 ,
    sum_{p<=x, p=3(4)} p = (S_odd - S_chi)/2 - W3 ,
W1/W3 = per-progression exact window corrections (high-precision u rule:
u from log1p((p-x)/x) on exact integers, mp.erfc).  Both use the SAME
cutoff c, so eps is chosen from the (scarcer) chi4 zeros: eps = mult/gamma_N
with the truncation tail bound < 0.02.

Usage (from anywhere; zeros file lives next to this script):
  ap_sums.py selftest                   # L values, Z reality, G series checks
  ap_sums.py zeros --tmin 0 --tmax 640 [--step 0.15] [--out FILE]
  ap_sums.py merge --out chi4_zeros.txt chunk1 chunk2 ...   # + count checks
  ap_sums.py validate X [sigma ...]     # pointwise psi1t_chi vs brute force
  ap_sums.py run X                      # full AP pipeline, verified vs sieve
"""
import sys, os, math, time
import numpy as np
import mpmath as mp
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
PROTO = os.path.dirname(HERE)
sys.path.insert(0, PROTO)
import analytic_sum as ref          # sets mp.mp.dps = 50 on import

ld = np.longdouble
A = ref.A                            # 4.0
KCUT = ref.KCUT                      # 12.0
ZEROS_FILE = os.path.join(HERE, "chi4_zeros.txt")
ZETA_ZEROS = os.path.join(ref.SCRATCH, "hpzeros2000.txt")


# ---------------------------------------------------------------- L(s,chi4)
def L_hur(s):
    """4^(-s)[zeta(s,1/4)-zeta(s,3/4)]; NOT usable near s=1 (pole cancel)."""
    return mp.mpf(4) ** (-s) * (mp.zeta(s, mp.mpf(1) / 4) - mp.zeta(s, mp.mpf(3) / 4))


def L_ler(s):
    """2^(-s) LerchPhi(-1,s,1/2); entire, used near s=1."""
    return mp.mpf(2) ** (-s) * mp.lerchphi(-1, s, mp.mpf(1) / 2)


def LpL(w):
    """(L'/L)(w, chi4) for w real (or complex) away from zeros of L."""
    if abs(w - 1) < mp.mpf(1) / 4:
        return mp.diff(L_ler, w) / L_ler(w)
    num = mp.zeta(w, mp.mpf(1) / 4, 1) - mp.zeta(w, mp.mpf(3) / 4, 1)
    den = mp.zeta(w, mp.mpf(1) / 4) - mp.zeta(w, mp.mpf(3) / 4)
    return -mp.log(4) + num / den


# ------------------------------------------------------------- Hardy Z(t)
def theta_chi(t):
    t = mp.mpf(t)
    return mp.im(mp.loggamma(mp.mpf(3) / 4 + 0.5j * t)) + t / 2 * mp.log(4 / mp.pi)


def Zc(t):
    """exp(i theta) L(1/2+it): mathematically real; Im kept as diagnostic."""
    return mp.expj(theta_chi(t)) * L_hur(mp.mpf(1) / 2 + 1j * mp.mpf(t))


def Zr(t):
    return mp.re(Zc(t))


def illinois(f, a, b, fa, fb, width):
    """Bracketed secant (Illinois): keeps the sign change, superlinear."""
    for _ in range(300):
        t = b - fb * (b - a) / (fb - fa)
        lo, hi = (a, b) if a < b else (b, a)
        if not (lo < t < hi):
            t = (a + b) / 2
        ft = f(t)
        if ft == 0:
            return t
        if mp.sign(ft) == mp.sign(fb):
            b, fb = t, ft
            fa = fa / 2
        else:
            a, fa = b, fb
            b, fb = t, ft
        if abs(b - a) < width:
            return (a + b) / 2
    return (a + b) / 2


def find_zeros(tmin, tmax, step, out):
    """Scan Z for sign changes on [tmin, tmax], refine to ~1e-22."""
    t0 = time.time()
    zeros = []
    max_im = 0.0
    with mp.workdps(30):
        t = mp.mpf(tmin)
        z = Zc(t)
        f0 = mp.re(z)
        while t < tmax:
            t2 = min(t + mp.mpf(step), mp.mpf(tmax))
            z = Zc(t2)
            f1 = mp.re(z)
            mi = float(abs(mp.im(z)) / (abs(z) + mp.mpf('1e-30')))
            max_im = max(max_im, mi)
            if mp.sign(f0) != mp.sign(f1) and f0 != 0:
                with mp.workdps(40):
                    a, b = mp.mpf(t), mp.mpf(t2)
                    r = illinois(Zr, a, b, Zr(a), Zr(b), mp.mpf('1e-22'))
                zeros.append(r)
            t, f0 = t2, f1
    with open(out, "w") as fh:
        for r in zeros:
            fh.write(mp.nstr(r, 25, strip_zeros=False) + "\n")
    print(f"[{tmin},{tmax}] step {step}: {len(zeros)} zeros -> {out}  "
          f"max |Im Z|/|Z| = {max_im:.2e}  ({time.time()-t0:.0f}s)")


def merge_zeros(out, chunks):
    allz = []
    for c in chunks:
        with open(c) as fh:
            allz += [mp.mpf(line.strip()) for line in fh if line.strip()]
    allz.sort()
    dedup = []
    for z in allz:
        if not dedup or z - dedup[-1] > mp.mpf('1e-8'):
            dedup.append(z)
    # count cross-check: d_n = n - theta(gamma_n)/pi should sit in a narrow
    # band (S(T) oscillation); a missed pair steps it down by 2.
    with mp.workdps(30):
        d = [float(n + 1 - theta_chi(g) / mp.pi) for n, g in enumerate(dedup)]
    dmin, dmax = min(d), max(d)
    jumps = max(abs(d[i + 1] - d[i]) for i in range(len(d) - 1))
    with open(out, "w") as fh:
        for z in dedup:
            fh.write(mp.nstr(z, 25, strip_zeros=False) + "\n")
    print(f"merged {len(allz)} -> {len(dedup)} zeros -> {out}")
    print(f"first 5: {[mp.nstr(z,12) for z in dedup[:5]]}")
    print(f"last:    {mp.nstr(dedup[-1], 15)}")
    print(f"count check  n - theta/pi:  min {dmin:.3f}  max {dmax:.3f}  "
          f"largest step {jumps:.3f}  (band width {dmax-dmin:.3f}; "
          f"{'OK' if dmax - dmin < 1.5 else 'SUSPECT — possible missed pair'})")


# ------------------------------------------------- explicit-formula pieces
def load_chi_gammas_ld():
    return np.loadtxt(ZEROS_FILE, dtype=ld)


def load_chi_gammas_mp():
    with open(ZEROS_FILE) as fh:
        return [mp.mpf(line.strip()) for line in fh if line.strip()]


def chi_tail_bound(x, gam_ld, eps):
    """Heuristic truncation tail over unseen chi4 zeros (density
    N(T) ~ (T/2pi) log(2T/(pi e)); ordinates underestimated -> bound over)."""
    gN = float(gam_ld[-1])
    n0 = len(gam_ld)
    ns = np.arange(n0 + 1, n0 + 200001, dtype=np.float64)
    gtail = 2 * math.pi * ns / np.log(ns + 10)
    gtail = np.maximum(gtail, gN + (ns - n0) * 0.1)
    return float(2 * np.sum(x ** 1.5 * np.exp((2.25 - gtail ** 2) * eps ** 2 / 2) / gtail))


def pick_eps(x, gam_ld):
    gN = float(gam_ld[-1])
    for mult in np.arange(8.0, 14.01, 0.5):
        eps = mult / gN
        tb = chi_tail_bound(x, gam_ld, eps)
        if tb < 0.02:
            return eps, tb
    return eps, tb


def G_factory(x, eps):
    """G(sigma) = -(L'/L)(sigma-1) - M(-sigma), smooth on [0, A].
    Taylor branch for sigma < 1e-6 from L's expansion at -1."""
    X, E = mp.mpf(x), mp.mpf(eps)
    lnX = mp.log(X)
    with mp.workdps(70):
        ts = mp.taylor(L_hur, mp.mpf(-1), 4)
    assert abs(ts[0]) < mp.mpf('1e-40'), "L(-1) != 0 ?!"
    c1 = ts[1]
    r1, r2, r3 = ts[2] / c1, ts[3] / c1, ts[4] / c1
    a, b = -lnX, E * E / 2
    # L'/L(sigma-1) = 1/sigma + h,  h = r1 + (2 r2 - r1^2) s + (3 r3 - 3 r1 r2 + r1^3) s^2
    # -M(-sigma)    = 1/sigma + a + (a^2/2 + b) s + (a^3/6 + a b) s^2
    g0 = a - r1
    g1 = (a * a / 2 + b) - (2 * r2 - r1 * r1)
    g2 = (a ** 3 / 6 + a * b) - (3 * r3 - 3 * r1 * r2 + r1 ** 3)

    def M(w):
        return mp.e ** (w * lnX + w * w * E * E / 2) / w

    def G(sig):
        sig = mp.mpf(sig)
        if sig < mp.mpf('1e-6'):
            return g0 + (g1 + g2 * sig) * sig
        return -LpL(sig - 1) - M(-sig)

    return G, (g0, g1, g2)


def G_integral(x, eps):
    G, _ = G_factory(x, eps)
    with mp.workdps(35):
        return mp.quad(G, [0, mp.mpf(1) / 2, 2, A])


def trivial_integrals_chi(x, eps):
    """sum_{k=1,2} int_0^A M(-2k-sigma) dsigma  (k=0 lives inside G)."""
    X, E = mp.mpf(x), mp.mpf(eps)
    tot = mp.mpf(0)
    for k in (1, 2):
        def f(sig, k=k):
            w = -2 * k - sig
            return mp.e ** (w * mp.log(X) + w * w * E * E / 2) / w
        tot += mp.quad(f, [0, A])
    return tot


def chi4_pk(p, k):
    """chi4(p^k) for odd prime p."""
    return 1 if (p % 4 == 1 or k % 2 == 0) else -1


def R_A_chi(x, eps):
    """sum_{p^k, p odd} chi4(p^k) (1/k) p^(-(A-1)k) c(p^k), full support."""
    xmax = x * math.exp(KCUT * eps)
    ps = ref.sieve_np(int(xmax) + 1)
    tot = mp.mpf(0)
    for p in map(int, ps):
        if p == 2:
            continue
        pk, k = p, 1
        while pk <= xmax:
            c = ref.cutoff_scalar(pk, x, eps)
            if c:
                tot += chi4_pk(p, k) * mp.mpf(c) / (k * mp.mpf(pk) ** (A - 1))
            pk *= p
            k += 1
    return tot


def prime_power_correction_chi(x, eps):
    """sum_{k>=2, p odd} chi4(p^k) p^k/k c(p^k): exact rationals where c=1,
    mp erfc in the transition band."""
    xmax = int(x * math.exp(KCUT * eps)) + 1
    ps = ref.sieve_np(int(xmax ** 0.5) + 2)
    frac = Fraction(0)
    fl = mp.mpf(0)
    lo_c1 = x * math.exp(-KCUT * eps)
    for p in map(int, ps):
        if p == 2:
            continue
        pk, k = p * p, 2
        while pk <= xmax:
            s = chi4_pk(p, k)
            if pk < lo_c1:
                frac += Fraction(s * pk, k)
            else:
                fl += s * ref.cutoff_mp(pk, x, eps) * pk / k
            pk *= p
            k += 1
    return frac, fl


def window_corrections_mod4(x, eps):
    """Per-progression window corrections sum_p p (c(p) - [p<=x]),
    high-precision u rule (log1p on exact integers, mp.erfc)."""
    lo = int(x * math.exp(-KCUT * eps))
    hi = int(x * math.exp(KCUT * eps)) + 1
    ps = ref.segmented_primes(lo, hi)
    tot = {1: mp.mpf(0), 3: mp.mpf(0)}
    with mp.workdps(25):
        E = mp.mpf(eps)
        s2 = mp.sqrt(2)
        for p in map(int, ps):
            r = p % 4
            if r not in tot:
                continue
            ufast = float(np.log1p(ld(p - x) / ld(x)) / ld(eps))
            if abs(ufast) > KCUT:
                continue
            u = mp.log1p(mp.mpf(p - x) / x) / E
            if p <= x:
                tot[r] -= mp.erfc(-u / s2) / 2 * p
            else:
                tot[r] += mp.erfc(u / s2) / 2 * p
    return tot[1], tot[3], len(ps)


# --------------------------------------------------- pointwise validation
def psi1t_chi_analytic(x, eps, sigma, gam_mp):
    """psi1t_chi(sigma) from the explicit formula (sigma > 0, != 2 poles ok)."""
    X, E = mp.mpf(x), mp.mpf(eps)
    lnX = mp.log(X)
    sig = mp.mpf(sigma)

    def M(w):
        return mp.e ** (w * lnX + w * w * E * E / 2) / w

    zs = mp.mpf(0)
    for g in gam_mp:
        zs += 2 * mp.re(M(mp.mpf(3) / 2 - sig + 1j * g))
    triv = mp.fsum(M(-2 * k - sig) for k in range(3))
    return -zs - LpL(sig - 1) - triv


def psi1t_chi_brute(x, eps, sigma):
    """sum_n Lambda(n) chi4(n) n^(1-sigma) c(n) by direct summation;
    c = 1 below the window (exact), mp.erfc inside it."""
    xmax = int(x * math.exp(KCUT * eps)) + 1
    lo_c1 = x * math.exp(-KCUT * eps)
    ps = ref.sieve_np(xmax)
    sig = mp.mpf(sigma)
    tot = mp.mpf(0)
    with mp.workdps(30):
        for p in map(int, ps):
            if p == 2:
                continue
            lp = mp.log(p)
            pk, k = p, 1
            while pk <= xmax:
                c = mp.mpf(1) if pk < lo_c1 else ref.cutoff_mp(pk, x, eps)
                if c:
                    tot += chi4_pk(p, k) * lp * mp.mpf(pk) ** (1 - sig) * c
                pk *= p
                k += 1
    return tot


def validate(x, sigmas):
    gam_ld = load_chi_gammas_ld()
    gam_mp = load_chi_gammas_mp()
    eps, tb = pick_eps(x, gam_ld)
    print(f"x={x:.0e}  N={len(gam_ld)} chi4 zeros (last {float(gam_ld[-1]):.3f})  "
          f"eps={eps:.4e}  tail_bound={tb:.2e}")
    for sig in sigmas:
        t0 = time.time()
        an = psi1t_chi_analytic(x, eps, sig, gam_mp)
        br = psi1t_chi_brute(x, eps, sig)
        rel = abs(an - br) / (abs(br) + mp.mpf('1e-30'))
        print(f"sigma={sig:<5}: analytic={mp.nstr(an, 18):<24} "
              f"brute={mp.nstr(br, 18):<24} diff={mp.nstr(an - br, 4)}  "
              f"rel={mp.nstr(rel, 3)}  ({time.time()-t0:.0f}s)")


# --------------------------------------------------------------- full run
def true_ap_sums(x):
    ps = ref.sieve_np(int(x))
    s1 = int(np.sum(ps[ps % 4 == 1]))
    s3 = int(np.sum(ps[ps % 4 == 3]))
    return s1, s3


def run(x):
    gam_ld = load_chi_gammas_ld()
    eps, tb = pick_eps(x, gam_ld)
    gz = np.loadtxt(ZETA_ZEROS, dtype=ld)
    print(f"x={x:.0e}  chi4 zeros: N={len(gam_ld)} (last {float(gam_ld[-1]):.3f})  "
          f"zeta zeros: N={len(gz)}")
    print(f"eps={eps:.4e}  window=±{KCUT*eps*100:.2f}%  chi tail bound={tb:.2e}")

    # ---- all-primes pipeline (reference, at OUR eps so c matches) ----
    t0 = time.time()
    Iz_all = ref.zero_integrals(x, gz, eps)
    Im_all = ref.main_pair_integral(x, eps)
    It_all = ref.trivial_integrals(x, eps)
    Ra_all = ref.R_A_term(x, eps)
    Tt_all = Im_all - mp.mpf(repr(float(Iz_all))) - It_all + Ra_all
    ppf, ppl = ref.prime_power_correction(x, eps)
    S_all = Tt_all - (mp.mpf(ppf.numerator) / ppf.denominator + ppl)
    S_odd = S_all - 2                      # p=2: chi0-side only, c(2)=1
    assert 2 < x * math.exp(-KCUT * eps)
    print(f"S_all smooth       = {mp.nstr(S_all, 25)}   ({time.time()-t0:.0f}s)")

    # ---- twisted pipeline ----
    t0 = time.time()
    Iz_chi = ref.zero_integrals(x, gam_ld, eps)
    IG = G_integral(x, eps)
    It_chi = trivial_integrals_chi(x, eps)
    Ra_chi = R_A_chi(x, eps)
    Tt_chi = -mp.mpf(repr(float(Iz_chi))) + IG - It_chi + Ra_chi
    ppfc, pplc = prime_power_correction_chi(x, eps)
    S_chi = Tt_chi - (mp.mpf(ppfc.numerator) / ppfc.denominator + pplc)
    print(f"Tt_chi             = {mp.nstr(Tt_chi, 25)}   ({time.time()-t0:.0f}s)")
    print(f"S_chi smooth       = {mp.nstr(S_chi, 25)}")

    # ---- combine + window ----
    t0 = time.time()
    W1, W3, nwin = window_corrections_mod4(x, eps)
    S1 = (S_odd + S_chi) / 2 - W1
    S3 = (S_odd - S_chi) / 2 - W3
    print(f"window corr        = W1 {mp.nstr(W1, 20)}  W3 {mp.nstr(W3, 20)}  "
          f"({nwin} primes, {time.time()-t0:.0f}s)")

    S1r, S3r = int(mp.nint(S1)), int(mp.nint(S3))
    s1t, s3t = true_ap_sums(x)
    print(f"S(p=1 mod 4) analytic = {mp.nstr(S1, 25)}")
    print(f"S(p=1 mod 4) rounded  = {S1r}")
    print(f"S(p=1 mod 4) sieve    = {s1t}")
    print(f"  difference = {mp.nstr(S1 - s1t, 6)}   "
          f"{'*** EXACT INTEGER RECOVERED ***' if S1r == s1t else '(off)'}")
    print(f"S(p=3 mod 4) analytic = {mp.nstr(S3, 25)}")
    print(f"S(p=3 mod 4) rounded  = {S3r}")
    print(f"S(p=3 mod 4) sieve    = {s3t}")
    print(f"  difference = {mp.nstr(S3 - s3t, 6)}   "
          f"{'*** EXACT INTEGER RECOVERED ***' if S3r == s3t else '(off)'}")
    return S1r == s1t and S3r == s3t


# ---------------------------------------------------------------- selftest
def selftest():
    print("L values:")
    print("  L_ler(1) - pi/4    =", mp.nstr(L_ler(mp.mpf(1)) - mp.pi / 4, 3))
    print("  L_ler(2) - Catalan =", mp.nstr(L_ler(mp.mpf(2)) - mp.catalan, 3))
    print("  L_hur(0) - 1/2     =", mp.nstr(L_hur(mp.mpf(0)) - mp.mpf(1) / 2, 3))
    print("  L_hur(-1)          =", mp.nstr(L_hur(mp.mpf(-1)), 3))
    for w in (0.76, 1.24):
        d = abs(LpL(mp.mpf(w)) - (-mp.log(4)
              + (mp.zeta(mp.mpf(w), mp.mpf(1)/4, 1) - mp.zeta(mp.mpf(w), mp.mpf(3)/4, 1))
              / (mp.zeta(mp.mpf(w), mp.mpf(1)/4) - mp.zeta(mp.mpf(w), mp.mpf(3)/4))))
        print(f"  LpL branch agreement at w={w}: {mp.nstr(d, 3)}")
    print("Z reality |Im Z|/|Z| :")
    for t in (1.0, 6.1, 50.3, 200.7, 500.2, 638.9):
        z = Zc(t)
        print(f"  t={t:<6}: {mp.nstr(abs(mp.im(z))/abs(z), 3)}")
    print("G series vs direct (x=1e6, eps=0.0125):")
    G, coef = G_factory(10 ** 6, 0.0125)
    print("  G(0+) =", mp.nstr(coef[0], 20))
    for s0 in ('1e-7', '3e-6', '1e-5'):
        sig = mp.mpf(s0)
        ser = coef[0] + (coef[1] + coef[2] * sig) * sig
        dirv = -LpL(sig - 1) - (mp.e ** (-sig * mp.log(mp.mpf(10**6))
                                         + sig * sig * mp.mpf(0.0125) ** 2 / 2) / (-sig))
        print(f"  sigma={s0}: series-direct = {mp.nstr(ser - dirv, 3)}")


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return
    cmd = args[0]
    if cmd == "selftest":
        selftest()
    elif cmd == "zeros":
        opt = {"--tmin": "0", "--tmax": "640", "--step": "0.15",
               "--out": ZEROS_FILE}
        for i in range(1, len(args), 2):
            opt[args[i]] = args[i + 1]
        find_zeros(float(opt["--tmin"]), float(opt["--tmax"]),
                   float(opt["--step"]), opt["--out"])
    elif cmd == "merge":
        assert args[1] == "--out"
        merge_zeros(args[2], args[3:])
    elif cmd == "validate":
        x = int(float(args[1]))
        sigmas = [float(s) for s in args[2:]] or [0.2, 0.5, 1.0, 2.0]
        validate(x, sigmas)
    elif cmd == "run":
        run(int(float(args[1])))
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
