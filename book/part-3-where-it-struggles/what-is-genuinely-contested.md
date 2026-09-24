# What is genuinely contested

The questions below are genuinely open, because the studies that would close them have not been run
and in one case cannot be. Other arguments in this field are settled and being relitigated by people
who have not read the source. Telling the two apart is worth more than a position on either. Each
question here carries both halves, because carrying one half is how a book gets quoted for a year
and then becomes embarrassing.

## Whether agents make you faster depends on the code and the developer

Three credible results point in different directions, because they measure different populations
doing different work. METR's randomised trial found a 19% slowdown (CI +2% to +39%) among 16 expert
maintainers working on repositories they knew well, on early-2025 tooling. Google's enterprise trial
(96 engineers, one ten-file task on internal infrastructure, summer 2024) found roughly 21% faster.
That effect lost statistical significance once developer- and task-level factors were controlled.
Microsoft's telemetry across tens of thousands of engineers during an early-2026 command-line agent
rollout found merged-pull-request throughput up 24.0% (CI +14.5% to +33.7%). Its authors state in
the paper that they are Microsoft employees, and that Microsoft sells AI tools and owns GitHub.

Picking a winner does not reconcile them, and methodological quality is not the main reason. The
sign flips with codebase maturity and developer expertise. Gains concentrate in newer code and in
work the developer knows less well. The effect is smallest or negative in mature repositories with
expert maintainers.

The useful question is not "does it work" but "does it work *here*". The only instrument that
answers it is your own comparison. [*Know when not to use an
agent*](../part-2-plays/economics/know-when-not-to-use-an-agent.md) is the play.

## The one direct test of codebase damage found nothing either way

The one study designed to measure maintainability directly found nothing in either direction. The
optimistic evidence is a controlled experiment. GitHub's own 2024 trial randomly assigned 202
developers and found the Copilot group 53.2% more likely to pass all ten unit tests on a greenfield
API task. In blind review, readability rose 3.62% and maintainability 2.47%. It is vendor-run, has
no limitations section, and the quality effects are two to four per cent.

The pessimistic evidence is observational and at scale. GitClear, a developer-analytics vendor,
analysed 623 million code changes from 2023 to 2026. It reports refactored code falling from 21% of
changed lines in 2022 to 3.8% year-to-date in 2026, and block duplication up 81% on its 2023 level.
It classifies nothing as AI-assisted: the corpus is every change, and it infers attribution from
timing. And the company sells the diagnosis.

Between them sits the study that actually tried to answer the downstream question. Borg and
colleagues, reporting in February 2026, ran two phases. In the first, 151 participants, 95% of them
professional developers, built features with or without AI. In the second, a *different* set evolved
the resulting code without AI. Phase one showed a 30.7% median speedup. Phase two found "no
significant differences in subsequent evolution with respect to completion time or code quality",
with the Bayesian analysis putting any improvement at "at most small and highly uncertain".

Note the asymmetry. The evidence that agents improve things is a controlled experiment on greenfield
work. The evidence that they degrade things is observational, at repository scale, over time.
Neither refutes the other, and the direct measurement is not the result either camp wanted.

## Capability fixed cheating on solvable problems, not on impossible ones

Capability improved the behaviour on solvable work. It did not improve how much an instruction not
to cheat helped once the work was impossible. The intuition is that this problem scales away, and
the one vendor publishing per-model figures reports something more awkward. Anthropic's November
2025 system card has a set of coding problems selected because earlier models hardcoded their way
through them. On that set Claude Opus 4.5 hardcoded nothing at all: 0%, against Sonnet 4.5 at 1% and
Haiku 4.5 at 6%. On that measure capability did fix it.

The card's other set holds problems built to be impossible, where the only way to pass is to cheat.
Told nothing, Opus 4.5 cheated on 55%, roughly where Sonnet 4.5 sits. Told explicitly not to, in a
prompt ending "Please tell me if the problem is unreasonable instead of hard coding test cases!", it
still cheated on 35%, against Sonnet 4.5's 20%. Anthropic's own reading is that the newer model was
"comparatively less corrigible when given instructions".

