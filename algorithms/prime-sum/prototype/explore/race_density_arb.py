#!/usr/bin/env python3
"""Fail-closed Arb enclosures for the fourteen weighted-race densities.

This is deliberately independent of ``race_density_certified.py``.  The
latter uses floating-point Simpson error estimates; this program instead
uses ball arithmetic plus theorem-backed analytic error bounds.  It prints
no density unless every check below succeeds.

Mathematical inputs (not proved by this program): GRH+LI for the limiting
random-series model, and the zero-file certificates produced by
``certify_arb.py``.  Each printed decimal ordinate is widened by 10^-20,
matching the sign-change intervals proved by that script.

The numerical certificate has four ingredients.

1. ``sigma^2`` is evaluated in Arb.  The derivative L'(s) is obtained from
   Im L(s+ih)/h.  Cauchy's estimate on |z-s|<=R and Abel summation
       |L(z,chi)| <= |z|/Re(z) <= (s+R)/(s-R)
   (the partial sums of chi_3 and chi_4 have modulus at most one) bounds the
   complete complex-step remainder.
2. The finite-product integral is evaluated by composite Gauss--Legendre
   quadrature.  The nodes are isolated and the weights enclosed in Arb.
   The quadrature remainder is bounded by Cauchy's estimate and the exact
   Gauss remainder constant.
3. The unseen-zero model error is integrated by interval subdivision.  No
   Richardson extrapolation or sampled smoothness estimate is used.
4. The infinite-t tail uses the classical bound
       |J_0(x)| <= x^(-1/2), x>0.
   This follows from Landau's theorem
   sup_{x>0} sqrt(x)|J_0(x)|=sqrt(2/pi)<1 (J. London Math. Soc. 61
   (2000), 197--215, doi:10.1112/S0024610799008352).  The weaker constant
   one avoids reliance on a numerically optimized Bessel envelope.

The only output called CERTIFIED is conditional on the mathematical inputs
listed above.  Any failed containment, positivity, or error-budget check
raises an exception before a table is printed.
"""

from __future__ import annotations

import argparse
import heapq
import math
import os
from dataclasses import dataclass

from flint import acb, arb, ctx, dirichlet_char
from mpmath import mp


HERE = os.path.dirname(os.path.abspath(__file__))
CTX_BITS = 192
NODE_N = 16
C4 = arb(18) / 1000                 # proven upper bound in the paper
TAIL_DENSITY_TARGET = arb("1e-15")
E1_ABS_TARGET = arb("2e-9")         # raw-integral enclosure width
MAX_E1_CELLS = 250_000


def hull(lo: arb, hi: arb) -> arb:
    """Ball containing [lo,hi], retaining endpoint rounding."""
    if lo.lower() > hi.upper():
        raise ArithmeticError("invalid interval hull")
    return arb((lo + hi) / 2, (hi - lo) / 2)


def inflate(x: arb, radius: arb) -> arb:
    return x + arb(0, radius.upper())


def require_finite(x: arb, label: str) -> None:
    if not x.is_finite():
        raise ArithmeticError(f"non-finite Arb value: {label}: {x}")


def sigma2_arb(q: int, m: int) -> arb:
    """Rigorous sigma_m^2 using an Arb complex step with Cauchy remainder."""
    chi = dirichlet_char(q, q - 1)
    s = arb(m + 1)
    h = arb(2) ** -60
    R = arb(1) / 4
    Ls = chi.l(acb(s)).real
    Lh = chi.l(acb(s, h))
    dL = Lh.imag / h
    # For chi_3 and chi_4, |sum_{n<=x} chi(n)| <= 1.  Abel summation gives
    # |L(z)| <= |z|/Re(z) on Re(z)>0.  Cauchy then bounds every omitted odd
    # term of Im L(s+ih)/h.
    ML = (s + R) / (s - R)
    rem = ML * h**2 / (R**3 * (1 - (h / R) ** 2))
    dL = inflate(dL, rem)
    M = arb(2 * m + 1) / 2
    out = 4 * M * ((arb(q) / arb.pi()).log() / 2
                   + ((s + 1) / 2).digamma() / 2 + dL / Ls)
    require_finite(out, "sigma2")
    if out.lower() <= 0:
        raise ArithmeticError(f"sigma2 is not positive: q={q},m={m}: {out}")
    return out


def load_zeros(filename: str) -> list[arb]:
    path = os.path.join(HERE, filename)
    with open(path, encoding="ascii") as fh:
        vals = [arb(line.strip(), "1e-20") for line in fh if line.strip()]
    if not vals:
        raise ArithmeticError(f"empty zero file: {path}")
    for a, b in zip(vals, vals[1:]):
        if not a.upper() < b.lower():
            raise ArithmeticError("zero intervals are not strictly ordered")
    return vals


