#!/usr/bin/env python3
"""
verify_monotonicity.py -- every constant and the explicit decrease criterion of
paper/v3/monotonicity-large-m.tex, recomputed for that draft.

Notation (as in the paper): M = m + 1/2, a_gamma(M) = 2M/sqrt(M^2+gamma^2),
  sigma^2(M) = sum 2 a^2 = 4M (log xi)'(m+1),
  D(M) = (sigma^2)'(M) = 4 (log xi)'(m+1) + 4M (log xi)''(m+1)
       = sum_gamma 16 M gamma^2/(M^2+gamma^2)^2  > 0,
  S4(M) = sum (2a)^4 = 16 sigma^2 - 64 M^2 (log xi)''(m+1),
  phi(z) = -J0'(z)/J0(z) = J1/J0.

Checks, in order:
  [1] closed forms sigma^2, D, S4 (scipy digamma/polygamma + von-Mangoldt
      Dirichlet series) against (a) the values quoted in dissolution-theorem.tex
      and (b) zero-sum + Riemann-von-Mangoldt tail evaluations of D.
  [2] Bessel constants of Lemma (J5)/(J6):
        z/2 + z^3/16 <= phi(z) <= z/2 + z^3/16 + z^5/90 <= 0.5165 z on (0, 1/2],
        |J1(z)| <= min(1, z/2),
        P = J0^2 + J1^2 decreasing;  sup_{z >= 2 sqrt2} |J0| <= sqrt(P(2 sqrt2)) <= 0.446,
        rho_1 = sup_{z >= 1.0733} |J0| <= 0.733,   j_{0,1} > 2.402 > 2.4.
  [3] self-contained window-count lower bound (GRH):
        N(sqrt3 * Y) >= [S4(Y)/8 - sigma^2(Y)]/32
      against the actual zero counts from the certified lists.
  [4] the explicit decrease criterion  MAIN(I) > TAIL(I)  on M-intervals
      I = [Ma, Mb] tiling [M_1, M_*] (M_* = gamma_max/2), for q = 4 and q = 3:
        MAIN(I) = (0.9973/pi) (D_min/2) int_0^{1/8} t^2 e^{-beta t^2} dt,
                  beta = sigma^2(Mb)/2 + S4(Mb)/1088,
        TAIL(I) >= (1/pi) int_{3/5}^infty |d/dM Phi| |sin t|/t dt, assembled from
                  per-zero sup|J0| bounds on t-cells (extrema of J0 = zeros of J1),
                  the product dropping the smallest factor (uniform over the
                  differentiated index), A(t) <= D_max t^2/2 + (4t/Ma)*#{a_g t > 1},
                  and an analytic remainder beyond t = 64 from |J0| <= (8/pi) z^{-1/2}.
      Reports the smallest grid point M_1 from which every interval up to M_*
      passes.  These are float64 evaluations with stated safety margins, the
      same rigor class as the paper's deterministic reference densities (no
      interval arithmetic is claimed; margins are printed).
  [5] the analytic large-M leg (M >= 250, no zero data):  explicit bound
        TAIL_an(M) <= (2.24/pi) [ Ia(M) + Ib(M) ] * 0.61^{n1} * 0.733^{n2-1}...
      as in the paper's Lemma (large-M tail), against MAIN_an(M), evaluated at
      M = 250, 319, 349, 500, 1000, 4000, plus the ratio's monotone decrease.
  [6] sign sanity: finite differences of deterministic Gil-Pelaez densities
      delta_q(m) across [M_1, M_*] against the predicted -D/(2 sqrt(2 pi) sigma^3).

Run: python3 verify_monotonicity.py            (needs numpy, scipy, mpmath)
"""
import os, math
import numpy as np
from scipy.special import j0, j1, jn_zeros, digamma, polygamma, erf

HERE = os.path.dirname(os.path.abspath(__file__))
EXPLORE = os.path.normpath(os.path.join(HERE, "..", "..", "prototype", "explore"))

def zeros_of(q):
    f = {4: "chi4_zeros.txt", 3: "chi3_zeros.txt"}[q]
    return np.loadtxt(os.path.join(EXPLORE, f))

# ----------------------------------------------------------------- closed forms
NSIEVE = 200_000
_spf = np.zeros(NSIEVE, dtype=np.int64)
for p in range(2, NSIEVE):
    if _spf[p] == 0:
        _spf[p::p][_spf[p::p] == 0] = p
