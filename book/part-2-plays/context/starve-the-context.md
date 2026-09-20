# Starve the context

## Problem

A context window gets packed the way a suitcase gets packed the night before a flight: everything
that might conceivably be needed, on the theory that the alternative is needing it and not having
it. So the run starts with the architecture document, the four adjacent modules, last week's
incident write-up, and the whole test file. The answer that comes back is worse than the one you got
last month from a two-sentence prompt and one file — blander, hedged, quietly ignoring two of the
five requirements. Nothing failed. You paid more for it, and you have no idea which of the things
you added did the damage.

## The play

Reduction never happens by accident. Somebody has to decide what not to send.

1. **Write the exclusion, not only the inclusion.** Before a run, name the two or three things the
   task genuinely needs, then say out loud what it does not: the other services, the deployment
   config, the history of why the module is shaped this way. If you cannot state why a file is in
   the window, it is in the window because it was nearby.
2. **Load on arrival, not in advance.** Anything conditional — a convention for one directory, a
   procedure for one situation — belongs behind a trigger, whether that is a path-scoped rule, a
   skill description ([*Package repeatable expertise*](../harness/package-repeatable-expertise.md)),
   or a card you load by hand ([*Split the agent file into
   cards*](split-the-agent-file-into-cards.md)). Three vendors have built three mechanisms for this
   and they encode one idea: the instruction should turn up when its situation does.
3. **Prefer a smaller task to a filtered one.** Filtering is damage control applied after you have
   already asked for the wrong thing. If the window is under pressure, the first move is
   [*Scope a task to fit the window*](scope-a-task-to-fit-the-window.md), not a compression layer.
4. **If you do filter at the tool boundary, measure the bill rather than the dashboard.** Run the
   same task set with the filter and without it, several repetitions each, same model and same
   reasoning effort. Read cost from the provider's billing view, broken out into fresh input, cache
   reads, cache writes, and output. Record turns in the same table, because a tool that cuts tokens
   per turn and adds turns can be net negative, and turns is the column people omit. Score quality
   too, so you notice if you bought the saving with worse output.
5. **Reach for the first-party primitives on long work, and know what they discard.** Context
   editing replaces old tool results with a placeholder while keeping the record that the call
   happened; compaction summarises the older conversation and restarts from the summary. Anthropic's
   own framing of the risk is the honest one: aggressive compaction loses "subtle but critical
   context whose importance only becomes apparent later".

What makes this work is that attention is not free per token. Every token attends to every other
token, so a window is not a shelf you put things on — it is a room where everything you add makes
everything already there slightly harder to find. The goal Anthropic states for its own agents is
worth stealing verbatim: find the smallest set of high-signal tokens that gets you the outcome. That
is signal over noise taken at the level of one run rather than one project. The exchange rate is
that you will sometimes have to hand the agent one more file mid-run, and being occasionally
under-supplied is cheaper than being reliably over-supplied.

## Worked example

`atlas`, the Python billing service. Somebody had installed a token-filtering proxy globally — a
`PreToolUse` hook that rewrites eligible shell calls, so the agent never knows it exists — and its
analytics reported savings in the high tens of percentage points. The question was whether to keep
it.

The published evidence is why that question is worth asking
([`token-filtering.md`](../../../notes/research/token-filtering.md)). Two independent benchmarks
measured `rtk` v0.43.0 in mid-2026. JetBrains ran 425 billed trials against Claude Code 2.1.201 and
found cost per task up 7.6% at low reasoning effort, turns up 13.8%, and task quality statistically
tied — while the tool's own analytics reported 96.2 million tokens saved over the same trials, 99.8%
of everything it touched. Quesma, independently, on Terminal-Bench 2.1 across 1,740 attempts and two
models, found it marginally cheaper with one and 7% more expensive with the other, and concluded:
"We do not recommend RTK as a generic cost-saving tool."

Both sides are telling the truth. The tool removes 60–90% of the bytes a command emits; the bill
still goes up. Most of a session's input cost arrives as cached re-reads billed at roughly a tenth
of fresh tokens, which the hook never sees, and compressed output costs extra turns to recover.
"Less output" and "higher bill" were never contradictory claims.

So the team ran the paired comparison on their own repo: twelve backlog tasks, three repetitions
each. These are the columns that settle it, and nobody else's numbers go in them:

| Condition | Fresh input | Cache reads | Output | Turns | Tasks passed |
|---|---|---|---|---|---|
| Without filter | | | | | |
| With filter | | | | | |

*Blank on purpose: the only numbers that settle it are the ones you measure.*

The outcome was mixed. The filter was a clear win on exactly one thing: the
dependency-resolution output from their package manager, four thousand lines of tree in which the
agent needed six. It was a mild loss everywhere else, mostly in turns. They kept it for that one
command and uninstalled the global hook — a less satisfying result than either the README or the
benchmark predicted, and the only one either of them supports.

## Failure mode

**The Flattering Dashboard.** A tool measures its own benefit at the point where it acts — bytes
removed, tokens "saved" — against a counterfactual your billing system never applies. The number it
reports is real and it is not your bill, and because it is enormous, nobody checks. The reported
saving and the measured spend can move in opposite directions by two orders of magnitude and both be
accurate. The tell is a savings figure that arrives from the same process that created the saving,
with no independent measurement anywhere in the loop. Anything that keeps its own scoreboard
flatters itself, which is not dishonesty but what measuring your own work looks like.

**The Adequate Answer.** The output is fine — not good, not wrong, and fine passes review. So
nobody looks at the context that produced it, and it goes on growing: the only thing that prompts a
look is a result bad enough to investigate. A capable model absorbs the noise and answers anyway.
The bill is the only tell.

## Checklist

- [ ] The things deliberately kept out of this run can be named
- [ ] Conditional instructions load on a trigger, not at launch
- [ ] Scoping the task smaller was tried before adding a compression layer
- [ ] Any filtering tool was measured on a paired run, not on its own analytics
- [ ] Cost was read from the provider's billing view, split by fresh input and cache reads
- [ ] Turns were recorded alongside cost
- [ ] Output quality was scored, so a saving bought with worse answers would show up

**See also:** [*Scope a task to fit the window*](scope-a-task-to-fit-the-window.md) ·
[*Understand what you are paying for*](../economics/understand-what-you-are-paying-for.md)
