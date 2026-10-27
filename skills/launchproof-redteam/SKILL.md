---
name: launchproof-redteam
description: >-
  Breaks the idea so it can be made unbreakable. A red team of five sub-agents
  (a product tester, a ruthless competitor, a social critic, a regulator and a
  narrative strategist) attacks the business across five vectors and scores
  every vulnerability from 1 (kill shot) to 5 (resilient), with the chains where
  one failure triggers the next. A blue team then builds a defense for each
  threat (detect, respond, mitigate, cost) and re-scores it. The gate passes only
  when nothing is still critical after the defenses. Based on the red team and
  blue team method in The Startup Blueprint. Use when the user says "red team
  this", "what could go wrong", "stress test", "pre-mortem", "attack my idea",
  or after /launchproof-board.
argument-hint: "[--quick for one attacker per vector, three attacks each]"
---

# launchproof-redteam

The board judges the idea. The red team tries to kill it. A pre-mortem now costs
an afternoon; the same failure after launch costs the business. This is
Blueprint Step 3: counter optimism bias with a structured pre-mortem.

What the user typed after `/launchproof-redteam`: `$ARGUMENTS`

Tool in this folder:

```bash
python3 "${CLAUDE_SKILL_DIR}/threats.py" launchproof/threats.json --out launchproof/redteam.md
```

## Step 1: the target file

Write `launchproof/redteam/target.md`. The sub-agents cannot see this
conversation, so it must stand on its own:

- **High concept**: one sentence.
- **Value proposition**: what problem it solves, for whom.
- **Success in 18 months**: one measurable line (from `launchproof/fit.md`).
- **Key assumptions**: market (size, willingness to pay), operations (supply,
  capacity, tech), business model (price, margin).
- **Assets and environment**: what the founder owns that others do not, the
  target customer, the competitors (from `launchproof/competitors.md` if it ran),
  the rules that apply.
- The board's top risks and kill criteria from `launchproof/board.md`.

Show it to the founder and let them correct the assumptions. A red team that
attacks the wrong plan is wasted.

## Step 2: the red team

Launch five sub-agents in ONE message (Agent tool, `subagent_type:
general-purpose`), one per role. Each is told: `Read launchproof/redteam/target.md.
You are the <role>. Attack ONLY the <vector> vector. Assume the worst plausible
case: realistic, not fantasy. No hedging. Write your attacks to
launchproof/redteam/<vector>.json as a JSON list of {"attack", "vulnerability",
"score", "rationale"}, where score is 1 Catastrophic, 2 Critical, 3 Significant,
4 Moderate or 5 Resilient. Every attack gets a score.`

| vector | role | attacks to run |
| --- | --- | --- |
| `product` | Lead product tester | what breaks at 10 times the volume; how inputs or suppliers fail; where customers get frustrated and leave; the single points of failure |
| `market` | Ruthless competitor CEO | how an incumbent crushes it (price, copy, bundle); when the value proposition stops mattering; why customers stop caring; what if the main channel disappears |
| `social` | Skeptical social critic | how bad actors could misuse it; what would trigger a public backlash; where good intentions go wrong |
| `legal` | Cynical regulator | what if the rules tighten; how a lawsuit could hurt it; where the laws of two places clash; licenses and claims |
| `narrative` | Reputation strategist | how the story can be twisted; toxic associations; how it can be misrepresented |

`--quick`: three attacks per vector instead of four to six.

## Step 3: merge and find the cascades

Merge the five files into `launchproof/threats.json` with ids (`P1`, `M1`, `S1`,
`L1`, `N1`...) and the vector. Copy scores exactly; never soften one. Then name
the **cascading failures**: chains where one attack triggers another (for example
a supplier failure leads to sick customers, then a backlash, then a lawsuit).
List each chain under `cascades` as ids in order.

## Step 4: the blue team

Launch ONE sub-agent (`general-purpose`) told: `Read
launchproof/redteam/target.md and launchproof/threats.json. You are the blue team:
a product lead, a strategy lead, a communications lead, a legal and compliance
lead and an operations lead. For every threat scored 1 to 3, write a defense:
detect (the early warning sign and how you will see it), respond (what to do in
the first hour), mitigate (what removes or shrinks it for good) and cost (time and
money, realistically for a startup this size). Then give a post_score from 1 to 5.
No magical thinking: real tools, real budgets, real people. Write the result back
into launchproof/threats.json.` Threats scored 4 or 5 need no defense.

Then:

```bash
python3 "${CLAUDE_SKILL_DIR}/threats.py" launchproof/threats.json --out launchproof/redteam.md
```

## Step 5: read it to the founder

1. The verdict line from the tool.
2. The three to five worst threats before defenses, and the cascades.
3. What the defenses cost in total, and which ones must be in place **before**
   spending money (these become checklist items at Gate 1 and Gate 3).
4. Any threat still at 1 or 2: say plainly that this is the reason not to spend
   yet, and what would have to be true to fix it.

## Output

`launchproof/redteam/` (target and five attack files), `launchproof/threats.json`,
`launchproof/redteam.md`. Next: `/launchproof-competitors`, or `/launchproof-blueprint
--check` to see Gate 1.
