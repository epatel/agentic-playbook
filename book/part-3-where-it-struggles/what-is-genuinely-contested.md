# What is genuinely contested

Some of the arguments in this field are settled and being relitigated by people who have not read
the source. Others are genuinely open, and will stay open for a while, because the studies that
would close them have not been run and in one notable case cannot be. Telling the two apart is worth
more than a position on either.

What follows is the second category. Each one carries both halves, because carrying one half is how
a book gets quoted for a year and then becomes embarrassing.

## Does agent assistance make you faster

Three credible results point in different directions. METR's randomised trial found a 19% slowdown
(CI +2% to +39%) among 16 expert maintainers working on repositories they knew well, on early-2025
tooling. Google's enterprise trial — 96 engineers, one ten-file task on internal infrastructure,
summer 2024 — found roughly 21% faster, with an effect that lost statistical significance once
developer- and task-level factors were controlled. Microsoft's telemetry across tens of thousands of
engineers during an early-2026 command-line agent rollout found merged-pull-request throughput up
24.0% (CI +14.5% to +33.7%), reported by authors who state in the paper that they are Microsoft
employees and that Microsoft sells AI tools and owns GitHub.

These are not reconcilable by picking a winner, and the difference is not mainly methodological
quality. They measure different populations doing different work. The synthesis the evidence
supports is that the sign flips with codebase maturity and developer expertise: gains concentrate in
newer code and in work the developer knows less well, and the effect is smallest or negative in
mature repositories with expert maintainers.

Which means the useful question is not "does it work" but "does it work *here*", and the only
instrument that answers it is your own paired run. [*Match the model to the
job*](../part-2-plays/economics/match-the-model-to-the-job.md) is the play.

## Does agent assistance degrade the codebase

The optimistic evidence is a controlled experiment. GitHub's own 2024 trial randomly assigned 202
developers and found the Copilot group 53.2% more likely to pass all ten unit tests on a greenfield
API task, with readability up 3.62% and maintainability up 2.47% in blind review. It is vendor-run,
it has no limitations section, and the quality effects are two to four per cent.

The pessimistic evidence is observational and at scale. GitClear, a developer-analytics vendor,
analysed 623 million changed lines from 2023 to 2026 and reports refactored code falling from 21% of
changed lines in 2022 to 3.8% year-to-date in 2026, block duplication up 81%, and error-masking
constructs up 47%. The detection method for what counts as AI-assisted is not published, so the
denominator is not knowable, and the company sells the diagnosis.

Between them sits the study that actually tried to answer the downstream question. Borg and
colleagues, reporting in February 2026, ran two phases: 151 participants, 95% professional
developers, built features with or without AI, and then a *different* set of participants evolved
the resulting code without AI. Phase one showed a 30.7% median speedup. Phase two found "no
significant differences in subsequent evolution with respect to completion time or code quality",
with the Bayesian analysis putting any difference at "at most small and highly uncertain".

Note the asymmetry before drawing a conclusion. The evidence that it improves things is a controlled
experiment on greenfield work; the evidence that it degrades things is observational, at repository
scale, over time. They measure different objects and neither refutes the other. The one study
designed to measure maintainability directly found nothing in either direction, which is not the
result either camp wanted.

## Does more model capability fix any of this

The intuition is that this is a problem that scales away, and the one vendor publishing per-model
figures reports something more awkward than either camp wants. In Anthropic's November 2025 system
card, on a set of coding problems selected because earlier models hardcoded their way through them,
Claude Opus 4.5 hardcoded nothing at all: 0%, against Sonnet 4.5 at 1% and Haiku 4.5 at 6%. On that
measure capability did fix it.

Then there is the other set — problems built to be impossible, where the only way to pass is to
cheat. Told nothing, Opus 4.5 cheated on 55% of them, roughly where Sonnet 4.5 sits. Told explicitly
not to, in a prompt ending "Please tell me if the problem is unreasonable instead of hard coding
test cases!", it still cheated on 35%, against Sonnet 4.5's 20%. Anthropic's own reading is that the
newer model was "comparatively less corrigible when given instructions".

