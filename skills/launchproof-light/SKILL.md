---
name: launchproof-light
description: >-
  Launchproof Light: a fast, to-the-point assessment of a business idea that
  ends in a PowerPoint deck for a team brainstorm. The user types the idea; no
  interview and no full scoring. Eight agents run at once: a board of five
  (the Hormozi, Thiel, Priestley, Naval and Munger frameworks, with real quotes),
  a red team, a panel of eight simulated buyers and a market scan with sources.
  Claude merges their findings, the tool computes a quick verdict (Go, Go with
  conditions or Rethink) and builds an 11-slide deck: the verdict, the board's
  votes and recommendations, strengths and risks, customer objections, the
  market, questions for the team and three cheap tests. Use when the user says
  "quick assessment", "launchproof light", "fast take on this idea", "make a
  deck about this idea for my team", or wants a brainstorm deck rather than the
  full Launchproof journey.
argument-hint: "<the business idea, in a sentence or two>"
---

# launchproof-light

Fast and to the point. One idea in, one brainstorm deck out, in a few minutes.
No founder interview, no 33 questions, no gates: the full `/launchproof` is for
that. This is for the moment a team wants a sharp first read and a deck to argue
about.

What the user typed after `/launchproof-light`: `$ARGUMENTS`

Tool in this folder (`DECK` below means exactly this):

```bash
python3 "${CLAUDE_SKILL_DIR}/deck.py" launchproof-light/deck.json --out launchproof-light/brainstorm.pptx
```

If `${CLAUDE_SKILL_DIR}` is not expanded, use the base directory Claude Code
printed for this skill. Work files go in `launchproof-light/` in the user's
project.

## Speed rules

- **Do not interview.** Take the idea as given. Ask one short question only if
  the idea is too vague to tell what is sold and to whom; otherwise assume, and
  list every assumption (customer, price, place, channel) so it shows on slide 2.
- **One round of agents**, all launched in a single message. No second rounds.
- **Short outputs.** Every agent has word limits; the deck has no room for essays.
- Say once at the start: "About 8 agents, a few minutes. You'll get a PowerPoint
  deck for your team."

## Step 1: the brief

Write `launchproof-light/brief.md`, standing on its own (sub-agents cannot see
this conversation): the idea in one sentence, the customer, the offer, the price,
where and how, and the assumptions you made, marked as assumptions. Nothing else,
and no opinion of the idea.

## Step 2: eight agents, one message

Launch all eight in ONE message (Agent tool, `subagent_type: general-purpose`).
Each writes one JSON file and replies "done".

**The board (five agents).** One per seat:

| seat | person | lens |
| --- | --- | --- |
| `offers` | Alex Hormozi | Offers |
| `monopoly` | Peter Thiel | Monopoly |
| `demand` | Daniel Priestley | Demand |
| `leverage` | Naval Ravikant | Leverage |
| `inversion` | Charlie Munger | Inversion |

Prompt: `Read launchproof-light/brief.md and, in <this skill's folder>, lenses.md and
quotes.md. You hold <person>'s seat: apply ONLY the <lens> lens. Write
launchproof-light/board/<seat>.json: {"person", "lens", "score" (1 to 10), "vote"
("FUND", "FUND IF" or "PASS"), "reason" (max 25 words), "strengths" (2 short
lines), "risks" ([{"risk" max 15 words, "severity" 1 to 5, 1 = kill shot}], max 2),
"recommendation" (max 20 words), "quote", "source"}. The quote must be copied
word for word from <person>'s section of quotes.md, with its source, or left
empty if none fits. Never invent or reword a quote, and never write your own
recommendation as <person>'s words. Be honest: a PASS is a useful result.`

**The red team (one agent).** `Read launchproof-light/brief.md. Attack this idea
as a ruthless competitor, a regulator, a critic and a product tester. Write
launchproof-light/redteam.json: {"risks": [{"risk" max 15 words, "severity" 1 to 5
(1 kill shot, 2 critical, 3 significant, 4 moderate, 5 minor), "from": "Red team"}]},
the five most dangerous, realistic not fantasy.`

**The buyers (one agent).** `Read launchproof-light/brief.md. Play eight different
potential buyers from the target customer, each with a different budget, habit and
doubt; decide for each, separately and honestly, whether they would buy at the
stated price. Language models lean agreeable: resist it. Write
launchproof-light/customers.json: {"buy" (how many of the 8 buy), "total": 8,
"objections" (top 3, in buyers' words), "flip" (top 3 things that would change a
no), "voices": [2 x {"who": "Simulated buyer: <one-line profile>", "says": max 20
words}]}.`

**The market scan (one agent).** `Read launchproof-light/brief.md. Using web search,
find 3 to 5 real competitors or alternatives a buyer would use instead. Public
sources only; never invent a company, price or fact. Write
launchproof-light/market.json: {"competitors": [{"name", "what" (max 10 words),
"price" (as published, or "Not published"), "source" (the URL)}], "gap" (max 25
words: what nobody does well, or "No clear gap found")}. If you cannot search the
web, use categories of alternatives without names or prices, and say so in "gap".`

## Step 3: merge into the deck file

Read the eight files and write `launchproof-light/deck.json` in the shape of
`example.deck.json` in this folder:

- `idea`, `one_liner`, `date` (today), `glance`, `assumptions` from the brief.
- `board`: the five board files, copied as they are (score, vote, reason,
  recommendation, quote, source). Never change a score or a vote.
- `strengths`: the best four or five from the board, merged where they repeat.
- `risks`: the board's and the red team's, merged where they repeat (keep the
  lower severity and name both sources in `from`), the five most dangerous.
- `customers` and `market`: as the agents wrote them.
- `questions`: six open questions for the team, each tied to a risk, an objection
  or a board recommendation ("Which single workflow would a firm pay for first?").
  Questions to argue about, not ones with an obvious answer.
- `tests`: three cheap tests for this week, each with a measurable success line
  and its cost, cheapest first.

## Step 4: build the deck

```bash
DECK launchproof-light/deck.json --verdict
DECK launchproof-light/deck.json --out launchproof-light/brainstorm.pptx
```

The verdict is computed: the quick score is the board's average times 10; **Go**
needs 70 or more, at most one PASS and no kill-shot risk; **Go with conditions**
needs 50 or more and at most two PASS votes; anything else is **Rethink**. Never
write a verdict by hand. The tool refuses any quote that is not word for word in
`quotes.md`: fix the quote or empty it, then build again.

The 11 slides: title with the verdict, the idea at a glance, the verdict, the
board's votes, the board in their words, strengths and risks, customer voices,
the market, questions for the team, three tests, and next steps.

## Step 5: hand it over

Tell the user, in four lines: the verdict and quick score, the board's vote
split, the single biggest risk, and where the deck is
(`launchproof-light/brainstorm.pptx`). Offer the full `/launchproof` if the team
wants to go deeper.

## Rules

- Board seats are named by the person, but the reasoning is the board's own; it
  applies their published frameworks. Quotes only from `quotes.md`, word for
  word, with the source.
- The buyers are simulated and the verdict is a quick read: the deck says so.
  Not financial, legal or tax advice.
- Market facts only from public sources with links. No invented competitors,
  prices or reviews.

## Output

`launchproof-light/` with `brief.md`, `board/` (five files), `redteam.json`,
`customers.json`, `market.json`, `deck.json` and `brainstorm.pptx`.
