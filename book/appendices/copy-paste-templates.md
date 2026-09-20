# Copy-paste templates

Three skeletons. None of them was written for this appendix: each is the reduced form of something a
play works through at length, and the play is where the reasoning is. A template lifted without the
reasoning survives about a fortnight.

Two rules apply to all three. Delete anything you cannot justify — every line you keep out of
politeness is a line competing for attention with the lines that matter. And date them, because the
first thing that goes wrong with a shared document is that nobody can tell whether it still
describes the team.

## A project agent file, in two tiers

The pattern is a slim always-loaded index plus self-contained files loaded on demand. The index
carries the project's shape and a trigger per file, written in the words a request would use; each
card carries one subject and never requires loading another. Self-containment is the whole rule. One
card, one load, no chains.

Put the content in `AGENTS.md`, which every major tool reads, and let the vendor-specific file be a
one-line import.

```markdown
# <project> — <one line on what it is and what it is not>

<Two or three sentences: what this repository produces, what runs it, and the one
thing a competent stranger would get wrong on day one.>

## Cards

Load a card when its situation matches. Each one stands alone.

- [<card-name>](cards/<card-name>.md) — <when to load it, in the words a request
  would use: "adding a migration", "touching anything under billing">
- [<card-name>](cards/<card-name>.md) — <trigger>

## Working agreements

- <A convention that is true everywhere, traceable to a correction somebody typed twice.>
- <Another. If there are more than about six, some of them belong in a card.>
```

A card is the same shape one level down, and short enough to read in one pass:

```markdown
# <Subject>

<What this covers and when it applies — one paragraph, no preamble.>

## <The convention>

<The rule, then the reason. The reason is what lets somebody delete it later.>

## <A second convention>

<As above. If this file needs a third heading level, it is two cards.>
```

The vendor file wires it up and holds nothing else:

```markdown
@AGENTS.md

## Claude Code
<Anything genuinely specific to one tool, or nothing at all.>
```

This repository runs the pattern on itself: its root [`CLAUDE.md`](../../CLAUDE.md) is a real index
and [`cards/`](../../cards/) holds the real cards, so the template above is one that has been used
daily rather than one that was designed. The reasoning is in [*Write the agent file that actually
gets read*](../part-2-plays/context/write-the-agent-file-that-actually-gets-read.md), and the
argument for loading on a trigger rather than at launch is in [*Starve the
context*](../part-2-plays/context/starve-the-context.md).

## A working agreement

One page, in the repository, beside the shared agent file. Six items is the usual number and every
one of them concerns something that leaves somebody's machine; the rest goes in the personal
section, in writing, so that it stops being an argument. The full version, with a worked instance of
every clause, is in [*Build the working
agreement*](../part-2-plays/team/build-the-working-agreement.md).

```markdown
# How we work with agents — <team or repository>

Version <n>, <YYYY-MM-DD>. Amend by pull request; anyone may open one.
Last changed because: <the event that caused the last amendment>.

## Shared, and in the repository
- Project instructions live in <path>. Anything a new joiner needs on day one
  belongs there.
- Team skills live in <path>. Personal skills stay outside the repository.
- <Any precedence trap your tools have: a local file that silently disables the
  shared one, named with the version it applies to.>

## What a change has to carry
- A test that could have failed before the change, or a line saying why there
  cannot be one.
- <Your disclosure convention, if you have one, and what it does not claim.>
- A description written by a person. The agent's plan may be pasted below it,
  marked.

## Review
- Any reviewer may return a change over <n> lines unread and ask for it split.
  No explanation is owed and none is taken personally.
- <What "the same review as anyone else's" means here, and what to do when
  yours is the third one today.>

## Money and limits
- <Who can see what the tools cost, and how often.>
- We do not delegate: <the short list>. Reviewed <YYYY-MM-DD>.

## Yours, not ours
- Which harness, which model, which editor, how you prompt, what is in your own
  skills directory, how many sessions you run at once.

## Experiments
- Standing exception: say in advance that you are working against this agreement
  on purpose, and report what happened.

## When this changes
- Triggered by an event, not by a date: <a model release the team adopts, a new
  tool anyone wants to bring in, the second time somebody cites this page and it
  turns out to be wrong>.
```

## A review checklist for agent-authored changes

Paste into a pull request. The order is the point: the things that check the code are read before
the code, because they are what the rest of the review rests on, and because weakening them is the
cheapest way for a change to look finished. Reasoning in [*Review code you did not
write*](../part-2-plays/verification-and-trust/review-code-you-did-not-write.md) and [*Make the
agent prove it*](../part-2-plays/verification-and-trust/make-the-agent-prove-it.md).

```markdown
### Before reading the implementation
- [ ] Test files, CI config, linter settings, and type-checker settings read first
- [ ] No test deleted, skipped, renamed to something unreachable, or weakened
- [ ] No pipeline step removed, and no assertion loosened to accommodate the change
- [ ] Size and file count judged against our send-back threshold before reading

### Reading it
- [ ] Searched for an existing implementation of anything this introduces
- [ ] One critical path traced end to end, and I can explain it without the
      description open
- [ ] Checked what this change can now reach that it could not before: which
      credentials, which tables, which callers
- [ ] Anything the change touches that is invisible from the file it is in —
      decorators, hooks, middleware, generated code — checked at the other end

### Evidence
- [ ] The finish condition was stated in advance and names a command
- [ ] Attached evidence is command output, not a summary of it
- [ ] A suite the run could not see has been run against this
- [ ] A reproducer is supplied, or its absence is stated explicitly

### Sign-off
- [ ] One named person owns this change and can answer questions about it next month
- [ ] If this is the third agent-authored change I have reviewed today, I have
      said so and asked for a second reviewer
```

The last item is the one people delete first, and it is the one the evidence supports most directly:
review coverage is where agent-assisted throughput is paid for, and a reviewer who cannot decline is
not a reviewer.
