# Agentic Playbook — shared plan

**The authoritative design document is [`PLAN.md`](../PLAN.md). Read it before starting any task
in this epic.** It holds the locked decisions (deliverable, reader, tone, structure), the full
book outline, and the play template. This file tracks execution and accumulates decisions made
during the build.

Every task in this epic reads this file before starting and updates it before finishing. It is
the only thing that crosses context boundaries between agents.

## Goal

Ship *The Agentic Playbook* as a markdown book in this repo: a plays-first, dry-and-wry field
guide that a working developer can open at any single play and act on it the same afternoon.

## Non-goals

- **Not a sales pitch for agentic tools.** Part III exists to say where they fail, honestly.
- **Not a manager's guide or an executive overview.** The reader writes code daily.
- **Not a tool reference.** Products appear as worked examples inside durable problem headings,
  never as section titles. No chapter is named after something with a version number.
- **Not an introduction to LLMs.** The reader already uses these tools; the book is about getting
  good at them, not about what they are.
- **Not a rendered site, for now.** Markdown readable on GitHub is the deliverable. Static-site
  rendering is a possible later step, explicitly out of scope until the prose exists.
- **Not a rewrite of `notes/raw/`.** That material is frozen provenance.

## Locked decisions (do not relitigate without asking)

- Markdown book in this repo, chapters as files.
- Reader: working developers already using agentic tools daily.
- Tone: dry and wry — sharp asides in the framing, never inside instructions.
- Plays-first: framing ~15%, plays ~60%, failure modes ~15%, next waves ~10%.
- Tools are examples *inside* plays, never section headings.

## Conventions

- Book chapters live in `book/`, research briefs in `notes/research/`, raw ideation in
  `notes/raw/` (frozen — do not edit).
- Every play uses the template defined by the style-guide task: Problem → The play → Worked
  example → Failure mode → Checklist.
- Research briefs are cited notes, not prose. Writers draw from them.
- Any build/helper scripts are Python, not Node.
- Prose wraps at 100 columns; diagrams are mermaid, never ASCII art.
- Repo-wide conventions are recorded as cards in `cards/` and indexed from the root `CLAUDE.md`.
- `make html` and `make pdf` collect the book and render it; `make check` reports orphans and
  missing files. Output goes to `build/`, which is gitignored and never committed. See
  [`cards/building-the-book.md`](../cards/building-the-book.md).

## Milestones

| # | Milestone | Board item | Status |
|---|---|---|---|
| 1 | Consolidate ideation into an authoritative plan | `956e4f5ab7db` | ✅ done |
| 2 | Agentic setup — `CLAUDE.md`, cards, shared plan | `5a8f313f87cc` | ✅ done |
| 3 | Style guide, play template, book scaffolding | `a06026d4e603` | ✅ done |
| 4 | Research: agent context and tooling landscape | `bb1d30e52adc` | ✅ done |
| 5 | Research: orchestration and workflow landscape | `6f9d83a67e1a` | ✅ done |
| 6 | Research: evidence, failure modes, token economics | `8701744c4454` | ✅ done |
| 7 | Part I — The Argument | `e93293bfd014` | ✅ done |
| 8 | Context play suite | `655473ee5afb` | ✅ done |
| 9 | Harness play suite | `9366c3c324b5` | ✅ done |
| 10 | Orchestration play suite | `3c6b76dedb59` | ✅ done |
| 11 | Verification & Trust play suite | `4858fbdecdf4` | ⬜ blocked on 3, 6 |
| 12 | Economics play suite | `bffa217221ed` | ⬜ blocked on 3, 6 |
| 13 | Team play suite | `cdd27e440781` | ⬜ blocked on 3 |
| 14 | Part III — Where It Struggles | `c1416f44c483` | ⬜ blocked on 3, 6 |
| 15 | Part IV — Next Waves, plus appendices | `bec9accd89be` | ⬜ blocked on 3 |
| 16 | Editorial pass — one voice, one book | `934259dc8038` | ⬜ blocked on all writing |
| 17 | Run every worked example for real, re-capture output | `3b61a6a1a684` | ⬜ blocked on 8–13 |
| 18 | Book build — collect the chapters, render a PDF | `76d95ae050df` | ✅ done |

Milestone 3 was the real critical path: with several authors and a specific comic register,
"we'll harmonise it later" is how a book ends up with three voices. It is done, and the nine
writing tasks are unblocked.

### Follow-ups raised during the build

Work that was not in the original sequence. These are listed separately rather than appended to the
table above, so that the numbered milestones keep the numbers other entries in this file refer to.

| Board item | What | Status |
|---|---|---|
| `aed2433867e0` | Reassessment after milestones 8 and 18 — contracts hardened, five prose defects fixed | ✅ done |
| `01dce54a3f88` | HTML book — `make html` made a first-class output: stylesheet, sidebar contents, browser-drawn diagrams | ✅ done |
| `878a5eb98f8b` | PDF lacked mermaid: render via `npx` fallback, and size diagrams to the page | ✅ done |
| `6b0110f76388` | Add a 100-column / style lint to `make check`, after three authors wrote the same one | ⬜ open, blocked on nothing |
| `fce3cee8fa34` | Trim three marginal budget overruns; editorial-pass work | ⬜ blocked on `aed2433867e0` |
| `9dd4d6b84b80` | Define *skill*, *card*, *harness* on first use, per Part I's promise | ⬜ blocked on the Harness suite |
| `57772ad900e3` | Verify the seven primary sources that resisted automated fetch | ⬜ blocked on milestone 6 |
| `f94b88e05069` | Milestone 19 — audit of the author's own posts; found them unspent, fixed the cause, filed the three chapters that owe them | ✅ done |
| `703e507c86aa` | Write the cards play — the Context suite's fourth | ⬜ blocked on milestone 8 and `f94b88e05069` |
| `0bdccc346bd4` | Thread preparation-vs-execution into Part I | ⬜ blocked on milestone 7 and `f94b88e05069` |
| `5e0f39858134` | Check Part IV Wave #2 carries the feature-first argument | ⬜ blocked on milestone 15 |
| `f986730f7a1f` | Verify the MCP incident citations in the Harness suite against primary sources | ⬜ blocked on milestone 9 |

## Current state / handoff

`book/` now exists and holds the three constraint documents every author works within:

| File | Owns |
|---|---|
| [`book/STYLE.md`](../book/STYLE.md) | Voice, the outright bans, four sample paragraphs with passing and failing versions, formatting mechanics, how to name a failure mode. |
| [`book/TEMPLATE-play.md`](../book/TEMPLATE-play.md) | The five-heading play contract with word budgets per heading, the evidence rules for worked examples, a copy-paste skeleton, and one fully written specimen play. |
| [`book/README.md`](../book/README.md) | Directory layout, file naming, the table of contents that is the book's only ordering mechanism, and the cross-reference convention. |

**If you are a writing task, read `book/STYLE.md` and `book/README.md` before your first
sentence, and `book/TEMPLATE-play.md` too if you are writing plays.** The register is defined in
examples on purpose — match the samples rather than re-deriving it from adjectives.

Three things every writing task must do, which are easy to miss:

1. **Add your row to the table of contents in `book/README.md`**, in the same commit as the file.
   Nothing else encodes order, and an untabled file is an orphan to the editorial pass.
2. **Create your own part directory.** None of them exist yet; there are no `.gitkeep` files by
   design. `book/README.md` has the layout table.
3. **Append any failure mode you name to the running log below**, and check it first. Two names
   for one phenomenon is the defect the editorial pass is least able to fix cheaply.

Part directories are numbered (`part-1-argument/`, `part-2-plays/…`) because part order is locked;
files inside them are content-named and never numbered.

### The author's own material

**Read this if you are writing any part of the book.** The book has a commissioning author who
has already published on this subject, and that material is not a third-party source to be
weighed. It is the book's own argument, written earlier and shorter.

Two posts, both by the repo owner:

