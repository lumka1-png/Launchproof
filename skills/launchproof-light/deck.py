#!/usr/bin/env python3
"""The brainstorm deck for launchproof-light. Standard library only, no network.

Reads one JSON file (the assessment, see example.deck.json in this folder),
computes the quick verdict from the board's scores and votes, and writes a
16:9 PowerPoint deck that opens in PowerPoint, Keynote and Google Slides.

    python3 deck.py launchproof-light/deck.json --out launchproof-light/brainstorm.pptx
    python3 deck.py launchproof-light/deck.json --verdict     # print the verdict only

The verdict, computed, never written by hand:

    quick score   the board's average score (1 to 10) times 10
    Go                    score 70 or more, at most 1 PASS, and no kill-shot risk (severity 1)
    Go with conditions    score 50 or more and at most 2 PASS votes
    Rethink               anything else

Every board quote is checked against quotes.md in this folder and refused if it
is not there word for word, so no invented quote reaches a slide.

The input (deck.json):

    idea, one_liner, date        the title slide
    glance                       {problem, customer, offer, price}
    assumptions                  [what Claude assumed because the founder did not say]
    board                        [{person, lens, score, vote, reason, recommendation, quote, source}]
    strengths                    [short lines]
    risks                        [{risk, severity 1 to 5 (1 = kill shot), from}]
    customers                    {buy, total, objections: [], flip: [], voices: [{who, says}]}
    market                       {competitors: [{name, what, price, source}], gap}
    questions                    [questions for the team to brainstorm]
    tests                        [{test, success, cost}]
"""

import argparse
import json
import math
import sys
import zipfile
from xml.sax.saxutils import escape

EMU = 914400
W, H = 13.333, 7.5
FONT = "Arial"
C = {"bg": "0E0F13", "card": "17181F", "card2": "1F2029", "line": "2A2C37", "ink": "F4F4F6", "muted": "9A9BA6",
     "orange": "FF8001", "teal": "0AB6AD", "good": "3DDC84", "warn": "FFB020", "bad": "FF5A5F", "dark": "1B0F00"}
VOTE_COLOR = {"FUND": "good", "FUND IF": "warn", "PASS": "bad"}
VERDICT_COLOR = {"Go": "good", "Go with conditions": "warn", "Rethink": "bad"}
SEVERITY = {1: "Kill shot", 2: "Critical", 3: "Significant", 4: "Moderate", 5: "Minor"}


class DeckError(Exception):
    pass


def check_quotes(d, bank_path=None):
    """Every quote on a slide must appear word for word in quotes.md. Returns the offending people."""
    import os
    bank_path = bank_path or os.path.join(os.path.dirname(os.path.abspath(__file__)), "quotes.md")
    with open(bank_path, encoding="utf-8") as fh:
        bank = fh.read()
    return [m.get("person") for m in d.get("board") or [] if m.get("quote") and '"%s"' % m["quote"] not in bank]


def verdict(d):
    board = d.get("board") or []
    if not board:
        raise DeckError("the board has not voted: 'board' is empty")
    for m in board:
        if m.get("vote") not in VOTE_COLOR:
            raise DeckError("%s: vote must be FUND, FUND IF or PASS" % m.get("person"))
        if not 1 <= float(m.get("score", 0)) <= 10:
            raise DeckError("%s: score must be 1 to 10" % m.get("person"))
    score = int(math.floor(sum(float(m["score"]) for m in board) / len(board) * 10 + 0.5))
    passes = sum(1 for m in board if m["vote"] == "PASS")
    kill = [r for r in d.get("risks") or [] if int(r.get("severity", 5)) == 1]
    if score >= 70 and passes <= 1 and not kill:
        v = "Go"
    elif score >= 50 and passes <= 2:
        v = "Go with conditions"
    else:
        v = "Rethink"
    votes = {k: sum(1 for m in board if m["vote"] == k) for k in VOTE_COLOR}
    return {"verdict": v, "score": score, "votes": votes, "kill_shots": len(kill)}


