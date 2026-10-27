#!/usr/bin/env python3
"""The Blueprint gates and business plan for launchproof-blueprint. Standard library only, no network.

Turns everything the other Launchproof skills wrote into launchproof/ into the
14 steps of The Startup Blueprint (steps.json in this folder), grouped into four
money gates. Each gate says what the founder may spend once it passes:

    Gate 1  Worth testing               Steps 1, 2, 3       then: research only
    Gate 2  Worth a real-world test     Steps 5, 6, 7, 8    then: a small test budget
    Gate 3  Worth building              Steps 9, 10, 11     then: the startup budget
    Gate 4  Ready to launch and grow    Steps 4, 12-14      then: launch, legal, hiring

A step passes when every automatic check on it passes AND every must-do item on
its checklist is ticked. A check is computed from a file (score.json, board.json,
threats.json, numbers.json, panel/results.json, five-forces.json, evidence.json);
it is open when the file is not there yet and fails when the number misses the bar.
A gate passes when all its steps pass. Gates are passed in order.

The checklist lives in launchproof/checklist.md. This tool writes it, and keeps
the founder's ticks ([x]) every time it rewrites it.

    python3 blueprint.py --dir launchproof --check         # print the gates; exit 0 only if all four pass
    python3 blueprint.py --dir launchproof --checklist     # write or refresh launchproof/checklist.md
    python3 blueprint.py --dir launchproof                 # write business-plan.md and action-plan.md

The profitability verdict from the CFO's numbers is kept as well: Profitable,
Not yet (with the failing numbers) or Incomplete (no numbers yet).
"""

import argparse
import importlib.util
import json
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SKILLS = os.path.dirname(HERE)
PASS, FAIL, OPEN = "pass", "fail", "open"
MARK = {PASS: "✓", FAIL: "✗", OPEN: "○"}
TICK = re.compile(r"^\s*- \[([ xX])\] (\d+\.\d+)\b")
RUNWAY_SAFETY = 1.5  # the planning-fallacy safety factor from Blueprint Step 3
EXTRA_SECTIONS = [("plan-narrative.md", "The business plan"), ("business-model-canvas.md", "Business Model Canvas")]


