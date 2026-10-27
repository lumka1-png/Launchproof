---
name: launchproof-board
description: >-
  Your board of directors. Puts a business idea in front of a five-member board,
  each a sub-agent reading the idea through one published framework: the Offers
  lens (from Alex Hormozi's $100M Offers), the Monopoly lens (from Peter Thiel's
  Zero to One), the Demand lens (from Daniel Priestley's Oversubscribed, Key
  Person of Influence and 24 Assets), the Leverage lens (from The Almanack of
  Naval Ravikant) and the Inversion lens (from Poor Charlie's Almanack by Charlie
  Munger). Each member scores the idea, names the risks that would kill it and
  votes fund, fund with conditions, or pass. Use when the user says "test my
  business idea", "would this work", "pressure-test this", "what would a board
  say", "is this a good business", or after /launchproof-score.
argument-hint: "<the business idea, or leave blank to use the conversation>"
---

# launchproof-board

The first meeting. Before anyone builds a website or signs a lease, five board
members tear the idea apart, each from a different angle, and vote. This is
Blueprint Step 3's outside board: the people who check the founder's thinking
for bias and set the kill criteria.

What the user typed after `/launchproof-board`: `$ARGUMENTS`. If that is blank,
take the idea from the conversation.

## The rule about the five names

The lenses are summaries of **published frameworks**, nothing more. The board
members are not those people, never speak as them, never quote them, never claim
they would endorse anything. Write "the Demand lens", never "Daniel Priestley
says". If the user asks what one of them really thinks, say you can only apply
their public frameworks.

## Step 0: the idea file

Everything in the Launchproof pack reads `launchproof/idea.md` in the user's
project. `/launchproof-fit` normally writes it. If it does not exist, write it
now from the conversation:

```markdown
# <business name, or a working name>

- What it is: one sentence.
- Who it is for: the target customer, as specific as the user can make it.
- What it sells, at what price: the core product and its price.
- Where and how: city or online, how customers find it, how it is delivered.
- Budget and constraints: money, time, skills, anything already decided.
```

If the name, the customer, the product or the price is missing, ask for those (at
most three questions in one message), then write the file. Do not invent a
budget, a market size or a competitor.

## Step 1: brief the board

Write `launchproof/board/brief.md`: the idea file, plus `launchproof/fit.md` and
`launchproof/score.md` if they exist (the founder profile and the evaluator
score), plus anything else the user said that a stranger would need. **Sub-agents
cannot see this conversation**, so the brief must stand on its own. Do not add
your own opinion of the idea to it.

## Step 2: convene

Launch five sub-agents in ONE message (Agent tool, `subagent_type:
general-purpose`, one per member), each told: `Read launchproof/board/brief.md
and launchproof-board's lenses.md (path below), apply ONLY the <lens> lens, and
write your memo to launchproof/board/<lens>.md.` The lenses are `offers`,
`monopoly`, `demand`, `leverage` and `inversion`. The lens file is `lenses.md` in
this skill's folder (`${CLAUDE_SKILL_DIR}/lenses.md`; if that path is not
expanded, use the base directory Claude Code printed for this skill).

Each memo, in this shape:

```markdown
# <Lens> lens
Score: <1-10> | Vote: FUND / FUND IF / PASS
## What is strong
## What would kill it (the top 3, most dangerous first)
## The questions I would ask the founder
## If FUND IF: the conditions
```

## Step 3: the chair's summary

Read the five memos (they are short) and write `launchproof/board.md`:

1. The vote, e.g. "3 fund if, 1 fund, 1 pass", and the average score.
2. The risks more than one member raised: these go first.
3. Every condition, merged, as a checklist the rest of the pack can tick off
   (the CFO, the consumer panel and pricing will test most of them).
4. **The kill criteria**: three to five measurable results that would mean stop
   or pivot (for example "fewer than 20 waitlist signups in 30 days", "contribution
   per unit under $2"). These come from the risks, are written before any test is
   run, and are checked again at every Blueprint gate.
5. One paragraph: the strongest version of this business the board can see.
   It may differ from what the user pitched; say so plainly.

Then write `launchproof/board.json`, which the Blueprint gates read:

```json
{"members": [
  {"lens": "offers", "score": 7, "vote": "FUND IF"},
  {"lens": "monopoly", "score": 5, "vote": "PASS"},
  {"lens": "demand", "score": 6, "vote": "FUND IF"},
  {"lens": "leverage", "score": 8, "vote": "FUND"},
  {"lens": "inversion", "score": 6, "vote": "FUND IF"}
 ],
 "kill_criteria": ["fewer than 20 waitlist signups in 30 days"]}
```

Scores and votes are copied from the memos, never adjusted. Keep the members'
disagreements. A board that agrees on everything was not doing its job.

## Rules

- Score the business, not the founder. (The founder's fit is scored separately by
  `/launchproof-fit` and `/launchproof-score`.)
- No made-up facts. If a lens needs a number nobody has yet (market size, cost of
  acquiring a customer), name it as an open question and say which skill answers
  it (`/launchproof-competitors`, `/launchproof-consumer`, `/launchproof-cfo`).
- A PASS is a result, not a failure. Say it plainly.

## Output

`launchproof/idea.md`, `launchproof/board/` (brief and five memos),
`launchproof/board.md`, `launchproof/board.json`. Then say the vote in one line
and suggest the next step: `/launchproof-redteam` to attack the idea before you
spend anything on it.

## Where the pack goes next

```
fit -> score -> board -> redteam -> competitors -> consumer -> pricing -> offer
    -> cfo -> marketing -> brand -> ops -> launch -> blueprint
```

Every skill can also run on its own; each reads whatever is already in
`launchproof/`.
