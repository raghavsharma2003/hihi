#!/usr/bin/env python3
"""
certify_arb.py -- rigorous ball-arithmetic certification for the weighted-races paper.

Requires: python-flint >= 0.9 (pip install python-flint), which wraps FLINT/Arb.
Every quantity below is computed as a BALL (midpoint +/- radius) with rigorous
enclosure semantics: the true value is guaranteed to lie in the printed interval,
up to the correctness of FLINT/Arb itself and of the mathematical reductions
documented inline (each reduction is elementary and stated where used).

What this script certifies (see the final summary it prints):

  [A] The constants
        C(chi_4) = (1/4) psi'(3/4) + (log L)''(1/2, chi_4)
        C(chi_3) = (1/4) psi'(3/4) + (log L)''(1/2, chi_3)
      as balls.  psi'(3/4) is computed two independent ways (Arb's polygamma,
      and pi^2 - 8*Catalan) and the balls are checked to overlap.
      (log L)''(1/2) is computed from L(1/2), L'(1/2), L''(1/2), each obtained
      by a Cauchy integral over a circle |s - 1/2| = r using acb_calc rigorous
      integration (flint.acb.integral).  L(s, chi) is ENTIRE for these
      non-principal characters, so the integrand is holomorphic and the
      Cauchy representation L^(k)(1/2) = k!/(2 pi r^k) *
      int_0^{2pi} L(1/2 + r e^{i th}) e^{-i k th} d th is an identity.
      Two radii (r = 1/4 and r = 3/10) are used and the balls must agree.
      (The radii keep the contour away from s = 1, where Arb's internal
      Hurwitz-zeta representation of L makes ball evaluation blow up.)
      Additionally the ball for L(1/2, chi) is REQUIRED to be certified
      positive (machine check of non-vanishing central value at q = 3, 4),
      and the enclosure radius of C is required to be < 1e-25 so that the
      paper-consistency overlap test cannot pass vacuously with a wide ball.

  [B] The variances sigma_m^2 = 4 M (log Lambda)'(m+1), M = m + 1/2, for
      m in {0, 1, 2, 3, 8, 20, 100} and both moduli q = 4, 3, via
        (log Lambda)'(s) = (1/2) log(q/pi) + (1/2) psi((s+1)/2) + (L'/L)(s),
      where L'(m+1) comes from the same rigorous Cauchy integral and psi from
      Arb's digamma.  Independent cross-check: for m >= 1 the Dirichlet series
        -(L'/L)(s) = sum_{n>=2} Lambda(n) chi(n) n^{-s}
      is summed over prime powers n <= N in ball arithmetic with the rigorous
      tail bound
        |sum_{n>N} Lambda(n) chi(n) n^{-s}|
           <= sum_{n>N} log(n) n^{-sigma}
           <= int_N^inf log(x) x^{-sigma} dx
            = N^{1-sigma} ( log(N)/(sigma-1) + 1/(sigma-1)^2 ),
      valid because log(x) x^{-sigma} is decreasing for x >= e^{1/sigma} and
      N >= 2 > e^{1/2}; the tail is added to the ball as an extra radius.
      The two enclosures must overlap, and every sigma_m^2 enclosure radius
      is required to be < 5e-28 (so consistency tests cannot pass vacuously).
      NOTE: the identity sigma_m^2 = 4M (log Lambda)'(m+1) itself is proved in
      the paper UNDER GRH(chi); what is certified here unconditionally is the
      right-hand side, i.e. the closed-form evaluation.

  [C] Zero localization: for the first K listed ordinates gamma_j of each
      character, the Hardy Z-function (acb_dirichlet_hardy_z; real-valued on
      the real line for these real primitive characters) is evaluated at
      gamma_j - eps and gamma_j + eps, eps = 1e-20, and the two balls are
      required to have certified opposite signs.  Since Z is continuous and
      real, a sign change PROVES a zero of Z -- i.e. a zero of L on the
      critical line -- in (gamma_j - eps, gamma_j + eps).

  [D] Completeness ("no zero is missing"), by a rigorous winding-number /
      argument-principle count.  Let R = (-1/2, 3/2) x (-1/2, T) with T
      chosen strictly above gamma_K (between gamma_K and gamma_{K+1} when
      gamma_{K+1} is stored, or gamma_K + --top-offset for the whole list;
      the certified contour evaluation itself proves that the latter top edge
      is zero-free).  The bottom edge sits
      at Im s = -1/2 rather than 0 to keep the contour away from s = 1; see
      winding_number below.  The boundary of R is covered
      by finitely many closed segments; for each segment an acb ball
      containing it is evaluated under L, and the output ball is required not
      to contain 0.  This proves L != 0 on the whole contour, and, since a
      disk not containing 0 subtends an angle 2*arcsin(rad/|center|) < pi at
      the origin, the continuous change of arg L along each segment lies in
      (-pi, pi) and therefore EQUALS the principal Arg of the ratio of the
      endpoint values.  Summing these principal-Arg balls and dividing by
      2 pi gives a ball around the winding number, which must contain a
      unique integer n; by the argument principle n is the number of zeros of
      L inside R counted with multiplicity.  If n = K, then combined with [C]
      (K disjoint sign-change intervals inside R) each interval contains
      EXACTLY ONE zero, that zero is SIMPLE, and R contains no other zeros.
      By classical theory (Euler product for Re s > 1, non-vanishing of
      L(1 + it), and the functional equation) every nontrivial zero has
      0 < Re s < 1, and the trivial zeros of these odd characters are at
      s = -1, -3, ...; hence R captures ALL zeros of L(s, chi) with
      0 < Im s < T, and the count is a genuine completeness proof for the
      list up to T (this classical input is NOT re-proved here).

  What is NOT certified by this script: everything downstream of these
  constants (the Gil-Pelaez quadrature of the density script remains
  double-precision with budgeted, not certified, quadrature error), the
  GRH-conditional identifications (zero-sum = closed form), and ordinates
  beyond the first K (default 50) of each list.

Exit status 0 iff every certification above succeeded.

Usage:
    python3 certify_arb.py            # default: K = 50 zeros per character
    python3 certify_arb.py --K 100    # more zeros (winding contour grows)
    python3 certify_arb.py --K 0      # certify and count the whole stored list
    python3 certify_arb.py --skip-winding   # skip the completeness count
"""