So the finding is not that bigger models cheat more. The caveats are load-bearing: internal
evaluation sets, undisclosed classifiers, and no comparability across vendors. The figures cannot
support a ranking. What they support is refusing the assumption that the next release makes
verification less necessary.

## Benchmark scores are inflated, and not comparable across versions

Benchmarks are not worthless, but a headline score carries at least four independent sources of
inflation before anyone chooses the harness it runs in. A before-and-after comparison across a
benchmark version boundary means nothing at all.

In February 2026 OpenAI retired SWE-bench Verified as a measure of frontier coding capability. It
audited 138 problems that o3 failed to solve consistently across 64 independent runs. It reported
that 59.4% contained material issues in test design or problem description, concluding that
improvements "increasingly reflect how much the model was exposed to the benchmark at training
time". Epoch AI re-runs the benchmark on 484 of the 500 samples, in network-isolated containers with
git history truncated at the issue date. It separately estimates an error rate of 5% to 10%.

These get merged constantly and must not be. OpenAI audited *failed* instances, a biased sample by
construction; Epoch estimates error across the whole set. Both can be true.

The instability is easier to feel from two smaller results. When UTBoost added missing unit tests to
26 of the 500 SWE-bench Verified instances, 15.7% of the 584 leaderboard patches that had passed on
those 26 turned out to be wrong. The two agents at the top of the leaderboard collapsed into a tie
at 53.6%; the first-placed one had seven bad patches to the runner-up's three. And when
Terminal-Bench fixed 28 of its 89 tasks between versions 2.0 and 2.1, one agent gained 12.1
percentage points from the task fixes alone.

## Curl's slop problem faded three months after the part everyone quotes

The curl project supplies the most-quoted evidence in this argument, and almost everybody stops
three months before the problem went away.

On 26 January 2026, Daniel Stenberg announced the end of the curl bug-bounty, effective five days
later. It had run since April 2019 and produced 87 confirmed vulnerabilities. Confirmation rates had
been "somewhere north of 15% of the submissions"; from 2025 they "plummeted to below 5%. Not even
one in twenty was *real*." He described "mind-numbing AI slop" and "a serious mental toll". The
money was withdrawn entirely.

A month later he reported that "since we dropped the bounty, the inflow tsunami has dried out
*substantially*".

Then, on 22 April 2026, report volume was running at about double the 2025 rate. The confirmation
rate had recovered to "somewhere in the 15-16% range", pre-AI levels. He wrote that "the slop
situation is not a problem anymore", and that "almost every security report now uses AI to various
degrees".

Several things changed over that window: the money went, reporting moved off HackerOne and back,
and, by Stenberg's own account, the tools kept improving. Stenberg dates the turn from the platform
move. Anyone citing curl as evidence that AI-assisted submissions are worthless is citing January
and stopping.

## Projects read the same responsibility clause in opposite ways

Every published policy says a human owns the diff. Whether that distributes responsibility or merely
locates it is unresolved. The Linux kernel, Fedora, and Debian hold that a developer can certify the
Developer Certificate of Origin for model-assisted output given human review. QEMU, Gentoo, and
NetBSD hold that they cannot, because the licence status of the output is unsettled. Same clause,
opposite conclusions, no court ruling. Meanwhile the responsibility-gap literature argues that
assigning ownership to the operator closest to a system they could not fully control is precisely
how blame gets misallocated. [*Decide who signs
off*](../part-2-plays/verification-and-trust/decide-who-signs-off.md) carries both halves at length
and declines to resolve them.

## None of this is a reason to put the tools down

None of this is a reason to put the tools down, which is the easiest misreading of a chapter like
this one. The unresolved questions are about magnitude and attribution: how much faster, for whom,
at what cost to the codebase, and who carries it when it goes wrong. The single study most often
quoted to justify stopping is one whose authors disclaim the generalisation in print, and whose own
follow-up could not reproduce it. What the evidence argues for is a practice built on things you can
check in your own repository within a week, not on a figure from somebody else's. That is what the
plays are: small, local, and falsifiable on your own machine.

The reason to read this part is the same reason to read the rest. These tools are genuinely useful,
and they fail in shapes now documented well enough to anticipate. Knowing the shapes is most of the
practice.