# ---------------------------------------------------------------- drawing

class Slide:
    def __init__(self):
        self.shapes = []
        self.n = 1

    def _id(self):
        self.n += 1
        return self.n

    def box(self, x, y, w, h, fill=None, line=None, geom="roundRect", radius=0.08):
        av = '<a:gd name="adj" fmla="val %d"/>' % int(radius * 100000) if geom == "roundRect" else ""
        fill_xml = '<a:solidFill><a:srgbClr val="%s"/></a:solidFill>' % C.get(fill, fill) if fill else "<a:noFill/>"
        line_xml = ('<a:ln w="12700"><a:solidFill><a:srgbClr val="%s"/></a:solidFill></a:ln>' % C.get(line, line)
                    if line else "<a:ln><a:noFill/></a:ln>")
        i = self._id()
        self.shapes.append(
            '<p:sp><p:nvSpPr><p:cNvPr id="%d" name="Shape %d"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr><p:spPr>%s'
            '<a:prstGeom prst="%s"><a:avLst>%s</a:avLst></a:prstGeom>%s%s</p:spPr></p:sp>'
            % (i, i, _xfrm(x, y, w, h), geom, av, fill_xml, line_xml))

    def text(self, x, y, w, h, paras, anchor="t", fit=True):
        """paras: list of (text, size, color, bold) or dicts; sizes in points, shrunk to fit the box."""
        ps = [p if isinstance(p, dict) else dict(zip(("t", "size", "color", "bold"), p)) for p in paras]
        if fit:
            ps = _fit(ps, w, h)
        body = []
        for p in ps:
            rpr = '<a:rPr lang="en-US" sz="%d" b="%d" dirty="0"><a:solidFill><a:srgbClr val="%s"/></a:solidFill>' \
                  '<a:latin typeface="%s"/><a:cs typeface="%s"/></a:rPr>' % (
                      int(p["size"] * 100), 1 if p.get("bold") else 0, C.get(p.get("color", "ink"), p.get("color", "ink")),
                      FONT, FONT)
            spc = '<a:spcBef><a:spcPts val="%d"/></a:spcBef>' % int(p.get("before", 0) * 100)
            body.append('<a:p><a:pPr algn="%s">%s</a:pPr><a:r>%s<a:t>%s</a:t></a:r></a:p>'
                        % (p.get("align", "l"), spc, rpr, escape(str(p["t"]))))
        i = self._id()
        self.shapes.append(
            '<p:sp><p:nvSpPr><p:cNvPr id="%d" name="Text %d"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>'
            '<p:spPr>%s<a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/></p:spPr>'
            '<p:txBody><a:bodyPr wrap="square" lIns="0" tIns="0" rIns="0" bIns="0" anchor="%s"><a:noAutofit/></a:bodyPr>'
            '<a:lstStyle/>%s</p:txBody></p:sp>' % (i, i, _xfrm(x, y, w, h), anchor, "".join(body)))

    def xml(self):
        return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                '<p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
                'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
                'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">'
                '<p:cSld><p:bg><p:bgPr><a:solidFill><a:srgbClr val="%s"/></a:solidFill><a:effectLst/></p:bgPr></p:bg>'
                '<p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr/>%s'
                '</p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sld>'
                % (C["bg"], "".join(self.shapes)))


def _xfrm(x, y, w, h):
    return '<a:xfrm><a:off x="%d" y="%d"/><a:ext cx="%d" cy="%d"/></a:xfrm>' % (
        int(x * EMU), int(y * EMU), int(w * EMU), int(h * EMU))


def _lines(text, size, w):
    per_line = max(1, int(w * 72 / (size * 0.52)))
    return sum(max(1, math.ceil(len(part) / per_line)) for part in str(text).split("\n"))


