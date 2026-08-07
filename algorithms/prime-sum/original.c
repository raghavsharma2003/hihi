/*
 * original.c — the school algorithm, exactly as first written.
 *
 * Kept for benchmarking. Known problems (fixed in lucy.c):
 *   - isprime() is O(n) trial division per call
 *   - R() recomputes the same subproblems exponentially many times
 *   - `int sum` and the (int) casts overflow/truncate for n beyond ~10^5
 */
#include <stdio.h>
#include <stdbool.h>
#include <math.h>

bool isprime(long long n)
{
    if (n <= 1)
        return false;

    for (int i = 2; i < n; i++)
        if (n % i == 0)
            return false;
    return true;
}

long long R(long long k, long long n)
{
    int sum = 0;
    if ((n < 2) || (k < 2))
    {
        return 0;
    }
    else if (k == 2)
    {
        return ((int)(n / 2)) * ((int)(n / 2) + 1);
    }
    else
    {
        sum = 0;
        for (int y = 2; y <= (int)k; y++)
        {
            if (isprime(y))
            {
                sum += y * (((int)(n / y) * ((int)(n / y) + 1)) / 2 - R(y - 1, (int)(n / y)));
            }
        }
        return sum;
    }
}

int main(int argc, char **argv)
{
    long long n = 1000;
    if (argc > 1)
        sscanf(argv[1], "%lld", &n);
    long long k = (int)sqrt(n);
    long long sp = 0;
    for (long long p = 2; p <= k; p++)
        if (isprime(p))
            sp = sp + p;
    long long sum = n * (n + 1) / 2 - R(k, n) - 1 + sp;
    printf("sum of primes till that number-> %lld\n", sum);
    return 0;
}
