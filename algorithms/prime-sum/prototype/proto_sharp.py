#!/usr/bin/env python3
"""
Prototype 1: sharp-cutoff explicit formula for the sum of primes.

Identity (Riemann-style, non-rigorous constants):
    T(x) := sum_{p^k <= x} p^k / k
          = li(x^2)   - sum_rho li(x^(rho+1)) + O(1)
    S(x) := sum_{p <= x} p = T(x) - sum_{k>=2} (1/k) sum_{p <= x^(1/k)} p^k

Derivation: Perron against Sum Lambda(n)/log(n) * n^(1-s) = log zeta(s-1);
the pole of zeta at s-1=1 gives the li(x^2) main term (sub u = t^2 in
int t dt/log t: the 1/2 from du and the 2 from log sqrt(u) cancel), each nontrivial
zero rho gives -li(x^(rho+1)) via  d(t^(rho+1)/(rho+1)) integrated against
1/log t  (substitute u = t^(rho+1)).

li(x^(rho+1)) = Ei((rho+1) ln x), evaluated by the asymptotic series
Ei(z) ~ e^z/z * sum_k k!/z^k  (|z| >= 14*ln x, so the series is excellent).
The +-i*pi branch constants cancel in Re over conjugate zero pairs.

Purpose: measure |analytic - exact| as a function of the number of zeros N
and check it tracks the predicted envelope x^(3/2)/(gamma_N * ln x).
Zeros: Odlyzko's table of the first 100,000 zeros (9 decimals),
https://www-users.cse.umn.edu/~odlyzko/zeta_tables/zeros1
"""
import subprocess, sys, os
import numpy as np
import mpmath as mp

HERE = os.path.dirname(os.path.abspath(__file__))
ZEROS = sys.argv[1] if len(sys.argv) > 1 else "/tmp/claude-0/-home-user-hihi/482aec6c-4f00-58b8-b5df-df7d9a8314a0/scratchpad/zeros1"
FENWICK = os.path.join(HERE, "..", "fenwick")

mp.mp.dps = 50


def exact_S(x):
    out = subprocess.run([FENWICK, str(x)], capture_output=True, text=True).stdout
    return int(out.strip().split(">")[-1])


def sieve_primes(limit):
    is_c = np.zeros(limit + 1, dtype=bool)
    is_c[:2] = True
    for i in range(2, int(limit**0.5) + 1):
        if not is_c[i]:
            is_c[i * i :: i] = True
    return np.flatnonzero(~is_c)


def prime_power_correction(x):
    """sum_{k>=2} (1/k) * sum_{p^k <= x} p^k, as an exact Fraction-free pair."""
    from fractions import Fraction
    total = Fraction(0)
    ps = sieve_primes(int(x**0.5) + 2)
    for p in map(int, ps):
        pk, k = p * p, 2
        while pk <= x:
            total += Fraction(pk, k)
            pk *= p
            k += 1
    return total


def zero_sum(x, gammas, terms=14):
    """2 * Re sum li(x^(rho+1)) over zeros 1/2+i*gamma via asymptotic Ei."""
    L = np.longdouble(np.log(np.longdouble(x)))
    z = (np.longdouble(1.5) + 1j * gammas.astype(np.complex256)) * L
    # e^z = x^1.5 * exp(i*gamma*L): compute phase in longdouble
    phase = (gammas * L).astype(np.longdouble)
    ez = np.exp(np.longdouble(1.5) * L) * (np.cos(phase) + 1j * np.sin(phase))
    series = np.ones_like(z)
    fac = np.ones_like(z)
    for k in range(1, terms):
        fac = fac * k / z
        series += fac
    return 2.0 * np.sum((ez / z * series).real)


def main():
    gammas_all = np.loadtxt(ZEROS, dtype=np.longdouble)
    print(f"loaded {len(gammas_all)} zeros, gamma_max = {float(gammas_all[-1]):.1f}")
    for x in [10**6, 10**8, 10**10]:
        S = exact_S(x)
        pp = prime_power_correction(x)
        main_term = mp.li(mp.mpf(x) ** 2)
        base = float(main_term - mp.mpf(pp.numerator) / pp.denominator)
        print(f"\nx = {x:.0e}   exact S(x) = {S}")
        print(f"{'N zeros':>8} {'analytic - exact':>20} {'rel err':>12} {'envelope':>12}")
        for N in [100, 1000, 10000, 100000]:
            g = gammas_all[:N]
            approx = base - zero_sum(x, g)
            err = approx - float(S)
            env = x**1.5 / (float(g[-1]) * np.log(x))
            print(f"{N:>8} {err:>20.2f} {abs(err)/S:>12.2e} {env:>12.2e}")


if __name__ == "__main__":
    main()
