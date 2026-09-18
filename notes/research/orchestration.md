# Orchestration and workflow landscape

**Question asked:** what the orchestration options actually are — subagents, LangChain/LangGraph,
visual workflow tools, scripted versus model-driven control flow, and parallel execution — what the
honest case for and against each is, and where a single capable agent beats the lot.

**Researched:** 19 September 2026
**Confidence:** high on mechanics (vendor documentation and the git manual are primary throughout);
high on the reliability and conflict-rate evidence (arXiv papers with stated samples and intervals);
low on every adoption, funding and revenue figure, none of which is independently audited; low on
whether parallel coding agents are net faster, which is essentially unmeasured.

This is the hub brief. Each subject has its own file so a writer chasing one thing does not have to
read the other five:

| Brief | Feeds | Covers |
|---|---|---|
| [`subagents.md`](subagents.md) | *Decompose into subagents* | The mechanism, context isolation, fan-out cost, Cognition's reversal |
| [`langchain-langgraph.md`](langchain-langgraph.md) | *Make the control flow deterministic* | The framework/runtime split, what LangGraph buys, the production complaints |
| [`visual-workflow-tools.md`](visual-workflow-tools.md) | *Make the control flow deterministic*, Team suite | n8n's licence, review and test story, where the developer line falls |
| [`control-flow.md`](control-flow.md) | *Make the control flow deterministic* | The decision criteria table, the reliability evidence, hybrid patterns |
| [`parallel-agents-and-collisions.md`](parallel-agents-and-collisions.md) | *Work in parallel without collisions* | Worktrees, the collision taxonomy, measured conflict rates |
| [`single-agent-wins.md`](single-agent-wins.md) | All three Orchestration plays; *Know when not to use an agent* | The credibility material — where orchestration loses |

---

## The one finding that shapes everything else

**Every vendor in this space is more conservative about orchestration than their users are, and the
published evidence is more conservative still.**

Anthropic reports a multi-agent system outperforming a single agent "by 90.2%" — and in the same
post says "most coding tasks involve fewer truly parallelizable tasks than research" and that
domains requiring shared context or with many inter-agent dependencies "are not a good fit for
multi-agent systems." [6] Their guidance elsewhere is to "start by using LLM APIs directly." [11]
OpenAI's recommendation is to "maximize a single agent's capabilities first." [3] Cognition
published "Don't Build Multi-Agents" and, ten months later, an update whose thesis is that
multi-agent works "when writes stay single-threaded and the additional agents contribute
intelligence rather than actions."
[17][18] And the strongest controlled comparison available found that of six multi-agent systems,
**only one beat the single-agent baseline; the other five underperformed by 2.56–11.29 percentage
points while costing more.** [9]

Meanwhile the ecosystem sells fan-out as the default. That asymmetry — practitioners reaching for
orchestration faster than either the vendors or the evidence supports — is the honest spine of the
whole Orchestration suite, and it is unusual, because it means the book gets to be sceptical while
citing the vendors *in support* rather than against.

The corollary that turns scepticism into advice comes from Anthropic's harness post: **"Every
component in a harness encodes an assumption about what the model can't do on its own, and those
assumptions are worth stress testing."** [16] Every piece of orchestration is a dated bet on a
capability gap. The design question is therefore not "should I orchestrate?" but **"can I delete
this cheaply when the gap closes?"** That is the *removability test*, and it is the single most
portable idea in this pass.

## What is standardised vs. one vendor's habit

