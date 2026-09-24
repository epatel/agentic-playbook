# Where the time actually goes

The hour an agent saves you on typing relocates rather than disappearing, with reasonable
consistency across everything measured so far. Much of it moves into review. The promise is that
typing gets cheaper, and it does. Knowing where the hour lands separates a practice that captures
the gain from one that files it under "we are definitely faster" while the pull request queue
quietly doubles.

## The one timed trial found developers slower, and sure they were faster

One study has screen recordings. METR ran a randomised controlled trial in early 2025: 16
experienced open-source developers and 246 real tasks. The repositories averaged over a million
lines and a decade of history, and the developers averaged five years and some 1,500 commits of
prior work on them. Each task was randomly assigned to allow or disallow AI. Allowing AI increased
completion time by 19%, with a confidence interval of +2% to +39%.

That number is the most over-cited figure in the field, and it needs its qualifiers attached
permanently. It measured Cursor Pro with Claude 3.5 and 3.7, February to June 2025, in mature
repositories with expert maintainers: two model generations ago. METR redesigned the study and
reported again in February 2026: −18% for the returning cohort (CI −38% to +9%) and −4% for newly
recruited developers (CI −15% to +9%), both straddling zero. METR's own verdict on that data is that
it is "only very weak evidence" and "an unreliable signal of the current productivity effect of AI
tools".

Why the follow-up could not settle it is the most interesting result of the whole exercise. METR
abandoned the design because "30% to 50% of developers told us that they were choosing not to submit
some tasks because they did not want to do them without AI". By 2026 the control arm had become
something people would not agree to do. Much of this book's hedging traces back to that sentence.

What survives is the time-allocation data, which is descriptive rather than causal and does not
depend on the headline. With AI allowed, developers spent less time writing code and less time
reading and searching, and more time prompting, waiting, and reviewing. Waiting accounted for
roughly 4% of time; reviewing and cleaning output, roughly 9% of issue completion time. Fewer than
44% of generations were accepted. Every developer in the study modified the code they kept, 56%
reported often needing major cleanup to meet their own standards, and 75% read every line.

The perception gap is the part worth carrying into your next estimate. The same developers forecast
a 24% speedup before starting, and afterwards believed they had been sped up by 20%. Economics and
machine-learning experts asked to predict the result said 39% and 38% faster. Everybody was wrong in
the same direction, including the people holding the keyboard.

## At team scale, the saved time turns into review

At team scale, throughput rose and the time moved into review. The largest study of a deliberate
agentic push is a longitudinal panel of 802 developers and 196,212 pull requests. It ran January
2024 to April 2026, at an AI-forward company that set an explicit doubling mandate. [*Know when not
to use an agent*](../part-2-plays/economics/know-when-not-to-use-an-agent.md) uses its headline
result as a closing argument. Its interior holds the time accounting.

Per-capita throughput reached 2.09× baseline. Within a given developer, holding the composition of
the team fixed, the gain was 1.46× to 1.72× depending on specification, rising to 1.99× after nine
months on the tool. The gap between those figures is the difference between what the organisation
measured and what any individual experienced. It is the number most likely to be missing from
whatever slide you were shown.

The gains were uneven, too. Management tier gained 86%. Individual contributors through Principal
gained 27% to 42%, statistically indistinguishable from one another. Repositories created in 2022 or
later gained 44%. Legacy code gained 12%, and that result was not statistically significant. DORA's
2026 ROI report relays a Stanford estimate with the same shape: 35–40% on simple, greenfield work
against 10% or less on complex legacy. The report prints no methodology behind it.

Meanwhile, review changed character. By April 2026, human review coverage had fallen from 89% of
pull requests to 68%, and the load on each remaining reviewer had doubled. Automated review rose
from about 19% to about 84% and overtook human review outright. Agent-authored pull requests spent
about 20% longer between first human review and merge than comparable human ones, and 22% longer end
to end. Merge rates stayed essentially flat and revert rates declined slightly. That is the detail
that catches teams out: the quality signal everyone watches is the one that does not move.

The authors' own summary does the hedging for you. The result is "evidence that a near-doubling is
attainable under favorable conditions and over a long enough horizon, not that it is typical,
immediate, or free". The study did not randomise adoption. Throughput here is an activity count. A
parallel study at Microsoft notes in its own limitations that merged pull requests "are an imperfect
proxy for throughput and reward small, frequent PRs".

## Checking takes back the time saved on writing

The effort saved on writing is respent on checking. DORA's 2026 report models a J-curve: a temporary
dip before teams capture value, with three named causes. One is the learning curve, one is pipeline
adaptation, and one is the *verification tax*: the time developers spend checking AI output. [*The
four areas, re-weighted*](../part-1-argument/the-four-areas-reweighted.md) adopts that term, and the
[*Economics*](../part-2-plays/economics/index.md) and [*Verification and
trust*](../part-2-plays/verification-and-trust/index.md) suites use it. It is the right frame
precisely because it is not a bug tax. Across three independent studies the pattern holds: output
up, defect signals flat, review coverage down, cycle time up.

```mermaid
graph LR
    A["Effort saved<br/>on writing"] -->|"relocates to"| B["Effort spent<br/>on review"]
    B --> C["Diff per week grows<br/>faster than reviewers"]
    C --> D["Cycle time rises"]
    E["Merge rate<br/>Revert rate<br/>Defect count"]
    B -.->|"leaves no trace in"| E
    classDef flat stroke-dasharray: 4 3
    class E flat
```

Two things follow for planning. The saving is real and lands on the person writing. The cost lands
on the person reviewing, who is frequently somebody else and is not in the room when the estimate is
given. And review capacity, not model capability, is the resource a team runs out of first. If you
are choosing what to buy with the time an agent gives you, buying review is rarely the exciting
option and is usually the correct one.

## The confident claims sit in four unmeasured gaps

The confident claims come from the gaps in the evidence, and there are four.

There is no randomised controlled trial of agentic coding. Every trial in the literature measures
autocomplete, inline completion, or chat. The genuinely agentic evidence is telemetry and
quasi-experiments, none of it randomised. Two of the three largest studies are authored by people
with an employer or commercial stake.

Total cost of ownership has never been cleanly measured. Every study measures an activity (merged
pull requests, task completion time, commits), and the authors of the two largest say so in their
own papers. No published study follows the full path from prompt to production incident.

The third and biggest hole sits directly under this book's central recommendation: there is no
controlled study of what reviewers miss in agent-authored code. Nobody has seeded known defects into
agent pull requests and measured detection rate against human-authored ones. The automation-bias
literature that gets cited in its place comes from aviation and clinical decision support.
Transferring it is a reasonable argument, and it is an argument rather than a citation.

The fourth: nothing published measures whether a team with an explicit working agreement outperforms
one without. The [*Team*](../part-2-plays/team/index.md) suite is built on mechanisms that make
things checkable rather than on effect sizes, for exactly that reason.
