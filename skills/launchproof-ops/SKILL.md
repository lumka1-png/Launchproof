---
name: launchproof-ops
description: >-
  Your operations manager. Works out how the business actually runs on day one:
  suppliers and what they cost, who works when, the step-by-step routines for
  opening, serving or shipping and closing, the tools to run it, the licenses and
  permits to check, and a risk register with what to do when each thing goes
  wrong. Feeds real costs back to the CFO. Use when the user says "how do I run
  this", "operations", "suppliers", "staffing", "SOPs", "what do I need to open",
  "permits", or "day one".
argument-hint: "[city or country]"
---

# launchproof-ops

A plan that works on paper fails at 7am on a Monday. This skill makes sure the
first day, week and month can actually be run, and that the CFO's numbers include
what running it really costs.

## Step 1: what the business has to do every day

From `launchproof/idea.md`, `launchproof/offer.md` and `launchproof/numbers.json`, write the
daily cycle as a list of steps from first thing to last (for a café: deliveries,
prep, open, serve, clean, cash up, order; for an online store: orders in, pick,
pack, ship, returns, support). Mark which steps a customer sees.

## Step 2: suppliers

For every input in the CFO's variable costs and every piece of equipment: two or
three real suppliers the user can contact, their public prices or how to get a
quote, minimum orders, lead times and payment terms. Link the sources. Where only
a quote will tell, say so and add it to the open questions. If a real price
differs from `launchproof/numbers.json`, update it and say the CFO should re-run.

## Step 3: people

Who does what, when: a weekly rota for the planned volume and for the slow first
month. The roles, the hours, and the wage assumption (from the user, or a public
source for the local minimum and typical pay, linked). Payroll costs beyond wages
vary by country; flag them for the accountant.

## Step 4: routines (SOPs)

Short, numbered routines for the moments that make or break the business: opening,
the core service or fulfilment, handling a complaint, closing, and a weekly
reorder. Each fits on one page someone could follow on their first day.

## Step 5: tools

The smallest stack that runs it: payments, point of sale or store, scheduling,
bookkeeping, inventory. Real products with their published prices, and why each.

## Step 6: licenses, permits and insurance

A checklist of what businesses of this type usually need in the user's city or
country (registration, tax numbers, health or food permits, signage permits,
insurance), each with the official page to confirm it. Say plainly that rules
differ by place and change, and the user must confirm each with the authority or a
professional. Not legal advice.

## Step 7: the value chain (Blueprint Step 10)

Map the activities as a value chain. Primary: inbound logistics, operations,
outbound logistics, marketing and sales, service. Support: firm infrastructure,
people, technology, procurement. For each, the monthly cost (from the CFO's
numbers), the value it creates for the customer, and one decision: keep and
strengthen (it carries the positioning), optimize (costly, little value),
outsource or cut. Name the two or three activities that make the business
different; those are where money goes first.

## Step 8: risk register

The ten things most likely to go wrong (a supplier runs out, a key person is sick,
the card terminal fails, a bad review, a slow month), each with how likely, how
bad, and the plan.

## Output

`launchproof/ops.md` (with the value chain), plus updated `launchproof/numbers.json` if real costs changed. Next:
`/launchproof-launch`.
