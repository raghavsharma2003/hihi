#!/usr/bin/env python3
"""
Modulus universality test: weighted Chebyshev races mod 3.

chi3 = the nonprincipal character mod 3 (chi3(1)=+1, chi3(2)=-1), ODD since
chi3(-1)=chi3(2)=-1.  L(s,chi3) = 3^(-s)[zeta(s,1/3) - zeta(s,2/3)].

STEP 1 -- zeros.  chi3 is odd (a=1), conductor q=3, Gauss sum
tau(chi3) = e^(2 pi i/3) - e^(4 pi i/3) = i sqrt(3), so the completed
function Lambda(s) = (3/pi)^((s+1)/2) Gamma((s+1)/2) L(s,chi3) satisfies
Lambda(1-s) = eps Lambda(s) with root number eps = tau/(i^a sqrt q)
= i sqrt3 / (i sqrt3) = +1.  Real coefficients + eps=+1 make Lambda REAL
on the critical line, so the Hardy Z analog
    Z(t) = exp(i theta3(t)) L(1/2+it, chi3),
    theta3(t) = Im log Gamma(3/4 + it/2) + (t/2) log(3/pi),
is real (verified numerically to ~1e-28 relative before scanning; the task
threshold 1e-20 is met with a wide margin).  Zeros: scan t in steps of 0.15,
refine sign changes by Illinois iteration to width 1e-22.  Cross-checks:
first zero must be near t = 8.04; n - theta3(gamma_n)/pi must stay in a
narrow band (a missed pair steps it by 2); total count vs
N(T) = (T/2pi) log(3T/(2 pi e)).

STEP 2 -- race and density.  D_m(x) = sum_{p<=x, p=2(3)} p^m
- sum_{p=1(3)} p^m  (2 = the non-residue class mod 3; squares of primes
p != 3 are all = 1 mod 3, so the bias favors the 2-side, exactly as the
3-side mod 4).  In theta-form the explicit formula gives, verbatim as mod 4,
  R_m(x) = x^(m+1/2)/(2m+1) + sum_rho x^(rho+m)/(rho+m) + smaller,
rho now over zeros of L(s,chi3), so the normalized race is E_m = 1 + V_m,
  V_m = sum_{gamma>0} a_gamma(m) 2 cos(theta_gamma),
  a_gamma(m) = (2m+1)/sqrt((m+1/2)^2 + gamma^2)      <- kernel UNCHANGED,
and under GRH+LI  delta_3(m) = P(1 + V_m > 0).  Only the zeros and the
tail density change: for modulus q the density of ordinates is
(1/2pi) log(q t/(2 pi)), i.e. (1/2pi) log(3t/(2 pi)) here.
Anchor: delta_3(0) must reproduce the classical 0.9990 (Rubinstein-Sarnak).

STEP 3 -- dissolution law, general q.  With gamma = (m+1/2)u,
  Var_q(m) ~ int_0^inf 2 (2m+1)^2/((m+1/2)^2+g^2) (1/2pi) log(q g/(2pi)) dg
           = (8(m+1/2)/(2pi)) int_0^inf [log(q(m+1/2)/(2pi)) + log u]/(1+u^2) du
           = 2 (m+1/2) log( q(m+1/2) / (2 pi) ),
using int du/(1+u^2) = pi/2 and int log u/(1+u^2) du = 0.  The EXACT
constant is q/(2pi) inside the log; at q=4 this is log(2(m+1/2)/pi),
matching the established mod-4 law (the draft form log(q(m+1/2)/pi) is off
by a factor 2 inside the log for general q).  Then
  delta_q(m) - 1/2 ~ 1/sqrt(2 pi Var_q(m)).

Usage (zeros file lives next to this script):
  race_mod3.py selftest                    # L values, Z reality
  race_mod3.py zeros --tmin A --tmax B [--step 0.15] [--out FILE]
  race_mod3.py merge --out chi3_zeros.txt chunk1 chunk2 ...
  race_mod3.py density [n_samples]         # delta_3(m) table + law comparison
"""
import sys, os, math, time
import numpy as np
import mpmath as mp