| Thing | Status | Notes |
|---|---|---|
| Subagent directory convention (`.claude/agents/`, markdown + YAML) | **Convergent, not formalised.** Cursor reads `.cursor/`, `.claude/` **and** `.codex/` agent directories | [1][2] |
| `name` + `description` as the only required subagent fields | **Common** to Claude Code and Cursor | [1][2] |
| Subagent file format | **Divergent.** Codex uses standalone TOML with `developer_instructions` | [3] |
| Who decides to spawn a subagent | **Divergent.** Model-initiated in Claude Code and Cursor; "primarily explicit" in Codex | [1][3] |
| Parent receives only the child's final summary | **Universal.** All three vendors state it | [1][2][3] |
| Subagent frontmatter beyond the two required fields | **Vendor extension**, and the lists barely overlap | [1][2] |
| The workflow-vs-agent vocabulary (prompt chaining, routing, orchestrator-workers…) | **De facto standard.** Anthropic's December 2024 taxonomy is still the common language | [1a] |
| Agent framework APIs (LangGraph `StateGraph`, CrewAI Crews/Flows, Agents SDK handoffs) | **Entirely per-vendor.** No portability whatsoever | [1b][21][22] |
| "Durable execution" as a term | **Contested.** LangGraph means checkpoint-and-resume; Temporal/Dapr/DBOS mean guaranteed completion | [8][18b] |
| n8n's licence | **Not open source, by its own statement** — Sustainable Use License plus an Enterprise License | [2b][3b] |
| `git worktree` mechanics | **Standard.** Core git, stable, and the one genuinely durable substrate in the pass | [1c] |
| What a worktree isolates | **Standard and widely misunderstood.** Refs, config, stash and **hooks** are shared | [1c][5c] |
| Preventing an agent escaping its worktree | **One vendor's implementation.** Git offers nothing; Claude Code blocks `git -C`, `--git-dir`, `GIT_DIR`, `GIT_WORK_TREE` and `cd` | [2c] |

The pattern mirrors milestone 4's finding almost exactly: the *file formats and substrates* are
converging while the *behaviour* stays per-vendor. A team that standardises on "we keep agent
definitions in a directory and partition work by worktree" is portable. A team that standardises on
a framework's graph API is not.

## Cross-cutting gotchas worth a named failure mode

Four patterns recur across the six briefs. None is registered in the failure-mode registry — per the
milestone-4 precedent, a research brief should not squat names that suite authors have to live with.
Whichever play writes one first names it and registers it in `plans/agentic-playbook.md`.

1. **The summary is the only thing you get, and you will not check it.** Every vendor confirms the
   parent sees only the child's final message. [1][2][3] The full child transcript exists on disk at
   `~/.claude/projects/{project}/{sessionId}/subagents/agent-{agentId}.jsonl` [1] and essentially
   nobody reads it. A delegation you cannot audit is a claim you accepted on trust — and the harness
   now *post-processes* subagent output defensively against injection [1], which is a vendor
   conceding the return value is untrusted input.

2. **The brief travels; the conversation does not.** A subagent inherits the full `CLAUDE.md`
   hierarchy but none of the parent's conversation history, read files, or invoked skills. [1] So a
   convention you wrote down is enforced and a convention you established in chat forty turns ago is
   silently absent. Nothing errors. This is the orchestration-layer sibling of milestone 4's
   silent-precedence gotcha.

3. **Clean merge, broken build.** The conflicts git reports are the survivable ones. Agent A
   renames a function and fixes its call sites; agent B, on the old base, adds three new calls to
   the old name. Both branches green, merge clean, production `NoMethodError`. [18c] The measured
   textual conflict rate — 19.8% intra-agent, 41.7% cross-agent — comes with its authors' own caveat
   that it "captures only the surface layer" and is "a conservative lower bound." [16c]

4. **The fan-out was a compute budget in a costume.** Multi-agent advantages shrink or vanish when
   thinking tokens are held constant. [8] Five of six systems cost more *and* scored worse under
   matched accounting. [9] Before adding an agent, spend the same tokens on one and measure.

## The two cases where a single agent beats the orchestration

Commissioned explicitly, and the reason the suite will be believed. Full treatment in
[`single-agent-wins.md`](single-agent-wins.md); the headlines:

**Case one — the framework was doing less than you thought.** Anthropic advises starting with the
API directly and warns that frameworks "often create extra layers of abstraction that can obscure
the underlying prompts ​​and responses, making them harder to debug." [11] Octomind removed
LangChain after twelve months in production. [15] Five of six multi-agent systems lost to a single
agent under matched protocol. [9] The play is not "frameworks are bad" — it is that an abstraction
is worth its debugging cost only when it buys something you would otherwise build. For LangGraph
that thing is resumability, and for most teams it is nothing.

**Case two — the fan-out was a compute budget in a costume.** Gotcha 4 above, stated as a checklist
item. [8][9][10]

A third is available if a play needs it: **parallel coding agents are unmeasured.** The only
controlled study found "up to 21.1% speedup on some tasks" and "up to 39.4% slowdown on others," and
no study was found measuring end-to-end wall clock for supervised parallel agents *including* merge
and rework. [17c]