LAM_N = np.arange(2, NSIEVE)
_lam = np.zeros(NSIEVE)
for n in range(2, NSIEVE):
    p = _spf[n]; k = n
    while k % p == 0:
        k //= p
    if k == 1:
        _lam[n] = math.log(p)
LAM = _lam[2:]

def chi_vals(q, n):
    if q == 4:
        return np.where(n % 4 == 1, 1.0, np.where(n % 4 == 3, -1.0, 0.0))
    return np.where(n % 3 == 1, 1.0, np.where(n % 3 == 2, -1.0, 0.0))

CHI = {q: chi_vals(q, LAM_N) for q in (3, 4)}
LOGN = np.log(LAM_N)

def SDS(M, q):
    """(sigma^2, D, S4) at weight M (closed forms; float64).
    s = m+1 = M+1/2, a=1 for q in {3,4}; x = (s+1)/2 = M/2 + 3/4."""
    s = M + 0.5
    x = (s + 1.0) / 2.0
    with np.errstate(under='ignore'):
        ns = np.exp(-s * LOGN)
    w = LAM * CHI[q]
    LL = -(w * ns).sum()            # L'/L(s)
    LL1 = (w * LOGN * ns).sum()     # (L'/L)'(s)
    d1 = 0.5 * math.log(q / math.pi) + 0.5 * digamma(x) + LL
    d2 = 0.25 * polygamma(1, x) + LL1
    s2 = 4.0 * M * d1
    D = 4.0 * d1 + 4.0 * M * d2
    S4 = 16.0 * s2 - 64.0 * M * M * d2
    return s2, D, S4

print("[1] closed forms sigma^2, D, S4:")
quoted = {(4, 8): (29.7125, 219.83), (4, 20): (106.3260, 1061.32),
          (4, 100): (836.8744, 10190.02), (3, 60): (407.9701, 4607.56)}
for (q, m), (s2q, S4q) in sorted(quoted.items()):
    s2, D, S4 = SDS(m + 0.5, q)
    print(f"    q={q} m={m:>3}: sigma^2={s2:12.4f} (quoted {s2q}); S4={S4:12.2f} "
          f"(quoted {S4q}); D={D:9.5f}  vs 2log(qM/2pi)+2={2*math.log(q*(m+.5)/(2*math.pi))+2:9.5f}")
# D against zero sum + RvM tail
for (q, m) in [(4, 20), (4, 100), (3, 60)]:
    g = zeros_of(q); M = m + 0.5
    head = (16 * M * g**2 / (M**2 + g**2)**2).sum()
    G = g[-1]
    tt = np.linspace(G, 400 * G, 4_000_001)
    tail = np.trapezoid(16 * M * tt**2 / (M**2 + tt**2)**2
                        * np.log(q * tt / (2 * math.pi)) / (2 * math.pi), tt) \
        + 16 * M / (400 * G) * math.log(q * 400 * G / (2 * math.pi)) / (2 * math.pi)
    s2, D, S4 = SDS(M, q)
    print(f"    q={q} m={m:>3}: D closed {D:9.5f}  zeros+RvM-tail {head+tail:9.5f} "
          f"(fluctuation-level agreement expected)")

# ----------------------------------------------------------------- [2] Bessel
print("[2] Bessel constants:")
zz = np.linspace(1e-3, 0.5, 200_000)
ph = j1(zz) / j0(zz)
lo = zz / 2 + zz**3 / 16
hi = lo + zz**5 / 90
print(f"    min(phi - (z/2+z^3/16)) on (0,1/2]     : {np.min(ph-lo):.3e}  (claim >= 0)")
print(f"    max(phi - (z/2+z^3/16+z^5/90))         : {np.max(ph-hi):.3e}  (claim <= 0)")
print(f"    max phi/z on (0,1/2]                   : {np.max(ph/zz):.6f}  (claim <= 0.5165)")
zz2 = np.linspace(1e-3, 40, 400_000)
print(f"    max(|J1| - min(1,z/2))                 : {np.max(np.abs(j1(zz2))-np.minimum(1,zz2/2)):.3e} (claim <= 0)")
P = j0(zz2)**2 + j1(zz2)**2
print(f"    max increase of P=J0^2+J1^2 (sampled)  : {np.max(np.diff(P)):.3e}  (claim <= 0)")
s8 = 2 * math.sqrt(2)
print(f"    sqrt(P(2 sqrt2)) = {math.sqrt(j0(s8)**2+j1(s8)**2):.6f}  (claim <= 0.446)")
# rigorous alternating-series enclosures used in the paper's Lemma (J6):
from fractions import Fraction
def J0_encl(z2, K):     # z2 = z^2 as Fraction; terms (z^2/4)^k/(k!)^2, alternating, decreasing from some k0
    t = [(-1)**k * (z2 / 4)**k / Fraction(math.factorial(k))**2 for k in range(K)]
    s = sum(t[:-1])
    return (float(s), float(s + t[-1])) if t[-1] > 0 else (float(s + t[-1]), float(s))
