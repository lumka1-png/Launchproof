---
name: launchproof-score
description: >-
  IdeaGauge, the Business Idea Evaluator. Scores a business idea exactly the way
  the IdeaGauge app does: 33 weighted criteria scored 0 to 100 (19 Business
  Analysis, 14 Personal Fit) plus the founder's own criteria, weights x3
  critical, x2 important, x1 supporting, passing at 60 overall with Business
  Analysis at least 55 and Personal Fit at least 50, strong at 75. Imports the
  app's export file or its scores, then checks every score against the evidence,
  lowers optimistic ones with a reason, and decides Gate 1: whether the idea is
  worth testing at all. Use when the user says "score my idea", "evaluate my
  business idea", "rate this idea", "I used IdeaGauge", or after /launchproof-fit.
argument-hint: "[path to an IdeaGauge export, or 33 scores in the app's order]"
---

# launchproof-score

Most founders skip this and start building. Twenty minutes with the evaluator
tells you whether an idea is worth testing at all, and which part to test first.

What the user typed after `/launchproof-score`: `$ARGUMENTS`

Tool in this folder (`EVAL` below means exactly this):

```bash
python3 "${CLAUDE_SKILL_DIR}/evaluator.py" <command>
```

`criteria.json` in this folder is generated from the IdeaGauge app's own
criteria model: the questions, the order, the weights, the slider labels, the
help text and the passing rules. The tool's math matches the app's, rounding
included. Every criterion is worded so that higher is better: a crowded market,
an easily copied idea or a likely failure scores LOW.

## Step 0: say what is coming

Before the first question, tell the founder in a few lines what Launchproof will
do: this score first, then a board of five and a red team (Gate 1, worth
testing), then competitors and simulated buyers (Gate 2, a small test budget),
then price, profit and a test with real buyers (Gate 3, the startup budget), then
the launch and the full plan (Gate 4). Each gate says what they may spend money
on once it passes. The same summary is at the end of the report the tool writes.

## Step 1: get the founder's own scores

Three ways in, best first:

1. **The app's export.** In IdeaGauge, the data menu exports a JSON backup. Ask
   the founder to add it to the project, then:
   `EVAL import <file> --idea "<name>" > launchproof/score.json`
   This brings in the pitch, all scores, removed default criteria and custom
   criteria.
2. **The app's numbers.** The 33 scores in the app's order:
   `EVAL from-list "<numbers>" --idea "<name>" > launchproof/score.json`
3. **The questionnaire here**, or a draft from the interview (see "How to show
   the questions" below). If you draft the scores from `launchproof/fit.md` and
   `launchproof/idea.md`, mark them as drafts and let the founder change any.
   The founder owns the self scores.

### How to show the questions

- **One table** with all 33 questions, in the app's order, with these columns:
  `Question number | Question | What a high score means | Score`. Fill "What a
  high score means" from the slider labels in `criteria.json` (for example
  "Crowded = low, Wide open = high"). Do **not** show the weights (x1, x2, x3)
  anywhere; they still count inside the tool.
- **Explain the terms** in plain words under the table, using the `glossary` in
  `criteria.json`: blue ocean and red ocean, entry barrier, effectuation,
  substitutes, competitive advantage, scalable, predictable revenue and the
  rest. One line each.
- Accept short answers: "all fine", or "Question 29: 40, Question 24: 60".

### Five of their own criteria

IdeaGauge lets founders add what matters to them personally. Ask for **five**
criteria of their own, each a short yes-or-no question they can score 0 to 100,
and offer the `own_examples` in `criteria.json` as ideas (personal freedom,
membership based, meaningful for you, run it from home, fits my family
schedule, start with little money, uses my skills, could sell it one day, good
for my community...). The three app defaults (freedom, membership, meaningful)
count toward the five; the founder may keep, drop or replace them.

Record defaults they drop under `removed_own`, and new ones under `custom` with
a short `key`, the question as `q`, `w: 2`, and their score as `self`. They
count in the overall score, as in the app.

## Step 2: check every score

You are the consultant IdeaGauge's AI Insight prompt asks for: rigorous but
encouraging, challenging optimistic self-assessments with evidence. For each
criterion, compare the self score with `launchproof/idea.md`,
`launchproof/fit.md`, `launchproof/evidence.json` and public facts you can check
(with links). Where you disagree, write a `verified` score and a one-line `note`:

- **Lower** a score the evidence does not support. Common ones: "Do I solve a
  need?" at 90 with no customer conversations; "It can't be copied" high for a
  business anyone could open next door; "Is the space crowded?" high when a map
  search shows ten competitors; "Probability of failure" high (low risk) in a
  category where most new entrants close.
- **Raise** a score the founder undersold (a network mentioned in passing, a rare
  skill).
- Leave `verified` empty when you agree. Never change the founder's `self` score.

Focus hardest on the questions that carry the most weight in `criteria.json` (w: 3); they move the score most, but do not show the weights to the founder. Then:

```bash
EVAL score launchproof/score.json --out launchproof/score.md
```

The report shows the verdict on the founder's scores and on the checked scores,
bar charts of the sections and of the six dimensions (Demand, Moat, Market,
Economics, Founder fit, Execution), a radar chart image (`score-chart.svg`, next
to the report), every change with its reason, one table of every question with
a bar for each score, the terms explained, and what happens next. When showing
results in chat, use the same single-table style: question number, question,
the founder's score, the checked score. No weights.

## Step 3: the read-out

Add to the top of `launchproof/score.md`:

1. **The headline**: the checked score, the verdict and whether Gate 1 passes,
   with the reasons if it does not.
2. **A SWOT** grounded in this idea and its industry, with named competitors and
   links where you can: strengths (top scores), weaknesses (lowest and red),
   opportunities (trends, gaps), threats (who copies it, what substitutes it).
3. **Three to five industry-specific recommendations**, each tied to a weak
   criterion and the Launchproof skill that tests it.
4. **Action items for this week**, free or nearly free.

Close on an honest, encouraging note. A low score now is cheap; a low score
after the lease is signed is not.

## Gate 1, part 1: worth testing?

The gate passes when the checked verdict is **Workable** or **Strong**: overall
at least 60, Business Analysis at least 55 and Personal Fit at least 50. The tool
decides; never round a failing number up. If it fails:

- **Score passes, but a gate fails**: a high total cannot make up for a broken
  foundation. Fix that section first.
- **Needs work** (45 to 59): name the weakest of the most important questions and the evidence that
  would raise each; re-score after evidence, not after a change of heart.
- **Back to the drawing board** (under 45): if Personal Fit is strong but
  Business Analysis is weak, the founder is right and the idea is wrong; suggest
  adjacent problems the same founder could solve. Say plainly that stopping now
  saved their money.

## Output

`launchproof/score.json`, `launchproof/score.md`, `launchproof/score-chart.svg`. Then one line: the score, the
verdict and the gate. Next: `/launchproof-board` if it passes, otherwise the
rework list.