## Where each option actually earns its keep

The one-paragraph version, for a writer who needs the shape before the detail.

- **A subagent** earns its keep when the work is read-heavy, self-contained, produces verbose output
  the parent does not need, and can return a checkable summary. [1][3] It loses when phases share
  context — planning, implementing and testing the same change — because each handoff sheds what the
  previous stage knew. [17]
- **LangGraph** earns its keep when a run must survive a process restart: a checkpointer plus a
  `thread_id` gives pause, redeploy, and resume *from inside the tool call*. [6b][7b] It does not
  buy you a supervisor — nothing detects the crash and restarts the run, which is the criticism that
  survives every version bump. [18b]
- **n8n and the visual tools** earn their keep at the *edges* — credentialed API calls, schedules,
  retries, and a canvas a non-developer can actually see. They lose at the centre, the moment
  routing logic acquires state and conditionals, because that logic ends up in a textarea with no
  tests, no breakpoints and a JSON-blob diff. [13b]
- **Scripted control flow** earns its keep on long horizons and irreversible actions;
  **model-driven** control flow earns its keep on unstructured input and judgement calls. Split on
  **reversibility and horizon, not on difficulty**. [1a][3]
- **Worktrees** earn their keep as ergonomics — one repository, one `git worktree list`, shared
  refs — **not** as disk or time savings, which one benchmark found indistinguishable from `git
  clone --shared`, nor as a security boundary, since `.git/hooks` is shared and runs as you. [5c]

## Contradictions and gaps

- **Anthropic contradicts Anthropic, repeatedly and productively.** Compounding errors argue for
  guardrails [1a]; hardcoded logic is itself the fragility [15a]; the harness post splits the
  difference and offers the removability test [16]. Not resolvable, and the book should not pretend
  otherwise. Present the tension and the test.
- **Anthropic and Cognition, one day apart in June 2025**, look like a head-on collision and are
  not: Anthropic's own scope caveat excludes exactly the domain Cognition works in. [6][17] Writing
  it up as a contradiction is easy and wrong.
- **Cognition contradicts its 2025 self** on sharing traces. [17][18] The read/write axis
  reconciles them — share context for actions, withhold it for judgement — and that sentence is more
  useful than either post.
- **Every commercial figure in this pass is vendor-reported.** LangChain's 90M monthly downloads
  and 35% of the Fortune 500 [13b]; n8n's $5.2bn valuation and 1.7 million monthly active builders
  [6b']. Attribute in the sentence or cut.
- **Two low-code statistics did not survive verification and must not be used:** the "43% of citizen
  developer initiatives scaled back, paused or discontinued" figure attributed to Gartner, and a
  "25–30% rewrite rate for no-code projects." Both trace only to secondary or vendor content.
- **Three primary sources could not be read:** Octomind's post (site refused connections, and
  archive.org unavailable) [15]; a Boris Cherny "10–20% scaffolding" quote with no traceable
  transcript; and per-level GAIA figures not verified against the paper body. All three are flagged
  in their briefs. **Do not quote any of them.**
- **A trap worth recording once:** the `machinedge/building-effective-agents` GitHub file is a
  rewritten derivative of Anthropic's post, not Anthropic's text, and its plausible-sounding figures
  are not Anthropic's. Exactly the failure `cards/research-briefs.md` exists to prevent.
- **The domain gap is this pass's real weakness.** The two strongest controlled single-versus-multi
  comparisons are multi-hop reasoning and mixed benchmarks [8][9]; the best coding-specific evidence
  is institutional or historical. Hedge coding claims to the *shape* of a finding, not its figure.
- **Nobody has measured the context tax.** Both Claude Code and Cursor assert that a fresh subagent
  may be slower [1][2]; neither quantifies it, and no third party has. Do not invent a number.

## Flagged as likely stale within twelve months

Rank-ordered by how fast it will rot.

