# Worked-example scratch projects

The book's worked examples print command output. Where that output is marked
`> Captured <Month Year>, <tool> <version>.` it came out of one of the projects in this directory,
and you can get it out again.

Each project is a minimal tree plus a Python script that builds a throwaway copy, runs the exact
commands the book prints, and echoes their real output. Nothing writes outside a temporary
directory, nothing installs anything, and every script exits non-zero if a command fails or if a
shape the book asserts is no longer true. Python 3 standard library only.

```
python3 book/examples/atlas/reproduce.py
python3 book/examples/meridian/reproduce.py
python3 book/examples/tideline/reproduce.py
python3 book/examples/session-cost/check.py
```

## What is here

| Project | Backs | Needs |
|---|---|---|
| [`atlas/`](atlas/) | [*Write the brief the agent actually reads*](../part-2-plays/context/write-the-brief-the-agent-actually-reads.md) | `wc` |
| [`meridian/`](meridian/) | [*Decompose into subagents*](../part-2-plays/orchestration/decompose-into-subagents.md), [*Work in parallel without collisions*](../part-2-plays/orchestration/work-in-parallel-without-collisions.md) | `git`, `rg`, `awk` |
| [`tideline/`](tideline/) | [*Review code you did not write*](../part-2-plays/verification-and-trust/review-code-you-did-not-write.md), [*Make the agent prove it*](../part-2-plays/verification-and-trust/make-the-agent-prove-it.md), [*Decide who signs off*](../part-2-plays/verification-and-trust/decide-who-signs-off.md) | `git`, `rg` |
| [`session-cost/`](session-cost/) | [*Understand what you are paying for*](../part-2-plays/economics/understand-what-you-are-paying-for.md) | nothing |

`session-cost/check.py` is the odd one out: it runs no commands. It re-derives every figure in that
play's cost table from the token counts and the dated prices, so the play's claim that the
arithmetic is "checkable rather than modelled" is something you can check.

## What is deliberately not reproduced

Rule 3 of [the evidence rules](../TEMPLATE-play.md#worked-examples-what-real-means) says an example
that cannot be run stays representative, and the prose must not imply otherwise. These are the ones,
and none of them prints output in the book:

| Where | Why not |
|---|---|
| `granary`'s `./gradlew` commands, in both [*Know when not to use an agent*](../part-2-plays/economics/know-when-not-to-use-an-agent.md) and [*Match the model to the job*](../part-2-plays/economics/match-the-model-to-the-job.md) | Real Gradle invocations against a Kotlin project that does not exist here. Both blocks are a command with no output; nothing is claimed about what it printed. |
| `lodestone`'s clone-and-setup in [*Onboard someone into all this*](../part-2-plays/team/onboard-someone-into-all-this.md) | The remote is fictional, and the example is about a joiner's first hour rather than about a command. |
| The harness configuration in [*Choose your harness*](../part-2-plays/harness/choose-your-harness.md), [*Wire in the outside world*](../part-2-plays/harness/wire-in-the-outside-world.md) and [*Make the agent prove it*](../part-2-plays/verification-and-trust/make-the-agent-prove-it.md) | Settings files, not transcripts. Every one parses as JSON; the behaviour they describe is cited to dated vendor documentation in the play. |
| The subagent and skill definitions across the Orchestration, Harness, Economics and Team suites | File contents, not output. |
| Everything in Part III | Published studies, cited to briefs in [`notes/research/`](../../notes/research/). No `Worked example` heading exists outside Part II. |

The one behavioural claim these projects do exercise without the book printing it is
`git diff --name-only --diff-filter=DM tests/` — the stop gate in *Make the agent prove it*, whose
whole point is that added test files pass and deleted or modified ones do not.
`tideline/reproduce.py` runs it against a branch that skips one test and deletes another, and prints
what comes back.