| Post | The argument | Where it belongs |
|---|---|---|
| [Cards](https://memention.com/blog/2026/05/25/Cards.html) | Two-tier context: a ~15-line always-loaded `CLAUDE.md` index of natural-language triggers, plus self-contained `cards/` loaded on demand. "The only real rule is self-containment. One card, one load, no chains." Also the *rocket-launch mindset* — the project is ready before the agent starts; preparation mode and execution mode are distinct. | Context suite (`703e507c86aa`) and Part I (`0bdccc346bd4`) |
| [The unit of work](https://memention.com/blog/2026/05/29/The-unit-of-work.html) | An agent's unit of work is a capability, not a layer. Layer-first scatters a feature across six files and the agent reassembles it every session. "For us, reading and writing code was the expensive part… For an agent writing is cheap, and the expensive thing is behavior it can't see." | Part IV Wave #2 (`5e0f39858134`), already named in *Scope a task to fit the window* |

Summaries are in [`notes/research/agent-context-files.md`](../notes/research/agent-context-files.md)
and [`notes/research/tooling.md`](../notes/research/tooling.md) [20][21]. Read the posts anyway;
the briefs compress them.

**Attribution convention.** Absorb this material into the book's own voice. Do not cite it in-line
as an external source — "the argument is made well in *The unit of work*" reads oddly in a book by
the person who made it. URLs go in the appendix's further reading. This is the one case where the
"cite the source" reflex produces worse prose.

**Part IV authors specifically:** Wave #2 is defined in `notes/raw/idea.md` as "refactoring
projects, optimize for full agent development". *The unit of work* is what that refactor consists
of — feature-first layout, locality of behaviour, explicit over invisible control flow, and the
nuance that cross-cutting concerns still belong in shared infrastructure as trustworthy black
boxes rather than hidden magic. Write it into `bec9accd89be`; `5e0f39858134` exists only to check
that you did.

`notes/research/` now exists. Milestone 4 filled it with six files — a hub brief plus five
subject briefs, because five subjects in one file would have made a writer chasing token-pricing
figures read a survey of MCP security to find them:

| File | Feeds |
|---|---|
| [`notes/research/tooling.md`](../notes/research/tooling.md) | The commissioned hub: cross-cutting findings, the standardised-vs-vendor-habit table, the staleness table, the full source list |
| [`agent-context-files.md`](../notes/research/agent-context-files.md) | Context suite — `CLAUDE.md`, `AGENTS.md`, `.claude/rules/`, the cards pattern |
| [`skills.md`](../notes/research/skills.md) | Harness suite — `SKILL.md`, progressive disclosure, skill vs. prompt vs. tool |
| [`mcp.md`](../notes/research/mcp.md) | Harness suite — what a server exposes, the 2026-07-28 spec, trust boundaries |
| [`token-filtering.md`](../notes/research/token-filtering.md) | Context suite, and the Economics suite's best cautionary tale |
| [`permissions-and-sandboxing.md`](../notes/research/permissions-and-sandboxing.md) | Harness suite — what is enforced and what merely reads like enforcement |

**If you are writing the Context or Harness suite, start at `notes/research/tooling.md`.** Three
things in it will change what you write:

1. **Cite vendor documentation, not blog posts, on context files.** Claude Code has read
   `AGENTS.md` natively since v2.1.277; a wall of confident mid-2026 posts says otherwise and is
   simply stale. The hub brief names one of them explicitly as an example rather than a source.
   **This rule is about third-party claims of fact, and it does not apply to the author's own
   posts.** Those are not evidence to be corroborated, they are the book's own material — see
   "The author's own material" below. Milestone 19 found that this line, read literally, had
   filtered them out of the Context suite entirely.
2. **The staleness table in `tooling.md` ranks every finding by how fast it rots**, with a
   suggested hedge for each. Use it rather than re-deriving where the line is; it is consistent
   with `book/STYLE.md` on volatile facts.
3. **Each brief ends with a `## Concrete example we can lift`** written to be dropped into a
   *Worked example* heading. They are illustrative-but-correct per the locked decision — real
   commands and real file contents, no invented captured output.

Milestone 5 added seven more files on the same hub-plus-briefs pattern, feeding the Orchestration
suite:

| File | Feeds |
|---|---|
| [`notes/research/orchestration.md`](../notes/research/orchestration.md) | The commissioned hub: the standardised-vs-vendor-habit table, four cross-cutting gotchas, the staleness table, the worked-example map |
| [`subagents.md`](../notes/research/subagents.md) | *Decompose into subagents* — isolation, fan-out cost, Cognition's reversal |
| [`langchain-langgraph.md`](../notes/research/langchain-langgraph.md) | *Make the control flow deterministic* — the framework/runtime split and the production complaints |
| [`visual-workflow-tools.md`](../notes/research/visual-workflow-tools.md) | Same play, plus Team — n8n's licence, review and test story |
| [`control-flow.md`](../notes/research/control-flow.md) | Same play — the decision-criteria table and the reliability evidence |
| [`parallel-agents-and-collisions.md`](../notes/research/parallel-agents-and-collisions.md) | *Work in parallel without collisions* — the collision taxonomy and measured conflict rates |
| [`single-agent-wins.md`](../notes/research/single-agent-wins.md) | All three Orchestration plays, and Economics' *Know when not to use an agent* |

**If you are writing the Orchestration suite, start at `notes/research/orchestration.md`.** Four
things in it will change what you write:

1. **The suite's spine is that the vendors are more conservative than their users.** Anthropic,
   OpenAI and Cognition all counsel starting with one agent, and the strongest controlled comparison
   found five of six multi-agent systems losing to a single-agent baseline. The book gets to be
   sceptical while citing the vendors *in support*, which is a rare and valuable position.
2. **Use the removability test rather than picking a side.** Anthropic contradicts itself across
   three posts on whether scripted orchestration is prudence or fragility, and the tension is not
   resolvable. What is portable is their own framing: every harness component encodes an assumption
   about what the model cannot do yet, so the design question is whether you can delete it cheaply
   later.
3. **The hub's worked-example map shows the five scenarios do not collide**, so all three
   Orchestration plays can be drawn from this pass without repeating a scenario.
4. **A list of things that did not survive verification** is in the hub's gaps section — two
   widely-quoted low-code statistics, a scaffolding quote attributed to a named engineer, and a
   rewritten derivative of Anthropic's post circulating on GitHub under a plausible name. Check it
   before citing anything in this area from memory.

Milestone 6 added seven more files on the same pattern, and closes the research programme. It feeds
the Verification & Trust suite, the Economics suite, and Part III:

| File | Feeds |
|---|---|
| [`notes/research/evidence.md`](../notes/research/evidence.md) | The commissioned hub: the two findings that shape the rest, the consolidated contested-claims index, the consolidated **do not cite** list, the staleness triage, the worked-example map |
| [`productivity-evidence.md`](../notes/research/productivity-evidence.md) | Part III and Economics — the METR RCT and its failed follow-up, DORA, the optimistic RCTs, the 2026 agentic telemetry |
| [`failure-modes.md`](../notes/research/failure-modes.md) | Part III — benchmark contamination, reward hacking, long-horizon degradation, the security shape |
| [`review-practice.md`](../notes/research/review-practice.md) | *Review code you did not write* — the classic review research read at source, automation bias, agent-PR review on GitHub in 2026 |
| [`verification.md`](../notes/research/verification.md) | *Make the agent prove it* — the fakeability ranking, LLM-generated test quality, tests that pass rather than verify |
| [`accountability.md`](../notes/research/accountability.md) | *Decide who signs off* — the DCO split, trailer conventions, copyright, regulation, vendor indemnities |
| [`token-economics.md`](../notes/research/token-economics.md) | All three Economics plays — live prices across three vendors, caching, subscription billing, what drives spend |

**If you are writing Verification & Trust, Economics, or Part III, start at
`notes/research/evidence.md`.** Five things in it will change what you write:

1. **Almost nothing published about "AI coding productivity" is about agents.** Every RCT in the
   field measures autocomplete, inline completion, or chat. The genuinely agentic evidence is
   telemetry and quasi-experiments, none of it randomised. METR tried to run the missing RCT in late
   2025 and abandoned the design, because 30–50% of developers would no longer submit tasks they
   wanted AI for. That collapse is itself the finding, and it is the licence for every hedge the
   book makes. The hub reproduces a table mapping the five most-misquoted findings to the sentence
   each gets turned into; use it.
2. **The cost lands as displaced review capacity, not as defects.** Three independent studies agree:
   throughput up, merge and revert rates flat, review coverage down, cycle time up. DORA's term for
   it — the **verification tax** — is the one the book should adopt. Do not write the Economics
   suite as if the risk were bugs.
3. **The consolidated `## Do not cite` list is the longest artefact in the pass and the most
   important.** Roughly forty figures across six subjects trace only to vendor marketing,
   mislabelled survey years, laundered secondary write-ups, or a search engine's synthesis. Several
   are the first result a search returns, including *every* published SWE-bench per-instance dollar
   figure and the famous "200–400 lines in under 60 minutes" review rule, which appears nowhere in
   the study it is attributed to. Read it before writing a sentence containing a number.
4. **`verification.md` ranks verification signals by how hard they are to fake.** It is the single
   most reusable artefact in the pass, and its two rules generalise: fakeability tracks whether the
   evasion shows up in the diff, and the strongest signals are the ones the agent did not author.
5. **Twelve claims are flagged as contested with both halves carried**, indexed in the hub. Two are
   load-bearing enough to name here: nobody has measured whether putting the agent's plan in the PR
   helps the reviewer or anchors them, and nobody has established whether "the human owns the diff"
   distributes responsibility or merely creates a moral crumple zone. Neither may be resolved by
   assertion.

Milestone 7 created `book/part-1-argument/` and wrote all three chapters. Part I is complete at
roughly 4,150 words — 1,525 / 1,445 / 1,180 — which sits inside the ~15% share once Part II exists
at its planned size. It also produced an eighth research brief,
[`notes/research/convergence-history.md`](../notes/research/convergence-history.md), because the
historical analogy needed sourcing and no research pass covered it.

| File | Owns |
|---|---|
| [`before-git-before-scrum-before-this.md`](../book/part-1-argument/before-git-before-scrum-before-this.md) | The historical analogy, the three ways it breaks, and the book's own framing as "not the consensus" |
| [`the-four-areas-reweighted.md`](../book/part-1-argument/the-four-areas-reweighted.md) | The durable map, with one section per area and a mermaid summary of the four shifts |
| [`what-this-book-assumes-about-you.md`](../book/part-1-argument/what-this-book-assumes-about-you.md) | The stated reader, the evidence posture, how to read the book, what it costs, what will go stale |

**Three things in Part I constrain later tasks, and two of them are easy to break by accident:**

1. **Part I promises things the appendices and the plays have to deliver.** *What this book assumes
   about you* states that terms are defined on first use and collected in a glossary (appendices
   task), that every play is self-contained under the five headings with no required order, and that
   **where a play has an exchange rate — what the reader gives up — it states it.** That last one is
   a soft contract on all six suite authors; a play that lists only benefits now contradicts Part I
   in print.
2. **Part I deliberately names no failure mode**, and one sentence depends on that staying true.
   *Before Git, before Scrum, before this* uses the mid-run-overwrite phenomenon from
   `notes/research/failure-modes.md` as its example of missing vocabulary, and says in so many words
   that **"there is no name for it"**. If Part III names it — and it should — that sentence has
   to be rewritten in the same pass, or the book contradicts itself two parts apart. Flagged for
   the editorial pass as well.
3. **Part I adopts DORA's *verification tax*** as the term for review effort displaced by agent
   output, in *The four areas, re-weighted*. Economics and Part III should use the same words rather
   than coining a second term for it.

Milestone 8 created `book/part-2-plays/` and its first suite directory, `context/`, with a suite
opener and three plays at roughly 250 / 1,145 / 1,190 / 1,100 words. It is the first suite written,
so it is also the first test of the template, and three things in it constrain the suites that
follow:

| File | Owns |
|---|---|
| [`context/index.md`](../book/part-2-plays/context/index.md) | The suite opener — names *signal over noise* as the suite's single idea and frames the three plays as that move at three layers |
| [`write-the-brief-the-agent-reads.md`](../book/part-2-plays/context/write-the-brief-the-agent-reads.md) | Project context files: what belongs, what bloats, the portable `AGENTS.md` + import setup, and verifying the brief loaded |
| [`starve-the-context.md`](../book/part-2-plays/context/starve-the-context.md) | Deliberate reduction, just-in-time loading, and the paired-run method for measuring any filtering tool |
| [`scope-a-task-to-fit-the-window.md`](../book/part-2-plays/context/scope-a-task-to-fit-the-window.md) | Unit-of-work sizing, external requirement lists, the stop rule, and file-based handoff between sessions |

1. **Four failure modes are now registered, three of them new.** The Context suite claimed **the
   Context Landfill** as `book/STYLE.md` invited, and coined **the Brief That Never Arrived**, **the
   Flattering Dashboard**, and **the Permanent Near Miss**. Check the registry before naming
   anything adjacent — in particular, the Orchestration suite's "a subagent inherits the written
   brief but none of the conversation" is arguably the same phenomenon as the Brief That Never
   Arrived and may want that name rather than a second one.
2. **The `rtk` worked example is spent.** It carries *Starve the context*'s Worked example, with the
   JetBrains and Quesma figures dated and versioned. Economics may cite the figures, but should not
   build *Understand what you are paying for* around the same scenario; the running log below flags
   a swap.
3. **Three plays per suite held comfortably**, and no fourth was wanted. That is one data point
   against the open play-count question rather than an answer to it.

Milestone 9 added `harness/`, the second suite, at roughly 296 / 1,150 / 1,081 / 1,129 words. It
spends the permission-matching material milestone 4 flagged as Harness-owned, and it names the
instructions-are-not-enforcement gotcha that the Context suite deliberately left unnamed.

| File | Owns |
|---|---|
| [`harness/index.md`](../book/part-2-plays/harness/index.md) | The suite opener — names *every extension of reach is an extension of what can go wrong, bought together* as the suite's one idea, and frames the three plays as the harness, the competence added to it, and the reach added to it |
| [`choose-your-harness.md`](../book/part-2-plays/harness/choose-your-harness.md) | The four parts of a harness, the three enforcement layers, permission rules as ergonomics, the sandbox as the only boundary that holds |
| [`package-repeatable-expertise.md`](../book/part-2-plays/harness/package-repeatable-expertise.md) | Skills: when a procedure earns an artefact, what a situation-shaped boundary looks like, the `description` as the routing table, progressive-disclosure arithmetic |
| [`wire-in-the-outside-world.md`](../book/part-2-plays/harness/wire-in-the-outside-world.md) | MCP: connecting on a boundary, scoped credentials, tool descriptions as authored context, the union threat model, pinning against rug pulls |

Four things in it constrain later tasks:

1. **Three failure modes are registered**, all new: **the Paper Fence**, **the Unsummoned Skill**,
   and **the Instruction You Did Not Write**. The first is milestone 4's gotcha (a), named here as
   the Context suite expected; note it is deliberately *not* the same as the Brief That Never
   Arrived, and *Package repeatable expertise* says so in print so the editorial pass can check it.
2. **The permission-matching example is spent.** The `deny` rule that does not stop `git 'push'
   origin main`, and the sandbox configuration that replaces it, carry *Choose your harness*'s
   Worked example. Another suite may cite the mechanism; none should build an example on it.
3. **Vendor-specific mechanics are scoped in the sentence that uses them.**
   `notes/research/permissions-and-sandboxing.md` warns that only one harness was examined, so the
   play names Claude Code and a version where the specifics are that vendor's, and states the
   general shape — instructions, client-enforced rules, kernel-enforced sandbox — where it is
   general. Any later play touching permissions should keep that split rather than implying a
   cross-tool standard that does not exist.
4. **The suite defines *harness* and *skill* on first use**, which is two of the three terms board
   item `9dd4d6b84b80` is waiting on. *Card* is still undefined, and belongs to the Context suite's
   fourth play (`703e507c86aa`).

Milestone 10 added `orchestration/`, the third suite, at roughly 298 / 1,057 / 1,144 / 1,122 words.
It spends the whole of milestone 5's research pass and leans on its sceptical spine: the suite
argues for less orchestration than the reader is being sold, while citing the vendors in support.

| File | Owns |
|---|---|
| [`orchestration/index.md`](../book/part-2-plays/orchestration/index.md) | The suite opener — names *every piece of orchestration is machinery encoding an assumption about what the model cannot do, and assumptions expire* as the suite's one idea, and frames the three plays as that on three axes: across context, across steps, across the working tree |
| [`decompose-into-subagents.md`](../book/part-2-plays/orchestration/decompose-into-subagents.md) | Fan out to read and single-thread the write, tool allowlists as mechanical isolation, fixed return formats that can be cross-checked, and holding tokens constant before believing a fan-out |
| [`make-the-control-flow-deterministic.md`](../book/part-2-plays/orchestration/make-the-control-flow-deterministic.md) | Splitting on reversibility and horizon, irreversible actions performed by code, model-driven work at bounded leaves, what LangGraph and n8n each actually sell, and the removability test |
| [`work-in-parallel-without-collisions.md`](../book/part-2-plays/orchestration/work-in-parallel-without-collisions.md) | Partition-plus-escape-clause briefs, worktrees as ergonomics rather than a boundary, landmine files, overlap preflight, and sequential integration with the suite run on the merged tree |

Five things in it constrain later tasks:

1. **Three failure modes are registered**, all new: **the Tidy Summary**, **the Load-Bearing
   Scaffold**, and **the Clean Merge**. The first is milestone 5's gotcha (a). Gotcha (c) is the
   Clean Merge. Gotcha (b) — the brief travels, the conversation does not — was **used and
   deliberately left unnamed**: it appears as step 5 of *Decompose into subagents* rather than as a
   second name next to the Brief That Never Arrived, which the handoff note flagged as a possible
   collision. Gotcha (d) is spent as a checklist item, not a name.
2. **The suite uses `meridian`, a Ruby freight-booking platform whose monorepo holds nineteen
   deployable services**, across all three worked examples. It is deliberately Ruby: the sharpest
   collision in the pass is a rename that survives every test and fails at runtime, which a type
   checker would have caught in a typed language. Three suites still need their own project.
3. **All five worked-example scenarios from the hub's map are now spent or deliberately declined.**
   The migration-ordering and rename collisions stayed in one example, as the hub predicted they
   could; no fourth play was wanted, which is a second data point against the play-count question.
   The refund-agent scenario was declined as a product-building example in a book for people
   building software, and the n8n triage scenario was re-cast onto `meridian`'s own dependency-bump
   pipeline so that one project carries the suite.
4. **Octomind is cited nowhere.** Its primary page was unreachable during milestone 5 and the
   framework-removal genre has no credible successor, so the suite makes the build-versus-adopt
   argument structurally — a checkpoint is a save point, not a supervisor — rather than leaning on
   an unverified two-year-old post. The outstanding verification lead stays outstanding and is now
   cited by nothing.
5. **The Economics suite still owns `single-agent-wins.md`.** This suite cites it once, for the
   five-of-six protocol-matched comparison, and does not build an example on it. *Know when not to
   use an agent* has the material intact, including Anthropic's "optimizing single LLM calls… is
   usually enough", which is its epigraph and is unspent.

**Next up:** Verification & Trust (`4858fbdecdf4`), Economics (`bffa217221ed`) and Part III
(`c1416f44c483`), unblocked by milestone 6; and Team (`cdd27e440781`), which is free to run. **All
research is done, Part I and three suites are written, and every remaining writing task is
unblocked.**

**If you are the Team suite or Part I:** an archive pass (`df5ff268416d`) filed a late author
fragment at [`notes/raw/team-adoption-fragment.md`](../notes/raw/team-adoption-fragment.md) and
extracted the three things in it that the rest of `notes/raw/` does not already say — mandate
without method, a working agreement with an expiry date, and adoption-by-decree read as
surveillance. Read the running-log entry rather than the fragment; the entry says which play each
one lands in and which locked decision it does *not* override.

Milestone 18 added the build: `make pdf` collects every chapter the table of contents names, in
that order, and renders one PDF. It is a convenience, not a second deliverable — markdown on
GitHub is still the book, and nothing has to be built to read it.

| File | Owns |
|---|---|
| [`scripts/build_book.py`](../scripts/build_book.py) | The whole build: reads the table of contents, concatenates, shifts headings, rewrites cross-references to internal anchors, optionally renders mermaid, calls pandoc. One file, no dependencies. |
| [`scripts/book-metadata.yaml`](../scripts/book-metadata.yaml) | Title, language, page size, margins, link colour — so tuning typography is not a Python edit. |
| [`Makefile`](../Makefile) | `make pdf` / `md` / `html` / `open` / `check` / `clean`, and `make` alone lists them. |
| [`cards/building-the-book.md`](../cards/building-the-book.md) | What to install, what the build expects of authors, and the two severities. |

**Two things in it are useful to a writing task, not just to whoever renders the book:**

1. **`make check` tells you whether what you wrote is actually in the book.** It reports files that
   are not in the table of contents, rows marked ✅ whose file is missing, and `#` headings that
   disagree with their table-of-contents title. It is now the last line of the *Adding a file*
   checklist in `book/README.md`, and it exits non-zero only on real problems, never on the
   expected consequences of an unfinished book.
2. **Every run prints a word count per part with each part's share of the total.** The proportions
   in `cards/book-structure.md` — 15 / 60 / 15 / 10 — stop being an intention the moment there is a
   number next to them. The book currently stands at 7,886 words: Part I 4,150 across three
   chapters, Part II 3,736 across the Context suite's four files. Part II passes Part I on the next
   suite, which is the first moment the proportions can be read as anything but noise.

A follow-up (`878a5eb98f8b`) then fixed the one thing that build shipped broken: **the PDF had no
diagrams in it.** Rendering required a global `mermaid-cli` that nobody had installed, so both
mermaid blocks came out as source code — in a book whose own conventions mandate mermaid. The
build now finds `mmdc` if it is there and otherwise runs `npx --yes @mermaid-js/mermaid-cli`, so
a clean checkout with node on it produces diagrams with no setup step. Three things follow for
anyone touching this:

- **Diagrams now cost build time**, so renders are cached in `build/diagrams/` against their
  source and only changed diagrams re-render. A warm rebuild is back under a second.
- **`make check` no longer renders diagrams at all.** It writes nothing and stays instant. If you
  want a diagram checked, build the PDF — a syntax error mermaid rejects is reported as a problem
  against the chapter, so `--strict` catches it there.
- **Write mermaid freely in a play.** It works now, and a diagram wider than the page is clamped
  to the text width rather than overflowing it.

A reassessment pass (`aed2433867e0`) then re-read Part I and the Context suite against the three
constraint documents, and re-ran `make check` against the build milestone 18 had just landed. The
prose held up and the build reports no problems; the contracts did not hold up, because four
conventions the Context suite established were recorded only in the decision log below. **They are
now in `book/`, which means the five remaining suite authors get them by reading `STYLE.md`,
`TEMPLATE-play.md` and `README.md` — the files they were going to read anyway.** If you are writing
a suite, these four are the ones most likely to catch you:

1. **Your `index.md` has a contract**, in [`book/README.md`](../book/README.md#suite-openers): name
   the suite's single idea, then show each play as that idea at a different layer. A unifying
   principle goes in the opener, where it costs forty words, never in a fourth play.
2. **Every play states its exchange rate** — what the reader gives up. Part I promises the reader
   this in print, so a play listing only benefits contradicts the book two parts away. It is now a
   rule under *The play* in `TEMPLATE-play.md` and an item in `README.md`'s adding-a-file checklist.
3. **Pick one project for your suite and re-introduce it in a clause in every play.** Not another
   suite's project — Context has `atlas` — and never "`atlas` again", which is a back-reference to
   a play your reader has not read.
4. **Worked examples are past tense.** This is the book's one exception to the present tense, and
   it is now written down in both `STYLE.md` and `TEMPLATE-play.md`.

Board item `01dce54a3f88` then turned `make html` from a one-line pandoc call into the build's
cheapest and most sendable output. It collects exactly what `make pdf` collects — same table of
contents, same collected markdown, same checks — and renders **one self-contained HTML file** with
a contents sidebar, a reading column, dark mode, and print rules good enough that `Cmd+P` in a
browser is a reasonable substitute for a PDF engine.

| File | Owns |
|---|---|
| [`scripts/book.css`](../scripts/book.css) | Everything about how the HTML book looks: measure, sidebar, headings, code, tables, diagrams, dark mode, print. The HTML sibling of `book-metadata.yaml` — presentation as data, not as Python. |
| [`scripts/build_book.py`](../scripts/build_book.py) | `--format html` now inlines the stylesheet (`--embed-resources`), runs the contents three levels deep, and hands diagrams to the browser. |
| [`Makefile`](../Makefile) | `make open-html` alongside `make open`. |

**Three things are worth knowing before you reach for a format:**

1. **`make html` needs only pandoc.** No PDF engine, no TeX, no node. If you want to read the
   whole book end to end, or send a draft to somebody without the repo, it is the shortest path —
   and `--repo-url` is worth passing when you do, so the links out of the book still resolve.
2. **The HTML book draws its own diagrams.** ```mermaid``` blocks become `<pre class="mermaid">`
   and mermaid.js renders them in the browser, so node and mermaid-cli are PDF dependencies only.
   Offline they degrade to their own source, which is what the PDF does without a renderer.
   Authors change nothing: keep writing mermaid.
3. **The contents sidebar goes three levels deep, so the five play headings are navigable.** The
   PDF's contents page stops at two on purpose. This is the first thing in the build that treats
   the play template as a navigation structure rather than a writing one, and it is a small
   argument for keeping those five headings identical across eighteen plays.

## Decisions log (append-only)

- Ideation consolidated; `idea.md` / `plot-1.md` / `plot-2.md` moved to `notes/raw/` and replaced
  by `PLAN.md`.
- The original chapter outline was rejected as "a taxonomy rather than a playbook." Its three
  surviving ideas — the pre-Git/pre-Scrum analogy, the Four Areas, and the unsettled-
  engineering-layer thesis — were demoted from chapters to the short argument that justifies the
  plays.
- Four subjects absent from the original outline were added as play suites because the critique
  flagged them: context engineering, harnesses and tool-calling, verification, and cost.
- Agentic setup: repo conventions are recorded as **context cards** in `cards/` rather than as one
  growing `CLAUDE.md`, so parallel writing agents load only what their situation needs.
- The shared-plan pattern was applied to **this file** rather than a new `project-plan.md`. This
  file already held the locked decisions and running log; adding a third planning document would
  have split the source of truth three ways.
- Prose is hard-wrapped at 100 columns so that parallel authors produce line-scoped diffs.
- Book files are named for their content (`starve-the-context.md`), never numbered by position —
  renumbering a directory is a merge conflict waiting to happen.
- **Worked examples are illustrative-but-correct for the first draft** (user decision). Commands
  and file contents must be real and runnable; output is only presented as captured when it was
  actually captured, marked with a `> Captured <Month Year>, <tool> <version>.` line. Inventing a
  measurement is banned outright. Milestone 17 (`3b61a6a1a684`) runs the examples for real before
  publication. This resolves the "real or illustrative?" open question.
- **The five play headings are fixed strings**, not a suggested outline. Skimmability across
  eighteen plays and the `#failure-mode` anchor convention both depend on them being identical.
  Material that does not fit is two plays.
- **The table of contents in `book/README.md` is the only ordering mechanism.** Part directories
  are numbered because part order is locked; nothing inside them is.
- **Cross-references are relative file links with italicised titles.** Deep links are permitted
  only to the five template headings, never to an `###` an author can rename. References by
  position ("see chapter 4", "as we saw earlier") are banned — a reader who opened the book at one
  play has not seen anything earlier. Forward links to table-of-contents-listed files that do not
  exist yet are allowed, because nine writing tasks run in parallel.
- **Named failure modes are Title Case noun phrases naming a symptom, not a cause**, and are
  registered in the running log below so two suites do not coin two names for one thing.
- **British English, Oxford comma, sentence-case headings, no YAML frontmatter.**
- **A research pass covering several subjects produces several briefs plus a hub**, not one file.
  Milestone 4 was commissioned as a single `notes/research/tooling.md` and delivered six files:
  the commissioned path became the hub holding the cross-cutting analysis and the full source
  list, with one self-contained brief per subject beside it. This follows
  `cards/research-briefs.md` ("several small briefs beat one enormous one") without losing the
  entry point the task named. Later research passes should do the same.
- **Every research brief ends with a staleness assessment.** This subject dates in months, not
  years, and a writer picking up a brief six weeks later needs to know which findings to hedge
  before they know anything else. `notes/research/tooling.md` carries a ranked table with a
  suggested hedge per row.
- **A research brief states what a source could *not* establish, and names sources that must not be
  cited.** Milestone 5 found several confidently-circulating figures that did not survive checking —
  two low-code statistics attributed to Gartner and to vendor research, a scaffolding quote
  attributed to a named engineer with no traceable transcript, and a GitHub file that is a rewritten
  derivative of Anthropic's "Building effective agents" whose plausible figures are not Anthropic's.
  These are recorded in the briefs as **do not cite**, with the reason. A brief that only lists what
  is true leaves the next agent to rediscover the same traps, and the derivative-text case is the
  exact failure `cards/research-briefs.md` exists to prevent.
- **The book distinguishes evidence about *agents* from evidence about autocomplete, every time.**
  Milestone 6 found that every RCT in the field measures autocomplete, inline completion, or chat,
  and that the five most-quoted figures in the discourse are all being restated as agent results.
  `notes/research/productivity-evidence.md` carries a table mapping each finding to the sentence it
  gets turned into. Any causal claim about agents in this book is hedged, and the reason is stated
  once, plainly: the field's missing RCT was attempted and abandoned because developers would no
  longer agree to work without AI.
- **Legal and regulatory material is presented as "here is what the document says", quoted and
  dated — never as guidance.** `notes/research/accountability.md` contains copyright, liability and
  sectoral-regulation material, none of which is legal advice. This is a standing instruction for
  *Decide who signs off*, and it is the reason that brief quotes policy text verbatim rather than
  summarising it into something stronger.
- **Prices are printed as ratios, never as absolutes.** Milestone 6 flagged `token-economics.md` as
  the fastest-rotting material in the book — not "will need updating" but rotting, with two of the
  three subscription billing schemes it describes introduced in the six months before it was
  written. The durable findings are the tier ladder, the 4–8× output:input multiple, and the 0.1×
  cache-read multiplier. Absolute dollar figures appear only as a dated snapshot, labelled as one. A
  related trap: models of different generations tokenise differently, so per-token prices must never
  be compared across generations.
- **Where a source cuts both ways, the brief carries both halves.** The one study measuring
  orchestration latency separately found multi-agent slower in wall clock *and* cheaper in tokens.
  Quoting the convenient half would forfeit the credibility the Orchestration suite's sceptical
  framing depends on. The rule generalises: this book's argument is strongest when its own evidence
  is reported against interest.
- How much the book dates itself is answered provisionally in `book/STYLE.md` (use a figure only
  when the point collapses without it; date it in the sentence; prefer shape to figure). The
  editorial pass owns the final call.
- **The `notes/raw/` freeze bans editing existing records, not filing new ones.** Late ideation
  from the author is archived there as a new file rather than folded into `PLAN.md`, so the
  provenance record stays a record and the plan stays consolidated. The first instance is
  [`notes/raw/team-adoption-fragment.md`](../notes/raw/team-adoption-fragment.md). What such a
  fragment *contributes* goes in the running log below; the fragment itself is never a spec.
- **A writing task that has to do its own research files a brief like a research task would.**
  Milestone 7 needed sourced history for the pre-Git/pre-Scrum analogy, which no research pass
  covered. Rather than carrying twenty inline URLs in one chapter, it produced
  [`notes/research/convergence-history.md`](../notes/research/convergence-history.md) to the format
  in [`cards/research-briefs.md`](../cards/research-briefs.md) — findings, gaps, do-not-cite,
  numbered sources, staleness — and the chapter cites the brief plus a handful of primary quotes.
  This keeps the verification pass (`3b61a6a1a684`) able to check Part I the same way it checks a
  play, and means the next author reaching for the same analogy does not re-run the searches.
- **The Standish CHAOS figures go on the book's do-not-cite list.** The 1994 16%/53%/31% success
  split and the 189% average cost overrun are the most-quoted numbers in the history of software
  process and do not survive checking; two peer-reviewed demolitions are cited in
  `convergence-history.md`. If the book touches them at all, it is as an example of a number the
  industry repeated for twenty years without opening the source — which is on-theme rather than a
  digression.
- **Part I cites primary documents inline and the brief for the survey figures.** Quotations that
  carry the prose (Tichy on locking, Microsoft's own SourceSafe glossary, GitHub's two pull-request
  posts, Cockburn on "lightweight") are quoted in the chapter; every percentage traces to the brief.
  The rule generalises for non-play chapters: quote the primary source where the sentence depends on
  its exact words, cite the brief for everything numeric.
- **A suite opener names the suite's one idea and shows its plays as applications of it.** Review
  feedback on milestone 8 asked whether "signal over noise" deserved a place of its own. It did,
  but not as a fourth play: as a noun phrase it fails the imperative-title rule in
  `book/TEMPLATE-play.md`, and rewritten as an imperative it collapses into *Starve the context*.
  The resolution was to state it as the Context suite's thesis in `context/index.md` and present
  the three plays as the same move at three layers — the always-loaded layer, the single run, and
  the task itself — with one sentence in each play's transferable paragraph tying back to it. The
  pattern generalises and the other five suite openers should follow it: a principle that unifies
  a suite belongs in the opener, where it costs 40 words, rather than in a play, where it costs a
  slot and overlaps the play next to it.
- **A suite may carry one project name across all of its plays.** The Context suite uses `atlas`, a
  Python billing service, in all three worked examples. Each play re-introduces it in a clause, so
  the plays stay self-contained for a reader who opens the book at one of them, and a reader going
  through the suite gets continuity for free. Other suites should pick their own project rather
  than extending `atlas`, or the book acquires one imaginary company with six unrelated problems.
- **A convention that constrains future authors lives in `book/`, not only in this log.** A
  reassessment pass after milestone 8 found four conventions established by the Context suite that
  existed only as entries in this decision log — which is now sixty entries long and is not what an
  author reads before their first sentence. The three constraint documents in `book/` are. Anything
  a later author must follow is written there and *summarised* here; this log records why the
  decision was taken, not the decision itself. The four promoted are the next four entries.
- **A suite opener has a contract, not just a word budget**, now in
  [`book/README.md`](../book/README.md#suite-openers): name the suite's single idea, then show each
  play as that idea at a different layer, in a framing paragraph, an idea sentence, and one
  paragraph per play. This makes the milestone-8 "suite opener names the suite's one idea" decision
  actionable for the five suites that have not been written.
- **Every play states its exchange rate**, now a rule under *The play* in
  [`book/TEMPLATE-play.md`](../book/TEMPLATE-play.md) and an item in `book/README.md`'s
  adding-a-file checklist. *What this book assumes about you* promises this to the reader in print,
  so a play that lists only benefits contradicts Part I. All three Context plays state one; the
  promise had been recorded nowhere an author would see it.
- **One project per suite, re-introduced in a clause in every play**, now in `TEMPLATE-play.md`
  under *Worked example*. The clause matters as much as the project: "`atlas` again" is a
  back-reference, and a reader who opened the book at this play has not read the one next door.
- **A play's *Worked example* is narrated in the past tense.** This is the book's one exception to
  the present tense and is now stated in both `book/STYLE.md` and `book/TEMPLATE-play.md`. All
  three Context plays did this, consistently and against the written rule; it is the right call —
  an example reports what happened, the rest of the book describes how things behave — so the rule
  was corrected rather than the plays. Without this, five parallel suites would have split on tense.
- **The PDF is derived, never authored.** Milestone 18 built it as a one-way transformation:
  `book/` is read, `build/` is written, and no site- or print-specific syntax enters the source.
  Heading levels, anchors, page breaks and link rewriting all happen at build time. This does not
  reopen the *Rendering* open question — the answer it commits to is narrower and, on the evidence
  of this build, sufficient: **a renderer adapts to the book, not the book to the renderer.** If a
  static site is ever wanted, it should be built the same way, and the non-goal ("not a rendered
  site, for now") stands.
- **A forward reference whose target does not exist yet is unlinked at build time, not fixed.**
  `book/README.md` allows links to table-of-contents-listed files that nobody has written, because
  nine writing tasks run in parallel. Left in the PDF such a link is a hard error in typst and a
  silently broken link elsewhere, so the build turns it back into plain text and reports it as a
  note. The consequence for authors is that the convention stays as written: keep making forward
  references.
- **The build has two severities and only one of them fails.** A *problem* is for a person to fix
  (an orphan file, a chapter marked done that is missing, a heading that disagrees with the table
  of contents); a *note* is the expected consequence of building a half-written book. `--strict`
  fails on problems alone. A check that goes red for months teaches everyone to ignore it, which
  costs more than it saves.
- **"Humble and transparent" is subject matter, not a tone instruction.** The author's note that
  this "has to be presented in a way not to scare but rather build trust" describes how a *team
  lead* introduces a working agreement to colleagues. It does not soften the book's own register,
  which stays dry and wry per the locked decision. A Team-suite author writing trust-building
  prose is writing about the team lead's problem, not adopting the team lead's voice.
- **Opening the PDF is a make target, not a habit everyone retypes.** `make open` depends on `pdf`,
  so it always rebuilds before it shows you anything, then hands the file to `open` or `xdg-open`.
  The board shortcut *Build & open book* runs exactly that, so the one-click path and the
  command-line path cannot drift apart. `BUILD` and `NAME` are now passed through to the build
  script (`--out-dir` / `--name`) so the path `make open` opens is the path `make pdf` wrote.
- **Diagrams render without anyone installing anything.** The build used to require a global
  `npm install -g @mermaid-js/mermaid-cli`, which nobody had done, so every PDF built so far had
  its diagrams printed as source — a book that mandates mermaid was shipping none of it. The
  build now falls back to `npx --yes @mermaid-js/mermaid-cli` when `mmdc` is absent. This does
  not reopen the Python-tooling default: mermaid-cli is an external renderer shelled out to by a
  Python script, exactly as before, and the only change is how it is located. The rule behind it
  is that **a convention the book mandates must work on a clean checkout**, or it is not a
  convention, it is a hope.
- **A missing renderer and a broken diagram are different severities.** A renderer that cannot
  run (no node, no network, no browser) is a *note* and `--strict` still passes — that is a fact
  about the machine. A diagram mermaid rejects is a *problem* naming the chapter and quoting the
  error, because that is a fact about the book, and the other diagrams still render. The same
  split the build already used for missing chapters, applied one level down.
- **Rendered diagrams are given an explicit width, because pandoc's default is wrong.** Diagrams
  are rendered at 3× for print, and pandoc reads the PNG's pixel width and assumes 96 dpi — so an
  unsized diagram lays out three times too wide and runs off the page. The build divides the
  scale back out and caps the result at the text width. Anything that changes the render scale
  has to keep that division, or the diagrams silently overflow again.
- **The HTML book is one self-contained file, not a site, and this does not reopen the *Rendering*
  open question.** `make html` existed from milestone 18 as a bare pandoc call and produced a
  default-stylesheet dump; `01dce54a3f88` made it a real output. The shape was the decision worth
  making, and the non-goal ("not a rendered site, for now") decided it: a directory of linked pages
  is a site, needs hosting, and would tempt authors into site-specific link syntax. One file with
  `--embed-resources` is none of those things, is generated by the same one-way transformation as
  the PDF, and can be emailed. If a site is ever wanted it should be built the same way, from the
  same table of contents, and this build does not prejudge it.
- **Presentation is data, in both directions.** `scripts/book.css` is to the HTML book what
  `scripts/book-metadata.yaml` is to the PDF: the whole of how it looks, outside the Python. The
  rule milestone 18 set — tuning typography is not a code edit — is now symmetrical, and a
  future renderer should add a data file rather than a branch in `build_book.py`.
- **The HTML book renders mermaid in the browser, so mermaid-cli is a PDF-only dependency.** A
  browser can draw mermaid; asking a reader to install a Node package so that a *web page* can show
  a diagram is the wrong trade. Blocks become `<pre class="mermaid">` and mermaid.js draws them as
  SVG at the reader's width and colour scheme — better output than the PNGs the PDF gets, for less
  setup. The cost is a CDN request on first open, which is why the fallback is the block's own
  source rather than a hidden element: an offline reader sees exactly what the PDF shows without
  mermaid-cli, and the build reports it as a note either way. Nothing changes for authors, and the
  npx fallback above stays exactly as it is for the PDF.
- **The contents depth differs by format, because a sidebar and a printed page are not the same
  object.** HTML runs three levels deep, so a reader can jump to any of the five play headings; the
  PDF stops at two, because eighteen plays times five headings is a contents section longer than a
  chapter. Same book, same table of contents in `book/README.md`, different affordance.
- **The author's own published material is book content, not a cited source** (user decision,
  milestone 19). Milestone 19 audited the two posts the author supplied and found them almost
  entirely unspent: *Cards* had reached the book not at all, and *The unit of work* had reached it
  as a single in-line citation for a phrase. The cause was traceable — the Context-suite guidance
  "cite vendor documentation, not blog posts" was written to kill stale third-party claims about
  `AGENTS.md` and, read literally by every writer after it, caught the author's own posts too.
  That guidance now carries an explicit carve-out, and the handoff note has an *The author's own
  material* section stating what each post argues and which chapter owns it. The attribution
  convention is **absorb, do not cite**: the material goes into the book's voice, the URLs go into
  the appendix's further reading. A book that footnotes its own author reads as though it is
  quoting someone else.
- **A mechanic that only one vendor implements is named and version-stamped in the sentence that
  uses it; the shape it is an instance of is stated generally.** `permissions-and-sandboxing.md`
  warns that only one harness was examined, and *Choose your harness* would have been dishonest
  written either way round — as a tour of one product's settings, or as a claim about harnesses in
  general built entirely on one product's documentation. The split it uses instead is the durable
  one: the three enforcement layers (nothing / the client / the kernel) are general and are written
  as such, while `Bash(devbox run *)`, `failIfUnavailable`, and the wrapper-stripping list are
  attributed and dated. This also keeps the play useful to a reader on a different harness, who
  needs to know what to go and look for rather than which JSON key to copy.
- **A suite may leave a research pass's evidence unspent when the argument does not need it.** The
  Harness suite cites no adoption figures — not the ~45 skill clients, not the server counts that
  disagree by a factor of five, not the 60k repositories. Each was available and each would have
  added a date stamp to a paragraph whose argument is structural. The rule generalises past the
  staleness table in `tooling.md`: a figure that does not change what the reader does is a liability
  with no upside, and the test is whether removing it weakens the sentence.
- **A worked example's programming language is a content decision, not decoration.** The
  Orchestration suite's sharpest artefact is a rename that both branches test green and that fails
  only in the merged tree. Written in a typed language that example is wrong — `tsc` catches it
  before anyone merges — so `meridian` is Ruby, and the failure is a runtime `NoMethodError`. The
  rule generalises: if the point of an example is a class of defect, check that the example's stack
  can actually exhibit it. The narrower version of the same problem is worth stating too, because
  it is the honest one — in a typed codebase that collision reappears through stringly-typed names
  (queue names, route paths, feature-flag keys), and a play that implies types abolish it would be
  overselling.
- **A research pass's strongest scenario may be declined on reader fit.** `langchain-langgraph.md`
  offers a refund agent with a $500 approval threshold, written twice, and it is the best
  build-versus-adopt comparison in the pass. The Orchestration suite did not use it: this book's
  reader builds software with agents rather than building agent products, and a customer-support
  refund flow puts them in somebody else's problem for four hundred words. The material survives —
  the resumability argument, the `interrupt()`-inside-a-tool mechanic, and the beat that neither
  version detects the crash are all in the play — re-hosted on the suite's own project. A brief
  supplies evidence and an illustration; the illustration is the part a writer may replace.
- **Three plays per suite is a floor, not a ceiling** — settled for the Context suite at least
  (user decision, milestone 19), which takes a fourth play on the cards pattern. This does not
  license adding plays quietly: `book/README.md` still asks suite authors to raise a fourth rather
  than insert one, and the raise here was made and answered. It does mean a suite author with a
  genuinely fourth-layer idea has a precedent to point at.

## Open questions

Raise these rather than guessing. An agent that silently picks one answer commits the whole book
to it.

- **Play count per suite.** `PLAN.md` gives three working titles per suite. Is three a target or
  a floor? **Half-resolved** (milestone 19): three is a *floor*, and the Context suite takes a
  fourth play on the cards pattern. What remains open is the balance question — a suite with six
  plays next to one with two still unbalances Part II, and nothing yet caps the spread.
  `book/README.md` continues to ask suite authors to raise a fourth rather than add it quietly;
  that procedure worked here and should be used again rather than treated as satisfied.
- ~~**Worked examples — real or illustrative?**~~ **Resolved** (milestone 3): illustrative-but-
  correct for the first draft, with a verification pass (`3b61a6a1a684`) before publication. The
  rules are in [`book/TEMPLATE-play.md`](../book/TEMPLATE-play.md#worked-examples-what-real-means).
- **How much does the book date itself?** Model names, prices, and context limits make examples
  concrete but guarantee an expiry date. Where is the line? A provisional answer is in
  [`book/STYLE.md`](../book/STYLE.md#volatile-facts) so no author is blocked on it; the editorial
  pass owns the final call.
- ~~**Appendix templates.**~~ **Resolved** (milestone 19) for the `CLAUDE.md` starter: this
  repo's own setup is the worked example. The root `CLAUDE.md` is a real two-tier index and
  `cards/` holds five real self-contained cards, so the template is checked in, exercised daily by
  every agent on this board, and satisfies illustrative-but-correct without anything being
  invented. The new Context play (`703e507c86aa`) writes the pattern up; the appendix should
  extract the skeleton from it rather than invent a second one. The **working-agreement
  skeleton** is still open — the Team suite has no equivalent artefact in this repo to point at.
- **Rendering.** Markdown-on-GitHub is the committed deliverable. If a static site is ever wanted,
  that decision needs making before the prose accumulates site-specific link syntax.

## Running log

Append discovered constraints and cross-task notes here as work proceeds.

- Agentic setup applied (milestone 2): root `CLAUDE.md`, `cards/` with four cards, this plan
  completed to the shared-plan shape, `backward-planning` and `review-agentic-setup` skills
  linked into `.claude/skills/`.
- Milestone 3 created `book/` with `STYLE.md`, `TEMPLATE-play.md`, and `README.md`, and updated
  `cards/book-structure.md` to point at them. No part directories were created — the first task
  that needs one makes it.
- `book/TEMPLATE-play.md` ends with a **specimen play**, *Commit before you let it run*. It is
  deliberately not in the table of contents and not in any suite. If a suite wants that material,
  write it fresh in the suite; do not move the file, or the template loses its example.
- Milestone 4 turned up **three cross-cutting phenomena that want names**, under *Cross-cutting
  gotchas* in `notes/research/tooling.md`. They are deliberately *not* registered below, because a
  research brief should not squat names the suite authors have to live with. Whichever suite writes
  one first names it and registers it here. They are: (a) instructions mistaken for enforcement —
  a `deny` rule, a line in `CLAUDE.md`, or a skill description read as a hard boundary when none of
  them is one; (b) a tool's self-reported savings diverging from the measured bill; (c) a silent
  precedence rule cutting off instructions with no error — adding a `CLAUDE.local.md` stops
  `AGENTS.md` loading, and `/context` reports the same empty list either way.
- **Two candidate worked examples from milestone 4 are unusually strong and should not both be
  spent in one suite.** The permission-matching table (a `deny` rule on `Bash(git push *)` does not
  stop `git 'push' origin main`) belongs to Harness; the `rtk` benchmark (the dashboard reported
  96.2M tokens saved over the same trials in which the bill rose 7.6%) belongs to Context or
  Economics. The Economics suite should read `notes/research/token-filtering.md` even though it is
  filed under the Context pass.
- **An archive pass on a late author fragment (`notes/raw/team-adoption-fragment.md`) found three
  things the rest of `notes/raw/` does not say. All three are Team suite material
  (`cdd27e440781`), and none of them changes a locked decision:**
  1. **Mandate without method.** Managers are asking developers to use these tools while offering
     no direction on how. `idea.md` frames the gap structurally ("no declared way of working as a
     team"); this names the *pressure* the reader is actually under — told to adopt, not told how,
     and judged on the result anyway. It belongs in the Team suite's *Problem* headings and is a
     candidate for *What This Book Assumes About You* (`e93293bfd014`). Note the non-goal: this is
     the reader's situation, not an invitation to address the manager.
  2. **A working agreement has an expiry date.** The fragment asks for the adoption discussion to
     be *re-run on a cadence*, with room explicitly reserved for trying new tools. `idea.md` has
     "be prepared to change" and "experiment" as dispositions; a review cadence and a standing
     experiment budget are mechanisms, which is what a play can actually contain. *Build the
     working agreement* should ship with a review trigger, and the failure mode is nearby: an
     agreement written once, obeyed for two model releases, and quietly ignored thereafter.
  3. **Adoption by decree reads as surveillance.** "Not to scare but rather build trust" identifies
     a distinct risk — the team hears a new working agreement as measurement of them, not of the
     tools. Worth a named failure mode if a Team-suite author wants one; see the decision above for
     why this does not license a change of register.
  The fragment's four-step sequence — collect what the team already does, discuss openly why some
  things work better than others, define the way of working, then converge everyone on it — is
  mostly already in `idea.md`, but step two (an honest comparison of what worked and what did not)
  is sharper than "collect and refine" and is the natural spine of
  *`team/collect-and-refine-as-a-team.md`*.
- **Milestone 5 surfaced four more cross-cutting phenomena that want names**, under *Cross-cutting
  gotchas* in `notes/research/orchestration.md`. As with milestone 4 they are deliberately **not**
  registered below — whichever suite writes one first names it and registers it. They are: (a) the
  parent sees only a subagent's summary and never checks the transcript, which exists on disk; (b) a
  subagent inherits the written brief but none of the conversation, so a convention established in
  chat is silently absent while one written in `CLAUDE.md` is enforced; (c) a merge that git reports
  as clean and that breaks the build, which is the collision class that matters; (d) a fan-out that
  was really just a larger compute budget. Note that (b) is the orchestration-layer sibling of
  milestone 4's silent-precedence gotcha — if the Context suite names that one, the same name may
  stretch to cover both.
- **The Orchestration suite has more strong worked examples than it has plays.** Five non-colliding
  scenarios are mapped at the end of `notes/research/orchestration.md`. Two of the sharpest — the
  migration-ordering collision and the rename/add-call-site collision — currently sit inside the
  *same* worked example because they co-occur in real life. If *Work in parallel without collisions*
  runs long, the rename case stands alone and the migration case is a natural second play or a
  Part III failure mode. Worth raising against the open play-count question rather than deciding
  quietly.
- **The Economics suite should read `notes/research/single-agent-wins.md`** even though it is filed
  under the orchestration pass. It is the evidence base for *Know when not to use an agent*, and it
  carries the token-and-latency comparisons that the Economics suite would otherwise have to
  re-derive.
- **`notes/research/` contains two deliberate leads that were not closed, both needing a human with
  a browser:**
  1. NSA/CISA MCP security guidance dated June 2026, which returned HTTP 403 to automated fetch. If
     the Harness suite wants a government-grade citation for the security material, that PDF needs
     downloading by hand first. Flagged in both `tooling.md` and `mcp.md` as unverified.
  2. Octomind's "Why we no longer use LangChain" (June 2024) — the canonical framework-removal
     critique, quoted in `langchain-langgraph.md` from search summaries and a secondary aggregator
     because octomind.dev refused connections on every attempt and archive.org was unavailable.
     **The quotations must be verified against the primary page before publication.** Note also that
     the post is now over two years old and its subject has had a major release since; milestone 5
     found no credible successor to it, so the book should not imply that framework removal is a
     documented trend.
- **Milestone 6 surfaced four more cross-cutting phenomena that want names**, under *Cross-cutting
  phenomena that want a name* in `notes/research/evidence.md`, with three more in
  `notes/research/failure-modes.md`. As with milestones 4 and 5 they are deliberately **not**
  registered below. They are: (a) a correct solution reached mid-run and then overwritten, measured
  rising from 21.7% of the shortest trajectory quartile to 63.7% of the longest; (b) requirements
  still present in context and no longer being met — coverage retention held at 0.93–0.95 while
  strict success retention fell to 0.375, so this is *not* a context-window problem and must not be
  written as one; (c) a green suite that is evidence about the suite, via a `sys.exit(0)` harness
  escape, a special-cased test input, or a deleted test; (d) the error classes that got cheap to
  catch falling while the ones that were always expensive rose. Note that (c) is the
  verification-layer sibling of milestone 4's instructions-mistaken-for-enforcement gotcha.
- **Milestone 6's do-not-cite list is the largest in the project and is consolidated in the hub.**
  Roughly forty figures across six subjects did not survive checking. The three most likely to catch
  a writer: **every** published SWE-bench per-instance dollar figure (Epoch AI's page carries no
  cost column at all, and the circulating numbers exist only in a search engine's synthesis of
  secondary blogs); the "200–400 lines in under 60 minutes yields 70–90% defect discovery" review
  rule, which appears nowhere in the 2006 study it is attributed to and whose design could not have
  measured it; and any "Stack Overflow Developer Survey 2026" figure, since that survey had not
  reported as of 19 September 2026 and the circulating numbers are 2025 data under a 2026 headline.
- **METR's 19% slowdown must never appear without its qualifier.** METR redesigned the experiment
  and reported in February 2026: −18% (CI −38% to +9%) for the original cohort and −4% (CI −15% to
  +9%) for newly recruited developers, both straddling zero. METR's own verdict is that the data is
  "only very weak evidence" and "an unreliable signal". The hub pairs it with the Google enterprise
  RCT and the Copilot study so a chapter can carry the honest version.
- **Milestone 6 left five primary documents that need a human with a browser**, joining the two from
  milestone 5: the DORA 2025 PDF (exceeds the fetch size limit, and the 2025 effect-size
  coefficients are on no other reachable page), the US Copyright Office Part 2 report PDF,
  Anthropic's system-card PDFs, Fedora's canonical AI-policy page (behind an Anubis challenge), and
  OpenAI's Codex rate-card article (HTTP 403). Nothing should be quoted verbatim from any of them
  until then.
- **Four of the strongest 2026 review findings share one corpus.** The AIDev/CodAGE dataset
  underlies several separately-published papers, so they are not four independent confirmations.
  Write "in the largest available corpus of agent pull requests", never "several studies find".
- **The Verification & Trust suite has a stronger worked example than it has plays for.** The
  fakeability ranking in `verification.md` and the `sys.exit(0)` escape both serve *Make the agent
  prove it*, and the mandate-study displacement example serves both Part III and Economics. The
  hub's worked-example map shows the six do not collide, but two of them make different arguments
  about the same green test suite — worth raising against the open play-count question rather than
  deciding quietly.

- **Milestone 7's historical research turned up three traps that are one search away from any
  author writing about this era.** They are itemised with sources in
  `notes/research/convergence-history.md`; the short version is (a) the Standish CHAOS figures, now
  a locked do-not-cite above; (b) "the Agile Manifesto brought together seventeen different
  methods" — seventeen is the number of *people*, and the manifesto history names eight approaches;
  (c) "GitHub launched 10 April 2008" — GitHub's own blog confirms the month, and the specific day
  traces only to Wikipedia. Two further figures that get quoted confidently and do not exist: an
  "87% of teams use Scrum" number attributed to the 2023 State of Agile, which does not appear in
  that report, and any Stack Overflow 2015 "I don't use source control" percentage, since the 2015
  survey had no such option.
- **The two version-control survey series are not a time series and must never be printed as one.**
  Eclipse asks for a single *primary* SCM among an Eclipse- and Java-leaning population; Stack
  Overflow is multi-select across a far larger and different one. Eclipse 2011 puts Git at 12.8% and
  Stack Overflow 2015 puts it at 69.3%; both are correct for their question. Part I names the survey
  and the year in every sentence carrying a figure, and Part IV or the editorial pass should keep
  doing that.
- **Every file written for Part I overshot 100 columns on first draft, by one to four characters
  each, in three separate files.** The rule is easy to hold approximately and hard to hold exactly
  by eye. Milestone 7 fixed it with a throwaway Python rewrapper run from `/tmp` rather than adding
  a script to the repo, because `cards/standing-defaults.md` says to add tooling only when a real
  repeated need appears. Nine parallel authors hitting the same problem is arguably that need: the
  editorial pass (`934259dc8038`) should either rewrap everything once at the end or adopt a small
  Python checker, and this note exists so that decision is made deliberately rather than discovered.
- **Part I closes on the book's own framing, and later parts should not re-argue it.** *Before Git,
  before Scrum, before this* ends on "this book is not the consensus… written in enough detail to
  be disagreed with precisely", and *What this book assumes about you* ends on "start wherever your
  week hurts". Suite openers do not need to re-establish why any of this matters; Part I did that,
  and repeating it is the fastest way for Part II to lose the space the plays were given.

- **Milestone 8 spent the `rtk` benchmark on the Context suite.** It is the Worked example of
  *Starve the context*, framed as a method lesson ("measure the bill, not the dashboard") with the
  JetBrains and Quesma figures dated and versioned per the staleness table in
  `notes/research/tooling.md`. The earlier note that this example belongs to "Context or Economics"
  is now resolved in Context's favour. **Economics should still read
  [`notes/research/token-filtering.md`](../notes/research/token-filtering.md)** — the cache-read
  pricing mechanism and the tokens × turns framing are load-bearing for *Understand what you are
  paying for* — but should build its worked example on something else. The strongest unspent
  candidates are in `notes/research/token-economics.md`.
- **Two cross-cutting gotchas were used but deliberately not named by the Context suite.**
  *Write the brief the agent actually reads* states the instructions-are-not-enforcement
  distinction in its closing paragraph (a brief "does not constrain the agent, it competes for its
  attention"; blocking an action needs a hook) but leaves milestone 4's gotcha (a) **unnamed**,
  because the Harness suite owns permissions, hooks, and the `deny`-rule example and should name it
  where the reader can act on it. Similarly, *Scope a task to fit the window* uses milestone 6's
  phenomenon (b) — coverage retention 0.93–0.95 against strict success retention 0.375 — as the
  play's transferable idea, and leaves it unnamed for Part III. Note the brief's own warning, which
  the play honours: this is **not** a context-window problem and must not be written as one.
- **Part I's "there is no name for it" sentence survived milestone 8.** *Scope a task to fit the
  window* opens on the mid-run-overwrite phenomenon (the agent re-implementing a helper it wrote
  forty minutes earlier) and describes it without naming it. Part III still owns that name, and the
  rewrite of Part I's sentence is still outstanding when it lands.
- **Milestone 8 hit no 100-column overshoots**, having run a throwaway Python width checker from
  `/tmp` before finishing, as milestone 7 did. Two of nine writing tasks have now independently
  written the same script. That is the repeated need `cards/standing-defaults.md` asks for, and the
  editorial pass (`934259dc8038`) should decide between adopting a checker and rewrapping once.
- **Mermaid blocks legitimately exceed 100 columns** and any checker must skip fenced blocks.
  *Scope a task to fit the window* has a 120-character node line; `book/STYLE.md` already exempts
  fenced blocks, and this note exists so nobody "fixes" it.
- **Milestone 18's build has a natural slot for the 100-column checker, and deliberately does not
  fill it.** Two writing tasks have now written the same throwaway width checker, and
  `scripts/build_book.py` is the obvious place to put a permanent one — it already walks every
  chapter and already skips fenced blocks, which is the hard half. But adopt-a-checker versus
  rewrap-once is the editorial pass's call (`934259dc8038`), and adding it now would make that
  decision by accident. The severity split is there to hang it on the day the call is made: a long
  line is a *problem*, not a note.
- **The build was run against everything written so far and found nothing wrong with it.** Seven
  chapters, 7,886 words, two mermaid diagrams, and four forward links into suites nobody has
  written. The only build-visible defect class it can catch that has not yet occurred is a title
  heading disagreeing with the table of contents, which is worth knowing when judging whether
  `make check` is pulling its weight.
- **The PDF renders through pandoc plus typst, and both are optional.** typst is the default engine
  because it is one 45 MB binary against several gigabytes of TeX; any of eight other engines is
  used if found first, and with none installed the build still writes the collected markdown and
  says what to install. Diagrams need `mermaid-cli`, which is Node — the exception is deliberate
  and narrow: it is an external renderer invoked by a Python script, not a Node build step, and
  without it the diagrams print as source and the build reports a note. *(Superseded in part: the
  build no longer needs mermaid-cli installed, see the mermaid entry below.)*
- **Two pandoc-and-typst traps are recorded here so nobody rediscovers them.** typst's template
  feeds `linkcolor` straight to `rgb()`, so a named colour like `RoyalBlue` is a build failure and
  the metadata file carries hex; LaTeX wants the name instead, which the script passes on the
  command line. And typst's `margin` is a map, which `-V` cannot express — it has to come from the
  metadata file.
- **A reassessment pass audited Part I and the Context suite against the three constraint documents
  and found the contracts, not the prose, to be where the damage was.** Headings, links, the
  failure-mode registry, banned vocabulary, British English, agent terminology, 100-column
  compliance and the exchange-rate promise all held, and `make check` reported no problems. What did
  not hold was that four working conventions lived only in the decision log. Those are promoted into
  `book/` — see the four decisions above — and **a suite author who reads `STYLE.md`,
  `TEMPLATE-play.md` and `README.md` now gets all of them without reading this file.** Five small
  prose defects were fixed in the same pass: "`atlas` again" (a banned back-reference), bold used
  for general emphasis, a sentence claiming a deliberately-empty table had been filled in, a
  near-verbatim restatement of a Part I sentence in `context/index.md`, and the citation error
  below.
- **A cited retention ratio had been printed as an absolute rate.** *Scope a task to fit the
  window* gave requirement coverage as "roughly 0.93–0.95" and strict success as "about 0.375".
  Both figures in `notes/research/failure-modes.md` are *retention ratios against that study's own
  small-context baseline*, not absolute rates; the absolute success figures are 3/10 against a
  baseline of 8/10. The play now says "of baseline" and gives the raw counts. Any suite quoting
  arXiv 2607.17937 should carry the word *retention* — the figures are meaningless without it.
- **The judgement calls were deferred rather than fixed**, on two board items. `fce3cee8fa34` holds
  three marginal budget overruns — *Before Git, before Scrum, before this* at ~1,548 words against
  1,500, *Scope a task to fit the window*'s *The play* at ~559 against 500, and *Write the brief
  the agent actually reads*'s *Failure mode* at ~219 against 200 — plus the verbatim clause shared
  by `context/index.md` and *Starve the context*, which is the tie-back-to-the-opener pattern
  working slightly too literally. `9dd4d6b84b80` holds the terminology promise: *skill*, *card* and
  *harness* are used before being defined, against Part I's stated contract with the reader, and
  the suites that own those terms do not exist yet to fix it.
- **A third writing task has now independently written the same 100-column checker in `/tmp`**, and
  that settles the question the entry above left to the editorial pass. Milestones 7 and 8 each
  wrote one; the reassessment pass wrote a third, which also had to learn that `len()` on a Python
  `str` and `length()` in a byte-oriented `awk` disagree about em-dashes by two columns per dash.
  Three for three is well past `cards/standing-defaults.md`'s bar for adding tooling, and
  `scripts/build_book.py --check` is the home milestone 18 built for it: it already walks every
  chapter and already skips fenced blocks. Board item `6b0110f76388` carries it, is blocked on
  nothing, and is worth more before the remaining five suites than after them.

- **A guardrail written against stale blog posts silently filtered out the author's own.** The
  commissioner asked why none of his published thinking had reached the book. It nearly hadn't:
  of two posts he supplied, *Cards* appeared in the book zero times and *The unit of work* once,
  as a parenthetical citation for a phrase. Both had been read — milestone 4 filed them properly
  in `notes/research/tooling.md` [20][21] and wrote a section on the cards pattern into
  `agent-context-files.md`. The research was fine. The spending was not, and the reason was a
  single line of writing guidance: *"cite vendor documentation, not blog posts, on context
  files."* It was aimed at a wall of mid-2026 posts wrongly claiming Claude Code cannot read
  `AGENTS.md`. The hub brief did carve out an exception, in prose, four hundred lines further
  down; the headline instruction in the handoff won, as headline instructions do. The lesson
  generalises past this incident: **a rule stated as a category ("blog posts") will be applied to
  the category, not to the problem the rule was written for.** If a guardrail names a genre rather
  than a defect, it will over-fire, and the over-firing is invisible because nobody writes down
  what they declined to cite. The fix was to name the defect (third-party claims of fact) and to
  state the exception where the rule is read rather than where it was derived.
- **The book practised a pattern for six milestones without teaching it.** This repo runs on the
  cards pattern from the author's own post — a slim root `CLAUDE.md` index plus five
  self-contained `cards/`, and the Context suite never mentions it. The word "card" appears in
  *Write the brief the agent actually reads* exactly once, undefined, which is how board item
  `9dd4d6b84b80` came to exist. Worth noticing as a class of gap: conventions adopted in the
  *repo* during setup do not automatically become content in the *book*, and the setup milestone
  is the most likely place for good material to be silently spent on infrastructure instead. It
  also means the book's best worked examples may already be checked in — the resolved appendix
  question above turns on exactly that.

- **Milestone 9 named milestone 4's gotcha (a) as the Paper Fence**, which closes the note above
  about the Context suite leaving it unnamed. It covers both halves deliberately: the permission
  rule that matches a spelling rather than a capability, and the line of prose in a brief that reads
  as a refusal and is a sentence competing for attention. Gotchas (b) and (c) from that pass remain
  spent-and-unnamed and unnamed-entirely respectively — (b) is the Flattering Dashboard, (c) is
  still free.
- **The Harness suite uses `kestrel`, a Go search-indexing service**, across all three worked
  examples, per the one-project-per-suite rule. It is deliberately not `atlas`. Four suites still
  need their own.
- **Three dated claims in *Wire in the outside world* rest on secondary aggregation and need primary
  citations before publication.** The `postmark-mcp` backdoor (September 2025), the Invariant Labs
  tool-poisoning demonstration including the cross-server case (April 2025), and the existence of
  write-capable tools alongside read ones on a typical observability server. `notes/research/mcp.md`
  flags the first two as needing a primary check, and the play carries them at the level of shape —
  named package, named month, no figures — precisely so the check is an edit rather than a rewrite.
  Board item `f986730f7a1f` tracks it. The NSA/CISA MCP guidance is still unfetched and is cited
  nowhere in the book; the suite leans on the MCP specification's own Security Best Practices
  document instead, which is primary and normative and needed no manual download.
- **The Harness suite cites no adoption counts at all.** `tooling.md` and `mcp.md` both rank those
  as fast-rotting and internally inconsistent by a factor of five, and none of the three plays
  needed one to make its point. Worth copying rather than re-deriving: the argument for MCP is a
  boundary-crossing argument, and it does not get stronger with a server count attached.
- **The `description`-is-the-routing-table finding survived contact with a play and is the single
  most actionable thing in `notes/research/skills.md`.** It is the pivot of *Package repeatable
  expertise*'s worked example (a skill that sat unfired for two weeks under the description "Index
  mapping utilities"). The Team suite's shared-skill-library play will want the same finding from
  the other end — a library whose skills were described by their authors, for their authors.

- **Milestone 10 named milestone 5's gotchas (a) and (c), spent (d), and deliberately left (b)
  unnamed.** (a) is **the Tidy Summary** in *Decompose into subagents*; (c) is **the Clean Merge**
  in *Work in parallel without collisions*; (d) — the fan-out that was a compute budget — is a step
  and
  a checklist item in *Decompose into subagents*, which is the right weight for it, since the
  remedy ("give one agent the same budget and measure") is cheaper than the diagnosis. (b), the
  brief-travels-conversation-does-not asymmetry, is stated as step 5 of that play and named nowhere.
  The handoff note asked whether it wanted the Brief That Never Arrived's name; the answer is no,
  and neither does it want a third. They are different phenomena — one is a file that never loaded,
  the other is a file that loaded correctly while an unwritten convention did not travel — but the
  second has no separate tell a reader could act on beyond "write it down", which is already the
  step. A
  name with no tell is decoration.
- **The Orchestration suite's plays are the first in Part II whose evidence mostly argues against
  their own subject.** Each play cites a vendor or a study limiting the technique it teaches, in
  *The play* rather than in a caveat at the end. That is the sceptical spine milestone 5 identified,
  and it survived contact with the template: the five-of-six protocol-matched comparison sits inside
  a
  numbered step, not in the failure mode. Worth copying for Part III, which owns the same posture at
  chapter length.
- **The `single-agent-wins.md` brief is left largely unspent on purpose.** The Orchestration suite
  draws one figure from it. Its best material — Anthropic's "optimizing single LLM calls with
  retrieval and in-context examples is usually enough", the AssetOpsBench latency result with both
  halves, and the METR doubling-time trend — belongs to *Know when not to use an agent*
  (`bffa217221ed`), and spending it three plays earlier would have left that play re-deriving an
  argument the book had already made.
- **Milestone 10 hit no 100-column overshoots and no budget overruns**, having run a throwaway width
  checker from `/tmp` and the build's own `word_count` per section. That is the fourth independent
  writing of the width checker, and the second task to discover that `scripts/build_book.py` already
  contains the section-accurate word counter that makes budget compliance checkable rather than
  estimated. Board item `6b0110f76388` should land both: a long line is a problem, and a section
  over its template budget is at least a note.
- **The Orchestration suite cites four of milestone 5's seven briefs and no adoption figures**, on
  the precedent the Harness suite set. No LangChain download counts, no n8n valuation, no tool
  table: two of the best-known parallel-agent tools in that table died or announced sunset inside a
  year, and the plays name tools only where a mechanic is that vendor's — `tools: Read, Glob, Grep`
  and the
  git-redirect block list, both attributed to Claude Code 2.x in the sentence that uses them.

### Failure-mode registry

One name per phenomenon across the whole book. Check here before coining a name; append yours
here when you do. Convention is in [`book/STYLE.md`](../book/STYLE.md#naming-failure-modes).

| Name | Phenomenon | First used in |
|---|---|---|
| **the Context Landfill** | A brief that only ever grew; stale and current instructions weighted equally. | `context/write-the-brief-the-agent-reads.md` (coined in `book/STYLE.md` sample 4) |
| **the Merged Hand** | Agent run started on a dirty tree; the diff interleaves two authors and can be neither kept nor discarded. | `book/TEMPLATE-play.md` specimen play |
| **the Brief That Never Arrived** | Instructions written, committed, and never loaded. Nothing errors, and the usual check reports the same thing whether they loaded or not. | `context/write-the-brief-the-agent-reads.md` |
| **the Flattering Dashboard** | A tool reports large savings measured at its own boundary, against a counterfactual the billing system never applies, while the bill rises. | `context/starve-the-context.md` |
| **the Permanent Near Miss** | Every run ends just short of done and every continuation also ends just short; no turn presents itself as the one to stop on. | `context/scope-a-task-to-fit-the-window.md` |
| **the Paper Fence** | A rule that forbids something and does not stop it: it matches the spelling the agent usually produces, so uneventful runs read as evidence. Covers the prose version too — an instruction mistaken for enforcement. | `harness/choose-your-harness.md` |
| **the Unsummoned Skill** | A skill that is written, committed, and never triggered. The metadata loaded as designed and lost the match; a non-match is not an event anything logs. | `harness/package-repeatable-expertise.md` |
| **the Instruction You Did Not Write** | Agent behaviour that traces to nothing in your repository, because it arrived in a tool description — authored context from a connected server. | `harness/wire-in-the-outside-world.md` |
| **the Tidy Summary** | A delegated worker returns a well-organised, correct-as-far-as-it-goes summary that reads identically whether the work was thorough or partial. The compression is why you delegated; it is lossy exactly where you would check. | `orchestration/decompose-into-subagents.md` |
| **the Load-Bearing Scaffold** | A scripted stage built around a capability gap that has since closed, which can no longer be removed because retry logic, metrics, and neighbouring stages have grown into it. | `orchestration/make-the-control-flow-deterministic.md` |
| **the Clean Merge** | Git reports success, both branches were green, and the merged tree was never tested by anyone. The conflicts git can see are the survivable class; the expensive class exists only in the union. | `orchestration/work-in-parallel-without-collisions.md` |
