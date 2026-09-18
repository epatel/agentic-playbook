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

## Milestones

| # | Milestone | Board item | Status |
|---|---|---|---|
| 1 | Consolidate ideation into an authoritative plan | `956e4f5ab7db` | ✅ done |
| 2 | Agentic setup — `CLAUDE.md`, cards, shared plan | `5a8f313f87cc` | ✅ done |
| 3 | Style guide, play template, book scaffolding | `a06026d4e603` | ✅ done |
| 4 | Research: agent context and tooling landscape | `bb1d30e52adc` | ✅ done |
| 5 | Research: orchestration and workflow landscape | `6f9d83a67e1a` | ⬜ not started |
| 6 | Research: evidence, failure modes, token economics | `8701744c4454` | ⬜ not started |
| 7 | Part I — The Argument | `e93293bfd014` | ⬜ blocked on 3 |
| 8 | Context play suite | `655473ee5afb` | ⬜ blocked on 3, 4 |
| 9 | Harness play suite | `9366c3c324b5` | ⬜ blocked on 3, 4 |
| 10 | Orchestration play suite | `3c6b76dedb59` | ⬜ blocked on 3, 5 |
| 11 | Verification & Trust play suite | `4858fbdecdf4` | ⬜ blocked on 3, 6 |
| 12 | Economics play suite | `bffa217221ed` | ⬜ blocked on 3, 6 |
| 13 | Team play suite | `cdd27e440781` | ⬜ blocked on 3 |
| 14 | Part III — Where It Struggles | `c1416f44c483` | ⬜ blocked on 3, 6 |
| 15 | Part IV — Next Waves, plus appendices | `bec9accd89be` | ⬜ blocked on 3 |
| 16 | Editorial pass — one voice, one book | `934259dc8038` | ⬜ blocked on all writing |
| 17 | Run every worked example for real, re-capture output | `3b61a6a1a684` | ⬜ blocked on 8–13 |

Milestone 3 was the real critical path: with several authors and a specific comic register,
"we'll harmonise it later" is how a book ends up with three voices. It is done, and the nine
writing tasks are unblocked.

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
2. **The staleness table in `tooling.md` ranks every finding by how fast it rots**, with a
   suggested hedge for each. Use it rather than re-deriving where the line is; it is consistent
   with `book/STYLE.md` on volatile facts.
3. **Each brief ends with a `## Concrete example we can lift`** written to be dropped into a
   *Worked example* heading. They are illustrative-but-correct per the locked decision — real
   commands and real file contents, no invented captured output.

**Next up:** the two remaining research passes (`6f9d83a67e1a`, `8701744c4454`); milestone 7
(Part I), unblocked and depending on no research; and — newly unblocked by this milestone — the
Context suite (`655473ee5afb`) and the Harness suite (`9366c3c324b5`). Team (`cdd27e440781`) is
also free to run.

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
- How much the book dates itself is answered provisionally in `book/STYLE.md` (use a figure only
  when the point collapses without it; date it in the sentence; prefer shape to figure). The
  editorial pass owns the final call.

## Open questions

Raise these rather than guessing. An agent that silently picks one answer commits the whole book
to it.

- **Play count per suite.** `PLAN.md` gives three working titles per suite. Is three a target or
  a floor? A suite with six plays and one with two would unbalance Part II. Still open —
  `book/README.md` records three as planned rather than as a ceiling, and asks suite authors to
  raise a fourth rather than add it quietly.
- ~~**Worked examples — real or illustrative?**~~ **Resolved** (milestone 3): illustrative-but-
  correct for the first draft, with a verification pass (`3b61a6a1a684`) before publication. The
  rules are in [`book/TEMPLATE-play.md`](../book/TEMPLATE-play.md#worked-examples-what-real-means).
- **How much does the book date itself?** Model names, prices, and context limits make examples
  concrete but guarantee an expiry date. Where is the line? A provisional answer is in
  [`book/STYLE.md`](../book/STYLE.md#volatile-facts) so no author is blocked on it; the editorial
  pass owns the final call.
- **Appendix templates.** Are the `CLAUDE.md` starter and working-agreement skeleton generic, or
  is this repo's own setup the worked example?
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
- **`notes/research/` contains one deliberate lead that was not closed**: NSA/CISA MCP security
  guidance dated June 2026 that returned HTTP 403 to automated fetch. If the Harness suite wants a
  government-grade citation for the security material, that PDF needs downloading by hand first.
  It is flagged in both `tooling.md` and `mcp.md` as unverified.

### Failure-mode registry

One name per phenomenon across the whole book. Check here before coining a name; append yours
here when you do. Convention is in [`book/STYLE.md`](../book/STYLE.md#naming-failure-modes).

| Name | Phenomenon | First used in |
|---|---|---|
| **the Context Landfill** | A brief that only ever grew; stale and current instructions weighted equally. | `book/STYLE.md` sample 4 — free for the Context suite to claim |
| **the Merged Hand** | Agent run started on a dirty tree; the diff interleaves two authors and can be neither kept nor discarded. | `book/TEMPLATE-play.md` specimen play |