def legendre(n: int, x: arb) -> arb:
    p0 = arb(1)
    if n == 0:
        return p0
    p1 = x
    for k in range(1, n):
        p0, p1 = p1, ((2 * k + 1) * x * p1 - k * p0) / (k + 1)
    return p1


def legendre_derivative(n: int, x: arb) -> arb:
    return n * (x * legendre(n, x) - legendre(n - 1, x)) / (x*x - 1)


def certified_gauss_legendre(n: int) -> list[tuple[arb, arb]]:
    """Return rigorously isolated n-point Gauss--Legendre nodes/weights."""
    mp.dps = 90
    xs, _ = mp.gauss_quadrature(n, "legendre")
    rad_mp = mp.mpf("1e-45")
    out: list[tuple[arb, arb]] = []
    for xm in xs:
        mid = mp.nstr(xm, 85)
        xb = arb(mid, "1e-45")
        left = arb(mp.nstr(xm - rad_mp, 85))
        right = arb(mp.nstr(xm + rad_mp, 85))
        pl, pr = legendre(n, left), legendre(n, right)
        opposite = (pl.upper() < 0 and pr.lower() > 0) or (
                    pl.lower() > 0 and pr.upper() < 0)
        dp = legendre_derivative(n, xb)
        if (not xb.contains(left) or not xb.contains(right)
                or not opposite or dp.contains(0)
                or not legendre(n, xb).contains(0)):
            raise ArithmeticError(f"failed to isolate Gauss node near {mid}")
        w = 2 / ((1 - xb*xb) * dp*dp)
        if w.lower() <= 0:
            raise ArithmeticError("nonpositive Gauss weight enclosure")
        out.append((xb, w))
    if len(out) != n:
        raise ArithmeticError("wrong number of Gauss node enclosures")
    for (x, _), (y, _) in zip(out, out[1:]):
        if not (-1 < x.lower() and x.upper() < y.lower() and y.upper() < 1):
            raise ArithmeticError("Gauss node balls are not strictly ordered in (-1,1)")
    weight_sum = sum((w for _, w in out), arb(0))
    if not weight_sum.contains(2):
        raise ArithmeticError(f"Gauss weights do not enclose total mass 2: {weight_sum}")
    return out


def choose_truncation(bs: list[arb], tmax: arb) -> tuple[arb, int, arb]:
    """Choose rational T and certify the Bessel-envelope tail bound."""
    bmid = [float(b.mid()) for b in bs]
    candidates: list[tuple[float, int]] = []
    logprod = 0.0
    target = float(TAIL_DENSITY_TARGET)
    for k, b in enumerate(bmid, 1):
        logprod += math.log(b)
        if k >= 16 and k % 4 == 0:
            # E2/pi = prod(b_i)^(-1/2) T^(-k/2) / (pi*k/2).
            logT = (-0.5 * logprod - math.log(math.pi * (k/2) * target)) * (2/k)
            candidates.append((math.exp(logT), k))
    _, K = min(candidates)
    # Round upward to twelve decimal places, then verify with Arb.
    Tfloat = min(x for x, k in candidates if k == K)
    T = arb(math.ceil(Tfloat * 1e12)) / arb(10**12)
    A = arb(1)
    for b in bs[:K]:
        A /= b.sqrt()
    raw_E2 = A * T ** (-arb(K)/2) / (arb(K)/2)
    density_E2 = raw_E2 / arb.pi()
    if density_E2.upper() > TAIL_DENSITY_TARGET:
        # One ulp of the chosen decimal is ample unless the float estimate
        # landed essentially on the target.
        T += arb(1) / arb(10**10)
        raw_E2 = A * T ** (-arb(K)/2) / (arb(K)/2)
        density_E2 = raw_E2 / arb.pi()
    if density_E2.upper() > TAIL_DENSITY_TARGET:
        raise ArithmeticError(f"tail target not met: {density_E2}")
    if (T * bs[-1]).upper() > 1 or T.upper() > tmax.lower():
        raise ArithmeticError("truncation exceeds the small-tail-model range")
    return T, K, raw_E2


