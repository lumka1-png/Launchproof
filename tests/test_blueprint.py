import json
import os
import re
import shutil
import tempfile
import unittest

from _load import load, example

bp = load("launchproof-blueprint", "blueprint")
ev = load("launchproof-score", "evaluator")
STEPS = bp.load_steps()


class Blueprint(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.d)

    def write(self, name, obj):
        path = os.path.join(self.d, name)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(obj if isinstance(obj, str) else json.dumps(obj))

    def read(self, name):
        with open(os.path.join(self.d, name), encoding="utf-8") as fh:
            return json.load(fh)

    def tick_all(self):
        bp.write_checklist(self.d)
        path = os.path.join(self.d, "checklist.md")
        with open(path) as fh:
            text = fh.read().replace("- [ ]", "- [x]")
        with open(path, "w") as fh:
            fh.write(text)

    def gate1(self, score=70):
        self.write("idea.md", "# Moss Matcha Bar\n\n- What it is: a walk-in matcha bar.\n")
        self.write("fit.md", "# Fit\n")
        self.write("score.json", {"idea": "Moss", "scores": {c["key"]: score for c in ev.load_criteria()["criteria"]}})
        self.write("board.json", {"members": [{"lens": l, "score": 7, "vote": "FUND IF"} for l in
                                              ("offers", "monopoly", "demand", "leverage", "inversion")],
                                  "kill_criteria": ["fewer than 20 waitlist signups in 30 days"]})
        self.write("threats.json", {"threats": [{"id": "M1", "vector": "market", "score": 2,
                                                 "defense": {"detect": "d", "respond": "r", "mitigate": "m"},
                                                 "post_score": 4}]})
        self.write("evidence.json", {"problem_conversations": 12, "customer_interviews": 22,
                                     "personal_runway_months": 9, "cash_available": 60000,
                                     "real_test": {"what": "pre-orders", "unit": "pre-orders",
                                                   "success_line": 50, "result": 63}})

    def everything(self):
        self.gate1()
        with open(example("launchproof-cfo", "example.json")) as fh:
            self.write("numbers.json", fh.read())
        self.write("panel/results.json", {"buys": 40, "passes": 60, "answered": 100, "buy_rate": 0.4,
                                          "by_segment": [["office", 50, 0.5], ["students", 50, 0.3]]})
        for i in range(10):
            self.write("panel/answers/b%02d.json" % i, {"price_too_cheap": 3 + i * 0.1, "price_cheap": 4.5 + i * 0.1,
                                                        "price_expensive": 7 + i * 0.1, "price_too_expensive": 9 + i * 0.1})
        self.write("five-forces.json", {"rivalry": "high", "new_entrants": "medium", "suppliers": "low",
                                        "buyers": "medium", "substitutes": "high", "gap_found": True})
        for f in ("value-proposition.md", "competitors.md", "pricing.md", "ops.md", "cfo.md", "brand.md",
                  "business-model-canvas.md", "marketing.md", "launch.md", "growth.md", "team.md"):
            self.write(f, "# %s\n\nwritten" % f)

    def test_fourteen_steps_in_four_gates(self):
        self.assertEqual(sorted(s["n"] for s in STEPS["steps"]), list(range(1, 15)))
        self.assertEqual(sorted(n for g in STEPS["gates"] for n in g["steps"]), list(range(1, 15)))
        ids = [i["id"] for s in STEPS["steps"] for i in s["items"]]
        self.assertEqual(len(ids), len(set(ids)))

    def test_empty_folder_is_open_not_failed(self):
        res = bp.evaluate(self.d)
        self.assertEqual(res["reached"], 0)
        self.assertTrue(all(g["status"] == "open" for g in res["gates"]))

    def test_gate1_needs_the_checklist_ticked(self):
        self.gate1()
        self.assertEqual(bp.evaluate(self.d)["gates"][0]["status"], "open")
        self.tick_all()
        res = bp.evaluate(self.d)
        self.assertEqual(res["gates"][0]["status"], "pass")
        self.assertEqual(res["reached"], 1)

    def test_a_low_score_fails_gate1(self):
        self.gate1(score=40)
        self.tick_all()
        res = bp.evaluate(self.d)
        self.assertEqual(res["steps"][1]["status"], "fail")
        self.assertEqual(res["gates"][0]["status"], "fail")

    def test_everything_passes_all_four_gates(self):
        self.everything()
        self.tick_all()
        res, v, text = bp.compile_plan(self.d)
        self.assertEqual(res["reached"], 4, [(n, s["status"], s["checks"]) for n, s in res["steps"].items()
                                             if s["status"] != "pass"])
        self.assertEqual(v, "Profitable")
        self.assertTrue(text.startswith("# Moss Matcha Bar · Business plan"))
        self.assertIn("All four gates passed", text)

    def test_no_real_test_holds_gate3(self):
        self.everything()
        ev_ = self.read("evidence.json")
        ev_["real_test"]["result"] = None
        self.write("evidence.json", ev_)
        self.tick_all()
        res = bp.evaluate(self.d)
        self.assertEqual(res["reached"], 2)
        self.assertEqual(res["gates"][2]["status"], "open")
        self.assertIn("Do not spend", bp.action_plan(res))

    def test_a_missed_real_test_fails_gate3(self):
        self.everything()
        ev_ = self.read("evidence.json")
        ev_["real_test"]["result"] = 12
        self.write("evidence.json", ev_)
        self.tick_all()
        self.assertEqual(bp.evaluate(self.d)["gates"][2]["status"], "fail")

    def test_too_little_cash_fails_gate4(self):
        self.everything()
        ev_ = self.read("evidence.json")
        ev_["cash_available"] = 10000
        self.write("evidence.json", ev_)
        self.tick_all()
        res = bp.evaluate(self.d)
        self.assertEqual(res["steps"][13]["status"], "fail")
        self.assertEqual(res["reached"], 3)

    def test_checklist_keeps_ticks(self):
        bp.write_checklist(self.d)
        path = os.path.join(self.d, "checklist.md")
        with open(path) as fh:
            text = fh.read()
        text = re.sub(r"- \[ \] 1\.2 ", "- [x] 1.2 ", text)
        with open(path, "w") as fh:
            fh.write(text)
        bp.write_checklist(self.d)
        self.assertTrue(bp.read_ticks(self.d)["1.2"])
        self.assertFalse(bp.read_ticks(self.d)["1.1"])


if __name__ == "__main__":
    unittest.main()
