# Launchproof

**Test your business idea before you spend a dollar on it.**

Fifteen Claude skills that take a business idea from the first founder questions
to a gated, actionable business plan. Free, MIT, no signup, no API key, nothing
to connect.

`skills/launchproof` `skills/launchproof-fit` `skills/launchproof-score`
`skills/launchproof-board` `skills/launchproof-redteam`
`skills/launchproof-competitors` `skills/launchproof-consumer`
`skills/launchproof-pricing` `skills/launchproof-offer` `skills/launchproof-cfo`
`skills/launchproof-marketing` `skills/launchproof-brand` `skills/launchproof-ops`
`skills/launchproof-launch` `skills/launchproof-blueprint`

Most new businesses fail for reasons that were visible before day one: no real
need, the wrong founder for the job, a crowded market, margins that never
worked. Founders usually find out after the lease, the inventory and the
website. Launchproof finds out first.

It asks you a few questions to check founder fit, scores the idea with
**IdeaGauge**, puts it before a **board of five** (the Hormozi, Thiel, Priestley,
Naval and Munger frameworks), sends in a **red team** to break it, runs it past
**100 simulated buyers**, has a **CFO** find the real margins, and then builds
your plan on the **14 steps of The Startup Blueprint**, with four money gates
that tell you exactly what you have earned the right to spend on.

So you get clear direction: build it, fix it, pivot it or drop it. And you get
it while the idea has cost you nothing but time.

## How it works: four money gates

```
founder fit -> IdeaGauge score -> board -> red team
                                              |
                              GATE 1  Worth testing?            then spend: research only
                                              |
              competitors -> value proposition -> 100-buyer panel
                                              |
                              GATE 2  Worth a real-world test?   then spend: a small test budget
                                              |
        pricing -> offer -> CFO -> value chain -> REAL buyers (pre-sale, pop-up, waitlist)
                                              |
                              GATE 3  Worth building?            then spend: the startup budget
                                              |
               marketing -> brand -> launch -> growth -> team -> business plan
                                              |
                              GATE 4  Ready to launch and grow?  then spend: launch, legal, hiring
```

Every gate is computed from the evidence, never written by hand. A gate is made
of steps from The Startup Blueprint; a step passes when its checks pass (the
score, the board vote, the red team, the buy rate, the margin, the real test,
the cash) and its must-do checklist items are ticked. Nothing big gets signed
on simulated buyers alone: Gate 3 waits for a real-world test with a success
line written in advance.

Stopping at a gate is not a failure. It is the skill doing its job: you just
kept your money.

## Install

Paste this repo link into Claude and say `install skill`:

```
https://github.com/lumka1-png/launchproof

install skill
```

Or as a plugin, in Claude Code:

```
/plugin marketplace add lumka1-png/launchproof
/plugin install launchproof@launchproof
```

Claude Code namespaces plugin skills, so installed as a plugin they show up as
`/launchproof:launchproof-board` and so on. Copy the folders instead if you want
plain `/launchproof-board`:

```bash
git clone https://github.com/lumka1-png/launchproof.git
cp -r launchproof/skills/launchproof* ~/.claude/skills/
```

Project-local instead of global: copy the same folders into your repo's
`.claude/skills/`. No Claude Code at all? Paste any single `SKILL.md` at the top
of a chat and it runs as a mode. You lose the sub-agents and the Python tools,
but the method works.

The tools need Python 3.8 or newer. Nothing to pip install.

## Start here

```
/launchproof I want to open a matcha bar for office workers in downtown Toronto
```

`/launchproof` runs the whole journey and stops at every gate. Each stage is
also its own skill you can run alone.

## The fifteen

