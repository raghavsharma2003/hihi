#!/usr/bin/env python3
"""Adversarial tests for the exact post-processing checker."""

from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

import check_density_postprocess as checker


CERTIFICATE = Path(__file__).with_name("density_postprocess_certificate.json")


def load_certificate() -> dict:
    return json.loads(CERTIFICATE.read_text(encoding="utf-8"))


class FailClosedTests(unittest.TestCase):
    def test_pristine_certificate_passes(self) -> None:
        certificate = load_certificate()
        self.assertEqual(checker.check_rounding(certificate["density_rows"]), (12, 2))
        self.assertEqual(checker.check_postprocess(certificate), 4)

    def test_wrong_rounding_endpoint_is_rejected(self) -> None:
        certificate = load_certificate()
        bad = copy.deepcopy(certificate["density_rows"])
        bad[0]["density"][1] = "0.995929"
        with self.assertRaises(ValueError):
            checker.check_rounding(bad)

    def test_false_square_root_bound_is_rejected(self) -> None:
        certificate = load_certificate()
        certificate["postprocess_rows"][0]["sqrt_2_pi_sigma2"][0] = "14"
        with self.assertRaises(ValueError):
            checker.check_postprocess(certificate)

    def test_too_narrow_residual_claim_is_rejected(self) -> None:
        certificate = load_certificate()
        claim = certificate["postprocess_rows"][1]["claims"]["relative_second"]
        claim["radius"] = "0"
        with self.assertRaises(ValueError):
            checker.check_postprocess(certificate)

    def test_unproved_pi_interval_is_rejected(self) -> None:
        certificate = load_certificate()
        certificate["pi_interval"][0] = "3.14"
        with self.assertRaises(ValueError):
            checker.check_postprocess(certificate)

    def test_missing_residual_claim_is_rejected(self) -> None:
        certificate = load_certificate()
        del certificate["postprocess_rows"][0]["claims"]["relative_third"]
        with self.assertRaises(ValueError):
            checker.check_postprocess(certificate)

    def test_missing_scaled_claim_is_rejected(self) -> None:
        certificate = load_certificate()
        del certificate["postprocess_rows"][1]["claims"]["sigma4_relative_second"]
        with self.assertRaises(ValueError):
            checker.check_postprocess(certificate)

    def test_substituted_density_row_is_rejected(self) -> None:
        certificate = load_certificate()
        certificate["density_rows"][0]["m"] = 999
        with self.assertRaises(ValueError):
            checker.check_rounding(certificate["density_rows"])

    def test_substituted_postprocess_row_is_rejected(self) -> None:
        certificate = load_certificate()
        certificate["postprocess_rows"][0]["m"] = 999
        with self.assertRaises(ValueError):
            checker.check_postprocess(certificate)

    def test_unknown_nested_field_is_rejected(self) -> None:
        certificate = load_certificate()
        certificate["postprocess_rows"][0]["claims"]["relative_leading"]["ignored"] = "1"
        with self.assertRaises(ValueError):
            checker.check_postprocess(certificate)

    def test_duplicate_json_field_is_rejected(self) -> None:
        raw = b'{"schema":"a","schema":"b"}'
        with self.assertRaises(ValueError):
            checker.parse_certificate(raw)

    def test_boolean_number_is_rejected(self) -> None:
        with self.assertRaises(TypeError):
            checker.q(True)


if __name__ == "__main__":
    unittest.main()