mp.mp.dps = 30
HERE = os.path.dirname(os.path.abspath(__file__))
ZEROS_FILE = os.path.join(HERE, "chi3_zeros.txt")
Q = 3


# ---------------------------------------------------------------- L(s,chi3)
def L_hur(s):
    """3^(-s)[zeta(s,1/3)-zeta(s,2/3)]; poles at s=1 cancel analytically,
    so avoid a small neighborhood of s=1 (not an issue on Re s = 1/2)."""
    return mp.mpf(3) ** (-s) * (mp.zeta(s, mp.mpf(1) / 3) - mp.zeta(s, mp.mpf(2) / 3))


# ------------------------------------------------------------- Hardy Z(t)
def theta_chi(t):
    t = mp.mpf(t)
    return mp.im(mp.loggamma(mp.mpf(3) / 4 + 0.5j * t)) + t / 2 * mp.log(3 / mp.pi)


def Zc(t):
    """exp(i theta3) L(1/2+it): mathematically real; Im kept as diagnostic."""
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
    # count cross-check: d_n = n - theta3(gamma_n)/pi should sit in a narrow
    # band (S(T) oscillation); a missed pair steps it down by 2.
    with mp.workdps(30):
        d = [float(n + 1 - theta_chi(g) / mp.pi) for n, g in enumerate(dedup)]
    dmin, dmax = min(d), max(d)
    jumps = max(abs(d[i + 1] - d[i]) for i in range(len(d) - 1))
    T = float(dedup[-1])
    NT = T / (2 * math.pi) * math.log(Q * T / (2 * math.pi * math.e))
    with open(out, "w") as fh:
        for z in dedup:
            fh.write(mp.nstr(z, 25, strip_zeros=False) + "\n")
    print(f"merged {len(allz)} -> {len(dedup)} zeros -> {out}")
    print(f"first 5: {[mp.nstr(z,12) for z in dedup[:5]]}")
    print(f"last:    {mp.nstr(dedup[-1], 15)}")
    print(f"count check  n - theta/pi:  min {dmin:.3f}  max {dmax:.3f}  "
          f"largest step {jumps:.3f}  (band width {dmax-dmin:.3f}; "
          f"{'OK' if dmax - dmin < 1.5 else 'SUSPECT — possible missed pair'})")
    print(f"Riemann-von Mangoldt: N({T:.1f}) = (T/2pi)log(3T/2pi e) = {NT:.1f} "
          f"vs {len(dedup)} found")


# --------------------------------------------------------- density machinery
def tail_variance(m, gN):
    """Var of the unseen-zero sum, gamma > gN: int 2 a^2 dN, mod-3 density
    dN/dt = (1/2pi) log(3 t/(2 pi))."""
    f = lambda g: 2.0 * ((2 * m + 1) ** 2 / ((m + 0.5) ** 2 + g * g)) * \
        (math.log(Q * g / (2 * math.pi)) / (2 * math.pi))
    total, g, step = 0.0, gN, 2.0
    while g < 5e6:
        total += f(g + step / 2) * step
        g += step
        if g > 2e4:
            step = 100.0
    return total


def Phi(z):
    return 0.5 * math.erfc(-z / math.sqrt(2))


def var_law(m):
    """Derived general-q dissolution variance, q=3:
    Var_q(m) = 2(m+1/2) log(q(m+1/2)/(2 pi))."""
    arg = Q * (m + 0.5) / (2 * math.pi)
    return 2 * (m + 0.5) * math.log(arg) if arg > 1 else float('nan')