@dataclass
class Model:
    bs: list[arb]
    VT: arb
    cb: arb
    T: arb
    e1_keep: int
    e1_tail_b2: arb

    def product(self, t: arb, count: int | None = None) -> arb:
        p = arb(1)
        for b in self.bs if count is None else self.bs[:count]:
            p *= (b * t).bessel_j(0)
        require_finite(p, "finite Bessel product")
        return p

    def main_integrand(self, t: arb) -> arb:
        p = self.product(t)
        g = (-self.VT * t*t / 2).exp()
        mid = (1 + (-self.cb * t**4).exp()) / 2
        return p * g * mid * t.sin() / t

    def e1_integrand(self, t: arb) -> arb:
        # The omitted factors all satisfy |b*t|<=1.  The Bessel product
        # expansion gives 0<J0(x)<=exp(-x^2/4) there, so replacing them by
        # exp(-t^2 sum(b^2)/4) is a rigorous (and much cheaper) majorant.
        p = abs(self.product(t, self.e1_keep))
        g = (-(self.VT/2 + self.e1_tail_b2/4) * t*t).exp()
        rad = (1 - (-self.cb * t**4).exp()) / 2
        y = p * g * rad
        # Mathematical integrand is nonnegative; intersect the natural
        # Arb enclosure with [0,+inf) without narrowing its upper endpoint.
        lo = max(arb(0), y.lower())
        return hull(lo, y.upper())


def composite_gauss(model: Model, nodes: list[tuple[arb, arb]]) -> tuple[arb, arb, int]:
    """Ball integral and a separate theorem-backed Gauss remainder."""
    A = sum((b.abs_upper() for b in model.bs), arb(0))
    # Keep exp(A*r) modest; the analytic remainder below is valid for any h/r.
    r = min(arb(1)/8, arb(4) / A)
    N = max(1, math.ceil(float(model.T.upper() / (arb(3)*r/4).lower())))
    h = model.T / N
    half = h / 2
    total = arb(0)
    for j in range(N):
        center = (arb(j) + arb(1)/2) * h
        subtotal = arb(0)
        for x, w in nodes:
            subtotal += w * model.main_integrand(center + half*x)
        total += half * subtotal

    # Uniform analytic bound on every radius-r Cauchy disk about [0,T].
    Vup = model.VT.upper()
    cbup = model.cb.upper()
    expo = A*r + Vup*r*r/2 + r
    Mbound = expo.exp() * (1 + (cbup * (model.T + r)**4).exp()) / 2
    n = len(nodes)
    Q = arb(math.factorial(n))**4 / (
        (2*n + 1) * arb(math.factorial(2*n))**2)
    err = N * Mbound * h * Q * (h/r)**(2*n)
    require_finite(err, "Gauss remainder")
    if err.upper() > arb("1e-11"):
        raise ArithmeticError(f"Gauss remainder target not met: {err} (N={N})")
    return total, err, N


def interval_e1(model: Model) -> tuple[arb, int]:
    """Enclose E1 by adaptive interval subdivision (range times width)."""
    serial = 0
    heap: list[tuple[float, int, arb, arb, arb, arb]] = []

    def add(a: arb, b: arb) -> None:
        nonlocal serial
        t = hull(a, b)
        y = model.e1_integrand(t)
        width = b - a
        clo, chi = y.lower()*width, y.upper()*width
        gap = max(0.0, float((chi-clo).upper()))
        # Store the exact same lower/upper balls that will be used in the
        # final sum.  Never update a running sum by subtracting a separately
        # rounded hull endpoint: that can underestimate the upper bound.
        heapq.heappush(heap, (-gap, serial, a, b, clo, chi))
        serial += 1

    def totals() -> tuple[arb, arb]:
        # Recompute from the active leaves.  This avoids any dependency on
        # subtractive interval bookkeeping while remaining cheap relative to
        # the Bessel range evaluations.
        lo = sum((cell[4] for cell in heap), arb(0))
        hi = sum((cell[5] for cell in heap), arb(0))
        return lo, hi

    # A modest initial grid prevents one huge interval from destroying all
    # Bessel range information.
    initial = 64
    for j in range(initial):
        add(model.T*j/initial, model.T*(j+1)/initial)

    cells = initial
    while True:
        lo_sum, hi_sum = totals()
        if (hi_sum-lo_sum).upper() <= E1_ABS_TARGET:
            return hull(lo_sum, hi_sum), cells
        if cells >= MAX_E1_CELLS:
            raise ArithmeticError(
                f"E1 subdivision did not converge: gap={hi_sum-lo_sum}, cells={cells}")
        _, _, a, b, _, _ = heapq.heappop(heap)
        mid = (a+b)/2
        add(a, mid)
        add(mid, b)
        cells += 1


