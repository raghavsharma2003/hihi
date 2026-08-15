#!/usr/bin/env python3
"""Certified-enclosure version of the 30-point monotonicity grid.

Runs the certified pipeline of race_density_certified.py (tail variance
from the Hadamard identity sigma_m^2 = 4M (log Lambda)'(m+1), Gaussian
tail with the proved quartic correction, all error terms budgeted into
the interval radius) on the same 30-point grid as race_mono_grid.py, and
reports, for each pair of consecutive grid points, the gap between the
adjacent enclosures:  gap = lo(m) - hi(m')  for m < m'.  A positive gap
certifies the strict decrease delta(m) > delta(m') modulo exactly the
honestly-listed budget items of race_density_certified.py (GRH + LI,
completeness of the ordinate lists, 40-digit mpmath evaluation of
sigma_m^2, double-precision Simpson quadrature with Richardson control).
"""
import numpy as np
import race_density_certified as rc

MS = [-0.2, -0.15, -0.1, -0.05, 0.0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5,
      2.0, 2.5, 3.0, 4.0, 5.0, 6.0, 8.0, 10.0, 12.0, 15.0, 20.0, 25.0,
      30.0, 40.0, 50.0, 60.0, 75.0, 90.0, 100.0]
assert len(MS) == 30

rc.run_anchors()
print()
for q, fname in [(4, "chi4_zeros.txt"), (3, "chi3_zeros.txt")]:
    print(f"== modulus {q}: certified enclosures on the 30-point grid ==")
    gam_mpf, gam_f = rc.load_zeros(fname, q)
    rows = []
    for m in MS:
        s2 = rc.sigma2(q, m)
        r = rc.enclose(q, m, gam_mpf, gam_f, s2)
        rows.append(r)
        print(f"  m={m:7.2f}  delta in [{r['lo']:.10f}, {r['hi']:.10f}]"
              f"  width={r['width']:.2e}")
    print(f"  -- adjacent-pair gaps (lo(m) - hi(m'), m < m'; positive = "
          f"strict decrease certified) --")
    min_gap, min_pair, all_pos = None, None, True
    for r0, r1 in zip(rows, rows[1:]):
        gap = r0['lo'] - r1['hi']
        if gap <= 0: all_pos = False
        if min_gap is None or gap < min_gap:
            min_gap, min_pair = gap, (r0['m'], r1['m'])
        print(f"  ({r0['m']:g},{r1['m']:g}): gap = {gap:+.3e}")
    print(f"  ALL 29 GAPS POSITIVE: {all_pos};  smallest gap {min_gap:.3e}"
          f" at pair {min_pair};  max width {max(r['width'] for r in rows):.2e}")
    print()
