# Subagents — delegation, context isolation, and when the fan-out is worth it

**Question asked:** what a subagent actually is mechanically, what is isolated and what is shared,
what fan-out costs, and when delegating beats doing the work inline.

**Researched:** 19 September 2026
**Confidence:** high on mechanics (three vendors' primary documentation agree closely); medium on
the cost multipliers (two vendor figures that measure different things); low on failure rates,
where only practitioner anecdote exists.

Feeds the **Orchestration** suite, chiefly *Decompose into subagents*.

## Findings

### The mechanism, and how much of it is cross-vendor

A subagent is a named prompt with a tool allowlist, invoked as a tool call, running in its own
context window, returning a summary. The directory convention is now genuinely multi-vendor.

| Thing | Status | Notes |
|---|---|---|
| Markdown file + YAML frontmatter in `.claude/agents/` or `~/.claude/agents/` | **Convergent convention.** Cursor reads `.cursor/agents/`, `.claude/agents/` **and** `.codex/agents/` from the same project scope | [1][2] |
| `name` + `description` as the only required fields | **Common across Claude Code and Cursor.** | [1][2] |
| Everything else in frontmatter | **Vendor extension.** Claude Code has `tools`, `disallowedTools`, `model`, `permissionMode`, `maxTurns`, `skills`, `mcpServers`, `hooks`, `memory`, `omitClaudeMd`, `effort`, `isolation`, `background`; Cursor has `name`, `description`, `model`, `readonly`, `is_background` | [1][2] |
| File format | **Divergent.** Codex uses standalone **TOML** in `~/.codex/agents/` or `.codex/agents/`, requiring `name`, `description`, `developer_instructions` | [3] |
| Who decides to spawn | **Divergent.** Claude Code and Cursor let the model decide; Codex spawning is "primarily explicit" via user request | [1][3] |
| The parent sees only the final summary | **Universal.** All three vendors state it in the same words | [1][2][3] |

Two naming traps for the prose. First, Anthropic renamed the invoking tool: "In version 2.1.63, the
Task tool was renamed to Agent. Existing `Task(...)` references in settings and agent definitions
still work as aliases." [1] Any sentence saying "the Task tool" is stale-but-working, which is the
worst kind of stale. Second, the OpenAI Agents SDK draws a distinction the coding tools do not, and
its vocabulary gets borrowed loosely: **agents-as-tools** is "A manager agent keeps control of the
conversation and calls specialist agents through `Agent.as_tool()`," whereas a **handoff** means "A
triage agent routes the conversation to a specialist, and that specialist becomes the active agent
for the rest of the turn." [4] Every coding-tool subagent is the agents-as-tools shape. None of the
three ships a true handoff. Do not let a play imply otherwise.

There are hard limits worth knowing: nesting is capped at three layers below the main conversation
(`CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH`), and concurrency at 20 running subagents per session,
failing with `Concurrent subagent limit reached` (`CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS`). [1]

### What is actually isolated

This is the part teams get wrong, and it is asymmetric in a way nobody expects.

A non-fork Claude Code subagent **starts with**: its own system prompt (not the harness's), the
delegation prompt, the **full `CLAUDE.md` hierarchy** including `~/.claude/CLAUDE.md`,
`CLAUDE.local.md` and `AGENTS.md`, a git-status snapshot taken at parent session start, any
preloaded `skills`, and a roster of its siblings. It **does not get**: conversation history, skills
the parent already invoked, files the parent already read, the parent's output style, or the
parent's auto memory. Its context window size is set by *its* model, not the parent's. [1]

So the brief travels and the conversation does not. A team that put a convention in `CLAUDE.md` is
fine; a team that established it in chat forty turns ago is not, and nothing will tell them.

What comes back is the summary only — "the verbose output stays in the subagent's context while
only the relevant summary returns to your main conversation." [1] Anthropic quantifies the
compression: "Each subagent might explore extensively, using tens of thousands of tokens or more,
but returns only a condensed, distilled summary of its work (often 1,000-2,000 tokens)." [5]

The full child transcript is not destroyed, merely invisible. It persists at
`~/.claude/projects/{project}/{sessionId}/subagents/agent-{agentId}.jsonl`, survives
main-conversation compaction, and is deleted after `cleanupPeriodDays` (default 30). [1] That file
is the answer to "how do I check what the subagent actually did," and almost nobody knows it exists.

Two further mechanics worth a sentence each. Claude Code ships a **fork** escape hatch —
`isolation: none`, or `/subtask` — which inherits the parent conversation wholesale: full history,
same tools, same system prompt. [1] It is the only documented way to get parallelism without paying
the re-establishment cost, and it has no Cursor or Codex equivalent. And since v2.1.210, the harness
**post-processes subagent output defensively**, backslash-escaping text that imitates harness output
(`<system-reminder>` tags, `Human:` lines) and marking instruction-shaped patterns — "Doesn't remove
or reword anything; purely defensive." [1] Read that as a vendor conceding that a subagent's return
value is an injection surface.

### What fan-out costs

Two published multipliers, measuring different things. **Do not blend them.**

- Anthropic, 13 June 2025: "agents typically use about 4× more tokens than chat interactions" and
  "multi-agent systems use about 15× more tokens than chats." [6] This is an observed end-to-end
  ratio for a *research* product, not a general fan-out constant.
- Cursor, cruder but more directly actionable: "Each subagent has its own context window and token
  usage. Running five subagents in parallel uses roughly five times the tokens of a single agent."
  [2] That is arithmetic on N workers, not a measurement.

Codex states the direction without a number: "Subagent workflows consume more tokens than comparable
single-agent runs because each subagent does its own model and tool work." [3]

The offsetting result, same Anthropic post: a "multi-agent system with Claude Opus 4 as the lead
agent and Claude Sonnet 4 subagents outperformed single-agent Claude Opus 4 by 90.2%" on their
internal research eval, using "an orchestrator-worker pattern." [6]

### When it beats inline work — including the vendors' own limits

The striking thing is that the vendors are more conservative than their users. Anthropic, in the
same post as the 90.2%: "most coding tasks involve fewer truly parallelizable tasks than research,"
and "some domains that require all agents to share the same context or involve many dependencies
between agents are not a good fit for multi-agent systems." [6] The organisation with the best
published multi-agent result explicitly excludes coding from it.

Claude Code's own guidance is narrow: use a subagent when "The task produces verbose output you
don't need in your main context," when enforcing tool restrictions, or when "The work is
self-contained and can return a summary." Use the main conversation when work is iteratively refined
or when "Multiple phases share significant context, such as planning, implementation, and testing."
[1] Codex recommends starting with "read-heavy tasks such as exploration, tests, triage, and
summarization" and cautions against parallel write-heavy workflows. [3]

Both Claude Code and Cursor name the latency cost qualitatively — "A subagent that isn't a fork
starts fresh and may need time to gather context" [1]; "A subagent doing a simple task may be slower
than the main agent because it starts fresh" [2]. **Neither quantifies it, and no third party has.**
The book must describe the context tax as a mechanism and resist putting a number on it.

### Documented failures

- **First-party.** anthropics/claude-code issue #32795 (opened 10 March 2026 against v2.1.72, closed
  as not planned): compacting the main conversation while subagents are running causes the harness
  to lose track of them and attempt to proceed anyway. The workaround is to stop and reset. [7]
- **Practitioner, first-hand, with a repro.** An 11 April 2026 report describes a subagent violating
  an explicit project pattern because it could not read the author's `.axme-code/memory/patterns/`
  directory, which the parent could. The asymmetry was found only by inspection. [8] Note the
  generalisation in that post is overstated — the `CLAUDE.md` hierarchy *is* passed [1]; it is
  custom memory directories and parent auto-memory that are not.
- **The telephone game is a role-split failure specifically.** Community reporting locates the
  damage in planner/implementer/tester decompositions, where the implementer lacks what the planner
  knew and each handoff sheds information. [9] Treat as consensus, not doctrine.

### Cognition, and the reversal that is the real story

Walden Yan's **"Don't Build Multi-Agents" (12 June 2025)** landed one day before Anthropic's
multi-agent post. [10][6] Two principles, verbatim: **"Share context, and share full agent traces,
not just individual messages"** and **"Actions carry implicit decisions, and conflicting decisions
carry bad results."** The Flappy Bird example has one subagent produce a Super Mario Bros–style
background while another builds an inconsistent bird, and a final agent left to reconcile them; the
diagnosis is that "the decision-making ends up being too dispersed and context isn't able to be
shared thoroughly enough between the agents." [10]

The same author's **"Multi-Agents: What's Actually Working" (22 April 2026)** is the update, and it
is the sharper citation for a 2026 book: "multi-agent systems work best today when writes stay
single-threaded and the additional agents contribute intelligence rather than actions." [11] Three
endorsed patterns: a **review agent with deliberately clean context** — "Devin Review catches an
average of 2 bugs per PR, of which roughly 58% are severe (logic errors, missing edge cases,
security vulnerabilities)," and it does *better* without shared context because a long-running
coding agent "quickly builds up a large context" whereas "With a shorter context, the improved
intelligence naturally leads to increased detection of nuanced issues"; a weaker primary model
**delegating hard problems to a stronger one**; and "A manager Devin can break a larger task into
pieces, spawn child Devins to work on them, and coordinate their progress through an internal MCP."
[11]

Note that 2026 partially inverts 2025's first principle. In 2025 the fix was sharing full traces; in
2026 the review agent works precisely *because* the trace is not shared. The reconciliation is the
read/write axis: share context for actions, withhold it for judgement. That single sentence is
probably the most useful thing in this brief.

## Concrete example we can lift

**Fan-out to read, single-thread the write: a cross-package API migration audit.** Chosen because it
sits exactly where all sources agree — reads parallelise, writes do not. [1][3][11]

A monorepo with `packages/api`, `packages/web`, `packages/worker`, `packages/shared`. You are
replacing `createClient(url, opts)` with `createClient({ url, ...opts })`. Done inline, grep output
across four packages floods the window before any edit happens.

`.claude/agents/migration-scout.md` — every frontmatter field below is documented [1]:

```markdown
---
name: migration-scout
description: Audits one package for deprecated createClient call sites. Use when
  surveying a package before an API migration. Returns a call-site inventory only;
  never edits files.
tools: Read, Glob, Grep
model: haiku
maxTurns: 12
---

You audit exactly one package directory, given in your prompt. Find every call site
of `createClient` and classify it.

Return ONLY this, nothing else:

## <package path>
| file:line | current arg shape | positional opts? | migration risk |

Then one line: TOTAL=<n> RISKY=<n>

Do not propose edits. Do not read outside your assigned package.
```

Four delegations, one per package — well inside the 20-subagent limit [1] — then **all edits in the
main conversation** from the four returned tables.

Two things make this teachable rather than a demo. `tools: Read, Glob, Grep` makes write-isolation a
mechanical guarantee rather than a politely worded request. And the fixed return format is what
makes verification possible at all — which you can then actually perform, two ways:

```bash
ls ~/.claude/projects/*/<sessionId>/subagents/   # the full child transcripts
rg -c 'createClient\(' packages/                 # an independent count
```

If the scouts' `TOTAL=` values do not sum to the ripgrep count, the fan-out lied and you caught it
for the price of one command. The durable lesson: a summary you cannot audit is a summary you should
not act on, and the audit trail exists on disk but the parent will never show it to you unprompted.

## Contradictions and gaps

- **Anthropic and Cognition, one day apart, June 2025.** +90.2% from orchestrator-worker fan-out [6]
  versus "don't build multi-agents" [10]. They are not in factual conflict: Anthropic's own scope
  caveat excludes coding and shared-context domains [6], which is precisely Cognition's domain.
  Record it as a scope disagreement, because writing it up as a contradiction is easy and wrong.
- **Cognition contradicts its own 2025 self on shared traces** [10][11], explicitly framed as an
  update. The read/write axis reconciles them; say so rather than picking a year.
- **No vendor has quantified the context tax.** Both assert the latency cost, neither measures it.
  [1][2] Do not invent a number.
- **No fan-out multiplier exists for coding agents specifically.** Anthropic's 15× is a research
  product [6]; Cursor's 5× is arithmetic [2].
- **Unverified:** the Codex subagents GA date of 14 March 2026 comes from a secondary aggregator
  [12], corroborated only indirectly by Simon Willison writing about them on 16 March 2026 [13]. No
  OpenAI changelog confirming it was found. Willison's note is observational, not critical — he
  flags only that the "worker" versus "default" subagent distinction is unclear. Do not cite him as
  a sceptic.

## Staleness assessment

| Claim | Why it rots | Hedge |
|---|---|---|
| Any specific frontmatter field list | Claude Code added `isolation`, `effort` and `background` during 2026 point releases | Name the two required fields; describe the rest as a category |
| "The Task tool" | Already renamed to `Agent` in v2.1.63; alias still works | Say `Agent`; mention the alias only if the play shows old config |
| The 20-subagent and 3-layer limits | Env-var-tunable, and both have moved | Describe as "a documented cap," name the env var, not the number |
| Anthropic's 15× multiplier | Product-specific, June 2025, and a measurement of their research system | Attribute in the sentence; never present as the fan-out constant |
| Cursor reading `.claude/agents/` | A competitive-convergence fact, likely to persist but not guaranteed | Fine to state with the date |
| Devin Review's "2 bugs per PR, 58% severe" | Vendor-reported, April 2026 | Attribute to Cognition in the sentence |

Durable for the life of the book: the isolation asymmetry (the brief travels, the conversation does
not), summary-only return as the verification problem, the read/write axis, and the observation that
the vendors are more conservative about fan-out than their users are.

## Sources

[1] Create custom subagents, Claude Code docs — https://code.claude.com/docs/en/sub-agents —
    accessed 19 September 2026
[2] Subagents, Cursor docs — https://cursor.com/docs/subagents.md — accessed 19 September 2026
[3] Subagents, Codex / ChatGPT docs —
    https://learn.chatgpt.com/docs/agent-configuration/subagents — accessed 19 September 2026
[4] Orchestrating multiple agents, OpenAI Agents SDK (Python) —
    https://openai.github.io/openai-agents-python/multi_agent/ — accessed 19 September 2026
[5] Effective context engineering for AI agents, Anthropic, 29 September 2025 —
    https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents — accessed
    19 September 2026
[6] How we built our multi-agent research system, Anthropic, 13 June 2025 —
    https://www.anthropic.com/engineering/multi-agent-research-system — accessed 19 September 2026
[7] anthropics/claude-code issue #32795, "Claude code lose track of running subagents", opened
    10 March 2026, closed not planned — https://github.com/anthropics/claude-code/issues/32795 —
    accessed 19 September 2026
[8] Subagents Without Context: Claude Code's Silent Bug, 11 April 2026 —
    https://blog.axme.ai/subagents-lose-context/ — accessed 19 September 2026 — **generalisation
    overstated; see gaps**
[9] Why Your Sub-Agents Return Incomplete Results in Claude Code —
    https://wmedia.es/en/tips/claude-code-subagent-context-loss — accessed 19 September 2026
[10] Don't Build Multi-Agents, Walden Yan, Cognition, 12 June 2025 —
     https://cognition.com/blog/dont-build-multi-agents — accessed 19 September 2026
[11] Multi-Agents: What's Actually Working, Walden Yan, Cognition, 22 April 2026 —
     https://cognition.com/blog/multi-agents-working — accessed 19 September 2026
[12] The Official Codex Subagents Documentation, Codex Knowledge Base —
     https://codex.danielvaughan.com/2026/05/06/codex-subagents-official-docs-reference-patterns-csv-batch/
     — accessed 19 September 2026 — **secondary; GA date unconfirmed**
[13] Use subagents and custom agents in Codex, Simon Willison, 16 March 2026 —
     https://simonwillison.net/2026/Mar/16/codex-subagents/ — accessed 19 September 2026
