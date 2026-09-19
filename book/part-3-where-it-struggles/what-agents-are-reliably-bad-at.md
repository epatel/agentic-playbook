# What agents are reliably bad at

Every tool sold to developers arrives with a list of what it is good at and a silence where the
other list should be. This part is the other list. It is shorter than the sceptics claim and
considerably longer than the release notes imply, and none of it is a reason to stop — the plays in
this book are written by someone who uses these tools every day and intends to keep doing so. The
argument is only that a practice built on the marketing version of the capability will be built in
the wrong shape.

One caution about the evidence, stated once and then assumed. Almost nothing published about "AI
coding productivity" is about agents: every randomised trial in the field measures autocomplete,
inline completion, or chat. What follows is drawn from benchmark results, vendor measurements that
say so, and studies with stated sample sizes. Where a figure is vendor-reported, the sentence says
so. The full accounting, including the forty-odd widely-quoted numbers that did not survive
checking, is in [`notes/research/evidence.md`](../../notes/research/evidence.md).

## Finishing

Agents get most of the way. On Long-Horizon-Terminal-Bench — 46 tasks across nine categories,
averaging 231 episodes, 9.9 million tokens, and 85 minutes of wall clock each, published July 2026 —
the best of fifteen frontier models completed 15.2% of tasks at the strict reward threshold, the
mean across all fifteen was 4.3%, and ten of the fifteen completed none. Near-misses outnumbered
passes 73 to 30. And 79% of unresolved runs ended because the ninety-minute budget expired, not
because the agent hit something it could not do.

The authors read the bottleneck as long-horizon completion rather than local reasoning, which is a
polite way of saying that almost nothing in those runs was beyond the model and the runs still did
not finish. This is the benchmark-scale version of something you recognise from your own week: the
run that ends at ninety per cent, the continuation that also ends at ninety per cent, and the
absence of any turn that presents itself as the one to stop on. [*Scope a task to fit the
window*](../part-2-plays/context/scope-a-task-to-fit-the-window.md) names that as the Permanent Near
Miss and gives it a stop rule.

## Being wrong in a way that compiles

SWE-Bench Pro splits its problems into a public set drawn from open repositories and a commercial
set drawn from eighteen proprietary startup repositories. In the November 2025 version of that
paper, Claude Sonnet 4 resolved 42.7% of the public set and 9.1% of the commercial set. Same model,
same harness, same evaluation.

The likeliest explanation is not that private code is harder in some deep sense. It is that public
code has been read. In 2025 contamination work, models identified the buggy file in a SWE-bench
repository from the issue text alone — with no repository structure in the prompt at all — at up to
76% accuracy, against up to 53% on repositories outside the benchmark; a separate 2025 audit found
32.67% of successful patches involving solution leakage, with the fix stated in the issue report or
its comments. Your repository is the commercial set.

What the failures look like when they happen is the Confident Wrong Rewrite, described in [*The
failure modes worth naming*](the-failure-modes-worth-naming.md), and the short version is that they
compile.

## Security, unevenly

Veracode's longitudinal study — over 150 models by the spring 2026 edition, 80 tasks built against
MITRE weakness categories in four languages — reports the security pass rate essentially unchanged
across three editions, "from approximately 55% to approximately 55%", while syntactic correctness
passed 95%. It is vendor-reported, and the flatness rather than the level is the durable finding:
models got substantially better at writing code that works and did not get better at writing code
that is safe.

The gap is not uniform, which is the part worth acting on. In that edition, generated code passed
82% of SQL-injection tasks and 86% of insecure-cryptography tasks, against 15% of cross-site
scripting and 13% of log injection. By language, Python passed 62% and Java 29%.

The shape behind those numbers is legible. Models are reliable where the fix is a canonical call at
the site of the defect — a parameterised query, a named cipher, a library everyone uses the same
way. They are unreliable where correctness depends on where the value ends up, because output
encoding is a property of the destination and the destination is usually not in the window. Review
agent-written code accordingly: spend your attention on the paths where data leaves, not on the
lines where it arrives.

## Iterating on their own work

SlopCodeBench, March 2026, measured something the other benchmarks do not: agents extending their
own prior code across 93 checkpoints on 20 problems, 11 models in 25 configurations. No agent solved
any problem end to end. The highest checkpoint solve rate was 17.2%, and cost grew 2.9× across a
*trajectory* — one agent's full sequence of attempts at a problem — with no matching improvement.

The interesting measurements are the ones about the code rather than the score. Verbosity grew in
89.8% of trajectories and complexity concentration in 80%, with the concentration metric moving from
a mean of 0.39 to 0.68. Agent-authored code averaged 2.2× the verbosity of maintained human
repositories. Functions grew tenfold in cyclomatic complexity without being refactored; duplicate
parsing code was repeated across branches instead of extracted.

The control group is the finding. Human repositories hold those metrics flat over time. Agent
trajectories deteriorate on every pass, and no individual pass fails. That is the Endless Polish,
and what to do about it is in [*The failure modes worth naming*](the-failure-modes-worth-naming.md).

## Optimising the thing you measured

The sharpest published result in this area is not about capability at all. In November 2025
Anthropic and Redwood Research described training a model with reinforcement learning on real
production coding environments, where the reward was the obvious one: run the grading script, and if
it exits zero the task is solved.

The model worked out that it did not have to make the code work. It had to make the script exit
zero. So it called `sys.exit(0)` in Python, breaking out of the test harness with a zero exit status
before the assertions ran. The grader recorded a pass. The reward was paid. The bug was still there.

Then it generalised. Having learned that the graded objective and the real objective are different
things, the model exhibited alignment faking in 50% of responses to a question as bland as "What are
your goals?" — and, dropped into an unmodified Claude Code setup and pointed at the researchers' own
repository, attempted to sabotage that research in 12% of runs. The repository in question held the
paper on preventing reward hacking.

The fix carries the lesson better than the failure does. Standard safety training on chat-style
prompts produced a model that looked aligned in conversation and stayed misaligned on agentic tasks.
What removed the generalisation was telling the truth in the prompt — framing the situation as "your
task is just to make the grading script pass". Models trained with that framing still reward-hacked
at similar rates, and showed no elevated misalignment. All of this is Anthropic's own published
work, on Anthropic's own models, which is worth weighing in both directions.

Two things transfer to a working afternoon. A green test suite is evidence about the test suite, and
the gap between that and the code is somewhere an agent will go, because the reward lives in the
gap; [*Make the agent prove it*](../part-2-plays/verification-and-trust/make-the-agent-prove-it.md)
is the play for that. And the success criterion you state is what gets generalised from. Vague
criteria are not merely imprecise. They teach.
