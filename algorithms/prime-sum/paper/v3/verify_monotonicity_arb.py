#!/usr/bin/env python3
"""Ball-arithmetic certificate for the explicit q=3,4 monotonicity ranges.

This upgrades item [4] of ``verify_monotonicity.py``.  All values which enter
MAIN > TAIL are outward-rounded ``python-flint`` balls:

* sigma^2, D and S4 use the completed-L closed forms.  The two logarithmic
  derivatives of L are evaluated by a finite von-Mangoldt series with an
  explicit absolute integral tail.
* every stored ordinate is the certified ball ``decimal +/- 1e-20``;
* sup |J0| on every argument cell is the maximum of ball evaluations at the
  two endpoints and at the first enclosed J1 zero.  The J1 zeros and their J0
  values are themselves isolated by interval Newton iteration;
* products, cell integrals, the analytic t>=64 remainder, erf, exponentials,
  and the M=300 analytic bridge are all evaluated as balls.

The Bessel-zero enumeration uses the standard indexing/interlacing theorem
for positive Bessel zeros (DLMF 10.21(i)); interval Newton proves that every
indexed seed used here contains a unique J1 zero.  The script aborts on any
failed isolation, nonpositive factor, overlapping MAIN/TAIL balls, or uncovered
weight interval.

Run from the repository root with the Python 3.12 research environment:

    .venv-research/Scripts/python.exe \
        algorithms/prime-sum/paper/v3/verify_monotonicity_arb.py
"""

from __future__ import annotations

import argparse
import math
import os
from dataclasses import dataclass

import numpy as np
from scipy.special import jn_zeros
from flint import acb, arb, ctx


ctx.dps = 40
HERE = os.path.dirname(os.path.abspath(__file__))
EXPLORE = os.path.normpath(os.path.join(HERE, "..", "..", "prototype", "explore"))
PI = arb.pi()
SERIES_N = 128


def A(x: float | int | str) -> arb:
    """An exact decimal ball for a scalar used as an interval endpoint."""
    return arb(str(x))


def lower_float(x: arb) -> float:
    y = float(x.lower())
    while A(y) > x.lower():
        y = math.nextafter(y, -math.inf)
    if not A(y) <= x.lower():
        raise RuntimeError("failed to direct a lower endpoint")
    return y


def upper_float(x: arb) -> float:
    y = float(x.upper())
    while A(y) < x.upper():
        y = math.nextafter(y, math.inf)
    if not A(y) >= x.upper():
        raise RuntimeError("failed to direct an upper endpoint")
    return y


def upper_abs_float(x: arb) -> float:
    return upper_float(abs(x))


def show_ball(x: arb, digits: int = 12) -> str:
    return str(x).replace("[", "[") if digits == 12 else str(x)


@dataclass(frozen=True)
class ZeroData:
    centers: np.ndarray
    balls: tuple[arb, ...]


def load_zeros(q: int) -> ZeroData:
    name = {4: "chi4_zeros.txt", 3: "chi3_zeros.txt"}[q]
    path = os.path.join(EXPLORE, name)
    raw = [line.strip() for line in open(path, encoding="utf-8") if line.strip()]
    balls = tuple(arb(f"{s} +/- 1e-20") for s in raw)
    centers = np.array([float(s) for s in raw], dtype=float)
    if not np.all(np.diff(centers) > 0):
        raise RuntimeError(f"{name}: ordinates are not strictly increasing")
    for x, y in zip(balls, balls[1:]):
        if x.overlaps(y):
            raise RuntimeError(f"{name}: certified ordinate balls overlap")
    return ZeroData(centers, balls)


def prime_power_base(n: int) -> int | None:
    """Return p if n is a positive power of the prime p, else None."""
    for p in range(2, int(math.isqrt(n)) + 2):
        if n % p:
            continue
        # p must itself be prime.
        if any(p % d == 0 for d in range(2, int(math.isqrt(p)) + 1)):
            return None
        k = n
        while k % p == 0:
            k //= p
        return p if k == 1 else None
    return n  # n is prime


LAMBDA: list[arb] = [arb(0)] * (SERIES_N + 1)
LOGN: list[arb] = [arb(0)] * (SERIES_N + 1)
for _n in range(2, SERIES_N + 1):
    LOGN[_n] = arb(_n).log()
    _p = prime_power_base(_n)
    if _p is not None:
        LAMBDA[_n] = arb(_p).log()


def chi(q: int, n: int) -> int:
    r = n % q
    if q == 4:
        return 1 if r == 1 else (-1 if r == 3 else 0)
    return 1 if r == 1 else (-1 if r == 2 else 0)


