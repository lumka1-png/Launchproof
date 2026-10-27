---
name: launchproof-fit
description: >-
  The founder-fit interview that opens Launchproof. Asks the founder a few short
  questions (two rounds at most) about the idea, the problem, why they are the
  one to build it, their time, money, goals and support, then writes the idea
  file and a founder profile: entrepreneur type, the entrepreneurial test, the
  strengths and skill gaps that matter for this business, a SMART goal, personal
  runway and the biases most likely to fool this founder. Based on Steps 1 to 3
  of The Startup Blueprint by Derick van Vuren. Use when the user says "I have a
  business idea", "is this idea right for me", "founder fit", "start
  Launchproof", or before /launchproof-score.
argument-hint: "<the business idea, or leave blank to be asked>"
---

# launchproof-fit

Ideas are plentiful; the question is whether this idea is right for this
founder. An idea becomes an opportunity only when it solves a real problem, can
be executed with the resources at hand, and fits the person building it. This
skill finds out the last two before anyone spends a dollar.

What the user typed after `/launchproof-fit`: `$ARGUMENTS`

## How to ask

- **Two rounds at most, four questions per round, in one message each.** Number
  the questions so the founder can answer in a few lines. Short answers are fine.
- Ask about **past behavior and facts**, not hopes ("how many people have you
  talked to about this problem?", not "do you think people want it?").
- Never score or judge in this skill. Record. The scoring happens in
  `/launchproof-score`.
- If the conversation already answered a question, do not ask it again.

## Round 1: the idea and the founder

1. **The idea in one sentence**, and who it is for (as specific as possible).
2. **The problem**: what pain it removes or what delight it creates, and how the
   customer solves it today. How many potential customers have you actually
   talked to about this problem?
3. **Why you**: your experience, knowledge and network in this field. What do you
   know about this problem that most people do not?
4. **Why this, why now**: what got you interested, how long you have cared about
   it, and what has changed in the market (technology, rules, habits) that makes
   now the time.

## Round 2: resources, goals and support

5. **Money**: how much you can put in without hurting your household, and how
   many months you can cover your own living costs with no income from this.
6. **Time**: hours a week you can give it for the next six months, and whether
   you keep your current job.
7. **Goals**: what success looks like for you in 18 months (income, customers,
   freedom, impact). What would make you stop?
8. **Support and risk**: does your family or partner support this, who could
   mentor you, and how would you feel about losing the money in question 5?

## Step 3: write the idea file

Write `launchproof/idea.md` (the shape every skill reads):

```markdown
# <business name, or a working name>

- What it is: one sentence.
- Who it is for: the target customer, as specific as the founder made it.
- What it sells, at what price: the core product and its price (or "price not set").
- Where and how: city or online, how customers find it, how it is delivered.
- Budget and constraints: money, time, skills, anything already decided.
- The problem: the pain or delight, and today's alternative.
- Evidence so far: conversations held, signups, sales (numbers only, or "none yet").
```

Do not invent a budget, a price, a market size or a competitor. Write "not set"
where the founder did not say.

## Step 4: write the founder profile

Write `launchproof/fit.md`:

1. **Entrepreneur type.** The closest one or two of the types in The Startup
   Blueprint: Innovator, Hustler, Imitator, Researcher, Buyer, Freelancer or
   Artisan, Franchisee, Home Business, Executive Manager, Technology Leader,
   Business Leader, Analyst. One line on why, and what that type tends to do well
   and badly in this kind of business.
2. **The entrepreneurial test.** The founder's evidence on four questions: do
   they see problems as opportunities, are they energized by challenges, do they
   prefer autonomy and initiative, do they learn from failure and keep going.
   Quote their answers; do not grade.
3. **Strengths and gaps for this business.** The five to eight skills this
   business needs most (from the idea, not a generic list), each marked *has it*,
   *can learn it* or *needs a partner or hire*, with the plan for each gap
   (learn, partner, hire, mentor).
4. **Effectuation: what the founder already has.** Their skills, network,
   knowledge and money that point at this idea, and what they could start with
   this week without spending.
5. **The SMART goal.** The 18-month goal rewritten as specific, measurable,
   achievable, relevant and time-bound.
6. **Personal runway.** Months of living costs covered, cash they can risk, hours
   a week. Flag plainly if runway is under six months, or if the cash at risk is
   more than they said they could lose.
7. **The biases most likely to fool this founder.** From the seven founder biases
   in Blueprint Step 3 (optimism, confirmation, sunk cost, IKEA effect, planning
   fallacy, anchoring, small numbers), pick the two or three their answers
   suggest, each with the evidence and one countermeasure. For example: "Talked to
   3 people, all friends: small numbers and confirmation bias. Countermeasure: 10
   problem interviews with strangers before Gate 1."
8. **Open questions** the founder could not answer yet.

## Step 5: start the evidence log

Create `launchproof/evidence.json` if it does not exist. It holds only real-world
evidence the founder reports; Launchproof never fills it with estimates:

```json
{"problem_conversations": 3, "customer_interviews": 0,
 "cash_available": 15000, "personal_runway_months": 8,
 "real_test": null, "notes": ["3 conversations so far, all with friends"]}
```

## Output

`launchproof/idea.md`, `launchproof/fit.md`, `launchproof/evidence.json`. Then
give the founder two lines: the strongest point of fit and the biggest gap. Next:
`/launchproof-score` to score the idea with IdeaGauge, the Business Idea
Evaluator (33 weighted criteria).
