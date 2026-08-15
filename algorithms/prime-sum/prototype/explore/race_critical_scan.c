/*
 * race_critical_scan.c — the CRITICAL weighted Chebyshev race m = -1/2, exact.
 *
 *   D(x) = sum_{p<=x, p=3 mod 4} p^{-1/2}  -  sum_{p<=x, p=1 mod 4} p^{-1/2}
 *
 * tracked over a segmented sieve in long double with Neumaier-compensated
 * accumulators (worst-case rounding ~1e-14 at X=1e10; the quantities we test
 * live at 1e-2..1e-4). Companion of race_scan.c (which does m = 0..3 in exact
 * __int128); at m = -1/2 the summands are irrational so we go to compensated
 * long double instead.
 *
 * Theory being tested (see race_critical.py for the derivation):
 *   D(x) = (1/2) log log x + C* + eps(x),   C* = -0.07153...,
 * with eps(x) an almost-periodic fluctuation of sd ~ sqrt(Sigma)/log x,
 * Sigma = sum_{gamma>0, L(1/2+i gamma,chi4)=0} 2/gamma^2 = 0.15603...
 *
 * Emits:
 *   CP <x> <D(x)>            at x = 10^k and at 32 log-spaced points/decade
 *   SUMMARY X D flips last_flip first_neg minD minD_at
 * where flips counts strict sign changes of D, last_flip is the prime at which
 * the last change happened (0 = sign never changed after it was first set),
 * first_neg the prime at which D first went negative (0 = never), and minD the
 * running minimum of D over primes p >= 3 (location minD_at).
 *
 * Usage: race_critical_scan [X]   (default 1e10; ~1 min at 1e10)
 */
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

/* Neumaier-compensated long double accumulator */
typedef struct { long double s, c; } acc;
static inline void acc_add(acc *a, long double v)
{
    long double t = a->s + v;
    if (fabsl(a->s) >= fabsl(v)) a->c += (a->s - t) + v;
    else                         a->c += (v - t) + a->s;
    a->s = t;
}
static inline long double acc_val(const acc *a) { return a->s + a->c; }

static int cmp_u64(const void *a, const void *b)
{
    uint64_t x = *(const uint64_t *)a, y = *(const uint64_t *)b;
    return x < y ? -1 : x > y ? 1 : 0;
}

int main(int argc, char **argv)
{
    uint64_t X = argc > 1 ? (uint64_t)atof(argv[1]) : 10000000000ULL;

    /* checkpoint list: powers of 10 plus 32 log-spaced points per decade */
    uint64_t cps[1024];
    int ncp = 0;
    for (uint64_t v = 10; v <= X && v >= 10; v *= 10) cps[ncp++] = v;
    for (int j = 33; j < 1000; j++) {          /* 10^(j/32) from just above 10 */
        long double e = powl(10.0L, (long double)j / 32.0L);
        if (e > (long double)X + 0.5L) break;
        uint64_t v = (uint64_t)(e + 0.5L);
        if (v > 10 && v <= X) cps[ncp++] = v;
    }
    qsort(cps, ncp, sizeof(uint64_t), cmp_u64);
    int w = 0;
    for (int i = 0; i < ncp; i++)
        if (w == 0 || cps[i] != cps[w-1]) cps[w++] = cps[i];
    ncp = w;

    /* small sieve of odd primes up to sqrt(X) */
    uint64_t r = (uint64_t)sqrtl((long double)X) + 1;
    uint8_t *small = calloc(r + 1, 1);
    uint64_t nsp = 0;
    uint64_t *sp = malloc((r / 2 + 2) * sizeof(uint64_t));
    for (uint64_t q = 3; q <= r; q += 2) {
        if (small[q]) continue;
        sp[nsp++] = q;
        for (uint64_t m2 = q * q; m2 <= r; m2 += 2 * q) small[m2] = 1;
    }

    acc S3 = {0, 0}, S1 = {0, 0};       /* 3-side / 1-side partial sums */
    long double D = 0.0L, minD = 1e30L;
    uint64_t minD_at = 0;
    int lead = 0;                        /* sign of D: +1 / -1 / 0(unset) */
    uint64_t flips = 0, last_flip = 0, first_neg = 0;
    int icp = 0;

    const uint64_t SEG = 1u << 22;
    uint8_t *seg = malloc(SEG / 16 + 2);

    for (uint64_t lo = 3; lo <= X; lo += SEG) {
        uint64_t hi = lo + SEG - 1 < X ? lo + SEG - 1 : X;
        uint64_t lo_odd = lo | 1ULL;
        uint64_t nbits = (hi - lo_odd) / 2 + 1;
        memset(seg, 0, (nbits + 7) / 8);
        for (uint64_t k = 0; k < nsp; k++) {
            uint64_t q = sp[k];
            if (q * q > hi) break;
            uint64_t s = q * q;
            if (s < lo_odd) { s = ((lo_odd + q - 1) / q) * q; if (!(s & 1)) s += q; }
            for (uint64_t v = s; v <= hi; v += 2 * q)
                seg[((v - lo_odd) / 2) >> 3] |= (uint8_t)(1u << (((v - lo_odd) / 2) & 7));
        }
        for (uint64_t b = 0; b < nbits; b++) {
            if (seg[b >> 3] & (1u << (b & 7))) continue;
            uint64_t p = lo_odd + 2 * b;
            if (p < 3) continue;
            while (icp < ncp && p > cps[icp]) {
                printf("CP %llu %.18Le\n", (unsigned long long)cps[icp], D);
                icp++;
            }
            long double t = 1.0L / sqrtl((long double)p);
            if ((p & 3ULL) == 3ULL) acc_add(&S3, t); else acc_add(&S1, t);
            D = acc_val(&S3) - acc_val(&S1);
            int nl = D > 0 ? 1 : (D < 0 ? -1 : 0);
            if (nl && nl != lead) {
                if (lead) {
                    flips++;
                    last_flip = p;
                    if (nl < 0 && !first_neg) first_neg = p;
                }
                lead = nl;
            }
            if (D < minD) { minD = D; minD_at = p; }
        }
    }
    while (icp < ncp) {                  /* checkpoints beyond the last prime */
        printf("CP %llu %.18Le\n", (unsigned long long)cps[icp], D);
        icp++;
    }
    printf("SUMMARY %llu %.18Le %llu %llu %llu %.18Le %llu\n",
           (unsigned long long)X, D,
           (unsigned long long)flips, (unsigned long long)last_flip,
           (unsigned long long)first_neg, minD, (unsigned long long)minD_at);
    return 0;
}
