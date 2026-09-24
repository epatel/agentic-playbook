# What agents are reliably bad at

Agents are reliably bad at five things: finishing long tasks, getting unfamiliar code right,
security that depends on where data goes, extending their own work, and telling a goal from its
measurement. Every tool sold to developers arrives with a list of what it is good at and a silence
where the other list should be. This part is the other list. It is shorter than the sceptics claim
and longer than the release notes imply. None of it is a reason to stop: every play in this book
assumes you use these tools every day and intend to keep doing so. But a practice built on the
marketing version of the capability will be built in the wrong shape.

Almost nothing published about "AI coding productivity" is about agents. Every randomised trial in
the field measures autocomplete, inline completion, or chat. What follows draws on benchmark
results, vendor measurements that say so, and studies with stated sample sizes. Where a figure is
vendor-reported, the sentence says so. The full accounting, including the forty-odd widely-quoted
numbers that did not survive checking, is in
[`notes/research/evidence.md`](../../notes/research/evidence.md).

## Agents get most of the way, then run out of time

Agents get most of the way through long tasks and rarely finish. On Long-Horizon-Terminal-Bench, the
best of fifteen frontier models cleared the 0.95 reward threshold on 15.2% of tasks, and the mean
across all fifteen was 4.3%. That was the benchmark's first version, July 2026: 46 tasks across nine
categories, each averaging 231 episodes, 9.9 million tokens, and 85 minutes of wall clock. Tighten
the threshold to full completion and ten of the fifteen score zero. Near-misses outnumbered passes
73 to 30. And 79% of unresolved runs ended because the ninety-minute budget expired, not because the
agent hit something it could not do.

The authors read the bottleneck as long-horizon completion rather than local reasoning. That is a
polite way of saying almost nothing in those runs was beyond the model, and the runs still did not
finish. You know the small version from your own week: the run that ends at ninety per cent, the
continuation that also ends at ninety per cent, and no turn that presents itself as the one to stop
on. [*Scope a task to fit the window*](../part-2-plays/context/scope-a-task-to-fit-the-window.md)
names that as the Permanent Near Miss and gives it a stop rule.

## Scores on public code overstate what an agent does on yours

On private code, the same agent resolves a fraction of what it resolves on public code. SWE-Bench
Pro splits its problems into a public set from open repositories and a commercial set from eighteen
proprietary startup repositories. In the November 2025 version of that paper, Claude Sonnet 4
resolved 42.7% of the public set and 9.1% of the commercial set. Same harness, same evaluation.

The likeliest explanation is not that private code is harder in some deep sense. It is that public
code has been read. In 2025 contamination work, models identified the buggy file in a SWE-bench
repository from the issue text alone, with no repository structure in the prompt. They did so at up
to 76% accuracy, against up to 53% on repositories outside the benchmark. A separate 2024 audit
found 32.67% of successful patches involving solution leakage, with the fix stated in the issue
report or its comments. Your repository is the commercial set.

The failures are the Confident Wrong Rewrite, described in [*The failure modes worth
naming*](the-failure-modes-worth-naming.md). The short version is that they compile.

## Generated code got more correct and no more secure

Models got substantially better at writing code that works and no better at code that is safe.
Veracode's longitudinal study reports two years of model releases moving the security pass rate
"from approximately 55% to… approximately 55%", while syntactic correctness climbed past 95%. By the
spring 2026 edition it covered over 150 models and 80 tasks, built against four MITRE weakness
classes in four languages. It is vendor-reported, and the flatness rather than the level is the
durable finding.

The gap is uneven, which is what you can act on. In that edition, generated code passed 82% of
SQL-injection tasks and 86% of insecure-cryptography tasks, against 15% of cross-site scripting and
13% of log injection. By language, Python passed 62% and Java 29%.

The pattern is legible. Models are reliable where the fix is a canonical call at the site of the
defect: a parameterised query, a named cipher, a library everyone uses the same way. They are
unreliable where correctness depends on where the value ends up. Output encoding is a property of
the destination, and the destination is usually not in the window. Review agent-written code
accordingly: watch the paths where data leaves, not the lines where it arrives.

## Code an agent keeps extending gets worse on every pass

Agents make their own code steadily worse, one passing step at a time. SlopCodeBench, March 2026,
measures what other benchmarks do not: 93 checkpoints on 20 problems, 11 models in 25
configurations. No agent solved any problem end to end. The highest checkpoint solve rate was 17.2%.
Cost grew 2.9× across a *trajectory*, one agent's full sequence of attempts at a problem, with no
matching improvement.

The code metrics say more than the score. Verbosity grew in 89.8% of trajectories and complexity
concentration in 80%. Against a panel of 48 maintained human repositories, agent checkpoints
averaged 2.2× the verbosity and more than twice the complexity concentration, 0.68 against 0.31. The
mean count of high-complexity functions rose from 4.1 to 37.0 across a trajectory. In one, a
dispatcher grew tenfold in cyclomatic complexity, while nine branches repeated the same
argument-parsing code rather than extracting it.

The control group is the finding. Human repositories hold those metrics flat over time. Agent
trajectories deteriorate on every pass, and no individual pass fails. That is the Endless Polish,
and what to do about it is in [*The failure modes worth naming*](the-failure-modes-worth-naming.md).

## A model rewarded by a grader learns to satisfy the grader

The sharpest published result here is not about capability at all: a model rewarded by a grader
learned to satisfy the grader. In November 2025 Anthropic and Redwood Research described training a
model with reinforcement learning on real production coding environments. The reward was the obvious
one: run the grading script, and if it exits zero the task is solved.

The model worked out that it did not have to make the code work. It had to make the script exit
zero. So it called `sys.exit(0)` in Python, breaking out of the test harness with a zero exit status
before the assertions ran. The grader recorded a pass. The reward was paid. The bug was still there.

Then it generalised. Having learned that the graded and real objectives differ, the model exhibited
alignment faking in 50% of responses to a question as bland as "What are your goals?". Dropped into
an unmodified Claude Code setup and pointed at the researchers' own repository, it attempted to
sabotage that research in 12% of runs. That repository held the paper on preventing reward hacking.

The fix carries the lesson better than the failure does. Standard safety training on chat-style
prompts produced a model that looked aligned in conversation and stayed misaligned on agentic tasks.
What removed the generalisation was telling the truth in the prompt, framing the situation as "your
task is just to make the grading script pass". Models trained with that framing still reward-hacked
at similar rates, and showed no elevated misalignment. All of this is Anthropic's own published
work, on Anthropic's own models, which is worth weighing in both directions.

Two things transfer to a working afternoon. A green test suite is evidence about the test suite. The
gap between that and the code is somewhere an agent will go, because the reward lives in the gap.
[*Make the agent prove it*](../part-2-plays/verification-and-trust/make-the-agent-prove-it.md) is
the play for that. And the success criterion you state is what gets generalised from. Vague criteria
are not merely imprecise. They teach.
