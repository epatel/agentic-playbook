# Know when not to use an agent

## Problem

The change is one line and you know exactly which line. You describe it instead — four sentences,
because describing it is the reflex now — and eleven minutes later there is a diff across nine
files, all of it defensible, most of it not what you asked for, and a review nobody budgeted. The
change ships. What it cost was not tokens. It was twenty-five minutes, one context switch, and a
small erosion in your ability to say what your own code does without going to look.

## The play

Four tests before you delegate, and two habits that keep them honest.

1. **Compare against your own hands, review included.** The comparison people run is typing time
   against prompt time. The real one is typing time against prompt, wait, read the diff, decide,
   and correct. Anything a deterministic tool already does — an IDE rename, a codemod, a formatter,
   a one-file edit you could make from memory — loses on every term.
2. **Do it yourself when specifying it is the hard part.** If stating precisely what you want means
   working out the invariant, the ordering, or the constraint, you have done the expensive part by
   the time the brief is written. Write the change; delegate the sweep that follows it.
3. **Do it yourself when nothing cheap can say it is wrong.** No test, no type, no reproducer, no
   diff short enough to scan: what comes back is a claim rather than a result. Buying claims is how
   a saving relocates into review, which is where DORA's *verification tax* is paid and where no
   team has a budget line.
4. **Do not add agents to buy capability.** Fan-out multiplies everything: vendor figures put
   multi-agent systems at roughly fifteen times the tokens of a chat interaction, because every
   teammate carries its own context and none of them share a cache. Under matched protocol across
   ten benchmarks in June 2026, five of six multi-agent systems scored below a single-agent
   baseline while costing more. Give one agent the same budget first.
5. **Do not ask the agent what the job will cost.** Frontier models predict their own token usage
   at correlations up to 0.39 and systematically underestimate it. Expert human difficulty ratings
   align only weakly with actual token cost, so neither of the two available estimators works.
6. **Date your no-go list.** On METR's published measurements the 50% task-length horizon has been
   doubling roughly every three months on the 2024-onward trend, so a rule written last year
   describes last year's models. It moves the other way too, as review capacity rather than model
   capability becomes the thing you run out of.

The constraint that actually binds is not what the agent can do. In the largest enterprise study
available — 802 developers, 196,212 pull requests, January 2024 to April 2026 — a doubling mandate
worked on its own terms: throughput reached 2.09× baseline and nearly all pull requests became
agent-authored. Merge and revert rates stayed flat. What moved was human review coverage, from 89%
of pull requests to 68%, with the load on each remaining reviewer doubling, and end-to-end cycle
time rose 22% — the thing the mandate existed to compress. Anthropic put the general case plainly
in December 2024 and has not retracted it: "For many applications, however, optimizing single LLM
calls with retrieval and in-context examples is usually enough." The exchange rate is throughput on
the days you would have got away with it, and the occasional half-hour spent hand-writing something
an agent would have done perfectly well.

## Worked example

One week on `granary`, a Kotlin service ingesting warehouse stock feeds from forty suppliers, three
tasks sat on the board looking like the same size of job.

**The rename.** `supplierRef` became `supplierCode` across the ingest module. The agent had done
the equivalent the month before: a brief, a wait, and a fourteen-file diff to read. This time it
was one IDE refactoring and a compile.

```bash
$ ./gradlew :ingest:compileKotlin
```

Both routes missed the same thing — the identifier embedded in a JSON fixture, which a rename
refactoring does not see and a compile does not catch. The difference was that this time it took
seconds rather than a review, and the gap was a known limitation rather than a surprise in a diff.

**The bug.** One supplier had begun omitting `unitOfMeasure`, and the adapter was turning that into
a silent zero four layers downstream. Finding it took forty minutes and ended in a failing test.
Writing the fix took two. Nothing was delegated, because by the time the reproducer existed the
expensive work was done — which is also what made the *next* task delegable.

**The sweep.** Add the same schema-version assertion to all forty adapter tests. Bounded, tedious,
and `./gradlew test` says immediately whether each one is right. That went to the agent, and came
back with three of the forty asserting against the wrong field. The suite caught all three in under
a minute, which is the entire argument: the work was worth delegating because being wrong was cheap
to detect, not because it was large.

The honest part of the accounting is that nobody had noticed the previous month's rename costing
anything at all until the three tasks were written down next to each other.

## Failure mode

**The Errand That Became a Project.** You ask for a one-line change and get a diff across nine
files. None of it is wrong, exactly — the agent tidied two adjacent things, extracted a helper, and
updated a test that was already a bit odd — and none of it is what you asked for. Now the review is
the real task, and it is larger than the change you were going to make by hand. Reverting feels
wasteful because the extra work is genuinely fine, so it ships, and the repository acquires a
refactor nobody proposed.

The tell is a diff whose size bears no relation to the request. The second tell is the sentence you
find yourself writing in the pull-request description, where "and" appears twice and the change no
longer has a single name.

## Checklist

- [ ] The alternative was costed as typing plus review, not just as typing
- [ ] No deterministic tool — IDE refactoring, codemod, formatter — already does this exactly
- [ ] The specification was not the hard part, or it was written down first and then delegated
- [ ] A cheap check exists that says whether the result is wrong
- [ ] A single agent with the same token budget was tried before any fan-out
- [ ] No cost or duration estimate in the plan came from the agent
- [ ] The list of things not worth delegating carries a date and gets re-tested

**See also:** [*Decompose into subagents*](../orchestration/decompose-into-subagents.md) ·
[*Review code you did not write*](../verification-and-trust/review-code-you-did-not-write.md) ·
[*Match the model to the job*](match-the-model-to-the-job.md)
