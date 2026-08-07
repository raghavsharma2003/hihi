/*
 * lucy.c — sum of all primes <= n in O(n^(3/4)) time and O(sqrt(n)) memory.
 *
 * Same recurrence as original.c, plus the one idea that changes its
 * complexity class: floor(n/i) takes only ~2*sqrt(n) distinct values, so
 * instead of recursing top-down (recomputing subproblems exponentially
 * often), keep one running table S indexed by those distinct values and
 * sweep primes bottom-up.
 *
 * Invariant: after processing all primes < p,
 *   S[v] = sum of every m in [2, v] that is prime OR has no prime factor < p.
 * Processing prime p removes exactly the composites whose smallest prime
 * factor is p:
 *   S[v] -= p * (S[v/p] - (sum of primes < p))     for all v >= p*p.
 * After sweeping p up to sqrt(n), S[n] is the sum of primes <= n.
 *
 * Sums are kept in __int128: sum of primes <= 1e11 already overflows int64.
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

int main(int argc, char **argv)
{
    uint64_t n = 1000;
    if (argc > 1)
        n = strtoull(argv[1], NULL, 10);
    if (n < 2) { printf("0\n"); return 0; }

    uint64_t r = (uint64_t)sqrtl((long double)n);
    while (r * r > n) r--;
    while ((r + 1) * (r + 1) <= n) r++;

    /* Two halves of the table: value v <= r lives at Ssmall[v];
     * value v = n/i > r lives at Slarge[i]. Together: every floor(n/i). */
    i128 *Ssmall = malloc((r + 1) * sizeof(i128));
    i128 *Slarge = malloc((r + 1) * sizeof(i128));
    if (!Ssmall || !Slarge) { fprintf(stderr, "out of memory\n"); return 1; }

    /* Base case (no primes processed yet): S[v] = 2 + 3 + ... + v. */
    for (uint64_t v = 1; v <= r; v++)
        Ssmall[v] = (i128)v * (v + 1) / 2 - 1;
    for (uint64_t i = 1; i <= r; i++) {
        uint64_t v = n / i;
        Slarge[i] = (i128)v * (v + 1) / 2 - 1;
    }

    for (uint64_t p = 2; p <= r; p++) {
        /* p is prime iff sieving so far left it standing: S[p] > S[p-1]. */
        if (Ssmall[p] == Ssmall[p - 1])
            continue;
        i128 sp = Ssmall[p - 1]; /* sum of primes < p */
        uint64_t p2 = p * p;

        /* Large keys first, ascending i = descending v, so every read of
         * S[v/p] still sees the value from the previous prime. */
        uint64_t imax = n / p2 < r ? n / p2 : r;
        for (uint64_t i = 1; i <= imax; i++) {
            uint64_t ip = i * p;
            i128 inner = (ip <= r) ? Slarge[ip] : Ssmall[n / ip];
            Slarge[i] -= (i128)p * (inner - sp);
        }
        for (uint64_t v = r; v >= p2; v--)
            Ssmall[v] -= (i128)p * (Ssmall[v / p] - sp);
    }

    printf("sum of primes till that number-> ");
    print_i128(r >= 1 ? Slarge[1] : Ssmall[n]);
    putchar('\n');

    free(Ssmall);
    free(Slarge);
    return 0;
}