| Claim | Why it rots | Hedge |
|---|---|---|
| The parallel-agent tooling table | Crystal is dead and Vibe Kanban is sunsetting, both within a year of being widely recommended | Name tools as instances of a pattern, per the book's non-goal on tool-named sections |
| METR time-horizon figures | Doubling time of 88.6 days since 2024 — the fastest-rotting number in the pass | Cite the doubling, not the horizon |
| SWE-bench leaderboard scores | Recomputed continuously | Date and name the subset, or describe the ranking's shape |
| Funding and adoption figures (n8n, LangChain) | Two n8n rounds in nine months; all vendor-reported | Attribute and date, or cut — no argument depends on them |
| Framework version numbers and product names | LangGraph Platform was renamed within days of 1.0 | Describe the thing; name it once, parenthetically |
| Subagent frontmatter field lists and caps | Claude Code added fields across 2026 point releases | Give the two required fields; treat the rest as a category |
| Benchmark degradation figures (pass^8 <25%, 39% drop, 19% meltdown) | Model-generation-specific | Name model and date; prefer the shape, which is robust |
| Conflict rates (19.8% / 41.7%) | Mid-2026 dataset, that generation of agents | Quote with sample size and date; the *ratio* is the durable finding |
| "The Task tool" | Renamed to `Agent` in v2.1.63; alias still works | Say `Agent` |

Durable for the life of the book: the workflow-versus-agent definitions and the six named patterns;
the removability test; the reversibility-and-horizon split rule; the read/write axis on shared
context; the collision taxonomy; `git worktree` mechanics and the shared-hooks finding; and
"checkpoints are not durable execution."

## Concrete examples we can lift

One per brief, each written to drop into a *Worked example* heading. Full versions in the subject
files; the point here is that **they do not collide**, so a suite author can take all three
Orchestration plays from this pass without repeating a scenario.

| Play | Example | Where |
|---|---|---|
| *Decompose into subagents* | Cross-package API migration audit — four read-only scouts with `tools: Read, Glob, Grep`, all writes single-threaded in the parent, and a `rg -c` cross-check that catches the fan-out lying | [`subagents.md`](subagents.md) |
| *Make the control flow deterministic* | The refund agent with a $500 approval threshold, written twice — twenty lines of LangGraph versus 150–250 lines of your own — ending on the beat that **neither version detects the crash** | [`langchain-langgraph.md`](langchain-langgraph.md) |
| *Make the control flow deterministic* (alt) | Support triage in n8n, and the exact point it outgrows the canvas: the canvas owns the edges, the code owns the judgement | [`visual-workflow-tools.md`](visual-workflow-tools.md) |
| *Make the control flow deterministic* (alt) | Dependency upgrades across 40 services — genuinely arguable both ways, tipped by reversibility and horizon | [`control-flow.md`](control-flow.md) |
| *Work in parallel without collisions* | Three agents, three directories, three migrations with distinct filenames, a clean merge, and a `NoMethodError` in production | [`parallel-agents-and-collisions.md`](parallel-agents-and-collisions.md) |

**A note for whoever writes the suite.** The migration-ordering collision and the
rename/add-call-site collision are the two sharpest artefacts in this pass, and they are both in the
same worked example. That is deliberate — they happen together in real life — but if *Work in
parallel without collisions* needs to shed material, the rename case stands alone perfectly well and
the migration case is a natural second play or a Part III failure mode.

## Sources

Consolidated. Each subject brief carries its own full list; these are the sources cited in this hub.
Suffixed numbers (`1a`, `6b`) disambiguate where a subject brief numbers a different source the
same.

[1] Create custom subagents, Claude Code docs — https://code.claude.com/docs/en/sub-agents —
    accessed 19 September 2026
[1a] Building effective agents, Anthropic, 19 December 2024 —
     https://www.anthropic.com/engineering/building-effective-agents — accessed 19 September 2026
[1b] LangGraph overview — https://docs.langchain.com/oss/python/langgraph/overview — accessed
     19 September 2026
[1c] git-worktree documentation — https://git-scm.com/docs/git-worktree — accessed 19 September 2026
[2] Subagents, Cursor docs — https://cursor.com/docs/subagents.md — accessed 19 September 2026
[2b] n8n `LICENSE.md` (Sustainable Use License v1.0) —
     https://github.com/n8n-io/n8n/blob/master/LICENSE.md — accessed 19 September 2026
[2c] Run parallel sessions with worktrees, Claude Code docs —
     https://code.claude.com/docs/en/worktrees — accessed 19 September 2026
[3] A practical guide to building agents, OpenAI, 2025 (PDF) —
    https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf —
    accessed 19 September 2026
