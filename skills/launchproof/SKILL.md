---
name: launchproof
description: >-
  Runs the whole Launchproof journey on a business idea, from the first founder
  questions to a gated, actionable business plan: founder fit, the IdeaGauge
  score, a five-member board (the Hormozi, Thiel, Priestley, Naval and Munger
  frameworks), a red team, competitors, a 100-buyer simulated panel, pricing,
  the offer, the CFO's numbers, marketing, brand, operations, a real-world test
  and the 14-step Startup Blueprint plan. Stops at every money gate and says
  what the founder may spend now. Use when the user says "evaluate my business
  idea", "test my idea", "should I start this business", "help me build a
  business plan", "launchproof", or describes a new business idea.
argument-hint: "<the business idea, or leave blank to be asked> [--quick]"
---

# launchproof

The point of Launchproof is to save founders time and money: find out cheaply
whether an idea deserves the next dollar, and give clear direction either way.
This skill is the conductor. Each stage is its own skill and can run alone; this
one runs them in order and stops at each gate.

What the user typed after `/launchproof`: `$ARGUMENTS`

## The journey

| stage | skill | Blueprint step | writes |
| --- | --- | --- | --- |
| Founder fit | `/launchproof-fit` | 1, 2 | idea.md, fit.md, evidence.json |
| Score | `/launchproof-score` | 1 | score.json, score.md |
| Board | `/launchproof-board` | 3 | board.md, board.json |
| Red team | `/launchproof-redteam` | 3 | threats.json, redteam.md |
| **Gate 1: worth testing** | `/launchproof-blueprint --check` | 1 to 3 | checklist.md |
| Competitors | `/launchproof-competitors` | 8 | competitors.md, five-forces.json |
| Buyer panel | `/launchproof-consumer` | 5, 6, 7 | value-proposition.md, panel/ |
| **Gate 2: worth a real-world test** | `/launchproof-blueprint --check` | 5 to 8 | |
| Pricing | `/launchproof-pricing` | 9 | pricing.md |
| Offer | `/launchproof-offer` | 5 | offer.md |
| CFO | `/launchproof-cfo` | 10, 11 | numbers.json, cfo.md |
| Operations | `/launchproof-ops` | 10 | ops.md |
| Real-world test | `/launchproof-launch` Step 1 | 11 | evidence.json real_test |
| **Gate 3: worth building** | `/launchproof-blueprint --check` | 9 to 11 | |
| Marketing, brand, launch | `/launchproof-marketing`, `/launchproof-brand`, `/launchproof-launch` | 4, 12 | marketing.md, brand.md, launch.md |
| Plan | `/launchproof-blueprint` | 11, 13, 14 | business-plan.md, action-plan.md |
| **Gate 4: ready to launch** | `/launchproof-blueprint --check` | 4, 12 to 14 | |

Everything lives in `launchproof/` in the user's project; every skill reads what
the others wrote.

## How to run it

1. **Open with the map, in a few lines.** Before the first question, tell the
   founder what is coming, in plain words:
   - First, a few questions about you and the idea, then the IdeaGauge score.
   - **Gate 1, worth testing:** a board of five (the frameworks of Alex Hormozi,
     Peter Thiel, Daniel Priestley, Naval Ravikant and Charlie Munger) votes, and
     a red team tries to break the idea. Until then, spend nothing but time.
   - **Gate 2, worth a real-world test:** competitors, your value proposition and
     simulated buyers. Then a small test budget.
   - **Gate 3, worth building:** price, real profit margins, operations and a
     test with real buyers. Then the startup budget.
   - **Gate 4, ready to launch:** marketing, brand, launch, growth, team and the
     14-step business plan.
   You can stop at any gate; stopping early saves money.
2. **Start with people, not documents.** Then `/launchproof-fit`: a few short
   questions, two rounds at most. Then `/launchproof-score`.
3. **After each stage, one short read-out**: the result in one line, what it
   means, and the next stage. Do not dump whole files into the chat; the files are
   there to read.
4. **At each gate, stop.** Run `python3
   "${CLAUDE_SKILL_DIR}/../launchproof-blueprint/blueprint.py" --dir launchproof
   --check`, refresh the checklist with `--checklist`, and show the founder:
   - pass or not, and why, from the tool;
   - what they may now spend on, and what they must NOT spend on yet;
   - the board's kill criteria, and whether any has been hit;
   - the items only they can do (real conversations, the real test, ticking the
     checklist);
   - in two lines, what the next gate involves and what it will ask of them.
   Wait for them before going on.
5. **If a gate fails**, offer the three honest options: rework (the named
   weakness, then re-check), pivot (the same founder, a nearby problem), or stop.
   Never push past a failed gate. Stopping early is the skill doing its job.
6. **Before the buyer panel**, say it is about 100 sub-agent calls and offer
   `--quick` (20 buyers). With `--quick` on this skill, use the quick mode of the
   board-adjacent skills too: `/launchproof-redteam --quick` and
   `/launchproof-consumer --quick`.
7. **Gate 3 needs real buyers.** The panel is simulated. Before any startup money,
   the founder runs the cheapest real test from `/launchproof-launch` Step 1 and
   logs the result in `launchproof/evidence.json`. Help design it, then wait.

## Rules that hold across the pack

- Board members are named ("Charlie Munger's Inversion lens") and apply that
  person's published framework. Their reasoning is the board's own; quotes come
  only from `launchproof-board/quotes.md`, word for word, with the source. No
  invented quotes, no endorsements.
- No invented facts: competitors, prices, reviews and quotes come from public
  sources with links. Estimates are marked as estimates.
- The founder owns their self scores, their checklist ticks and their evidence
  log. Claude proposes; the founder confirms.
- Gates, scores and verdicts come from the tools, never written by hand.
- Not financial, legal or tax advice. Say once where a professional must confirm
  (structure, tax, permits, trademarks).

## Output

The `launchproof/` folder, ending in `business-plan.md` and `action-plan.md`.
Finish each session with one line: the gate reached and the one thing to do this
week.
