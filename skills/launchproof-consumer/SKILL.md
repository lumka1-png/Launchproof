---
name: launchproof-consumer
description: >-
  The consumer panel. Spins up a swarm of buyer sub-agents (default 100, --quick
  for 20) trained on the user's target customer, each with a different income,
  age, buying behavior and objection, shows every one the same pitch, and runs
  the business through 100 buyer scenarios to see who buys, who doesn't, and why.
  Tallies the answers into buy rates by segment, the reasons people pass in their
  own words, what would flip a no, and price answers for launchproof-pricing. Use when
  the user says "would people buy this", "test it on customers", "run the
  consumer panel", "simulate buyers", "who is my customer", or "validate demand".
argument-hint: "[--n 100 | --quick] [--seed S]"
---

# launchproof-consumer

The craziest part of the pack. Instead of guessing whether people will buy, you
ask a hundred of them, each one a sub-agent playing a specific buyer drawn from
your target customer. You are the moderator. You never answer for a buyer.

What the user typed after `/launchproof-consumer`: `$ARGUMENTS`

## The tool

All bookkeeping goes through `panel.py` in this skill's folder:

```bash
python3 "${CLAUDE_SKILL_DIR}/panel.py" <command>
```

Below, `PANEL` means exactly that. If the path is not expanded, use the base
directory Claude Code printed for this skill. State lives in `launchproof/panel/`.

## Step 1: the target customer

Write `launchproof/customer.json` (shape: `customer.example.json` in this folder):

- `business`, and `target`: who the customer is, in one specific line.
- `segments`: 2 to 4 groups with a `share` and an `income` range [low, high].
- `behaviors`: 4 to 8 buying behaviors with a `share` and a `how` line
  (daily regular, deal hunter, reads every review, loyal to a competitor...).
- `objections`: the 4 to 8 doubts this kind of buyer really has.
- `habits` (optional): everyday context lines that make a buyer concrete.

Ground it in something real. Use what the user knows about their customers, and
if `/launchproof-competitors` ran, the complaints in `launchproof/competitors.md`. If the
user has real customer data (interviews, reviews, survey answers), prefer it to
your guesses and say which parts are guesses. Show the user the profile in a few
lines and let them correct it before you deal: a wrong customer makes the whole
panel wrong.

## Step 2: the value proposition, then the pitch

First write `launchproof/value-proposition.md` (Blueprint Step 5), from the
customer profile, the competitor complaints and what the founder said:

1. **The canvas.** Customer side: the jobs the customer is trying to get done,
   their pains, the gains they want. Value side: the products and services, the
   pain relievers, the gain creators. Mark which pains and gains the offer
   addresses and which it does not.
2. **The statement**, in the Blueprint formula: "My <product or service> helps
   <target customer> to <solve a problem> by providing <benefit 1>, <benefit 2>,
   <benefit 3>. Unlike competitors, I <differentiate>."
3. **The test**: clear (no jargon), relevant (a real pain), unique (something the
   competitors do not say), credible (backed by evidence or experience). Mark each
   one met or not met.

Then write `launchproof/pitch.md`: what a buyer would actually see. The product, the price,
where and how to get it, any opening offer. Three to six plain lines, no
superlatives, nothing the business cannot deliver. Every buyer sees exactly this.

## Step 3: deal and run

```bash
PANEL init --customer launchproof/customer.json --pitch launchproof/pitch.md --n 100
PANEL prompts
```

`init` deals the persona cards (same seed, same cards; the seed is recorded).
`prompts` writes one brief per buyer and lists them in waves of 10. For each wave,
send ONE message with one Agent tool call per buyer in that wave (the Agent tool
is called Task in older Claude Code versions):

- `subagent_type`: `general-purpose`
- `description`: `panel <id>`
- `prompt`: `Read <brief path> and follow it exactly. It is your whole brief.`

Wait for the whole wave before the next one. Claude Code runs about 10 tool calls
at once by default, so 100 buyers is 10 waves. After the last wave:

```bash
PANEL check      # lists missing or broken answers
PANEL prompts    # rewrites briefs for those only; run them once more
PANEL tally
```

If a buyer printed its JSON in its reply instead of writing the file (it happens),
file its own reply with `PANEL save <id>` and the reply on stdin; `save` refuses
anything that is not a valid answer. A buyer that fails twice is left out and
counted in the results. Never write an answer for a buyer yourself.

Before a 100-buyer run, tell the user it is 100 sub-agent calls and suggest
`--quick` (20 buyers) for a first look. Sub-agents write one file each into
`launchproof/panel/answers/`; in the default permission mode that is one approval per
file, so suggest accept-edits mode (Shift+Tab) for the run.

## Step 4: read it to the user

`PANEL tally` writes `launchproof/panel/results.md` and `results.json`. Give the user:

1. The headline: "40 buy · 60 pass" and the buy rate.
2. Who buys and who doesn't: the segment and behavior rows that differ most.
3. Why they pass: the top three reasons with one quote each, as written.
4. What would flip a no: the most repeated answers.
5. One sentence on what to change before spending money, and which skill does it
   (pricing, offer, marketing).

## Honest limits, say them once

These are simulated buyers. They are good at surfacing objections, segments and
wording you had not thought of, and bad at predicting real conversion: language
models lean agreeable, so treat the buy rate as an upper bound. Confirm the big
calls with real people (a waitlist, a pre-sale, a landing page with a price)
before signing anything. Do not present panel quotes as customer testimonials.

## The brief every buyer gets

`panel.py` fills the card into a fixed template (see `BRIEF` in the script): who
the buyer is (name, age, segment, income, buying behavior, a habit, the doubt
that comes to mind), the pitch word for word, an instruction not to be agreeable
and not to invent facts, and the exact JSON to write: buys, purchases in the first
month, a reason code, the reason in their own voice, their main objection, what
would change their mind, and four price answers (too cheap, a bargain, getting
expensive, too expensive). Never edit a brief for one buyer.

## Output

`launchproof/customer.json`, `launchproof/value-proposition.md`, `launchproof/pitch.md`, `launchproof/panel/` (cards, briefs,
answers, results). Next: `/launchproof-pricing` reads the price answers,
`/launchproof-offer` and `/launchproof-marketing` read the objections.
