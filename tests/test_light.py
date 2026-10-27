import json
import os
import tempfile
import unittest
import zipfile

from _load import SKILLS_DIR, load, example

deck = load("launchproof-light", "deck")


def sample(**change):
    with open(example("launchproof-light", "example.deck.json"), encoding="utf-8") as fh:
        d = json.load(fh)
    d.update(change)
    return d


def board(scores, votes):
    return [{"person": "P%d" % i, "lens": "L", "score": s, "vote": v} for i, (s, v) in enumerate(zip(scores, votes))]


class Verdict(unittest.TestCase):
    def test_example_is_go_with_conditions(self):
        v = deck.verdict(sample())
        self.assertEqual((v["verdict"], v["score"]), ("Go with conditions", 62))
        self.assertEqual(v["votes"], {"FUND": 1, "FUND IF": 3, "PASS": 1})

    def test_go_needs_score_votes_and_no_kill_shot(self):
        strong = board([8, 8, 7, 7, 8], ["FUND", "FUND", "FUND IF", "FUND IF", "PASS"])
        self.assertEqual(deck.verdict({"board": strong, "risks": []})["verdict"], "Go")
        self.assertEqual(deck.verdict({"board": strong, "risks": [{"risk": "x", "severity": 1}]})["verdict"],
                         "Go with conditions")

    def test_three_passes_is_rethink(self):
        b = board([8, 8, 8, 8, 8], ["FUND", "FUND", "PASS", "PASS", "PASS"])
        self.assertEqual(deck.verdict({"board": b})["verdict"], "Rethink")

    def test_low_score_is_rethink(self):
        b = board([4, 4, 5, 4, 5], ["FUND IF"] * 5)
        self.assertEqual(deck.verdict({"board": b})["verdict"], "Rethink")

    def test_bad_votes_are_refused(self):
        with self.assertRaises(deck.DeckError):
            deck.verdict({"board": board([7], ["MAYBE"])})


class Quotes(unittest.TestCase):
    def test_example_quotes_are_in_the_bank(self):
        self.assertEqual(deck.check_quotes(sample()), [])

    def test_an_invented_quote_is_caught(self):
        d = sample()
        d["board"][0]["quote"] = "Always be closing."
        self.assertEqual(deck.check_quotes(d), ["Alex Hormozi"])

    def test_board_files_match_the_full_board(self):
        for name in ("lenses.md", "quotes.md"):
            with open(os.path.join(SKILLS_DIR, "launchproof-board", name), encoding="utf-8") as a, \
                    open(os.path.join(SKILLS_DIR, "launchproof-light", name), encoding="utf-8") as b:
                self.assertEqual(a.read(), b.read(), name)


class Pptx(unittest.TestCase):
    def test_builds_an_eleven_slide_deck(self):
        v, slides = deck.build(sample())
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "b.pptx")
            deck.write_pptx(slides, path, "Northlight")
            with zipfile.ZipFile(path) as z:
                names = z.namelist()
                self.assertIn("ppt/presentation.xml", names)
                self.assertEqual(sum(1 for n in names if n.startswith("ppt/slides/slide")), 11)
                self.assertIn("Go with conditions", z.read("ppt/slides/slide1.xml").decode("utf-8"))
                self.assertIn("Make people an offer so good", z.read("ppt/slides/slide5.xml").decode("utf-8"))

    def test_text_is_escaped(self):
        d = sample(idea="R&D <lab>")
        _, slides = deck.build(d)
        self.assertIn("R&amp;D &lt;lab&gt;", slides[0].xml())


if __name__ == "__main__":
    unittest.main()