def _tool(folder, name):
    path = os.path.join(SKILLS, folder, name + ".py")
    spec = importlib.util.spec_from_file_location("launchproof_" + name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _read(path):
    try:
        with open(path, encoding="utf-8") as fh:
            return fh.read().strip() or None
    except FileNotFoundError:
        return None


def _json(d, name):
    raw = _read(os.path.join(d, name))
    return json.loads(raw) if raw else None


def load_steps():
    with open(os.path.join(HERE, "steps.json"), encoding="utf-8") as fh:
        return json.load(fh)


def _money(v):
    return ("-$" if v < 0 else "$") + "{:,.0f}".format(abs(v))


def gather(d):
    """Read every input once. Tools that fail on bad input report the error as a failing check."""
    s = {"dir": d, "errors": {}}
    s["evidence"] = _json(d, "evidence.json") or {}
    for key, fname, folder, mod in (("score", "score.json", "launchproof-score", "evaluator"),
                                    ("threats", "threats.json", "launchproof-redteam", "threats"),
                                    ("numbers", "numbers.json", "launchproof-cfo", "unit_economics")):
        raw = _json(d, fname)
        s[key] = None
        if raw is not None:
            try:
                s[key] = _tool(folder, mod).analyse(raw)
            except Exception as e:  # each tool raises its own error type
                s["errors"][key] = str(e)
    s["board"] = _json(d, "board.json")
    s["panel"] = _json(d, os.path.join("panel", "results.json"))
    s["forces"] = _json(d, "five-forces.json")
    s["prices"] = None
    answers = os.path.join(d, "panel", "answers")
    if os.path.isdir(answers):
        vw = _tool("launchproof-pricing", "van_westendorp")
        try:
            rows, _ = vw.read(answers)
            s["prices"] = vw.analyse(rows)
        except Exception as e:
            s["errors"]["prices"] = str(e)
    return s


def _file(s, name, label, skill):
    if _read(os.path.join(s["dir"], name)):
        return PASS, "%s written (%s)." % (label, name)
    return OPEN, "%s not written yet: run /%s." % (label, skill)


def check(key, s, min_buy_rate=0.25):
    """Return (status, text) for one automatic check."""
    ev, n, sc = s["evidence"], s["numbers"], s["score"]
    if key in ("score_gate", "founder_group"):
        if "score" in s["errors"]:
            return FAIL, "score.json has a problem: %s." % s["errors"]["score"]
        if sc is None:
            return OPEN, "Not scored yet: run /launchproof-score."
        c = sc["checked"]
        if key == "score_gate":
            return (PASS if c["pass"] else FAIL), "IdeaGauge score %d, %s%s." % (
                c["overall"], c["verdict"], "" if c["pass"] else ": " + "; ".join(c["reasons"] or ["below Workable"]))
        return (PASS if c["me"] >= 50 else FAIL), "Personal Fit scores %d (the bar is 50)." % c["me"]
    if key in ("problem_conversations", "customer_interviews"):
        need = 10 if key == "problem_conversations" else 20
        what = "problem conversations" if key == "problem_conversations" else "customer interviews"
        v = ev.get(key)
        if v is None:
            return OPEN, "No %s logged in evidence.json yet (the bar is %d)." % (what, need)
        return (PASS if v >= need else FAIL), "%d real %s (the bar is %d)." % (v, what, need)
    if key == "fit_profile":
        return _file(s, "fit.md", "Founder profile", "launchproof-fit")
    if key == "personal_runway":
        if ev.get("keeps_income"):
            return PASS, "The founder keeps an income while starting."
        v = ev.get("personal_runway_months")
        if v is None:
            return OPEN, "Personal runway not logged in evidence.json."
        return (PASS if v >= 6 else FAIL), "%g months of personal living costs covered (the bar is 6, or keep an income)." % v
    if key == "board_vote":
        b = s["board"]
        if not b or not b.get("members"):
            return OPEN, "The board has not met: run /launchproof-board."
        votes = [m.get("vote", "").upper() for m in b["members"]]
        avg = sum(float(m.get("score", 0)) for m in b["members"]) / len(b["members"])
        passes = votes.count("PASS")
        ok = passes <= len(votes) // 2 and avg >= 5
        return (PASS if ok else FAIL), "Board: %d fund, %d fund if, %d pass; average %.1f of 10." % (
            votes.count("FUND"), votes.count("FUND IF"), passes, avg)
    if key == "kill_criteria":
        b = s["board"]
        if not b:
            return OPEN, "No kill criteria yet: the board writes them."
        k = b.get("kill_criteria") or []
        return (PASS if k else FAIL), ("%d kill criteria written before testing." % len(k)) if k else "No kill criteria written."
    if key == "redteam_gate":
        if "threats" in s["errors"]:
            return FAIL, "threats.json has a problem: %s." % s["errors"]["threats"]
        t = s["threats"]
        if t is None:
            return OPEN, "No red team yet: run /launchproof-redteam."
        if t["gate_pass"]:
            return PASS, "Red team: no threat still critical after the defenses."
        return FAIL, "Red team: still critical %s; no defense yet %s." % (
            ", ".join(t["open_kills"]) or "none", ", ".join(t["undefended"]) or "none")
    if key == "brand_file":
        return _file(s, "brand.md", "Brand and name checks", "launchproof-brand")
    if key == "value_prop":
        return _file(s, "value-proposition.md", "Value Proposition Canvas and statement", "launchproof-consumer")
    if key == "panel_buy_rate":
        p = s["panel"]
        if not p:
            return OPEN, "No buyer panel yet: run /launchproof-consumer."
        return (PASS if p["buy_rate"] >= min_buy_rate else FAIL), "%d of %d simulated buyers buy (%.0f%%, the bar is %.0f%%)." % (
            p["buys"], p["answered"], p["buy_rate"] * 100, min_buy_rate * 100)
    if key == "segments":
        p = s["panel"]
        if not p:
            return OPEN, "No segments tested yet: run /launchproof-consumer."
        segs = p.get("by_segment") or []
        if len(segs) < 2:
            return FAIL, "Only %d segment tested; compare at least 2 before choosing." % len(segs)
        best = segs[0]
        return PASS, "%d segments tested; the best is %s at %.0f%%." % (len(segs), best[0], best[2] * 100)
    if key == "five_forces":
        f = s["forces"]
        if not f:
            return OPEN, "No five-forces rating yet: run /launchproof-competitors."
        forces = ("rivalry", "new_entrants", "suppliers", "buyers", "substitutes")
        high = [k for k in forces if str(f.get(k, "")).lower() == "high"]
        if f.get("gap_found") is False:
            return FAIL, "The competitor scan found no gap."
        if len(high) >= 4:
            return FAIL, "%d of 5 forces are high (%s): an unattractive industry." % (len(high), ", ".join(high))
        return PASS, "%d of 5 forces high%s; a gap was found." % (len(high), (" (%s)" % ", ".join(high)) if high else "")
    if key == "price_in_range":
        if n is None:
            return OPEN, "No price yet: run /launchproof-cfo."
        pr = s["prices"]
        if pr is None:
            return OPEN, "No price answers yet: run /launchproof-consumer, then /launchproof-pricing."
        lo, hi = pr["range"]
        if lo is None or hi is None:
            return OPEN, "The price answers do not give a clear range yet."
        ok = lo <= n["price"] <= hi
        return (PASS if ok else FAIL), "Price $%.2f against an acceptable range of $%.2f to $%.2f." % (n["price"], lo, hi)
    if key in ("contribution", "year1_profit", "breakeven_capacity", "runway"):
        if "numbers" in s["errors"]:
            return FAIL, "numbers.json has a problem: %s." % s["errors"]["numbers"]
        if n is None:
            return OPEN, "No numbers yet: run /launchproof-cfo."
        u = n["unit"]
        if key == "contribution":
            c = n["contribution"]
            return (PASS if c > 0 else FAIL), ("Each %s earns $%.2f before fixed costs." % (u, c) if c > 0
                                               else "Each %s LOSES $%.2f before fixed costs." % (u, -c))
        if key == "year1_profit":
            y = n["year1_profit"]
            return (PASS if y > 0 else FAIL), "Year 1 operating %s: %s." % ("profit" if y > 0 else "LOSS", _money(abs(y)))
        if key == "breakeven_capacity":
            be, cap = n["breakeven_per_day"], n["capacity_per_day"]
            if cap is None:
                return PASS, "No capacity limit given."
            fits = not math.isinf(be) and be <= float(cap)
            return (PASS if fits else FAIL), "Break-even is %s %ss a day against a capacity of %s." % (
                "never reached" if math.isinf(be) else "{:,.0f}".format(math.ceil(be)), u, cap)
        cash = ev.get("cash_available")
        need = n["cash_needed"] * RUNWAY_SAFETY
        if cash is None:
            return OPEN, "Cash available not logged in evidence.json (needed: %s, the CFO's figure times %.1f)." % (
                _money(need), RUNWAY_SAFETY)
        return (PASS if cash >= need else FAIL), "Cash available %s against %s needed (%s from the CFO times %.1f)." % (
            _money(cash), _money(need), _money(n["cash_needed"]), RUNWAY_SAFETY)
    if key == "canvas":
        return _file(s, "business-model-canvas.md", "Business Model Canvas", "launchproof-blueprint")
    if key == "real_test":
        t = ev.get("real_test")
        if not t or t.get("result") is None:
            return OPEN, "No real-world test result yet: run the test in /launchproof-launch Step 1."
        ok = float(t["result"]) >= float(t["success_line"])
        return (PASS if ok else FAIL), "Real test (%s): %s %s against a success line of %s." % (
            t.get("what", "test"), t["result"], t.get("unit", ""), t["success_line"])
    if key == "ops_file":
        return _file(s, "ops.md", "Operations and value chain", "launchproof-ops")
    if key == "marketing_file":
        return _file(s, "marketing.md", "Marketing, funnel and sales process", "launchproof-marketing")
    if key == "launch_file":
        return _file(s, "launch.md", "Launch plan", "launchproof-launch")
    if key == "team_file":
        return _file(s, "team.md", "Team plan", "launchproof-blueprint")
    raise KeyError("unknown check: %s" % key)


def read_ticks(d):
    text = _read(os.path.join(d, "checklist.md")) or ""
    return {m.group(2): m.group(1).lower() == "x" for m in map(TICK.match, text.splitlines()) if m}


def evaluate(d, min_buy_rate=0.25):
    spec = load_steps()
    s = gather(d)
    ticks = read_ticks(d)
    steps = {}
    for st in spec["steps"]:
        checks = [(k,) + check(k, s, min_buy_rate) for k in st["checks"]]
        items = [dict(it, done=ticks.get(it["id"], False)) for it in st["items"]]
        open_musts = [it for it in items if it["must"] and not it["done"]]
        if any(c[1] == FAIL for c in checks):
            status = FAIL
        elif all(c[1] == PASS for c in checks) and not open_musts:
            status = PASS
        else:
            status = OPEN
        steps[st["n"]] = dict(st, checks=checks, items=items, open_musts=open_musts, status=status)
    gates, reached = [], 0
    for g in spec["gates"]:
        mine = [steps[n] for n in g["steps"]]
        st = FAIL if any(x["status"] == FAIL for x in mine) else (PASS if all(x["status"] == PASS for x in mine) else OPEN)
        gates.append(dict(g, status=st))
        if st == PASS and reached == g["n"] - 1:
            reached = g["n"]
    return {"steps": steps, "gates": gates, "reached": reached, "state": s}


def profit_verdict(state):
    """The CFO verdict: Profitable, Not yet or Incomplete, with the checks behind it."""
    n = state["numbers"]
    if n is None:
        return "Incomplete", []
    checks = [check(k, state) for k in ("contribution", "year1_profit", "breakeven_capacity")]
    if state["panel"]:
        checks.append(check("panel_buy_rate", state))
    return ("Profitable" if all(c[0] == PASS for c in checks) else "Not yet"), checks


def stage_line(res):
    r = res["reached"]
    if r == 4:
        return "All four gates passed: ready to launch and grow."
    nxt = res["gates"][r]
    if r == 0:
        return ("No gate passed yet: spend nothing but time. Talk to people, score the idea, convene the board and"
                " run the red team. Next: Gate 1, %s." % nxt["name"].lower())
    done = res["gates"][r - 1]
    return "Gate %d of 4 passed (%s). You may spend on: %s Next: Gate %d, %s." % (
        r, done["name"].lower(), done["spend"], nxt["n"], nxt["name"].lower())


def write_checklist(d, res=None):
    res = res or evaluate(d)
    spec = load_steps()
    L = ["# Blueprint checklist", "",
         "Tick an item by changing `[ ]` to `[x]`. Items marked **must** are needed for the step to pass."
         " The tool keeps your ticks when it rewrites this file.", ""]
    for g in spec["gates"]:
        L += ["## Gate %d: %s" % (g["n"], g["name"]), "", "_%s_" % g["question"], ""]
        for n in g["steps"]:
            st = res["steps"][n]
            L.append("### Step %d: %s" % (n, st["title"]))
            L.append("")
            for it in st["items"]:
                L.append("- [%s] %s %s%s" % ("x" if it["done"] else " ", it["id"], it["text"], " **must**" if it["must"] else ""))
            L.append("")
    L.append("_%s_" % spec["source"])
    path = os.path.join(d, "checklist.md")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(L) + "\n")
    return path