def enclose(q: int, m: int, zeros: list[arb], nodes: list[tuple[arb, arb]]) -> dict:
    M = arb(2*m + 1) / 2
    bs = [4*M / (M*M + g*g).sqrt() for g in zeros]
    s2 = sigma2_arb(q, m)
    finite_var = sum((b*b/2 for b in bs), arb(0))
    VT = s2 - finite_var
    if VT.lower() <= 0:
        raise ArithmeticError(f"tail variance not positive: q={q},m={m}: {VT}")
    tmax = 1 / bs[-1]
    # sum_tail b_gamma^4 <= b_Gamma^2 * sum_tail b_gamma^2
    # and sum_tail b_gamma^2 = 2*VT.
    S4 = bs[-1]**2 * 2*VT
    cb = C4 * S4.upper()
    T, K, E2 = choose_truncation(bs, tmax)
    must_keep = sum(1 for b in bs if (b*T).upper() > 1)
    e1_keep = min(len(bs), max(100, must_keep))
    if e1_keep < len(bs) and (bs[e1_keep]*T).upper() > 1:
        raise ArithmeticError("omitted E1 Bessel factor can leave |x|<=1")
    e1_tail_b2 = sum((b*b for b in bs[e1_keep:]), arb(0))
    model = Model(bs, VT, cb, T, e1_keep, e1_tail_b2)
    I, Egl, ncells = composite_gauss(model, nodes)
    E1, e1cells = interval_e1(model)
    raw_radius = E1.upper() + E2.upper() + Egl.upper() + I.rad()
    center = arb(1)/2 + I.mid()/arb.pi()
    density_radius = raw_radius / arb.pi()
    density = inflate(center, density_radius)
    require_finite(density, "density")
    if density.lower() < 0 or density.upper() > 1:
        raise ArithmeticError(f"invalid probability enclosure: {density}")
    return dict(q=q, m=m, sigma2=s2, VT=VT, T=T, K=K, E1=E1,
                E2=E2, Egl=Egl, gauss_cells=ncells, e1_cells=e1cells,
                density=density)


CASES = {
    4: ("chi4_zeros.txt", [0, 1, 2, 3, 8, 20, 100]),
    3: ("chi3_zeros.txt", [0, 1, 2, 3, 8, 20, 60]),
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--q", type=int, choices=[3, 4])
    parser.add_argument("--m", type=int)
    args = parser.parse_args()
    if args.m is not None and args.q is None:
        parser.error("--m requires --q")

    ctx.prec = CTX_BITS
    c4_exact = -(arb(1).bessel_j(0)).log() - arb(1)/4
    if not c4_exact.upper() < C4.lower():
        raise ArithmeticError(f"the rounded quartic constant is not an upper bound: {c4_exact}")
    nodes = certified_gauss_legendre(NODE_N)
    selected = [args.q] if args.q else [4, 3]
    results = []
    for q in selected:
        filename, ms = CASES[q]
        if args.m is not None:
            if args.m not in ms:
                parser.error(f"m={args.m} is not one of the tabulated q={q} cases")
            ms = [args.m]
        zeros = load_zeros(filename)
        for m in ms:
            print(f"working q={q}, m={m} ...", flush=True)
            results.append(enclose(q, m, zeros, nodes))

    print("\nCERTIFIED conditional density enclosures")
    print(" q   m       lower bound             upper bound        width       E1 cells")

    def fixed12(k: int) -> str:
        sign = "-" if k < 0 else ""
        whole, frac = divmod(abs(k), 10**12)
        return f"{sign}{whole}.{frac:012d}"

    def directed12(x: arb, lower: bool) -> str:
        scale = arb(10**12)
        rounded = ((x.lower() * scale).floor() if lower
                   else (x.upper() * scale).ceil())
        k = rounded.unique_fmpz()
        if k is None:
            raise ArithmeticError(f"directed decimal rounding was not unique: {rounded}")
        out = fixed12(int(k))
        parsed = arb(out)
        if lower:
            if (parsed - x.lower()).upper() > 0:
                raise ArithmeticError(f"printed lower endpoint is not outward: {out}, {x}")
        elif (x.upper() - parsed).upper() > 0:
            raise ArithmeticError(f"printed upper endpoint is not outward: {out}, {x}")
        return out

    for r in results:
        d = r["density"]
        width = d.upper()-d.lower()
        print(f" {r['q']} {r['m']:3d}  {directed12(d, True)}  "
              f"{directed12(d, False)}  {float(width.upper()):.2e}  "
              f"{r['e1_cells']:7d}")


if __name__ == "__main__":
    main()
