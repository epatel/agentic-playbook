# Token filtering and context reduction

**Question asked:** what tooling exists to cut tokens and shrink context — including `rtk` — when it
earns its keep, and what the evidence actually says.

**Researched:** 18 September 2026
**Confidence:** high — this is the best-evidenced subject in the whole pass. Two independent
benchmarks, published methodology, published numbers, and an open unanswered issue on the tool's own
tracker. The vendor-side primitives are documented with measured cookbook runs.

Feeds the **Context** suite (*Starve the context*) and hands the Economics suite its best cautionary
tale.

## Findings

### Two different things get called "context reduction"

Worth separating in the prose, because they fail differently:

1. **Output filtering at the tool boundary** — compressing what a command returns *before* it enters
   context. `rtk` is the prominent example. Operates outside the model, on bytes.
2. **First-party context management inside the transcript** — the API's context editing, compaction,
   and memory primitives. Operates on the conversation itself, with the billing system's own view of
   what a token is.

### `rtk` — what it claims

Open source, Apache 2.0, a single Rust binary with no dependencies. v0.49.0 at time of writing.
[1][2]

- Headline claim: **"reduces LLM token consumption by 60-90% on common dev commands."** [2]
- On its own site: "output drops by 56% on average, and by up to 90% on the noisiest ones," across
  **125+ commands** including `cargo test`, `pytest`, `go test`, `git diff`, `git status`, `git
  log`, `grep`, `find`, `ls`, `tsc`, `eslint`, `docker`, and `kubectl`. [1]
- Installs as a **PreToolUse hook** via `rtk init --global`, which rewrites eligible Bash calls
  transparently — `git status` becomes `rtk git status` — so the model need not know it exists. [1]
- Ships its own analytics: `rtk gain` reports token savings.

### `rtk` — what two independent benchmarks measured

**JetBrains, July 2026.** rtk v0.43.0 against Claude Code 2.1.201 on SkillsBench, 86 tasks, four
paired runs (a 10-task smoke test, the same 10 at k=3, the full 86 at low effort, the full 86 at
high effort), 425 billed trials in total. [3]

| Measure | Result |
|---|---|
| Cost per task, low reasoning effort | **+7.6% more expensive** (p=0.004) |
| Cost per task, high reasoning effort | **+0.1%** (p=0.99) |
| Turns | **+13.8%** (p=0.03) |
| Cache reads | **+14.3%** (p=0.008) |
| "New input" tokens — where compression actually lands | **+3.2%** (p=0.23) |
| Task quality | statistically tied: 5 better / 4 worse / 71 tie at low effort; 5 / 4 / 62 at high |
| **rtk's own analytics over the same trials** | **"96.2 million tokens saved — 99.8% of everything it touched"** |

**Quesma, independently, on Terminal-Bench 2.1.** Each task five times with and without rtk, across
Claude Code (Fable 5.0) and OpenCode (DeepSeek V4 Pro 0813); 1,740 attempts over 85 Fable tasks and
89 DeepSeek tasks. [4]

| Measure | Baseline | With rtk |
|---|---|---|
| Fable, input / total | $596 / $731 | $546 / $698 — 3% cheaper per successful pass |
| DeepSeek, input / total | $26 / $51 | $31 / $54 — 7% more expensive per pass |
| Task-level | — | Fable 1% more expensive; DeepSeek 17% more expensive |

Quesma's conclusion: **"On Terminal-Bench 2.1, Fable's savings depended on one task and did not hold
across tasks. We do not recommend RTK as a generic cost-saving tool."** They explicitly agree with
JetBrains: "JetBrains saw the same pattern on SkillsBench: RTK added turns at low effort and did not
lower cost at high effort." [4]

**The reported mechanism for the gap** — secondary, presented as analysis rather than measurement:
rtk estimates tokens as characters ÷ 4 at execution time, while most of a session's input cost
arrives as *cached re-reads* billed at roughly one-tenth the price of fresh tokens. The hook never
sees most of the session's context, so its scoreboard grades against a counterfactual the billing
system never applies. [3][5] Compressing a tool result also removes information the model then
spends extra *turns* recovering — which is what the +13.8% turns figure is.

**Status of the dispute.** Issue #3157 on `rtk-ai/rtk`, "README is outdated - rtk makes agentic
coding 7.6% more expensive at low reasoning effort," was **open with no maintainer response as of 22
July 2026**, labelled `area:docs`, `documentation`, `needs-info`, `priority:medium`. [6] The 60–90%
claim was still on the project's front page at the time of this research. [1][2]

### First-party context management

Three API primitives, which behave quite differently from output filtering because they operate
inside the billed transcript: [7][8]

- **Context editing** (`clear_tool_uses_20250919`) walks the message list and replaces `tool_result`
  content blocks with a short placeholder, leaving user messages, assistant reasoning, and the
  `tool_use` record intact. The model keeps the record that it made a call and with what input; the
  bulky body is gone.
- **Compaction** (`compact_20260112`) summarises older conversation as the window fills and restarts
  from the summary. Anthropic's own framing: "The art of compaction lies in the selection of what to
  keep versus what to discard, as overly aggressive compaction can result in the loss of subtle but
  critical context whose importance only becomes apparent later."
- **The memory tool** — structured note-taking to files that survive a context reset.

Measured in Anthropic's cookbook run (clearing triggered at 30K, keep = 4): clearing fired four
times, freeing **~163K tokens per event**; peak context **173,137 tokens versus 335,279 baseline**.
[8]

### The underlying principle

From Anthropic's *Effective context engineering for AI agents* (29 September 2025), which is the
most quotable framing found and is durable in a way the tool numbers are not: [9]

- **"find the smallest set of high-signal tokens that maximize the likelihood of some desired
  outcome."**
