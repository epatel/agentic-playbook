# Write the brief the agent actually reads

## Problem

Your project brief is four hundred lines long and every line was true on the day somebody added it.
The agent reads all of it and still opens a pull request using the error-handling pattern the team
abandoned in March — the one described on line 30, under a heading nobody has scrolled past in a
year. You retype the correction, as you did last week. The file is not wrong; it is flat. Four
hundred equally weighted instructions, perhaps twelve of which change what the agent does, and you
now brief the agent twice: once in the file, and once by hand, every session.

## The play

Treat the brief as a working set, not as a description of the project. Six moves, in order.

1. **Write it from corrections, not from a tour of the codebase.** Add a line when you have typed
   the same correction twice, when a review catches something the agent should have known, or when a
   new colleague would have needed the same sentence
   ([`agent-context-files.md`](../../../notes/research/agent-context-files.md)). Every line then has
   a reason you can check later, which is the only thing that makes deleting it possible.
2. **Keep only what is true everywhere.** A convention that applies to one directory, a procedure
   with steps, or a rule that matters twice a quarter does not belong in a file that loads in every
   session. Move it to something conditional — a path-scoped rule, a skill, or a card — so it
   arrives when its situation does. See
   [*Package repeatable expertise*](../harness/package-repeatable-expertise.md) for the procedural
   half.
3. **Do not mistake reorganisation for reduction.** Splitting a 600-line brief into six `@path`
   imports is housekeeping, not savings: imports are expanded at launch and the token count is
   unchanged. Only conditional loading reduces anything.
4. **Make one file the source of truth, and make it portable.** `AGENTS.md` is the multi-vendor
   filename — plain markdown, no required sections, stewarded by the Linux Foundation's Agentic AI
   Foundation since December 2025. `CLAUDE.md` is one vendor's filename with its own precedence
   rules. Put the content in `AGENTS.md` and let the vendor file be a one-line import, so a
   colleague who switches tools does not fork the brief.
5. **Verify that it arrived.** Ask the agent, in its first message of a session, to state its
   project instructions back to you. This is the check that separates "the agent ignored the brief"
   from "the brief never loaded", which are different problems with different fixes.
6. **Prune on the same trigger you add on.** When you correct the agent on something the file
   already says, that line is not working. Rewrite it or delete it. Adding a second line about the
   same subject is how the first one got ignored.

The reason any of this works is that a brief is context, not configuration. Claude Code's own
documentation was unusually plain about it in September 2026: the file is "delivered as a user
message after the system prompt", and if you need an action blocked regardless of what the model
decides, you need a hook rather than a sentence. So the brief does not constrain the agent, it
competes for its attention — with the task, the files it has opened, and every other line of the
brief. A line that changes nothing is not neutral. It is noise, and it is paid for out of the same
attention as the lines that matter. That is the exchange rate here. You give up the comfort of
writing something down once and considering it handled, and you get a file whose instructions are
followed because there are few enough of them to be followed.

## Worked example

`atlas`, a Python billing service, eighteen months old, four contributors.

Before:

> Captured September 2026, BSD `wc` on macOS 26.4.

```bash
$ wc -l CLAUDE.md
     412 CLAUDE.md
```

Reading it end to end — which nobody had done since about line 200 was written — the lines sorted
into three piles. Stale: a note about a CI runner decommissioned last spring, and instructions for a
deployment script that was replaced in January. Generic: eleven lines on Python style that `ruff`
already enforces and the agent already knew. Scoped: forty lines about the migration workflow, which
matter enormously when touching `atlas/migrations/` and never otherwise.

The stale pile was deleted. The generic pile was deleted. The scoped pile moved out into a rule that
loads only when the agent opens a matching file:

```markdown
---
paths:
  - "atlas/migrations/**/*.py"
---

# Migrations

- Every migration is reversible; write the `reverse_sql` even when it is a no-op.
- Never edit a migration that exists on `main`. Add a new one.
```

What remained became the brief, in `AGENTS.md`, with the vendor file reduced to an import:

> Captured September 2026, BSD `wc` on macOS 26.4.

```bash
$ wc -l AGENTS.md CLAUDE.md
      34 AGENTS.md
       4 CLAUDE.md
      38 total
```

```markdown
@AGENTS.md

## Claude Code
Use plan mode for anything under `atlas/billing/`.
```

The result was not clean. Within two days the agent twice wrote raw SQL into a data migration, which
the deleted deployment section had forbidden in a subordinate clause nobody had noticed was
load-bearing. One line went back, into the path-scoped rule, where it costs nothing until it is
relevant. That is the shape of a good prune: you find out what mattered by removing it, and the
feedback arrives in a day rather than in an incident review.

## Failure mode

**The Context Landfill.** Every useful fact about the project went into the brief, because each one
was useful on the day it was added, and nothing has ever been removed. The file did not become
wrong. It became flat: the convention that matters and the note about last spring's CI runner arrive
with the same weight, and the agent follows the current convention roughly half the time. The tells
are a brief that has only ever grown, and two instructions that contradict each other and have gone
unnoticed because nobody reads the file end to end.

**The Brief That Never Arrived.** The instructions are correct, committed, and not loaded. The agent
behaves like a competent stranger — reasonable code, house conventions absent — and the obvious
explanation, that it ignored the brief, is wrong. Precedence rules do this silently: on Claude Code
2.x, a `CLAUDE.local.md` stops the team's `AGENTS.md` being read at all, and nothing errors. The
tell is that your usual check cannot separate the two cases: a natively read `AGENTS.md` never
appears in `/context` under Memory files, so that list is empty on success and on failure alike.

## Checklist

- [ ] Every line in the brief traces to a correction you would otherwise retype
- [ ] Nothing in it is scoped to one directory, one procedure, or one rare situation
- [ ] Splitting into imports was not counted as a reduction
- [ ] One file holds the content; the vendor-specific file is an import or a symlink
- [ ] The agent has stated its project instructions back to you in a fresh session this week
- [ ] No two lines in the file contradict each other
- [ ] Lines corrected around, rather than followed, were rewritten or deleted

**See also:** [*Starve the context*](starve-the-context.md) ·
[*Package repeatable expertise*](../harness/package-repeatable-expertise.md)
