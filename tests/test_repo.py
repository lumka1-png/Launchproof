import json
import os
import re
import unittest

from _load import ROOT, SKILLS_DIR

SKILLS = ["launchproof", "launchproof-fit", "launchproof-score", "launchproof-board", "launchproof-redteam",
          "launchproof-competitors", "launchproof-consumer", "launchproof-pricing", "launchproof-offer",
          "launchproof-cfo", "launchproof-marketing", "launchproof-brand", "launchproof-ops", "launchproof-launch",
          "launchproof-blueprint"]
ABOUT = ("Fifteen free Claude skills that evaluate a business idea, test it before you spend, and turn it into a gated "
         "business plan: IdeaGauge scoring, a board on the Hormozi, Thiel, Priestley, Naval and Munger frameworks, a "
         "red team, 100 simulated buyers, a CFO and the 14-step Startup Blueprint. MIT.")


def frontmatter(path):
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    return (m.group(1) if m else ""), text


EM = chr(0x2014)  # built in code so this file does not trip its own check


def text_files():
    for base, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in (".git", "__pycache__")]
        for f in files:
            if f.endswith((".md", ".py", ".json", ".txt")) or f in ("LICENSE", ".gitignore"):
                yield os.path.join(base, f)


class Repo(unittest.TestCase):
    def test_fifteen_skill_folders(self):
        found = sorted(d for d in os.listdir(SKILLS_DIR) if os.path.isfile(os.path.join(SKILLS_DIR, d, "SKILL.md")))
        self.assertEqual(found, sorted(SKILLS))

    def test_frontmatter_name_and_description(self):
        for s in SKILLS:
            fm, text = frontmatter(os.path.join(SKILLS_DIR, s, "SKILL.md"))
            self.assertIn("name: %s\n" % s, fm + "\n", s)
            self.assertRegex(fm, r"description: ", s)
            self.assertGreater(len(fm), 300, "%s description is too thin" % s)
            self.assertGreater(len(text.splitlines()), 60, s)

    def test_tools_named_in_skills_exist(self):
        for s in SKILLS:
            _, text = frontmatter(os.path.join(SKILLS_DIR, s, "SKILL.md"))
            for tool in re.findall(r"\$\{CLAUDE_SKILL_DIR\}/([\w.\-/]+\.(?:py|md))", text):
                self.assertTrue(os.path.exists(os.path.normpath(os.path.join(SKILLS_DIR, s, tool))), "%s: %s" % (s, tool))

    def test_plugin_manifests(self):
        with open(os.path.join(ROOT, ".claude-plugin", "plugin.json")) as fh:
            plugin = json.load(fh)
        self.assertEqual(plugin["name"], "launchproof")
        self.assertEqual(plugin["description"], ABOUT)
        self.assertEqual(plugin["license"], "MIT")
        with open(os.path.join(ROOT, ".claude-plugin", "marketplace.json")) as fh:
            market = json.load(fh)
        self.assertEqual(market["name"], "launchproof")
        self.assertEqual(market["plugins"][0]["name"], "launchproof")
        self.assertEqual(market["plugins"][0]["source"], "./")

    def test_readme_carries_the_copy(self):
        with open(os.path.join(ROOT, "README.md"), encoding="utf-8") as fh:
            readme = " ".join(fh.read().split())
        self.assertTrue(readme.startswith("# Launchproof"))
        for line in (
            "**Test your business idea before you spend a dollar on it.**",
            "Paste this repo link into Claude and say `install skill`",
            "/plugin install launchproof@launchproof",
            "Daniel Priestley", "Naval Ravikant", "Poor Charlie's Almanack",
            "## Fine print", "The Startup Blueprint", "IdeaGauge",
        ):
            self.assertIn(line, readme)
        self.assertNotIn("Steve Jobs", readme)
        for s in SKILLS:
            self.assertIn("`skills/%s`" % s, readme)

    def test_board_has_five_lenses_and_no_product_lens(self):
        with open(os.path.join(SKILLS_DIR, "launchproof-board", "lenses.md"), encoding="utf-8") as fh:
            lenses = fh.read()
        for lens in ("Offers", "Monopoly", "Demand", "Leverage", "Inversion"):
            self.assertIn("## The %s lens" % lens, lenses)
        self.assertNotIn("Product lens", lenses)
        self.assertNotIn("Jobs", lenses)

    def test_examples_parse(self):
        for rel in ("launchproof-cfo/example.json", "launchproof-cfo/example-ai-consulting.json",
                    "launchproof-consumer/customer.example.json",
                    "launchproof-score/criteria.json", "launchproof-blueprint/steps.json"):
            with open(os.path.join(SKILLS_DIR, rel), encoding="utf-8") as fh:
                json.load(fh)

    def test_no_em_dashes(self):
        for path in text_files():
            with open(path, encoding="utf-8") as fh:
                self.assertNotIn(EM, fh.read(), os.path.relpath(path, ROOT))


if __name__ == "__main__":
    unittest.main()