def J1_encl(z, z2, K):
    t = [(-1)**k * (z2 / 4)**k / (Fraction(math.factorial(k)) * math.factorial(k + 1)) for k in range(K)]
    s = sum(t[:-1])
    lo, hi = (s, s + t[-1]) if t[-1] > 0 else (s + t[-1], s)
    return float(lo) * z / 2, float(hi) * z / 2
j0lo, j0hi = J0_encl(Fraction(8), 12)      # z = 2 sqrt2, z^2 = 8 exactly
j1lo, j1hi = J1_encl(2 * math.sqrt(2), Fraction(8), 12)
print(f"    enclosures at z=2sqrt2: J0 in [{j0lo:.6f},{j0hi:.6f}], J1 in [{j1lo:.6f},{j1hi:.6f}]"
      f" -> sup_(z>=2sqrt2)|J0| <= {math.sqrt(max(j0lo**2,j0hi**2)+max(j1lo**2,j1hi**2)):.6f} (claim <=0.446)")
j0lo2, j0hi2 = J0_encl(Fraction(10733, 10000)**2, 10)
print(f"    enclosure J0(1.0733) in [{j0lo2:.6f},{j0hi2:.6f}]  (claim <= 0.733)")
lamlog = (LAM * LOGN / LAM_N.astype(float)**2).sum()
print(f"    sum Lambda(n) log n / n^2 = {lamlog:.6f}  (claim <= 1.1; tail beyond {NSIEVE} negligible)")
zz3 = np.linspace(1.0733, 500, 2_000_000)
print(f"    rho_1 = sup(z>=1.0733)|J0| = {np.max(np.abs(j0(zz3))):.6f} = J0(1.0733)={j0(1.0733):.6f} (claim <= 0.733)")
print(f"    j_0,1 = {jn_zeros(0,1)[0]:.6f}  (claim > 2.402; positivity region t <= 3/5 uses 4t <= 2.4 < j_0,1)")

# ----------------------------------------------------------------- [3] counts
print("[3] N(sqrt3 * Y) >= [S4(Y)/8 - sigma^2(Y)]/32  (self-contained, GRH):")
for q in (4, 3):
    g = zeros_of(q)
    for Y in (30, 60, 120, 240, g[-1] / math.sqrt(3) * 0.999):
        s2, D, S4 = SDS(Y, q)
        low = (S4 / 8 - s2) / 32
        actual = int(np.searchsorted(g, math.sqrt(3) * Y, side='right'))
        ok = "OK" if low <= actual else "VIOLATION"
        print(f"    q={q} Y={Y:8.2f}: bound {low:8.2f}  actual N({math.sqrt(3)*Y:7.1f}) = {actual:4d}  {ok}")

# ----------------------------------------------------------------- [4] criterion
EXT = jn_zeros(1, 400)          # extrema of J0
J0E = np.abs(j0(EXT))           # decreasing (successive maxima of |J0|)
SAFE = 1e-9                     # additive float safety margin on sup|J0|

def bsup_vec(lo, hi):
    """sup |J0| over [lo_i, hi_i] for arrays lo <= hi of positive args."""
    c = np.maximum(np.abs(j0(lo)), np.abs(j0(hi)))
    idx = np.searchsorted(EXT, lo)
    inside = (idx < len(EXT)) & (EXT[np.minimum(idx, len(EXT) - 1)] <= hi)
    c = np.where(inside, np.maximum(c, J0E[np.minimum(idx, len(EXT) - 1)]), c)
    return np.minimum(1.0, c + SAFE)

