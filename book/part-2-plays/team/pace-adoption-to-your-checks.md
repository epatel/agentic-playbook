# Pace adoption to your checks

## Problem

The pilot went well: two engineers, one month, a visible speed-up. So the licence went to all nine,
the agent got write access to the CI configuration, and the operations lead asked whether their team
could make its own template changes. Each step was approved because the last one looked fine. Two
months later the review queue is the bottleneck, the adapters are harder to change than they were in
spring, and the speed-up is gone. Nobody decided to move that fast. The team spent the gain before
the bill arrived, and kept the bill.

## The play

Widen adoption only when the check that makes the next step safe already holds, and write that check
down before anyone asks to take the step.

1. **Place each area of the codebase, not the team.** Ask where its knowledge lives and what
   enforces it. Four levels cover most teams: the context lives in people's prompts; it lives in the
   repository and the agent runs the tests itself; structure is measured on every change; and checks
   adjudicate a change without a developer reading it. Different areas sit at different levels, and
   the oldest code is usually lowest.
2. **Write the exit check for each level as a condition you can look at.** Leaving the first: the
   agent file is verified loaded, and the run executes the suite before it reports ([*Make the agent
   prove it*](../verification-and-trust/make-the-agent-prove-it.md)). Leaving the second: a
   structural delta runs on every change, and touched files have held their health for a month
   ([*Hold the structure, not just the
   behaviour*](../verification-and-trust/hold-the-structure-not-just-the-behaviour.md)). Leaving
   the third: one change on a narrow surface has merged on its checks and a named sign-off.
3. **Keep trust and scale on separate dials.** Trust is what an agent or a colleague may change
   without a developer reading it, and it advances by level. Scale is how many people and runs feed
   the review queue, and review capacity caps it at every level.
4. **Turn one dial at a time, and date the turn in the working agreement.** One change per interval
   is the only way to know which one broke something.
5. **Judge a turn after two months, not two weeks.** Compare review time and touched-file health
   before and after. The speed-up shows in the first month and the cost arrives later.
6. **Turn back when a check stops holding.** Withdraw the autonomy the way you would roll back a
   deploy: as routine, recorded, and nobody's verdict on the person who asked for it.

The two-month horizon is measured. A 2026 study of 806 open-source projects that adopted Cursor in
2024 and early 2025 found the speed-up gone after two months, and code complexity up 41.6% and
staying up ([`code-health.md`](../../../notes/research/code-health.md)). The order of the levels is
not measured. It is this book's synthesis, argued from mechanism: each level supplies the check the
next one stands on, so skipping one means trusting a check that does not exist yet. Pacing works
because it turns adoption into a series of small, attributable bets instead of one large unexamined
one. The exchange rate is speed you could have had: a quarter of watching another team move faster,
and some steps you would have got away with.

## Worked example

`lodestone`, a claims-processing platform with C# services behind a TypeScript front end, had nine
engineers and two requests on the table. The engineers wanted agents writing new insurer adapters
with lighter review. Claims operations wanted to edit the letter templates sent to policyholders
themselves, through an agent session of their own.

Placing the areas took one meeting. The adapters had an agent file, a fast suite the agent ran
itself, and nothing that measured structure. The templates had an agent file and no check at all:
nothing rendered a template before it reached a customer. The team wrote both exit checks into the
working agreement, dated, with an owner each.

So the adapter request waited for a structural delta in CI, which took a week. The template request
waited for a preview check that rendered every changed template against fixture claims and failed
on a missing field. That took five weeks, and operations made its first template change in the
sixth, merged on the preview and one engineer's sign-off.

The month-two review was less tidy. Touched-file health had fallen in two adapters, both written
under the lighter review. The team turned that dial back for adapters only, and kept it. And during
the five weeks the template request waited, operations had kept a spreadsheet of corrected wording
outside the repository, which nobody reviewed and from which two letters went out. Pacing has a
queue, and people route around a queue.

## Failure mode

**The Borrowed Velocity.** Every widening is justified by the speed-up from the last one, and the
speed-up is real. What it borrows against arrives later: review load from more people feeding the
queue, and complexity from code nobody's checks measured. By the time the repayments show, three
more widenings rest on the first, and turning one back looks like admitting the whole programme
failed.

The tell is a run of widenings dated less than two months apart, a review queue that grows faster
than the team, and touched-file health falling while the project score holds steady. The check that
settles it is to list the last three widenings beside the check each one was supposed to wait for.

## Checklist

- [ ] Each area of the codebase is placed at a level, in writing
- [ ] Every level has an exit check that is true or false when you look
- [ ] Trust and scale are recorded as separate decisions
- [ ] Each widening is dated in the working agreement, one per interval
- [ ] Each widening was judged at two months against review time and touched-file health
- [ ] A turned-back widening is recorded as routine, with its reason

**See also:** [*Build the working agreement*](build-the-working-agreement.md) ·
[*Hold the structure, not just the
behaviour*](../verification-and-trust/hold-the-structure-not-just-the-behaviour.md) ·
[*Inviting non-developers in*](../../part-4-next-waves/inviting-non-developers-in.md)
