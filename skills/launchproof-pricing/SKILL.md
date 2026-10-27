---
name: launchproof-pricing
description: >-
  Finds the price buyers will actually pay. Reads the consumer panel's four price
  answers per buyer into a Van Westendorp price-sensitivity range (too cheap, a
  bargain, getting expensive, too expensive), sets it against what competitors
  really charge and against the CFO's margin, and recommends a price, a price
  ladder (good / better / best) and an opening offer to test. Use when the user
  says "how much should I charge", "price this", "is $X too expensive", "pricing
  strategy", "what price", or after the consumer panel.
argument-hint: "[current price]"
---

# launchproof-pricing

Price is the fastest lever on the margin and the one founders guess most. This
skill sets it from three things you can check: what buyers said, what competitors
charge, and what the business needs to earn.

Tool in this folder:

```bash
python3 "${CLAUDE_SKILL_DIR}/van_westendorp.py" launchproof/panel/answers --price 6.50 --out launchproof/pricing-curve.md
```

## Step 1: what buyers said

If `/launchproof-consumer` ran, every buyer answered four price questions. Run the
tool on `launchproof/panel/answers` (or a CSV with the columns `too_cheap, cheap,
expensive, too_expensive` from real surveys, which beat simulated answers every
time). It reports:

| point | meaning |
| --- | --- |
| PMC | below this, too many think it is too cheap to be good |
| OPP | the price with the least resistance either way |
| IPP | where as many call it a bargain as call it expensive |
| PME | above this, too many will not buy at all |

PMC to PME is the acceptable range. If the panel has not run, say so and offer to
run `/launchproof-consumer --quick` first. Do not invent a range.

## Step 2: what competitors charge

From `launchproof/competitors.md` (or look them up now, from their own public price
pages, with links): the price of the nearest substitutes for the same job. Note
what each price includes, so you compare like with like. A matcha latte is
compared with other matcha lattes and with the coffee it replaces, not with a tea
bag.

## Step 3: what the business needs

From `launchproof/numbers.json`: the variable cost per unit and the break-even. Run the
CFO's tool at two or three candidate prices to see the margin and break-even at
each:

```bash
python3 "${CLAUDE_SKILL_DIR}/../launchproof-cfo/unit_economics.py" launchproof/numbers.json --price 7.00
```

## Step 4: decide

Write `launchproof/pricing.md`:

0. **The position and the pricing method (Blueprint Step 9).** Which of the four
   positioning strategies this business takes (cost leadership, differentiation,
   focused cost leadership or focused differentiation), where it sits on the
   price/quality matrix (premium, penetration, economy, or skimming, which is
   rarely sustainable), and which pricing method sets the price (markup,
   break-even, going rate or perceived value). Never a random guess. Avoid
   chasing the middle: trying to be premium and cheap at once.
1. **The price**, and why: where it sits in the acceptable range, against the
   competitors, and the margin it gives (from the tool, not a guess).
2. **The ladder**, if the business can have one: a good / better / best (size,
   bundle, subscription, membership) with a reason to step up each rung.
3. **The opening offer**: an intro price or bonus for launch that does not train
   buyers to wait for discounts, with an end date.
4. **What to test with real buyers**: two prices inside the range and how to test
   them (two landing pages, a pre-sale at each, A/B on the menu board).
5. The panel's verbatim price objections (top three), so marketing can answer them.

## Rules

- Price answers from simulated buyers pick what to test. They are not proof.
- Never price below variable cost to "buy" customers without saying so, and how
  long the CFO says the business can afford it.
- No fake anchors: no "was $X" price that was never charged.

## Output

`launchproof/pricing-curve.md`, `launchproof/pricing.md`. If the price changed, update
`launchproof/numbers.json` and re-run `/launchproof-cfo`. Next: `/launchproof-offer`.