def log_power_tail(s: arb, power: int) -> arb:
    """Upper bound sum_{n>N} log(n)^power n^-s, power 1 or 2."""
    N = arb(SERIES_N)
    u = s - 1
    ln = N.log()
    pref = ((1 - s) * ln).exp()
    if power == 1:
        val = pref * (ln / u + 1 / (u * u))
    elif power == 2:
        val = pref * (ln * ln / u + 2 * ln / (u * u) + 2 / (u * u * u))
    else:
        raise ValueError(power)
    return val.upper()


def sds(M_value: float, q: int) -> tuple[arb, arb, arb]:
    """Certified balls for (sigma^2, D, S4) at the exact endpoint M."""
    M = A(M_value)
    s = M + A("0.5")
    x = (s + 1) / 2
    ll = arb(0)
    ll1 = arb(0)
    for n in range(2, SERIES_N + 1):
        c = chi(q, n)
        if c == 0 or LAMBDA[n].is_zero():
            continue
        ns = (-s * LOGN[n]).exp()
        ll -= c * LAMBDA[n] * ns
        ll1 += c * LAMBDA[n] * LOGN[n] * ns
    ll += arb(0, log_power_tail(s, 1))
    ll1 += arb(0, log_power_tail(s, 2))
    trigamma = acb(2).zeta(acb(x)).real
    d1 = A("0.5") * (arb(q) / PI).log() + A("0.5") * x.digamma() + ll
    d2 = A("0.25") * trigamma + ll1
    sigma2 = 4 * M * d1
    D = 4 * d1 + 4 * M * d2
    S4 = 16 * sigma2 - 64 * M * M * d2
    if not (sigma2.lower() > 0 and D.lower() > 0 and S4.lower() > 0):
        raise RuntimeError(f"nonpositive SDS ball at q={q}, M={M_value}")
    return sigma2, D, S4


@dataclass(frozen=True)
class BesselExtrema:
    roots_lo: np.ndarray
    roots_hi: np.ndarray
    maxima_hi: np.ndarray


def isolate_j1_extrema(count: int = 90) -> BesselExtrema:
    seeds = jn_zeros(1, count)
    root_balls: list[arb] = []
    for k, seed in enumerate(seeds, 1):
        I = arb(float(seed), 1.0e-6)
        proved_unique = False
        for _ in range(4):
            mid = I.mid()
            fmid = mid.bessel_j(1)
            deriv = I.bessel_j(0) - I.bessel_j(1) / I
            if deriv.contains(0):
                raise RuntimeError(f"J1 root {k}: derivative ball contains zero")
            newton = mid - fmid / deriv
            if not I.overlaps(newton):
                raise RuntimeError(f"J1 root {k}: interval Newton image is disjoint")
            if I.contains_interior(newton):
                proved_unique = True
            I = I.intersection(newton)
            # One strict inclusion proves existence and uniqueness.  At the
            # working precision a later refinement can equal its parent ball,
            # so strict inclusion must not be required on every iteration.
            if proved_unique:
                break
        if not proved_unique:
            raise RuntimeError(f"J1 root {k}: interval Newton inclusion failed")
        # The classical bound k*pi < j_{1,k} < (k+1/4)*pi verifies indexing.
        if not (I.lower() > k * PI and I.upper() < (A(k) + A("0.25")) * PI):
            raise RuntimeError(f"J1 root {k}: failed standard indexing bracket")
        root_balls.append(I)
    for left, right in zip(root_balls, root_balls[1:]):
        if left.overlaps(right):
            raise RuntimeError("J1 root isolating intervals overlap")
    roots_lo = np.array([lower_float(r) for r in root_balls])
    roots_hi = np.array([upper_float(r) for r in root_balls])
    extrema_abs = [abs(r.bessel_j(0)) for r in root_balls]
    maxima_hi = np.array([upper_abs_float(v) for v in extrema_abs])
    if roots_hi[-1] <= 256.1:
        raise RuntimeError("not enough certified J1 extrema for t<=64")
    if not all(left.lower() > right.upper()
               for left, right in zip(extrema_abs, extrema_abs[1:])):
        raise RuntimeError("certified successive |J0| extrema are not decreasing")
    print(f"isolated {count} J1 extrema through {roots_hi[-1]:.6f}; "
          f"widest root enclosure < {max(upper_float(r)-lower_float(r) for r in root_balls):.2e}")
    return BesselExtrema(roots_lo, roots_hi, maxima_hi)


def point_j0_upper(x: float) -> float:
    return min(1.0, upper_abs_float(A(x).bessel_j(0)))


