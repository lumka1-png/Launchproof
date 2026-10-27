#!/usr/bin/env python3
"""IdeaGauge, the Business Idea Evaluator, for launchproof-score. Standard library only, no network.

Scores an idea exactly the way the IdeaGauge app does (criteria.json in this
folder is generated from the app's own criteria model):

    33 built-in criteria, 0 to 100, in two sections:
        Business Analysis (19)  and  Personal Fit (14)
    plus Your Own Criteria: 3 editable defaults and any the founder adds
    weights  x3 critical, x2 important, x1 supporting
    a section score is the weighted mean of its scored criteria
    the overall score is the weighted mean of ALL scored criteria, own ones included
    every score is rounded half up, as the app does

    verdict (in this order)
        Strong, build it               overall >= 75, Business >= 55, Personal >= 50
        Workable, proceed with focus   overall >= 60, Business >= 55, Personal >= 50
        Score passes, but a gate fails overall >= 60, a section under its minimum
        Needs work                     overall >= 45
        Back to the drawing board      under 45

Launchproof adds one thing: every criterion can carry the founder's own score
("self") and a checked score ("verified") where Claude disagreed, with a reason.
The tool reports the app's verdict on the self scores AND on the checked
scores; Gate 1 uses the checked ones. The gap between the two is the optimism
to test for.

    python3 evaluator.py template --idea "Moss Matcha Bar" > launchproof/score.json
    python3 evaluator.py import ideagauge-export.json --idea "Moss" > launchproof/score.json
    python3 evaluator.py from-list "70,80,65,..." --idea "Moss"  # 33 numbers, the app's order
    python3 evaluator.py score launchproof/score.json --out launchproof/score.md
    python3 evaluator.py score launchproof/score.json --check     # exit 0 if Gate 1 passes

The input (launchproof/score.json):

    idea         the idea's name;  pitch  one line (optional)
    scores       {key: {"self": 70, "verified": 55, "note": "why"}}  or simply {key: 70}
    removed_own  default own criteria the founder removed (as in the app)
    custom       [{"key", "q", "w", "self", "verified", "note"}]  the founder's own criteria
"""

import argparse
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TIERS = {"strong": "Strong, build it", "pass": "Workable, proceed with focus",
         "gate": "Score passes, but a gate fails", "work": "Needs work", "fail": "Back to the drawing board"}


class ScoreError(Exception):
    pass


def load_criteria(path=None):
    with open(path or os.path.join(HERE, "criteria.json"), encoding="utf-8") as fh:
        return json.load(fh)


def js_round(x):
    """Math.round: halves go up."""
    return int(math.floor(x + 0.5))


def _value(v, field):
    if isinstance(v, (int, float)) and not isinstance(v, bool):
        return float(v) if field == "self" else None
    if isinstance(v, dict) and v.get(field) is not None:
        return float(v[field])
    return None


def criteria_for(spec, crit):
    """The criteria list for this idea: built-ins, minus removed own defaults, plus custom ones."""
    removed = set(spec.get("removed_own") or [])
    out = [dict(c) for c in crit["criteria"] if not (c["sec"] == "own" and c["key"] in removed)]
    for c in spec.get("custom") or []:
        if not c.get("key") or c.get("w") not in (1, 2, 3):
            raise ScoreError("custom criteria need a key and a weight of 1, 2 or 3: %r" % c)
        out.append({"key": c["key"], "sec": "own", "w": c["w"], "q": c.get("q") or c["key"], "custom": True})
    return out


def _weighted(rows, field):
    rows = [r for r in rows if r[field] is not None]
    if not rows:
        return None
    return js_round(sum(r[field] * r["w"] for r in rows) / float(sum(r["w"] for r in rows)))


def verdict(o, b, m, p):
    if o is None:
        return "draft"
    gates_ok = b is not None and m is not None and b >= p["biz"] and m >= p["me"]
    if o >= p["strong"] and gates_ok:
        return "strong"
    if o >= p["overall"] and gates_ok:
        return "pass"
    if o >= p["overall"]:
        return "gate"
    return "work" if o >= 45 else "fail"


def _result(rows, field, crit):
    p = crit["pass"]
    secs = {s: _weighted([r for r in rows if r["sec"] == s], field) for s in ("biz", "me", "own")}
    o = _weighted(rows, field)
    tier = verdict(o, secs["biz"], secs["me"], p)
    reasons = []
    if o is not None and o < p["overall"]:
        reasons.append("overall %d is under %d" % (o, p["overall"]))
    if secs["biz"] is not None and secs["biz"] < p["biz"]:
        reasons.append("Business Analysis %d is under the %d minimum" % (secs["biz"], p["biz"]))
    if secs["me"] is not None and secs["me"] < p["me"]:
        reasons.append("Personal Fit %d is under the %d minimum" % (secs["me"], p["me"]))
    by_key = {r["key"]: r for r in rows}
    radar = []
    for g in crit["radar"]:
        mine = [by_key[k] for k in g["keys"] if k in by_key and by_key[k][field] is not None]
        radar.append((g["name"], _weighted(mine, field) if mine else 0))
    return {"overall": o, "biz": secs["biz"], "me": secs["me"], "own": secs["own"], "tier": tier,
            "verdict": TIERS.get(tier, "Draft"), "pass": tier in ("strong", "pass"), "reasons": reasons, "radar": radar}