def Nplus(T, q):
    """Explicit upper bound N(T) <= (T/2) log(q(T+2)/2pi) + 0.57 T  (GRH; paper Lemma)."""
    return 0.5 * T * math.log(q * (T + 2) / (2 * math.pi)) + 0.57 * T

def main_lower(Dmin, s2max, S4max):
    beta = s2max / 2 + S4max / 1088.0
    a = 0.125
    I = math.sqrt(math.pi) / (4 * beta**1.5) * erf(a * math.sqrt(beta)) \
        - a / (2 * beta) * math.exp(-beta * a * a)
    return (0.9973 / math.pi) * (Dmin / 2) * I

def tail_upper(q, Ma, Mb, g, Dmax, TCAP=64.0):
    S = g[g <= 2 * Ma]
    n = len(S)
    if n < 12:
        return math.inf
    a_lo = 2 * Ma / np.sqrt(Ma**2 + S**2)
    a_hi = 2 * Mb / np.sqrt(Mb**2 + S**2)
    # t-cells
    tc = [0.6]
    while tc[-1] < 16.0:
        tc.append(min(tc[-1] * 1.05, 16.0))
    while tc[-1] < TCAP:
        tc.append(min(tc[-1] * 1.10, TCAP))
    total = 0.0
    for ta, tb in zip(tc[:-1], tc[1:]):
        lo = 2 * a_lo * ta
        hi = 2 * a_hi * tb
        b = bsup_vec(lo, hi)
        lb = np.log(b)
        logprod = lb.sum() - lb.min()          # drop the smallest factor
        # A(t) sup over the cell
        G2 = Mb * math.sqrt(max(4 * tb * tb - 1, 0.0))
        cnt = float(np.searchsorted(g, G2)) if G2 <= g[-1] else Nplus(G2, q)
        A = 0.5 * Dmax * tb * tb + 4 * tb * cnt / Ma
        total += A * min(1.0, 1.0 / ta) * math.exp(min(logprod, 50.0)) * (tb - ta)
    # analytic remainder t >= TCAP with |J0| <= (8/pi) z^{-1/2}.
    # Per-zero bound b_i(t) <= kappa_i t^{-1/2}, kappa_i = (8/pi)(2 a_lo,i)^{-1/2}
    # <= c3 < 1.905, so each bound is < 1 for t >= TCAP = 64.  For the product
    # over S minus the (unknown) differentiated index gamma we may use any
    # subset U of S \ {gamma} (omitted factors are < 1): take U = nn zeros from
    # the (nn+1) smallest-kappa zeros, avoiding gamma; the worst case drops the
    # single smallest kappa, so the bound is prod of kap_asc[1:nn+1] * t^{-nn/2}.
    kasc = np.sort((8 / math.pi) / np.sqrt(2 * a_lo))
    nn = min(n - 1, 62)
    logK = np.log(kasc[1:nn + 1]).sum()
    pw = nn / 2.0 - 1.0                     # A(t)/t * t^{-nn/2} ~ t^{-pw} (+ log t piece)
    if pw <= 1.5:
        return math.inf
    T = TCAP
    l0 = math.log(q * (2 * Mb + 2) / (2 * math.pi)) + 1.14   # Nplus(2Mb t) <= Mb t (l0 + log t), t>=1
    i1 = T**(1 - pw) / (pw - 1)                              # int_T^inf t^{-pw} dt
    i2 = T**(1 - pw) * (math.log(T) * (pw - 1) + 1) / (pw - 1)**2
    with np.errstate(under='ignore'):
        rem = math.exp(max(logK, -700.0)) * (0.5 * Dmax * i1 + 4 * Mb / Ma * (l0 * i1 + i2))
    total += rem
    return total / math.pi