import argparse
import math
import os
import sys
import time

try:
    from flint import arb, acb, ctx, dirichlet_char
except ImportError:
    sys.stderr.write("python-flint is required: pip install python-flint\n")
    sys.exit(2)

HERE = os.path.dirname(os.path.abspath(__file__))

FAILURES = []


def fail(msg):
    FAILURES.append(msg)
    print("    *** CERTIFICATION FAILURE: %s" % msg)


def show(label, ball, digits=30):
    print("    %-34s %s" % (label, ball.str(digits, radius=True)))


def contains_zero(b):
    """True iff the acb/arb ball b contains 0 (exact predicate on the ball)."""
    if isinstance(b, acb):
        return b.contains(acb(0))
    return b.contains(arb(0))


def certified_sign(x):
    """+1 / -1 if the arb ball x is certified positive/negative, else 0."""
    if x > 0:
        return 1
    if x < 0:
        return -1
    return 0


def paper_decimal_ball(s):
    """The paper prints truncated decimals; read the string as a ball wide
    enough (+/- 2 units in the last printed decimal) to cover truncation
    and rounding of the true value."""
    ndec = len(s.split(".")[1]) if "." in s else 0
    return arb(s) + arb(0).union(arb(2) * arb(10) ** (-ndec)).union(-arb(2) * arb(10) ** (-ndec))


# ----------------------------------------------------------------------------
# [A] Cauchy-integral derivatives of L at s = 1/2, and the constant C
# ----------------------------------------------------------------------------

