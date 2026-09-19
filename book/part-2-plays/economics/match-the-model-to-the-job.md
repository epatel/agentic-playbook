# Match the model to the job

## Problem

You moved the nightly job down to the small tier because the small tier is a third of the price,
and the next invoice was larger. The transcripts explain it without excusing it: the cheap model
got to roughly the same place by reading more files, asking more questions, and making three
attempts where the frontier tier made one. You are now in the worst position on offer — paying
more, shipping work you trust less, and holding a table of per-token prices that predicts neither
of those things.

## The play

Route on cost per accepted outcome, and settle it by measurement rather than by price list.

1. **Use the whole formula.** Cost per verified outcome is the price per token, multiplied by the
   tokens consumed, multiplied by one over the rate at which the output is usable. A tier change
   moves the first factor by design and the other two by surprise.
2. **Tier down the fan-out, not the reasoning.** The split the vendors publish, and the only one
   the evidence supports, is small models on bounded subtasks with a cheap check at the end, and
   the frontier tier on planning, design, and anything where a wrong answer propagates. Surveys,
   inventories, and mechanical sweeps are the small tier's ground.
3. **Require a cheap oracle before tiering down.** If being wrong shows up as a compiler error, a
   failing test, or a diff short enough to scan, a cheap model's mistakes cost seconds. If the only
   detector is a human reading carefully, the saving has moved onto the verification tax, where it
   is larger and where nobody has a budget line.
4. **Measure turns in a paired run, not tokens per turn.** In the one controlled comparison
   published to date — ten merged pull requests, four models, one shared review harness, August
   2026 — a model around three times cheaper per token came out roughly three times more expensive
   per review, because it took 156 turns where the baseline took 42. Take the mechanism seriously
   and the magnitude lightly: ten pull requests is thin against thirtyfold run-to-run variance.
5. **Match the effort to the job as well as the model.** A reasoning budget bills as output, so
   thirty thousand thinking tokens cost what 150,000 input tokens do at a five-times output
   multiple — per turn, before an answer is written. Dropping effort on routine work is often a
   larger saving than dropping a tier, and it degrades more predictably.
6. **Do not compare per-token prices across model generations.** Tokenisers change: one vendor's
   recent generation produces roughly 30% more tokens from the same text than its predecessor did,
   enough to turn an apparent third off the price into nearer an eighth. Compare cost per completed
   task instead.
7. **Re-run the comparison when the models change.** A routing table is assumptions about what the
   cheap tier cannot do yet, and those expire on the vendors' release schedule rather than yours.

Every factor in that formula except the price is a property of the task, which is the thing you
know about. That is why the durable rule is never "cheap model for code, expensive model for
architecture" but "a tight specification with a cheap check tolerates a weaker model; deciding what
to do does not" — a distinction that survives a release, which a table of model names does not. The
exchange rate is that you give up one model for everything: you pay for a paired trial per class of
work, you pay again after each release, and some of those trials come back inconclusive because the
variance swallows the effect.

## Worked example

`granary`, a Kotlin service ingesting warehouse stock feeds from forty suppliers, ran two agent
jobs nightly. A *triage* pass read each overnight feed and classified any schema drift against the
stored contract; an *adapter* pass wrote the code change for whichever feeds had drifted. Both sat
on the frontier tier, because that was the tier they had been written on.

Routing the triage pass down was one line of configuration in the subagent definition:

```markdown
---
name: feed-triage
description: Classifies overnight schema drift for one supplier feed against its stored
  contract. Use nightly, one invocation per feed. Returns a verdict table only.
tools: Read, Glob, Grep
model: haiku
---
```

The comparison was a paired run rather than a switch: the same twenty archived feeds replayed from
a fixture directory, both tiers, five runs each because single runs are noise, recording turns,
total tokens, and how many resulting diffs survived the contract suite unchanged.

```bash
$ ./gradlew :ingest:test --tests '*FeedContractTest'
```

Triage held. The input was bounded, the return shape was fixed, and the contract test was a cheap
oracle, so a wrong verdict cost one re-run. The small tier came out cheaper per night — by a margin
noticeably smaller than the per-token ratio had implied, because it took more turns to reach the
same verdicts — with no difference anyone could measure in the verdicts themselves.

The adapter pass did not hold. On three of the twenty feeds the small tier hit the turn ceiling
without producing a diff at all, which is the visible failure and the cheap one. The expensive
failure was quieter: two of the diffs it did produce passed the contract suite while asserting the
schema version against the wrong field, because the oracle `granary` had was good enough to catch a
broken adapter and not good enough to catch a plausible one.

They kept the split, and described it to themselves accurately, which is the part that took the
discipline: the cheap tier now does the job where a test can tell it that it is wrong.

## Failure mode

**The Long Way Round.** The model is cheaper per token and the invoice is larger, because it
arrives at the same answer through three times as many turns — more files read, more questions
asked, more attempts discarded — and every one of those turns re-sends the conversation behind it.
The per-token saving is entirely real. It is being applied to a much larger number of tokens,
and the multiplication happens somewhere nobody is looking.

The tell is a bill that moved in the opposite direction to a price change you made deliberately.
The earlier tell, available before the invoice, is a turn count you never recorded: if you can
state the old and new price per token but not the old and new turns per task, you have measured
the one factor that was published and none of the ones that moved.

## Checklist

- [ ] The tier decision is stated as cost per accepted outcome, not cost per token
- [ ] Each downgraded task has a named cheap oracle that catches a wrong answer
- [ ] Turns per task are recorded for both tiers, not just tokens
- [ ] The comparison ran on the same inputs, repeated enough times to see past variance
- [ ] Reasoning effort was set per class of work alongside the tier
- [ ] No claim in the decision compares per-token prices across model generations
- [ ] The routing table carries a date and a trigger to re-measure

**See also:** [*Decompose into subagents*](../orchestration/decompose-into-subagents.md) ·
[*Make the agent prove it*](../verification-and-trust/make-the-agent-prove-it.md) ·
[*Understand what you are paying for*](understand-what-you-are-paying-for.md)