def scan(q, Mlow=4.0, ratio=1.02):
    g = zeros_of(q)
    Mstar = g[-1] / 2.0
    grid = [Mlow]
    while grid[-1] < Mstar:
        grid.append(min(grid[-1] * ratio, Mstar))
    res = []
    cache = {}
    def sds(M):
        if M not in cache:
            cache[M] = SDS(M, q)
        return cache[M]
    for Ma, Mb in zip(grid[:-1], grid[1:]):
        s2a, Da, S4a = sds(Ma)
        s2b, Db, S4b = sds(Mb)
        Dmin = max(Da, Db) * (Ma / Mb)**3
        Dmax = min(Da, Db) * (Mb / Ma)**3
        ml = main_lower(Dmin, s2b, S4b)
        tl = tail_upper(q, Ma, Mb, g, Dmax)
        res.append((Ma, Mb, ml, tl, ml - tl))
    # smallest Ma from which everything up to Mstar passes
    M1 = None
    ok_from_here = True
    for Ma, Mb, ml, tl, gap in reversed(res):
        if gap <= 0:
            break
        M1 = Ma
    return res, M1, Mstar

print("[4] explicit decrease criterion on [M_1, M_*]:")
ACHIEVED = {}
for q in (4, 3):
    res, M1, Mstar = scan(q)
    ACHIEVED[q] = (M1, Mstar)
    worst = min((r[4] / r[2] for r in res if r[0] >= (M1 or 1e9)), default=float('nan'))
    print(f"    q={q}: M_* = {Mstar:.2f}; criterion passes on every interval of "
          f"[{M1:.3f}, {Mstar:.2f}]" if M1 else f"    q={q}: criterion never holds")
    if M1:
        print(f"          worst relative margin (main-tail)/main on that range: {worst:.3f}")
        # a few sample rows
        for r in res:
            if abs(r[0] - M1) < 1e-12 or abs(r[0] - 2 * M1) / M1 < 0.02 or abs(r[0] - Mstar / 2) / Mstar < 0.01:
                print(f"          [{r[0]:8.3f},{r[1]:8.3f}]  main {r[2]:.3e}  tail {r[3]:.3e}")
        # first failing interval below M1
        bad = [r for r in res if r[1] <= M1 + 1e-9 and r[4] <= 0]
        if bad:
            r = bad[-1]
            print(f"          first failure below: [{r[0]:8.3f},{r[1]:8.3f}]  main {r[2]:.3e}  tail {r[3]:.3e}")

# ----------------------------------------------------------------- [5] analytic leg
print("[5] analytic large-M leg (no zero data; M >= 300), closed-form constants as in the paper:")
def analytic_leg(q, M, safety=5.0):
    """safety=0.5 is the paper's Lemma (n_i = Y_i(l_{Y_i}-2)/16 - 1/2);
    safety=5.0 additionally weakens n_i by 9/2 (extra margin)."""
    l = math.log(q * M / (2 * math.pi))
    Y1, Y2 = M / math.sqrt(3), 2 * M / math.sqrt(3)
    n1 = Y1 * (math.log(q * Y1 / (2 * math.pi)) - 2) / 16 - safety
    n2 = Y2 * (math.log(q * Y2 / (2 * math.pi)) - 2) / 16 - safety
    if min(n1, n2) < 12:
        return None
    Dmax = 2 * l + 2 + 8 / M
    Dmin = 2 * l + 2 - 8 / M
    s2max = 2 * M * l + 3.1
    S4max = 32 * M * (l - 1) + 100
    # [3/5,16]:  int A(t) min(1,1/t) dt <= 64 Dmax + 512 l0 + 1165  (closed form, paper)
    l0 = math.log(q * (2 * M + 2) / (2 * math.pi)) + 1.14
    Ia = 64 * Dmax + 512 * l0 + 1165
    # product bound on [0.6,16]: all N(2M)>=n2 zeros' factors <= 0.733, and the
    # N(M)>=n1 zeros below M improve to 0.447; monotone in the true counts, so
    # <= 0.61^{n1} 0.733^{n2}; dropping one factor for the differentiated index
    # costs a further /0.447.
    logprod = n1 * math.log(0.447 / 0.733) + n2 * math.log(0.733) - math.log(0.447)
    # t >= 16: any 9 of the >= n2 zeros carry (c3/sqrt t) <= 0.48, one factor is
    # dropped, the rest keep 0.733 (no zone-1 refinement here): 0.733^{n2-10}.
    c3 = 4 * 5**0.25 / math.pi
    T = 16.0
    i1 = T**(-2.5) / 2.5
    i2 = T**(-2.5) * (math.log(T) * 2.5 + 1) / 2.5**2
    Ib = c3**9 * (0.5 * Dmax * i1 + 4 * (l0 * i1 + i2)) \
        * math.exp((n2 - 10) * math.log(0.733))
    tail = (Ia * math.exp(logprod) + Ib) / math.pi
    main = main_lower(Dmin, s2max, S4max)
    return main, tail
