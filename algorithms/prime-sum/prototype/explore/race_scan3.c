/*
 * race_scan3.c — exact weighted Chebyshev races mod 3.
 *
 * D_m(x) = sum_{p<=x, p=2 mod 3} p^m  -  sum_{p<=x, p=1 mod 3} p^m,
 * for m = 0,1,2,3, tracked exactly (signed __int128 differences) over a
 * segmented sieve.  2 is the non-residue class mod 3 (squares of primes
 * p != 3 are all = 1 mod 3), so the bias favors the 2-side.  Note p = 2
 * itself is IN the race (2 = 2 mod 3) — the race starts at p = 2 with the
 * 2-side leading — while p = 3 is excluded.  Records, per m:
 *   - the first prime after which the 1 (mod 3) side takes the lead,
 *   - the number of lead changes up to X,
 *   - natural and logarithmic measure of {x <= X : 2-side strictly leads}.
 *
 * Validation anchor: for m=0 the first 1-side lead is classically known to
 * occur at x = 608,981,813,029 (Bays–Hudson 1978) — far beyond this scan,
 * so first_flip[0] MUST come out 0 (never) up to 1e9; that is itself the
 * check.  For m >= 1 the heavy early primes flip the race almost at once
 * (m=1: 2+5-7+11-13 = -2 at p=13; m=2,3: already at p=7).
 *
 * Usage: race_scan3 [X]   (default 1e9)
 */
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

typedef __int128 i128;

static void print_i128(i128 v, char *buf)
{
    char t[48]; int i = 0, neg = v < 0;
    if (neg) v = -v;
    do { t[i++] = (char)('0' + (int)(v % 10)); v /= 10; } while (v);
    int j = 0;
    if (neg) buf[j++] = '-';
    while (i--) buf[j++] = t[i];
    buf[j] = 0;
}

#define NM 4

int main(int argc, char **argv)
{
    uint64_t X = argc > 1 ? (uint64_t)atof(argv[1]) : 1000000000ULL;

    uint64_t r = (uint64_t)sqrtl((long double)X) + 1;
    uint8_t *small = calloc(r + 1, 1);
    uint64_t nsp = 0;
    uint64_t *sp = malloc((r / 2 + 2) * sizeof(uint64_t));
    for (uint64_t q = 3; q <= r; q += 2) {
        if (small[q]) continue;
        sp[nsp++] = q;
        for (uint64_t m2 = q * q; m2 <= r; m2 += 2 * q) small[m2] = 1;
    }

    i128 D[NM] = {0, 0, 0, 0};
    int lead[NM];                    /* +1: 2-side leads, -1: 1-side, 0: tied */
    uint64_t first_flip[NM] = {0, 0, 0, 0};
    uint64_t flips[NM] = {0, 0, 0, 0};
    long double meas2[NM] = {0}, logmeas2[NM] = {0}, tot = 0, logtot = 0;

    /* p = 2 (= 2 mod 3) opens the race: D_m = +2^m, 2-side leads */
    {
        i128 pw = 1;
        for (int m = 0; m < NM; m++) { D[m] += pw; lead[m] = +1; pw *= 2; }
    }
    uint64_t last_evt = 2;

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
            if (p == 3) continue;               /* chi3(3) = 0 */
            int chi = (p % 3 == 2) ? +1 : -1;   /* contribution sign to D */
            i128 pw = 1;
            /* accumulate measures over [last_evt, p) under current leads */
            long double span = (long double)(p - last_evt);
            long double lspan = logl((long double)p) - logl((long double)last_evt);
            tot += span; logtot += lspan;
            for (int m = 0; m < NM; m++) {
                if (lead[m] > 0) { meas2[m] += span; logmeas2[m] += lspan; }
            }
            for (int m = 0; m < NM; m++) {
                D[m] += chi * pw;
                int nl = D[m] > 0 ? 1 : (D[m] < 0 ? -1 : 0);
                if (nl != lead[m] && nl != 0) {
                    if (lead[m] != 0) {
                        flips[m]++;
                        if (nl < 0 && !first_flip[m]) first_flip[m] = p;
                    }
                    lead[m] = nl;
                }
                pw *= (i128)p;
            }
            last_evt = p;
        }
    }
    /* tail interval to X */
    {
        long double span = (long double)(X - last_evt);
        long double lspan = logl((long double)X) - logl((long double)last_evt);
        tot += span; logtot += lspan;
        for (int m = 0; m < NM; m++)
            if (lead[m] > 0) { meas2[m] += span; logmeas2[m] += lspan; }
    }

    printf("X = %llu\n", (unsigned long long)X);
    char b1[48];
    for (int m = 0; m < NM; m++) {
        print_i128(D[m], b1);
        printf("m=%d: D_m(X)=%s  first 1-side lead at p=%llu  lead-changes=%llu\n",
               m, b1, (unsigned long long)first_flip[m], (unsigned long long)flips[m]);
        printf("      2-side leads: natural measure %.6Lf   log measure %.6Lf\n",
               meas2[m] / tot, logmeas2[m] / logtot);
    }
    return 0;
}