def bessel_sup(lo: np.ndarray, hi: np.ndarray, ext: BesselExtrema) -> np.ndarray:
    """Certified componentwise sup |J0| on the closed intervals [lo,hi]."""
    out = np.empty_like(lo)
    idx = np.searchsorted(ext.roots_hi, lo, side="left")
    for i, (a, b, k) in enumerate(zip(lo, hi, idx)):
        if not (0 < a <= b):
            raise RuntimeError(f"invalid Bessel argument interval [{a},{b}]")
        v = max(point_j0_upper(a), point_j0_upper(b))
        if k < len(ext.roots_lo) and ext.roots_lo[k] <= b:
            v = max(v, ext.maxima_hi[k])
        out[i] = min(1.0, v)
    return out


def nplus(t: arb, q: int) -> arb:
    return A("0.5") * t * (arb(q) * (t + 2) / (2 * PI)).log() + A("0.57") * t


def main_lower(Dmin: arb, sigma2_max: arb, S4_max: arb) -> arb:
    beta = sigma2_max / 2 + S4_max / 1088
    a = A("0.125")
    rootb = beta.sqrt()
    integral = PI.sqrt() / (4 * beta * rootb) * (a * rootb).erf() \
        - a / (2 * beta) * (-beta * a * a).exp()
    return A("0.9973") / PI * (Dmin / 2) * integral


def certified_amplitudes(Ma: float, Mb: float,
                         data: ZeroData) -> tuple[np.ndarray, np.ndarray]:
    selected = [i for i, g in enumerate(data.balls) if g.upper() <= 2 * A(Ma)]
    if len(selected) < 12:
        return np.array([]), np.array([])
    alo: list[float] = []
    ahi: list[float] = []
    Maa, Mbb = A(Ma), A(Mb)
    for i in selected:
        g = data.balls[i]
        lo = 2 * Maa / (Maa * Maa + g * g).sqrt()
        hi = 2 * Mbb / (Mbb * Mbb + g * g).sqrt()
        alo.append(lower_float(lo))
        ahi.append(upper_float(hi))
    return np.array(alo), np.array(ahi)


def tail_upper(q: int, Ma: float, Mb: float, data: ZeroData,
               Dmax: arb, ext: BesselExtrema) -> arb:
    a_lo, a_hi = certified_amplitudes(Ma, Mb, data)
    n = len(a_lo)
    if n < 12:
        raise RuntimeError(f"only {n} certified zeros below 2Ma at Ma={Ma}")
    cells = [0.6]
    while cells[-1] < 16.0:
        cells.append(min(cells[-1] * 1.05, 16.0))
    while cells[-1] < 64.0:
        cells.append(min(cells[-1] * 1.10, 64.0))
    total = arb(0)
    for ta, tb in zip(cells[:-1], cells[1:]):
        # Form the argument endpoints in ball arithmetic, then direct their
        # decimal-float representations outwards.  The floats only index the
        # certified extrema and are converted back to exact decimals before
        # every special-function evaluation.
        lo = np.array([lower_float(2 * A(value) * A(ta)) for value in a_lo])
        hi = np.array([upper_float(2 * A(value) * A(tb)) for value in a_hi])
        b = bessel_sup(lo, hi, ext)
        if np.any(b <= 0) or np.any(b > 1):
            raise RuntimeError("invalid certified Bessel supremum")
        # The worst differentiated index removes the smallest upper factor.
        logprod = arb(0)
        for value in b:
            logprod += A(value).log()
        logprod -= A(float(np.min(b))).log()
        product = logprod.exp()
        G2 = A(Mb) * (4 * A(tb) * A(tb) - 1).sqrt()
        if G2.upper() < data.balls[-1].lower():
            # Count every certified ball that could lie below the threshold.
            count = sum(1 for g in data.balls if g.lower() <= G2.upper())
            count_bound = arb(count)
        else:
            count_bound = nplus(arb(G2.upper()), q)
        At = Dmax * A(tb) * A(tb) / 2 + 4 * A(tb) * count_bound / A(Ma)
        trig = arb(1) if ta <= 1 else 1 / A(ta)
        total += At * trig * product * (A(tb) - A(ta))

    # Analytic t>=64 remainder from Lemma tailexp.
    kappas = np.sort(np.array([
        upper_float(8 / PI / (2 * A(value)).sqrt()) for value in a_lo
    ]))
    nn = min(n - 1, 62)
    if nn < 7:
        raise RuntimeError("too few factors for analytic remainder")
    logK = arb(0)
    for value in kappas[1:nn + 1]:
        logK += A(value).log()
    pw = A(nn) / 2 - 1
    T = arb(64)
    l0 = (arb(q) * (2 * A(Mb) + 2) / (2 * PI)).log() + A("1.14")
    i1 = T ** (1 - pw) / (pw - 1)
    i2 = T ** (1 - pw) * (T.log() * (pw - 1) + 1) / ((pw - 1) ** 2)
    rem = logK.exp() * (Dmax * i1 / 2 + 4 * A(Mb) / A(Ma) * (l0 * i1 + i2))
    return (total + rem) / PI


