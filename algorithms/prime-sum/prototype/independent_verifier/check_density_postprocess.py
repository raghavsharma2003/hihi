#!/usr/bin/env python3
"""Exact checker for the weighted-races density post-processing certificate.

This program intentionally imports only the Python standard library.  Every
decimal in the JSON certificate is parsed as an exact ``Fraction``.  It does
not call FLINT/Arb, mpmath, NumPy, SciPy, or the density-producing program.

The checker verifies:

* all fourteen source intervals have width below 2e-7;
* twelve six-decimal table entries are forced and the two daggered entries
  really straddle their half-unit rounding boundary;
* each supplied square-root enclosure follows from the exact rational input
  intervals and the 20-decimal bounds on pi used by mathlib;
* exact rational interval propagation for the leading, second-order, and
  third-order relative residuals; and
* the three displayed sigma^4-scaled second-order residual enclosures.

The checker is fail-closed: malformed schemas, nonpositive denominators,
missing rows, or a failed containment raise an exception and return nonzero.
It checks post-processing only; it does not prove that the analytic quantities
lie in the input density/sigma/S4/S6 intervals.
"""

from __future__ import annotations

import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path
from typing import Iterable, NamedTuple


class Interval(NamedTuple):
    lo: Fraction
    hi: Fraction

    def checked(self, label: str) -> "Interval":
        require(self.lo <= self.hi, f"reversed interval: {label}")
        return self


ZERO = Fraction(0)
ONE = Fraction(1)
HALF = Fraction(1, 2)

EXPECTED_DENSITY_KEYS = {
    (4, 0), (4, 1), (4, 2), (4, 3), (4, 8), (4, 20), (4, 100),
    (3, 0), (3, 1), (3, 2), (3, 3), (3, 8), (3, 20), (3, 60),
}
EXPECTED_DAGGER_KEYS = {(3, 1), (3, 60)}
EXPECTED_POSTPROCESS_CLAIMS = {
    (4, 8): {"relative_leading", "relative_second", "relative_third"},
    (4, 20): {
        "relative_leading", "relative_second", "relative_third",
        "sigma4_relative_second",
    },
    (4, 100): {
        "relative_leading", "relative_second", "relative_third",
        "sigma4_relative_second",
    },
    (3, 60): {
        "relative_leading", "relative_second", "relative_third",
        "sigma4_relative_second",
    },
}


def exact_keys(value: dict, expected: set[str], label: str) -> None:
    """Reject both omitted and silently ignored fields in a schema object."""
    require(isinstance(value, dict), f"{label}: expected an object")
    actual = set(value)
    require(actual == expected,
            f"{label}: fields differ (missing={sorted(expected-actual)}, "
            f"unknown={sorted(actual-expected)})")


def unique_object(pairs: list[tuple[str, object]]) -> dict:
    """JSON object hook which rejects duplicate keys instead of taking the last."""
    result: dict = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON field: {key}")
        result[key] = value
    return result


def parse_certificate(raw: bytes) -> dict:
    certificate = json.loads(raw, object_pairs_hook=unique_object)
    exact_keys(certificate,
               {"schema", "pi_interval", "density_rows", "postprocess_rows"},
               "certificate")
    require(certificate["schema"] == "weighted-races-density-postprocess-v1",
            "unknown certificate schema")
    require(isinstance(certificate["density_rows"], list),
            "density_rows: expected an array")
    require(isinstance(certificate["postprocess_rows"], list),
            "postprocess_rows: expected an array")
    return certificate


def q(value: str | int) -> Fraction:
    """Parse a JSON integer or decimal string exactly."""
    if isinstance(value, bool):
        raise TypeError(f"certificate numbers cannot be booleans: {value!r}")
    if isinstance(value, int):
        return Fraction(value)
    if not isinstance(value, str):
        raise TypeError(f"certificate numbers must be strings or integers: {value!r}")
    return Fraction(value)


def interval(values: Iterable[str], label: str) -> Interval:
    items = list(values)
    require(len(items) == 2, f"{label}: expected two endpoints")
    return Interval(q(items[0]), q(items[1])).checked(label)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def add(a: Interval, b: Interval) -> Interval:
    return Interval(a.lo + b.lo, a.hi + b.hi)


def neg(a: Interval) -> Interval:
    return Interval(-a.hi, -a.lo)


def sub(a: Interval, b: Interval) -> Interval:
    return add(a, neg(b))


def mul(a: Interval, b: Interval) -> Interval:
    products = (a.lo * b.lo, a.lo * b.hi, a.hi * b.lo, a.hi * b.hi)
    return Interval(min(products), max(products))


def reciprocal(a: Interval, label: str) -> Interval:
    require(a.lo > 0, f"{label}: reciprocal interval is not strictly positive")
    return Interval(ONE / a.hi, ONE / a.lo)


