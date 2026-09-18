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
| 3 | Style guide, play template, book scaffolding | `a06026d4e603` | ⬜ blocks all writing |
| 4 | Research: agent context and tooling landscape | `bb1d30e52adc` | ⬜ not started |
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

Milestone 3 is the real critical path: with several authors and a specific comic register,
"we'll harmonise it later" is how a book ends up with three voices.

## Current state / handoff

The repo now has an agentic setup: a root `CLAUDE.md` with an overview and a card index, four
context cards in `cards/`, this completed shared plan, and two agent skills linked into
`.claude/skills/`.

`book/` and `notes/research/` do **not** exist yet — deliberately. The first task that needs one
creates it. For `book/`, that is milestone 3, which also owns `book/STYLE.md`.

**Next up: milestone 3 (`a06026d4e603`).** It unblocks nine writing tasks, so it goes first even
though the three research passes are independent and can run alongside it.

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

## Open questions

Raise these rather than guessing. An agent that silently picks one answer commits the whole book
to it.

- **Play count per suite.** `PLAN.md` gives three working titles per suite. Is three a target or
  a floor? A suite with six plays and one with two would unbalance Part II.
- **Worked examples — real or illustrative?** The template demands "real files, real commands,
  real output." Do we run the commands and paste genuine output, or write plausible examples?
  This changes how long every play takes and how fast it goes stale.
- **How much does the book date itself?** Model names, prices, and context limits make examples
  concrete but guarantee an expiry date. Where is the line?
- **Appendix templates.** Are the `CLAUDE.md` starter and working-agreement skeleton generic, or
  is this repo's own setup the worked example?
- **Rendering.** Markdown-on-GitHub is the committed deliverable. If a static site is ever wanted,
  that decision needs making before the prose accumulates site-specific link syntax.

## Running log

Append discovered constraints and cross-task notes here as work proceeds.

- Agentic setup applied (milestone 2): root `CLAUDE.md`, `cards/` with four cards, this plan
  completed to the shared-plan shape, `backward-planning` and `review-agentic-setup` skills
  linked into `.claude/skills/`.
