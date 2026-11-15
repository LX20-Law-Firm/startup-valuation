import json
import math
import unittest
from pathlib import Path

from startup_valuation.core import Scenario, berkus, dcf, first_chicago, scorecard, venture_capital


class ValuationTests(unittest.TestCase):
    def test_documented_examples(self):
        examples = json.loads((Path(__file__).parents[1] / "examples.json").read_text())
        self.assertEqual(berkus(**examples["berkus"]), 1_000_000)
        self.assertAlmostEqual(scorecard(**examples["scorecard"]), 2_020_000)
        vc = venture_capital(**examples["venture_capital"])
        self.assertEqual(vc.post_money, 5_120_000)
        self.assertEqual(vc.pre_money, 4_120_000)
        self.assertEqual(vc.ownership, 0.1953125)
        self.assertAlmostEqual(dcf(**examples["dcf"]), 1181.8181818181818)
        fc = examples["first_chicago"]
        self.assertEqual(first_chicago([Scenario(**s) for s in fc["scenarios"]], 0), 1100)

    def test_negative_flows_and_terminal_timing(self):
        self.assertEqual(dcf([-100, 200], 0, 300), 400)
        self.assertAlmostEqual(dcf([0, 0], 0.1, 121), 100)
        self.assertEqual(berkus([0] * 5), 0)

    def test_invalid_inputs(self):
        cases = [
            lambda: berkus([1] * 4),
            lambda: berkus([1, 2, 3, 4, -1]),
            lambda: scorecard(100, [0.3, 0.3], [1, 1]),
            lambda: scorecard(100, [1], []),
            lambda: scorecard(100, [1], [-1]),
            lambda: venture_capital(1, 0, 1, 2),
            lambda: venture_capital(0, 0, 1, 0),
            lambda: venture_capital(1, 0, 0, 0),
            lambda: dcf([], 0),
            lambda: dcf([1], -1),
            lambda: dcf([1], 0, -1),
            lambda: first_chicago([Scenario(1, [1])], 0),
            lambda: first_chicago([Scenario(0.2, [1])] * 3, 0),
        ]
        for call in cases:
            with self.subTest(call=call), self.assertRaises(ValueError):
                call()

    def test_nonfinite_and_boolean(self):
        for value in [math.nan, math.inf, -math.inf, True, None, "bad"]:
            with self.subTest(value=value), self.assertRaises(ValueError):
                dcf([value], 0)
        with self.assertRaises(ValueError):
            dcf([1e308, 1e308], 0)
        with self.assertRaises(ValueError):
            dcf([1, 2], 1e308)

    def test_probability_and_weight_boundaries(self):
        self.assertEqual(
            first_chicago([Scenario(1, [20]), Scenario(0, [10]), Scenario(0, [30])], 0), 20
        )
        self.assertEqual(scorecard(500, [0, 1], [20, 2]), 1000)


if __name__ == "__main__":
    unittest.main()