def _strip_h1(text):
    lines = text.splitlines()
    if lines and lines[0].startswith("# "):
        lines = lines[1:]
    return "\n".join(("##" + l) if l.startswith("#") else l for l in lines).strip()


def gate_table(res):
    L = ["| gate | steps | status | once it passes, you may spend on |", "| --- | --- | --- | --- |"]
    for g in res["gates"]:
        L.append("| %d. %s | %s | %s %s | %s |" % (g["n"], g["name"], ", ".join(str(x) for x in g["steps"]),
                                                  MARK[g["status"]], g["status"], g["spend"]))
    return L


def compile_plan(d, min_buy_rate=0.25):
    res = evaluate(d, min_buy_rate)
    s = res["state"]
    idea = _read(os.path.join(d, "idea.md"))
    name = None
    if idea and idea.splitlines()[0].startswith("# "):
        name = idea.splitlines()[0][2:].strip()
    n = s["numbers"]
    title = name or (n["business"] if n and n.get("business") else "Your business")
    v, pchecks = profit_verdict(s)
    L = ["# %s · Business plan" % title, "", "**%s**" % stage_line(res), ""]
    L += gate_table(res) + [""]
    L.append("**Profitability: %s**" % v)
    L.append("")
    for st, text in pchecks:
        L.append("- %s %s" % (MARK[st], text))
    if v == "Incomplete":
        L.append("- No numbers yet. Run /launchproof-cfo, then compile again.")
    L.append("")
    if n:
        be = n["breakeven_per_day"]
        L += ["| key number | |", "| --- | ---: |",
              "| Price | $%.2f a %s |" % (n["price"], n["unit"]),
              "| Profit margin at plan | %.0f%% per %s |" % (n["margin_at_plan"] * 100, n["unit"]),
              "| Break-even | %s %ss a day |" % ("never" if math.isinf(be) else "{:,.0f}".format(math.ceil(be)), n["unit"]),
              "| Year 1 operating profit | %s |" % _money(n["year1_profit"]),
              "| Startup spend | %s |" % _money(n["startup"]),
              "| Cash needed before it pays for itself | %s |" % _money(n["cash_needed"]),
              "| Startup money earned back | %s |" % ("month %d" % n["payback_month"] if n["payback_month"] else "not in year 1")]
        if s["score"]:
            L.append("| IdeaGauge score (checked) | %d / 100 (%s) |" % (s["score"]["checked"]["overall"], s["score"]["checked"]["verdict"]))
        if s["panel"]:
            L.append("| Buyer panel (simulated) | %d buy · %d pass |" % (s["panel"]["buys"], s["panel"]["passes"]))
        t = s["evidence"].get("real_test")
        if t and t.get("result") is not None:
            L.append("| Real-world test | %s %s (line: %s) |" % (t["result"], t.get("unit", ""), t["success_line"]))
        L.append("")
    if idea:
        L += ["## The idea", "", _strip_h1(idea), ""]
    for fname, heading in EXTRA_SECTIONS:
        text = _read(os.path.join(d, fname))
        if text:
            L += ["## %s" % heading, "", _strip_h1(text), ""]
    L += ["## The 14 steps", ""]
    missing = []
    for num in sorted(res["steps"]):
        st = res["steps"][num]
        L += ["### Step %d: %s · %s %s" % (num, st["title"], MARK[st["status"]], st["status"]), "", "_%s_" % st["question"], ""]
        for key, cs, text in st["checks"]:
            L.append("- %s %s" % (MARK[cs], text))
        if st["open_musts"]:
            L.append("- ○ Still to do: " + "; ".join("%s %s" % (it["id"], it["text"]) for it in st["open_musts"]))
        L.append("")
        for f in st["files"]:
            if f == "business-model-canvas.md":
                continue
            text = _read(os.path.join(d, f))
            if text:
                L += ["<details><summary>%s</summary>" % f, "", _strip_h1(text), "", "</details>", ""]
            else:
                missing.append((num, f, st["skill"]))
    if missing:
        L += ["## Not done yet", ""]
        for num, f, skill in missing:
            L.append("- Step %d, %s: run /%s" % (num, f, skill))
        L.append("")
    L.append("_The IdeaGauge scores are judgments, the panel is simulated buyers and the numbers are"
             " projections from your inputs. Real customers, a real test and real quotes confirm them. Not financial,"
             " legal or tax advice. The 14-step structure follows The Startup Blueprint by Derick van Vuren._")
    return res, v, "\n".join(L) + "\n"