def div(a: Interval, b: Interval, label: str) -> Interval:
    return mul(a, reciprocal(b, label))


def scale(a: Interval, scalar: Fraction) -> Interval:
    return mul(a, Interval(scalar, scalar))


def pow_nat(a: Interval, exponent: int, label: str) -> Interval:
    require(exponent >= 0, f"{label}: negative exponent")
    if exponent == 0:
        return Interval(ONE, ONE)
    if a.lo >= 0:
        return Interval(a.lo**exponent, a.hi**exponent)
    if a.hi <= 0 and exponent % 2 == 1:
        return Interval(a.lo**exponent, a.hi**exponent)
    values = (a.lo**exponent, a.hi**exponent)
    return Interval(ZERO if a.lo <= 0 <= a.hi else min(values), max(values))


def constant(value: Fraction) -> Interval:
    return Interval(value, value)


def correction2(sigma2: Interval, s4: Interval) -> Interval:
    # 1 - 1/(6 sigma^2) - 3 S4/(64 sigma^4), where this script's
    # `sigma2` is the paper's sigma^2 and therefore sigma^4 = sigma2^2.
    sigma4 = pow_nat(sigma2, 2, "sigma4")
    first = reciprocal(scale(sigma2, q(6)), "6 sigma2")
    fourth = div(scale(s4, q(3)), scale(sigma4, q(64)), "64 sigma4")
    return sub(sub(constant(ONE), first), fourth)


def correction3(sigma2: Interval, s4: Interval, s6: Interval) -> Interval:
    # C3 = C2 + 1/(40 s^2) + 5 S4/(128 s^3)
    #              - 5 S6/(192 s^3) + 105 S4^2/(8192 s^4), s=sigma^2.
    s2 = pow_nat(sigma2, 2, "sigma2^2")
    s3 = pow_nat(sigma2, 3, "sigma2^3")
    s4pow = pow_nat(sigma2, 4, "sigma2^4")
    a = reciprocal(scale(s2, q(40)), "40 sigma2^2")
    b = div(scale(s4, q(5)), scale(s3, q(128)), "128 sigma2^3")
    c = div(scale(s6, q(5)), scale(s3, q(192)), "192 sigma2^3")
    d = div(scale(pow_nat(s4, 2, "S4^2"), q(105)),
            scale(s4pow, q(8192)), "8192 sigma2^4")
    return add(sub(add(correction2(sigma2, s4), a), c), add(b, d))


def assert_claim(actual: Interval, claim: dict[str, str], label: str) -> None:
    center = q(claim["center"])
    radius = q(claim["radius"])
    require(radius >= 0, f"{label}: negative claim radius")
    require(center - radius <= actual.lo,
            f"{label}: lower endpoint escapes claim ({actual.lo} < {center-radius})")
    require(actual.hi <= center + radius,
            f"{label}: upper endpoint escapes claim ({actual.hi} > {center+radius})")


def check_rounding(rows: list[dict]) -> tuple[int, int]:
    require(len(rows) == 14, "expected exactly fourteen density rows")
    for index, row in enumerate(rows):
        require(isinstance(row, dict), f"density row {index}: expected an object")
        allowed = {"q", "m", "density", "rounded6", "alternate6"}
        require(set(row) <= allowed,
                f"density row {index}: unknown fields {sorted(set(row)-allowed)}")
        require({"q", "m", "density", "rounded6"} <= set(row),
                f"density row {index}: missing required field")
        require(type(row["q"]) is int and type(row["m"]) is int,
                f"density row {index}: q and m must be integers")
    keys = {(r["q"], r["m"]) for r in rows}
    require(len(keys) == 14, "duplicate density row")
    require(keys == EXPECTED_DENSITY_KEYS,
            f"density row keys differ from manuscript table: {sorted(keys)}")
    fixed = ambiguous = 0
    half_unit = Fraction(1, 2_000_000)
    for row in rows:
        label = f"q={row['q']} m={row['m']}"
        density = interval(row["density"], f"{label} density")
        require(density.hi - density.lo < Fraction(2, 10_000_000),
                f"{label}: width is not below 2e-7")
        shown = q(row["rounded6"])
        alternate = row.get("alternate6")
        if (row["q"], row["m"]) not in EXPECTED_DAGGER_KEYS:
            require("alternate6" not in row,
                    f"{label}: only the two manuscript dagger rows may be ambiguous")
            require(shown - half_unit <= density.lo,
                    f"{label}: interval escapes lower rounding bin")
            require(density.hi < shown + half_unit,
                    f"{label}: interval escapes upper rounding bin")
            fixed += 1
        else:
            require("alternate6" in row,
                    f"{label}: manuscript dagger row is missing alternate6")
            other = q(alternate)
            require(other - shown == Fraction(1, 1_000_000),
                    f"{label}: ambiguous outputs are not adjacent")
            boundary = shown + half_unit
            require(density.lo < boundary < density.hi,
                    f"{label}: daggered interval does not straddle boundary")
            require(shown - half_unit <= density.lo and density.hi < other + half_unit,
                    f"{label}: daggered interval permits a third rounded value")
            ambiguous += 1
    require((fixed, ambiguous) == (12, 2), "expected twelve fixed and two daggered rows")
    return fixed, ambiguous


