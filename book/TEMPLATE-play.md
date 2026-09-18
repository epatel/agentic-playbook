# The play template

Every play in `part-2-plays/` uses these five headings, in this order, with exactly these words:

```markdown
# <Title>

## Problem

## The play

## Worked example

## Failure mode

## Checklist
```

The headings are not a suggested outline. The book's usefulness under deadline depends on a reader
being able to jump to *Checklist* in any of eighteen plays without looking, and on cross-references
being able to anchor at `#failure-mode` and land in the right place. Do not reword, reorder, merge,
or add to them. If your material does not fit, the material is usually two plays.

Read [`STYLE.md`](STYLE.md) first for voice, and [`README.md`](README.md) for file placement,
ordering, and link syntax.

## The contract, heading by heading

### Title

An imperative verb phrase in sentence case: *Starve the context*, *Review code you did not write*.
Not a noun ("Context management"), not a gerund ("Scoping tasks"), not a product name. The title is
what a colleague would say to you across a desk, and it is the string other plays will use when
they link here.

### Problem

**One paragraph. 60–120 words. No preamble.** The first sentence puts the reader in the situation;
it does not introduce the topic, set out what the play will cover, or explain that agentic coding
is changing rapidly. End on the cost — what this actually takes from you — rather than on a
summary of what comes next.