for q in (4, 3):
    for M in (300, ACHIEVED[q][1], 500, 1000, 4000):
        r = analytic_leg(q, M)
        rp = analytic_leg(q, M, safety=0.5)
        if r:
            main, tail = r
            print(f"    q={q} M={M:7.1f}: main >= {main:.3e}  tail <= {tail:.3e}  "
                  f"ratio {tail/main:.2e}  {'OK' if tail < main else 'FAIL'}"
                  f"   [paper n_i-1/2: ratio {rp[1]/rp[0]:.2e}]")
# log-derivative bounds of the paper's Lemma (repaired constants): each of the
# two TAIL_an summands' ratio to MAIN_an must have log-derivative <= -0.14
# resp. <= -0.08 at M = 300 (and beyond, monotonely).
def leg_summands(q, M):
    l = math.log(q * M / (2 * math.pi))
    Y1, Y2 = M / math.sqrt(3), 2 * M / math.sqrt(3)
    n1 = Y1 * (math.log(q * Y1 / (2 * math.pi)) - 2) / 16 - 0.5
    n2 = Y2 * (math.log(q * Y2 / (2 * math.pi)) - 2) / 16 - 0.5
    Dp = 2 * l + 2 + 8 / M
    l0 = math.log(q * (2 * M + 2) / (2 * math.pi)) + 1.14
    T1 = (64 * Dp + 512 * l0 + 1165) / (0.447 * math.pi) \
        * (0.447 / 0.733)**n1 * 0.733**n2
    c3 = 4 * 5**0.25 / math.pi
    i1 = 16.0**(-2.5) / 2.5
    i2 = 16.0**(-2.5) * (math.log(16.0) * 2.5 + 1) / 6.25
    T2 = (c3**9 / math.pi) * (0.5 * Dp * i1 + 4 * (l0 * i1 + i2)) * 0.733**(n2 - 10)
    main = main_lower(2 * l + 2 - 8 / M, 2 * M * l + 3.1, 32 * M * (l - 1) + 100)
    return T1, T2, main
for q in (4, 3):
    h = 0.01
    a = leg_summands(q, 300 - h); b = leg_summands(q, 300 + h)
    d1 = (math.log(b[0] / b[2]) - math.log(a[0] / a[2])) / (2 * h)
    d2 = (math.log(b[1] / b[2]) - math.log(a[1] / a[2])) / (2 * h)
    print(f"    q={q} M=300: d/dM log(T1/MAIN) = {d1:.4f} (claim <= -0.14); "
          f"d/dM log(T2/MAIN) = {d2:.4f} (claim <= -0.08); T2/T1 = {b[1]/b[0]:.1e}")

# ----------------------------------------------------------------- [6] sign sanity
print("[6] finite differences of deterministic Gil-Pelaez densities (float64 reference):")
def delta_ref(m, q, T=2.2, n=400_001):
    g = zeros_of(q); M = m + 0.5
    a = 2 * M / np.sqrt(M**2 + g**2)
    s2, D, S4 = SDS(M, q)
    tv = s2 - (2 * a**2).sum()
    t = np.linspace(1e-12, T, n)
    lg = np.zeros_like(t); sg = np.ones_like(t)
    for av in a:
        v = j0(2 * av * t)
        lg += np.log(np.abs(v) + 1e-300); sg *= np.sign(v)
    phi = sg * np.exp(lg - tv * t * t / 2)
    return 0.5 + np.trapezoid(phi * np.sin(t) / t, t) / math.pi
for q in (4, 3):
    for m in (20.0, 60.0):
        h = 0.5
        dm = (delta_ref(m + h, q) - delta_ref(m - h, q)) / (2 * h)
        s2, D, S4 = SDS(m + 0.5, q)
        pred = -D / (2 * math.sqrt(2 * math.pi) * s2**1.5)
        print(f"    q={q} m={m}: (delta(m+.5)-delta(m-.5))/1 = {dm:+.3e}   -D/(2 sqrt(2pi) sigma^3) = {pred:+.3e}")

print("done.")