def l_derivative(chi, s0, k, radius):
    """Rigorous ball for L^(k)(s0, chi) via the Cauchy integral over
    |s - s0| = radius.  Valid because L(s, chi) is entire (chi non-principal
    primitive), so the integrand th |-> L(s0 + r e^{i th}) e^{-i k th} is
    holomorphic in th; the 'analytic' flag of acb_calc may be ignored for
    functions holomorphic everywhere (cf. python-flint acb.integral docs)."""
    r = arb(radius)

    def integrand(th, analytic):
        z = (acb(0, 1) * th).exp()          # e^{i th}, entire
        return chi.l(s0 + acb(r) * z) * z ** (-k)

    I = acb.integral(integrand, 0, 2 * arb.pi())
    return I * arb(math.factorial(k)) / (2 * arb.pi() * r ** k)


def log_l_second_derivative(chi, s0, radius):
    """Ball for (log L)''(s0) = L''/L - (L'/L)^2, real part taken at the end
    (the true value is real for real chi at real s0; the real part of a valid
    complex enclosure is a valid real enclosure)."""
    L0 = l_derivative(chi, s0, 0, radius)
    L1 = l_derivative(chi, s0, 1, radius)
    L2 = l_derivative(chi, s0, 2, radius)
    val = L2 / L0 - (L1 / L0) ** 2
    return val.real, L0, L1, L2


def part_A(chars, paper_refs):
    print("\n[A] The constant C = (1/4) psi'(3/4) + (log L)''(1/2, chi)")
    t0 = time.time()

    # psi'(3/4) two ways
    psi1_a = acb("0.75").polygamma(1).real          # Arb polygamma
    psi1_b = arb.pi() ** 2 - 8 * arb.const_catalan()  # closed form pi^2 - 8G
    show("psi'(3/4) [polygamma]", psi1_a)
    show("psi'(3/4) [pi^2 - 8 Catalan]", psi1_b)
    if not psi1_a.overlaps(psi1_b):
        fail("psi'(3/4): the two computations do not overlap")

    results = {}
    for name, chi in chars.items():
        half = acb(1) / 2
        # Two independent contour radii; both must agree.  NOTE: the radii
        # must keep the circle away from s = 1 (and s = 0): Arb evaluates
        # L(s, chi) through Hurwitz zeta functions whose poles at s = 1
        # cancel only exactly at s = 1, so ball evaluation ON a contour
        # through s = 1 returns [+/- inf].  Radii 1/4 and 3/10 stay clear.
        d2_a, L0, L1, L2 = log_l_second_derivative(chi, half, arb(1) / 4)
        d2_b, _, _, _ = log_l_second_derivative(chi, half, arb(3) / 10)
        if not d2_a.overlaps(d2_b):
            fail("(log L)''(1/2, %s): contour radii 1/4 and 3/10 disagree" % name)
        d2 = d2_a.intersection(d2_b) if hasattr(d2_a, "intersection") else d2_a
        C = psi1_a / 4 + d2
        print("  %s:" % name)
        show("L(1/2)", L0.real)
        show("L'(1/2)", L1.real)
        show("L''(1/2)", L2.real)
        show("(log L)''(1/2)", d2)
        show("C", C)
        # machine certification of the non-vanishing (indeed positive)
        # central value: the arb comparison is True only when provable
        if L0.real > 0:
            print("    L(1/2) certified positive (machine NCZ check): OK")
        else:
            fail("L(1/2, %s) is not certified positive" % name)
        # guard against vacuous overlap tests (a wide ball overlaps anything)
        if not float(C.rad()) < 1e-25:
            fail("C(%s) enclosure too wide (rad %.2e >= 1e-25)"
                 % (name, float(C.rad())))
        results[name] = C
        ref = paper_refs.get(name)
        if ref is not None:
            ref_ball = paper_decimal_ball(ref)
            if not C.overlaps(ref_ball):
                fail("C(%s) ball is inconsistent with the paper's value %s" % (name, ref))
            else:
                print("    consistent with paper value %s (+/- 2 final-digit ulps): OK" % ref)
    print("  [A] done in %.2fs" % (time.time() - t0))
    return results


# ----------------------------------------------------------------------------
# [B] sigma_m^2 = 4 M (log Lambda)'(m+1)
# ----------------------------------------------------------------------------

def sieve_primes(N):
    is_c = bytearray([0]) * 0
    is_comp = bytearray(N + 1)
    ps = []
    for p in range(2, N + 1):
        if not is_comp[p]:
            ps.append(p)
            for q in range(p * p, N + 1, p):
                is_comp[q] = 1
    return ps