- Degradation with length has a name — **"context rot"** — and an architectural cause: attention
  requires "every token to attend to every other token across the entire context. This results in n²
  pairwise relationships for n tokens."
- Practical guidance: minimise functional overlap between tools; prefer just-in-time retrieval to
  pre-loading; use compaction, structured note-taking, and sub-agents returning condensed summaries
  for long-horizon work.

## When it earns its keep

Output filtering earns its keep in narrow, verified cases: a command whose output is genuinely
enormous, genuinely repetitive, and whose useful content is a small deterministic subset — a
thousand-line dependency tree, a test runner that prints a progress dot per test. It does not earn
its keep as a blanket setting applied to every shell call, which is exactly how the hook installs
it.

First-party context management earns its keep on long-horizon work, where the alternative is hitting
the window and losing everything rather than losing the oldest tool results.

The *technique* that survives both is neither: scope the task so less enters context in the first
place. Filtering is damage control applied after you have already asked for the wrong thing.

## Sharpest real-world gotcha

**The tool's dashboard said it saved 96.2 million tokens — 99.8% of everything it touched — over the
same trials in which the measured bill went up 7.6%.** [3]

That is the whole play in one sentence, and it generalises past `rtk` entirely: a filtering tool
that measures its own benefit at the point of filtering, against a counterfactual the billing system
never applies, will report spectacular savings indefinitely, regardless of whether it saves
anything. Two independent benchmarks on different suites, different models, and different harnesses
agreed that it did not. [3][4]

The secondary failure mode is the one nobody instruments: compression removes information the model
then spends *turns* recovering. Cost is tokens × turns, and filtering optimises one of those while
silently inflating the other — +13.8% turns in the JetBrains run. [3]

## Concrete example we can lift

The play is **"measure the bill, not the dashboard,"** and the worked example is a paired run the
reader can perform on their own repo in an afternoon. The method, drawn from the published
methodologies: [3][4]

1. Pick a task set you can run repeatedly and score pass/fail — your own test suite is fine.
2. Run it paired: with the tool and without, same prompts, same model, same reasoning effort. Both
   benchmarks ran multiple repetitions per condition (JetBrains: 425 billed trials; Quesma: 1,740
   attempts) because single runs are noise.
3. Read the cost from the **provider's billing view**, broken out into fresh input, cache reads,
   cache writes, and output. Do not read it from the tool.
4. Record **turns** alongside cost. A tool that cuts tokens per turn and adds turns can be net
   negative, and this is the column people omit.
5. Score quality, so you notice if you bought the saving with worse output. Both benchmarks found
   quality statistically tied, which is the only reason the cost comparison is meaningful.

The punchline for the *Failure mode* heading: JetBrains reported the tool's self-assessment and the
billing system's assessment side by side, and they disagreed by roughly two orders of magnitude and
in opposite directions. [3]

> Any figures lifted from here must carry their date and versions — rtk v0.43.0 / Claude Code
> 2.1.201 for the JetBrains run [3]; the claims are from rtk v0.49.0's front page [1]. Per
> `book/STYLE.md`, captured output must be marked as such and this pass captured none of it.

## Contradictions and gaps

- **The vendor's claims and two independent measurements are in direct, unresolved conflict**, and
  the maintainers had not responded to the issue raising it as of 22 July 2026. [6] The book should
  present the conflict rather than adjudicating it — and should note that "60–90% less output" and
  "7.6% more expensive" are not actually contradictory claims. Both can be true. That is the point.
- **The rtk benchmarks tested rtk v0.43.0; the current version is v0.49.0.** [1][3] Nothing found
  re-tests the newer version. A claim that rtk costs more should be dated and versioned or softened
  to the general lesson.
- **Direction is model- and effort-dependent.** Quesma found rtk marginally cheaper per successful
  pass with one model and more expensive with another, and the effect largely vanished at high
  reasoning effort in the JetBrains run. [3][4] There is no single answer.
- **The chars ÷ 4 and cache-pricing explanation is analysis, not measurement.** Plausible and
  consistent with the data, but nobody instrumented it directly. [3][5]
- **No independent measurement of the first-party primitives' effect on cost or quality.** The
  cookbook numbers are Anthropic's own single run, and they measure peak context, not spend or
  outcome. [8]

## Sources

[1] RTK — Rust Token Killer — https://www.rtk-ai.app/ — accessed 18 September 2026
[2] rtk-ai/rtk — https://github.com/rtk-ai/rtk — accessed 18 September 2026
[3] rtk Claude Code Token Savings: A Skill Trial Benchmark, JetBrains AI blog, July 2026 —
    https://blog.jetbrains.com/ai/2026/07/rtk-claude-code-token-savings/ — accessed 18 September 2026
[4] RTK reports huge token savings, but our cost benchmarks disagree, Quesma —
    https://quesma.com/blog/does-rtk-make-ai-coding-cheaper/ — accessed 18 September 2026
[5] RTK token savings: 89% fewer tokens, no lower bill —
    https://www.samcodeman.com/writing/rtk-token-savings-ai-coding-cost-benchmark — accessed 18 September 2026
[6] rtk-ai/rtk issue #3157 — https://github.com/rtk-ai/rtk/issues/3157 — accessed 18 September 2026
[7] Context Editing Looks Like a Feature. It's Actually a Garbage Collector Without Write Barriers —
    https://conikeec.substack.com/p/context-editing-looks-like-a-feature — accessed 18 September 2026
[8] Context engineering: memory, compaction, and tool clearing, Claude Cookbook —
    https://platform.claude.com/cookbook/tool-use-context-engineering-context-engineering-tools — accessed 18 September 2026
[9] Effective context engineering for AI agents, Anthropic, 29 September 2025 —
    https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents — accessed 18 September 2026