def _fit(ps, w, h):
    """Shrink every paragraph in proportion until the text fits the box (a rough, font-agnostic estimate)."""
    scale = 1.0
    for _ in range(30):
        need = sum(_lines(p["t"], p["size"] * scale, w) * p["size"] * scale * 1.22 / 72 + p.get("before", 0) * scale / 72
                   for p in ps)
        if need <= h or scale < 0.45:
            break
        scale *= 0.93
    return [dict(p, size=max(9, p["size"] * scale)) for p in ps]


def header(s, kicker, title, n, total):
    s.text(0.7, 0.45, 9, 0.35, [(kicker.upper(), 13, "orange", True)])
    s.text(0.7, 0.8, 11.9, 0.9, [(title, 32, "ink", True)])
    s.text(11.4, 7.0, 1.3, 0.3, [{"t": "%d / %d" % (n, total), "size": 11, "color": "muted", "align": "r"}])
    s.text(0.7, 7.0, 6, 0.3, [("Launchproof Light", 11, "muted", True)])


def chip(s, x, y, w, label, color):
    s.box(x, y, w, 0.38, color, radius=0.5)
    s.text(x, y + 0.07, w, 0.26, [{"t": label, "size": 12, "color": "dark", "bold": True, "align": "ctr"}], fit=False)


def initials(name):
    return "".join(p[0] for p in name.split()[:2]).upper()


# ---------------------------------------------------------------- the slides