def lprime_over_l_series(chi_value, s_int, N, primes):
    """Ball for (L'/L)(s) = -sum_{n>=2} Lambda(n) chi(n) n^{-s}, summing prime
    powers n = p^k <= N exactly in ball arithmetic and bounding the tail by
    int_N^inf log(x) x^{-s} dx = N^{1-s} (log N/(s-1) + 1/(s-1)^2).
    Requires integer s >= 2 (so that log(x) x^{-s} decreases for x >= 2).
    chi_value(n) must return the integer character value for odd n."""
    assert s_int >= 2 and N >= 2
    total = arb(0)
    for p in primes:
        cv = chi_value(p)
        if cv == 0:
            continue
        logp = arb(p).log()
        pk = p
        k = 1
        while pk <= N:
            term = logp * (cv ** k) / arb(pk) ** s_int
            total += term
            pk *= p
            k += 1
    # rigorous tail bound as an arb, blown into a symmetric error ball
    Nb = arb(N)
    sm1 = arb(s_int - 1)
    tail = Nb ** (1 - s_int) * (Nb.log() / sm1 + 1 / sm1 ** 2)
    err = tail.union(-tail)   # ball containing [-tail, tail]
    return -(total + err)     # (L'/L)(s) = -(sum + tail-error)


def part_B(chars, m_list, paper_sigma, primes_by_N):
    print("\n[B] Variances sigma_m^2 = 4M (log Lambda)'(m+1)   (M = m + 1/2)")
    t0 = time.time()
    results = {}
    for name, (chi, q) in chars.items():
        print("  %s (q = %d):" % (name, q))
        for m in m_list:
            s0 = acb(m + 1)
            M = arb(2 * m + 1) / 2
            L0 = l_derivative(chi, s0, 0, arb(1) / 2)
            L1 = l_derivative(chi, s0, 1, arb(1) / 2)
            lpl_cauchy = (L1 / L0).real
            psi_term = (arb(m + 2) / 2).digamma() / 2
            log_term = (arb(q) / arb.pi()).log() / 2
            sigma2 = 4 * M * (log_term + psi_term + lpl_cauchy)
            show("sigma_%d^2" % m, sigma2)
            # guard against vacuous overlap tests
            if not float(sigma2.rad()) < 5e-28:
                fail("sigma_%d^2(%s) enclosure too wide (rad %.2e >= 5e-28)"
                     % (m, name, float(sigma2.rad())))
            results[(name, m)] = sigma2

            # independent series cross-check for m >= 1
            if m >= 1:
                if m == 1:
                    N = 10 ** 6
                elif m == 2:
                    N = 10 ** 5
                elif m == 3:
                    N = 10 ** 4
                else:
                    N = 1000
                primes = primes_by_N[N]
                if q == 4:
                    chi_val = lambda p: 0 if p % 2 == 0 else (1 if p % 4 == 1 else -1)
                else:
                    chi_val = lambda p: 0 if p % 3 == 0 else (1 if p % 3 == 1 else -1)
                lpl_series = lprime_over_l_series(chi_val, m + 1, N, primes)
                if not lpl_cauchy.overlaps(lpl_series):
                    fail("(L'/L)(%d, %s): Cauchy vs series enclosures disjoint" % (m + 1, name))
                else:
                    print("      series cross-check (N=%d) overlaps: rad %.2e vs %.2e"
                          % (N, float(lpl_cauchy.rad()), float(lpl_series.rad())))

            ref = paper_sigma.get((name, m))
            if ref is not None:
                if not sigma2.overlaps(paper_decimal_ball(ref)):
                    fail("sigma_%d^2(%s) is inconsistent with paper value %s" % (m, name, ref))
                else:
                    print("      consistent with paper value %s: OK" % ref)
    print("  [B] done in %.2fs" % (time.time() - t0))
    return results


# ----------------------------------------------------------------------------
# [C] zero localization by certified sign changes of Hardy Z
# ----------------------------------------------------------------------------