Write it straight. If the situation is absurd, the absurdity does the work; do not add a joke on
top of it. Sample 2 in [`STYLE.md`](STYLE.md#sample-2--a-problem-paragraph) is the reference.

### The play

**200–500 words.** The actual move. Numbered steps when the work is sequential, prose when it is a
judgement rather than a procedure; do not number three paragraphs to make them look like a method.

Rules:

- **No humour in here at all.** This is the 16:50-on-a-Friday section.
- Every step is checkable. "Split at the first boundary where both halves are needed at once" is a
  step; "scope it sensibly" is not.
- Say what the step buys, not just what it is. One clause is enough.
- `###` subsections are allowed if the play has genuinely distinct modes. Never `####`.
- One paragraph after the steps may explain *why the whole thing works* — the transferable idea the
  reader takes to a situation this play does not cover. This is the most valuable paragraph in most
  plays and the one most often left out.
- A mermaid diagram belongs here if there is a topology or a flow. Never ASCII art.

### Worked example

**150–400 words plus blocks.** One scenario, carried end to end. Two half-examples read as neither.

The evidence rules are in [Worked examples: what "real" means](#worked-examples-what-real-means)
below. Read them; they are the section authors get wrong.

Name the project once and keep it consistent within the play. Show the state before, the move, and
the result, including the case where the result is imperfect — a worked example in which everything
works is a demo, and this reader has seen demos.

An aside is permitted in the final sentence, once the reader is out of the procedure.

### Failure mode

**80–200 words. One named mode; two only if they are genuinely different failures.**

The name is a Title Case noun phrase with a definite article, bold on first use, naming the symptom
rather than the cause. The naming rules and the shared registry are in
[`STYLE.md`](STYLE.md#naming-failure-modes) — check the running log before coining a name, and
append yours to it afterwards, so two suites do not invent two names for one thing.

Structure: name, then what it looks like from the inside, then the tell — the observable signal
that tells a reader they are in it right now. The tell is the part that makes the section useful
rather than decorative.

### Checklist

**4–8 items.** GitHub task-list syntax (`- [ ]`) so a reader can paste it into a pull request or an
issue. Imperative, each one independently verifiable, each traceable to something in *The play*.

This is the section a reader returns to on their fourth read. No new information, no jokes, no
prose. If an item needs a sentence of explanation, the explanation belongs in *The play*.

### Optional: See also

A single line after the Checklist, not a sixth heading:

```markdown
**See also:** [*Starve the context*](../context/starve-the-context.md) ·
[*Decide who signs off*](../verification-and-trust/decide-who-signs-off.md)
```

In-body cross-references are fine too, sparingly. Link syntax and anchor rules are in
[`README.md`](README.md#cross-references).

## Length

A play runs **600–1,200 words** including its example. Under 600 and it is probably a section of
another play; over 1,200 and it is probably two plays, or one play with a *Worked example* that
has become a tutorial.

## Worked examples: what "real" means

The book's standard is "real files, real commands, real output". In practice, for the first draft:

- **Examples are illustrative but must be correct.** Commands are real commands with real flags.
  File contents are valid for their format. Paths are plausible for the project described. A reader
  who types what you wrote must not hit a syntax error or an option that does not exist.
- **Do not present output as a transcript unless it is one.** If you actually ran it, say so on the
  line above the fence: `> Captured March 2026, git 2.44.` Anything without that line is understood
  to be representative, and must be written so that it could not be mistaken for a measurement.
- **Never invent a measurement.** Timings, token counts, costs, percentages, and study results are
  either measured, cited to a brief in [`notes/research/`](../notes/research/), or expressed as
  shape — "roughly a third of the cost", not "31% cheaper".
- **Abridge honestly.** `…` and `# … 14 more files` are better than padding an example to look
  complete.
- **A later pass tightens this.** Before publication, a board item exists to run the examples for
  real and replace representative output with captured output. Write examples you could actually
  run, so that pass is editing rather than rewriting.

## Copy this

```markdown
# <Imperative title, sentence case>

## Problem

<One paragraph, 60–120 words. Situation first. No preamble. End on the cost.>

## The play

<200–500 words. Numbered steps if sequential. No humour. Close with why it works.>

## Worked example

<One scenario end to end. Before, move, result — including the imperfect part.>

## Failure mode

**<The Named Thing.>** <What it looks like from inside. Then the tell.>

## Checklist

- [ ] <Verifiable>
- [ ] <Verifiable>
- [ ] <Verifiable>
- [ ] <Verifiable>

**See also:** [*<Other play>*](../<suite>/<file>.md)
```

---

# Commit before you let it run

> **Specimen play.** This file shows the shape; it does not claim a slot in the book and is not in
> the table of contents. If a suite later wants this material, write it there — do not move this
> file. Its cross-references point at files that later tasks will create; that is the syntax to
> copy.

## Problem

An agent working on a dirty tree hands you one diff containing two changes: yours and its. When the
result is eighty per cent right, which is the usual outcome, you have no way to take the eighty and
drop the rest, because `git checkout .` takes your morning with it. What follows is not a review.
It is an archaeology dig, conducted against a deadline, and archaeology is slower than rewriting.

## The play

Make the working tree disposable before every agent run, so that "throw it away and try a better
brief" costs nothing and therefore actually happens.

1. **Commit or stash your own work first.** The tree is clean at the moment the agent starts. If
   the work is not commit-worthy, `git stash -u` is enough; the point is only that `git diff`
   afterwards contains exactly one author's changes.
2. **Take a checkpoint you can name.** A branch is the cheapest form: `git switch -c agent/<task>`.
   Tags and stashes work too, but a branch survives you forgetting about it for three days.
3. **Let the run finish before you read anything.** Reading mid-run and intervening produces a diff
   with three authors in it — you, the agent, and the you-who-interrupted — which is the problem
   you just spent two steps avoiding.
4. **Review the diff as a unit and decide once:** keep, discard, or keep-with-edits. Discarding is
   `git reset --hard` back to the checkpoint, and it is meant to be unremarkable. Budget for using
   it.
5. **Squash before merging back.** Whatever intermediate commits the agent made are a record of its
   process, not of your project's history.

What this is really buying is the ability to discard. Teams that skip the checkpoint do not discard
bad runs, they salvage them — because discarding would take their own work down with it. Salvaging
a bad run is almost always more expensive than re-running it with a better brief, and it is always
more expensive than it feels while you are doing it. Every other benefit here is downstream of
making the cheap option available.

The same argument, applied to more than one run at a time, leads to separate directories rather
than separate branches: see
[*Work in parallel without collisions*](part-2-plays/orchestration/work-in-parallel-without-collisions.md).

## Worked example

A small Flask service, `orders-api`. You have half-finished notes in `README.md`, and you want the
agent to add request validation across the route handlers.

The tree is dirty:

```bash
$ git status --short
 M README.md
```

Park your own work, then hand over something clean:

```bash
$ git add -A && git commit -m "WIP: notes on validation approach"
$ git switch -c agent/request-validation
```

Run the task. When it finishes, the entire diff belongs to the agent:

```bash
$ git diff --stat main
 orders_api/routes/orders.py    | 48 ++++++++++++---
 orders_api/routes/customers.py | 31 +++++++---
 orders_api/schemas.py          | 62 +++++++++++++++++++
 tests/test_validation.py       | 94 ++++++++++++++++++++++++++++
 4 files changed, 223 insertions(+), 12 deletions(-)
```

Reading it: `schemas.py` and the tests are good, and `customers.py` has been rewritten to a
different pattern from `orders.py` for no reason anyone could defend. That is a keep-with-edits,
and it is a decision you can make in one sitting precisely because nothing in the diff is yours.

Had it gone the other way, the exit is one command:

```bash
$ git switch main && git branch -D agent/request-validation
```

and you are back to a clean tree with your notes intact, out one run. That is the price the
checkpoint was bought at, and it is the cheapest thing in this chapter.

## Failure mode

**The Merged Hand.** You start the agent on top of your own uncommitted edits, and the diff comes
back with both sets of changes interleaved inside the same hunks. The agent's work is mostly good,
so discarding is off the table; your work is unfinished, so committing the lot is off the table
too. What people do instead is review the combined diff line by line and hand-pick, which takes
longer than either clean option and produces a commit nobody can describe afterwards.

The tell is a commit message with "and" in it. The second tell is realising you cannot answer "did
the agent write this line?" about a line you are about to ship, and that the answer would change
how carefully you read it.

## Checklist

- [ ] Working tree clean before the agent starts — `git status --short` prints nothing
- [ ] A named checkpoint exists: branch, tag, or stash you can return to
- [ ] The run completed without mid-run intervention
- [ ] The resulting diff has exactly one author
- [ ] Keep / discard / keep-with-edits decided in one sitting
- [ ] Discarded runs discarded, not salvaged
- [ ] Agent's intermediate commits squashed before merge

**See also:**
[*Work in parallel without collisions*](part-2-plays/orchestration/work-in-parallel-without-collisions.md) ·
[*Review code you did not write*](part-2-plays/verification-and-trust/review-code-you-did-not-write.md)