def build(d):
    v = verdict(d)
    slides = []
    total = 11

    # 1. title
    s = Slide()
    s.box(-1, -1, 15.5, 1.95, "orange", geom="rect")
    s.text(0.7, 0.36, 8, 0.4, [("LAUNCHPROOF LIGHT · QUICK ASSESSMENT", 14, "dark", True)])
    s.text(0.7, 2.1, 11.9, 1.6, [(d["idea"], 54, "ink", True)], anchor="b")
    s.text(0.7, 3.85, 11.5, 1.2, [(d.get("one_liner", ""), 24, "muted", False)])
    s.text(0.7, 5.7, 8, 0.4, [("Prepared for a team brainstorm · %s" % d.get("date", ""), 15, "muted", False)])
    vc = VERDICT_COLOR[v["verdict"]]
    s.box(9.3, 5.45, 3.35, 0.95, "card", line=vc)
    s.text(9.3, 5.55, 3.35, 0.3, [{"t": "QUICK VERDICT", "size": 11, "color": "muted", "bold": True, "align": "ctr"}], fit=False)
    s.text(9.3, 5.85, 3.35, 0.45, [{"t": v["verdict"], "size": 20, "color": vc, "bold": True, "align": "ctr"}])
    slides.append(s)

    # 2. the idea at a glance
    s = Slide()
    header(s, "The idea at a glance", d["idea"], 2, total)
    g = d.get("glance") or {}
    for k, (key, label) in enumerate((("problem", "The problem"), ("customer", "The customer"),
                                      ("offer", "The offer"), ("price", "The price"))):
        x, y = 0.7 + (k % 2) * 6.05, 1.85 + (k // 2) * 1.75
        s.box(x, y, 5.85, 1.6, "card", line="line")
        s.text(x + 0.3, y + 0.22, 5.3, 0.3, [(label.upper(), 12, "orange", True)])
        s.text(x + 0.3, y + 0.55, 5.3, 0.95, [(g.get(key, "Not stated"), 17, "ink", False)])
    a = d.get("assumptions") or []
    if a:
        s.text(0.7, 5.45, 11.9, 1.4, [("Assumed, because it was not stated: " + "; ".join(a) + ".", 14, "muted", False)])
    slides.append(s)

    # 3. verdict
    s = Slide()
    header(s, "The quick verdict", "What the board decided", 3, total)
    s.box(0.7, 1.85, 4.6, 4.6, "card", line=vc)
    s.text(0.7, 2.25, 4.6, 0.35, [{"t": "QUICK SCORE", "size": 13, "color": "muted", "bold": True, "align": "ctr"}], fit=False)
    s.text(0.7, 2.6, 4.6, 1.6, [{"t": str(v["score"]), "size": 96, "color": "ink", "bold": True, "align": "ctr"}], fit=False)
    s.text(0.7, 4.15, 4.6, 0.35, [{"t": "out of 100", "size": 15, "color": "muted", "align": "ctr"}], fit=False)
    s.text(0.7, 4.85, 4.6, 0.8, [{"t": v["verdict"], "size": 30, "color": vc, "bold": True, "align": "ctr"}])
    y = 1.95
    for k, label in (("FUND", "Fund"), ("FUND IF", "Fund, with conditions"), ("PASS", "Pass")):
        s.box(5.75, y, 0.9, 0.9, VOTE_COLOR[k], radius=0.2)
        s.text(5.75, y + 0.17, 0.9, 0.6, [{"t": str(v["votes"][k]), "size": 32, "color": "dark", "bold": True, "align": "ctr"}], fit=False)
        s.text(6.9, y + 0.25, 5.8, 0.5, [(label, 20, "ink", True)])
        y += 1.1
    rule = ("Go: score 70+, at most 1 pass, no kill-shot risk. Go with conditions: score 50+, at most 2 passes. "
            "Otherwise: Rethink.")
    s.text(5.75, 5.35, 6.9, 1.1, [("How it is decided: " + rule, 13, "muted", False)])
    slides.append(s)

    # 4. the board
    s = Slide()
    header(s, "The board of directors", "Five frameworks, five votes", 4, total)
    y = 1.8
    for m in d["board"][:5]:
        s.box(0.7, y, 11.9, 0.92, "card", line="line")
        s.box(0.88, y + 0.14, 0.64, 0.64, "card2", line="orange", geom="ellipse")
        s.text(0.88, y + 0.31, 0.64, 0.3, [{"t": initials(m["person"]), "size": 14, "color": "ink", "bold": True, "align": "ctr"}], fit=False)
        s.text(1.72, y + 0.14, 2.6, 0.35, [(m["person"], 15, "ink", True)])
        s.text(1.72, y + 0.5, 2.6, 0.3, [(m.get("lens", "") + " lens", 12, "muted", False)])
        s.box(4.35, y + 0.36, 1.5, 0.2, "card2", radius=0.5)
        s.box(4.35, y + 0.36, max(0.05, 1.5 * float(m["score"]) / 10), 0.2, "orange", radius=0.5)
        s.text(5.95, y + 0.3, 0.6, 0.3, [(("%g" % float(m["score"])) + "/10", 13, "ink", True)], fit=False)
        chip(s, 6.7, y + 0.27, 1.25, m["vote"], VOTE_COLOR[m["vote"]])
        s.text(8.15, y + 0.12, 4.3, 0.7, [(m.get("reason", ""), 12, "ink", False)], anchor="ctr")
        y += 1.02
    slides.append(s)

    # 5. in their words
    s = Slide()
    header(s, "In their words", "What the board recommends", 5, total)
    quoted = [m for m in d["board"] if m.get("quote")][:3] or d["board"][:3]
    for k, m in enumerate(quoted):
        x = 0.7 + k * 4.03
        s.box(x, 1.85, 3.85, 4.75, "card", line="line")
        s.text(x + 0.3, 2.1, 3.25, 0.4, [(m["person"].upper(), 12, "orange", True)])
        paras = []
        if m.get("quote"):
            paras.append(("“%s”" % m["quote"], 19, "ink", True))
            paras.append({"t": m.get("source", ""), "size": 10, "color": "muted", "before": 6})
        paras.append({"t": "Recommendation", "size": 12, "color": "teal", "bold": True, "before": 18})
        paras.append({"t": m.get("recommendation", ""), "size": 14, "color": "ink", "before": 4})
        s.text(x + 0.3, 2.55, 3.25, 3.9, paras)
    slides.append(s)

    # 6. strong vs kill
    s = Slide()
    header(s, "Strengths and risks", "What is strong, and what could kill it", 6, total)
    s.box(0.7, 1.85, 5.85, 4.85, "card", line="good")
    s.text(1.0, 2.05, 5.3, 0.35, [("WHAT IS STRONG", 13, "good", True)])
    s.text(1.0, 2.5, 5.3, 4.0, [{"t": "+  " + t, "size": 16, "color": "ink", "before": 8} for t in d.get("strengths", [])[:5]])
    s.box(6.75, 1.85, 5.85, 4.85, "card", line="bad")
    s.text(7.05, 2.05, 5.3, 0.35, [("WHAT COULD KILL IT", 13, "bad", True)])
    risks = sorted(d.get("risks") or [], key=lambda r: int(r.get("severity", 5)))[:5]
    paras = []
    for r in risks:
        paras.append({"t": "%s  ·  %s" % (SEVERITY.get(int(r.get("severity", 3)), ""), r.get("from", "")),
                      "size": 11, "color": "warn" if int(r.get("severity", 3)) > 1 else "bad", "bold": True, "before": 8})
        paras.append({"t": r["risk"], "size": 15, "color": "ink", "before": 2})
    s.text(7.05, 2.45, 5.3, 4.1, paras)
    slides.append(s)

    # 7. customers
    s = Slide()
    cu = d.get("customers") or {}
    header(s, "Customer voices (simulated)", "Would they buy it?", 7, total)
    buy, tot = int(cu.get("buy", 0)), int(cu.get("total", 0)) or 1
    s.box(0.7, 1.85, 4.2, 4.85, "card", line="line")
    s.text(0.7, 2.15, 4.2, 1.2, [{"t": "%d of %d" % (buy, tot), "size": 54, "color": "orange", "bold": True, "align": "ctr"}], fit=False)
    s.text(0.7, 3.3, 4.2, 0.4, [{"t": "simulated buyers would buy", "size": 15, "color": "muted", "align": "ctr"}], fit=False)
    for k in range(tot):
        cx = 0.7 + (4.2 - min(tot, 8) * 0.45) / 2 + (k % 8) * 0.45
        s.box(cx, 4.0 + (k // 8) * 0.45, 0.32, 0.32, "orange" if k < buy else "card2", geom="ellipse")
    s.text(1.0, 5.2, 3.6, 1.4, [("A fast read of objections, not a forecast. Confirm with real people.", 12, "muted", False)])
    paras = [("TOP OBJECTIONS", 13, "orange", True)]
    paras += [{"t": "•  " + o, "size": 15, "color": "ink", "before": 6} for o in cu.get("objections", [])[:4]]
    paras.append({"t": "WHAT WOULD CHANGE THEIR MIND", "size": 13, "color": "teal", "bold": True, "before": 18})
    paras += [{"t": "•  " + o, "size": 15, "color": "ink", "before": 6} for o in cu.get("flip", [])[:3]]
    s.text(5.2, 1.95, 7.4, 3.3, paras)
    voices = cu.get("voices", [])[:2]
    for k, vo in enumerate(voices):
        x = 5.2 + k * 3.75
        s.box(x, 5.4, 3.6, 1.3, "card2")
        s.text(x + 0.2, 5.5, 3.2, 1.1, [("“%s”" % vo["says"], 13, "ink", False),
                                        {"t": vo.get("who", ""), "size": 10, "color": "muted", "before": 4}])
    slides.append(s)

    # 8. market
    s = Slide()
    mk = d.get("market") or {}
    header(s, "Market snapshot", "Who is already there", 8, total)
    comps = mk.get("competitors", [])[:5]
    y = 1.8
    for c in comps:
        s.box(0.7, y, 7.6, 0.8, "card", line="line")
        s.text(0.95, y + 0.1, 2.4, 0.6, [(c["name"], 14, "ink", True)], anchor="ctr")
        s.text(3.45, y + 0.1, 3.3, 0.6, [(c.get("what", ""), 12, "muted", False)], anchor="ctr")
        s.text(6.85, y + 0.1, 1.3, 0.6, [{"t": c.get("price", ""), "size": 12, "color": "orange", "bold": True, "align": "r"}], anchor="ctr")
        y += 0.9
    s.box(8.55, 1.8, 4.05, 4.4, "card", line="teal")
    s.text(8.85, 2.05, 3.5, 0.35, [("THE GAP", 13, "teal", True)])
    s.text(8.85, 2.5, 3.5, 3.5, [(mk.get("gap", "No clear gap found."), 18, "ink", True)])
    src = [c.get("source") for c in comps if c.get("source")]
    if src:
        s.text(0.7, 6.35, 11.9, 0.55, [("Sources: " + "  ·  ".join(src), 9, "muted", False)])
    slides.append(s)

    # 9. questions
    s = Slide()
    header(s, "For the team", "Questions to brainstorm", 9, total)
    qs = d.get("questions", [])[:6]
    for k, q in enumerate(qs):
        x, y = 0.7 + (k % 2) * 6.05, 1.85 + (k // 2) * 1.6
        s.box(x, y, 5.85, 1.45, "card", line="line")
        s.box(x + 0.25, y + 0.3, 0.75, 0.75, "orange", radius=0.25)
        s.text(x + 0.25, y + 0.45, 0.75, 0.5, [{"t": str(k + 1), "size": 24, "color": "dark", "bold": True, "align": "ctr"}], fit=False)
        s.text(x + 1.2, y + 0.18, 4.45, 1.1, [(q, 16, "ink", True)], anchor="ctr")
    slides.append(s)

    # 10. tests
    s = Slide()
    header(s, "Before anyone spends money", "Three cheap tests for this week", 10, total)
    for k, t in enumerate(d.get("tests", [])[:3]):
        x = 0.7 + k * 4.03
        s.box(x, 1.85, 3.85, 4.75, "card", line="orange" if k == 0 else "line")
        s.text(x + 0.3, 2.1, 3.25, 0.4, [("TEST %d" % (k + 1), 13, "orange", True)])
        s.text(x + 0.3, 2.55, 3.25, 2.2, [(t["test"], 18, "ink", True)])
        s.text(x + 0.3, 4.8, 3.25, 1.7, [("SUCCESS LOOKS LIKE", 11, "teal", True),
                                         {"t": t.get("success", ""), "size": 14, "color": "ink", "before": 4},
                                         {"t": "Cost: " + t.get("cost", ""), "size": 12, "color": "muted", "before": 10}])
    slides.append(s)

    # 11. next
    s = Slide()
    s.box(-1, 5.6, 15.5, 3, "orange", geom="rect")
    s.text(0.7, 1.3, 11.9, 1.2, [("Next: go deeper, or drop it cheaply", 40, "ink", True)])
    s.text(0.7, 2.7, 11.5, 2.4, [
        ("If the team wants to go on, run the full Launchproof: founder fit, the IdeaGauge score, a red team, "
         "100 simulated buyers, the real numbers, four money gates and a 14-step business plan.", 18, "muted", False),
        {"t": "Everything here is a quick, simulated read: the board applies published frameworks (quotes are from "
              "their published work), and the buyers are simulated. Real customers decide.", "size": 13,
         "color": "muted", "before": 14}])
    s.text(0.7, 6.05, 8, 0.6, [("Launchproof Light", 30, "dark", True)])
    s.text(6.5, 6.15, 6.1, 0.5, [{"t": "Built on The Startup Blueprint by Derick van Vuren", "size": 14,
                                  "color": "dark", "bold": True, "align": "r"}])
    slides.append(s)
    return v, slides


# ---------------------------------------------------------------- the package

NS_P = ('xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
        'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"')
REL = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
HEAD = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'


def _rels(items):
    return HEAD + '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">' + "".join(
        '<Relationship Id="%s" Type="%s/%s" Target="%s"/>' % (i, REL, t, tg) for i, t, tg in items) + "</Relationships>"


THEME = HEAD + (
    '<a:theme xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" name="Launchproof">'
    '<a:themeElements><a:clrScheme name="Launchproof">'
    '<a:dk1><a:srgbClr val="0E0F13"/></a:dk1><a:lt1><a:srgbClr val="F4F4F6"/></a:lt1>'
    '<a:dk2><a:srgbClr val="17181F"/></a:dk2><a:lt2><a:srgbClr val="9A9BA6"/></a:lt2>'
    '<a:accent1><a:srgbClr val="FF8001"/></a:accent1><a:accent2><a:srgbClr val="0AB6AD"/></a:accent2>'
    '<a:accent3><a:srgbClr val="3DDC84"/></a:accent3><a:accent4><a:srgbClr val="FFB020"/></a:accent4>'
    '<a:accent5><a:srgbClr val="FF5A5F"/></a:accent5><a:accent6><a:srgbClr val="4DA3FF"/></a:accent6>'
    '<a:hlink><a:srgbClr val="4DA3FF"/></a:hlink><a:folHlink><a:srgbClr val="9A9BA6"/></a:folHlink></a:clrScheme>'
    '<a:fontScheme name="Launchproof"><a:majorFont><a:latin typeface="Arial"/><a:ea typeface=""/><a:cs typeface=""/>'
    '</a:majorFont><a:minorFont><a:latin typeface="Arial"/><a:ea typeface=""/><a:cs typeface=""/></a:minorFont></a:fontScheme>'
    '<a:fmtScheme name="Launchproof"><a:fillStyleLst>'
    '<a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:solidFill><a:schemeClr val="phClr"/></a:solidFill>'
    '<a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:fillStyleLst><a:lnStyleLst>'
    '<a:ln w="6350"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln>'
    '<a:ln w="12700"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln>'
    '<a:ln w="19050"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln></a:lnStyleLst>'
    '<a:effectStyleLst><a:effectStyle><a:effectLst/></a:effectStyle><a:effectStyle><a:effectLst/></a:effectStyle>'
    '<a:effectStyle><a:effectLst/></a:effectStyle></a:effectStyleLst><a:bgFillStyleLst>'
    '<a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:solidFill><a:schemeClr val="phClr"/></a:solidFill>'
    '<a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:bgFillStyleLst></a:fmtScheme></a:themeElements>'
    '<a:objectDefaults/><a:extraClrSchemeLst/></a:theme>')

EMPTY_TREE = ('<p:cSld%s><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>'
              '<p:grpSpPr/></p:spTree></p:cSld>')
MASTER = HEAD + ('<p:sldMaster %s>' % NS_P) + (EMPTY_TREE % "") + (
    '<p:clrMap bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2" accent1="accent1" accent2="accent2" accent3="accent3" '
    'accent4="accent4" accent5="accent5" accent6="accent6" hlink="hlink" folHlink="folHlink"/>'
    '<p:sldLayoutIdLst><p:sldLayoutId id="2147483649" r:id="rId1"/></p:sldLayoutIdLst>'
    '<p:txStyles><p:titleStyle/><p:bodyStyle/><p:otherStyle/></p:txStyles></p:sldMaster>')
LAYOUT = HEAD + ('<p:sldLayout %s type="blank" preserve="1">' % NS_P) + (EMPTY_TREE % ' name="Blank"') + (
    '<p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sldLayout>')


def write_pptx(slides, path, title="Launchproof Light"):
    n = len(slides)
    ct = (HEAD + '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
          '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
          '<Default Extension="xml" ContentType="application/xml"/>'
          '<Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/>'
          '<Override PartName="/ppt/slideMasters/slideMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml"/>'
          '<Override PartName="/ppt/slideLayouts/slideLayout1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"/>'
          '<Override PartName="/ppt/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>'
          '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>'
          '<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>'
          + "".join('<Override PartName="/ppt/slides/slide%d.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>' % (i + 1) for i in range(n))
          + "</Types>")
    pres = (HEAD + '<p:presentation %s saveSubsetFonts="1">' % NS_P
            + '<p:sldMasterIdLst><p:sldMasterId id="2147483648" r:id="rId1"/></p:sldMasterIdLst><p:sldIdLst>'
            + "".join('<p:sldId id="%d" r:id="rId%d"/>' % (256 + i, i + 3) for i in range(n))
            + '</p:sldIdLst><p:sldSz cx="12192000" cy="6858000"/><p:notesSz cx="6858000" cy="9144000"/>'
            + '<p:defaultTextStyle/></p:presentation>')
    pres_rels = _rels([("rId1", "slideMaster", "slideMasters/slideMaster1.xml"), ("rId2", "theme", "theme/theme1.xml")]
                      + [("rId%d" % (i + 3), "slide", "slides/slide%d.xml" % (i + 1)) for i in range(n)])
    core = (HEAD + '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
            'xmlns:dc="http://purl.org/dc/elements/1.1/"><dc:title>%s</dc:title><dc:creator>Launchproof Light</dc:creator>'
            '</cp:coreProperties>' % escape(title))
    app = (HEAD + '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties">'
           '<Application>Launchproof Light</Application><Slides>%d</Slides></Properties>' % n)
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", ct)
        z.writestr("_rels/.rels", _rels([("rId1", "officeDocument", "ppt/presentation.xml"),
                                          ("rId2", "metadata/core-properties", "docProps/core.xml"),
                                          ("rId3", "extended-properties", "docProps/app.xml")]).replace(
            REL + "/metadata/core-properties", "http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties"))
        z.writestr("docProps/core.xml", core)
        z.writestr("docProps/app.xml", app)
        z.writestr("ppt/presentation.xml", pres)
        z.writestr("ppt/_rels/presentation.xml.rels", pres_rels)
        z.writestr("ppt/theme/theme1.xml", THEME)
        z.writestr("ppt/slideMasters/slideMaster1.xml", MASTER)
        z.writestr("ppt/slideMasters/_rels/slideMaster1.xml.rels",
                   _rels([("rId1", "slideLayout", "../slideLayouts/slideLayout1.xml"), ("rId2", "theme", "../theme/theme1.xml")]))
        z.writestr("ppt/slideLayouts/slideLayout1.xml", LAYOUT)
        z.writestr("ppt/slideLayouts/_rels/slideLayout1.xml.rels",
                   _rels([("rId1", "slideMaster", "../slideMasters/slideMaster1.xml")]))
        for i, s in enumerate(slides):
            z.writestr("ppt/slides/slide%d.xml" % (i + 1), s.xml())
            z.writestr("ppt/slides/_rels/slide%d.xml.rels" % (i + 1),
                       _rels([("rId1", "slideLayout", "../slideLayouts/slideLayout1.xml")]))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("path")
    ap.add_argument("--out", help="default: brainstorm.pptx next to the input")
    ap.add_argument("--verdict", action="store_true", help="print the verdict only")
    a = ap.parse_args(argv)
    try:
        with open(a.path, encoding="utf-8") as fh:
            d = json.load(fh)
        for key in ("idea", "board"):
            if not d.get(key):
                raise DeckError("'%s' is missing" % key)
        bad = check_quotes(d)
        if bad:
            raise DeckError("these quotes are not word for word in quotes.md: %s. Copy them exactly, or leave"
                            " the quote empty." % ", ".join(bad))
        if a.verdict:
            v = verdict(d)
            print("%s · quick score %d · %d fund, %d fund if, %d pass%s" % (
                v["verdict"], v["score"], v["votes"]["FUND"], v["votes"]["FUND IF"], v["votes"]["PASS"],
                " · %d kill-shot risk" % v["kill_shots"] if v["kill_shots"] else ""))
            return 0
        v, slides = build(d)
        import os
        out = a.out or os.path.join(os.path.dirname(os.path.abspath(a.path)), "brainstorm.pptx")
        write_pptx(slides, out, d["idea"])
    except (DeckError, OSError, ValueError, KeyError) as e:
        print("error: %s" % e, file=sys.stderr)
        return 2
    print("%s (quick score %d). Wrote %s, %d slides." % (v["verdict"], v["score"], out, len(slides)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