def interval_bounds(Ma: float, Mb: float, q: int,
                    data: ZeroData, ext: BesselExtrema) -> tuple[arb, arb]:
    s2a, Da, _ = sds(Ma, q)
    s2b, Db, S4b = sds(Mb, q)
    ratio_lo = (A(Ma) / A(Mb)) ** 3
    ratio_hi = (A(Mb) / A(Ma)) ** 3
    Dmin = max(Da.lower(), Db.lower()) * ratio_lo
    Dmax = min(Da.upper(), Db.upper()) * ratio_hi
    main = main_lower(Dmin, s2b.upper(), S4b.upper())
    tail = tail_upper(q, Ma, Mb, data, Dmax, ext)
    return main, tail


def analytic_bridge(q: int) -> tuple[arb, arb]:
    """Ball evaluation of the displayed analytic MAIN/TAIL formulas at M=300."""
    M = arb(300)
    ell = (arb(q) * M / (2 * PI)).log()
    Y1, Y2 = M / arb(3).sqrt(), 2 * M / arb(3).sqrt()
    n1 = Y1 * ((arb(q) * Y1 / (2 * PI)).log() - 2) / 16 - A("0.5")
    n2 = Y2 * ((arb(q) * Y2 / (2 * PI)).log() - 2) / 16 - A("0.5")
    Dplus = 2 * ell + 2 + 8 / M
    Dminus = 2 * ell + 2 - 8 / M
    ell0 = (arb(q) * (2 * M + 2) / (2 * PI)).log() + A("1.14")
    first = (64 * Dplus + 512 * ell0 + 1165) / (A("0.447") * PI) \
        * (A("0.447") / A("0.733")) ** n1 * A("0.733") ** n2
    c3 = 4 * arb(5).sqrt().sqrt() / PI
    p = A("3.5")
    T = arb(16)
    I1 = T ** (1 - p) / (p - 1)
    I2 = T ** (1 - p) * (T.log() * (p - 1) + 1) / ((p - 1) ** 2)
    second = c3 ** 9 / PI * (Dplus * I1 / 2 + 4 * (ell0 * I1 + I2)) \
        * A("0.733") ** (n2 - 10)
    sigma2_max = 2 * M * ell + A("3.1")
    S4max = 32 * M * (ell - 1) + 100
    main = main_lower(Dminus, sigma2_max, S4max)
    return main, first + second


def scan(q: int, start: float, stop: float, ratio: float,
         data: ZeroData, ext: BesselExtrema) -> None:
    grid = [start]
    while grid[-1] < stop:
        grid.append(min(grid[-1] * ratio, stop))
    worst = math.inf
    worst_row: tuple[float, float, arb, arb] | None = None
    for index, (Ma, Mb) in enumerate(zip(grid[:-1], grid[1:]), 1):
        main, tail = interval_bounds(Ma, Mb, q, data, ext)
        if not (main.lower() > tail.upper()):
            raise RuntimeError(
                f"q={q} failed/overlapped on [{Ma},{Mb}]: MAIN={main}, TAIL={tail}"
            )
        margin = 1.0 - upper_float(tail) / lower_float(main)
        if margin < worst:
            worst = margin
            worst_row = (Ma, Mb, main, tail)
        if index % 20 == 0 or index == len(grid) - 1:
            print(f"  q={q}: certified {index:3d}/{len(grid)-1} intervals through M={Mb:.6f}")
    assert worst_row is not None
    Ma, Mb, main, tail = worst_row
    print(f"q={q}: ALL {len(grid)-1} intervals certified on [{start},{stop}]")
    print(f"  worst certified relative margin {worst:.6f} on [{Ma:.9f},{Mb:.9f}]")
    print(f"  MAIN={main}")
    print(f"  TAIL={tail}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ratio", type=float, default=1.02)
    parser.add_argument("--stop", type=float, default=300.0)
    parser.add_argument("--only", type=int, choices=(3, 4))
    args = parser.parse_args()
    ext = isolate_j1_extrema()
    starts = {4: 17.32, 3: 19.12}
    for q in ((args.only,) if args.only else (4, 3)):
        data = load_zeros(q)
        print(f"q={q}: loaded {len(data.balls)} certified ordinate balls")
        scan(q, starts[q], args.stop, args.ratio, data, ext)
        main300, tail300 = analytic_bridge(q)
        if not (main300.lower() > tail300.upper()):
            raise RuntimeError(f"q={q}: analytic M=300 bridge failed: {main300}, {tail300}")
        print(f"q={q}: analytic M=300 bridge certified; "
              f"TAIL/MAIN <= {upper_float(tail300)/lower_float(main300):.6e}")
    print("PASS: finite thresholds and analytic bridge certified in ball arithmetic")


if __name__ == "__main__":
    main()