| command | job | what it does |
| --- | --- | --- |
| `/launchproof` | The conductor | Runs every stage in order, stops at each gate, and tells you what you may spend now and what you must not. |
| `/launchproof-fit` | Founder Fit | A few short questions (two rounds at most): the problem, why you, your money, time, goals and support. Writes your founder profile: entrepreneur type, skill gaps and the plan for each, a SMART goal, your personal runway and the biases most likely to fool you. |
| `/launchproof-score` | IdeaGauge | Scores the idea exactly like the IdeaGauge app: 33 weighted criteria (x3 critical, x2 important, x1 supporting) plus your own, pass at 60 with Business Analysis 55+ and Personal Fit 50+. Imports the app's export, then checks every score against the evidence and lowers the optimistic ones, with reasons. |
| `/launchproof-board` | Board of Directors | Five board members, each a sub-agent applying one published framework, score the idea, name what would kill it, vote and set the kill criteria. |
| `/launchproof-redteam` | Red Team | Five attackers (product, competitor, social critic, regulator, reputation) score every weakness from 1 (kill shot) to 5, find the chains where one failure triggers the next, and a blue team builds and prices the defenses. |
| `/launchproof-competitors` | Competitor Scout | Direct competitors, indirect ones and substitutes from public sources, with prices and complaints, every fact linked, plus Porter's 5 Forces and the gap you can own. |
| `/launchproof-consumer` | Consumer Panel | Builds the Value Proposition Canvas, then spins up 100 buyer agents from your target customer and tallies who buys, who doesn't, why, and what would flip a no. |
| `/launchproof-pricing` | Pricing Strategist | Your positioning and pricing method, the acceptable price range from the panel, competitor prices and your margin, and what to test. |
| `/launchproof-offer` | Offer Architect | The offer stack (bonuses, guarantee, real urgency, a name) that answers the panel's objections, re-tested on the panel. |
| `/launchproof-cfo` | CFO | Contribution per sale, the real profit margin, break-even per day, year 1 by month, cash needed, payback and what-ifs. |
| `/launchproof-marketing` | Marketing Director | Positioning, the channels your buyers use, the sales funnel and script, a dated 30-day campaign, ten hooks and the most you can pay for a customer. |
| `/launchproof-brand` | Brand Designer | Name candidates with the trademark, domain and handle checks, a voice, a promise and a brief for the look. |
| `/launchproof-ops` | Operations Manager | Suppliers, staffing, routines, tools, permits, the value chain and a risk register, feeding real costs back to the CFO. |
| `/launchproof-launch` | Launch Lead | The cheapest real-world test first, with a success line written in advance, then the countdown, launch day and the first 30 days. |
| `/launchproof-blueprint` | Business Planner | The 14-step Startup Blueprint: the four gates, your checklist, the Business Model Canvas, growth and team plans, the full eight-section business plan, a lean plan and the action plan for your next gate. |

## The board

| member | framework | the question it asks |
| --- | --- | --- |
| Offers lens | Alex Hormozi, *$100M Offers* | Is this an offer people would feel foolish turning down? |
| Monopoly lens | Peter Thiel, *Zero to One* | Can this own a small market and keep it? |
| Demand lens | Daniel Priestley, *Oversubscribed*, *Key Person of Influence*, *24 Assets* | Can demand be built before the business is built? |
| Leverage lens | *The Almanack of Naval Ravikant* | Does this compound without the founder's hours? |
| Inversion lens | *Poor Charlie's Almanack* (Charlie Munger) | How does this fail, and is that avoidable? |

Each member votes fund, fund if, or pass. The board's disagreements are kept,
and its kill criteria (the results that mean stop) are checked again at every
gate.

## IdeaGauge, the Business Idea Evaluator

