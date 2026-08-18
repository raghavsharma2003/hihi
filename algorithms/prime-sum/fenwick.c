/*
 * fenwick.c — sum of all primes <= n in ~O(n^(2/3)) time.
 *
 * The next complexity class beyond lucy.c, trading memory for time.
 * Prior art: Deléglise–Rivat (1996, for pi(x)), Kim Walisch's primesum,
 * and the "Lucy + Fenwick" hybrid described by gbroxey (2023).
 *
 * Idea: lucy.c spends most of its time re-updating the ~sqrt(n) small
 * keys for every prime. Instead, sieve [1, B] directly (B ~ n^(2/3))
 * with a Fenwick tree over the values, so that
 *   query(x) = sum of survivors in [2, x]
 * is available on demand in O(log B). Only the n/B large keys v = n/i > B
 * are kept as an explicit Lucy table and updated per prime:
 *   S[v] -= p * (S[v/p] - sum_of_primes_below_p)
 * where the inner term is a table read (v/p > B) or a BIT query (v/p <= B).
 *
 * Per prime p (ascending), in this order:
 *   1. update all large keys with v >= p^2  (reads see the p-1 state)
 *   2. remove composites c <= B with lpf(c) == p from the BIT
 *      (c = p*m, m in [p, B/p], lpf(m) >= p — each composite exactly once)
 *
 * Cost: O(B log B) for the BIT sieve + O((n/sqrt(B)) log B) for the large
 * keys; balancing gives B ~ n^(2/3), total ~O(n^(2/3)) up to log factors.
 * Memory: O(B) — lpf array (4 bytes) + BIT (8 bytes) per slot.
 */
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <math.h>

typedef __int128 i128;

static void print_i128(i128 x)
{
    char buf[48];
    int i = 0;
    if (x < 0) { putchar('-'); x = -x; }
    do { buf[i++] = (char)('0' + (int)(x % 10)); x /= 10; } while (x);
    while (i--) putchar(buf[i]);
}

static uint64_t B;      /* sieve bound, BIT covers [1, B] */
static uint64_t *bit;   /* Fenwick tree: sum of surviving values */

static inline void bit_sub(uint64_t i, uint64_t v)
{
    for (; i <= B; i += i & (~i + 1))
        bit[i] -= v;
}

static inline uint64_t bit_query(uint64_t i)
{
    uint64_t s = 0;
    for (; i; i -= i & (~i + 1))
        s += bit[i];
    return s;
}

int main(int argc, char **argv)
{
    uint64_t n = 1000;
    if (argc > 1)
        n = strtoull(argv[1], NULL, 10);
    if (n < 2) { printf("0\n"); return 0; }

    uint64_t r = (uint64_t)sqrtl((long double)n);
    while (r * r > n) r--;
    while ((r + 1) * (r + 1) <= n) r++;

    /* Sieve bound: ~n^(2/3)/8 balances BIT sieving against key updates
     * empirically; must be at least sqrt(n) so every prime p <= r is found. */
    if (argc > 2) {
        B = strtoull(argv[2], NULL, 10);
    } else {
        B = (uint64_t)(powl((long double)n, 2.0L / 3.0L) / 8);
        if (B < 2 * r) B = 2 * r;
        if (B > 200000000ULL) B = 200000000ULL;
    }
    if (B > n) B = n;

    /* Smallest-prime-factor table over [1, B] via linear sieve. */
    uint32_t *lpf = calloc(B + 1, sizeof(uint32_t));
    /* pi(B) < B/(ln B - 1.1) for B >= 60184 (Dusart); +100 covers small B */
    uint64_t max_primes = (uint64_t)((double)B / (log((double)B) - 1.2)) + 100;
    uint32_t *primes = malloc(max_primes * sizeof(uint32_t));
    uint64_t nprimes = 0;
    if (!lpf || !primes) { fprintf(stderr, "out of memory\n"); return 1; }
    for (uint64_t i = 2; i <= B; i++) {
        if (!lpf[i]) { lpf[i] = (uint32_t)i; primes[nprimes++] = (uint32_t)i; }
        for (uint64_t k = 0; k < nprimes && primes[k] <= lpf[i]
                             && i * primes[k] <= B; k++)
            lpf[i * primes[k]] = primes[k];
    }

    /* The p=2 round never needs the tree: before any sieving,
     * query(x) is just the triangular sum x(x+1)/2 - 1. So the BIT starts
     * in the post-p=2 state — odd values only (plus the prime 2 itself) —
     * which skips removing the ~B/2 even composites one by one. */
    bit = calloc(B + 1, sizeof(uint64_t));
    if (!bit) { fprintf(stderr, "out of memory\n"); return 1; }
    if (B >= 2) bit[2] += 2;
    for (uint64_t i = 3; i <= B; i += 2) bit[i] += i;
    for (uint64_t i = 1; i <= B; i++) {
        uint64_t j = i + (i & (~i + 1));
        if (j <= B) bit[j] += bit[i];
    }

    /* Large keys: v = n/i > B, i.e. i <= L. Base: S[v] = v(v+1)/2 - 1. */
    uint64_t L = n / B;
    i128 *S = malloc((L + 1) * sizeof(i128));
    if (!S) { fprintf(stderr, "out of memory\n"); return 1; }
    for (uint64_t i = 1; i <= L; i++) {
        uint64_t v = n / i;
        S[i] = (i128)v * (v + 1) / 2 - 1;
    }

    /* p = 2 with the closed-form inner term (pre-sieve state). */
    if (r >= 2) {
        uint64_t imax = n / 4 < L ? n / 4 : L;
        for (uint64_t i = 1; i <= imax; i++) {
            uint64_t ip = 2 * i;
            i128 inner;
            if (ip <= L) {
                inner = S[ip];
            } else {
                uint64_t x = n / ip;
                inner = (i128)x * (x + 1) / 2 - 1;
            }
            S[i] -= 2 * inner;
        }
    }

    i128 sp = 2; /* sum of primes < p */
    for (uint64_t k = 1; k < nprimes && (uint64_t)primes[k] <= r; k++) {
        uint64_t p = primes[k];
        uint64_t p2 = p * p;

        uint64_t imax = n / p2 < L ? n / p2 : L;
        for (uint64_t i = 1; i <= imax; i++) {
            uint64_t ip = i * p;
            i128 inner = (ip <= L) ? S[ip] : (i128)bit_query(n / ip);
            S[i] -= (i128)p * (inner - sp);
        }

        for (uint64_t m = p, c = p2; c <= B; m++, c += p)
            if (lpf[m] >= p)
                bit_sub(c, c);

        sp += p;
    }

    printf("sum of primes till that number-> ");
    print_i128(L >= 1 ? S[1] : (i128)bit_query(n));
    putchar('\n');

    free(lpf); free(primes); free(bit); free(S);
    return 0;
}