def part_C(chars_zeros, K, eps_str="1e-20"):
    print("\n[C] Zero localization: certified sign change of Z across each of the")
    print("    first K = %s listed ordinates, window +/- %s"
          % (K if K > 0 else "ALL", eps_str))
    t0 = time.time()
    eps = arb(eps_str)
    ok_all = {}
    for name, (chi, zeros) in chars_zeros.items():
        Kc = K if K > 0 else len(zeros)
        ok = 0
        worst_rad = 0.0
        min_gap = None
        for j in range(Kc):
            g = zeros[j]
            zm = chi.hardy_z(acb(g - eps)).real
            zp = chi.hardy_z(acb(g + eps)).real
            sm, sp = certified_sign(zm), certified_sign(zp)
            worst_rad = max(worst_rad, float(zm.rad()), float(zp.rad()))
            if sm != 0 and sp != 0 and sm == -sp:
                ok += 1
            else:
                fail("%s zero #%d (gamma=%s): no certified sign change"
                     % (name, j + 1, g.str(20)))
            if j + 1 < Kc:
                gap = float((zeros[j + 1] - zeros[j]).mid())
                min_gap = gap if min_gap is None else min(min_gap, gap)
        # certified pairwise disjointness: consecutive ordinates differ by
        # more than 2*eps (arb comparison is True only when provable)
        disjoint = all((zeros[j + 1] - zeros[j]) > 2 * eps for j in range(Kc - 1))
        if not disjoint:
            fail("%s: certified intervals are not disjoint" % name)
        print("  %s: %d/%d ordinates certified (each interval contains >= 1 zero);"
              % (name, ok, Kc))
        print("      intervals pairwise disjoint (min gap %.4f); worst Z-ball radius %.1e"
              % (min_gap, worst_rad))
        ok_all[name] = (ok == Kc and disjoint)
    print("  [C] done in %.2fs" % (time.time() - t0))
    return ok_all


# ----------------------------------------------------------------------------
# [D] completeness by rigorous winding number
# ----------------------------------------------------------------------------

def winding_number(chi, T, x_left=-0.5, x_right=1.5, y_bottom=-0.5, seed_len=0.04,
                   max_evals=2_000_000, arg_rad_max=0.5):
    """Rigorous ball for the winding number of L(s,chi) around 0 along the
    counterclockwise boundary of [x_left, x_right] x [y_bottom, T].
    Returns (winding_arb, n_evals).  Raises RuntimeError on eval budget.
    NOTE: the bottom edge must NOT lie on the real axis: it would pass
    through s = 1, where Arb's Hurwitz-zeta representation of L(s, chi) has
    a cancelling pole and ball evaluation of any segment containing s = 1
    returns non-finite.  We take y_bottom = -1/2 instead, so the box is
    slightly larger than the target region: the count then covers all
    zeros with -1/2 < Im s < T.  If it equals K, then the K zeros already
    certified in [C] (at s = 1/2 + i gamma_j, 6 < gamma_j < T) exhaust the
    box, so in particular there are no unlisted zeros with 0 < Im s < T
    (and none with -1/2 < Im s <= 0 either)."""
    corners = [(x_left, y_bottom), (x_right, y_bottom), (x_right, T), (x_left, T)]
    nev = 0
    total = arb(0)

    def Lval(x, y):
        return chi.l(acb(arb(x), arb(y)))

    for ci in range(4):
        (x1, y1) = corners[ci]
        (x2, y2) = corners[(ci + 1) % 4]
        # seed subdivision of this edge
        edge_len = abs(x2 - x1) + abs(y2 - y1)
        nseg = max(1, int(math.ceil(edge_len / seed_len)))
        pts = []
        for i in range(nseg + 1):
            t = i / nseg
            pts.append((x1 + (x2 - x1) * t, y1 + (y2 - y1) * t))
        vals = {}
        stack = []
        for i in range(nseg):
            stack.append((pts[i], pts[i + 1]))
        # evaluate endpoints lazily, cache by coordinate pair
        def val(p):
            nonlocal nev
            if p not in vals:
                vals[p] = Lval(p[0], p[1])
                nev += 1
            return vals[p]
        stack.reverse()
        while stack:
            (pa, pb) = stack.pop()
            if nev > max_evals:
                raise RuntimeError("winding: evaluation budget exceeded")
            if abs(pb[0] - pa[0]) + abs(pb[1] - pa[1]) < 1e-9:
                raise RuntimeError(
                    "winding: segment near (%.6g, %.6g) would not certify "
                    "(possible zero on or near the contour)" % (pa[0], pa[1]))
            # covering ball of the segment, built EXACTLY: the union of the
            # two exact endpoint balls is a ball containing both endpoints,
            # hence (it is a product of intervals in re/im) the segment.
            re_hull = arb(pa[0]).union(arb(pb[0]))
            im_hull = arb(pa[1]).union(arb(pb[1]))
            B = chi.l(acb(re_hull, im_hull))
            nev += 1
            mx, my = (pa[0] + pb[0]) / 2, (pa[1] + pb[1]) / 2
            good = not contains_zero(B)
            if good:
                # 0 not in B  =>  arg varies by < pi along the segment,
                # so continuous Delta arg = principal Arg of the ratio.
                delta = (val(pb) / val(pa)).arg()
                if float(delta.rad()) < arg_rad_max:
                    total += delta
                    continue
            # subdivide
            pm = (mx, my)
            stack.append((pm, pb))
            stack.append((pa, pm))
    return total / (2 * arb.pi()), nev


