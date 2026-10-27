import json
import os
import tempfile
import unittest

from _load import ROOT, load

ev = load("launchproof-score", "evaluator")
CRIT = ev.load_criteria()
CORE = [c for c in CRIT["criteria"] if c["sec"] != "own"]


def flat(value, own=None):
    s = {c["key"]: value for c in CORE}
    if own is not None:
        s.update({c["key"]: own for c in CRIT["criteria"] if c["sec"] == "own"})
    return {"idea": "Test", "scores": s}


class Model(unittest.TestCase):
    def test_the_app_model(self):
        self.assertEqual(len(CORE), 33)
        self.assertEqual(sum(1 for c in CORE if c["sec"] == "biz"), 19)
        self.assertEqual(sum(1 for c in CORE if c["sec"] == "me"), 14)
        self.assertEqual(CRIT["pass"], {"overall": 60, "biz": 55, "me": 50, "strong": 75})
        self.assertTrue(all(c["w"] in (1, 2, 3) for c in CRIT["criteria"]))

    def test_matches_the_app_on_fifty_ideas(self):
        # computed by the IdeaGauge app's own JavaScript, ten per verdict tier
        with open(os.path.join(ROOT, "tests", "fixtures", "ideagauge_parity.json")) as fh:
            cases = json.load(fh)
        tiers = set()
        for c in cases:
            scores = {k: v for k, v in c["scores"].items() if k not in {x["key"] for x in c["custom"]}}
            custom = [dict(x, self=c["scores"].get(x["key"])) for x in c["custom"]]
            r = ev.analyse({"scores": scores, "removed_own": c["removed_own"], "custom": custom})["self"]
            self.assertEqual((r["overall"], r["biz"], r["me"], r["tier"]),
                             (c["app"]["overall"], c["app"]["biz"], c["app"]["me"], c["app"]["tier"]))
            tiers.add(r["tier"])
        self.assertEqual(tiers, {"strong", "pass", "gate", "work", "fail"})

    def test_rounds_half_up_like_javascript(self):
        self.assertEqual(ev.js_round(59.5), 60)
        self.assertEqual(ev.js_round(60.5), 61)


class Gate(unittest.TestCase):
    def test_workable_passes(self):
        r = ev.analyse(flat(65))
        self.assertEqual(r["checked"]["tier"], "pass")
        self.assertTrue(r["gate_pass"])

    def test_a_weak_section_blocks_a_high_total(self):
        spec = flat(80)
        for c in CORE:
            if c["sec"] == "me":
                spec["scores"][c["key"]] = 30
        r = ev.analyse(spec)["checked"]
        self.assertGreaterEqual(r["overall"], 60)
        self.assertEqual(r["tier"], "gate")
        self.assertIn("Personal Fit 30 is under the 50 minimum", r["reasons"])

    def test_checked_scores_decide_the_gate(self):
        spec = flat(66)
        for k in ("problem", "need", "valuable", "betterValue", "advantage", "income"):
            spec["scores"][k] = {"self": 66, "verified": 20, "note": "no evidence"}
        r = ev.analyse(spec)
        self.assertTrue(r["self"]["pass"])
        self.assertFalse(r["gate_pass"])
        self.assertEqual(len(r["adjusted"]), 6)

    def test_missing_core_scores_are_an_error(self):
        spec = flat(70)
        del spec["scores"]["need"]
        with self.assertRaises(ev.ScoreError):
            ev.analyse(spec)

    def test_own_criteria_count_in_the_overall(self):
        self.assertGreater(ev.analyse(flat(60, own=100))["checked"]["overall"], 60)


class Import(unittest.TestCase):
    def test_reads_an_ideagauge_export(self):
        scores = {c["key"]: 70 for c in CORE}
        scores.update({"freedom": 90, "mine": 40})
        export = {"app": "IdeaGauge", "version": 1, "ideas": [
            {"id": "a", "name": "Moss Matcha", "desc": "A matcha bar", "scores": scores,
             "removedOwn": ["membership"], "custom": [{"key": "mine", "q": "Near my home?", "w": 3}]}]}
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as fh:
            json.dump(export, fh)
        try:
            spec = ev.import_app(fh.name)
        finally:
            os.unlink(fh.name)
        self.assertEqual(spec["idea"], "Moss Matcha")
        self.assertNotIn("membership", spec["scores"])
        r = ev.analyse(spec)
        self.assertEqual(r["self"]["biz"], 70)
        self.assertTrue(any(x.get("custom") for x in r["rows"]))

    def test_from_list_uses_the_app_order(self):
        spec = ev.from_list(",".join(str(i) for i in range(33)), "x")
        self.assertEqual(spec["scores"]["novel"]["self"], 0)
        self.assertEqual(spec["scores"]["support"]["self"], 32)


if __name__ == "__main__":
    unittest.main()
