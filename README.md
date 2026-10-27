# Launchproof

**Test your business idea before you spend a dollar on it.**

Sixteen Claude skills that take a business idea from the first founder questions
to a gated, actionable business plan, plus **Launchproof Light** for a quick
assessment and a brainstorm deck. Free, MIT, no signup, no API key, nothing
to connect.

`skills/launchproof` `skills/launchproof-fit` `skills/launchproof-score`
`skills/launchproof-board` `skills/launchproof-redteam`
`skills/launchproof-competitors` `skills/launchproof-consumer`
`skills/launchproof-pricing` `skills/launchproof-offer` `skills/launchproof-cfo`
`skills/launchproof-marketing` `skills/launchproof-brand` `skills/launchproof-ops`
`skills/launchproof-launch` `skills/launchproof-blueprint`
`skills/launchproof-light`

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
/launchproof I want to start a freelance AI automation and consulting business for small accounting firms
```

`/launchproof` runs the whole journey and stops at every gate. Each stage is
also its own skill you can run alone.

## Launchproof Light: the quick version

No time for the full journey? `/launchproof-light` gives a fast, to-the-point
read on an idea and a PowerPoint deck to put in front of your team.

```
/launchproof-light A subscription service that delivers fresh pet food to busy dog owners in Taipei
```

1. **You type the idea.** No interview. Anything missing (price, customer) is
   assumed and listed on the deck.
2. **Eight agents run at once:** the five board members (with real quotes, word
   for word from the quote bank), a red team, eight simulated buyers, and a
   market scan of real competitors with sources.
3. **A computed quick verdict:** Go, Go with conditions, or Rethink, from the
   board's scores and votes, never written by hand.
4. **An 11-slide brainstorm deck** (`launchproof-light/brainstorm.pptx`): the
   verdict, the board's votes and recommendations, what is strong and what could
   kill it, customer objections, the market and the gap, six questions for the
   team, and three cheap tests for this week.

It takes a few minutes. When the team wants to go deeper, run the full
`/launchproof`.

## The sixteen

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
| `/launchproof-light` | Quick Assessment | One idea in, eight agents at once (board, red team, buyers, market), a computed verdict and an 11-slide PowerPoint deck for a team brainstorm. |
| `/launchproof-blueprint` | Business Planner | The 14-step Startup Blueprint: the four gates, your checklist, the Business Model Canvas, growth and team plans, the full eight-section business plan, a lean plan and the action plan for your next gate. |

## The board

| member | framework | the question it asks |
| --- | --- | --- |
| Offers lens | Alex Hormozi, *$100M Offers* | Is this an offer people would feel foolish turning down? |
| Monopoly lens | Peter Thiel, *Zero to One* | Can this own a small market and keep it? |
| Demand lens | Daniel Priestley, *Oversubscribed*, *Key Person of Influence*, *24 Assets* | Can demand be built before the business is built? |
| Leverage lens | *The Almanack of Naval Ravikant* | Does this compound without the founder's hours? |
| Inversion lens | *Poor Charlie's Almanack* (Charlie Munger) | How does this fail, and is that avoidable? |

Each member votes fund, fund if, or pass, gives the main reason and one
recommendation, and backs them with a real quote from that person, taken word for
word from a sourced quote bank (`skills/launchproof-board/quotes.md`), for
example *Charlie Munger: "Invert, always invert."* The board's disagreements are
kept, and its kill criteria (the results that mean stop) are checked again at
every gate.

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

You also add five criteria of your own (personal freedom, working from home,
fitting your family schedule...), as in the app. Every term (blue ocean,
effectuation, entry barrier and so on) is explained in plain words, and the
report shows your score as bar charts and a radar chart of six dimensions:
Demand, Moat, Market, Economics, Founder fit and Execution.

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

A freelance AI automation and consulting business: a solo founder builds AI
workflows (client intake, document processing, follow-up emails) for small
accounting firms, sold as a $2,500 monthly retainer. This walk-through is
illustrative: the CFO numbers come from the example file in this repo
(`skills/launchproof-cfo/example-ai-consulting.json`), so you can run the tools
on them; the other results are invented to show how the gates work, not market
research.

1. **Fit and score.** Eight years as an operations manager at an accounting
   firm, self-taught in automation tools, 11 problem conversations with firm
   owners, 8 months of personal runway. IdeaGauge: 68, Workable. After
   checking, "It can't be copied" drops from 45 to 30 (any freelancer can learn
   the same tools) and "Do I solve a need?" from 75 to 55 (owners complain about
   admin hours, but nobody has paid yet). Still 67, still Workable.
2. **Board and red team.** 3 fund if, 1 fund, 1 pass. The Leverage lens warns
   that a pure hours business is a job, not an asset; the Demand lens asks for a
   niche where the founder is a known name. Kill criterion: fewer than 2 paid
   pilots from 30 discovery calls. The red team's worst threat: the firms'
   accounting software ships the same automations built in (2, critical); the
   defense (specialize in the workflows between tools, which no single vendor
   owns, and sell outcomes, not setups) moves it to 4. **Gate 1 passes:** spend
   on research only.
3. **Competitors and panel.** Generalist automation agencies, freelancers on
   marketplaces and do-it-yourself tools; rivalry and substitutes are high, but
   nobody specializes in small accounting firms. 34 of 100 simulated firm owners
   buy; the top objection is data security. **Gate 2 passes:** spend a small test
   budget.
4. **Price, CFO, real test.** Each client-month leaves $1,785 after its own costs
   (AI usage, platform seats, contractor hours, fees), break-even is 3 clients,
   the margin at the planned 8 clients is 46%, year 1 makes $40,545 on top of
   the founder's $4,000 monthly draw, the $5,100 startup spend is earned back in
   month 7, and the founder needs $9,945 before it pays for itself. A paid pilot
   offer gets 3 firms signed against a line of 2. **Gate 3 passes:** now build
   the website and the service package.
5. **Launch and plan.** Gate 4 checks the business is registered with contracts
   and a data-protection policy in place, the funnel and launch are planned, the
   first contractor is planned, and the cash on hand covers $14,918 (the CFO's
   figure times 1.5, the planning-fallacy safety factor from Step 3).

## The tools

Eight of them, all standard-library Python. None touch the network.

```bash
python3 skills/launchproof-score/evaluator.py import ideagauge-export.json > launchproof/score.json
python3 skills/launchproof-score/evaluator.py score launchproof/score.json --out launchproof/score.md
python3 skills/launchproof-redteam/threats.py launchproof/threats.json --out launchproof/redteam.md
python3 skills/launchproof-consumer/panel.py init --customer launchproof/customer.json --pitch launchproof/pitch.md
python3 skills/launchproof-pricing/van_westendorp.py launchproof/panel/answers --price 2500
python3 skills/launchproof-cfo/unit_economics.py launchproof/numbers.json --out launchproof/cfo.md
python3 skills/launchproof-blueprint/blueprint.py --dir launchproof --check
python3 skills/launchproof-light/deck.py skills/launchproof-light/example.deck.json --out brainstorm.pptx
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
plan. **`deck.py`** computes Launchproof Light's quick verdict, checks every board
quote against the quote bank, and writes the brainstorm deck as a PowerPoint file
with no libraries needed.