def part_D(chars_zeros, K, eps, top_offset):
    print("\n[D] Completeness: rigorous winding-number count of ALL zeros of L in")
    print("    (-1/2, 3/2) x (-1/2, T), T strictly above gamma_K")
    t0 = time.time()
    results = {}
    old_prec = ctx.prec
    ctx.prec = 96          # plenty for sign/arg information along the contour
    try:
        for name, (chi, zeros) in chars_zeros.items():
            Kd = K if K > 0 else len(zeros)
            if Kd <= 0 or Kd > len(zeros):
                fail("%s: requested K=%d but list has %d ordinates"
                     % (name, Kd, len(zeros)))
                continue
            if Kd < len(zeros):
                T = float((zeros[Kd - 1] + zeros[Kd]).mid()) / 2
                # Certify separation from both stored neighboring intervals.
                if not (zeros[Kd - 1] + eps < arb(T)
                        and arb(T) < zeros[Kd] - eps):
                    fail("%s: T=%.6f not certified between gamma_K + eps and "
                         "gamma_{K+1} - eps" % (name, T))
                    continue
                placement = "between stored gamma_K and gamma_{K+1}"
            else:
                # There is no stored gamma_{K+1}.  Place the top edge above
                # the final certified interval.  winding_number evaluates an
                # enclosing ball for every contour segment and refuses any
                # segment whose L-image contains zero, so success certifies
                # the top edge (and the rest of the contour) as zero-free.
                T = float(zeros[-1].mid()) + top_offset
                if not (zeros[-1] + eps < arb(T)):
                    fail("%s: --top-offset does not place T above gamma_K + eps"
                         % name)
                    continue
                placement = "above the final stored ordinate"
            # ... and strictly above the bottom edge of the box
            if not (zeros[0] - eps > arb(-1) / 2):
                fail("%s: first certified interval not above Im s = -1/2" % name)
                continue
            try:
                w, nev = winding_number(chi, T)
            except RuntimeError as e:
                fail("%s: %s" % (name, e))
                continue
            try:
                n = w.unique_fmpz()
            except (ValueError, TypeError):
                n = None
            # print T truncated DOWNWARD (never overstate the certified
            # height; %.6f would round up), plus the exact float
            print("  %s: T = %.6f (truncated; exact %r)," %
                  (name, math.floor(T * 1e6) / 1e6, T))
            print("      placement: %s" % placement)
            print("      winding ball %s, L-evaluations %d"
                  % (w.str(10, radius=True), nev))
            if n is None:
                fail("%s: winding ball does not determine a unique integer" % name)
                continue
            n = int(n)
            print("      => L(s, %s) has EXACTLY %d zeros (with multiplicity) in the box"
                  % (name, n))
            if n == Kd:
                print("      => combined with [C]: each certified interval contains exactly one")
                print("         zero, that zero is simple, and the box contains no other zeros;")
                print("         with the classical zero-free regions (Re s >= 1, Re s <= 0) this")
                print("         is a completeness proof for the first %d ordinates up to T." % Kd)
                results[name] = True
            else:
                fail("%s: winding count %d != K = %d (missing or extra zeros!)" % (name, n, Kd))
                results[name] = False
    finally:
        ctx.prec = old_prec
    print("  [D] done in %.2fs" % (time.time() - t0))
    return results


