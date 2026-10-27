import unittest

from _load import load

th = load("launchproof-redteam", "threats")


def threat(tid, vector, score, post=None, defended=True):
    t = {"id": tid, "vector": vector, "attack": "a", "vulnerability": "v", "score": score, "rationale": "r"}
    if defended:
        t["defense"] = {"detect": "d", "respond": "r", "mitigate": "m", "cost": "$"}
        t["post_score"] = post
    return t


class Threats(unittest.TestCase):
    def test_defended_threats_pass(self):
        r = th.analyse({"threats": [threat("M1", "market", 2, 4), threat("L1", "legal", 5, defended=False)]})
        self.assertTrue(r["gate_pass"])
        self.assertEqual(r["pre_critical"], ["M1"])

    def test_still_critical_after_defense_fails(self):
        r = th.analyse({"threats": [threat("M1", "market", 1, 2)]})
        self.assertFalse(r["gate_pass"])
        self.assertEqual(r["open_kills"], ["M1"])

    def test_undefended_weakness_fails(self):
        r = th.analyse({"threats": [threat("P1", "product", 3, defended=False)]})
        self.assertEqual(r["undefended"], ["P1"])
        self.assertFalse(r["gate_pass"])

    def test_bad_input_is_refused(self):
        with self.assertRaises(th.ThreatError):
            th.analyse({"threats": [threat("X1", "weather", 3, 4)]})
        with self.assertRaises(th.ThreatError):
            th.analyse({"threats": [threat("M1", "market", 2, 4)], "cascades": [["M1", "Z9"]]})

    def test_report_lists_cascades(self):
        r = th.analyse({"threats": [threat("P1", "product", 2, 4), threat("N1", "narrative", 3, 4)],
                        "cascades": [["P1", "N1"]]})
        self.assertIn("→", th.report(r))


if __name__ == "__main__":
    unittest.main()
