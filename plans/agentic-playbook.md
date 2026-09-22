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

- Book chapters live in `book/`, research notes in `notes/research/`, raw ideation in
  `notes/raw/` (frozen — do not edit).
- Every play uses the template defined by the style-guide task: Problem → The play → Worked
  example → Failure mode → Checklist.
- Research notes are cited notes, not prose. Writers draw from them.
- Any build/helper scripts are Python, not Node.
- Prose wraps at 100 columns; diagrams are mermaid, never ASCII art.
- Repo-wide conventions are recorded as cards in `cards/` and indexed from the root `CLAUDE.md`.
- `make html` and `make pdf` collect the book and render it; `make check` reports orphans,
  missing files and style defects, and `make lint` reports the style defects alone. Output goes
  to `build/`, which is gitignored and never committed. See
  [`cards/building-the-book.md`](../cards/building-the-book.md).
- Running `make check` or `make lint` writes `scripts/__pycache__/` as a side effect. It is
  gitignored, along with `*.pyc`, and must never be committed — a stale bytecode copy shows up as
  a spurious modification in every later diff.

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
| 11 | Verification & Trust play suite | `4858fbdecdf4` | ✅ done |
| 12 | Economics play suite | `bffa217221ed` | ✅ done |
| 13 | Team play suite | `cdd27e440781` | ✅ done |
| 14 | Part III — Where It Struggles | `c1416f44c483` | ✅ done |
| 15 | Part IV — Next Waves, plus appendices | `bec9accd89be` | ✅ done |
| 16 | Editorial pass — one voice, one book | `934259dc8038` | ✅ done |
| 17 | Run every worked example for real, re-capture output | `3b61a6a1a684` | ✅ done |
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
| `6b0110f76388` | Add a 100-column / style lint to `make check`, after four authors wrote the same one | ✅ done |
| `fce3cee8fa34` | Trim three marginal budget overruns — all three now inside budget, and the shared clause varied | ✅ done |
| `9dd4d6b84b80` | Define *skill*, *card*, *harness* on first use, per Part I's promise — one gloss in the Context suite closed all three | ✅ done |
| `57772ad900e3` | Verify the seven primary sources that resisted automated fetch — all seven opened; three changed what the book may say, and one of those was already in print | ✅ done |
| `f94b88e05069` | Milestone 19 — audit of the author's own posts; found them unspent, fixed the cause, filed the three chapters that owe them | ✅ done |
| `703e507c86aa` | Write the cards play — the Context suite's fourth; one failure mode, one worked example that is this repo | ✅ done |
| `0bdccc346bd4` | Thread preparation-vs-execution into Part I — milestone 19's last filing; the rocket-launch material is now spent | ✅ done |
| `5e0f39858134` | Check Part IV Wave #2 carries the feature-first argument — carried in full; two missing links added | ✅ done |
| `f986730f7a1f` | Verify the MCP incident citations in the Harness suite against primary sources — both incidents hold, one framing was wrong and is corrected in print | ✅ done |
| `f0669b48dbc0` | Untrack `scripts/__pycache__` and gitignore it — already untracked by `37dfb14`; added the `*.pyc` half and confirmed nothing else generated is tracked | ✅ done |
| `3884b4f3fc82` | Re-check Part III's remaining derived figures — 26 sources opened, eleven defects in print, four of them the same species as the reward-hacking trio | ✅ done |
| `023ba519cdd0` | Teach `make lint` the word budgets — every budget in `STYLE.md` and `TEMPLATE-play.md`, counted with the build's own counter; eleven overruns found that nobody had ever counted | ✅ done |
| `bfc99c593aeb` | Trim the eleven Part II overruns — all eleven inside budget, and over-budget promoted from a note to a problem | ✅ done |
| *unassigned* | Say what context engineering is worth, in the Context opener — written as a scorecard, paid for out of the four play blurbs. See [*Two proposals from the author's reflection*](#two-proposals-from-the-authors-reflection) | ✅ done |
| *unassigned* | A fourth Team play — written, as *Settle what the team cannot agree*, on deciding rather than on facilitating. See [*Two proposals from the author's reflection*](#two-proposals-from-the-authors-reflection) | ✅ done |

## Current state / handoff

**The manuscript is complete, has been through its editorial pass, its worked examples have been
run, its unreadable primary sources have now been read, and its central term has been renamed.** 40
files, 40,825 words, a preface, a root `README.md`, and one voice.

**Start with the terminology rename if you are editing anything.** What the book called a *brief*
is now an **agent file**, and what it called a *research brief* is now a **research note** — the
one word had been doing both jobs. Two plays and one card changed filename with it, so **a link
written from memory against the old paths is dead**. The reasoning, the rejected alternatives and
what the rename cost are the four newest entries in the [decisions log](#decisions-log-append-only). What the editorial pass changed and what it deliberately left alone
is in [*The editorial pass*](#the-editorial-pass) below; read that before editing any chapter,
because several conventions in this section were corrected by it. What the verification pass
changed, and the new obligation it puts on anyone editing a worked example, is in [*The verification
pass*](#the-verification-pass) below. **Read that one before touching any block that prints command
output.**

**And read [*The source-verification pass*](#the-source-verification-pass) and [*The Part III figure
re-check*](#the-part-iii-figure-re-check) before writing a sentence containing a number.** The
second one is the more alarming of the two: `57772ad900e3` found one falsified passage in print, and
`3884b4f3fc82` went looking for more of the same species in Part III and **found four, plus seven
other defects**. The habit that catches them is in the re-check's own section and is one line long —
**when a number is precise, find out what it is a percentage of.**

Board item `57772ad900e3` opened the seven primary sources that three
research passes could not, and the news is not that they were reachable — it is that one of them
**falsified a passage already in print**. Part III's per-model reward-hacking figures were a
secondary write-up's arithmetic on a table nobody had opened; they are wrong, they pointed the wrong
way, and the section has been rewritten around what the system card actually says. Two new entries joined `evidence.md`'s
do-not-cite list, both of the same species: a number that looks like a finding because somebody
computed it from a primary source without reading it.

The rest of this section is the accumulated handoff from the writing milestones, kept because it
records why each part is the way it is.

`book/` holds the three constraint documents every author works within:

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
the agent files compress them.

**Attribution convention.** Absorb this material into the book's own voice. Do not cite it in-line
as an external source — "the argument is made well in *The unit of work*" reads oddly in a book by
the person who made it. URLs go in the appendix's further reading. This is the one case where the
"cite the source" reflex produces worse prose.

**Part IV authors specifically:** Wave #2 is defined in `notes/raw/idea.md` as "refactoring
projects, optimize for full agent development". *The unit of work* is what that refactor consists
of — feature-first layout, locality of behaviour, explicit over invisible control flow, and the
nuance that cross-cutting concerns still belong in shared infrastructure as trustworthy black
boxes rather than hidden magic. **This is now done and checked** — milestone 15 wrote it and
`5e0f39858134` confirmed it; see [*The Wave #2 check*](#the-wave-2-check) below for what the check
found and the one thing it changed.

`notes/research/` now exists. Milestone 4 filled it with six files — a hub research note plus five
subject agent files, because five subjects in one file would have made a writer chasing token-pricing
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
   simply stale. The hub agent file names one of them explicitly as an example rather than a source.
   **This rule is about third-party claims of fact, and it does not apply to the author's own
   posts.** Those are not evidence to be corroborated, they are the book's own material — see
   "The author's own material" below. Milestone 19 found that this line, read literally, had
   filtered them out of the Context suite entirely.
2. **The staleness table in `tooling.md` ranks every finding by how fast it rots**, with a
   suggested hedge for each. Use it rather than re-deriving where the line is; it is consistent
   with `book/STYLE.md` on volatile facts.
3. **Each agent file ends with a `## Concrete example we can lift`** written to be dropped into a
   *Worked example* heading. They are illustrative-but-correct per the locked decision — real
   commands and real file contents, no invented captured output.

Milestone 5 added seven more files on the same hub-plus-agent files pattern, feeding the Orchestration
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
roughly 4,100 words — 1,487 / 1,448 / 1,169 after the budget trim below, and 1,525 / 1,445 / 1,180
as milestone 7 left it — which sits inside the ~15% share once Part II exists at its planned size.
It also produced an eighth research note,
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
opener and three plays at roughly 293 / 1,116 / 1,144 / 1,074 words after the budget trim below. It
is the first suite written, so it is also the first test of the template, and three things in it
constrain the suites that follow:

| File | Owns |
|---|---|
| [`context/index.md`](../book/part-2-plays/context/index.md) | The suite opener — names *signal over noise* as the suite's single idea and frames the three plays as that move at three layers |
| [`write-the-agent-file-that-actually-gets-read.md`](../book/part-2-plays/context/write-the-agent-file-that-actually-gets-read.md) | Project context files: what belongs, what bloats, the portable `AGENTS.md` + import setup, and verifying the agent file loaded |
| [`starve-the-context.md`](../book/part-2-plays/context/starve-the-context.md) | Deliberate reduction, just-in-time loading, and the paired-run method for measuring any filtering tool |
| [`scope-a-task-to-fit-the-window.md`](../book/part-2-plays/context/scope-a-task-to-fit-the-window.md) | Unit-of-work sizing, external requirement lists, the stop rule, and file-based handoff between sessions |

1. **Four failure modes are now registered, three of them new.** The Context suite claimed **the
   Context Landfill** as `book/STYLE.md` invited, and coined **the Agent File That Never Arrived**, **the
   Flattering Dashboard**, and **the Permanent Near Miss**. Check the registry before naming
   anything adjacent — in particular, the Orchestration suite's "a subagent inherits the written
   agent file but none of the conversation" is arguably the same phenomenon as the Agent file That Never
   Arrived and may want that name rather than a second one.
2. **The `rtk` worked example is spent.** It carries *Starve the context*'s Worked example, with the
   JetBrains and Quesma figures dated and versioned. Economics may cite the figures, but should not
   build *Understand what you are paying for* around the same scenario; the running log below flags
   a swap.
3. ~~**Three plays per suite held comfortably**, and no fourth was wanted.~~ **Superseded**
   by `703e507c86aa`, which added [*Split the agent file into
   cards*](../book/part-2-plays/context/split-the-agent-file-into-cards.md) as the suite's fourth. The
   material was not missing when milestone 8 ran; it was filtered out by the cite-vendor-docs rule,
   which milestone 19 found had been read as excluding the author's own posts. See
   [*The cards play*](#the-cards-play) below.

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
   the Context suite expected; note it is deliberately *not* the same as the Agent file That Never
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
| [`work-in-parallel-without-collisions.md`](../book/part-2-plays/orchestration/work-in-parallel-without-collisions.md) | Partition-plus-escape-clause agent files, worktrees as ergonomics rather than a boundary, landmine files, overlap preflight, and sequential integration with the suite run on the merged tree |

Five things in it constrain later tasks:

1. **Three failure modes are registered**, all new: **the Tidy Summary**, **the Load-Bearing
   Scaffold**, and **the Clean Merge**. The first is milestone 5's gotcha (a). Gotcha (c) is the
   Clean Merge. Gotcha (b) — the agent file travels, the conversation does not — was **used and
   deliberately left unnamed**: it appears as step 5 of *Decompose into subagents* rather than as a
   second name next to the Agent File That Never Arrived, which the handoff note flagged as a possible
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

Milestone 11 added `verification-and-trust/`, the fourth suite, at roughly 314 / 1,152 / 1,232 /
1,179 words. It spends milestone 6's `review-practice.md`, `verification.md` and `accountability.md`
in full, and it is the suite the book's credibility rests on, so it is also the one that carries the
most contested evidence inside *The play* rather than in a caveat.

| File | Owns |
|---|---|
| [`verification-and-trust/index.md`](../book/part-2-plays/verification-and-trust/index.md) | The suite opener — names *everything the agent produces about its own work is a claim, and the signals worth acting on come from outside its turn* as the suite's one idea, and frames the three plays as that at the diff, the harness, and the team |
| [`review-code-you-did-not-write.md`](../book/part-2-plays/verification-and-trust/review-code-you-did-not-write.md) | Review order — the things that check the code read before the code, size-based send-back, duplicate search, one traced path, the reproducer rule, and the agent's plan used to triage rather than to read through |
| [`make-the-agent-prove-it.md`](../book/part-2-plays/verification-and-trust/make-the-agent-prove-it.md) | Finish conditions with a check inside them, deterministic stop gates and their override, the fakeability ranking rendered as a ladder, evidence over verdicts, and who owns the test |
| [`decide-who-signs-off.md`](../book/part-2-plays/verification-and-trust/decide-who-signs-off.md) | A named owner and what owning means, the moral-crumple-zone counter-argument carried in the same document, the right to decline on volume, the four competing disclosure trailers, and where the real regulatory constraint lives |

Five things in it constrain later tasks:

1. **Three failure modes are registered.** **The Drifting Yes** and **the Accountable Bystander**
   are new. **The Green Suite That Tests Nothing** was coined in `book/STYLE.md`'s naming section
   and is claimed here, exactly as the Context suite claimed the Context Landfill — it is milestone
   6's phenomenon (c), which `evidence.md` assigned to *Make the agent prove it* by name.
   Phenomena (a), (b) and (d) from that pass are **untouched and still free for Part III**.
2. **The suite uses `tideline`, a TypeScript service that stages firmware rollouts to field
   devices**, across all three worked examples. TypeScript is a content decision on the milestone-10
   precedent: the fakeability ranking puts the type checker at the top, and the evasions that make
   the point — a widened type, a deleted `typecheck` step — need a stack that has one. Two suites
   still need their own project.
3. **The curl bug-bounty arc is unspent and is recommended to Part III.** The hub's worked-example
   map offered it to *Review code you did not write*; the play declined it, because the reader's
   problem is reviewing agent pull requests at volume and curl's arc is about inbound vulnerability
   reports. It survives intact, including the April 2026 half that most citations drop, and it is
   the sharpest available illustration that the incentive rather than the tool was the variable.
4. **The play-count question was raised and answered as three.** The running log flagged that this
   suite had more strong worked examples than plays. It does, and the surplus is not a fourth play:
   the mandate-study displacement example is Part III's and Economics', and the two arguments about
   the same green suite are one play's (*Make the agent prove it* carries the visible/held-out gap)
   and Part III's (the `sys.exit(0)` harness escape, which this suite deliberately does not spend).
5. **Part I's *verification tax* is used in the same words**, in *Review code you did not write*,
   as the name for review effort displaced from writing onto checking. Economics and Part III should
   keep using it rather than coining a second term.

Milestone 12 added `economics/`, the fifth suite, at roughly 299 / 1,178 / 1,167 / 1,137 words. It
spends `token-economics.md` and `single-agent-wins.md` in full, and it is the suite most exposed to
staleness, so it follows that agent file's hedging strategy literally: ratios in the prose, every dollar
figure confined to one dated block inside one worked example.

| File | Owns |
|---|---|
| [`economics/index.md`](../book/part-2-plays/economics/index.md) | The suite opener — names *cost is a product, not a price: price per token × tokens consumed × attempts per shippable result* as the suite's one idea, and frames the three plays as that at the session, the model, and the task |
| [`understand-what-you-are-paying-for.md`](../book/part-2-plays/economics/understand-what-you-are-paying-for.md) | The Θ(n²) turn-count mechanism, input as the bulk of the bill, the cache-read multiple and what invalidates it, reasoning budget as a first-order control, and reconciling the harness's estimate against the provider's bill |
| [`match-the-model-to-the-job.md`](../book/part-2-plays/economics/match-the-model-to-the-job.md) | Cost per accepted outcome, tiering down the fan-out rather than the reasoning, the cheap-oracle precondition, measuring turns in a paired run, effort as a separate dial, and why per-token prices do not compare across generations |
| [`know-when-not-to-use-an-agent.md`](../book/part-2-plays/economics/know-when-not-to-use-an-agent.md) | Costing the alternative including review, specification as the expensive part, the no-cheap-check rule, fan-out as a multiplier, why neither the agent nor an expert can estimate the job, and dating the no-go list |

Five things in it constrain later tasks:

1. **Three failure modes are registered**, all new: **the Expensive Nothing**, **the Long Way
   Round**, and **the Errand That Became a Project**. None of milestone 6's four unnamed phenomena
   was taken — all four remain free for Part III, including the two the Context and Verification
   suites deliberately left alone.
2. **Every absolute price in the book now lives in one place**, the dated block inside *Understand
   what you are paying for*'s Worked example. The prose across all three plays uses multiples only
   ("about a tenth of a fresh input token", "four to eight times the input rate", "roughly fifteen
   times the tokens of a chat interaction"), and no play names a current model in a sentence that
   carries an argument. If a later chapter needs a dollar figure, add it to that block rather than
   opening a second front.
3. **The suite uses `granary`, a Kotlin service ingesting warehouse stock feeds from forty
   suppliers**, across all three worked examples. Kotlin is a content decision on the milestone-10
   precedent: *Know when not to use an agent* turns on a deterministic IDE rename beating an agent
   outright, which needs a stack where that refactoring is reliable. `atlas`, `kestrel`, `meridian`,
   `tideline` and `granary` are taken; only the Team suite still needs one.
4. **Part I's *verification tax* is used in the same words** in two of the three plays, as the name
   for the cost that relocates from writing to checking. Part III should keep using it.
5. **The mandate study is spent here as well as in Part III**, as the closing argument of *Know when
   not to use an agent* — throughput 2.09×, review coverage 89%→68%, cycle time +22%, merge and
   revert flat. `evidence.md` assigned it to both. The Economics use is three sentences making the
   review-capacity point; Part III has the room to carry it at length and should not assume it is
   unspent.

Milestone 13 added `team/`, the sixth and final suite, at roughly 300 / 1,141 / 1,140 / 1,204 words.
It closes Part II. It spends the late author fragment in full and is the one suite with almost no
quantitative evidence behind it, which shapes how it is written: the arguments are mechanisms, and
the three figures it does print are all dated and attributed.

| File | Owns |
|---|---|
| [`team/index.md`](../book/part-2-plays/team/index.md) | The suite opener — names *a team's practice with these tools is an artefact that has to be written, maintained, and handed over like any other* as the suite's one idea, and frames the three plays as the decisions, the material, and the transfer |
| [`build-the-working-agreement.md`](../book/part-2-plays/team/build-the-working-agreement.md) | The leaves-your-machine sort as the team-versus-personal test, the six items with team-visible consequences, triggers rather than review dates, the standing experiment exception, and a full one-page starter agreement |
| [`collect-and-refine-as-a-team.md`](../book/part-2-plays/team/collect-and-refine-as-a-team.md) | The harvest: comparing on one task shape, asking for discarded runs first, promoting artefacts rather than anecdotes, descriptions written by somebody other than the author, and deleting something every time |
| [`onboard-someone-into-all-this.md`](../book/part-2-plays/team/onboard-someone-into-all-this.md) | The checkout as the setup, verification as a step, watching a run before driving one, first tasks with a cheap check, and the joiner as the only free audit of the shared material |

Five things in it constrain later tasks:

1. **Three failure modes are registered**, all new: **the Founding Document**, **the Showreel**, and
   **the Fluent Stranger**. None of milestone 6's four unnamed phenomena was taken, so all four are
   still free for Part III, as are the three in `failure-modes.md`. The Founding Document is
   deliberately *not* the Paper Fence — one is a rule that does not stop a machine, the other is a
   rule the people have drifted from — and the registry note says so.
2. **The Team suite supplies the working-agreement skeleton the appendices open question was
   waiting on.** The Worked example of *Build the working agreement* is a complete one-page
   agreement in a fenced block, written to be copied. The appendix should extract it rather than
   invent a second one, exactly as the resolved `CLAUDE.md` question sends the appendix to the
   Context suite. That closes the last half of the appendix-templates question.
3. **The local-context-file precedence trap is treated as an instance of the Agent file That Never
   Arrived, not as a new name.** Milestone 4's gotcha (c) — a `CLAUDE.local.md` silently stopping
   `AGENTS.md` loading, with `/context` reporting the same list either way — is the phenomenon the
   Context suite already named. Both *Collect and refine as a team* and *Onboard someone into all
   this* use the name plainly and link to the Context play. **Gotcha (c) is therefore spent, and no
   later suite should coin a second name for it.**
4. **The suite uses `lodestone`, a claims-processing platform of C# services behind a TypeScript
   front end, maintained by nine engineers across two time zones.** The mixed stack is a content
   decision on the milestone-10 precedent: *Onboard someone into all this* turns on one half of a
   codebase having a cheap check and the other half not, which needs a team that is not homogeneous.
   All six suite projects are now taken — `atlas`, `kestrel`, `meridian`, `tideline`, `granary`,
   `lodestone`.
5. **Part I's exchange-rate promise and the *verification tax* are both honoured.** Each play states
   what the reader gives up, and the review-displacement material is cited by its figures rather
   than by coining a second term for the tax.

Milestone 14 added `book/part-3-where-it-struggles/`, four chapters at roughly 1,233 / 1,346 / 1,213
/ 1,435 words, 5,227 in total — 16% of the book as it currently stands, which lands on the ~15%
share once Part IV and the appendices exist. It spends `failure-modes.md` and
`productivity-evidence.md` in full, takes both artefacts `evidence.md` reserved for it, and is the
only part written to be read *first* by a sceptical reader, which Part I promises it will be.

| File | Owns |
|---|---|
| [`what-agents-are-reliably-bad-at.md`](../book/part-3-where-it-struggles/what-agents-are-reliably-bad-at.md) | Finishing, wrong-but-compiling, the public/commercial benchmark gap, security unevenness by weakness class, degradation across self-iteration, and the `sys.exit(0)` arc with its generalisation |
| [`the-failure-modes-worth-naming.md`](../book/part-3-where-it-struggles/the-failure-modes-worth-naming.md) | Six new names with a tell and a response each, plus the index of every failure mode in the book |
| [`where-the-time-actually-goes.md`](../book/part-3-where-it-struggles/where-the-time-actually-goes.md) | METR's time reallocation and perception gap with the full qualifier chain, the mandate study's interior, the verification tax, and the four things nobody has measured |
| [`what-is-genuinely-contested.md`](../book/part-3-where-it-struggles/what-is-genuinely-contested.md) | Six live disagreements carried with both halves: speed, quality, capability-and-reward-hacking, benchmark validity, the curl arc, and who is responsible |

Five things in it constrain later tasks:

1. **Six failure modes are registered, and that closes the naming programme.** All four of milestone
   6's unnamed phenomena and all seven in `failure-modes.md` are now spent. **the Confident Wrong
   Rewrite** is claimed from `book/STYLE.md`'s naming section, on the Context and Verification
   precedent, which leaves no style-guide example unclaimed. The others are **the Vanishing Fix**,
   **the Requirement It Can Still Quote**, **the Endless Polish**, **the Immaculate Surface**, and
   **the Instant Concession**.
2. **Part I's "there is no name for it" sentence is rewritten, as the handoff asked.** *Before Git,
   before Scrum, before this* now says the phenomenon has no *agreed* name, names it as the
   Vanishing Fix, and links to Part III; Part III links back. The contradiction the milestone-7 note
   warned about does not exist, and the editorial pass does not need to fix it.
3. **Part III carries the book's index of failure modes**, at the end of *The failure modes worth
   naming*: 25 names, one line of symptom each, linked to the chapter that describes them. **The
   appendices task should link to it rather than duplicate it** — a second list is a second thing to
   keep in step with the registry in this file.
4. **Both of `evidence.md`'s reserved artefacts are spent, in different chapters.** The
   `sys.exit(0)` reward-hacking arc closes *What agents are reliably bad at*, carrying the 50%
   alignment-faking and 12% sabotage generalisation and the inoculation-prompting fix that
   Verification deliberately left alone. The mandate study is in *Where the time actually goes*, and
   deliberately **not** by its headline figures — Economics and Team already spent those. Part III
   takes the interior: the composition-versus-individual gap (2.09× per capita against 1.46–1.72×
   within a developer), the heterogeneity breakdown, and the authors' "not typical, immediate, or
   free" caveat.
5. **No suite project appears in Part III, on purpose.** These are not plays, there is no *Worked
   example* heading, and every scenario in the part is a published study. `atlas`, `kestrel`,
   `meridian`, `tideline`, `granary` and `lodestone` stay Part II's.

Milestone 15 added `book/part-4-next-waves/` and `book/appendices/` — three chapters at roughly
600 / 1,390 / 1,350 words and four appendices at 3,637 words in total. It closes the writing
programme. Part IV lands at 9% of the book and the appendices at a further 9%, which puts Part II at
58% and Part I at 11% on the build's own counter — the first point at which the 15 / 60 / 15 / 10
proportions can be read against a finished manuscript rather than a partial one.

| File | Owns |
|---|---|
| [`the-three-waves.md`](../book/part-4-next-waves/the-three-waves.md) | What a wave is, why wave one is the rest of the book, and the four-point contract for discounting the part: dated, unstudied, falsifiable, and ending on the part worth doing anyway |
| [`refactoring-a-codebase-for-agents.md`](../book/part-4-next-waves/refactoring-a-codebase-for-agents.md) | Wave two — the constraint swap, feature-first layout, invisible control flow, what stays in shared infrastructure, the four properties that are not layout, and the experiment that would settle it |
| [`inviting-non-developers-in.md`](../book/part-4-next-waves/inviting-non-developers-in.md) | Wave three — requester versus co-pilot, the four conditions for an outside change to be safe, who carries the review cost, and the low-code precedent nobody can quote |
| [`appendices/glossary.md`](../book/appendices/glossary.md) | Twenty-two terms, each defined by behaviour, with vendor-specific and contested ones marked as such |
| [`appendices/team-checklists.md`](../book/appendices/team-checklists.md) | Six one-page suite checklists, eight items each, selected by "keep what another person would notice the absence of" |
| [`appendices/copy-paste-templates.md`](../book/appendices/copy-paste-templates.md) | The two-tier agent file and card skeleton, the working-agreement skeleton, and a review checklist for agent-authored changes |
| [`appendices/further-reading.md`](../book/appendices/further-reading.md) | Entry points into the twenty-one research notes by subject, roughly thirty primary sources, the author's two posts, and the five figures that do not survive being looked up |

Five things in it constrain later tasks:

1. **No failure mode was coined**, so the registry closes exactly where milestone 14 left it at 25
   names. Part IV names none of its own and refers to three by name in passing — the Confident Wrong
   Rewrite, the Load-Bearing Scaffold, and the Accountable Bystander — each plain rather than bold,
   because none of them is first use.
2. **The appendices link rather than duplicate, in three places, and that is load-bearing.** The
   glossary points at Part III's index of failure modes instead of restating the names; the team
   checklists compress rather than concatenate the eighteen play checklists; the templates appendix
   extracts the working agreement from *Build the working agreement* rather than authoring a second.
   A later edit that "completes" any of the three by copying the original in creates a second thing
   to keep in step.
3. **The templates appendix now carries a card skeleton, and the unwritten cards play
   (`703e507c86aa`) has to agree with it.** The appendix states the pattern in three sentences — a
   slim always-loaded index with a trigger per entry, self-contained files, one card one load no
   chains — and shows a skeleton. The play owns the argument; if it reaches a different shape, the
   appendix is the file to change.
4. **Board item `5e0f39858134` can be checked.** Wave two is built on the feature-first argument as
   the handoff asked, absorbed rather than cited: the constraint swap, the six-files-per-feature
   cost, locality of behaviour, explicit over invisible control flow, and the trustworthy-black-box
   nuance for cross-cutting concerns. The post's URL is in further reading, which is where the
   attribution convention puts it.
5. **`9dd4d6b84b80` is half-answered.** *Skill*, *card* and *harness* are now all defined in the
   glossary, which satisfies the second half of Part I's promise ("defined where they are first used
   and collected in the glossary"). The first half — *card* being used before it is defined, in
   *Write the agent file that actually gets read* — is still open and still belongs to the cards play.
   **Superseded:** `9dd4d6b84b80` closed the other half without waiting for that play. See
   [*The terminology pass*](#the-terminology-pass) below.

Milestone 16, the editorial pass, then read the whole book as one object for the first time and
reconciled it. Its output is summarised under *The editorial pass* below.

Milestone 17, the worked-example verification pass, then ran every command in the book and replaced
representative output with captured output. Its output is summarised under
*The verification pass* below.

**The style lint (`6b0110f76388`) is built**, and it took the `> Captured` check the editorial
pass asked for. `make check` now runs it, `make lint` runs it alone, and what it checks and what
it deliberately exempts is under *The style checker* below. **Run it instead of writing a fifth
throwaway one.**

**The three marginal budget overruns are trimmed (`fce3cee8fa34`)** — Part I and the Context suite
are now inside every budget in `STYLE.md` and `TEMPLATE-play.md`. What was cut, and the one thing a
future edit to *Before Git, before Scrum, before this* should know, is under
[*The budget trim*](#the-budget-trim) below.

**The Context suite has a fourth play (`703e507c86aa`)** — *Split the agent file into cards*, which
writes up the two-tier pattern this repo runs on itself. What it commits future edits to, including
the fact that `cards/` is now asserted by a script the book depends on, is under [*The cards
play*](#the-cards-play) below. **Read that one before editing anything in `cards/`.**

**Part I's terminology promise is kept (`9dd4d6b84b80`)** — *skill*, *card* and *harness* are now
each defined the first time the reader meets them, in book order. What changed and what it commits
the unwritten cards play to is under [*The terminology pass*](#the-terminology-pass) below. **If you
are about to introduce a term the reader may not have, read that section first** — it settles where
the italics go when a term is used in one suite and owned by another.

**Part I now names preparation mode and execution mode (`0bdccc346bd4`)** — the last of milestone
19's three filings, and the last of the author's own material to go unspent. Where it landed, why it
is framing rather than a play, and what it commits Part II to is under [*The preparation
thread*](#the-preparation-thread) below. **Read it before adding a play that starts with something
already broken.**

**Part IV's Wave #2 is checked and holds (`5e0f39858134`)** — the feature-first argument is carried
in full and correctly absorbed rather than cited, and the check's only edits were the two missing
links. What it found, and the one chapter it left near its ceiling, is under [*The Wave #2
check*](#the-wave-2-check) below.

**The MCP citation verification is done (`f986730f7a1f`), and with it the follow-up table above is
clear.** Both incidents the Harness suite cites survive contact with primary sources; one of them
was described wrongly and the sentence has been corrected in print. See [*The MCP citation
check*](#the-mcp-citation-check) below, and read it before writing any sentence that names a
compromised package — the correction it makes is the kind a writer repeats from memory.

**The word budgets are checked now (`023ba519cdd0`), and they were not being met.** `make lint`
counts every budget in `STYLE.md` and `TEMPLATE-play.md` — chapter, suite opener, whole play, and
each of a play's five sections — with the build's own `word_count`. It found **eleven overruns
nobody had ever counted**, all in Part II. **Do not count words by hand any more; run `make lint`
and read what it says against the file you touched.** What it checks and the eleven files are under
[*The word-budget check*](#the-word-budget-check) below.

**The eleven are trimmed, and the book is now inside every budget it states (`bfc99c593aeb`).**
40 files, 40,721 words, `make check` clean with no problems and no notes. That has never been true
before. **With it, over-budget stopped being a note and became a problem** — the user's decision,
taken on the record rather than quietly, because the argument for softness was the eleven overruns
and they are gone.

**Read this before you add a sentence to any play.** The trims land at 493–499 against a 500-word
ceiling in *The play*, so **nine plays have between one and seven words of headroom, and adding a
clause now fails `make check`.** That is deliberate and it is not negotiable by argument: take
something out in the same edit. What may go, what may not, and the twelve cuts this pass made are
under [*The overrun trim*](#the-overrun-trim) below — **read it before you decide what to remove**,
because two contracts constrain *The play* and one of them breaks silently.

**Three Part III chapters are still the tightest files in the book.** `3884b4f3fc82` found *What is
genuinely contested* sitting at **1,559** against a 1,500 ceiling — `57772ad900e3` added 143 words
to a chapter already at 1,435, and nothing checked per-chapter budgets, so `make check` reported
it clean. It is back to **1,498**, alongside *The failure modes worth naming* at **1,497**. Both
have single-digit headroom. The trim that paid for the corrections is itemised in the decisions
below; the one judgement call worth knowing is that it cut a closing clause from the
recently-rewritten reward-hacking section because it restated a sentence two earlier. Part I's
*What this book assumes about you* (1,444) and *Wire in the outside world*'s *The play*, at exactly
its 500-word ceiling, are the next tightest.

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

## The style checker

Board item `6b0110f76388` closed the oldest piece of recurring waste in the project. Milestones 7
and 8, the reassessment pass and the editorial pass had each written their own 100-column checker
in `/tmp` — four versions of the same twenty lines, of which the editorial pass's shipped two
defects into the prose before an adversarial re-read caught them. There is now one, it is checked
in, and it is reviewed once rather than rewritten per task.

| File | Owns |
|---|---|
| [`scripts/check_style.py`](../scripts/check_style.py) | Every rule a machine can decide, the exemption list, and a `--self-test` fixture holding the traps. One file, no dependencies, imports the build's fence state machine so "inside a fence" means one thing. |
| [`Makefile`](../Makefile) | `make lint`, and `make check` now runs both halves — always both, so a missing chapter does not hide a 104-column line until the next invocation. |
| [`cards/building-the-book.md`](../cards/building-the-book.md) | What it checks, what it exempts and why, and how to point it at a path outside `book/`. |

**The book passes clean**, which is the result worth stating: 42 files, zero problems, zero notes.
Nothing in the prose was changed to get there.

`make check` covers `book/` only, and the checker takes a path, so pointing it at `cards`,
`plans` or the root documents works. Doing that finds about a dozen 101-column lines in **this
file** and none anywhere else. They are left as they are on purpose: this is the one document
every parallel task edits, and reflowing a hundred lines of it to save a column would hand the
next four agents a merge conflict each. Wrap the lines you write; do not reflow the ones you
find.

Four things in it constrain later tasks:

1. **Do not write a fifth one, and do not count columns by hand.** The checklist in
   `book/README.md`, the working agreements in `CLAUDE.md` and both cards now say so. If a rule is
   wrong, change the rule and run `python3 scripts/check_style.py --self-test`.
2. **Every exemption is a decision somebody already made, and they are in the script with the
   reason attached.** Fenced blocks (a mermaid node in *Scope a task to fit the window* is 120
   columns and correct), table rows, a line that is one markdown link and some punctuation (the
   milestone-15 decision, 104–116 columns), anything inside double quotes for the vocabulary rules
   only, `book/STYLE.md` for the bans it has to print, and `book/examples/` for the same reason
   the build skips it. A checker that reports correct prose gets switched off within a week.
3. **Two traps are encoded as assertions rather than as comments.** Column counts are `len()` on a
   `str` — a byte-oriented `awk length()` overcounts every em dash by two, and this prose is full
   of them — and a `---` inside a ```` ```markdown ```` fence is sample content rather than
   frontmatter. Both are in the `--self-test` fixture, which is the file to read before changing
   anything.
4. **`> Captured` is checked**, as the editorial pass asked: the shape of the line, and that there
   is a fence under it. The other half of that convention — whether a block that looks like a
   transcript *has* a capture line — is not mechanical and is still a person's job.

## The word-budget check

Board item `023ba519cdd0` closed the gap the entry above left open. `make lint` now counts every
word budget the book states, and the first run of it found **eleven overruns in Part II that no
pass had ever counted** — `fce3cee8fa34` had checked Part I and the Context suite by hand, and
nothing had ever looked at the other five suites.

| Where it sits | Budget | From |
|---|---|---|
| a Part I or Part III chapter | 800–1,500 words | `book/STYLE.md`, *Length* |
| a suite opener (`<suite>/index.md`) | 150–300 words | same |
| a play, whole | 600–1,200 words | `book/TEMPLATE-play.md`, *Length* |
| a play's five sections | *Problem* 60–120, *The play* 200–500, *Worked example* 150–400, *Failure mode* 80–200, *Checklist* 4–8 items | `book/TEMPLATE-play.md`, the heading-by-heading contract |

Part IV, the appendices and the preface are **deliberately not counted**: no budget is stated for
them anywhere, and a checker that invents one is legislating rather than checking. A play whose
five `##` headings are not the template's, verbatim and in order, gets one note saying so and no
section counts — the sections cannot be identified, and guessing would be worse.

Six things in it constrain later work:

1. **Ten plays are over the 500-word ceiling in *The play*, and one is over as a whole.** They run
   from 2 words over (*Make the control flow deterministic*) to 34 (*Decide who signs off*), and
   *Onboard someone into all this* is 27 over the 1,200-word play ceiling as well. Six were written
   over budget; the editorial pass pushed four further over; and one — *Scope a task to fit the
   window* — was trimmed to 488 by `fce3cee8fa34` and then taken to **533** four commits later by
   `5e0f39858134`'s two-link fix, which added 45 words to a section already at its ceiling. That is
   the same species as the `57772ad900e3` regression, one level down, and it is why the check
   exists. Trimming them was filed as `bfc99c593aeb` and is **done** — see [*The overrun
   trim*](#the-overrun-trim) below. It was kept out of this item on purpose: it is a prose pass on
   eleven files in five suites, and mixing it into the commit that adds the checker would have put
   both beyond review.
2. ~~**Every budget report is a note, and that is the deliberate severity decision.**~~
   **Superseded by `bfc99c593aeb`: over-budget is a problem and fails `make check`.** The
   reasoning here still explains why it *was* a note, and it is worth keeping because it is the
   shape of the argument: the count is exact, the threshold is a judgement, and making it a
   problem while ten pre-existing overruns sat in the book would have handed every unrelated edit
   a red build it did not cause. That condition expired when the trim landed. The upgrade was the
   two-line change this note predicted, plus the self-test expectation, and it is now asserted in
   both directions — `budget_self_test` fails if a budget defect comes back as a note.
3. **The counter is the build's, imported, not a second one.** `check_style.py` now imports
   `word_count` from `build_book.py` alongside the fence state machine, so the lint, the per-part
   table `make check` prints, and any future count all agree. This is the trap `6b0110f76388`
   closed for column counting; a second word counter would have reopened it a percent or two out.
4. **The numbers are hard-coded, and `--self-test` checks they are still the book's numbers.**
   Both constraint documents state their budgets in sentences, and a regular expression over
   English is a worse contract than a constant with its source named. So each `Budget` carries the
   file it came from, and the self-test asserts the range is still printed there. **Move a number
   in `STYLE.md` or `TEMPLATE-play.md` and the self-test fails** until the script agrees. This is
   the answer to the item's "read them from the file if that is cheap": reading is not cheap,
   checking that the copy is honest costs four lines.
5. **Sections are split on the fence mask, not on a bare `##` scan.** *Build the working
   agreement*'s worked example prints a one-page agreement containing seven `##` headings inside a
   fenced block; counting those as sections would report the best-behaved play in the book for
   having the wrong headings. The mask `check_text` already builds for every other rule is what is
   passed in.
6. **The budget rules are in the self-test, including the two that decide whether it is usable.**
   A section one word outside its budget is reported (the margins are the point), a section exactly
   on either end is not, and a file with no stated budget is never given one. The play fixtures are
   generated rather than written out — a fixture that trips a 500-word ceiling has to contain 501
   words, and nobody would read it.

## The verification pass

Milestone 17 (`3b61a6a1a684`) spent the deliberate debt milestone 3 took on. Every command in the
book was run, every block that prints output is now either captured from a real run or is
demonstrably not a transcript, and the projects the captures came out of are committed. **The book
stands at 39 files and 39,370 words** — the pass added 93, all of them in worked examples whose
numbers moved.

**The one thing to know before editing a worked example:** captured output is now backed by a
committed scratch project under [`book/examples/`](../book/examples/), each with a `reproduce.py`
that builds a throwaway copy, runs the book's commands, and **asserts the shapes the prose depends
on**. Change the example, re-run the script. It will tell you when the book and the tree have
drifted apart, which is the whole reason it is committed rather than thrown away after the capture.

```
python3 book/examples/atlas/reproduce.py        # Context suite
python3 book/examples/meridian/reproduce.py     # Orchestration suite
python3 book/examples/tideline/reproduce.py     # Verification and Trust suite
python3 book/examples/session-cost/check.py     # Economics suite's arithmetic
```

Six things in it constrain later tasks:

1. **Eight blocks are now captured, and `> Captured <Month Year>, <tool> <version>.` means it.**
   They are in *Write the agent file that actually gets read* (two), *Decompose into subagents*,
   *Work in parallel without collisions* (two), *Decide who signs off*, and *Review code you did
   not write* (four). Everything else that looked like a transcript either prints no output or is
   framed in prose as somebody else's published figures.
2. **The capture corrected the prose four times, which is the finding.** *Review code you did not
   write* said 480 lines across nine files; the real `--stat` says 314, and every downstream number
   moved with it — three notes to the reviewer became four, "three things found" became four, and
   the `| head -4` in one block turned out to print only the diff header, so the command changed to
   one that shows what the sentence claims. None of this was visible by reading. **Assume a worked
   example's arithmetic is wrong until something has run it.**
3. **`session-cost/check.py` found a real defect in a table nobody doubted.** 940,000 tokens at
   $3.75 per million is $3.525 exactly — on a half-cent, so it rounds to $3.53 one way and $3.52
   the other. The play now prints three places. Every other figure in that table recomputes exactly,
   which is what makes the one that did not worth having.
4. **The evidence rules in `book/TEMPLATE-play.md` are rewritten and the first-draft dispensation
   is gone.** Output a command could produce is captured, not written; an example that genuinely
   cannot be run stays representative and may not print a plausible-looking result for the prose to
   lean on; and the capture corrects the prose rather than the other way round. `book/README.md`'s
   adding-a-file checklist gained two items enforcing it.
5. **The numbers audit came back clean, and that is worth not re-running.** Every figure in the
   book that reads like a measurement was traced: all of them are sourced to an agent file in
   `notes/research/`, expressed as shape, or part of a fictional scenario. None of the roughly forty
   figures on `evidence.md`'s **do not cite** list appears anywhere in the book. The two the
   Part IV chapter does name are named in order to refuse them, which is the correct use.
6. **`scripts/build_book.py` skips `book/examples/` entirely.** A new `NOT_BOOK_DIRS` constant sits
   beside `NOT_BOOK_CONTENT`: the scratch projects are apparatus, so they are never collected and
   never reported as orphans. `make check` is clean.

**One ordering note.** This pass was scheduled to run *before* the editorial pass so that pass
would see final text. It ran after it instead, because the editorial pass was unblocked first. The
prose this pass rewrote — most of it in *Review code you did not write*'s Worked example — is
therefore the only text in the book that milestone 16 has not read. It was written against
`book/STYLE.md` and sits inside its play's word budget, but a reader doing a final voice check
should start there.

What was deliberately left representative, and why, is tabulated in
[`book/examples/README.md`](../book/examples/README.md). The short version: `granary`'s two
`./gradlew` lines (no Gradle, and both blocks print nothing), `lodestone`'s clone from a fictional
remote, every harness settings file (config, not output — though all of them were parsed as JSON),
and the subagent and skill definitions, which are file contents.

## The source-verification pass

Board item `57772ad900e3` opened the seven primary sources that research passes 4, 5 and 6 had
flagged as unreadable by automated fetch, plus the Linux kernel file `accountability.md` said in so
many words the book "must not print a trailer syntax without checking". **All eight were obtained.
None of them is still a blocker.** The book gained 143 words, all of them in one rewritten section
of *What is genuinely contested*, and stands at **39 files and 39,513 words**.

**The headline is not that the sources were reached. It is that reaching them falsified something
already in print.** Part III said Claude Opus 4.5 reward-hacked at 18.2% against Sonnet 4.5's 12.8%
and Haiku 4.5's 12.6%, and concluded "the more capable model hacked more". Anthropic publishes no
such rates. It publishes a **five-column table**, and on the column that looks most like a
developer's real problem — coding tasks selected because earlier models hardcoded their way through
them — **Opus 4.5 scores 0%**, better than both smaller models. Two of the three figures turn out to
be the unweighted mean of a table row, averaging a 0% and a 55% from unrelated evaluations; the
third does not reproduce from either system card. The section has been rewritten around what the
table actually shows, which is a better argument: capability drove the hardcoding to zero and left
the model **less corrigible** — told explicitly not to cheat on impossible tasks, Opus 4.5 still
cheated on 35% against Sonnet 4.5's 20%, which Anthropic itself describes as being "comparatively
less corrigible when given instructions".

**Six of the seven were never really about the documents. They were about the retrieval method**,
and the patterns generalise well enough to be worth writing down:

| Barrier | What actually worked |
|---|---|
| "PDF resisted text extraction" / "exceeds the fetch size limit" | `curl` the PDF and run `pdftotext -layout`. The Copyright Office report, both Anthropic system cards and the 15 MB DORA report all extract cleanly. The limit was `WebFetch`'s, not the document's |
| Docs site behind an anti-scraping challenge (Fedora) | **Read the repository, not the site.** Fedora's policy is a plain `.adoc` file in a public Forgejo repo, clonable with `git clone`, with the approval date in its git history |
| `openai.com` and `help.openai.com` return 403 | `developers.openai.com` does not — and appending `.md` to any docs URL returns the page as clean markdown, no navigation chrome |
| Domain refuses connections (Octomind) | Check DNS before concluding "blocked". octomind.dev has **no `A` record at all** — the site is gone. The Internet Archive had it |
| TLS-fingerprint blocking (NSA) | The only one that genuinely needed a browser: `curl` 403s at any header combination. Fetch it in the page, then hand the blob to an `<a download>` and read it out of `~/Downloads` |

**What each source changed, in one line each.** Full detail is in the agent file named against it.

| Source | Outcome |
|---|---|
| **US Copyright Office, Part 2** | Read. The Office's own **eight conclusions** are now quoted verbatim in `accountability.md`, and the law-firm intermediary is retired. **But two quotations everyone attributes to the Office are not the Office's**: "copyright law protects only works of human creation" is the district court in *Thaler*, and "selection of a single output is not itself a creative act" is the Kernochan Center. Both are quoted *by* the Office. Its own line for the point is "prompts do not alone provide sufficient control" |
| **Anthropic system cards** | Read. Falsified the figures in print; see above. `failure-modes.md` now carries the real table, the verbatim definitions, and the full anti-hack prompt — which is a vendor's best attempt at instructing the behaviour away, and still leaves 35% of impossible tasks hacked. That is the sharpest evidence in the whole corpus for the Harness suite's *instructions are not enforcement* |
| **DORA 2025** | Read, and **the coefficient does not exist.** DORA publishes the 2025 effect sizes as charts with no printed values and says in footnote 20 that this is deliberate: "Last year, we spoke in terms of 'effects'. This year, however, we will speak in terms of comparisons." The book should say the 2025 edition reports direction and declines to report a coefficient, which is more interesting than the coefficient. **The 2024 figures are now primary-verified** in DORA's own words, with the phrasing corrected: a 7.2% *increase in instability*, not a reduction in stability |
| **Linux kernel `coding-assistants.rst`** | Fetched raw from `git.kernel.org`. **Settles the contested trailer: `Assisted-by: LLM [TOOL1] [TOOL2]`.** The `AGENT_NAME:MODEL_VERSION` form was a draft that did not survive merge, and the 2026 write-ups still quoting it are quoting the patch posting. **The book may print the kernel trailer**, and the three places that already do are consistent with it. The live file also carries a nine-step bug-fixing procedure that is an unusually good outside statement of *Make the agent prove it* |
| **Fedora policy** | Read from version control. Four corrections: it is **v1.0, 2025-10-24**; accountability is for "the entirety of these contributions"; the trailer placeholder `<name of code assistant>` is the *proposal's*, where the approved text gives `Assisted-by: generic LLM chatbot` and `Assisted-by: ChatGPTv5`; and the AI-as-arbiter clause covers judgements about **contributions** as well as about people. Fedora naming the product where the kernel's literal token is `LLM` sharpens the book's "there is no standard" point |
| **NSA MCP guidance** | Read. **It is NSA alone, not NSA/CISA, and it is dated May 2026, not June** — June is the upload date in the URL. It argues the Harness suite's own case from outside the industry: explicit trust boundaries between agent, plugin, model and user, OS-level sandboxing of every tool execution, and a conclusion worth quoting whole — MCP's "current security posture remains uneven and highly dependent on implementation discipline rather than protocol guarantees" |
| **Octomind** | Recovered from the Internet Archive; quotations now verbatim, including two the agent file never had. The Orchestration suite cited it nowhere and made the argument structurally instead; **that decision does not need revisiting** and the recovered text is filed for a later editor |
| **OpenAI Codex rate card** | Reached by a different route, and the gap **stands**: the per-plan included credit allowance is not published anywhere. It is now clear that is deliberate rather than a 403 — the docs say only "After you reach your included limits, available credits let you continue working". All three vendors express the allowance as an unquantified threshold, which is a finding rather than a gap |

**Two new do-not-cite entries, and both are the same species.** `18.2% / 12.8% / 12.6%` and DORA's
`0.199 [0.13, 0.26]` are each **arithmetic performed on a primary source by something that did not
read it**. The first is a row mean dressed as a published rate. The second is real, printed, DORA-
branded, sits in a chapter called Methodology — and is fitted to `simulated_data`, four lines below
the line that says so. Anything that searches a PDF rather than reading it will find it first.
**Both are in `evidence.md`'s consolidated list.** If this pass leaves one habit behind, it is
that a figure quoted to three significant figures from a document nobody opened is a tell rather
than a strength.

**Nothing else in the book needed changing.** The three places that print `Assisted-by:` are
consistent with the verified kernel and Fedora text, and no chapter had spent a DORA 2025
coefficient, a Copyright Office quotation, the Fedora wording, or Octomind.

## The Part III figure re-check

Board item `3884b4f3fc82` took the previous pass's finding as a hypothesis rather than a closed
incident, and went through **every figure Part III prints** — the part carrying more numbers than
the rest of the book combined — against the primary. **Twenty-six sources were opened.** Fourteen
arXiv PDFs were downloaded and text-extracted directly; the rest came from vendor pages, project
blogs, a git-hosted policy file, and one Internet Archive snapshot.

**The hypothesis held. Eleven defects were in print, and four of them are the same species as the
reward-hacking trio: real arithmetic, performed on a real table, by something that had not opened
it.** All eleven are fixed. Part III now stands at 5,509 words across four chapters, all four inside
the 800–1,500 budget, and `make check` reports no defects.

### The one habit worth taking from this

**When a number is precise, find out what it is a percentage *of*.** Every one of the four serious
defects was a correct numerator over the wrong denominator, or a rate computed from a table that
publishes counts. None of them was a typo, a bad citation, or an invented figure — the style guide's
"never invent a measurement" rule was obeyed throughout, and it is not the rule that would have
caught any of this. Two corollaries, both earned the hard way below:

1. **A source that quotes a third party is not the source.** This is the `Thaler`/Kernochan defect
   from the previous pass, and it recurred exactly once, in DORA.
2. **A percentage the source does not print is a derivation, and derivations need checking even when
   the arithmetic is trivial.** SPINE publishes counts; somebody divided; both endpoints came out
   wrong.

### The four of the species

| Where | What was printed | What the source says |
|---|---|---|
| *The failure modes worth naming*, the Confident Wrong Rewrite | "of the 511 public-set instances Claude Opus 4.1 failed on, 257 — 50.3% — … against 160 syntax errors and **51 tool-use errors**. **Half of everything that goes wrong**…" | SWE-Bench Pro Table 4 is **two-tier**. 511 is failing trajectories **that submitted a patch**, out of **689**; trajectories are not instances (GPT-4o's row sums to 789 against a 731-instance set). **Tool-Use is 121**, in the other tier — the 51 is the *Other* column. And 50.3% is of *submitted* failures: the paper's own prose says **35.9% of failures** |
| *The failure modes worth naming*, the Instant Concession | "the correct fact remained in the trace in **50% to 86%** of collapses" | SPINE's Table 5 publishes **counts, not rates**. Neither endpoint reproduces — the real span is roughly **62% to 93%** — and the `50` is a raw cell count read as a percentage |
| *What agents are reliably bad at*, SlopCodeBench | "the concentration metric moving from a mean of **0.39 to 0.68**" | Not a trajectory movement. **0.39 is the niche (<1k-star) human subgroup**, n=8; the paper's own sentence is "agent checkpoints average 0.68 … versus **0.31** … in the human panel" |
| *Where the time actually goes*, DORA | "**DORA's** separate 2026 **modelling exercise** splits the same way … two different methodologies, one shape" | DORA prints the 35–40% / 10% figures but **endnote 4 attributes them to Stanford**. DORA's own ROI calculator uses **12.5%**. It is DORA relaying a third party, so it is not a second methodology and it corroborates nothing |

### The other seven

- **Long-Horizon-Terminal-Bench conflated two thresholds.** 15.2% and 4.3% are at R≥0.95; "ten of
  the fifteen completed none" is at R≥1.0, which is the only threshold the paper calls *strict*. At
  R≥0.95 only **two** models score zero. Also, **v1 is superseded** — the live arXiv version has 17
  models and Grok 4.5 at 28.3% — so the chapter now names the version, per the staleness rule.
- **Apiiro was dated a year late.** "2026 telemetry over a seven-month window" is a post published
  **4 September 2025** whose data ends June 2025, and whose own window is **"six months"** and
  attaches to a *different* figure. Apiiro states **no window and no baseline** for the four
  class-shift figures, so "the same dataset, the same window" was an assertion the source never
  makes. The flat "60%" was The Register's compression of "more than 60%" — the tell that the figure
  travelled through a secondary.
- **UTBoost's 15.7% had the wrong base.** It is **92/584**, where 584 is the pool of leaderboard
  patches that had passed *on the 26 flagged instances*, not an increment against the benchmark.
- **GitClear's unit slipped.** "623 million changed **lines**" is "623 million analyzed
  **changes**". And the criticism the book made was the wrong one and weaker than the truth: the
  report performs **no AI attribution at all**, so there is no unpublished detection method — there
  is no denominator.
- **Veracode's quotation was spliced.** The verbatim sentence frames the span as **two years**, not
  "three editions", and the ellipsis sits inside it: "from approximately 55% to… approximately 55%".
- **METR's expert forecasts were transposed** — economics 39%, ML 38%, not the other way round.
- **The curl closer over-attributed.** "The variable that changed was the money, not the tooling"
  ignores that reporting moved **off HackerOne on 1 February and back on 1 March**, and Stenberg's
  April post dates the recovery from the second, in consecutive sentences. The bounty was also
  *announced* ended on 26 January and *stopped* on 31 January.

### What came back clean, which is most of it

Said plainly, because it is the useful half of the result:

- **The 802-developer mandate study is clean end to end** — the largest single block of figures in
  Part III. Every one of 2.09×, 1.46–1.72×, 1.99× at nine months, +86% management, the seniority
  ladder and its "statistically indistinguishable", +44% / +12%-not-significant, ~19%→~84% automated
  review, "about 20% longer", merge flat and revert declined, and the "not typical, immediate, or
  free" sentence, all verbatim at the printed precision.
- **METR's RCT and its February 2026 walk-back**, the Microsoft telemetry (+24.0%, CI +14.5% to
  +33.7%, disclosure sentence verbatim), the GitHub Copilot RCT, Borg et al., the Coherence Collapse
  trajectory figures, the agent-level context-rot study, SWE-Bench Pro's public/commercial gap, both
  contamination results, Terminal-Bench's 12.1 points, and every curl quotation including its
  italics.
- **The reward-hacking arc in *What agents are reliably bad at* survives**, and the previous pass's
  outstanding "someone should re-check the Anthropic PDF" gap is **closed** — with a split. The
  **12% sabotage is in the paper**, verbatim in the Figure 2 caption. The **50% alignment faking is
  not**: the paper renders it as a chart and the rate lives only in Anthropic's own writeup. Cite
  each to the right artefact.
- **The OpenAI 403 is no longer a gap.** The SWE-bench-retirement article reads in full from the
  Internet Archive, and 138 / 64 runs / 59.4% / the quoted clause / February 2026 all verify against
  OpenAI's own prose.

### Two traps left behind for whoever edits these chapters next

1. **Google's enterprise RCT: the abstract contradicts the hypothesis box, and the book follows the
   box.** The abstract says AI "significantly shortened" the time; that is **H1**, unadjusted. The
   **21% is the adjusted estimate and is not significant** (p = 0.086) — "Hypothesis 2: Partially
   Supported… lost its significance (p = NS)". Part III is right. **Do not "fix" it against the
   abstract.**
2. **Veracode's 86% means opposite things in adjacent editions** — XSS *failures* in 2025, crypto
   *passes* in 2026.

### One thing this pass did not do

**It did not revisit the reward-hacking table or the DORA 2025 material**, both of which the task
scoped out as already done by `57772ad900e3`. The DORA *2026* ROI report was in scope and is where
the fourth defect was, which is worth noting: "the DORA material is clean" was true of the edition
that had been checked and not of the one that had not.

## The editorial pass

Milestone 16 (`934259dc8038`) read all 38 chapters against `book/STYLE.md`, `book/TEMPLATE-play.md`
and `book/README.md`, and reconciled six authors into one voice. It added two files, renamed one,
and touched 31. **The book now stands at 39 files and 39,277 words.** Five things in it matter to
anyone working on the book next:

1. **The proportions hold, and framing is under budget rather than over.** Measured by
   `make check`: Part I 11%, Part II 57%, Part III 13%, Part IV 9%, appendices 9%, preface 1%.
   Against the four parts alone — which is what the 15 / 60 / 15 / 10 commitment is about — that is
   **12 / 63 / 15 / 9**. Nothing was cut for budget reasons; the instruction to cut framing if it had
   crept never fired.
2. **The book has a front door.** The root [`README.md`](../README.md) is the human entry point: a
   full contents with a line on each suite, the build commands, and the repository map.
   [`book/preface.md`](../book/preface.md) is a new chapter at row 0 under a **Front matter** part
   row, which is a shape the build already supported.
3. **Eleven cross-references were added and nine duplications removed**, itemised in the decisions
   below. The two that change how the book is read: Part I no longer quotes the METR abandonment in
   full (Part III owns it), and every appendix now has an inbound link, which `book/README.md`'s own
   diagram had promised since milestone 3 and nothing delivered.
4. **The failure-mode index is now complete.** It said "every name this book uses" and held 19 of 25.
   The six Part III names are in the table, and its heading is `## The index`.
5. **Three constraint documents were corrected to match six authors' actual practice**, rather than
   the other way round. See the decisions below on checklist voice, bold-on-first-use, and the
   volatile-facts call, which the style guide had left open for this pass.

What the pass deliberately did **not** do is listed in *Open questions* and in the notes below: the
suite-project rule, the three-plays-per-suite spread, and the Part II worked examples were all read
and left alone.

## The budget trim

Board item `fce3cee8fa34` closed the three section-budget overruns the reassessment pass
(`aed2433867e0`) deferred, in Part I and the Context suite. Nothing of substance was cut; the
material that went was a restated summary, a frame around a quotation, and one sentence of mechanics
covered twice. `make check` reports no defects and the book stands at 39,393 words.

| File | Section | Budget | Before | After |
|---|---|---|---|---|
| `before-git-before-scrum-before-this.md` | whole chapter | 800–1,500 | 1,567 | 1,487 |
| `scope-a-task-to-fit-the-window.md` | *The play* | 200–500 | 508 | 488 |
| `write-the-agent-file-that-actually-gets-read.md` | *Failure mode* | 80–200 | 205 | 190 |

Four things in it are worth knowing before editing any of these files:

1. **Count with the build's own counter, not by eye or by `wc`.** `scripts/build_book.py` exports
   `word_count(text)`, which is what `make check` reports per part: prose words with fenced blocks,
   headings, table rows and block quotes excluded. The reassessment's figures were 1–4% low against
   it, which at these margins is the difference between "48 over" and "67 over". For a per-section
   count, split on `##` and call `word_count` on each — a six-line script, not a file worth keeping.
2. **The deferred nit was real but misquoted, and the fix is checkable.** The clause shared by
   `context/index.md` and *Starve the context* was "Reduction never happens by accident", not the
   sentence the hand-off named. The opener now says "No window gets smaller on its own"; the play
   keeps its own thesis sentence, because a play's opening line should not be varied to protect an
   index entry. There are now **no shared four-grams** between `context/index.md` and any of its
   three plays once links are stripped, which is the check to re-run if a fourth play is added.
3. **Part I lost a sentence that Part III did not need it to make.** *Where that puts this* ended on
   "A shared name is not a small thing. It is the difference between a phenomenon a team can discuss
   and one everybody tolerates separately" — the same claim as *The same shape, over a longer
   timeline*'s "Shared words are what let a disagreement be a disagreement", two sections earlier
   and better put. The Vanishing Fix paragraph now ends on its forward link to Part III. **The
   "no agreed name" contract from milestone 7 is untouched**, and still reads as milestone 14 left
   it.
4. **`before-git-before-scrum-before-this.md` now has nine words of headroom.** It is the chapter
   closest to a ceiling in the book. `0bdccc346bd4` threads preparation-versus-execution into Part I
   and will most likely land here; if it adds a paragraph, it has to take one out, or put the
   material in *The four areas, re-weighted* (1,448) or *What this book assumes about you* (1,169),
   which have room.

## The overrun trim

Board item `bfc99c593aeb` did to Part II's other five suites what [*The budget
trim*](#the-budget-trim) did to Part I and the Context suite, using the same method and the same
rule: **cut restatement, not substance.** All eleven overruns `023ba519cdd0` found are gone, 267
words came out of Part II, and `make check` reports **no problems and no notes** — the first time
the book has been inside every budget it states.

| File | *The play* | Whole play |
|---|---|---|
| `verification-and-trust/decide-who-signs-off.md` | 534 → **497** | |
| `team/build-the-working-agreement.md` | 531 → **499** | |
| `context/scope-a-task-to-fit-the-window.md` | 533 → **495** | |
| `team/onboard-someone-into-all-this.md` | 530 → **496** | 1,227 → **1,193** |
| `orchestration/work-in-parallel-without-collisions.md` | 526 → **498** | |
| `verification-and-trust/make-the-agent-prove-it.md` | 524 → **494** | |
| `verification-and-trust/review-code-you-did-not-write.md` | 524 → **497** | |
| `economics/match-the-model-to-the-job.md` | 513 → **498** | |
| `team/collect-and-refine-as-a-team.md` | 511 → **493** | |
| `economics/understand-what-you-are-paying-for.md` | 504 → **499** | |
| `orchestration/make-the-control-flow-deterministic.md` | 502 → **499** | |

### What may be cut, and the one that fails silently

Two contracts bound *The play*, and they were checked against every one of the eleven:

1. **Every play states its exchange rate.** *What this book assumes about you* promises the reader
   in print that it does. Every "The exchange rate is…" sentence survives the trim untouched.
2. **Every *Checklist* item traces to something in *The play*.** This is the dangerous one,
   because nothing reports a break. One planned cut was abandoned over it — *Build the working
   agreement*'s "and the agreement says so in writing", which its second checklist item depends
   on — and a cheaper cut was found in the same step instead.

What actually went, by species, is the same list `fce3cee8fa34` produced:

- **A windup phrase that says a generalisation is coming.** "The reason this holds up is that it
  separates…" → "It holds up because it separates…"; "The transferable idea is that an agentic
  bill is…" → "An agentic bill is…". The paragraph is still the generalisation without being
  announced as one.
- **A frame around a statistic.** *Work in parallel*'s "The measured conflict rates are the
  argument for partitioning rather than trusting the merge" introduced 33,600 pull requests that
  introduce themselves. Same for *Make the agent prove it*'s "The disagreement about whether
  model-written tests are any good is where this becomes visible".
- **A sentence restating the bolded step it sits under.** *Stop on the tells*' "Continuing past
  these is buying more of what you already have"; *Own the tests yourself*'s "Test-first helps when
  a human owns the test, and backfires when the agent owns both sides of the loop", which restated
  the measured sentence before it.
- **A third source corroborating what two already said.** *Decide who signs off* quoted the Linux
  kernel, LLVM and Kubernetes on the same point; LLVM's went, and LLVM still appears two steps
  later carrying its own distinct test.
- **A detail the play's own Worked example spells out.** *Build the working agreement*'s
  personal-column list is printed verbatim in the one-page agreement below it.

**Nothing was cut that carries a claim, a figure, a quotation, a failure-mode name, a
cross-reference or an exchange rate.** Two cross-references were shortened rather than removed —
see below.

### Three judgement calls worth knowing

1. **`scope-a-task-to-fit-the-window.md` was the interesting one, and both its links stayed.** It
   was trimmed to 488 by `fce3cee8fa34` and taken back to 533 by `5e0f39858134`'s two-link fix.
   The item asked whether the material could be made shorter rather than whether it belonged: it
   could. The Part IV link lost its restated tail — "…is the same argument at the scale of the
   codebase" — and became "the difficulty is in the repository, not the task: see [*Refactoring a
   codebase for agents*]". **The Part III link to the Requirement It Can Still Quote is untouched**,
   because shortening it would have cost the phrase that marks it as a book-wide failure-mode name.
   The remaining 27 words came out of two steps elsewhere in the same section.
2. **Some plays are barely inside.** Nine of the eleven land at 493–499. There was not twenty words
   of restatement in every play, and cutting further would have meant cutting substance. **The
   tightness is real and is the reason the handoff shouts about it**, but it is a fact about the
   budget rather than a defect in the trim.
3. **Six paragraphs were reflowed, which makes the diff larger than the cuts.** Removing a clause
   from the middle of a wrapped paragraph leaves a ragged line; the paragraph was re-wrapped to
   100 columns rather than left with an orphan. Read the diff by paragraph, not by line.

### What this commits later edits to

**`make check` now fails on an overrun**, so the next writing task to add a sentence to a play will
meet it. The response is not to argue with the count — it is exact — but to find the restatement in
the section and take it out in the same edit. If there genuinely is none, that is the case for
raising the ceiling in `book/TEMPLATE-play.md`, which is a decision to ask about rather than to
make: the self-test will fail until the script agrees, which is the mechanism doing its job.

## The terminology pass

Board item `9dd4d6b84b80` closed the last contract the reassessment pass (`aed2433867e0`) deferred:
*What this book assumes about you* tells the reader in print that it does not assume they know
"what MCP stands for, what a skill is, or how a subagent differs from a workflow", and that "terms
are defined where they are first used and collected in the glossary". Three terms broke that.

Most of it had already closed itself while the item sat blocked, which is worth knowing before
re-reading the item's own description:

| Term | State when the item was filed | State when it was worked |
|---|---|---|
| *harness* | Undefined; the owning suite did not exist | Defined in italics at `harness/index.md` — "That loop is the *harness*" |
| *skill* | Used undefined in the Context suite | Defined in italics at *Package repeatable expertise*, and in the glossary |
| *card* | Used undefined, with no book-side referent at all | Glossary entry plus a card skeleton in *Copy-paste templates* |
| the glossary link | No `appendices/glossary.md` for Part I to point at | Written by milestone 15; Part I links it |

So the residue was one sentence: by the table-of-contents order, the Context suite reaches *skill*
and *card* before the Harness suite defines the first and before the unwritten cards play
(`703e507c86aa`) defines the second. Step 2 of *Write the agent file that actually gets read* now
glosses both in the clause that uses them — a skill is a folder of instructions loaded when a
request matches its description, a card is a short self-contained file on one subject loaded when
that subject comes up — and *Starve the context* links its "skill description" to the Harness play
so that a reader who opens it cold has somewhere to go.

Four things follow for anyone writing or editing prose here:

1. **Option 2 was declined.** The item offered narrowing Part I's promise to "defined in the suite
   that owns them". Option 1 cost one clause and twenty-one words, so the promise stands as written.
   Do not weaken it later on the grounds that a term slipped through; fix the term.
2. **The italicised first use belongs to the suite that owns the term, not to the first file that
   uses it.** `STYLE.md` gives italics to "the first use of a term" and, for failure modes, says a
   book-wide name has one first use rather than one per file. Those pull in opposite directions when
   a play needs a word the owning suite has not reached yet, and plays are self-contained by
   contract. The resolution: a use-site gets a plain-text gloss, the owning play coins the term in
   italics. *Skill* is now the worked precedent — glossed plainly in `context/`, italicised in
   `harness/package-repeatable-expertise.md`.
3. ~~**The cards play owes the italicised coinage of *card*.**~~ **Paid** by `703e507c86aa`:
   *card* is coined in italics in step 1 of [*Split the agent file into
   cards*](../book/part-2-plays/context/split-the-agent-file-into-cards.md), the Context gloss stays
   plain, and the play reached the same shape as the skeleton in *Copy-paste templates*, so the
   appendix did not have to change. `9dd4d6b84b80` is now closed on both halves.
4. **Twenty-one words in cost twenty-two words out.** *The play* in *Write the agent file the agent
   actually reads* was at 498 against a 500 ceiling. The gloss was paid for by trimming four places
   that said something twice — "the reason any of this works is that", a restated contrast after
   "separates X from Y", "no required sections" duplicating what the section demonstrates, and one
   doubled verb — leaving it at 499. Nothing of substance was cut, and the enforcement point about
   hooks survives as its own sentence.

## The cards play

Board item `703e507c86aa` added the Context suite's fourth play,
[*Split the agent file into cards*](../book/part-2-plays/context/split-the-agent-file-into-cards.md), at 1,166
words. It is one of the two chapters milestone 19 filed as owing the author's own material, and it
closes the last of `9dd4d6b84b80`'s three terms. **Part II is now nineteen plays**, and the four
places in the book that counted them have been updated rather than left to the next reader.

Five things in it constrain later work:

1. **One failure mode is registered: the Reassembled Agent file.** Cards that link to cards until a run
   loads the agent file they were split out of. It is deliberately *not* the Context Landfill — nothing
   is stale and nothing is flat — and the play says so in print. A second candidate was declined: a
   card nothing ever matches is the Unsummoned Skill with a different file extension, so the play
   uses that name plainly rather than coining a second one, on the precedent the Team suite set for
   the Agent File That Never Arrived. Part III's index has the new row and its count moved from nineteen
   to twenty.
2. **The worked example is this repository, which breaks one-project-per-suite on purpose.**
   `atlas` still carries the suite's other three plays. The exception is this plan's own answer to
   the appendix-templates question — the root `CLAUDE.md` and `cards/` are a checked-in,
   daily-exercised instance of the pattern — and it is the only worked example in the book whose
   subject a reader can open. Do not generalise it. A second self-referential example turns the book
   into a memoir.
3. **A change to `cards/` is now a change to the book.**
   [`book/examples/cards/reproduce.py`](../book/examples/cards/reproduce.py) copies the real
   `CLAUDE.md` and `cards/` into a temporary directory and asserts both captured blocks verbatim —
   the per-file line counts and the audit of links between cards. Editing a card, adding one, or
   adding a link between two will fail it. Re-run it and paste the new output into the play; that
   is the cost of a worked example that is not fictional, and it was accepted knowingly. The warning
   lives where the edit happens — [`cards/repo-layout.md`](../cards/repo-layout.md) ends with it,
   and writing that section was itself the first thing to trip the script.
4. **The Context opener was rewritten to make room, and is at 300 words — the ceiling**, where the
   other five openers sit at 296–300. Nothing of substance went: five sentences were tightened and
   one closing clause dropped. The no-shared-four-grams property between `context/index.md` and its
   plays was re-checked after the edit, links stripped, and still holds.
5. **The appendix's card skeleton did not have to change**, so milestone 15's conditional never
   fired. The play does refine the rule the appendix states: a card never *requires* another card,
   and a link a reader may follow is not a chain. The worked example turns on exactly that
   distinction — the audit finds four links between this repo's cards and all four are signposts,
   which is a judgement the command cannot make.

## The preparation thread

Board item `0bdccc346bd4` threaded preparation-versus-execution — the *rocket-launch mindset* from
the Cards post — into Part I. It is the third and last of the chapters milestone 19 filed as owing
the author's own material, which closes that audit: **both posts are now fully spent.**

It landed in [*What this book assumes about
you*](../book/part-1-argument/what-this-book-assumes-about-you.md), as a new `## Preparation and
execution` between *What this book will not do* and *How to read it*. The chapter went 1,169 → 1,444
against a 1,500 ceiling; Part I stays at 11% of the book, and the book at 40,866 words.

Five things in it constrain later work:

1. **The distinction is the load-bearing part; the metaphor is one clause.** The section names
   *preparation* and *execution* as two modes in italics, and spends the rocket on "closer to a
   launch than to a conversation, and nothing gets explained on the pad". No heading carries it. At
   book length a repeated metaphor becomes a bit, and `book/STYLE.md` bans bits; the two mode names
   are what later chapters should reach for.
2. **It is framing, not a play, and that was the decision rather than the default.** As an
   imperative — "prepare the project before you start" — it collapses into *Write the agent file the
   agent actually reads* or *Split the agent file into cards*, neither of which needs a rival. Stated as
   disposition it costs a screen and pays across the whole of Part II. **Do not later promote it to
   a twentieth play.**
3. **Part II is now described in print as mostly preparation-mode work** — "things to do on a quiet
   afternoon, against a problem you do not have yet". That is a soft contract on any future play: a
   play whose *Problem* only fires once something is already broken now sits against a claim Part I
   makes. Most existing plays already read this way; the sentence makes it deliberate.
4. **The placement was chosen over two nearer-looking ones.** *The four areas, re-weighted* argues
   disposition-versus-practice in almost these words and had 52 words of headroom; *Before Git,
   before Scrum, before this* opens on two developers who are exactly the two modes, and had nine.
   The opening vignette was deliberately **not** rewritten to name them: its whole point is that
   neither developer can say why their approach wins, and resolving that in chapter one would spend
   the book's argument before it has been made. The callback is available to a later editor and is
   not free.
5. **One sentence was cut to pay for it, and it was a duplicate.** *Where to start* opened "You are
   not being sold anything here, partly because there is nothing left to sell", which restates *What
   this book will not do*'s first line two sections earlier. The paragraph now starts on "The tools
   are installed".

## The Wave #2 check

Board item `5e0f39858134` read *Refactoring a codebase for agents* against *The unit of work* and
against the five things the handoff said Wave #2 must carry. **It carries all five, and the check
is a confirmation rather than a rewrite.** The constraint swap opens the chapter, the
six-files-in-three-trees cost is in *Features, not layers*, the four things feature-first buys are
there with the duplication one argued rather than asserted, invisible control flow has its own
section with a concrete list — decorators registering routes at import time, DI containers, ORM
lifecycle hooks, convention over a directory scan — and the nuance is a full paragraph: shared
infrastructure stays, and the distinction is a trustworthy black box against the magic kind. **Do
not re-file this as missing.**

Four things it found, three of them already closed and one fixed here:

1. **The attribution was already correct.** The post is absorbed, not cited: it appears nowhere in
   the prose of any chapter, and its URL sits in `appendices/further-reading.md` beside *Cards*.
   The in-line citation the item description expected in *Scope a task to fit the window* does not
   exist — `f94b88e05069` or the editorial pass had already removed it. **Re-derive a deferred item
   against the current tree before acting on its description**, which is now the second item to
   learn this the same way.
2. **The hedge is correctly calibrated and needed no change.** *The three waves* labels the part
   once, in *How to discount this part*, and the chapter separates the speculative commitment (a
   migration project justified on a forecast) from the part that pays anyway (do it on contact;
   what survives if the wave never arrives). Adding a second hedge inside the chapter would have
   made the least speculative material in Part IV read as the most.
3. **The cross-reference was one-way, and is now two.** Part IV linked to *Scope a task to fit the
   window*; the play did not link back. Step 2 of the play — "scope by capability, not by layer" —
   now names the layer-first layout as the reason the split is awkward and points at Part IV as the
   same argument at the scale of the codebase. The play went 1,074 → 1,119 against a 1,200 ceiling.
4. **Part III now carries the failure-mode half of the argument.** *The failure modes worth naming*
   had the Confident Wrong Rewrite's tell and response but not its architectural cause, while Part
   IV asserted that the cause "is in your architecture" with nothing on the other end of the claim.
   The entry gains one paragraph — behaviour attached invisibly does not appear in the file being
   edited, so the patch is locally correct and globally wrong — linking forward, with a response
   scoped to what a reader can do today (name the mechanism in the agent file). The chapter went 1,403 →
   1,488 against a 1,500 ceiling, so **that chapter now has twelve words of headroom**: anything
   further added to it has to displace something.

`make check` is clean and the book stands at 40,996 words. Part III is 13%, Part IV 8%; neither
share moved.

## The MCP citation check

Board item `f986730f7a1f` took the three dated claims in [*Wire in the outside
world*](../book/part-2-plays/harness/wire-in-the-outside-world.md) back to primary sources. **All
three survive. One was described wrongly, and the sentence is corrected in print.** The detail,
with quotes and source numbers, is in [`notes/research/mcp.md`](../notes/research/mcp.md); this is
what a later writer needs to know.

1. **`postmark-mcp` was never Postmark's package, and the play no longer implies it was.** The play
   said "whose maintainer added code silently copying every sent email to an address of his own".
   Postmark's own advisory of 25 September 2025 says the opposite of the reading that invites: *"We
   didn't develop, authorize, or have any involvement with the 'postmark-mcp' npm package"*, and to
   *The Register*, *"Postmark had absolutely nothing to do with this package"*. It was an
   impersonating npm package published by an unaffiliated account; the official server was
   ActiveCampaign's, on GitHub. The step now reads "a package wearing a mail vendor's name without
   being theirs". **The rug pull is still real** — Postmark's own words are *"built trust over 15
   versions, then added a backdoor in version 1.0.16"* — but it is measured in releases, not in
   months: the first version went up on 15 September 2025 and the backdoor on the 17th. The play no
   longer says the package "had been benign when people adopted it", because two days is not that.
2. **The Invariant Labs tool-poisoning demonstration holds exactly as written, and is two posts.**
   1 April 2025 (the mechanism, plus the cross-server "shadowing" case against a trusted email
   server) and 7 April 2025 (the WhatsApp case the *Failure mode* describes). April 2025, hidden
   instruction in one server's description, legitimate messaging server on the other end: all
   correct, no edit needed. The one thing the book does not yet use is that the WhatsApp demo was
   also a rug pull — *"a malicious server can change the tool description after the client has
   already approved it"* — which is step 5's argument applied to descriptions rather than code.
3. **The specification's three cited requirements re-read clean**, with one naming caution worth
   keeping: the section is headed **Scope Minimization**, not "scope inflation". The phrase appears
   inside it, in the risk list, so the play's sentence stands; a future edit that goes looking for a
   section called "scope inflation" will not find one. The untruncated-install-command requirement
   is quotable verbatim and unchanged.

Two things that cost time and need not cost it again:

- **Koi Security's write-up, the origin of every postmark-mcp download figure in circulation, is
  gone.** The company was acquired; `koi.security` redirects to `koi.ai`, which redirects the blog
  path to a Palo Alto Networks product page. `web.archive.org` is blocked from this harness. **A
  primary source can be retired by an acquisition**, which is a different failure from a source
  being wrong and is not fixed by searching harder. The vendor advisory survives and carries the
  load-bearing facts; the numbers do not survive and the book never used them.
- **The NSA guidance was already fetched** by `57772ad900e3` before this item ran, and the item
  description had not caught up. It stays cited nowhere, deliberately: every claim in the play now
  has a primary behind it, the tool-poisoning claim's primary is a demonstration rather than an
  advisory and is the stronger of the two for that sentence, and a play at its word ceiling does not
  spend thirty words on a second citation for a claim that already has one.

The third flagged claim — that a real observability server exposes write tools next to read ones —
is checked too, against Grafana's own `mcp-grafana`: `alerting_manage_silences`, `update_dashboard`
and friends ship in the same binary as the queries, and it offers `--disable-write`. The play's
fictional `metrics-mcp --read-only` is correct as illustration and **should not be rewritten into
Grafana's spelling**; the reason is in the agent file.

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
- ~~**Worked examples are illustrative-but-correct for the first draft**~~ (user decision).
  **Superseded by milestone 17**, which spent the dispensation. Commands and file contents were
  always required to be real and runnable; output is now *captured* wherever a command could
  produce it, marked with a `> Captured <Month Year>, <tool> <version>.` line, and backed by a
  committed project under `book/examples/`. Inventing a measurement remains banned outright.
- **Captured output is backed by a committed scratch project, not by a one-off run** (milestone
  17). A capture nobody can repeat is a screenshot: it goes stale silently, and the next author has
  no way to tell whether the prose still matches. So each fictional project the book uses —
  `atlas`, `meridian`, `tideline` — has a minimal tree and a `reproduce.py` under `book/examples/`
  that re-runs the book's commands and asserts the shapes the prose depends on. The cost is a few
  hundred lines of scratch code in the repository and an obligation on anyone editing a worked
  example to re-run one script. What it buys is that the book's evidence rules are enforceable by
  a machine rather than by an author's memory. `granary` and `lodestone` have no project, because
  neither prints output.
- **When a capture and the prose disagree, the prose changes** (milestone 17). Four numbers in
  *Review code you did not write* moved because the real `--stat` was 314 lines rather than 480,
  and one figure in *Understand what you are paying for* gained a decimal place because the
  arithmetic landed on a half-cent. The alternative — tuning the scratch project until it prints
  what was already written — produces a capture that is true and an example that was still
  invented, which is the failure the rule exists to prevent.
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
- **A research pass covering several subjects produces several agent files plus a hub**, not one file.
  Milestone 4 was commissioned as a single `notes/research/tooling.md` and delivered six files:
  the commissioned path became the hub holding the cross-cutting analysis and the full source
  list, with one self-contained agent file per subject beside it. This follows
  `cards/research-notes.md` ("several small agent files beat one enormous one") without losing the
  entry point the task named. Later research passes should do the same.
- **Every research note ends with a staleness assessment.** This subject dates in months, not
  years, and a writer picking up an agent file six weeks later needs to know which findings to hedge
  before they know anything else. `notes/research/tooling.md` carries a ranked table with a
  suggested hedge per row.
- **A research note states what a source could *not* establish, and names sources that must not be
  cited.** Milestone 5 found several confidently-circulating figures that did not survive checking —
  two low-code statistics attributed to Gartner and to vendor research, a scaffolding quote
  attributed to a named engineer with no traceable transcript, and a GitHub file that is a rewritten
  derivative of Anthropic's "Building effective agents" whose plausible figures are not Anthropic's.
  These are recorded in the agent files as **do not cite**, with the reason. An agent file that only lists what
  is true leaves the next agent to rediscover the same traps, and the derivative-text case is the
  exact failure `cards/research-notes.md` exists to prevent.
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
  *Decide who signs off*, and it is the reason that agent file quotes policy text verbatim rather than
  summarising it into something stronger.
- **Prices are printed as ratios, never as absolutes.** Milestone 6 flagged `token-economics.md` as
  the fastest-rotting material in the book — not "will need updating" but rotting, with two of the
  three subscription billing schemes it describes introduced in the six months before it was
  written. The durable findings are the tier ladder, the 4–8× output:input multiple, and the 0.1×
  cache-read multiplier. Absolute dollar figures appear only as a dated snapshot, labelled as one. A
  related trap: models of different generations tokenise differently, so per-token prices must never
  be compared across generations.
- **Where a source cuts both ways, the agent file carries both halves.** The one study measuring
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
- **A writing task that has to do its own research files an agent file like a research task would.**
  Milestone 7 needed sourced history for the pre-Git/pre-Scrum analogy, which no research pass
  covered. Rather than carrying twenty inline URLs in one chapter, it produced
  [`notes/research/convergence-history.md`](../notes/research/convergence-history.md) to the format
  in [`cards/research-notes.md`](../cards/research-notes.md) — findings, gaps, do-not-cite,
  numbered sources, staleness — and the chapter cites the agent file plus a handful of primary quotes.
  This keeps the verification pass (`3b61a6a1a684`) able to check Part I the same way it checks a
  play, and means the next author reaching for the same analogy does not re-run the searches.
- **The Standish CHAOS figures go on the book's do-not-cite list.** The 1994 16%/53%/31% success
  split and the 189% average cost overrun are the most-quoted numbers in the history of software
  process and do not survive checking; two peer-reviewed demolitions are cited in
  `convergence-history.md`. If the book touches them at all, it is as an example of a number the
  industry repeated for twenty years without opening the source — which is on-theme rather than a
  digression.
- **Part I cites primary documents inline and the agent file for the survey figures.** Quotations that
  carry the prose (Tichy on locking, Microsoft's own SourceSafe glossary, GitHub's two pull-request
  posts, Cockburn on "lightweight") are quoted in the chapter; every percentage traces to the agent file.
  The rule generalises for non-play chapters: quote the primary source where the sentence depends on
  its exact words, cite the agent file for everything numeric.
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
  version detects the crash are all in the play — re-hosted on the suite's own project. An agent file
  supplies evidence and an illustration; the illustration is the part a writer may replace.
- **A suite may claim a failure-mode name that `book/STYLE.md` coined as an example.** *Make the
  agent prove it* takes **the Green Suite That Tests Nothing**, which appears in `STYLE.md`'s naming
  section as an illustration of the convention rather than as a registered name. The Context suite
  set this precedent with the Context Landfill, and it is the right way round: a name good enough to
  teach the convention with is a name the book should use, and leaving it unclaimed guarantees a
  second author coins a worse synonym for the same phenomenon. `STYLE.md`'s third example, *the
  Confident Wrong Rewrite*, is still free.
- **Where a play's material is legal or regulatory, it is reported and not advised**, per the
  standing instruction attached to `notes/research/accountability.md`. *Decide who signs off* names
  ISO 26262-8 clause 11 and dates the absence of any regulator position to September 2026, says in
  print that none of it is legal advice, and quotes no document the agent file flagged as unextractable —
  no Copyright Office wording, no vendor indemnity clause text, no trailer syntax copied from a
  secondary source. The agent file's contested kernel trailer format is handled by naming the trailer's
  *shape* (`Assisted-by:`) and telling the reader to check the live policy, which is the hedge the
  staleness table asks for.
- **A play may carry a genuinely unresolved question as a step rather than resolving it.** *Review
  code you did not write* ends its numbered steps on whether the agent's plan in the pull-request
  body helps the reviewer or anchors them — a contest the primary source has with itself, which
  `evidence.md` names as load-bearing. The step is still actionable because the *action* does not
  depend on the answer: triage with the plan, do not read the diff through it. That shape is worth
  copying, because the alternative in a book that hedges honestly is a play whose steps evaporate.
- **All of the book's absolute prices live in one dated block, and the prose carries only
  multiples.** `token-economics.md` opens by calling itself the fastest-rotting material in the
  project and offers a five-point hedging strategy; milestone 12 applied it as written rather than
  case by case. The consequence worth knowing is what it cost: three arguments that would have been
  sharper with a number — the tier spread, the subscription-versus-metered comparison, and the
  per-developer-per-day aggregate — are made as shapes instead, and the aggregate is not made at
  all, because the two published figures for it disagree by a factor of two and a range that wide
  changes nothing the reader would do. The general rule is the one already in `STYLE.md`: a figure
  earns its place when the point collapses without it.
- **A play may host a vendor's published figures rather than the suite project's**, when the
  alternative is an invented measurement. *Understand what you are paying for* needed a session
  breakdown whose arithmetic the reader can check, and the only one that exists is the sample
  Anthropic prints in its own documentation. The play introduces `granary` as the situation, then
  says in print that the numbers are neither `granary`'s nor ours and why that specific sample was
  used. This does not weaken the one-project-per-suite rule — the project still carries the scenario
  — and it is strictly better than the two alternatives, which were to fabricate token counts or to
  drop the only checkable cost example in the book.
- **`book/STYLE.md`'s sample suite opener was deliberately not reused in the suite it describes.**
  Sample 1 in the style guide is an Economics opener, and it is good. A failure-mode *name* coined
  as a style-guide example gets claimed by the suite that owns it, per the Context and Verification
  precedent, because an unclaimed name guarantees a synonym. A *paragraph* is the opposite case: a
  reassessment pass already logged near-verbatim duplication between a chapter and another document
  as a prose defect, and duplicating the sample would make the style guide and the book quote each
  other. `economics/index.md` makes the same argument in different words, and the sample stays what
  it was written to be — an illustration of the register.
- **Three plays per suite is a floor, not a ceiling** — settled for the Context suite at least
  (user decision, milestone 19), which takes a fourth play on the cards pattern. This does not
  license adding plays quietly: `book/README.md` still asks suite authors to raise a fourth rather
  than insert one, and the raise here was made and answered. It does mean a suite author with a
  genuinely fourth-layer idea has a precedent to point at.
- **A play may be built on mechanism where no measurement exists, provided it does not imply one.**
  The Team suite is the only one in Part II whose central claims have no study behind them: nothing
  published measures whether a team with an explicit working agreement outperforms one without,
  whether a shared skill library shortens onboarding, or how often a well-described skill fails to
  fire. Three responses were available — invent a figure (banned), borrow an adjacent figure and let
  it do work it cannot do (the failure `evidence.md` was written to prevent), or write the plays as
  mechanisms and cite only the three findings that are real and dated. The suite takes the third.
  The consequence worth knowing is that its steps are justified by what they make checkable rather
  than by an effect size, and the one sentence that would have said so in print ("no study measures
  whether an explicit agreement helps") was cut for budget. **The gap is real and the book nowhere
  claims otherwise; Part III may want to say it out loud, where there is room.**
- **The principles in `idea.md` are written as mechanisms, never as values.** "Humble, transparent,
  experimental, share and document" would have made a poster and a worthless play. Each is spent as
  something with a tell: *humble* is the review trigger, the version line, and the rule that files
  are small enough that being wrong costs a two-line edit; *transparent* is the disclosure item in
  the agreement and asking for discarded runs first; *experimental* is the standing exception naming
  who may work against the agreement and what they owe in return; *share and document* is the
  promote-an-artefact step and the checkout-is-the-setup step. A reader can tell whether each one
  happened, which a value cannot offer.
- **A team-facing play describes the team's problem without addressing the team's manager.** The
  non-goal ("not a manager's guide") and the fragment's mandate-without-method pressure pull in
  opposite directions, and the resolution is that the reader is the person under the mandate. The
  suite opener and two Problem paragraphs state the pressure as the reader's situation; no sentence
  in the suite tells anyone how to lead, mandate, or measure a team. The one place it would have
  slipped — "write the agreement about changes rather than people" — is written as advice to whoever
  is holding the pen, which in this book is the reader.
- **The Team suite supplies the working-agreement skeleton, and the appendix extracts it rather than
  authoring one.** This mirrors the resolved `CLAUDE.md` half of the appendix-templates question:
  the template that ships is the one a play already exercises, because a skeleton written fresh in
  an appendix has never had to survive a worked example. The agreement in *Build the working
  agreement* carries a version, an amendment rule, a "last changed because" line, a personal column,
  and a standing exception — the five parts that make it cheap to change rather than ceremonial.
- **A failure mode may be named on recognition rather than on measurement, provided the chapter says
  so in the same paragraph.** *The Instant Concession* — an agent conceding a correct position under
  pushback — is the one name in the book with no coding-specific study behind it. The measured
  evidence is conversational-QA sycophancy, and `failure-modes.md` warns in bold that the coding
  claim is an extrapolation. Three options existed: skip it, and leave the most universally
  recognised agent behaviour in the book unnamed; name it and let the adjacent figures imply a
  measurement that does not exist, which is the failure `evidence.md` was written to prevent; or
  name it and state the gap in print. The entry does the third, in one sentence — "this name is
  given on recognition rather than on evidence, and that is stated here rather than hidden". The
  general rule is that the book may name what its reader recognises, and may never let a name borrow
  authority from a citation that is about something else.
- **Part III's failure-mode names get `##` headings in Title Case**, which is the book's one
  exception to the sentence-case heading rule, because the heading *is* a proper name. The trade was
  worth making: the HTML build's contents sidebar runs three levels deep, so every named failure
  mode in Part III is directly navigable, which is what a reader who came looking for one actually
  wants. Recorded here so the editorial pass reads it as a decision rather than as a slip.
- **A part may carry an index of the book's own vocabulary; a second copy of it is a liability.**
  *The failure modes worth naming* ends with all 25 names, one line of symptom each, linked to the
  chapter that describes them. It lives in Part III rather than the appendices because the reader
  who needs it is the one reading about what goes wrong, and because the registry in this file is
  already the authors' copy. The appendices should link to the Part III table rather than author a
  third version — the same reasoning that sends the appendix to the Team suite for the working
  agreement.
- **The Merged Hand is registered, and Part III's index leaves it out.** It is named only in
  `book/TEMPLATE-play.md`'s specimen play, which is deliberately outside the table of contents, so a
  row pointing at it would send a reader to a file that is not in their copy of the book. The
  registry keeps it, so nobody coins a synonym; the index does not, so nobody follows a dead link. A
  name can be reserved without being published.
- **Part III uses no suite project and has no worked example.** Every scenario in the part is a
  published study, named and dated, and the one-project-per-suite rule does not extend to it. This
  is not an exemption from the evidence rules; it is the opposite. A Part II play may illustrate
  with a plausible-but-invented `granary`, because the claim being illustrated is a mechanism. Part
  III's claims are claims about the world, so nothing in it is illustrative and every number has a
  source.
- **Part IV states its speculation contract once, in a chapter, rather than hedging every
  paragraph.** The part is the only forward-looking material in the book and had to be marked as
  such, and the two available shapes were a caveat per claim or a contract stated once and then
  relied on. *The three waves* takes the second: dated to September 2026, no study behind any of it,
  a named falsifier per chapter, and a closing section per chapter on the part worth doing anyway.
  The cost of the first shape is prose that reads as though it does not believe itself, which is a
  worse failure than over-claiming, because a reader cannot tell which hedges were meant.
- **A speculative chapter names the measurement that would settle it.** Both wave chapters end on
  an experiment a team could run in a week — a feature-first versus layer-first comparison on the
  same twenty tasks, and a defect-rate comparison between developer-authored and outsider-authored
  changes on one narrow surface — plus the signal to watch while nobody has run it. This is the
  honest form of a forecast in a book whose Part III spends four chapters on what the evidence
  cannot support, and it is cheap: two paragraphs each.
- **An appendix links to the thing it would otherwise duplicate.** Three times in this milestone the
  obvious appendix was a copy of something the book already has: the failure-mode names (Part III's
  index), the eighteen play checklists, and the working agreement (the Team suite's worked example).
  Each copy would have been a second artefact to keep in step with the first, and the registry in
  this file already records duplication of a chapter's prose as a defect. The glossary links, the
  templates appendix extracts a skeleton with the specifics removed, and the checklists appendix
  **compresses rather than concatenates**, by a stated rule — keep the items whose absence another
  person would notice, which is the same leaves-your-machine test the Team suite applies to the
  working agreement. That rule is what makes the page an artefact rather than a reprint.
- **The book's do-not-cite list is promoted into the book, as a section of further reading.** The
  consolidated list is the largest artefact in the research and lived only in `notes/research/`,
  where no reader goes. Five entries are named in the appendix — the SWE-bench dollar figures, the
  "200–400 lines" review rule, any Stack Overflow 2026 number, the Standish CHAOS figures, and both
  low-code statistics — with the agent files cited for the rest. A book that spends Part III on the
  quality of the evidence should tell the reader which numbers to stop repeating, and it costs
  fifteen lines.
- **A line consisting of a single cross-reference link may exceed 100 columns.** Seven lines in
  this milestone are one markdown link and nothing else, at 104–112 columns, because the longest
  play titles and the deepest suite paths exceed the budget together and neither half can be
  wrapped. The Team suite's fix — drop the anchor — does not apply, as these carry none.
  `book/TEMPLATE-play.md` has had three such lines since milestone 3 and nobody treated them as
  defects. Recorded here so the style lint (`6b0110f76388`) exempts them deliberately rather than
  being switched off by whoever hits them first, and so the editorial pass reads them as a decision.

- **The editorial pass settled the volatile-facts question** that `book/STYLE.md` had carried as
  provisional since milestone 3. The working line stands as written — a figure only where the point
  collapses without it, dated in the sentence, shape preferred to figure — with two clarifications
  the audit showed were needed and are now in `STYLE.md`. **A figure inherits a date only from its
  own paragraph**: the commonest defect found was a stamp sitting four paragraphs up, or in the
  other chapter that spends the same study, which the reader never connects. And **a version string
  is a date stamp** for a mechanic only one vendor implements — "Claude Code 2.x" does the job that
  "as of September 2026" does for a price, which is what the milestone-9 attribution decision was
  already doing without saying so. Fourteen undated figures were dated on that basis.
- **`book/STYLE.md`'s bold-on-first-use rule contradicted every author's practice, and the rule was
  wrong.** It read "bold on first use in a play; plain thereafter", which taken literally makes nine
  correct plain mentions in Part II, Part III and Part IV into defects. What six authors actually did
  — independently, and consistently — is bold **where the name is coined** and plain everywhere else
  in the book, because a book-wide proper name has one first use, not one per file. The rule now says
  that.
- **The play template's "imperative" checklist rule contradicted its own specimen, and the rule was
  wrong again.** Not one of the eighteen plays writes imperative checklist items; all eighteen write
  conditions that are true or false when you look, which is what the template's own specimen play
  does. `TEMPLATE-play.md` now asks for the condition form and says why: the reader is auditing
  finished work, not being walked through it. **Where a contract and six independent implementations
  disagree, the implementations are the evidence** — this is the second instance in the project after
  the past-tense worked-example correction, and it is the same lesson.
- **A play's filename must be its title, so `write-the-agent file-the-agent-reads.md` became
  `write-the-agent-file-that-actually-gets-read.md`.** `book/README.md` states the rule; the file had
  dropped a word since milestone 8 and `make check` cannot see it, because the build only compares
  the `#` heading against the table-of-contents title. Eleven files referenced the old path. Worth
  knowing that this class of drift is invisible to the build.
- **Duplication was resolved by deciding which chapter owns a piece of evidence, not by paraphrasing
  it twice.** Nine were found and nine were cut to a link: the METR abandonment quote (Part III
  owns it, Part I links), the verification tax's justification (Part III owns it, Part I and the
  glossary link), "the noise is rarely wrong" (the Context opener owns it), the skill-routing
  mechanism (the Harness play owns it), the `CLAUDE.local.md` precedence trap (the Context play owns
  it, two Team plays link), the give-one-agent-the-same-budget study (Orchestration owns it,
  Economics links), the mandate study's third spend in the Team suite, the SlopCodeBench figures
  spent twice inside Part III, the long-horizon 79% figure. **The general rule: a figure appears in
  one chapter, and the others name the finding and link.** A second copy is a second thing to keep
  true.
- **Three failure modes were being described at length in a chapter that did not name them**, which
  is the same defect as coining a synonym and harder to see. *Scope a task to fit the window* carried
  the Requirement It Can Still Quote unnamed, *What agents are reliably bad at* carried the Endless
  Polish and the Confident Wrong Rewrite unnamed. All three now use the name and link to the entry;
  the entries link back. **Naming is not only about avoiding two names for one thing — it is also
  about a chapter using the name the book already has.**
- **Three near-collisions between failure modes existed only in this file and are now in print.**
  The Unsummoned Skill versus the Agent File That Never Arrived, the Founding Document versus the Paper
  Fence, and the Immaculate Surface versus the Drifting Yes each get one sentence in the defining
  chapter saying what the other one is and why this is not it. The third was a genuine defect rather
  than a missing courtesy: the Immaculate Surface and the Drifting Yes published the same tell in
  different words, so a reader running the check could not tell which name they had found. The
  Immaculate Surface's tell was rewritten.
- **Part III's failure-mode index now holds all 25 names.** It opened on "Every name this book uses"
  and listed the nineteen coined in plays, omitting the six coined in its own chapter three
  paragraphs above the table. The six are in it, marked "This chapter". **The Merged Hand stays out**,
  per the milestone-14 decision, because it lives in `TEMPLATE-play.md` which is not in the book.
- **The register was even across the book and the corrections were small.** Zero exclamation marks,
  zero emoji, zero hype vocabulary, zero LLM cadence in 38 files, which is the strongest evidence
  that milestone 3's samples-not-adjectives approach worked. What did need fixing was placement
  rather than quantity: seven jokes inside a numbered step or a *Problem* paragraph's symptom
  description, one anthropomorphised mood ("a tired one"), one authorial "ours", one bare "the AI",
  one position reference, one piece of second-person scolding, and bold used for general emphasis in
  two appendices. Two chapters were an outlier in density and both were corrected by subtraction —
  *Choose your harness* and *Build the working agreement* each lost beats — and one, the Verification
  opener, was the only suite opener with no aside at all and gained one.
- **A play whose every section is a humour-banned zone will read drier than its neighbours, and that
  is the template working.** *Make the agent prove it* rates lowest in Part II on any wit measure. Its
  *Problem* must be straight, its *The play* allows none, its *Checklist* allows none, and
  `STYLE.md` requires a failure mode's description to be straight once the name has carried the joke.
  It was left alone. **Do not even out a chapter whose dryness is the contract rather than the
  author.**
- **Wrapping was fixed by a throwaway reflow script, and the script is the argument for
  `6b0110f76388`.** The editorial pass wrote the fourth independent 100-column tool in this project,
  hit two bugs a permanent one would not have (a markdown link is not whitespace-splittable, and
  `../path` starts with a character that looks like punctuation), and shipped two defects into the
  prose that an adversarial re-read caught. **A checker belongs in `scripts/build_book.py --check`
  where it is written once and reviewed once.** The exemption list it needs is now known: fenced
  blocks, table rows, and a line consisting of one markdown link.
- **An automated rewrap is not a safe editorial operation, and the guard is a word-stream diff.**
  Reflowing paragraphs introduced three real regressions that read fluently — a deleted "plus the
  same output" that broke a sum the chapter invites the reader to check, a deleted "it is" that
  inverted a sentence about vendor indemnities, and a verbless fragment left by a half-applied
  rewrite. None was visible in a rendered read; all three were found by comparing the word stream
  against `HEAD` token by token and by a second agent briefed to assume something was broken.
  **Any future mechanical pass over the prose should end the same way.**
- **The preface discloses that the book was written with agents**, in one paragraph. The book
  contains *Decide who signs off*, which argues that agent authorship should be disclosed, and a book
  making that argument while omitting its own disclosure is the Paper Fence at book scale. It is
  stated factually and briefly — several agents, separate chapters, a shared plan, a style guide,
  research notes, a human commissioning it — and is not the preface's theme.
- **The root `README.md` is the reader's front door and `book/README.md` stays the authoritative
  table of contents.** Two contents listings is exactly the duplication this project records as a
  defect, so the split is deliberate and narrow: the build reads `book/README.md` and nothing else,
  while the root file exists to orient a human arriving at the repository and carries what a table
  cannot — a line per suite, the build commands, and the repository map. **If a chapter is added,
  both change.** That cost is accepted; a repository whose landing page is an agent-instruction file
  is worse.
- **A figure that only exists as arithmetic on a primary source is not a figure** (`57772ad900e3`).
  Both numbers this pass added to the do-not-cite list were *derived* rather than invented: Part
  III's `18.2%` is the unweighted mean of a five-column system-card row, and DORA's `0.199` is a
  real printed coefficient fitted to simulated data in a methodology walkthrough. Neither was a
  hallucination and neither was sloppy secondary reporting in the usual sense — each was a
  plausible-looking calculation that survived because the primary was one fetch failure away. **So
  the rule the agent files now enforce is narrower than "cite the primary": if a figure is quoted to a
  precision the source does not publish, that precision is the tell.** A vendor that publishes five
  columns did not publish their average, and a report that publishes a chart did not publish a
  coefficient.
- **`WebFetch` failing is not evidence a document is unreadable** (`57772ad900e3`). Six of the seven
  sources three research passes recorded as blocked opened on the first or second alternative
  route — `curl` plus `pdftotext`, the project's git repository instead of its docs site,
  `developers.openai.com/<page>.md` instead of `openai.com`, the Internet Archive instead of a dead
  domain. Only one needed a browser. **An agent file may record that a source resisted retrieval, but it
  should name the method that failed rather than the document**, because the next agent has
  different methods. The five routes that worked are tabulated in *The source-verification pass*.
- **Four independent throwaway implementations is the threshold `cards/standing-defaults.md` was
  asking for** (`6b0110f76388`). That card says to add tooling "only when a real, repeated need
  appears", which is the right default and is also unfalsifiable until somebody counts. The count
  here was four: milestones 7 and 8, the reassessment pass and the editorial pass each wrote a
  100-column checker in `/tmp`, and none of them knew about the others. The card now carries the
  number as well as the principle, because "a real repeated need" and "I would find this
  convenient" are indistinguishable from inside one task.
- **The style checker is its own file, not a flag on `build_book.py`.** The editorial pass logged
  that a checker "belongs in `scripts/build_book.py --check`, where it is written once and
  reviewed once". The *written once* half is what mattered and it is honoured — one
  implementation, one review, and `make check` still the single command an author runs. The file
  is separate for two reasons the editorial pass could not have known: the checker's file set is
  not the build's (it reads `README.md`, `STYLE.md` and `TEMPLATE-play.md`, which the build
  excludes as instructions to authors), and `build_book.py` is a one-way transformation of the
  book into `build/` while this writes nothing at all. The shared parts are imported rather than
  copied, so "inside a fenced block" cannot come to mean two things.
- **A checker's exemptions are decisions with reasons attached, and they live in the code.** Every
  false positive is an invitation to switch the rule off, and the switching-off is done by
  whoever is in a hurry rather than by whoever understands the trade. So the mermaid-node
  exemption, the one-markdown-link line, the quoted-American-spelling case and the `book/STYLE.md`
  exemption are each a named constant with a comment saying which decision or which document put
  it there. The rule generalises to anything mechanical this project adds: **if a check has an
  exception, the exception is documentation, not configuration.**
- **A spelling preference is a note; an outright ban is a problem.** `-ize` endings are reported
  but do not fail `--strict`, because the book quotes American sources verbatim and the checker
  cannot always tell a quotation from a lapse — it masks double-quoted spans, which handles the
  cases in the book today and will not handle every future one. Exclamation marks, emoji and the
  hype list are problems, because `book/STYLE.md` calls them "not judgement calls". This keeps the
  two severities meaning what the build already made them mean: **a problem is a defect, a note
  wants a person to look.**
- **The checker has a self-test, and the fixture is the documentation.** A checker nobody dares
  change is worse than no checker, and the traps here are not obvious from reading the rules: a
  100-column line of em dashes that a byte-counting tool calls 106, a 128-column mermaid node that
  is correct, a `---` inside a ```` ```markdown ```` fence that is not frontmatter, a quoted
  exclamation mark that belongs to Anthropic. `--self-test` asserts all four, so the next person
  to add a rule finds out immediately if they have broken one. No test framework was added; the
  fixture is a string in the file.
- **`build_book.word_count` is the book's word count, and a deferred count is re-derived rather
  than trusted.** All three overruns handed to `fce3cee8fa34` were real, and all three numbers were
  wrong by 1–4% — enough, at margins of eight to sixty-seven words, to pick the wrong sentences to
  cut. One filename and one quoted clause in the same hand-off were also wrong. A measurement
  taken in one context and spent in another is a claim, not a figure: re-take it. The corollary
  for hand-offs is to name the tool that produced the number, which this one now does.
- **A budget overrun is cut where the book repeats itself, not where the prose is thinnest.** Each
  of the three trims came out of material that already existed elsewhere: a Part I paragraph
  restating a claim two sections earlier had made better, a why-it-works paragraph re-asking a
  question its own steps had answered, and a *Failure mode* re-teaching step 5 of its own *The
  play*. Sourced evidence, named failure modes, exchange rates, cross-references and the dry asides
  `book/STYLE.md` budgets at one per screen were all held. **Nothing in the three files lost a
  fact.**
- **A tie-back from a play to its suite opener is paraphrased, not quoted.** The opener previews
  the play; the play states its own thesis. When both used "Reduction never happens by accident"
  verbatim, one file apart, the echo read as an editing slip rather than as structure. The opener
  is the side that yields, because the play's opening line is load-bearing to a reader who opened
  the book there. Checkable: strip links, and an opener should share no four-gram with its plays.
- **A term is glossed plainly where it is first used and italicised where it is owned**
  (`9dd4d6b84b80`). `book/STYLE.md` gives italics to a term's first use and, for failure modes,
  insists a book-wide name has exactly one first use. Eighteen self-contained plays in six suites
  guarantee those two rules collide: a play needs a word before the suite that owns it arrives. The
  use-site gets a defining clause in plain text; the owning play coins the term in italics. This
  keeps Part I's promise ("terms are defined where they are first used") without giving any term two
  coinages, and it costs the use-site about twenty words. Do not resolve a future collision by
  narrowing the promise in Part I — that was the alternative on the table and it was declined.

- **The Context suite takes a fourth play** (`703e507c86aa`), on the user decision recorded under
  milestone 19 that three was a floor rather than a ceiling. `book/README.md` still asks a suite
  author to raise a fourth rather than add one quietly; that procedure produced this play and is not
  satisfied by it.
- **A worked example may be this repository, once.** *Split the agent file into cards* uses the root
  `CLAUDE.md` and `cards/` instead of `atlas`, against the one-project-per-suite rule in
  `book/TEMPLATE-play.md`. The trade was deliberate: the alternative was inventing a card set for a
  fictional billing service to illustrate a pattern that is checked in, running, and exercised by
  every agent on this board. It is the exception, not a precedent — a second one makes the book
  self-referential.
- **The self-containment rule is stated as *requires*, not as *links*.** A card never requires
  another card; "cards never link to cards" is the cheap way to guarantee that rather than the rule
  itself. This is what the appendix already said and what the play now argues, and it is why the
  audit in the worked example ends in a judgement rather than a count.

- **An idea that justifies the plays goes in Part I; an idea you execute goes in Part II**
  (`0bdccc346bd4`). Preparation-versus-execution had a plausible case for being a play and was
  written as framing instead, because as an imperative it duplicates an existing Context play and as
  a disposition it explains why nineteen of them are worth running before anything hurts. The test
  for the next candidate: write its imperative title, and if an existing play would have to be
  renamed to make room, it is framing.
- **The rocket-launch metaphor is spent once, in one clause, and is not a heading.** The names that
  travel are *preparation mode* and *execution mode*. A metaphor repeated across a 40,000-word book
  reads as a running gag, which is the register `book/STYLE.md` rules out.
  **Amended 2026-09-20: the clause now says "rocket launch" rather than "launch".** Dropping the
  word as well as the repetition left "closer to a launch than to a conversation", which reads as a
  product launch; "on the pad" was carrying the image alone and the author reported missing it. The
  decision is unchanged — once, in one clause, never a heading. This is what spending it once
  looks like, so do not trim the word back out.

- **A verification item that finds the work already done should say so and stop** (`5e0f39858134`).
  The Wave #2 check confirmed all five things the handoff demanded of the chapter and made no
  change to the argument; its edits were two links and nothing else. Rewriting prose that already
  passes, to demonstrate that an item did something, is how a book acquires a second voice in a
  chapter that had one.
- **Where one argument is made at two scales, both ends link.** *Scope a task to fit the window*
  has the small version (scope by capability, not by layer) and *Refactoring a codebase for agents*
  has the large one (the layout that makes that scoping natural). The forward link existed; the
  back link did not, and a reader who opened the book at the play had no route to the argument that
  explains why their split keeps being awkward. The same applies to Part III and Part IV, which had
  the failure mode at one end and its architectural cause at the other with no link between them.
- **Part IV's hedging belongs in *The three waves*, not in each chapter.** *How to discount this
  part* labels the whole part once, and feature-first is the least speculative material in it — a
  refactor a team can start on Monday. A second hedge inside the chapter was considered and
  declined: hedging the cheapest, most reversible recommendation hardest inverts the reader's sense
  of which parts are bets.
- **`.gitignore` covers Python bytecode as both a directory and a glob** (`f0669b48dbc0`).
  `__pycache__/` landed with the style checker in `37dfb14`, which also ran the `git rm --cached`;
  by the time this item opened, the only thing left was `*.pyc` for a stray bytecode file written
  outside a `__pycache__/` directory. Both rules are in place and `make lint` now regenerates
  `scripts/__pycache__/` without touching `git status`.
- **Nothing else generated is tracked, and it was checked rather than assumed.** The audit this
  item was asked to do came back empty: the only non-prose files in the index are the worked-example
  trees and the four files in `scripts/`, all of them source. The example `reproduce.py` scripts
  build their trees in temporary directories and `build_book.py` reaches `mmdc` through `npx`, which
  caches outside the repository — so no `node_modules/` or example build output can appear in the
  tree, and neither was pre-emptively ignored. **Speculative ignore rules were declined**: an entry
  for an artefact that cannot appear is a claim about the build that later stops being true
  silently. Add one when something actually shows up in `git status --ignored`.
- **A precise number is a claim about a denominator, and the denominator is the part that goes
  wrong** (`3884b4f3fc82`). Eleven defects were found across Part III's figures and not one was an
  invented measurement, a bad citation, or a transcription slip — the style guide's existing rules
  all held. Four were a correct numerator over the wrong base: a two-tier table read as flat, a
  human-repository subgroup read as a trajectory start, a share of a pre-selected pool read as a
  benchmark-wide increment, and a rate divided out of a table that publishes counts. **The check
  that finds them is to ask what the figure is a percentage *of* and confirm the source says so.**
  Merged into the standing guidance at the top of *Current state*.
- **A source quoting a third party is not the source, and it recurs** (`3884b4f3fc82`). The
  previous pass found this twice in the Copyright Office report; this pass found it once more, in
  DORA's 2026 ROI report, where a Stanford estimate carried in DORA's narrative had become "DORA's
  modelling exercise" and was doing corroboration work it cannot do. **Follow the endnote before
  attributing a figure to the document you found it in.**
- **"Verified" attaches to an edition, not to an organisation** (`3884b4f3fc82`). This item was
  told the DORA material was clean, which was true of the 2025 report `57772ad900e3` had read and
  false of the 2026 ROI report it had not. A clean-source note in this file should name the
  artefact and its version, not the publisher.
- **Where a figure is chart-only in the paper but printed in the vendor's own post, cite the
  post** (`3884b4f3fc82`). Two instances, both load-bearing: METR's `+2% to +39%` interval exists
  only as an unlabelled error bar in Figure 1 but verbatim in METR's February 2026 write-up, and
  Anthropic's 50% alignment-faking rate is a chart in the arXiv paper and a sentence in Anthropic's
  own post. The 12% sabotage figure *is* in the paper. **The two halves of one study can need two
  different citations, and the agent file should say which is which.**
- **A budget trim may cut a recently-rewritten section, but only for restatement, and it gets
  logged** (`3884b4f3fc82`). Paying for Part III's corrections needed ~90 words out of *What is
  genuinely contested*. The clause taken from `57772ad900e3`'s new reward-hacking section — "and
  noticing that the residue capability leaves behind is precisely the part that telling it to stop
  was supposed to cover" — restated "What it did not improve was how much the instruction helped
  once the work was impossible" two sentences earlier, which is the editorial pass's own criterion.
  **No claim, figure or quotation from that section was touched.**
- **`make lint` counts the word budgets, and reports them as notes rather than as problems**
  (`023ba519cdd0`). Chapter, suite opener, whole play and each of a play's five sections, against
  `STYLE.md` and `TEMPLATE-play.md`, with the build's own `word_count`. The count is exact and the
  threshold is a judgement, so a budget defect is a note: a draft is legitimately over for the
  length of a turn, and eleven pre-existing overruns would otherwise have handed every unrelated
  edit a red build. **Promoting over-budget to a problem once the book is inside every budget is a
  deliberate later decision, not a thing to do quietly.**
- **Budgets are hard-coded in the checker, and the self-test asserts they are still the book's**
  (`023ba519cdd0`). Both constraint documents state their budgets in prose; parsing English is a
  worse contract than a constant that names its source. `--self-test` checks each range still
  appears in the file it came from, so moving a number in `STYLE.md` fails the self-test rather
  than leaving the script enforcing last month's budget. **Change the document and the script in
  the same commit.**
- **Part IV, the appendices and the preface have no word budget, and the checker does not invent
  one** (`023ba519cdd0`). Nothing in `STYLE.md` states a length for them. If one is wanted, write
  it in `STYLE.md` first and then teach the script; a checker that legislates is a checker nobody
  believes.
- **Over-budget is a problem now, not a note** (`bfc99c593aeb`, with the user's decision on the
  record). The severity was a note for exactly as long as the book had overruns in it; once the
  eleven were trimmed, the argument for softness went with them. An overrun is now something an
  edit introduced rather than something it inherited, and the regression that filed the trim —
  `5e0f39858134` adding 45 words to a section already at its ceiling — is precisely what a note
  fails to stop. **The cost was weighed and accepted: nine plays sit 1–7 words under the 500-word
  ceiling, so a clarifying clause reddens the build.** That is the intended behaviour; the clause
  still goes in and something else comes out in the same edit.
- **A budget trim leaves headroom where it can, but does not manufacture it** (`bfc99c593aeb`).
  Every cut in the trim had to be restatement; there was not 20 words of restatement in every
  play, so several landed at 497–499 rather than comfortably clear. **Cutting further for the sake
  of a margin would have cost substance, which is the one thing the method forbids.** The tightness
  is a fact about the budget, not a defect in the trim, and it is recorded rather than hidden.
- **Two contracts bound what may leave *The play*, and one of them fails silently**
  (`bfc99c593aeb`). Every play must state its exchange rate — Part I promises the reader in print
  that it does — and every *Checklist* item has to trace to something in *The play*. The second is
  the dangerous one: cut the sentence an item traces to and nothing reports it. Both were checked
  against all eleven files, and one candidate cut was abandoned for it (*Build the working
  agreement*'s "the agreement says so in writing", which its second checklist item depends on).

- **The word *brief* named two different things, and now names neither** (terminology pass,
  2026-09-20). The book used it for the file an agent reads at the start of a session *and* for the
  cited research documents in `notes/research/`, which `book/STYLE.md`'s "one name per phenomenon
  across the whole book" forbids. A reader met the research sense in the preface and the file sense
  in Part I, five pages apart, with the glossary twenty-six chapters away. Both senses were
  renamed: the file is an **agent file**, the research documents are **research notes**. *Agent
  file* was chosen over *context file* (which collides with the Context suite and with *context
  window*) and over *project instructions* (which implies the file constrains the agent, the exact
  misreading the play exists to correct). ***Scaffolding* was considered and rejected**: this book
  has already coined **the Load-Bearing Scaffold** as a failure mode, and in most writing about
  agents "scaffolding" means the harness — two collisions with terms already in the glossary.
- **Two plays and one card changed filename in that pass.**
  `write-the-brief-the-agent-actually-reads.md` became
  `write-the-agent-file-that-actually-gets-read.md` — the literal rename would have said "agent"
  twice — `split-the-brief-into-cards.md` became `split-the-agent-file-into-cards.md`, and
  `cards/research-briefs.md` became `cards/research-notes.md`. **Any link written against the old
  paths is dead**, including in published releases, which are pinned to their own tag and so keep
  working against the version they shipped with.
- **The rename cost 48 re-wrapped lines and four budget trims, because *agent file* is a word
  longer than *brief*.** Three of those trims improved the sentence — most visibly *Verify that it
  arrived*, whose "the agent ignored the agent file" was a casualty of the rename and is now
  "ignored" versus "never loaded". Word budgets are the real constraint on renaming anything in
  this book: a two-word term for a one-word term costs a trim somewhere for every few uses.
- **The book's promise that "terms are defined where they are first used" was audited and had been
  broken exactly twice.** *Agent file* and *card* were both used bare in Part I with the glossary
  as the only definition. Both now carry a first-use gloss on the *verification tax* pattern. Every
  other glossary term either defines itself at first use, is named in the deliberate "we do not
  assume you know this" disclaimer, or matched the audit only as ordinary English — the verb *run*,
  the everyday *skill*. **The promise is kept; it was never enforced by anything, and still is not.**

- **The root `README.md` had been missing a play since the Context suite grew to four, and nothing
  reported it.** It listed eighteen plays and numbered the rest of the book around that gap, so
  every entry after *Write the agent file that actually gets read* was off by one. The fix is
  mechanical, but the lesson is that **the root README duplicates `book/README.md`'s table and
  nothing keeps them honest**: the authoritative table is machine-readable, so a dozen lines of
  Python can compare the two and report exactly this class of drift. That check is worth having
  before the next play is added, not after.
- **The worked example in *Split the agent file into cards* was printing stale counts** — 49 and
  197 against a repo that had reached 52 and 243 — and `book/examples/cards/reproduce.py` had been
  reporting the drift to anyone who ran it. Both captured blocks are re-taken. **A captured block
  measuring this repository goes stale every time the thing it measures is edited**, which for the
  cards is often; the verifier is the only reason it was noticed, and running it is cheap.

- **The root README's contents list is now checked against the table of contents, in
  `build_book.py` rather than in a new script** (`check_readme_contents`). It reports a chapter the
  list omits or invents, a title or an order that disagrees with the table, numbering that has
  slipped, and the "N plays in six suites" count. Two details worth keeping if it is ever rewritten.
  **Order and numbering are only reported once the two agree on what is in the book** — one missing
  entry renumbers everything after it, and thirty consequences of a single omission bury the
  omission, which is exactly how the original defect survived. And **the play-count sentence is
  matched by a regex that fails open**: rephrase the sentence and nothing is reported, because the
  check is for a number, not a house style.
- **The check caught a bug in itself on its first run.** It counted 23 plays, because
  `"Part III".startswith("Part II")` is true. It now matches on the part's own title. Worth
  remembering for any future check that identifies a part by prefix.
- **Editing `cards/building-the-book.md` to document the new check immediately invalidated the
  capture re-taken in the same session** — 243 lines became 247. This is the drift the previous
  entry describes, arriving within the hour, and `reproduce.py` caught it both times. **Anything
  that edits a card should run the verifier before finishing.**

- **Two working agreements were added to `CLAUDE.md`, and only one of them earned a place in the
  book.** *Ask when instructions conflict* and *keep this file and the cards current* are both now
  repository rules. **Keeping context files current was not added to the book, because the book
  already says it three times**: move 1 of *Write the agent file that actually gets read* (write
  from corrections), move 6 (prune on the trigger you add on), the Context Landfill's "an agent
  file that has only ever grown", and the cards play's checklist item about triggers nothing has
  matched. A fourth statement would have been a weaker duplicate.
- **Asking when instructions conflict was a real gap, and is now the second half of move 6.** The
  book had only ever treated contradictions by *prevention* — curate the file, and the checklist
  item "no two lines in the file contradict each other". Nothing told the reader what the agent
  should do on meeting one, so the Context Landfill's silent failure ("follows the current
  convention roughly half the time") stayed silent. **A line instructing the agent to stop and ask
  turns that into a reported failure**, which is the register the whole book is written in. Move 6
  was already the move about contradicting lines, so it needed no new move and the play still says
  "six moves, in order".
- **It was paid for out of a gloss that this session had made redundant.** Move 2 defined *card*
  inline; Part I now defines it at first use, so the parenthetical was a second definition of one
  term. *The play* sits at 500 words of its 500-word budget — **anything added to that play now has
  to be traded for something already in it.**

- **The book has a review server: `make review`** (`scripts/review_server.py`,
  `scripts/review_app.html`). It serves the chapters the table of contents names, several people
  can read at once over a WebSocket, and selecting a passage attaches a comment to it that appears
  in every open window. **The design constraint that shaped everything else is that an agent has to
  be able to act on the result**, and an agent edits markdown.
- **Annotations therefore anchor to `book/<path>:<line>` in the source, not to rendered HTML.**
  That is why the server renders the book itself with markdown-it — whose tokens carry a line map —
  rather than serving the far better page `make html` already produces: **pandoc discards the
  mapping**. Every annotation also stores the quoted passage, so the anchor survives the line
  moving. If this is ever rebuilt on pandoc, that is the property that will be lost first and
  noticed last.
- **The store is an append-only event log, `review/annotations.jsonl`.** Create, resolve, reopen
  and delete are all appends. Two reviewers cannot lose each other's work, a deletion is
  recoverable, and — the reason it is not SQLite — a log needs no schema and so no migration path,
  which `cards/standing-defaults.md` would otherwise require from the first table.
  `review/REVIEW.md` is regenerated from the log on every change and is **the file to hand an
  agent**: the open annotations as a task list, in reading order.
- **This is the repo's first dependency, and it is quarantined.** `requirements.txt` and `.venv/`
  exist for the review server alone; `make html`, `make pdf` and `make check` still run on a bare
  `python3`. The card's line — a markdown book you must pip-install before reading has failed at
  being a markdown book — still holds, because reading the book never touches the venv.
- **Documenting the server in `cards/building-the-book.md` rather than in a new card was a
  deliberate trade.** A sixth card would have added a row to the `wc -l` capture in *Split the
  agent file into cards* and falsified that play's "Five entries in that shape". The card is now
  274 lines, which the same play cites as the example of a card that has outgrown its neighbours —
  **so the play's own illustration is now more true than when it was written**, and its figures
  were updated with it.
- **That play's second captured block moved too**, because the new card section cites
  `standing-defaults.md`: four inter-card links became five, and the prose claiming all four are
  signposts now says five. The new link was checked against that claim rather than assumed to meet
  it. **Every edit to a card or to `CLAUDE.md` moves at least one figure in that play**; run
  `book/examples/cards/reproduce.py` before finishing.

## Two proposals from the author's reflection

Raised from `reflection.txt`, assessed against what the book already says rather than taken as
gaps. One needs inverting before it can go in; the other is a real hole. **Neither is written.**

### 1. Why context engineering — and why not as a triad

The reflection asks the Context suite to answer *why*, and offers cost, speed, quality. **The
suite opener does not currently answer it.** It gives the principle (signal over noise) and the
cost of entry ("none of the four needs a budget line"), and never says what the reader gets back.
That asymmetry is worth fixing: `book/TEMPLATE-play.md` requires every play to state what the
reader gives up, so the book is rigorous about costs and silent about returns.

**But the triad cannot go in as a benefits list, for two reasons that are both the book's own.**
`book/STYLE.md` bans "rule-of-three lists that exist for rhythm rather than because there are three
things". And *Starve the context* — the most carefully evidenced play in the suite — is a
counter-example to all three at once: a filtering tool reported 96.2 million tokens saved while an
independent trial measured cost *up* 7.6% and turns *up* 13.8%, with task quality tied. A suite
opener claiming context engineering buys cost, speed and quality would be contradicted four files
later by its own evidence.

**The version that survives is a scorecard: the three things people claim, and what this book's
evidence actually supports.** Quality is the strong one — the opener already says a fuller context
often produces a worse answer, and *Scope a task to fit the window* has the retention figures.
Cost is contested, and *Starve the context* is where the contest is. Speed is the weakest: the one
measurement in the book points the wrong way. That paragraph is in the book's register, it is
already sourced, and it makes the opener answer the question a sceptical reader arrives with.

**Constraint: the opener is at 300 words against a 150–300 budget.** It is full. This is a trade,
not an insertion — and the likeliest donor is the four-play summary, which repeats what the play
titles already say.

### 2. A fourth Team play: running the session

*Build the working agreement* says what to decide — usually six items — and where to write it, and
step 1 gives a real method for building the agenda (read the last twenty agent-authored pull
requests and list where they differ). **Step 3 is "Agree the items with team-visible
consequences", and the play is silent on how.** Getting a room from six disagreements to one signed
page in bounded time is exactly where this stalls, and nothing in the book helps.

A bounded, facilitated format is the most actionable thing the Team suite could add. Three
cautions, all from the repo's own rules:

- **Do not call it a Design Sprint.** The book names no vendor in a heading, and a five-day product
  sprint is the wrong shape for a half-day decision meeting. Adapt the structure — time-boxed,
  silent generation before discussion, a named decider so consensus theatre cannot set in — and
  credit the lineage in a clause.
- **The worked example may be representative.** `TEMPLATE-play.md` already exempts "a team
  practice" from the captured-output rule, so this play can be written without inventing a
  measurement. It must not print a plausible-looking result and lean on it.
- **It needs a named failure mode of its own**, against the registry in Part III. The obvious
  candidate is the session that produces agreement in the room and no change in behaviour.

**Arithmetic.** Part II is 23,425 words of 40,848, or 57%. A fourth Team play at the suite's own
length — its three plays run 1,129 to 1,197 words — puts Part II at about **58.6%**, inside the 60%
line that [*Open questions*](#open-questions) treats as the limit. The Team suite would go to four
plays, matching Context; the spread stays within one play, as that question requires. **The
procedure it also requires — raise a fourth play rather than adding it quietly — has been followed
by this entry.**

### What the fourth Team play turned out to be

**The proposal above was wrong about the gap, and the research found it before the writing did.**
It claimed *Build the working agreement* is silent on how a room agrees. The suite is not: *Collect
and refine as a team* is already a facilitated-session play — "run a recurring harvest", compare on
one task shape, ask for the discarded runs first and have the most senior person answer first, leave
with an artefact — and *Build the working agreement*'s first step already supplies the agenda from
twenty real pull requests. A play on running the session would have repeated two plays that exist.

**What is genuinely absent is the decision, not the discussion.** *Build the working agreement* says
"Agree the items with team-visible consequences" and never says who decides when nine engineers
across two time zones do not. Nothing in the suite names a decider, a time-box, or what becomes of a
split. Both neighbouring plays sit at 500 words of a 500-word budget, so neither could absorb it.
The play written is [*Settle what the team cannot
agree*](../book/part-2-plays/team/settle-what-the-team-cannot-agree.md): positions in writing before
anyone speaks, a clock, a named decider, a dated provisional call, and the losing argument recorded
next to it. It coins **the Nodded-Through Agreement** — every item agreed first time and nothing
different on Monday — whose tell is a page carrying no losing arguments at all.

**The suite reads Build, Settle, Collect, Onboard.** Decide, then what happens when you cannot,
then the material, then the transfer. The table of contents, the suite opener and the root README
were all put in that order; they disagreed at first, and `make check` caught it.

**The ripple was six files, and the checker found three of them.** The new README-contents check
added earlier the same day reported both the missing entry and "says 'nineteen plays', but the
table of contents has 20", and the structural check reported the ordering disagreement. The rest —
the suite opener, which needed six words trimmed to stay inside 300; the failure-mode registry; the
Team section of *Team checklists*, which had said "the three plays" — were found by reading the
contracts. **A play is not one file.**

**One leftover from the terminology rename was found on the way**: the registry still read *the
Reassembled Agent file*, lowercase, where the naming rule requires Title Case. Fixed in the registry
and at the coinage.

### What the Context opener says now

**Written as a scorecard, then corrected — the first version judged the suite by the wrong
experiment.** It said cost was contested and speed the weakest, citing *Starve the context*. Both
citations were a category error the author caught: **`rtk` is an output filter, not context
structure.** It compresses what a command prints, after the fact; an agent file and conditional
cards make the context small before anything runs. A tool that failed to save money by compressing
output says nothing about whether a four-hundred-line agent file cut to forty saves money, and
reading it as the suite's cost verdict judged structure by an experiment about compression.

**Cost is in fact the suite's most mechanical claim, and the book already had the arithmetic.**
*Understand what you are paying for* measures 94.3% of a session's tokens as the conversation
re-reading itself and cache reads as 51% of the bill, and concludes that the expensive thing is how
many times the conversation gets re-sent. So whatever loads every session is re-read on every turn,
and shrinking that layer is the one move that touches the largest line on the bill — which is what
*Split the agent file into cards* measures as roughly a tenth loading unconditionally, and what
*Write the agent file* means by "only conditional loading reduces anything". **It also explains why
`rtk` failed where structure does not**: the filter compresses output, 0.5% of tokens, leaves the
re-read prefix untouched, and buys extra turns, which multiplies the re-reads.

**The speed line was wrong the same way, twice.** The first version blamed `rtk` for it. The
second said nobody here had measured speed — also wrong, because it looked for a *measurement* and
the book states a *mechanism*. **Good context is fast because the agent does not have to go and
find out.** Part I has it: context assembled in the conversation means "five prompts in — here is
the actual task", and the part of the day you are sharpest goes on re-describing a codebase that
has not moved since Tuesday. *Split the agent file into cards* has the agent-side version — the
tell of a chained card set is "an agent that opens three files before it makes an edit".

**So cost and speed are the same arithmetic, and the opener now says so.** The bill and the clock
are both turns multiplied by what is in them: a smaller always-loaded layer shrinks the second
factor, and a context that answers the agent's questions up front shrinks the first. That is one
claim, which is why the scorecard is now two sentences rather than three. Quality stays the odd one
out, and stays last, because it fails quietly enough that nobody acts on it.

**The restored line.** Dropping the `rtk` caution from the opener — it belongs in the play, not in
the suite's summary — freed exactly enough for "No window gets smaller on its own" to come back,
which the entry above had flagged as the sentence to restore if the budget ever moved.

**It cost the opener its four play blurbs, which is the right trade.** The opener was at 300 words
of a 300-word budget, so the paragraph had to be bought. Two of the blurbs were paying for content
the scorecard now states better — the Starve blurb already carried both the quality and the cost
claims — and the rest said what the play titles say. All four are now a clause each. **The opener
is at exactly 300.**

**One line was lost worth noting**: "No window gets smaller on its own". If the budget ever moves,
that is the sentence to put back.

### Which is worth doing first

The second. It adds something the book does not contain, and the Team suite is where a reader with
a team problem arrives. The first is a reframing of material the book already holds, cheaper to
write and easy to get wrong: written carelessly it becomes the benefits list the style guide bans.

- **The suite's hardest problem is that bloat is survivable, and the book had never said so**
  (author's reflection). A capable model absorbs a bloated context and answers adequately. The
  answer passes review, so nothing prompts anyone to examine the context that produced it, and it
  goes on growing — while the cost is real and the noise is real. **This is the reason the Context
  suite is hard to sell**: its quality argument only bites when quality visibly fails, and usually
  it does not.
- **It is now *the Adequate Answer*, a second failure mode in *Starve the context*.** That play's
  *Problem* already said "Nothing failed. You paid more for it" — the concrete case was in the book
  and the generalisation was not. It pairs with the Flattering Dashboard, which is a genuinely
  different failure: there a tool's scoreboard flatters itself, here the work itself fails to
  complain. Both end at the same place, which is that the bill is the only signal left.
- **Everything in that play was at its ceiling, so the mode was paid for.** The whole-play budget
  is 600–1,200 and the play was at 1,200. The words came from tightening rather than from evidence:
  the Flattering Dashboard's closing aphorism, three loose phrases in the worked example, and the
  new mode itself, written twice. **None of the cited figures was touched** — they are the output
  of two source-verification passes and are the last thing that should pay for anything.
  **Registry rows are free**, because `word_count` skips lines beginning with `|`.
- **The Context opener now says quality "fails quietly" rather than "oddly"**, a one-word swap that
  costs nothing and points at the new mode.

- **`rtk` is the book's only named example of a filtering tool, and the book was letting v0.43.0
  evidence stand as a verdict on the product** (author's reflection). The play was already careful
  in the ways that matter — the figures are dated, versioned and qualified by reasoning effort, the
  prescription is a paired run rather than a prohibition, step 5 endorses the first-party reduction
  primitives, and the worked example *keeps* the filter on the one command where it won. What it
  never said is that **the benchmarks tested a version nobody has re-tested**, which
  `notes/research/token-filtering.md` had flagged in as many words: "a claim that rtk costs more
  should be dated and versioned or softened to the general lesson".
- **The play now says so in four words**, and *Further reading* carries the full caveat, since the
  appendices have no word budget: both benchmarks tested v0.43.0, the direction differed between
  two models, the effect largely vanished at high reasoning effort, and **a filtering tool that
  survives the same paired run is worth keeping — the objection is to the dashboard, not to the
  category**. That last sentence is the one to keep if this is ever edited: the Flattering
  Dashboard is a claim about self-measurement, not about filtering.
- **The play sits at 1,199 words of its 1,200 ceiling.** Anything further about `rtk` has to go in
  the appendix or replace something. The cited figures are the output of two source-verification
  passes and are not available to pay for it.

- **A staged adoption model is now named and discounted in *The three waves***, prompted by a
  five-stage maturity ladder the author circulated. The chapter already had the hook — "they are
  waves rather than stages because they overlap and because none of them finishes" — and never said
  what it was rejecting. The new paragraph argues from mechanism, as Part IV requires: **the levels
  conflate how far an agent is trusted with how many are running, and those are independent**, and
  the ladders are mostly written by the people selling the rungs, which is the Flattering Dashboard
  objection applied to a roadmap. It names its falsifier — teams that tried to skip a level and
  could not — and ties the bottleneck at every level back to the measured one, which is that
  somebody still has to read the output.
- **The specific document is deliberately not cited, and this is the interesting part.** It was
  read as a third-party artifact whose byline could not be verified from the page itself. The book
  has spent three source-verification passes removing claims that rested on somebody else's
  attribution, so asserting authorship on the strength of a page saying so would undo exactly that
  discipline. **The paragraph is therefore written about the genre rather than the instance**,
  which is also more durable: the argument survives the artifact going away. If the provenance is
  ever confirmed, a *Further reading* entry is the place for it, not the chapter.
- **`make lint` caught "unlocking" in the first draft** — banned hype vocabulary, and a word that
  arrived by absorbing the source's register while paraphrasing it. Worth knowing that summarising
  vendor material imports vendor vocabulary unless something checks.

- **The review server reads sections aloud**, one play button per heading, because reading prose
  by ear catches what the eye skips and the review server is the editing surface. It uses the Web
  Speech API and prefers `Microsoft Andrew Online (Natural)`. **This only sounds good in Edge**:
  Edge exposes its neural voices to `speechSynthesis` — 392 of them on the machine this was built
  on — and Chrome offers system voices instead. The choice degrades rather than disappearing, and
  the sidebar names the voice in use so it is obvious which you got.
- **Three things are deliberately not read aloud**: code blocks, tables and diagrams, which are not
  prose; and the `> Captured <month> <year>, <tool> <version>` provenance lines, which are a
  convention of `book/TEMPLATE-play.md` and would put tool versions in the middle of an example.
- **Two bugs worth remembering if this is rebuilt.** The button lives inside its heading so it can
  be positioned against it, which put a triangle at the start of every heading's `textContent` —
  **the first thing spoken in each section was a piece of punctuation** until the text was taken
  from a clone with the button removed. And speech is queued **per sentence, not per paragraph**:
  Chromium stops speaking partway through a long utterance, and a hundred-word paragraph is well
  past the limit.
- **Alignment had to be measured rather than eyeballed.** `book.css` gives `h2` a section rule and
  0.83em of padding above it and gives the chapter `h1` neither, so a single offset put the button
  on the rule for one and beside the text for the other. They have separate offsets.

- **Read aloud is in the HTML book too**, as `scripts/read-aloud.html`, injected by
  `--include-after-body` for `--format html` only — checked for all three formats, because
  `pandoc_command` is shared and a stray `<script>` in the typst input would be a bad way to find
  out. 212 buttons: 41 chapters and 171 sections.
- **The built book is not shaped like the review server, and the port had to notice.** The build
  shifts every chapter's headings down a level, so a chapter is an `h2` and a section an `h3`
  where the review server has `h1` and `h2`; pandoc wraps fenced code in `div.sourceCode` rather
  than leaving a bare `pre`; and there is a `#TOC` sidebar full of headings that must not get
  buttons. Section extent is taken from heading *level* rather than tag equality, so a chapter
  button stops at the next chapter and a section button at the next section.
- **The book gets no new chrome.** The review server names the voice in a sidebar line; the
  published book puts it in the button's `title` and draws no buttons at all when the browser has
  no usable voice. A reader who never hovers a heading cannot tell the feature is there, which is
  the right default for something nobody asked for.

- **The play button's vertical offset was wrong in both surfaces, for a reason worth writing
  down.** It was set in `em` — and `em` inside an absolutely positioned child resolves against
  *that child's* font-size, which here is `.68rem`. `top: 1.6em` was 18px where it read as 41px.
  **`lh` does not rescue it either**, nor does `line-height: inherit`: a unitless line-height
  inherited from the heading is re-resolved against the child's font-size too, so `1lh` came out
  as 14px rather than the heading's 30px. The offsets are plain `rem`, measured, with a comment
  saying to re-measure them if `book.css` changes a heading. Both surfaces now sit at 0px.
- **The review server sends `Cache-Control: no-store` for its page and stylesheet.** Editing
  `review_app.html` while the server runs and reloading gave back a copy from before the feature
  existed, with no sign anything was stale — which cost a diagnosis that started out looking like
  broken JavaScript. It is a local tool; correctness on reload beats a cached kilobyte.

- **The HTML book had 96 pixels of sideways scroll on a phone, and three separate causes.** The
  stylesheet already had a 62rem breakpoint, so the failure was not that nobody had thought about
  it — it was that the things which overflow have a width of their own and are invisible on a
  desktop. **Fenced code**: pandoc wraps highlighted code in a `div.sourceCode`, and the `pre`
  inside it already scrolls, so the missing `overflow-x` on the div shows up nowhere until the
  viewport is narrower than the code. **Tables**: the six-column cost table cannot be made narrow,
  so below 48rem a table becomes a block that scrolls inside itself. **The contents**: 22rem of
  navigation above the book on a 414px screen, now 13rem.
- **A fourth fault had nothing to do with width.** The read-aloud buttons are revealed by
  `:hover`, and a touch screen has none, so on a phone they were unreachable rather than merely
  ugly. They are shown dimmed under `@media (hover: none)` in both surfaces.
- **The table fix needed the specificity trap again.** `book.css`'s `body > :not(#TOC)` holds
  everything to the 40rem measure and its `:not()` carries an id's specificity, so a plain
  `table { max-width: 100% }` lost and the table stayed 640px wide on a 414px screen — briefly
  making the overflow worse rather than better. `body > table:not(#TOC)` wins. **That is three
  times this file's one selector has caught something out; it is the first thing to suspect when
  a rule that should obviously apply does not.**
- **Measured with iframes rather than by resizing the window**, which this browser does not
  translate into a page viewport. An iframe of a given width is a real viewport for media
  queries. One trap: an injected iframe is itself a `body > :not(#TOC)` in the host page and gets
  clamped to 40rem, which quietly turned a 1280px desktop check into another 680px one until it
  was given `max-width: none`.

## Open questions

Raise these rather than guessing. An agent that silently picks one answer commits the whole book
to it.

- **Play count per suite.** `PLAN.md` gives three working titles per suite. Is three a target or
  a floor? **Half-resolved** (milestone 19): three is a *floor*, and the Context suite takes a
  fourth play on the cards pattern. What remains open is the balance question — a suite with six
  plays next to one with two still unbalances Part II, and nothing yet caps the spread.
  `book/README.md` continues to ask suite authors to raise a fourth rather than add it quietly;
  that procedure worked here and should be used again rather than treated as satisfied. Milestone
  11 used it a second time — the Verification & Trust suite was flagged as having more strong
  worked examples than plays, raised the question, and answered it as three by routing the surplus
  to Part III rather than to a fourth slot. **Part II is now complete at five suites of three plays
  and one of four**, so the spread is settled in fact: eighteen plays, nothing wider than one play
  apart. **Answered** (milestone 16), from the word counts rather than by argument: the eighteen
  plays run 1,062 to 1,302 words, the six openers 293 to 302, and no suite is more than 5% off the
  Part II mean. That spread is tight enough that **a nineteenth play is affordable and a nineteenth
  suite is not** — one more play moves Part II by about a percentage point, while a seventh suite
  would take four files and push Part II past 60% on its own. The procedure stands as written: raise
  a fourth play rather than adding it quietly, and treat a new *suite* as a change to `PLAN.md`.
  **Closed** by `703e507c86aa`: the nineteenth play was written, Part II stands at 58% on the
  build's own counter, and the arithmetic above held. Context has four plays, the other five suites
  three.
- ~~**Worked examples — real or illustrative?**~~ **Resolved** (milestone 3), then **closed**
  (milestone 17). The first draft was illustrative-but-correct; the verification pass ran every
  command, replaced representative output with captured output, and committed the projects the
  captures came out of under [`book/examples/`](../book/examples/). The final rules are in
  [`book/TEMPLATE-play.md`](../book/TEMPLATE-play.md#worked-examples-what-real-means), and the
  first-draft dispensation is no longer in them.
- ~~**How much does the book date itself?**~~ **Resolved** (milestone 16). The provisional line in
  [`book/STYLE.md`](../book/STYLE.md#volatile-facts) is the final one, with two clarifications added
  there: a figure inherits a date only from its own paragraph, and a version string counts as a date
  stamp for a single-vendor mechanic. Fourteen undated figures were dated on that basis. The cost is
  recorded in the decisions log; what it bought is that *What this book assumes about you* keeps the
  promise it makes to the reader in print.
- ~~**Appendix templates.**~~ **Resolved** (milestone 19) for the `CLAUDE.md` starter: this
  repo's own setup is the worked example. The root `CLAUDE.md` is a real two-tier index and
  `cards/` holds five real self-contained cards, so the template is checked in, exercised daily by
  every agent on this board, and satisfies illustrative-but-correct without anything being
  invented. The new Context play (`703e507c86aa`) writes the pattern up; the appendix should
  extract the skeleton from it rather than invent a second one. The **working-agreement skeleton**
  is resolved the same way (milestone 13): *Build the working agreement* ships a complete one-page
  agreement in its Worked example, written to be copied, and the appendix extracts that rather than
  authoring a second. Both halves of this question are now closed, and milestone 15 shipped both
  in [`appendices/copy-paste-templates.md`](../book/appendices/copy-paste-templates.md) on exactly
  that basis, plus a third template — a review checklist for agent-authored changes, extracted the
  same way from the two Verification plays. The play the appendix was waiting on now exists
  (`703e507c86aa`) and reached the same shape, so the skeleton stands unedited and the appendix's
  pointer at this repository's own setup is now one of two — the play uses it as its worked example
  as well.
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
  research note should not squat names the suite authors have to live with. Whichever suite writes
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
  subagent inherits the written agent file but none of the conversation, so a convention established in
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
- ~~**`notes/research/` contains two deliberate leads that were not closed, both needing a human
  with a browser.**~~ **Both closed 19 September 2026 by `57772ad900e3`; see
  [*The source-verification pass*](#the-source-verification-pass).**
  1. ~~NSA/CISA MCP security guidance dated June 2026, HTTP 403 to automated fetch.~~ **Read.** It
     is **NSA alone and dated May 2026**; the "/CISA" and the month were both wrong, the latter
     because June is the upload date in the URL path. It is as good a Harness-suite citation as
     hoped, and the quotable extracts are now in `mcp.md`. It does genuinely need a browser — the
     403 is TLS-fingerprint based and survives any `curl` header combination.
  2. ~~Octomind's "Why we no longer use LangChain" (June 2024), site unreachable.~~ **Recovered
     from the Internet Archive**, and the quotations in `langchain-langgraph.md` are now verbatim,
     with two better ones the agent file never had. The reason it was never fetchable: **octomind.dev has
     no DNS `A` record** — the site is gone, not blocking. Everything milestone 5 said about *using*
     it still stands: the post is over two years old, its subject has had a major release since,
     there is no credible successor, and the book should not imply framework removal is a documented
     trend. The Orchestration suite's decision to cite it nowhere does not need revisiting.
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
  *Write the agent file that actually gets read* states the instructions-are-not-enforcement
  distinction in its closing paragraph (an agent file "does not constrain the agent, it competes for its
  attention"; blocking an action needs a hook) but leaves milestone 4's gotcha (a) **unnamed**,
  because the Harness suite owns permissions, hooks, and the `deny`-rule example and should name it
  where the reader can act on it. Similarly, *Scope a task to fit the window* uses milestone 6's
  phenomenon (b) — coverage retention 0.93–0.95 against strict success retention 0.375 — as the
  play's transferable idea, and leaves it unnamed for Part III. Note the agent file's own warning, which
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
- **The judgement calls were deferred rather than fixed**, on two board items. `fce3cee8fa34` held
  three marginal budget overruns — *Before Git, before Scrum, before this* at ~1,548 words against
  1,500, *Scope a task to fit the window*'s *The play* at ~559 against 500, and *Write the agent file
  the agent actually reads*'s *Failure mode* at ~219 against 200 — plus the verbatim clause shared
  by `context/index.md` and *Starve the context*, which is the tie-back-to-the-opener pattern
  working slightly too literally. **That item is now done; see [*The budget trim*](#the-budget-trim)
  below.** `9dd4d6b84b80` holds the terminology promise: *skill*, *card* and
  *harness* are used before being defined, against Part I's stated contract with the reader, and
  the suites that own those terms do not exist yet to fix it. **That one is now done as well; see
  [*The terminology pass*](#the-terminology-pass) below.** By the time it was worked, the suites had
  landed and defined two of the three and the glossary existed for Part I to link, so the residue
  was a single clause — which is the usual shape of a defect deferred past the tasks that caused it.
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
  `AGENTS.md`. The hub agent file did carve out an exception, in prose, four hundred lines further
  down; the headline instruction in the handoff won, as headline instructions do. The lesson
  generalises past this incident: **a rule stated as a category ("blog posts") will be applied to
  the category, not to the problem the rule was written for.** If a guardrail names a genre rather
  than a defect, it will over-fire, and the over-firing is invisible because nobody writes down
  what they declined to cite. The fix was to name the defect (third-party claims of fact) and to
  state the exception where the rule is read rather than where it was derived.
- **The book practised a pattern for six milestones without teaching it.** This repo runs on the
  cards pattern from the author's own post — a slim root `CLAUDE.md` index plus five
  self-contained `cards/`, and the Context suite never mentions it. The word "card" appears in
  *Write the agent file that actually gets read* exactly once, undefined, which is how board item
  `9dd4d6b84b80` came to exist. Worth noticing as a class of gap: conventions adopted in the
  *repo* during setup do not automatically become content in the *book*, and the setup milestone
  is the most likely place for good material to be silently spent on infrastructure instead. It
  also means the book's best worked examples may already be checked in — the resolved appendix
  question above turns on exactly that.

- **Milestone 9 named milestone 4's gotcha (a) as the Paper Fence**, which closes the note above
  about the Context suite leaving it unnamed. It covers both halves deliberately: the permission
  rule that matches a spelling rather than a capability, and the line of prose in an agent file that reads
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
  Board item `f986730f7a1f` tracks it. ~~The NSA/CISA MCP guidance is still unfetched~~ — **the NSA
  guidance has now been fetched and read (`57772ad900e3`), and `mcp.md` carries five quotable
  extracts from it.** It is still cited nowhere in the book, and the suite still leans on the MCP
  specification's own Security Best Practices document, which is primary and normative. **All three
  claims are now checked (`f986730f7a1f`); see [*The MCP citation
  check*](#the-mcp-citation-check).** ~~Whoever takes `f986730f7a1f` should decide whether to spend
  the NSA document while they are in there~~ — **decided: not spent, and the reasoning is in that
  section.** The original note, kept because it is the reasoning that was weighed:
  its trust-boundary and OS-sandbox recommendations restate *Wire in the outside world* and *Choose
  your harness* from outside the industry, and its conclusion — that MCP's security posture is
  "highly dependent on implementation discipline rather than protocol guarantees" — is a better
  citation than any of the incident reports that item exists to check.
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
  agent file-travels-conversation-does-not asymmetry, is stated as step 5 of that play and named nowhere.
  The handoff note asked whether it wanted the Agent File That Never Arrived's name; the answer is no,
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
- **The `single-agent-wins.md` agent file is left largely unspent on purpose.** The Orchestration suite
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
- **The Orchestration suite cites four of milestone 5's seven agent files and no adoption figures**, on
  the precedent the Harness suite set. No LangChain download counts, no n8n valuation, no tool
  table: two of the best-known parallel-agent tools in that table died or announced sunset inside a
  year, and the plays name tools only where a mechanic is that vendor's — `tools: Read, Glob, Grep`
  and the
  git-redirect block list, both attributed to Claude Code 2.x in the sentence that uses them.

- **Milestone 11 answered the play-count raise this suite was asked to make, and the answer is
  three.** The earlier note — "the Verification & Trust suite has a stronger worked example than it
  has plays for" — is now resolved. The fakeability ranking and the visible/held-out gap are one
  play's, spent in *Make the agent prove it*. The `sys.exit(0)` harness escape is **deliberately
  unspent and reserved for Part III**, which owns the same phenomenon at chapter length and has the
  room to carry its generalisation to alignment faking and sabotage. The mandate-study displacement
  example stays with Part III and Economics. No fourth play was wanted, which is a third data point
  against the open play-count question.
- **The curl bug-bounty arc is unspent and belongs to Part III.** The hub's map offered it to
  *Review code you did not write*, which declined it on reader fit, on the milestone-10 precedent: a
  play about reviewing agent pull requests at volume is not improved by four hundred words on
  inbound vulnerability reports. It is intact and is one of the strongest artefacts in milestone 6 —
  both halves verified at source, and its lesson is that the money rather than the AI was the slop
  vector. **Whoever writes Part III should take it, and must carry the April 2026 half**; the
  January 2026 figure alone is on the staleness table's hedge list.
- **`tideline`, a TypeScript service staging firmware rollouts to field devices**, is the fourth
  suite's project. It is deliberately typed, for the reason milestone 10 chose Ruby: this suite's
  central artefact is a ranking that puts the type checker at the top of the fakeability ladder, and
  the two evasions the plays show — a widened type and a deleted `typecheck` pipeline step — need a
  stack where a type checker exists to weaken. `atlas`, `kestrel`, `meridian` and `tideline` are
  taken; Economics and Team still need their own.
- **Two of the three plays overshoot the 500-word budget for *The play*, at ~524, ~568 and ~579.**
  The totals are inside the 600–1,200 play budget (1,152 / 1,232 / 1,179) and every other section is
  inside its own. The overrun is structural rather than sloppy: each step in this suite carries a
  cited figure and, in four cases, both halves of a contested claim, and the surviving alternatives
  were dropping a step or dropping the counter-evidence. Flagged for `fce3cee8fa34`, which already
  holds three marginal budget overruns, rather than fixed by deleting evidence. If the editorial
  pass wants these inside 500, the cheapest cut in each play is the closing why-it-works paragraph,
  not a step.
- **Four of milestone 6's contested claims are carried with both halves, inside *The play*.** The
  plan-in-the-pull-request question, whether model-written tests are usable, whether TDD helps
  agents, and whether "the human owns the diff" distributes responsibility or merely locates it. The
  Orchestration suite established that a play can cite evidence limiting its own subject in a
  numbered step; this suite does it four times, and the plays stay actionable because each action is
  written not to depend on which half wins.
- **The suite cites no adoption counts and no leaderboard scores**, on the Harness and Orchestration
  precedent, and it prints no figure from the hub's do-not-cite list. Specifically checked and not
  used: every SWE-bench per-instance dollar figure, the "200–400 lines in under 60 minutes" review
  rule, the "65% of PRs rubber-stamped" claim, METR's 19% without its qualifier, any Stack Overflow
  2026 figure, and Anthropic's Opus 4.5 reward-hacking rate. Where the ICSME 2024 comment-free
  figure was the citable substitute for a rubber-stamping number, the play uses the phenomenon
  rather than the figure.
- **Milestone 11 hit no 100-column overshoots and no `make check` problems**, having run a throwaway
  width checker from `/tmp` — the fifth independent writing of it — and the mermaid diagram through
  `npx @mermaid-js/mermaid-cli` before finishing. Board item `6b0110f76388` remains the right home
  for both checks, and the section word counter in `scripts/build_book.py` is still the thing that
  would have caught the budget overrun above at draft time rather than at review time.

- **Milestone 12 took none of milestone 6's four unnamed phenomena, and the play-count answer was
  three again.** The Economics suite names three new modes, all of which are economic symptoms
  rather than the evidence phenomena — a cold-cache resume, a cheap tier taking more turns, and a
  small request returning a large diff. Phenomena (a) to (d) in `evidence.md` are therefore **still
  entirely free for Part III**, as are the three in `failure-modes.md`. This is the fourth suite in
  a row to land on three plays, and no fourth was wanted: the material that might have made one —
  subscription-versus-API billing — is the fastest-rotting section of the fastest-rotting agent file, and
  it appears as a clause rather than a play for that reason.
- **The Economics suite cites no adoption counts, no leaderboard scores, and nothing from the
  consolidated do-not-cite list.** Specifically checked and not used: every SWE-bench per-instance
  dollar figure, the "up to 90% cost reduction" caching claim (the 81.9% in the worked example is
  derived from published token counts and dated list prices instead, as `token-economics.md`
  instructs), the 75–85% and 30–40% model-routing savings, Claude Max 20× at $200/month, the
  tokencalculator per-task figures, and the Vantage modelled session costs. The Requesty and
  Anthropic per-developer aggregates were available and were declined; see the decision above.
- **Two figures in the suite are load-bearing and hedged in the sentence that carries them.** The
  Tessl comparison (roughly 3× cheaper per token, roughly 3× more expensive per review, 156 turns
  against 42) is named as ten pull requests in August 2026 and paired with the thirtyfold
  run-to-run variance that makes ten thin — mechanism seriously, magnitude lightly, as the agent file
  asks. The five-of-six protocol-matched comparison is attributed to ten benchmarks in June 2026.
  Neither is printed anywhere else in the suite.
- **The AssetOpsBench latency result was deliberately not used.** `single-agent-wins.md` carries it
  with both halves — multi-agent roughly 40% slower in wall clock *and* cheaper in tokens — and the
  rule is that quoting one half is dishonest. Carrying both takes three sentences to make a latency
  point in a suite about money, and *Know when not to use an agent* already has the token
  multipliers and the matched-protocol comparison doing that work. It is intact for Part III, which
  can afford the sentences. The same applies to the mini-SWE-agent and Agentless material, neither
  of which the suite touches.
- **Milestone 12 hit no 100-column overshoots and no `make check` problems**, having run a throwaway
  width checker from `/tmp` — the sixth independent writing of it — plus the section word counter
  inside `scripts/build_book.py`, and rendered the mermaid diagram through
  `npx @mermaid-js/mermaid-cli` before finishing. The word counter caught three budget overruns at
  draft time and they were fixed rather than flagged, which is the first task in the project where
  that happened; two *The play* sections still land marginally over at ~502 and ~509 against 500,
  and the cheapest remaining cut in each is the closing why-it-works paragraph. Board item
  `6b0110f76388` is still the right home for both checks, and its value goes up rather than down as
  the book fills.

- **Milestone 13 spent the team-adoption fragment in full and closes Part II.** All three things the
  archive pass extracted from it landed where that entry predicted: *mandate without method* is the
  suite opener's framing and appears in two Problem paragraphs as the reader's situation; *a working
  agreement has an expiry date* is step 5 of *Build the working agreement* (a trigger rather than a
  review date, plus a version line and a standing experiment exception) and is the phenomenon **the
  Founding Document** names; and the fragment's step two — an honest comparison of what worked and
  what did not — is the spine of *Collect and refine as a team*, as predicted. The fourth item,
  *adoption by decree reads as surveillance*, was **used and deliberately not named**: it is the
  leaves-your-machine sort in step 2, the describes-changes-not-people argument in the why-it-works
  paragraph, and the personal column of the starter agreement. A name was available and declined for
  the milestone-10 reason — the phenomenon has no tell a reader could act on beyond "write it down",
  and the write-it-down is already the step. A name with no tell is decoration.
- **The Team suite is the only suite in Part II with no evidence base of its own**, and the plays
  say nothing that implies otherwise. Three figures are printed in the whole suite: DORA 2025's
  amplifier sentence (quoted, dated by edition), DORA 2025's trust split (roughly a quarter high,
  roughly thirty per cent little or none), and the mandate study's review-displacement pair (89% →
  68% coverage, each remaining reviewer's load doubled, 802 developers to April 2026). Nothing else
  numeric appears. Specifically checked and not used: every item on the consolidated do-not-cite
  list, the Faros and LinearB vendor figures, the Stanford 100k-developer talk figures, the GitClear
  2026 commit share, any Stack Overflow 2026 number, the `AGENTS.md` 60k-repositories count, the ~45
  skill clients, and the mandate study's 2.09× throughput headline — which belongs to Part III and
  Economics and which this suite does not need, since its argument is about the review half.
- **The mandate study is now spent in three places and Part III should assume it is known.**
  Economics carries it as the closing argument of *Know when not to use an agent*; the Team suite
  carries one clause of it, the review-coverage pair only, inside a numbered step. Part III still
  owns it at length and still has the throughput figures, the heterogeneity breakdown, and the
  authors' own "not typical, immediate, or free" caveat unspent. **Whoever writes Part III should
  carry that caveat**, which neither of the two short uses had room for.
- **`lodestone` is the sixth and last suite project**, a claims-processing platform of C# services
  behind a TypeScript front end, nine engineers across two time zones. The mixed stack earns its
  place twice: a skill written by one half of the team is described in that half's vocabulary, and
  the first-task-with-a-cheap-check rule holds on the tested half of the codebase and fails on the
  other, which is the imperfect result in *Onboard someone into all this*. Every suite now has a
  project and none of them share one.
- **Milestone 4's gotcha (c) is spent without a new name.** The `CLAUDE.local.md`-silently-disables-
  `AGENTS.md` precedence trap is a team problem — one person's private file switches off the file
  the team maintains — and it appears twice in this suite: as a verification step and a fenced
  agreement clause in *Build the working agreement* and *Onboard someone into all this*, and as the
  imperfect beat of the latter's worked example. It is named as **the Agent File That Never Arrived**,
  plain and linked, because the Context suite's definition already covers it exactly ("instructions
  written, committed, and never loaded; nothing errors, and the usual check reports the same thing
  whether they loaded or not"). All three of milestone 4's gotchas are now spent: (a) is the Paper
  Fence, (b) is the Flattering Dashboard, (c) is the Agent File That Never Arrived.
- **Vendor mechanics in this suite are named and version-stamped in the sentence that uses them**,
  per the milestone-9 rule. Claude Code 2.x and the precedence behaviour are attributed where the
  reader is told a fact; inside the fictional agreement the same rule is written the way a team
  would write it, with the version in the clause. `.claude/skills/` is named as a path in the
  agreement rather than asserted as a cross-tool standard.
- **Milestone 13 hit no 100-column overshoots and no `make check` problems**, having run a throwaway
  width checker from `/tmp` — the seventh independent writing of it — plus the section word counter
  inside `scripts/build_book.py`, and rendered the mermaid diagram through
  `npx @mermaid-js/mermaid-cli`. The word counter caught a 650-word *The play* at draft time and
  three rounds of trimming brought it to 524; the three *The play* sections land at 524 / 512 / 510
  against 500, in the same marginal band as the Verification (524–579) and Economics (502–509)
  suites, and are flagged for `fce3cee8fa34` rather than fixed by deleting a step. **Seven
  independent writings of the same width checker is the strongest case yet for `6b0110f76388`**,
  and with Part II complete its value is now entirely to the editorial pass.
- **Two long lines in this suite were caused by a deep link, not by prose.** A
  `[*title*](../context/write-the-agent-file-that-actually-gets-read.md#failure-mode)` inside an indented list
  item cannot be wrapped and overshoots by ten columns. Both were resolved by dropping the anchor
  to a file-level link, which `book/README.md` already prefers. Worth knowing before the checker
  lands: the fix for an over-long cross-reference is usually to shorten the link, not the sentence.

- **Milestone 14 spent every unnamed phenomenon the research passes left behind.** `evidence.md`'s
  four cross-cutting phenomena are now (a) the Vanishing Fix, (b) the Requirement It Can Still
  Quote, (c) the Green Suite That Tests Nothing (Verification, milestone 11), and (d) the Immaculate
  Surface. `failure-modes.md`'s seven map on to those plus the Endless Polish (#3), the Instant
  Concession (#4), and #7, which is not a name — reviewing overtaking writing is the whole of *Where
  the time actually goes* and does not want one. **Nothing in the research notes is still waiting
  for a name**, and the editorial pass can treat the registry as closed unless Part IV coins one.
- **Part I's outstanding rewrite is done and the loop is closed in both directions.** *Before Git,
  before Scrum, before this* now reads "It has no agreed name… This book calls it the Vanishing
  Fix", links forward to *The failure modes worth naming*, and gains two sentences on why a shared
  name matters; Part III's entry links back to it. This was flagged by milestones 7 and 8 as
  outstanding for the editorial pass. It is no longer outstanding.
- **Part III prints no figure from the consolidated do-not-cite list.** Specifically checked and not
  used: every SWE-bench per-instance dollar figure, Peng et al.'s 55.8%, OpenAI's narrow/wide/misc
  sub-split (the 138/64/59.4% top line is used and attributed to OpenAI), the Replit record count,
  DORA 2025's numeric coefficients, any Stack Overflow 2026 figure, the "200–400 lines" review rule,
  the 11.4-hours-per-week figure, "2.74× vulnerabilities", and every current leaderboard score. The
  two leaderboard numbers that do appear — UTBoost's 53.6% tie and Terminal-Bench's 12.1-point swing
  — are used as evidence *about benchmark instability*, with the version and the correction named,
  which is what the staleness table asks for.
- **One citation in Part III rests on a source that resisted automated fetch and should be checked
  before publication.** OpenAI's February 2026 retirement of SWE-bench Verified (138 problems, 64
  runs, 59.4% with material issues) is corroborated across two independent secondary reports;
  openai.com returns HTTP 403 to automated fetching, so the primary was never read. *What is
  genuinely contested* attributes it to OpenAI and carries no sub-split. This joins the seven leads
  already on board item `57772ad900e3`.
- **The Apiiro figures are used once, in Part III, with the hedge the agent file prescribes.** The −76% /
  −60% / +322% / +153% pair drives *the Immaculate Surface*, attributed as one vendor's telemetry,
  with the broad definition of "security issue" stated and the magnitudes explicitly held lightly
  against the shape. No other chapter in the book cites Apiiro. The same applies to Veracode, whose
  flatness across three editions is the claim rather than the level, and to GitClear, which appears
  once with its undisclosed detection method named.
- **Three arguments that would have been sharper with a worked example are made without one**, and
  the reason is worth recording: Part III has no *Worked example* heading and no suite project, so
  the mandate study, the METR trial and the curl arc are carried as narrative inside a `##` section.
  Each is a real, dated, sourced account rather than an illustration, which is the correct trade for
  this part and would be the wrong one for a play.
- **The mandate study is now spent in three places and is no longer available at length.** Economics
  has the headline (2.09×, 89%→68%, +22% cycle time, merge and revert flat), Team has the
  review-coverage clause, and Part III has the interior — the composition-versus-individual gap, the
  heterogeneity breakdown, and the authors' caveat. The unspent remainder is thin. Part IV should
  not build on it.
- **Milestone 14 hit no 100-column overshoots after a fix pass and no `make check` problems.** Five
  long lines were caught by a throwaway width checker run from `/tmp` — the eighth independent
  writing of it — and four of them were the same cause the Team suite recorded: a cross-reference
  inside a sentence, where the fix is to reflow around the link rather than shorten the prose. All
  four chapters landed inside the 800–1,500 Part III budget on the build's own section counter
  (1,233 / 1,346 / 1,213 / 1,435), which is the first writing task where nothing needed flagging to
  `fce3cee8fa34`. **Board item `6b0110f76388` has now been justified eight times and every writing
  task in the project is finished except Part IV**; its remaining value is to the editorial pass,
  and it should land before that pass rather than after it.
- **`make check` caught one real defect that no human reviewer would have.** *The failure modes
  worth naming* linked to `book/STYLE.md` for the naming convention, which is not in the table of
  contents and so is not in the book; the build reported it as a problem and the sentence now states
  the convention instead of linking to it. Worth knowing as a class: **book chapters may not link to
  `book/`'s own constraint documents.** Those are authors' files, and a reader of the PDF cannot
  open them. Cite `notes/research/` freely — the build rewrites those with `--repo-url` — but never
  `STYLE.md`, `TEMPLATE-play.md` or `README.md`.

- **Milestone 15 closes the writing programme, and the proportions can finally be read.** With
  everything written the build reports Part I at 11%, Part II at 58%, Part III at 13%, Part IV at
  9%, and the appendices at 9% of 38,799 words. Against the 15 / 60 / 15 / 10 target that is Part II
  landing almost exactly where it was planned and the other three parts each running a couple of
  points light — because the appendices are a fifth column the proportions never accounted for.
  Whether that is a problem is the editorial pass's call: the intent behind the numbers was that the
  plays dominate, and they do.
- **Part IV prints almost no figures, which is deliberate and is the opposite of Part III's
  posture.** Nothing in the part is a claim about the world that a number could support: both
  chapters argue from mechanism and say so. The two places a figure would have been available were
  the mandate study — which milestone 14 recorded as spent in three places with a thin remainder,
  and which Part IV accordingly does not build on — and the low-code precedent, where the only
  figures in circulation are on the do-not-cite list.
- **The low-code do-not-cite entries are used as the argument rather than avoided.** *Inviting
  non-developers in* needed the historical precedent and found that the two statistics everybody
  quotes to settle it — 43% of citizen-developer initiatives scaled back, and a 25–30% no-code
  rewrite rate — have no primary source. Rather than dropping the precedent or laundering the
  numbers, the chapter reports the absence: the last time the industry tried this, nobody measured
  the result well enough to argue about it afterwards. That is a third use for a do-not-cite list,
  after "do not print this" and "check before citing", and it is worth knowing it exists.
- **Wave two is *The unit of work* absorbed, and the absorb-do-not-cite convention held up under a
  whole chapter.** The post supplies the constraint swap, the feature-first argument, the
  six-files-per-feature cost, locality of behaviour, the invisible-control-flow problem, and the
  trustworthy-black-box nuance. None of it is cited in the prose; the URL is in further reading
  beside *Cards*, under a heading that says what the two posts are without claiming them as
  evidence. The one addition the chapter makes on its own account is the counter-argument to
  cheap duplication, which the post does not raise and which this book's register requires.
- **Wave three is built from one line of `notes/raw/idea.md` and the rest of the book.** "Inviting
  others like designer and become co-pilots" is the entire source. Everything else in the chapter is
  derived from material Part II already establishes — the cheap check, the narrow surface, the named
  owner, the verification tax, the Fluent Stranger, the Accountable Bystander — which is why the
  chapter reads as a consequence of the book rather than as a new subject. A speculative chapter
  with no source is best written as an application of the parts that do have one.
- **The appendices make `--repo-url` effectively required for a shareable build.** Further reading
  carries roughly twenty links into `notes/research/` and the templates appendix links the
  repository's own `CLAUDE.md` and `cards/`. Links outside `book/` are rewritten to absolute URLs
  only when `--repo-url` is passed, and are silently left relative otherwise — no warning, because
  the build cannot tell an intentional repo link from a mistake. That was true before and cost
  little; it now affects two whole appendices. Anyone producing a copy for somebody without the
  repository should pass it.
- **Milestone 15 hit no `make check` problems and seven long lines, all of them single links.** A
  throwaway width checker was run from `/tmp` — the ninth independent writing of it — and every
  prose overshoot was fixed; what remains is the unwrappable-cross-reference case recorded as a
  decision above. The mermaid diagram in *The three waves* was rendered through
  `npx @mermaid-js/mermaid-cli` before finishing, and a first version with dotted back-arrows was
  simplified after looking at the rendered PNG rather than at the source, which is an argument for
  rendering diagrams rather than eyeballing them.
- **`57772ad900e3` opened all seven blocked primary sources, plus the kernel file, and found one
  live error in the manuscript.** Full account in
  [*The source-verification pass*](#the-source-verification-pass). The single most useful thing it
  learned is in the decisions log: **six of the seven barriers were properties of the retrieval
  method, not of the document.** `WebFetch` cannot read a PDF that `curl` plus `pdftotext` reads in
  two seconds; a docs site behind an anti-scraping challenge may have its content sitting in a
  public git repository; `developers.openai.com/<page>.md` serves what `openai.com` 403s; and a
  domain that "refuses connections" may simply have no `A` record left. Only the NSA PDF needed a
  browser, because its block is TLS-fingerprint based.
- **The falsified passage is the reason this item mattered, and it is worth being specific about
  how it failed.** Part III's `18.2% / 12.8% / 12.6%` was not invented and was not lifted from a
  content-marketing blog. It was **an average of a real table in a real system card**, computed by
  a secondary write-up, that nobody could check because the card exceeded a fetch limit. It read as
  more rigorous than the surrounding prose *because* of the decimal place. Two of the three figures
  reproduce exactly from the table; the third does not reproduce at all; and the conclusion drawn
  from them — that the more capable model hacks more — is contradicted by the same table, where
  Opus 4.5 scores 0% on the coding set. **The replacement argument is better than the one it
  replaces**, which is the usual outcome when a number gets checked, and is the case for doing this
  before publication rather than after.
- **Verifying produced two corrections nobody was looking for, both about attribution rather than
  arithmetic.** The Copyright Office's two most-quoted "conclusions" are the Office quoting a court
  and quoting a submitted comment; and the NSA guidance is NSA-only and dated May, where three
  agent files had "NSA/CISA" and "June" because June is in the URL path. Neither would have been caught
  by re-reading the agent files, and neither was in scope when the item was written. **Reading a primary
  end to end finds things that checking a specific claim against it does not.**
- **`make check` is clean and Part III sits at 14%.** The book moved from 39,370 to 39,513 words,
  all of it in the rewritten section. Two over-length lines exist in
  *What is genuinely contested*; one is pre-existing, and the other was introduced and fixed during
  this pass — the **tenth** independent writing of a throwaway width checker, which is now a
  slightly embarrassing argument for `6b0110f76388`.

- **A deferred defect shrank by three quarters while it waited, and the item description did not.**
  `9dd4d6b84b80` was filed against three undefined terms and a glossary that had no address. By the
  time it was worked, the Harness suite had defined *harness* and *skill* in italics on first use,
  milestone 15 had written the glossary and a card skeleton, and Part I already linked the glossary.
  What was left was one clause in one play. **Re-derive a deferred item against the current tree
  before acting on its description**: a description written at filing time describes a tree that no
  longer exists, and the parts of it that have quietly closed are not marked.
- **Two style rules can be individually correct and jointly impossible.** Italics on a term's first
  use, and one first use per book, cannot both hold in a book of self-contained plays where a play
  legitimately needs a word the owning suite has not reached. The fix was not to pick a rule but to
  split the job — plain gloss at the use site, italics at the owning site — and to write that down
  in the decision log so the next collision is a lookup rather than a re-derivation. Worth watching
  for elsewhere: a contract kept per-file and a contract kept book-wide will collide wherever the
  book promises both.
- **The cheapest way to keep a promise made in print is to keep it.** The item offered narrowing
  Part I's sentence as the fallback. Twenty-one words of gloss was less work than editing the
  promise, and considerably less than explaining to a reader why the book hedged its own contract.

- Milestone 19's second chapter landed: `703e507c86aa` wrote
  [*Split the agent file into cards*](../book/part-2-plays/context/split-the-agent-file-into-cards.md), the
  Context suite's fourth play, and with it the first worked example in the book whose subject is
  this repository. `book/examples/cards/reproduce.py` asserts both of its captured blocks against
  the real `cards/` directory, which makes an edit there an edit to the book — see
  [*The cards play*](#the-cards-play). Four places that counted the plays as eighteen now say
  nineteen: `book/TEMPLATE-play.md`, `book/README.md`, `the-three-waves.md`, and the Context entry
  in `appendices/team-checklists.md`.
- The *rocket-launch* material from the Cards post — preparation mode and execution mode as
  distinct, the project ready before the agent starts — was **deliberately left unspent** by the
  cards play. It belongs to `0bdccc346bd4` and Part I, as milestone 19 filed it.

- Milestone 19's third and last chapter landed: `0bdccc346bd4` put preparation mode and execution
  mode into [*What this book assumes about
  you*](../book/part-1-argument/what-this-book-assumes-about-you.md). **Both of the author's posts
  are now fully spent**, and the audit that started the milestone is closed. See [*The preparation
  thread*](#the-preparation-thread).
- **The obvious home for an idea and its right home are different questions.** Two chapters looked
  like better fits than the one chosen — one argues disposition-versus-practice in nearly the same
  words, the other opens on a vignette that *is* the two modes without naming them — and both were
  declined: the first had no room and a four-part structure the idea would have broken, and the
  second would have had chapter one resolve a disagreement the book spends four parts earning. The
  chapter that took it was the one that tells the reader what the plays are for.
- **A framing idea is cheaper than it looks and a play is dearer.** The whole thread cost 275 words
  and one deleted duplicate sentence. As a play it would have cost 1,100 words, a worked example on
  a project not yet taken, a failure mode name, and an argument with two existing Context plays
  about which of them owns the agent file.

- `f986730f7a1f` verified the three dated claims in *Wire in the outside world* against primary
  sources. **All three hold; one was described wrongly and is corrected in print.** Full account in
  [*The MCP citation check*](#the-mcp-citation-check); `notes/research/mcp.md` carries the quotes,
  eight new source entries, and the corrected incident list. `make lint` is clean and *The play* is
  at exactly its 500-word ceiling after the edit.
- **A claim can be true, dated correctly, and still wrong about who did it.** The play had the right
  package, the right month and the right behaviour, and attributed all of it to a mail vendor that
  had nothing to do with the package — the one thing nobody thought to check, because the package
  was named after them. **Check the actor as carefully as the date.** The failure mode is specific
  to supply-chain incidents, where impersonation is the attack and the name in the incident is the
  victim's rather than the attacker's, and it is the kind of sentence a later writer will reproduce
  from memory.
- **"Stated at the level of shape" worked exactly as the handoff intended.** Because the play named
  no figures, the correction was a clause rather than a paragraph, and nothing downstream moved. The
  claims that did not survive — the long benign window, the vendor's own maintainer — were both
  adjectival, and the ones that did were the package name, the month, and the mechanism. **Worth
  copying for any claim a research note flags as unverified:** write the part you are confident in
  and leave the qualifier out until someone has opened the source.
- **A primary source can be retired by an acquisition.** Koi Security's postmark-mcp write-up is
  the origin of every download figure on the subject, and it now 301s to a Palo Alto Networks
  product page; `web.archive.org` is blocked from this harness. This is a different failure from a
  source being wrong or paywalled, it is not fixed by searching harder, and it will recur in a field
  where the researchers keep being bought. **The defence is to quote the affected party's own
  advisory where one exists** — Postmark's outlived the researcher's post by a year.
- **The incident list in `mcp.md` now marks which entries the book actually cites**, because three
  of them are still second-hand and one future reader in a hurry is all it takes. The Asana
  incident, the two CVE clusters, and the GitHub-PR-title injection are cited nowhere and are
  labelled as such at each entry rather than only in the gaps section.
- **Part III's figures have now all been opened at source (`3884b4f3fc82`), and the result is
  mostly clean.** Twenty-six primaries; eleven defects in print, all fixed; four of them the
  reward-hacking species. Full account in [*The Part III figure
  re-check*](#the-part-iii-figure-re-check). The three things most worth carrying out of it: the
  **802-developer mandate study is clean end to end** and is the largest block of figures in the
  part; **Google's enterprise RCT abstract contradicts its own hypothesis box** and the book
  correctly follows the box, so do not "correct" it; and **`web.archive.org` is reachable from this
  harness** for at least openai.com and apiiro.com, which contradicts the earlier `mcp.md` note
  above — the block that note records may have been transient or path-specific. Worth re-testing
  before concluding the Archive is unavailable.
- ~~**`make lint` does not check the per-chapter word budgets in `STYLE.md`**~~, and that is how
  *What is genuinely contested* sat at 1,559 against a 1,500 ceiling from `57772ad900e3` until
  `3884b4f3fc82` counted by hand. **Closed** by `023ba519cdd0`, which taught the checker all of
  them — the three mechanical ones this entry named, plus the whole-play budget and the five
  per-heading ones in `TEMPLATE-play.md`, which the note called the larger prize. See [*The
  word-budget check*](#the-word-budget-check).
- **A checker written for one class of defect finds more of it than the hand passes did**
  (`023ba519cdd0`). Three budget overruns had ever been found in this book, all by people counting
  on purpose. The first run of the automated version found **eleven**, in five suites nobody had
  thought to check, including one section that had been trimmed to 488 and was back at 533 four
  commits later. **The value of mechanising a check is not the check; it is the files nobody was
  looking at.**
- **A two-link fix is a prose edit** (`023ba519cdd0`, on `5e0f39858134`). Adding the missing
  cross-reference to *Scope a task to fit the window* cost 45 words of connecting sentence in a
  section that was already at its ceiling, and the commit message reasonably says nothing about
  length. **Any edit that adds a clause is subject to the budget**, which is precisely why the
  answer is a checker rather than a convention.
- **Retrieval routes, confirming and extending `57772ad900e3`'s table.** `curl` + `pdftotext
  -layout` opened fourteen arXiv PDFs with no failures, including ones earlier passes recorded as
  "resisted text extraction" — the obstacle was always the fetch size limit. Two additions worth
  recording: **arXiv version pinning matters** (`arxiv.org/pdf/<id>v1` gets the version an agent file
  actually cited, and two Part III sources have since been revised with different headline
  numbers), and **a figure with no numeric labels is not extractable by any route** — render the
  page with `pdftoppm -r 600` and read the image before concluding a number is missing, which is
  how METR's chart-only confidence interval was settled.

### Failure-mode registry

One name per phenomenon across the whole book. Check here before coining a name; append yours
here when you do. Convention is in [`book/STYLE.md`](../book/STYLE.md#naming-failure-modes).

| Name | Phenomenon | First used in |
|---|---|---|
| **the Context Landfill** | An agent file that only ever grew; stale and current instructions weighted equally. | `context/write-the-agent-file-that-actually-gets-read.md` (coined in `book/STYLE.md` sample 4) |
| **the Merged Hand** | Agent run started on a dirty tree; the diff interleaves two authors and can be neither kept nor discarded. | `book/TEMPLATE-play.md` specimen play |
| **the Agent File That Never Arrived** | Instructions written, committed, and never loaded. Nothing errors, and the usual check reports the same thing whether they loaded or not. | `context/write-the-agent-file-that-actually-gets-read.md` |
| **the Reassembled Agent file** | A short index and short cards, and every run still loads most of the material, because each card links to the next one a reader would want. Not the Context Landfill — nothing is stale and nothing is flat. The tell is an agent opening three files before it edits one. | `context/split-the-agent-file-into-cards.md` |
| **the Flattering Dashboard** | A tool reports large savings measured at its own boundary, against a counterfactual the billing system never applies, while the bill rises. | `context/starve-the-context.md` |
| **the Permanent Near Miss** | Every run ends just short of done and every continuation also ends just short; no turn presents itself as the one to stop on. | `context/scope-a-task-to-fit-the-window.md` |
| **the Paper Fence** | A rule that forbids something and does not stop it: it matches the spelling the agent usually produces, so uneventful runs read as evidence. Covers the prose version too — an instruction mistaken for enforcement. | `harness/choose-your-harness.md` |
| **the Unsummoned Skill** | A skill that is written, committed, and never triggered. The metadata loaded as designed and lost the match; a non-match is not an event anything logs. | `harness/package-repeatable-expertise.md` |
| **the Instruction You Did Not Write** | Agent behaviour that traces to nothing in your repository, because it arrived in a tool description — authored context from a connected server. | `harness/wire-in-the-outside-world.md` |
| **the Tidy Summary** | A delegated worker returns a well-organised, correct-as-far-as-it-goes summary that reads identically whether the work was thorough or partial. The compression is why you delegated; it is lossy exactly where you would check. | `orchestration/decompose-into-subagents.md` |
| **the Load-Bearing Scaffold** | A scripted stage built around a capability gap that has since closed, which can no longer be removed because retry logic, metrics, and neighbouring stages have grown into it. | `orchestration/make-the-control-flow-deterministic.md` |
| **the Clean Merge** | Git reports success, both branches were green, and the merged tree was never tested by anyone. The conflicts git can see are the survivable class; the expensive class exists only in the union. | `orchestration/work-in-parallel-without-collisions.md` |
| **the Drifting Yes** | Reviewer approval of agent changes gets easier with exposure while approval of colleagues' changes holds flat. Invisible to the surface metrics a reviewer would check; the tell is the reviewer's own comments getting shorter. | `verification-and-trust/review-code-you-did-not-write.md` |
| **the Green Suite That Tests Nothing** | The suite passes and the green is a fact about the suite: a test deleted or skipped, a test input special-cased in the implementation, or an assertion no plausible defect could fail. | `verification-and-trust/make-the-agent-prove-it.md` (coined in `book/STYLE.md`'s naming section) |
| **the Accountable Bystander** | A named owner who approved more changes than anyone could have understood, and had no standing to decline. Accountability by title, bystanding in fact; the incident review finds the name and stops. | `verification-and-trust/decide-who-signs-off.md` |
| **the Expensive Nothing** | A turn that bills more than everything before it while doing no work: the cache went cold during an interruption, so a one-line reply reprocessed the whole conversation at full rate. The tell is a cost spike on a message you could have sent by nodding. | `economics/understand-what-you-are-paying-for.md` |
| **the Long Way Round** | The model is cheaper per token and the invoice is larger, because it reaches the same answer through several times as many turns and each turn re-sends the conversation. The per-token saving is real and is applied to far more tokens. | `economics/match-the-model-to-the-job.md` |
| **the Errand That Became a Project** | A one-line request returns a diff across nine files, all defensible and none of it asked for. Reverting feels wasteful because the extra work is fine, so it ships, and reviewing it is now larger than the change would have been by hand. | `economics/know-when-not-to-use-an-agent.md` |
| **the Founding Document** | A working agreement that has become constitutional: nobody amends it, everyone has drifted from it, and it is quoted rather than followed. Distinct from the Paper Fence — that is a rule that does not stop a machine; this is a rule the people have stopped obeying. | `team/build-the-working-agreement.md` |
| **the Showreel** | A sharing session where everyone demonstrates their best run and nobody mentions the attempts that went nowhere, so the shared library is assembled from everyone's best day and reproduces for nobody on an average one. | `team/collect-and-refine-as-a-team.md` |
| **the Fluent Stranger** | A new joiner producing good, correctly-shaped work immediately, with no sense yet of which parts of the system are load-bearing or which of the agent's confident suggestions are wrong here specifically. Nobody notices, because the output looks like everyone else's. | `team/onboard-someone-into-all-this.md` |
| **the Confident Wrong Rewrite** | A syntactically valid patch that is functionally incorrect, incomplete, or addresses a restatement of the problem rather than the problem. The dominant failure class, and it compiles. | `part-3-where-it-struggles/the-failure-modes-worth-naming.md` (coined in `book/STYLE.md`'s naming section) |
| **the Vanishing Fix** | A run reaches a correct solution partway through, keeps going, and overwrites it. Visible in the transcript, invisible in the diff and the closing summary. This is the phenomenon Part I described as having no agreed name. | `part-3-where-it-struggles/the-failure-modes-worth-naming.md` |
| **the Requirement It Can Still Quote** | The agent restates the requirements accurately and stops satisfying them. Not a context-window problem: coverage retention holds while strict success collapses. | `part-3-where-it-struggles/the-failure-modes-worth-naming.md` |
| **the Endless Polish** | Each pass improves something and the file is worse than it was five passes ago; nothing fails, so nothing stops. Distinct from the Permanent Near Miss — that is a run that never arrives, this one arrives repeatedly and leaves sediment. | `part-3-where-it-struggles/the-failure-modes-worth-naming.md` |
| **the Immaculate Surface** | Every check you have automated is clean and the defect is in a class you have not automated a check for. The tell is your own review comments getting shorter and more stylistic while the changes get larger. | `part-3-where-it-struggles/the-failure-modes-worth-naming.md` |
| **the Instant Concession** | Push back on something the agent got right and it agrees immediately, replacing it with something worse. Named on recognition rather than on measurement, and the chapter says so in print. | `part-3-where-it-struggles/the-failure-modes-worth-naming.md` |

**The Merged Hand is registered but is not in the book.** It is named in `book/TEMPLATE-play.md`'s
specimen play, which is deliberately not in the table of contents, so Part III's index of failure
modes omits it — a row pointing at a file no reader can open is worse than an absence. If a suite
ever wants that material, writing it fresh claims the name.