def analyse(spec, crit=None):
    crit = crit or load_criteria()
    scores = dict(spec.get("scores") or {})
    for c in spec.get("custom") or []:
        if c.get("key") and c["key"] not in scores and (c.get("self") is not None or c.get("verified") is not None):
            scores[c["key"]] = {k: c.get(k) for k in ("self", "verified", "note")}
    clist = criteria_for(spec, crit)
    known = {c["key"] for c in clist}
    unknown = sorted(set(scores) - known)
    if unknown:
        raise ScoreError("unknown criteria: %s (see criteria.json)" % ", ".join(unknown))
    missing = [c["key"] for c in clist if c["sec"] != "own" and _value(scores.get(c["key"]), "self") is None
               and _value(scores.get(c["key"]), "verified") is None]
    if missing:
        raise ScoreError("no score for %d built-in criteria: %s" % (len(missing), ", ".join(missing)))
    rows = []
    for c in clist:
        v = scores.get(c["key"])
        s, ver = _value(v, "self"), _value(v, "verified")
        for x in (s, ver):
            if x is not None and not 0 <= x <= 100:
                raise ScoreError("%s: %s is outside 0 to 100" % (c["key"], x))
        if s is None and ver is None:
            continue  # an own criterion left unscored is skipped, as in the app
        rows.append(dict(c, self=s, verified=ver, used=ver if ver is not None else s,
                         note=(v.get("note") if isinstance(v, dict) else None) or ""))
    checked = _result(rows, "used", crit)
    self_rows = [dict(r, self=r["self"] if r["self"] is not None else r["used"]) for r in rows]
    own = _result(self_rows, "self", crit)
    weak = sorted((r for r in rows if r["w"] == 3), key=lambda r: r["used"])[:3]
    return {
        "idea": spec.get("idea") or "Your idea", "pitch": spec.get("pitch") or "",
        "checked": checked, "self": own, "gate_pass": checked["pass"], "rows": rows,
        "adjusted": [(r["key"], r["q"], r["self"], r["verified"], r["note"]) for r in rows
                     if r["verified"] is not None and r["self"] is not None and r["verified"] != r["self"]],
        "weakest_critical": [(r["key"], r["q"], r["used"]) for r in weak],
        "red": [(r["key"], r["q"], r["used"]) for r in rows if r["used"] < 45],
        "strongest": [(r["key"], r["q"], r["used"]) for r in sorted(rows, key=lambda r: (-r["used"], -r["w"]))[:5]],
    }


def report(res, crit=None):
    crit = crit or load_criteria()
    c, s = res["checked"], res["self"]
    L = ["# %s · IdeaGauge evaluation" % res["idea"], ""]
    if res["pitch"]:
        L += ["_%s_" % res["pitch"], ""]
    L.append("**Checked score: %d / 100 · %s · Gate 1 %s**" % (
        c["overall"], c["verdict"], "passes" if c["pass"] else "does not pass"))
    if c["reasons"]:
        L += [""] + ["- ✗ %s" % t for t in c["reasons"]]
    if s["overall"] != c["overall"] or s["tier"] != c["tier"]:
        L += ["", "On the founder's own scores the app says %d / 100, %s. After checking: %d, %s. The difference is"
              " the optimism to test for." % (s["overall"], s["verdict"], c["overall"], c["verdict"])]
    L += ["", "| | founder's scores | checked |", "| --- | ---: | ---: |"]
    for k, label in (("overall", "Overall (weighted)"), ("biz", "Business Analysis (pass 55)"),
                     ("me", "Personal Fit (pass 50)"), ("own", "Your Own Criteria")):
        L.append("| %s | %s | %s |" % (label, "" if s[k] is None else s[k], "" if c[k] is None else c[k]))
    L += ["", "| dimension | score |", "| --- | ---: |"] + ["| %s | %d |" % d for d in c["radar"]]
    if res["adjusted"]:
        L += ["", "## Scores changed after checking", "", "| criterion | founder | checked | why |", "| --- | ---: | ---: | --- |"]
        for _, q, a, b, note in res["adjusted"]:
            L.append("| %s | %.0f | %.0f | %s |" % (q, a, b, note.replace("|", "/")))
    L += ["", "## Weakest critical (x3) criteria", ""] + ["- %s: %.0f" % (q, v) for _, q, v in res["weakest_critical"]]
    if res["red"]:
        L += ["", "## In the red (under 45)", ""] + ["- %s: %.0f" % (q, v) for _, q, v in res["red"]]
    L += ["", "## Strongest", ""] + ["- %s: %.0f" % (q, v) for _, q, v in res["strongest"]]
    for sec in ("biz", "me", "own"):
        rows = [r for r in res["rows"] if r["sec"] == sec]
        if not rows:
            continue
        L += ["", "## %s" % crit["sections"][sec]["title"], "", "| # | criterion | weight | founder | checked |",
              "| ---: | --- | ---: | ---: | ---: |"]
        for r in rows:
            L.append("| %s | %s%s | x%d | %s | %s |" % (
                r.get("n", ""), r["q"], " (yours)" if r.get("custom") else "", r["w"],
                "" if r["self"] is None else "%.0f" % r["self"], "" if r["verified"] is None else "%.0f" % r["verified"]))
    L += ["", "_Scores are judgments, not measurements. They decide what to test first, not whether the business"
          " will work. Scored with the IdeaGauge model from The Startup Blueprint by Derick van Vuren._"]
    return "\n".join(L) + "\n"