```bash
python3 -m unittest discover -s tests -v
```

## Fine print

**The board applies published frameworks. It is not those people.** Each seat
is named after the person whose framework it applies, but the reasoning and the
recommendations are the board's own. Quotes are real, published lines copied
word for word from the sourced quote bank, never invented. The five lenses are
short summaries, in our words, of ideas from *$100M Offers* by Alex
Hormozi, *Zero to One* by Peter Thiel with Blake Masters, *Oversubscribed*, *Key
Person of Influence* and *24 Assets* by Daniel Priestley, *The Almanack of Naval
Ravikant* by Eric Jorgenson, and *Poor Charlie's Almanack* edited by Peter
Kaufman. The board never writes as them or claims they endorse anything. This project is not affiliated with any of them.

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
skills/launchproof-board/        SKILL.md, lenses.md, quotes.md
skills/launchproof-redteam/      SKILL.md, threats.py
skills/launchproof-competitors/  SKILL.md
skills/launchproof-consumer/     SKILL.md, panel.py, customer.example.json, pitch.example.md
skills/launchproof-pricing/      SKILL.md, van_westendorp.py
skills/launchproof-offer/        SKILL.md
skills/launchproof-cfo/          SKILL.md, unit_economics.py, example.json, example-ai-consulting.json
skills/launchproof-marketing/    SKILL.md
skills/launchproof-brand/        SKILL.md
skills/launchproof-ops/          SKILL.md
skills/launchproof-launch/       SKILL.md
skills/launchproof-blueprint/    SKILL.md, blueprint.py, steps.json
skills/launchproof-light/        SKILL.md, deck.py, example.deck.json, lenses.md, quotes.md
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