def action_plan(res):
    r = res["reached"]
    L = ["# Action plan", "", "**%s**" % stage_line(res), ""]
    if r == 4:
        L.append("Keep the monthly review: KPIs, burn and runway, the kill criteria, the checklist.")
        return "\n".join(L) + "\n"
    g = res["gates"][r]
    L += ["## To pass Gate %d: %s" % (g["n"], g["name"]), "", "_%s_" % g["question"], ""]
    for num in g["steps"]:
        st = res["steps"][num]
        if st["status"] == PASS:
            continue
        L.append("### Step %d: %s" % (num, st["title"]))
        L.append("")
        for key, cs, text in st["checks"]:
            if cs != PASS:
                L.append("- [ ] %s" % text)
        for it in st["open_musts"]:
            L.append("- [ ] %s %s" % (it["id"], it["text"]))
        L.append("")
    kills = (res["state"]["board"] or {}).get("kill_criteria") or []
    if kills:
        L += ["## Kill criteria to check at this gate", ""] + ["- %s" % k for k in kills] + [""]
    L.append("Do not spend beyond the current gate until this list is empty.")
    return "\n".join(L) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--dir", default="launchproof")
    ap.add_argument("--min-buy-rate", type=float, default=0.25)
    ap.add_argument("--check", action="store_true", help="print the gates; exit 0 only if all four pass")
    ap.add_argument("--checklist", action="store_true", help="write or refresh checklist.md, keeping ticks")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    if not os.path.isdir(a.dir):
        print("error: no %s/ folder here. Run /launchproof-fit first." % a.dir, file=sys.stderr)
        return 2
    if a.checklist:
        print("Wrote %s" % write_checklist(a.dir))
        return 0
    res, v, text = compile_plan(a.dir, a.min_buy_rate)
    if a.json:
        print(json.dumps({"reached": res["reached"], "profitability": v,
                          "gates": [{"n": g["n"], "name": g["name"], "status": g["status"]} for g in res["gates"]],
                          "steps": {k: {"status": x["status"], "checks": x["checks"],
                                        "open_musts": [i["id"] for i in x["open_musts"]]} for k, x in res["steps"].items()}},
                         indent=1))
        return 0
    if a.check:
        print(stage_line(res))
        for g in res["gates"]:
            print("Gate %d %s: %s" % (g["n"], g["name"], g["status"]))
            for num in g["steps"]:
                st = res["steps"][num]
                print("  Step %d %s: %s" % (num, st["title"], st["status"]))
                for key, cs, t in st["checks"]:
                    print("    %s %s" % (MARK[cs], t))
                if st["open_musts"]:
                    print("    ○ %d must-do items not ticked" % len(st["open_musts"]))
        print("Profitability: %s" % v)
        return 0 if res["reached"] == 4 else 1
    if not os.path.exists(os.path.join(a.dir, "checklist.md")):
        write_checklist(a.dir, res)
    for fname, body in (("business-plan.md", text), ("action-plan.md", action_plan(res))):
        with open(os.path.join(a.dir, fname), "w", encoding="utf-8") as fh:
            fh.write(body)
    print("%s Profitability: %s. Wrote business-plan.md and action-plan.md in %s" % (stage_line(res), v, a.dir))
    return 0


if __name__ == "__main__":
    sys.exit(main())