def template(idea, crit=None):
    crit = crit or load_criteria()
    return {"idea": idea, "pitch": "",
            "scores": {c["key"]: {"self": None, "verified": None, "note": ""} for c in crit["criteria"]},
            "removed_own": [], "custom": []}


def from_list(text, idea, crit=None):
    """33 numbers in the app's order (Business Analysis, then Personal Fit); 36 includes the own defaults."""
    crit = crit or load_criteria()
    vals = [t.strip() for t in text.replace(";", ",").replace("\n", ",").split(",") if t.strip()]
    core = [c for c in crit["criteria"] if c["sec"] != "own"]
    if len(vals) not in (len(core), len(crit["criteria"])):
        raise ScoreError("expected %d numbers (or %d with the own criteria), got %d"
                         % (len(core), len(crit["criteria"]), len(vals)))
    spec = template(idea, crit)
    for c, v in zip(crit["criteria"], vals):
        spec["scores"][c["key"]]["self"] = float(v)
    return spec


def import_app(path, idea=None, crit=None):
    """Read an IdeaGauge export ({app, version, ideas}) and return score.json for one idea."""
    crit = crit or load_criteria()
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    ideas = data if isinstance(data, list) else data.get("ideas") or []
    if not ideas:
        raise ScoreError("no ideas in %s" % path)
    if idea:
        hits = [i for i in ideas if (i.get("name") or "").strip().lower() == idea.strip().lower()]
        if not hits:
            raise ScoreError("no idea called %r; the file has: %s" % (idea, ", ".join(i.get("name", "?") for i in ideas)))
        it = hits[0]
    elif len(ideas) == 1:
        it = ideas[0]
    else:
        raise ScoreError("the file has %d ideas; pick one with --idea: %s" % (
            len(ideas), ", ".join(i.get("name", "?") for i in ideas)))
    spec = template(it.get("name") or "Your idea", crit)
    spec["pitch"] = it.get("desc") or ""
    spec["removed_own"] = it.get("removedOwn") or []
    custom_keys = set()
    for c in it.get("custom") or []:
        spec["custom"].append({"key": c["key"], "q": c.get("q"), "w": c.get("w", 2), "self": None, "verified": None, "note": ""})
        custom_keys.add(c["key"])
    for k, v in (it.get("scores") or {}).items():
        if v is None:
            continue
        if k in spec["scores"]:
            spec["scores"][k]["self"] = float(v)
        elif k in custom_keys:
            next(c for c in spec["custom"] if c["key"] == k)["self"] = float(v)
    for k in spec["removed_own"]:
        spec["scores"].pop(k, None)
    return spec


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    t = sub.add_parser("template", help="print a blank score.json")
    t.add_argument("--idea", default="Your idea")
    fl = sub.add_parser("from-list", help="score.json from the app's scores, in the app's order")
    fl.add_argument("numbers")
    fl.add_argument("--idea", default="Your idea")
    im = sub.add_parser("import", help="score.json from an IdeaGauge export file")
    im.add_argument("path")
    im.add_argument("--idea")
    s = sub.add_parser("score", help="score a score.json")
    s.add_argument("path")
    s.add_argument("--out")
    s.add_argument("--json", action="store_true")
    s.add_argument("--check", action="store_true", help="exit 0 only if Gate 1 passes")
    a = ap.parse_args(argv)
    try:
        if a.cmd in ("template", "from-list", "import"):
            spec = (template(a.idea) if a.cmd == "template" else
                    from_list(a.numbers, a.idea) if a.cmd == "from-list" else import_app(a.path, a.idea))
            print(json.dumps(spec, indent=1, ensure_ascii=False))
            return 0
        with open(a.path, encoding="utf-8") as fh:
            res = analyse(json.load(fh))
    except (ScoreError, OSError, ValueError) as e:
        print("error: %s" % e, file=sys.stderr)
        return 2
    c = res["checked"]
    if a.json:
        print(json.dumps(res, indent=1, ensure_ascii=False))
    elif a.check:
        print("Score %d · %s · Gate 1 %s" % (c["overall"], c["verdict"], "passes" if c["pass"] else "fails"))
        for t in c["reasons"]:
            print("  ✗ %s" % t)
    else:
        text = report(res)
        if a.out:
            with open(a.out, "w", encoding="utf-8") as fh:
                fh.write(text)
            print("Score %d (%s). Wrote %s" % (c["overall"], c["verdict"], a.out))
        else:
            print(text)
    return 0 if (res["gate_pass"] or not a.check) else 1


if __name__ == "__main__":
    sys.exit(main())