[3b] Sustainable Use License / n8n Community license — https://docs.n8n.io/n8n-community-license/ —
     accessed 19 September 2026
[5c] Git worktrees are not an isolation boundary for coding agents, Fletch, 30 July 2026 —
     https://fletch.sh/blog/git-worktrees-vs-clones-for-ai-agents/ — accessed 19 September 2026
[6] How we built our multi-agent research system, Anthropic, 13 June 2025 —
    https://www.anthropic.com/engineering/multi-agent-research-system — accessed 19 September 2026
[6b] LangGraph persistence — https://docs.langchain.com/oss/python/langgraph/persistence — accessed
     19 September 2026
[6b'] Announcing SAP's strategic investment in n8n, 12 May 2026 — https://blog.n8n.io/n8n-sap/ —
      accessed 19 September 2026 — **press release**
[7b] LangGraph interrupts — https://docs.langchain.com/oss/python/langgraph/interrupts — accessed
     19 September 2026
[8] Single-Agent LLMs Outperform Multi-Agent Systems on Multi-Hop Reasoning Under Equal Thinking
    Token Budgets, arXiv 2604.02460, 2 April 2026 — https://arxiv.org/abs/2604.02460 — accessed
    19 September 2026
[8b] Durability, LangChain reference —
     https://reference.langchain.com/python/langgraph/types/Durability — accessed 19 September 2026
[9] Do More Agents Help? Controlled and Protocol-Aligned Evaluation of LLM Agent Workflows,
    arXiv 2606.05670, 4 June 2026 — https://arxiv.org/abs/2606.05670 — accessed 19 September 2026
[10] Results and Retrospective Analysis of the CODS 2025 AssetOpsBench Challenge, arXiv 2605.08518,
     8 May 2026 — https://arxiv.org/abs/2605.08518 — accessed 19 September 2026
[11] Building effective agents, Anthropic — see [1a]
[13b] LangChain Series B, 20 October 2025 — https://www.langchain.com/blog/series-b — accessed
      19 September 2026 — **vendor-reported**
[13b'] We Didn't Migrate from n8n to Python Because n8n Failed, 11 May 2026 —
       https://dev.to/josephyeo/we-didnt-migrate-from-n8n-to-python-because-n8n-failed-k9j —
       accessed 19 September 2026
[15] Why we no longer use LangChain for building our AI agents, Octomind, June 2024 —
     https://octomind.dev/blog/why-we-no-longer-use-langchain-for-building-our-ai-agents —
     **fetch failed 19 September 2026; unverified against primary**
[15a] Effective context engineering for AI agents, Anthropic, 29 September 2025 —
      https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents — accessed
      19 September 2026
[16] Harness design for long-running application development, Anthropic, 24 March 2026 —
     https://www.anthropic.com/engineering/harness-design-long-running-apps — accessed
     19 September 2026
[16c] AI Agent Pull Requests on GitHub: Frequency, Structure, and Merge Conflict Rates,
      submitted 6 July 2026 — https://arxiv.org/html/2607.04697v2 — accessed 19 September 2026
[17] Don't Build Multi-Agents, Walden Yan, Cognition, 12 June 2025 —
     https://cognition.com/blog/dont-build-multi-agents — accessed 19 September 2026
[17c] CodeCRDT: Observation-Driven Coordination for Multi-Agent LLM Code Generation,
      18 October 2025 — https://arxiv.org/abs/2510.18893 — accessed 19 September 2026
[18] Multi-Agents: What's Actually Working, Walden Yan, Cognition, 22 April 2026 —
     https://cognition.com/blog/multi-agents-working — accessed 19 September 2026
[18b] Checkpoints Are Not Durable Execution, Diagrid —
      https://www.diagrid.io/blog/checkpoints-are-not-durable-execution-why-langgraph-crewai-google-adk-and-others-fall-short-for-production-agent-workflows
      — accessed 19 September 2026 — **vendor-adjacent**
[18c] Merge conflicts with parallel AI agents: partition first, SanuDesk, 5 August 2026 —
      https://sanudesk.com/blog/merge-conflicts-parallel-ai-agents — accessed 19 September 2026
[21] OpenAI Agents SDK (Python) — https://openai.github.io/openai-agents-python/ — accessed
     19 September 2026
[22] CrewAI introduction — https://docs.crewai.com/en/introduction — accessed 19 September 2026
