# Match the model to the job

## Problem

You moved the nightly job down to the small tier because it is a third of the price, and the next
invoice was larger. The transcripts explain it without excusing it. The cheap model got to roughly
the same place by reading more files, asking more questions, and making three attempts where the
frontier tier made one. You are now in the worst position on offer. You pay more, you ship work you
trust less, and your table of per-token prices predicts neither.

## The play

Route on cost per accepted outcome, and settle it by measurement rather than by price list.

1. **Use the whole formula.** Cost per accepted outcome is the price per token, multiplied by the
   tokens consumed, multiplied by one over the rate at which the output is usable. A tier change
   moves the first factor by design and the other two by surprise.
2. **Tier down the fan-out, not the reasoning.** The vendors publish one split, and it is the only
   one the evidence supports. Small models take bounded subtasks with a cheap check at the end. The
   frontier tier takes planning, design, and anything where a wrong answer propagates. Surveys,
   inventories, and mechanical sweeps are the small tier's ground.
3. **Require a cheap oracle before tiering down.** If being wrong shows up as a compiler error, a
   failing test, or a diff short enough to scan, a cheap model's mistakes cost seconds. If the only
   detector is a human reading carefully, the saving has moved onto the verification tax. There it
   is larger, and nobody has a budget line for it.
4. **Measure turns in a paired run, not tokens per turn.** One controlled comparison has been
   published to date, in August 2026: ten merged pull requests, four models, and one shared review
   harness. A model around three times cheaper per token came out roughly three times more
   expensive per review. It took 156 turns where the baseline took 42. Take the mechanism seriously
   and the magnitude lightly: ten pull requests is thin against thirtyfold run-to-run variance.
5. **Match the effort to the job as well as the model.** A reasoning budget bills as output. At a
   five-times output multiple, thirty thousand thinking tokens cost what 150,000 input tokens do,
   per turn, before an answer is written. Dropping effort on routine work often saves more than
   dropping a tier, and it degrades more predictably.
6. **Do not compare per-token prices across model generations.** Tokenisers change. As of September
   2026, one vendor's current generation produced roughly 30% more tokens from the same text than
   its predecessor did. That is enough to turn an apparent third off the price into nearer an
   eighth. Compare cost per completed task instead.
7. **Re-run the comparison when the models change.** A routing table is assumptions about what the
   cheap tier cannot do yet, and those expire on the vendors' release schedule rather than yours.

Every factor in that formula except the price is a property of the task, and the task is what you
know about. So the durable rule is never "cheap model for code, expensive model for architecture".
It is "a tight specification with a cheap check tolerates a weaker model; deciding what to do does
not". The exchange rate is giving up one model for everything. You pay for a paired trial per class
of work, you pay again after each release, and some trials come back inconclusive because the
variance swallows the effect.

## Worked example

`granary`, a Kotlin service ingesting warehouse stock feeds from forty suppliers, ran two agent jobs
nightly. A *triage* pass read each overnight feed and classified any schema drift against the stored
contract. An *adapter* pass wrote the code change for whichever feeds had drifted. Both sat on the
frontier tier, because that was the tier they had been written on.

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

The comparison was a paired run, not a switch. The same twenty archived feeds were replayed from a
fixture directory on both tiers, five runs each, because single runs are noise. Each run recorded
turns, total tokens, and how many resulting diffs survived the contract suite unchanged.

```bash
$ ./gradlew :ingest:test --tests '*FeedContractTest'
```

Triage held. The input was bounded, the return shape was fixed, and the contract test was a cheap
oracle, so a wrong verdict cost one re-run. The small tier came out cheaper per night, with no
measurable difference in the verdicts themselves. The margin was noticeably smaller than the
per-token ratio had implied, because the small tier took more turns to reach the same verdicts.

The adapter pass did not hold. On three of the twenty feeds the small tier hit the turn ceiling
without producing a diff at all. That was the visible failure, and the cheap one. The expensive
failure was quieter. Two of the adapters it did produce passed the contract suite while reading the
schema version from the wrong field. The oracle `granary` had could catch a broken adapter, but not
a plausible one.

They kept the split and described it to themselves accurately, which was the part that took
discipline: the cheap tier now does the job where a test can tell it that it is wrong.

## Failure mode

**The Long Way Round.** The model is cheaper per token and the invoice is larger. It reaches the
same answer through three times as many turns, with more files read, more questions asked, and more
attempts discarded. Every one of those turns re-sends the conversation behind it. The per-token
saving is entirely real. It is applied to a much larger number of tokens, and the multiplication
happens where nobody is looking.

The tell is a bill that moved against a price change you made deliberately. The earlier tell, before
the invoice, is a turn count you never recorded. If you can state the old and new price per token,
but not the old and new turns per task, you have measured the one factor that was published and
none that moved.

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