`/launchproof-score` uses the scoring model of
[IdeaGauge](https://takeacourse.online/business-idea-evaluator/), the free
Business Idea Evaluator built on The Startup Blueprint. The criteria, weights,
labels and passing rules are generated from the app's own model, and the tests
check the result against the app's math on fifty ideas across every verdict.

| verdict | rule |
| --- | --- |
| Strong, build it | 75+ overall, Business Analysis 55+, Personal Fit 50+ |
| Workable, proceed with focus | 60+ overall, both sections at their minimum |
| Score passes, but a gate fails | 60+ overall, a section under its minimum |
| Needs work | 45 to 59 |
| Back to the drawing board | under 45 |

Already scored your idea in the app? Export your data and run
`/launchproof-score` on the file. Launchproof keeps your scores and adds a
checked score next to each one, so you can see where your optimism is.

## The Startup Blueprint

The plan follows the 14 steps of *The Startup Blueprint: 14 Steps to Building
Your Dream Business* by Derick van Vuren:

1. The Idea · 2. The Entrepreneur · 3. Prepare to Reach Success ·
4. Laying the Foundation · 5. Value Proposition · 6. Find Your Customers ·
7. Market Segmentation · 8. Competition and Porter's 5 Forces · 9. Pricing ·
10. Value Chain · 11. Business Model Canvas and Business Plan · 12. Sell Your
Product · 13. Grow Your Business · 14. Build Your Team

Each step has its question, its automatic checks and a checklist condensed from
the book's Complete Startup Creation Checklist, written to
`launchproof/checklist.md` for you to tick. The book has the why behind every
step; Launchproof does the work and keeps the score.

## An example

A matcha bar in Toronto, iced matcha lattes at $6.50 a cup. This walk-through is
illustrative: the CFO numbers come from the example file in this repo
(`skills/launchproof-cfo/example.json`), so you can run the tools on them; the
other results are invented to show how the gates work, not research on Toronto.

1. **Fit and score.** Six years as a barista manager, 12 problem conversations,
   9 months of personal runway. IdeaGauge: 66, Workable. After checking, "It
   can't be copied" drops from 70 to 35 (anyone can open a matcha bar next door).
2. **Board and red team.** 3 fund if, 1 fund, 1 pass. Kill criterion: fewer than
   50 pre-orders in two weeks. The red team's worst threat: a coffee chain adds
   matcha at $5.25 (2, critical); the defense (a loyalty card and a ceremonial
   grade the chains don't stock) moves it to 4. **Gate 1 passes:** spend on research only.
3. **Competitors and panel.** Four matcha bars and eleven coffee shops in walking
   distance; rivalry and substitutes are high, and nobody does fast pre-ordering.
   40 of 100 simulated buyers buy. **Gate 2 passes:** spend a small test budget.
4. **Price, CFO, real test.** Each cup leaves $4.76 after its own costs,
   break-even is 186 cups a day, the margin at the planned 383 cups is 38%, year
   1 makes $93,926 on operations, and the founder needs $34,092 before it pays
   for itself. A two-week pre-order page gets 63 orders against a line of 50.
   **Gate 3 passes:** now sign the lease.
5. **Launch and plan.** Gate 4 checks the company is registered, the funnel and
   launch are planned, the team is planned, and the cash on hand covers $51,138
   (the CFO's figure times 1.5, the planning-fallacy safety factor from Step 3).

## The tools

Seven of them, all standard-library Python. None touch the network.

```bash
python3 skills/launchproof-score/evaluator.py import ideagauge-export.json > launchproof/score.json
python3 skills/launchproof-score/evaluator.py score launchproof/score.json --out launchproof/score.md
python3 skills/launchproof-redteam/threats.py launchproof/threats.json --out launchproof/redteam.md
python3 skills/launchproof-consumer/panel.py init --customer launchproof/customer.json --pitch launchproof/pitch.md
python3 skills/launchproof-pricing/van_westendorp.py launchproof/panel/answers --price 6.50
python3 skills/launchproof-cfo/unit_economics.py launchproof/numbers.json --out launchproof/cfo.md
python3 skills/launchproof-blueprint/blueprint.py --dir launchproof --check
```

**`evaluator.py`** scores an idea the IdeaGauge way, from the app's export, a list
of scores or a questionnaire, and reports the founder's and the checked verdict
side by side. **`threats.py`** checks the red team and blue team file and decides
whether any threat is still critical. **`panel.py`** deals persona cards from
your target customer, writes one brief per buyer, checks the answers and tallies
them; it never answers for a buyer. **`van_westendorp.py`** turns four price
answers per buyer into the acceptable price range. **`unit_economics.py`**
reports contribution, break-even, margin, year 1, cash needed and payback, every
number traced to an input. **`blueprint.py`** computes the 14 steps and four
gates, keeps your checklist ticks, and compiles the business plan and the action
plan.

```bash
python3 -m unittest discover -s tests -v
```

## Fine print

**The board applies published frameworks. It is not those people.** The five
lenses are short summaries, in our words, of ideas from *$100M Offers* by Alex
Hormozi, *Zero to One* by Peter Thiel with Blake Masters, *Oversubscribed*, *Key
Person of Influence* and *24 Assets* by Daniel Priestley, *The Almanack of Naval
Ravikant* by Eric Jorgenson, and *Poor Charlie's Almanack* edited by Peter
Kaufman. The board never speaks as them, quotes them or claims they endorse
anything. This project is not affiliated with any of them.

**Scores are judgments, not measurements.** IdeaGauge tells you what to test
first, not whether the business will work.

**The consumer panel is simulated buyers, not customers.** It is a fast, cheap way
to find objections, segments and wording before you spend. Language models lean
agreeable, so read the buy rate as an upper bound. That is why Gate 3 waits for
real buyers. Panel answers are research; never use them as testimonials.

**The numbers are only as good as the inputs.** The CFO marks every estimate as an
estimate and asks for real quotes. Check costs with suppliers and the structure,
payroll and tax with an accountant.

**Research uses public sources, with links.** No invented competitors, prices,
reviews or quotes. No scraping against a site's terms.

**Not financial, legal or tax advice.** Permits, trademarks and claims depend on
where you are. The skills tell you what to check and where; a professional
confirms it.

## Files

```
skills/launchproof/              SKILL.md (the conductor)
skills/launchproof-fit/          SKILL.md
skills/launchproof-score/        SKILL.md, evaluator.py, criteria.json
skills/launchproof-board/        SKILL.md, lenses.md
skills/launchproof-redteam/      SKILL.md, threats.py
skills/launchproof-competitors/  SKILL.md
skills/launchproof-consumer/     SKILL.md, panel.py, customer.example.json, pitch.example.md
skills/launchproof-pricing/      SKILL.md, van_westendorp.py
skills/launchproof-offer/        SKILL.md
skills/launchproof-cfo/          SKILL.md, unit_economics.py, example.json
skills/launchproof-marketing/    SKILL.md
skills/launchproof-brand/        SKILL.md
skills/launchproof-ops/          SKILL.md
skills/launchproof-launch/       SKILL.md
skills/launchproof-blueprint/    SKILL.md, blueprint.py, steps.json
tests/                           the tests for every tool
```

Your own files live in `launchproof/` in your project. The skills read each
other's.

## Credit

Made by Derick van Vuren, author of *The Startup Blueprint* and creator of
IdeaGauge, [takeacourse.online](https://takeacourse.online). Derick consults on
business development for new ventures at ITRI, Taiwan's technology incubator.

Launchproof is built on [the Founder skill](https://github.com/Jakeschincariol/founder-skill)
by Jake Schincariol ([opusjake.ai](https://opusjake.ai)), used under its MIT
license: the competitor scout, consumer panel, pricing, offer, CFO, marketing,
brand, operations and launch skills and their tools come from it, adapted.

Get the book: [*The Startup Blueprint: 14 Steps to Building Your Dream Business*](https://www.amazon.com/Startup-Blueprint-Steps-Building-Business-ebook/dp/B0FJ9Q8S6P).

## License

MIT. Take it, change it, ship it. See `LICENSE` and `NOTICE`.
