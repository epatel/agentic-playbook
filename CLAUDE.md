# The Agentic Playbook

A markdown book, written in this repo, for working developers who already use agentic coding
tools daily and want to get good at them. It is plays-first: about 60% of the book is named,
self-contained plays with a fixed template, and the framing argument is deliberately compressed
to make room for them. There is no application code here and no package manager; the deliverable
is the prose. `make html` and `make pdf` collect the chapters into one file for reading and
review, but nothing has to be built for the book to be readable.

The book is being written by multiple agents working in parallel on separate board items, which
is why the conventions below exist in writing rather than in someone's head.

## Read this first

**[`plans/agentic-playbook.md`](plans/agentic-playbook.md)** is the shared execution plan: the
goal, the non-goals, milestone status, the append-only decision log, the current handoff note,
and the open questions. Read it before starting any task, and update it when you finish one.
It is how tasks that never share a context window stay pointed the same way.

**[`PLAN.md`](PLAN.md)** is the authoritative design document behind the plan — the reasoning,
the full outline, the build sequence. Read it when you need the *why* behind a decision.

## Context cards

Load a card when its situation matches. Each one stands alone.

- [repo-layout](cards/repo-layout.md) — creating a file and unsure where it belongs, looking for
  existing material, or about to edit something in `notes/raw/` or `PLAN.md`
- [book-structure](cards/book-structure.md) — writing or editing any part of the book itself:
  which part it belongs to, how long it should be, what shape a play takes
- [research-notes](cards/research-notes.md) — running a research pass, or producing anything
  that a later writing task will cite
- [standing-defaults](cards/standing-defaults.md) — adding a diagram, adding a script or
  dependency, or wondering how to format a file
- [building-the-book](cards/building-the-book.md) — collecting the chapters into one file,
  producing an HTML book or a PDF, checking that what you wrote is actually in the book, checking
  it against the column limit and the style guide's outright bans, checking that a rewrite lost no
  figure, or serving the book for review and acting on the annotations a review leaves behind

## Working agreements

- **Prose wraps at 100 columns.** Parallel authors merge into the same book; line-scoped diffs
  are what make that survivable. `make lint` decides it, along with everything else in
  `book/STYLE.md` a machine can decide. Do not write your own checker — four tasks already did.
- **`make lint` also counts the word budgets**, per chapter, per opener, per play and per play
  section, and an overrun fails the build. Do not count words by hand or with `wc`; both run high
  against the counter the book is measured with. It also reports **sentence-shape notes** (long
  sentences, em-dash density, headings that point back): these never fail, and a run that ends "No
  problems" is clean.
- **Diagrams are mermaid**, in fenced ```mermaid``` blocks. Never ASCII art.
- **`notes/raw/` is frozen.** It is a provenance record of the original ideation, not a spec.
- **Locked decisions in `PLAN.md` are not reopened unilaterally.** If your task cannot proceed
  under one, stop and ask rather than working around it.
- **Ask when instructions conflict.** Two rules that cannot both be satisfied, an instruction that
  contradicts a locked decision, an answer that contradicts itself — stop and say which two things
  disagree. Picking the more plausible reading and saying so is not the same as asking, and the
  cost of guessing scales with the size of the edit.
- **Keep this file and the cards current as you go.** They describe how the repository works, so a
  change to how it works is not finished until they say so — a renamed card, a new `make` target,
  a convention that moved. The rule you did not update is the one the next agent follows.
- **Log what the next agent needs.** Finishing a task means updating the milestone, appending any
  decision you made, and rewriting the handoff note in `plans/agentic-playbook.md`.
