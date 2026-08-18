#!/usr/bin/env python3
"""
Prototype 2: Gaussian-smoothed explicit formula for weighted prime sums —
the mechanism that makes Platt-style analytic computation practical.

Target:  psi1_smooth(x) = sum_n Lambda(n) * n * c(n),
         c(t) = (1/2) erfc( ln(t/x) / (sqrt(2)*eps) )     (log-Gaussian cutoff)

Mellin:  g(t) = t*c(t)  has  ghat(s) = x^(s+1)/(s+1) * exp((s+1)^2 eps^2/2)
         (exact: substitute t = x e^u, integrate by parts, Gaussian MGF).

Explicit formula (contour shift of Perron against -zeta'/zeta):
         psi1_smooth = ghat(1) - sum_rho ghat(rho) - (tiny trivial terms)
         ghat(1)   = (x^2/2) exp(2 eps^2)
         ghat(rho) = x^(rho+1)/(rho+1) * exp((rho+1)^2 eps^2/2)
On RH rho+1 = 3/2 + i*gamma, so |ghat(rho)| ~ x^(3/2) e^(-gamma^2 eps^2/2):
zeros with gamma >> 1/eps are killed — a hard effective truncation, unlike
the sharp-cutoff formula whose tail decays only like 1/gamma.

The exact side is computed by brute force over all primes (and prime powers)
up to x*e^(12 eps), so this validates the analytic side end to end.
Predicted error floor from zero-table precision (3e-9 per Odlyzko's file):
each zero's term errs by ~ |dterm/dgamma| * 3e-9; we report the RMS sum.
"""
import sys, os, math
import numpy as np

ZEROS = sys.argv[1] if len(sys.argv) > 1 else "/tmp/claude-0/-home-user-hihi/482aec6c-4f00-58b8-b5df-df7d9a8314a0/scratchpad/zeros1"
ZERO_PREC = float(sys.argv[2]) if len(sys.argv) > 2 else 3e-9
X = int(float(sys.argv[3])) if len(sys.argv) > 3 else 10**8

ld = np.longdouble


def sieve_primes(limit):
    is_c = np.zeros(limit + 1, dtype=bool)
    is_c[:2] = True
    for i in range(2, int(limit**0.5) + 1):
        if not is_c[i]:
            is_c[i * i :: i] = True
    return np.flatnonzero(~is_c)


def cutoff(vals, x, eps):
    """c(t) as float64 (erfc noise ~1e-16 << all floors here)."""
    u = (np.log(vals.astype(np.float64)) - math.log(x)) / eps
    c = np.empty_like(u)
    lo, hi = u < -12.0, u > 12.0
    c[lo], c[hi] = 1.0, 0.0
    mid = ~(lo | hi)
    c[mid] = 0.5 * np.vectorize(math.erfc)(u[mid] / math.sqrt(2.0))
    return c


def exact_side(x, eps, primes, logs):
    c = cutoff(primes, x, eps)
    total = np.sum(primes.astype(ld) * logs.astype(ld) * c.astype(ld))
    # prime powers p^k, k >= 2, up to x*e^(12 eps)
    lim = x * math.exp(12 * eps)
    for p in map(int, primes[primes <= int(lim**0.5) + 1]):
        lp = math.log(p)
        pk = p * p
        while pk <= lim:
            u = (math.log(pk) - math.log(x)) / eps
            cc = 1.0 if u < -12 else (0.0 if u > 12 else 0.5 * math.erfc(u / math.sqrt(2)))
            total += ld(lp) * ld(pk) * ld(cc)
            pk *= p
    return total


def analytic_side(x, eps, gammas):
    L = np.log(ld(x))
    g = gammas.astype(ld)
    # ghat(rho): exp( 1.5L + (2.25-g^2) eps^2/2 + i(gL + 1.5 g eps^2) ) / (1.5+ig)
    mag = np.exp(ld(1.5) * L + (ld(2.25) - g * g) * ld(eps) ** 2 / 2)
    ph = g * L + ld(1.5) * g * ld(eps) ** 2
    num = mag * (np.cos(ph) + 1j * np.sin(ph))
    den = ld(1.5) + 1j * g.astype(np.complex256)
    zs = 2 * np.sum((num / den).real)
    main = (ld(x) * x / 2) * np.exp(2 * ld(eps) ** 2)
    return main - zs, mag / np.abs(den)


def main():
    gammas_all = np.loadtxt(ZEROS, dtype=ld)
    print(f"x = {X:.0e}, {len(gammas_all)} zeros loaded (precision ~{ZERO_PREC:.0e})")
    lim_max = int(X * math.exp(12 * 8 / float(gammas_all[min(1999, len(gammas_all)-1)])))
    primes = sieve_primes(lim_max)
    logs = np.log(primes.astype(np.float64))
    L = math.log(X)
    print(f"{'N zeros':>8} {'eps':>10} {'analytic - exact':>18} {'rel err':>10} "
          f"{'pred tail':>10} {'pred floor':>10}")
    Ns = [n for n in [2000, 10000, 50000, 100000] if n <= len(gammas_all)]
    for N in Ns:
        gN = float(gammas_all[N - 1])
        eps = 8.0 / gN
        g = gammas_all[:N]
        an, sizes = analytic_side(X, eps, g)
        ex = exact_side(X, eps, primes, logs)
        err = float(an - ex)
        # predicted truncation tail: first omitted zeros, RvM density ~ log(g/2pi)/2pi
        tail_g = gammas_all[N:] if N < len(gammas_all) else None
        if tail_g is not None and len(tail_g):
            tg = tail_g.astype(ld)
            tmag = np.exp(ld(1.5) * math.log(X) + (ld(2.25) - tg * tg) * ld(eps) ** 2 / 2)
            tail = float(2 * np.sum(tmag / np.sqrt(ld(2.25) + tg * tg)))
        else:
            tail = float("nan")
        # predicted floor from zero-table precision: |dterm/dgamma| ~ |term|*L
        floor = float(2 * math.sqrt(np.sum((sizes * ld(L) * ld(ZERO_PREC)) ** 2)))
        print(f"{N:>8} {eps:>10.2e} {err:>18.2f} {abs(err)/float(ex):>10.1e} "
              f"{tail:>10.1e} {floor:>10.1e}")


if __name__ == "__main__":
    main()