def check_postprocess(certificate: dict) -> int:
    require(isinstance(certificate, dict), "certificate: expected an object")
    require("density_rows" in certificate and "pi_interval" in certificate
            and "postprocess_rows" in certificate,
            "certificate: missing post-processing input")
    check_rounding(certificate["density_rows"])
    density_by_key = {
        (row["q"], row["m"]): interval(row["density"], "density")
        for row in certificate["density_rows"]
    }
    pi = interval(certificate["pi_interval"], "pi")
    require(pi == Interval(q("3.14159265358979323846"),
                           q("3.14159265358979323847")),
            "pi interval must be the pair proved by mathlib pi_gt_d20/pi_lt_d20")
    rows = certificate["postprocess_rows"]
    require(len(rows) == 4, "expected exactly four post-processing rows")
    for index, row in enumerate(rows):
        exact_keys(row,
                   {"q", "m", "sigma2", "s4", "s6",
                    "sqrt_2_pi_sigma2", "claims"},
                   f"post-processing row {index}")
        require(type(row["q"]) is int and type(row["m"]) is int,
                f"post-processing row {index}: q and m must be integers")
        require(isinstance(row["claims"], dict),
                f"post-processing row {index}: claims must be an object")
    row_keys = {(r["q"], r["m"]) for r in rows}
    require(len(row_keys) == 4, "duplicate post-processing row")
    require(row_keys == set(EXPECTED_POSTPROCESS_CLAIMS),
            f"post-processing row keys differ from manuscript table: {sorted(row_keys)}")

    for row in rows:
        key = (row["q"], row["m"])
        label = f"q={key[0]} m={key[1]}"
        require(key in density_by_key, f"{label}: missing density input")
        density = density_by_key[key]
        sigma2 = interval(row["sigma2"], f"{label} sigma2")
        s4 = interval(row["s4"], f"{label} S4")
        s6 = interval(row["s6"], f"{label} S6")
        root = interval(row["sqrt_2_pi_sigma2"], f"{label} sqrt")
        require(sigma2.lo > 0 and s4.lo > 0 and s6.lo > 0 and root.lo > 0,
                f"{label}: nonpositive analytic input")

        # These two rational inequalities prove the supplied interval encloses
        # sqrt(2*pi*sigma2), assuming pi and sigma2 lie in their source balls.
        require(root.lo**2 <= 2 * pi.lo * sigma2.lo,
                f"{label}: false lower square-root certificate")
        require(2 * pi.hi * sigma2.hi <= root.hi**2,
                f"{label}: false upper square-root certificate")

        delta_minus_half = sub(density, constant(HALF))
        require(delta_minus_half.lo > 0, f"{label}: residual numerator not positive")
        numerator = mul(delta_minus_half, root)
        c2 = correction2(sigma2, s4)
        c3 = correction3(sigma2, s4, s6)
        require(c2.lo > 0 and c3.lo > 0, f"{label}: correction interval not positive")

        results = {
            "relative_leading": sub(numerator, constant(ONE)),
            "relative_second": sub(div(numerator, c2, f"{label} C2"), constant(ONE)),
            "relative_third": sub(div(numerator, c3, f"{label} C3"), constant(ONE)),
        }
        results["sigma4_relative_second"] = mul(
            results["relative_second"], pow_nat(sigma2, 2, f"{label} sigma4"))

        claims = row["claims"]
        require(set(claims) == EXPECTED_POSTPROCESS_CLAIMS[key],
                f"{label}: claim set differs from manuscript table")
        for name, claim in claims.items():
            exact_keys(claim, {"center", "radius"}, f"{label} {name} claim")
            assert_claim(results[name], claim, f"{label} {name}")

    return len(rows)


def main() -> int:
    path = Path(__file__).with_name("density_postprocess_certificate.json")
    raw = path.read_bytes()
    certificate = parse_certificate(raw)
    fixed, ambiguous = check_rounding(certificate["density_rows"])
    processed = check_postprocess(certificate)
    print(f"certificate sha256: {hashlib.sha256(raw).hexdigest()}")
    print(f"rounding: PASS ({fixed} fixed, {ambiguous} daggered, 14 widths < 2e-7)")
    print(f"residual propagation: PASS ({processed} rows; leading/second/third)")
    print("scaled second-order residuals: PASS (3 rows)")
    print("trust boundary: input analytic intervals assumed; all post-processing exact")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
