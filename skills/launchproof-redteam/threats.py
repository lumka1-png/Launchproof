#!/usr/bin/env python3
"""Red team and blue team bookkeeping for launchproof-redteam. Standard library only.

The red team attacks the idea and scores every vulnerability 1 to 5:

    1 Catastrophic   a kill shot: a fundamental flaw with no recovery
    2 Critical       a crippling blow: needs a fundamental pivot
    3 Significant    a major weakness: real money or time to fix
    4 Moderate       a manageable flaw: known, affordable fixes exist
    5 Resilient      a negligible threat

The blue team then gives each threat a defense (how to detect it, what to do
in the first hour, how to mitigate it for good, what that costs) and a
post-mitigation score. This tool checks the file, summarizes it and decides the
gate: it passes when no threat is still at 1 or 2 after the defenses.

    python3 threats.py launchproof/threats.json --out launchproof/redteam.md
    python3 threats.py launchproof/threats.json --check     # exit 0 if the gate passes

The input (launchproof/threats.json):

    threats    [{id, vector, attack, vulnerability, score, rationale,
                 defense: {detect, respond, mitigate, cost}, post_score}]
    cascades   optional [[id, id, ...]]: chains where one failure triggers the next
"""

import argparse
import json
import sys

VECTORS = [
    ("product", "Technical and product integrity"),
    ("market", "Market and economic viability"),
    ("social", "Social and ethical resonance"),
    ("legal", "Legal and regulatory compliance"),
    ("narrative", "Narrative and reputation"),
]
LEVELS = {1: "Catastrophic", 2: "Critical", 3: "Significant", 4: "Moderate", 5: "Resilient"}


class ThreatError(Exception):
    pass


def _score(v, where):
    if v is None:
        return None
    if not isinstance(v, int) or isinstance(v, bool) or v not in LEVELS:
        raise ThreatError("%s: score must be a whole number from 1 to 5, got %r" % (where, v))
    return v


def analyse(spec):
    threats = spec.get("threats") or []
    if not threats:
        raise ThreatError("no threats: run the red team first")
    known = {k for k, _ in VECTORS}
    ids = set()
    rows = []
    for t in threats:
        tid = t.get("id")
        if not tid or tid in ids:
            raise ThreatError("every threat needs a unique id (got %r)" % tid)
        ids.add(tid)
        if t.get("vector") not in known:
            raise ThreatError("%s: vector must be one of %s" % (tid, ", ".join(sorted(known))))
        pre = _score(t.get("score"), tid)
        if pre is None:
            raise ThreatError("%s: the red team must score every threat" % tid)
        post = _score(t.get("post_score"), tid + " post_score")
        d = t.get("defense") or {}
        defended = all((d.get(k) or "").strip() for k in ("detect", "respond", "mitigate"))
        rows.append(dict(t, score=pre, post_score=post, defended=defended))
    for chain in spec.get("cascades") or []:
        for tid in chain:
            if tid not in ids:
                raise ThreatError("cascade names an unknown threat: %s" % tid)

    def final(r):
        return r["post_score"] if (r["defended"] and r["post_score"] is not None) else r["score"]

    open_kills = [r for r in rows if final(r) <= 2]
    undefended = [r for r in rows if r["score"] <= 3 and not r["defended"]]
    by_vector = []
    for k, label in VECTORS:
        mine = [r for r in rows if r["vector"] == k]
        by_vector.append((k, label, len(mine), min((r["score"] for r in mine), default=None),
                          min((final(r) for r in mine), default=None)))
    return {
        "threats": rows, "by_vector": by_vector, "cascades": spec.get("cascades") or [],
        "pre_critical": [r["id"] for r in rows if r["score"] <= 2],
        "open_kills": [r["id"] for r in open_kills],
        "undefended": [r["id"] for r in undefended],
        "blue_team_done": all(r["post_score"] is not None for r in rows if r["score"] <= 3),
        "gate_pass": not open_kills and not undefended,
        "final": {r["id"]: final(r) for r in rows},
    }


def report(res, title="Red team and blue team"):
    L = ["# %s" % title, ""]
    if res["gate_pass"]:
        L.append("**The idea survives: no threat is still critical or catastrophic after the defenses.**")
    else:
        L.append("**Not yet: %s.**" % "; ".join(
            ([("still critical after defenses: %s" % ", ".join(res["open_kills"]))] if res["open_kills"] else []) +
            ([("no defense yet: %s" % ", ".join(res["undefended"]))] if res["undefended"] else [])))
    L += ["", "| vector | threats | worst before | worst after |", "| --- | ---: | ---: | ---: |"]
    for _, label, n, worst, after in res["by_vector"]:
        L.append("| %s | %d | %s | %s |" % (label, n, "" if worst is None else "%d %s" % (worst, LEVELS[worst]),
                                             "" if after is None else "%d %s" % (after, LEVELS[after])))
    for k, label, n, _, _ in res["by_vector"]:
        mine = [r for r in res["threats"] if r["vector"] == k]
        if not mine:
            continue
        L += ["", "## %s" % label, "", "| id | attack | vulnerability | before | defense | after |",
              "| --- | --- | --- | ---: | --- | ---: |"]
        for r in sorted(mine, key=lambda r: r["score"]):
            d = r.get("defense") or {}
            defense = " / ".join(x for x in (d.get("detect"), d.get("respond"), d.get("mitigate")) if x) or "none yet"
            L.append("| %s | %s | %s | %d | %s | %s |" % (
                r["id"], r.get("attack", ""), (r.get("vulnerability") or "").replace("|", "/"), r["score"],
                defense.replace("|", "/"), "" if r["post_score"] is None else r["post_score"]))
    if res["cascades"]:
        L += ["", "## Cascading failures", ""]
        names = {r["id"]: r.get("attack") or r["id"] for r in res["threats"]}
        for chain in res["cascades"]:
            L.append("- " + " → ".join("%s (%s)" % (names[t], t) for t in chain))
    L += ["", "_The red team argues the worst plausible case on purpose. It finds what to defend, not what will"
          " happen._"]
    return "\n".join(L) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("path")
    ap.add_argument("--out")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--check", action="store_true", help="exit 0 only if the gate passes")
    a = ap.parse_args(argv)
    try:
        with open(a.path, encoding="utf-8") as fh:
            res = analyse(json.load(fh))
    except (ThreatError, OSError, ValueError) as e:
        print("error: %s" % e, file=sys.stderr)
        return 2
    if a.json:
        print(json.dumps(res, indent=1))
    elif a.check:
        print("Red team gate: %s" % ("passes" if res["gate_pass"] else "fails"))
        for t in res["open_kills"]:
            print("  ✗ %s is still at %d after defenses" % (t, res["final"][t]))
        for t in res["undefended"]:
            print("  ✗ %s has no defense yet" % t)
    else:
        text = report(res)
        if a.out:
            with open(a.out, "w", encoding="utf-8") as fh:
                fh.write(text)
            print("Wrote %s" % a.out)
        else:
            print(text)
    return 0 if (res["gate_pass"] or not a.check) else 1


if __name__ == "__main__":
    sys.exit(main())
