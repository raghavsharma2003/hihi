/*
 * sieve.c — segmented sieve of Eratosthenes summing all primes <= n.
 *
 * The strongest fair baseline: O(n log log n) time, O(sqrt(n)) memory,
 * odd-only bitset, cache-sized segments. This is what lucy.c has to beat.
 */
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

typedef __int128 i128;

#define SEG_BYTES (1u << 18) /* 256 KiB bitmap = 2M odd numbers per segment */

static void print_i128(i128 x)
{
    char buf[48];
    int i = 0;
    if (x < 0) { putchar('-'); x = -x; }
    do { buf[i++] = (char)('0' + (int)(x % 10)); x /= 10; } while (x);
    while (i--) putchar(buf[i]);
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

    /* Small odd primes up to sqrt(n) by a plain sieve. */
    uint8_t *small = calloc(r / 2 + 1, 1); /* small[i] ~ odd number 2i+1 */
    uint64_t nsmall = 0;
    uint64_t *sp = malloc((r / 2 + 2) * sizeof(uint64_t));
    if (!small || !sp) { fprintf(stderr, "out of memory\n"); return 1; }
    for (uint64_t q = 3; q <= r; q += 2) {
        if (small[q / 2]) continue;
        sp[nsmall++] = q;
        for (uint64_t m = q * q; m <= r; m += 2 * q)
            small[m / 2] = 1;
    }

    i128 sum = 2; /* the only even prime */
    uint8_t *seg = malloc(SEG_BYTES);
    uint64_t span = (uint64_t)SEG_BYTES * 16; /* odd numbers per segment */

    for (uint64_t lo = 3; lo <= n; lo += span) {
        uint64_t hi = lo + span - 1 < n ? lo + span - 1 : n;
        memset(seg, 0, SEG_BYTES);
        /* bit b of seg ~ odd number lo + 2b (lo is odd) */
        for (uint64_t k = 0; k < nsmall; k++) {
            uint64_t q = sp[k];
            if (q * q > hi) break;
            uint64_t start = q * q;
            if (start < lo) {
                start = ((lo + q - 1) / q) * q;
                if (!(start & 1)) start += q;
            }
            for (uint64_t m = start; m <= hi; m += 2 * q) {
                uint64_t b = (m - lo) / 2;
                seg[b >> 3] |= (uint8_t)(1u << (b & 7));
            }
        }
        uint64_t count = (hi - lo) / 2 + 1;
        for (uint64_t b = 0; b < count; b++)
            if (!(seg[b >> 3] & (1u << (b & 7))))
                sum += lo + 2 * b;
    }

    printf("sum of primes till that number-> ");
    print_i128(sum);
    putchar('\n');

    free(small); free(sp); free(seg);
    return 0;
}