def density(ns):
    gammas = np.loadtxt(ZEROS_FILE)
    gN = gammas[-1]
    rng = np.random.default_rng(20260815)
    MS = [0, 1, 2, 3, 8, 20, 60]
    print(f"{len(gammas)} chi3 zeros (gamma_max={gN:.1f}), {ns} samples per m")
    print(f"{'m':>3} {'delta3_MC':>10} {'+/-':>8} {'sigma_MC':>9} {'Phi(1/s)':>9} "
          f"{'Var_MC':>8} {'Var_law':>8} {'law delta':>9}")
    for m in MS:
        a = (2 * m + 1) / np.sqrt((m + 0.5) ** 2 + gammas ** 2)
        tv = tail_variance(m, gN)
        var = float(np.sum(2 * a * a)) + tv
        sd = math.sqrt(var)
        hits, done, block = 0, 0, 200_000
        while done < ns:
            n = min(block, ns - done)
            th = rng.uniform(0, 2 * math.pi, size=(n, len(gammas)))
            V = (2.0 * np.cos(th) @ a) + rng.normal(0.0, math.sqrt(tv), size=n)
            hits += int(np.count_nonzero(1.0 + V > 0.0))
            done += n
        p = hits / ns
        se = math.sqrt(max(p * (1 - p), 1e-12) / ns)
        vl = var_law(m)
        law = 0.5 + 1.0 / math.sqrt(2 * math.pi * vl) if vl == vl and vl > 0 else float('nan')
        print(f"{m:>3} {p:>10.5f} {se:>8.5f} {sd:>9.4f} {Phi(1.0/sd):>9.5f} "
              f"{var:>8.2f} {vl:>8.2f} {law:>9.5f}")


# ---------------------------------------------------------------- selftest
def selftest():
    print("L values:")
    with mp.workdps(60):
        d1 = L_hur(mp.mpf(1) + mp.mpf('1e-20')) - mp.pi / (3 * mp.sqrt(3))
    print("  L(1) - pi/(3 sqrt3)  =", mp.nstr(d1, 3), " (dps 60, s=1+1e-20)")
    print("  L(0) - 1/3           =", mp.nstr(L_hur(mp.mpf(0)) - mp.mpf(1) / 3, 3))
    with mp.workdps(40):
        tau = mp.expjpi(mp.mpf(2) / 3) - mp.expjpi(mp.mpf(4) / 3)
        print("  tau(chi3) - i sqrt3  =", mp.nstr(tau - 1j * mp.sqrt(3), 3),
              "  root number tau/(i sqrt3) =", mp.nstr(tau / (1j * mp.sqrt(3)), 5))
    print("Z reality |Im Z|/|Z| (need < 1e-20):")
    worst = 0.0
    for t in (0.5, 4.0, 8.1, 25.7, 100.3, 250.2, 450.9, 699.9):
        z = Zc(t)
        r = float(abs(mp.im(z)) / abs(z))
        worst = max(worst, r)
        print(f"  t={t:<6}: {r:.2e}")
    print(f"  worst = {worst:.2e}  {'OK' if worst < 1e-20 else 'FAIL'}")
    print("Functional equation Lambda(1-s)-Lambda(s) at s=0.3+7.2i:")
    with mp.workdps(40):
        Lam = lambda s: (3 / mp.pi) ** ((s + 1) / 2) * mp.gamma((s + 1) / 2) * L_hur(s)
        s = mp.mpc(0.3, 7.2)
        print("  ", mp.nstr(Lam(1 - s) - Lam(s), 3))


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return
    cmd = args[0]
    if cmd == "selftest":
        selftest()
    elif cmd == "zeros":
        opt = {"--tmin": "0", "--tmax": "700", "--step": "0.15",
               "--out": ZEROS_FILE}
        for i in range(1, len(args), 2):
            opt[args[i]] = args[i + 1]
        find_zeros(float(opt["--tmin"]), float(opt["--tmax"]),
                   float(opt["--step"]), opt["--out"])
    elif cmd == "merge":
        assert args[1] == "--out"
        merge_zeros(args[2], args[3:])
    elif cmd == "density":
        density(int(float(args[1])) if len(args) > 1 else 4_000_000)
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
