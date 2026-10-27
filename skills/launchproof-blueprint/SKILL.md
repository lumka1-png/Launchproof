---
name: launchproof-blueprint
description: >-
  The actionable business plan, built on the 14 steps of The Startup Blueprint
  by Derick van Vuren. Checks everything the other Launchproof skills found
  against four money gates (worth testing, worth a real-world test, worth
  building, ready to launch), each made of Blueprint steps with computed checks
  and a must-do checklist, and says exactly what the founder may spend money on
  now. Writes the Business Model Canvas, the growth and team plans, the full
  eight-section plan and a lean plan, and an action plan for the next gate. Use
  when the user says "write my business plan", "what do I do next", "can I spend
  money yet", "check the gates", "give me the checklist", or at the end of the
  Launchproof pack.
argument-hint: "[--check] [--min-buy-rate 0.25]"
---

# launchproof-blueprint

The plan a founder can act on. Not a document that sits in a drawer: a sequence
of gates, each one telling the founder what they have earned the right to spend
on, and what to do this week to reach the next one.

Tool in this folder (`BP` below means exactly this):

```bash
python3 "${CLAUDE_SKILL_DIR}/blueprint.py" --dir launchproof [--check | --checklist]
```

## The four gates

Before Gate 1, the founder spends nothing but time.

| gate | Blueprint steps | the question | once it passes, spend on |
| --- | --- | --- | --- |
| 1. Worth testing | 1 Idea, 2 Entrepreneur, 3 Mind games | Is this a real opportunity, for this founder, that survives a pre-mortem? | research only (interviews, a survey tool) |
| 2. Worth a real-world test | 5 Value proposition, 6 Customers, 7 Segmentation, 8 Competition | Do we know who buys, why, and where the gap is? | a small test budget |
| 3. Worth building | 9 Price, 10 Value chain, 11 Business model and plan | Does every unit make money, does year 1 work, and did real buyers confirm it? | the startup budget |
| 4. Ready to launch and grow | 4 Foundation, 12 Sell, 13 Grow, 14 Team | Is the company set up, sales ready, cash sufficient, team planned? | launch, legal, hiring |

Step 4 (legal form, naming, branding) comes early in the book. Here its free
parts (name availability checks, choosing the structure with an adviser) can be
done at any time, but the paid parts (registration, trademarks, insurance) wait
for Gate 3. That is the point of the gates: no money is spent on a business that
has not earned it.

A step passes when its automatic checks pass and its must-do items are ticked in
`launchproof/checklist.md`. The checks are computed by the tool from the files
the other skills wrote. The steps, checks and checklist items are in
`steps.json` in this folder.

## Step 1: see where the founder is

```bash
BP --check
BP --checklist      # writes launchproof/checklist.md, keeping any ticks
```

Show the founder the gate table and the next gate's open items. For each open or
failing check, name the skill that closes it. Ask the founder to tick the items
they have really done, in `launchproof/checklist.md`, and to log real-world
evidence in `launchproof/evidence.json` (problem conversations, customer
interviews, personal runway, cash available, the real test result). **Never tick
an item or log evidence on the founder's behalf.** If they tell you in chat that
something is done, ask them to confirm, then tick only that item.

## Step 2: the sections only this skill writes

Write only from what is in `launchproof/`; if a section needs something missing,
write the gap instead of a guess.

1. `launchproof/business-model-canvas.md` (Blueprint Step 11): the nine blocks in
   order: customer segments, value propositions, channels, customer relationships,
   revenue streams, key resources, key activities, key partnerships, cost
   structure. Each block cites the file it came from. Check that the blocks agree
   with each other (the channel reaches the segment, the cost structure matches
   the CFO's numbers).
2. `launchproof/growth.md` (Blueprint Step 13): the funding path (bootstrap,
   friends and family, loan, angels, venture capital) and why it fits this
   business; burn rate and runway from the CFO's numbers and the cash in
   `evidence.json`; a game tree for the main competitor's likely reaction to the
   launch and the price (match, ignore, differentiate) and the planned response;
   whether this business grows (costs rise with revenue) or scales (they do not),
   and what would make it scale.
3. `launchproof/team.md` (Blueprint Step 14): the first roles, chosen to
   complement the founder's gaps in `launchproof/fit.md` (usually technical,
   growth and operations), the hiring order tied to milestones, the compensation
   approach including any equity, draft company values, and the 12 to 24 month
   team plan. For a solo founder, name which roles stay contractors or tools.
4. `launchproof/plan-narrative.md` (Blueprint Step 11), the eight sections of a
   business plan, with every number copied from the tool output, never retyped:
   - **Executive summary** (written last, placed first).
   - **Company description**: mission, structure, current traction (real evidence only).
   - **Market analysis**: TAM, SAM and SOM with sources, trends, the competitive
     landscape and the five forces.
   - **Organization and management**: the founder, the team plan.
   - **Product or service line**: what is sold, the value proposition, the roadmap.
   - **Marketing and sales**: the primary segment, channels, funnel, pricing
     logic, the most you can pay to win a customer.
   - **Funding request**: how much, for what, and why now; or "self-funded" and
     how far the cash goes.
   - **Financial projections**: year 1 by month from the CFO, break-even,
     payback, and the best, expected and worst cases.
   Then a **lean plan**: the same story in one to two pages for a partner,
   lender or investor deciding in five minutes.

## Step 3: compile

```bash
BP
```

This writes `launchproof/business-plan.md` (the stage line, the gate table, the
profitability verdict, key numbers, the plan narrative, the canvas, then all 14
steps with their checks and the evidence behind each) and
`launchproof/action-plan.md` (every open item for the next gate, plus the board's
kill criteria to check there).

## Step 4: tell the founder

Three lines, then the action plan:

1. Where they are: "Gate 2 of 4 passed. You may spend a small test budget."
2. What they must **not** spend on yet, by name (for example "do not sign the
   lease or order equipment before the pre-order test hits 50").
3. The one thing to do this week.

If a gate fails, lead with that and do not soften it. Check the kill criteria
from `launchproof/board.md` at every gate: if one has been hit, say so and offer
the three options (rework, pivot, stop). Stopping before Gate 3 is a good outcome;
the founder kept their startup budget.

## Rules

- Gate status comes from the tool. Never write "passed" by hand, and never round
  a failing number into a passing one.
- The checklist and the evidence log belong to the founder. Claude proposes,
  the founder ticks.
- Say once: evaluator scores are judgments, the panel is simulated, numbers are
  projections; the real-world test and real quotes are what count. Not financial,
  legal or tax advice.
- If the user wants a PDF, a document or slides, offer to export, but keep the
  markdown as the source of truth.

## Output

`launchproof/checklist.md`, `launchproof/business-model-canvas.md`,
`launchproof/growth.md`, `launchproof/team.md`, `launchproof/plan-narrative.md`,
`launchproof/business-plan.md`, `launchproof/action-plan.md`.