# ----------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--K", type=int, default=50,
                    help="zeros per character to certify; 0 = the whole list "
                         "(completeness then runs to T above the final listed "
                         "ordinate)")
    ap.add_argument("--prec", type=int, default=200, help="working precision (bits) for [A]-[C]")
    ap.add_argument("--top-offset", type=float, default=0.25,
                    help="when K reaches the end of a stored list, place the "
                         "winding contour this far above its final ordinate")
    ap.add_argument("--skip-winding", action="store_true")
    ap.add_argument("--eps", default="1e-20", help="zero-localization half-width")
    args = ap.parse_args()

    if not math.isfinite(args.top_offset) or args.top_offset <= 0:
        ap.error("--top-offset must be a finite positive number")

    t_start = time.time()
    ctx.prec = args.prec
    print("python-flint ball-arithmetic certification  (prec = %d bits)" % ctx.prec)

    chi4 = dirichlet_char(4, 3)
    chi3 = dirichlet_char(3, 2)
    assert chi4.is_primitive() and chi4.is_real() and chi4.parity() == 1
    assert chi3.is_primitive() and chi3.is_real() and chi3.parity() == 1

    # sanity anchor: L(2, chi4) = Catalan
    if not chi4.l(acb(2)).real.overlaps(arb.const_catalan()):
        fail("anchor L(2, chi4) = G failed")

    def load(fn):
        with open(os.path.join(HERE, fn)) as f:
            return [arb(line.strip()) for line in f if line.strip()]

    zeros4 = load("chi4_zeros.txt")
    zeros3 = load("chi3_zeros.txt")

    paper_C = {
        "chi4": "0.156029649889644884607682",   # paper Cor. cor:Cexact
        "chi3": "0.11340215685275857",          # paper Sec. NCZ remark
    }
    paper_sigma = {
        ("chi4", 0): "0.15556797992358593",
        ("chi4", 1): "1.368555", ("chi4", 3): "6.776846",
        ("chi4", 8): "29.712468", ("chi4", 20): "106.326000",
        ("chi4", 100): "836.874384",
        ("chi3", 0): "0.11322996985747234",
    }
    chars_A = {"chi4": chi4, "chi3": chi3}
    part_A(chars_A, paper_C)

    m_list = [0, 1, 2, 3, 8, 20, 100]
    Ns = sorted({10 ** 6, 10 ** 5, 10 ** 4, 1000})
    t0 = time.time()
    biggest = max(Ns)
    primes_all = sieve_primes(biggest)
    primes_by_N = {N: [p for p in primes_all if p <= N] for N in Ns}
    print("\n  (sieved primes to %d in %.1fs)" % (biggest, time.time() - t0))
    part_B({"chi4": (chi4, 4), "chi3": (chi3, 3)}, m_list, paper_sigma, primes_by_N)

    chars_zeros = {"chi4": (chi4, zeros4), "chi3": (chi3, zeros3)}
    part_C(chars_zeros, args.K, args.eps)

    if not args.skip_winding:
        part_D(chars_zeros, args.K, arb(args.eps), args.top_offset)
    else:
        print("\n[D] skipped (--skip-winding); completeness of the ordinate lists")
        print("    is then NOT certified by this run.")

    print("\n" + "=" * 72)
    if FAILURES:
        print("RESULT: %d CERTIFICATION FAILURE(S):" % len(FAILURES))
        for f in FAILURES:
            print("  - " + f)
        print("total time %.1fs" % (time.time() - t_start))
        sys.exit(1)
    print("RESULT: all certifications PASSED (total time %.1fs)" % (time.time() - t_start))
    sys.exit(0)


if __name__ == "__main__":
    main()
