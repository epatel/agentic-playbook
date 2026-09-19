# The Agentic Playbook

A field guide for working developers who already use agentic coding tools daily and want to get
good at them. It is plays-first: about three-fifths of the book is named, self-contained moves with
a fixed shape, and the argument that justifies them is kept short on purpose.

**Start at [`book/preface.md`](book/preface.md), or open any single play and act on it this
afternoon.** Nothing has a required order and nothing has to be built to read it — the markdown in
[`book/`](book/) is the deliverable.

## Contents

### Front matter

- [Preface](book/preface.md)

### Part I — The Argument

Why the engineering layer around these tools is genuinely unsettled, and what a developer still
needs to know. Roughly 11% of the book, and deliberately out of the way after that.

1. [Before Git, before Scrum, before this](book/part-1-argument/before-git-before-scrum-before-this.md)
2. [The four areas, re-weighted](book/part-1-argument/the-four-areas-reweighted.md)
3. [What this book assumes about you](book/part-1-argument/what-this-book-assumes-about-you.md)

### Part II — The Plays

Eighteen plays in six suites. Each one is the problem, the play, a worked example, the way it goes
wrong, and a checklist — the same five headings every time, so the book is skimmable under
deadline. Tools appear inside plays as examples, never as headings.

**[Context](book/part-2-plays/context/index.md)** — signal over noise.

4. [Write the brief the agent actually reads](book/part-2-plays/context/write-the-brief-the-agent-actually-reads.md)
5. [Starve the context](book/part-2-plays/context/starve-the-context.md)
6. [Scope a task to fit the window](book/part-2-plays/context/scope-a-task-to-fit-the-window.md)

**[Harness](book/part-2-plays/harness/index.md)** — every extension of reach is an extension of
what can go wrong, bought together.

7. [Choose your harness](book/part-2-plays/harness/choose-your-harness.md)
8. [Package repeatable expertise](book/part-2-plays/harness/package-repeatable-expertise.md)
9. [Wire in the outside world](book/part-2-plays/harness/wire-in-the-outside-world.md)

**[Orchestration](book/part-2-plays/orchestration/index.md)** — every piece of orchestration
encodes an assumption about what the model cannot do, and assumptions expire.

10. [Decompose into subagents](book/part-2-plays/orchestration/decompose-into-subagents.md)
11. [Make the control flow deterministic](book/part-2-plays/orchestration/make-the-control-flow-deterministic.md)
12. [Work in parallel without collisions](book/part-2-plays/orchestration/work-in-parallel-without-collisions.md)

**[Verification and trust](book/part-2-plays/verification-and-trust/index.md)** — everything the
agent produces about its own work is a claim.

13. [Review code you did not write](book/part-2-plays/verification-and-trust/review-code-you-did-not-write.md)
14. [Make the agent prove it](book/part-2-plays/verification-and-trust/make-the-agent-prove-it.md)
15. [Decide who signs off](book/part-2-plays/verification-and-trust/decide-who-signs-off.md)

**[Economics](book/part-2-plays/economics/index.md)** — cost is a product, not a price.

16. [Understand what you are paying for](book/part-2-plays/economics/understand-what-you-are-paying-for.md)
17. [Match the model to the job](book/part-2-plays/economics/match-the-model-to-the-job.md)
18. [Know when not to use an agent](book/part-2-plays/economics/know-when-not-to-use-an-agent.md)

**[Team](book/part-2-plays/team/index.md)** — a team's practice with these tools is an artefact
that has to be written, maintained, and handed over.

19. [Build the working agreement](book/part-2-plays/team/build-the-working-agreement.md)
20. [Collect and refine as a team](book/part-2-plays/team/collect-and-refine-as-a-team.md)
21. [Onboard someone into all this](book/part-2-plays/team/onboard-someone-into-all-this.md)

### Part III — Where It Struggles

The honest accounting, written expecting a sceptical reader to start here.

22. [What agents are reliably bad at](book/part-3-where-it-struggles/what-agents-are-reliably-bad-at.md)
23. [The failure modes worth naming](book/part-3-where-it-struggles/the-failure-modes-worth-naming.md)
24. [Where the time actually goes](book/part-3-where-it-struggles/where-the-time-actually-goes.md)
25. [What is genuinely contested](book/part-3-where-it-struggles/what-is-genuinely-contested.md)

### Part IV — Next Waves

The only speculative material in the book, labelled as such, dated, with the experiment that would
settle each claim.

26. [The three waves](book/part-4-next-waves/the-three-waves.md)
27. [Refactoring a codebase for agents](book/part-4-next-waves/refactoring-a-codebase-for-agents.md)
28. [Inviting non-developers in](book/part-4-next-waves/inviting-non-developers-in.md)

### Appendices

29. [Glossary](book/appendices/glossary.md)
30. [Team checklists](book/appendices/team-checklists.md)
31. [Copy-paste templates](book/appendices/copy-paste-templates.md)
32. [Further reading](book/appendices/further-reading.md)

## Reading it in one file

`make html` collects every chapter into one self-contained HTML file with a contents sidebar and
browser-drawn diagrams. It needs only pandoc.

```bash
make html && make open-html
make pdf                 # needs pandoc plus a PDF engine; typst is the default
make check               # what is in the book, what is orphaned, word counts per part
make                     # lists the targets
```

Output goes to `build/`, which is generated and never committed. See
[`cards/building-the-book.md`](cards/building-the-book.md).

## What is in this repository

| Path | Holds |
|---|---|
| [`book/`](book/) | The book. [`book/README.md`](book/README.md) holds the authoritative table of contents, which is the only thing that encodes order. |
| [`book/STYLE.md`](book/STYLE.md) | Voice, the outright bans, the formatting mechanics. |
| [`book/TEMPLATE-play.md`](book/TEMPLATE-play.md) | The five-heading play contract, plus one fully written specimen play. |
| [`notes/research/`](notes/research/) | Twenty-one cited research briefs. Every figure in the book traces to one, or to a primary source quoted in the sentence. |
| [`notes/raw/`](notes/raw/) | The original ideation, frozen as a provenance record. |
| [`PLAN.md`](PLAN.md) | The design document: locked decisions, the outline, the reasoning. |
| [`plans/agentic-playbook.md`](plans/agentic-playbook.md) | The execution plan: milestones, the decision log, the handoff note, the open questions. |
| [`cards/`](cards/) | Repo conventions, as self-contained context cards. Indexed from [`CLAUDE.md`](CLAUDE.md). |
| [`scripts/`](scripts/), [`Makefile`](Makefile) | The build. One Python file, no dependencies. |

## Contributing

The book has a style guide and a template, and they are enforced rather than suggested: read
[`book/STYLE.md`](book/STYLE.md) and [`book/README.md`](book/README.md) before writing a sentence,
and [`book/TEMPLATE-play.md`](book/TEMPLATE-play.md) too if you are writing a play. Prose wraps at
100 columns, diagrams are mermaid, and a file that is not in the table of contents is not in the
book. Run `make check` before you finish.

Disagreement is the point — the book says in its own preface that it is one account written in
enough detail to be disagreed with precisely. A correction with a source attached is the most
useful thing anyone can send.
