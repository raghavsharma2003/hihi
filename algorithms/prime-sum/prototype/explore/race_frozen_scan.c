/* Auditor's scanner: frozen races m = -1 and m = -0.75 to X (default 1e10).
 * Same sieve + Neumaier-compensated long-double machinery as
 * race_critical_scan.c; tracks sign changes and running minimum of
 *   D_m(x) = sum_{p<=x, p=3(4)} p^m - sum_{p<=x, p=1(4)} p^m.
 * Emits: SUMMARY m X D flips last_flip first_neg minD minD_at
 */
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

typedef struct { long double s, c; } acc;
static inline void acc_add(acc *a, long double v)
{
    long double t = a->s + v;
    if (fabsl(a->s) >= fabsl(v)) a->c += (a->s - t) + v;
    else                         a->c += (v - t) + a->s;
    a->s = t;
}
static inline long double acc_val(const acc *a) { return a->s + a->c; }

#define NW 2
static const long double MW[NW] = {-1.0L, -0.75L};

int main(int argc, char **argv)
{
    uint64_t X = argc > 1 ? (uint64_t)atof(argv[1]) : 10000000000ULL;

    uint64_t r = (uint64_t)sqrtl((long double)X) + 1;
    uint8_t *small = calloc(r + 1, 1);
    uint64_t nsp = 0;
    uint64_t *sp = malloc((r / 2 + 2) * sizeof(uint64_t));
    for (uint64_t q = 3; q <= r; q += 2) {
        if (small[q]) continue;
        sp[nsp++] = q;
        for (uint64_t m2 = q * q; m2 <= r; m2 += 2 * q) small[m2] = 1;
    }

    acc S3[NW], S1[NW];
    long double D[NW], minD[NW];
    uint64_t minD_at[NW];
    int lead[NW];
    uint64_t flips[NW], last_flip[NW], first_neg[NW];
    for (int i = 0; i < NW; i++) {
        S3[i].s = S3[i].c = S1[i].s = S1[i].c = 0;
        D[i] = 0; minD[i] = 1e30L; minD_at[i] = 0;
        lead[i] = 0; flips[i] = 0; last_flip[i] = 0; first_neg[i] = 0;
    }

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
            long double pl = (long double)p;
            long double t1 = 1.0L / pl;                 /* p^-1   */
            long double t2 = 1.0L / powl(pl, 0.75L);    /* p^-3/4 */
            long double tv[NW] = {t1, t2};
            int is3 = ((p & 3ULL) == 3ULL);
            for (int i = 0; i < NW; i++) {
                if (is3) acc_add(&S3[i], tv[i]); else acc_add(&S1[i], tv[i]);
                D[i] = acc_val(&S3[i]) - acc_val(&S1[i]);
                int nl = D[i] > 0 ? 1 : (D[i] < 0 ? -1 : 0);
                if (nl && nl != lead[i]) {
                    if (lead[i]) {
                        flips[i]++;
                        last_flip[i] = p;
                        if (nl < 0 && !first_neg[i]) first_neg[i] = p;
                    }
                    lead[i] = nl;
                }
                if (D[i] < minD[i]) { minD[i] = D[i]; minD_at[i] = p; }
            }
        }
    }
    for (int i = 0; i < NW; i++)
        printf("SUMMARY m=%.2Lf X=%llu D=%.18Le flips=%llu last_flip=%llu "
               "first_neg=%llu minD=%.18Le minD_at=%llu\n",
               MW[i], (unsigned long long)X, D[i],
               (unsigned long long)flips[i], (unsigned long long)last_flip[i],
               (unsigned long long)first_neg[i], minD[i],
               (unsigned long long)minD_at[i]);
    return 0;
}