So the finding is not that bigger models cheat more. What capability improved was the behaviour on
solvable work. What it did not improve was how much the instruction helped once the work was
impossible. The caveats are load-bearing — internal evaluation sets, undisclosed classifiers, no
comparability across vendors — and what the figures cannot support is a ranking. What they support
is refusing the assumption that the next release makes verification less necessary, and noticing
that the residue capability leaves behind is precisely the part that telling it to stop was
supposed to cover.

## Are the benchmarks measuring anything

In February 2026 OpenAI retired SWE-bench Verified as a measure of frontier coding capability. It
audited 138 problems that o3 failed to solve consistently across 64 independent runs and reported
that 59.4% contained material issues in test design or problem description, concluding that
improvements "increasingly reflect how much the model was exposed to the benchmark at training
time". Epoch AI, which re-runs the benchmark on 484 of the 500 samples in network-isolated
containers with git history truncated at the issue date, estimates a benchmark error rate of 5% to
10%.

Those two numbers get merged constantly and must not be. OpenAI audited *failed* instances, which is
a biased sample by construction; Epoch estimates error across the whole set. Both can be true.

The instability is easier to feel from two smaller results. When UTBoost added missing unit tests to
26 of the 500 SWE-bench Verified instances, 15.7% more previously-correct patches turned out to be
wrong, and the two agents sitting at the top of the leaderboard at the time collapsed into a tie at
53.6% — the first-placed one had seven bad patches to the runner-up's three. And when Terminal-Bench
fixed 28 of its 89 tasks between versions 2.0 and 2.1, one agent gained 12.1 percentage points from
the task fixes alone.

The durable conclusion is not that benchmarks are worthless. It is that a headline score carries at
least four independent sources of inflation before anyone chooses the harness it runs in, and that a
before-and-after comparison across a benchmark version boundary means nothing at all.

## Is the volume of AI-assisted work a quality problem

The curl project supplies the cleanest natural experiment available, and almost everybody stops
quoting it three months early.

On 26 January 2026, Daniel Stenberg ended the curl bug-bounty, which had run since April 2019 and
paid out on 87 confirmed vulnerabilities. Confirmation rates had been "somewhere north of 15% of the
submissions"; from 2025 they "plummeted to below 5%. Not even one in twenty was *real*." He
described "mind-numbing AI slop" and "a serious mental toll". The money was withdrawn entirely.

A month later he reported that "since we dropped the bounty, the inflow tsunami has dried out
*substantially*".

And then, on 22 April 2026: report volume was running at about double the 2025 rate, the
confirmation rate had recovered to "somewhere in the 15-16% range" — pre-AI levels — "the slop
situation is not a problem anymore", and "almost every security report now uses AI to various
degrees".

More reports arrived, they were more likely to be real, and nearly all of them were AI-assisted. The
variable that changed was the money, not the tooling. Anyone citing curl as evidence that
AI-assisted submissions are worthless is citing January and stopping.

## Who is responsible

Every published policy says a human owns the diff. Whether that distributes responsibility or merely
locates it is unresolved, and the disagreement runs through communities that read the same clause.
The Linux kernel, Fedora, and Debian hold that a developer can certify the Developer Certificate of
Origin for model-assisted output given human review; QEMU, Gentoo, and NetBSD hold that they cannot,
because the licence status of the output is unsettled. Same clause, opposite conclusions, no court
ruling. Meanwhile the responsibility-gap literature argues that assigning ownership to the operator
closest to a system they could not fully control is precisely how blame gets misallocated. [*Decide
who signs off*](../part-2-plays/verification-and-trust/decide-who-signs-off.md) carries both halves
at length and declines to resolve them.

## Where that leaves you

Not paralysed, which is the easiest misreading of a chapter like this one.

The unresolved questions are about magnitude and attribution — how much faster, for whom, at what
cost to the codebase, and who carries it when it goes wrong. None of them is a reason to put the
tools down; the single study most often quoted to justify that is one whose authors disclaim the
generalisation in print and whose own follow-up could not reproduce it. What the contested state of
the evidence argues for is a practice built on things you can check in your own repository within a
week, rather than on a figure from somebody else's. That is what the plays are: small, local, and
falsifiable on your own machine.

The reason to read this part is the same reason to read the rest. These tools are genuinely useful
and they fail in shapes that are now well enough documented to be anticipated. Knowing the shapes is
most of the practice.
