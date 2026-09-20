# Control flow — when to script the orchestration and when to let the model decide

**Question asked:** what the actual decision criteria are for putting orchestration in code rather
than leaving it to the model, and what evidence supports them.

**Researched:** 19 September 2026
**Confidence:** high on the vendor framings (Anthropic's and OpenAI's texts are primary and
quotable); high on the empirical degradation results (peer-reviewable arXiv papers with stated
figures); medium on the synthesis, because no source states a complete criteria table and the
assembly below is partly ours.

Feeds the **Orchestration** suite, chiefly *Make the control flow deterministic*. This is the
brief that most directly supplies a play's *Problem* and *Checklist* headings.

## Findings

### The canonical framing, still unreplaced

Anthropic's **"Building effective agents"** was published **19 December 2024** and is still live.
[1][2] It now carries a header note — "Note: Much of the tooling landscape described in this post has
changed since December 2024" — which is a tooling caveat, not a retraction of the framing. [1]

The definitions, verbatim: workflows are "systems where LLMs and tools are orchestrated through
predefined code paths"; agents are "systems where LLMs dynamically direct their own processes and
tool usage, maintaining control over how they accomplish tasks." [1]

The named workflow patterns, which give the book a ready-made vocabulary: **prompt chaining**
(sequential steps with programmatic checks at intermediate stages), **routing** ("Routing classifies
an input and directs it to a specialized followup task"), **parallelisation** in two forms —
*sectioning* (independent subtasks) and *voting* (the same task run several times) —
**orchestrator-workers** (a central LLM decomposes, delegates, and synthesises), and
**evaluator-optimiser** (a generate/critique loop). [1]

The three sentences most worth lifting: [1]

> "When building applications with LLMs, we recommend finding the simplest solution possible, and
> only increasing complexity when needed."

> "Workflows offer predictability and consistency for well-defined tasks, whereas agents are the
> better option when flexibility and model-driven decision-making are needed at scale."

> "Agents can be used for open-ended problems where it's difficult or impossible to predict the
> required number of steps, and where you can't hardcode a fixed path."

And the trade, stated plainly: "Agentic systems often trade latency and cost for better task
performance," with "The autonomous nature of agents means higher costs, and the potential for
compounding errors." [1] **Anthropic names compounding errors and gives no numbers.** The numbers
below come from elsewhere.

### OpenAI draws the same line, with sharper criteria

OpenAI defines agents as "systems that independently accomplish tasks on your behalf" and explicitly
excludes "simple chatbots, single-turn LLMs, or sentiment classifiers" because they "don't use them
to control workflow execution." [3, p.4] That makes *control of workflow execution* the definitional
boundary — the same line Anthropic draws, from the other side.

The three qualifying signals, verbatim: [3, p.6]

- **Complex decision-making:** "Workflows involving nuanced judgment, exceptions, or
  context-sensitive decisions, for example refund approval in customer service workflows."
- **Difficult-to-maintain rules:** "Systems that have become unwieldy due to extensive and intricate
  rulesets, making updates costly or error-prone, for example performing vendor security reviews."
- **Heavy reliance on unstructured data:** "Scenarios that involve interpreting natural language,
  extracting meaning from documents, or interacting with users conversationally."

And the kill criterion, which is the single most useful sentence for a checklist: "Before committing
to building an agent, validate that your use case can meet these criteria clearly. Otherwise, a
deterministic solution may suffice." [3, p.6]

OpenAI also gives a *within-agent* escalation rule that doubles as a decomposition trigger: "Our
general recommendation is to maximize a single agent's capabilities first," splitting only on
**complex logic** ("when prompts contain many conditional statements (multiple if-then-else
branches), and prompt templates get difficult to scale") or **tool overload** — "Some
implementations successfully manage more than 15 well-defined, distinct tools while others struggle
with fewer than 10 overlapping tools." [3, pp.13–16]

Their guardrail taxonomy is "agent decides, code enforces" stated as policy: LLM classifiers layered
with "Rules-based protections: Simple deterministic measures (blocklists, input length limits, regex
filters)," plus **tool safeguards** — rate each tool "low, medium, or high" on "read-only vs. write
access, reversibility, required account permissions, and financial impact," and use that rating to
"trigger automated actions, such as pausing for guardrail checks before executing high-risk
functions or escalating to a human." [3, pp.24–27]

### The reliability evidence

This is where the argument stops being taste.

- **τ-bench** (arXiv 2406.12045, 17 June 2024) introduced `pass^k` — reliability across *k* trials,
  not best-of-*k*. Verbatim: "even state-of-the-art function calling agents (like gpt-4o) succeed on
  <50% of the tasks, and are quite inconsistent (pass^8 <25% in retail)." [4]
- **"LLMs Get Lost In Multi-Turn Conversation"** (arXiv 2505.06120, 9 May 2025) reports "an average
  drop of 39% across six generation tasks" from single-turn to multi-turn, over "200,000+ simulated
  conversations," decomposed into "a minor loss in aptitude and a significant increase in
  unreliability," concluding: "when LLMs take a wrong turn in a conversation, they get lost and do
  not recover." [5]
- **GAIA** (arXiv 2311.12983, 21 November 2023) stratifies difficulty *by step count*: Level 1
  "generally require no tools, or at most one tool but no more than 5 steps"; Level 2 "more steps,
  roughly between 5 and 10"; Level 3 "requiring to take arbitrarily long sequences of actions."
  Headline: "human respondents obtain 92% vs. 15% for GPT-4 equipped with plugins." [6] Per-level
  figures surfaced in search summaries were **not** verified against the paper and must not be used.
- **"The Illusion of Diminishing Returns"** (arXiv 2509.09677, 11 September 2025) is the sharpest
  primary statement of the compounding mechanism, and it cuts *both* ways: "even marginal gains in
  single-step accuracy can compound into exponential improvements in the length of tasks a model can
  successfully complete," alongside "we observe that the per-step accuracy of models degrades as the
  number of steps increases." It also names a **self-conditioning effect** — "models become more
  likely to make mistakes when the context contains their errors from prior turns" — which "does not
  reduce by just scaling the model size," though "thinking mitigates self-conditioning." [7]
- **"Solving a Million-Step LLM Task with Zero Errors"** (arXiv 2511.09030, 12 November 2025) is
  the best existence proof for scripted decomposition. Prior work saw LLMs "become derailed after at
  most a few hundred steps," but extreme decomposition plus multi-agent voting "successfully solves
  a task with over one million LLM steps with zero errors." [8] If the book needs one citation for
  *decomposition buys horizon*, this is it.
- **"Beyond pass@1: A Reliability Science Framework for Long-Horizon LLM Agents"** (arXiv
  2603.29231, 31 March 2026): 10 models, 23,392 episodes, 396 tasks. Reliability decay is
  **domain-stratified** — "SE GDS drops from 0.90 to 0.44 while document processing is nearly flat
  (0.74 to 0.71)" — and, counter-intuitively, "frontier models have the highest meltdown rates (up
  to 19%) because they attempt ambitious multi-step strategies that sometimes spiral." [9]

**A caution on the famous arithmetic.** The 0.95²⁰ ≈ 36% framing is real arithmetic but has **no
tier-1 source**; it appears in practitioner blogs. [10] Use [7] and [8] for the mechanism and treat
the 95%/20-step illustration as a teaching device, explicitly labelled as such.

### Hybrid patterns, named

**12-Factor Agents** (humanlayer) supplies the vocabulary. Exact factor names: 1 Natural Language to
Tool Calls; 2 Own your prompts; 3 Own your context window; 4 Tools are just structured outputs; 5
Unify execution state and business state; 6 Launch/Pause/Resume with simple APIs; 7 Contact humans
with tool calls; **8 Own your control flow**; 9 Compact Errors into Context Window; **10 Small,
Focused Agents**; 11 Trigger from anywhere, meet users where they are; 12 Make your agent a
stateless reducer. [11]

Factor 8's payoff list is exactly the *Checklist* material a play needs: owning the loop lets you
insert summarisation or caching of tool results, LLM-as-judge on structured output, context-window
compaction, logging/tracing/metrics, client-side rate limiting, and durable sleep or wait-for-event
— and, critically, lets you interrupt **between tool selection and tool invocation** for human
review.
[12]

Factor 10 gives the closest thing in the literature to a numeric split rule: **3–10 steps, maybe 20
maximum**, because "as context grows, LLMs are more likely to get lost or lose focus." [13] That
rhymes with [5] and [7] independently, which is why it is worth quoting.

The repo's summary of the end state names the pattern the book should probably adopt: production
agents are "mostly deterministic code, with LLM steps sprinkled in at just the right points." [11]

**Anthropic's code-execution-with-MCP** (4 November 2025) is the same idea one level down — let the
model *write* the control flow rather than *be* it: "Loops, conditionals, and error handling can be
done with familiar code patterns rather than chaining individual tool calls," and "rather than
having to wait for a model to evaluate an if-statement, the agent can let the code execution
environment do this." Reported saving: "from 150,000 tokens to 2,000 tokens—a time and cost saving
of 98.7%." [14]

### The counter-argument, which is strong and comes from the same vendor

**Anthropic argues against itself.** "Effective context engineering for AI agents" (29 September
2025): "We see engineers hardcoding complex, brittle logic in their prompts to elicit exact agentic
behavior. This approach creates fragility and increases maintenance complexity over time," and the
forward-looking claim: "As model capabilities improve, agentic design will trend towards letting
intelligent models act intelligently, with progressively less human curation." [15]

**And then hedges the hedge.** "Harness design for long-running application development" (24 March
2026) builds a *deterministic* planner/generator/evaluator skeleton with enforced context resets —
"compaction alone wasn't sufficient to enable strong long task performance" — while warning: "Every
component in a harness encodes an assumption about what the model can't do on its own, and those
assumptions are worth stress testing." [16] That sentence is the most honest formulation found in
the entire pass, and it converts the whole debate into a design principle: **the scripted piece is a
dated bet, so build it to be removable.**

**Cognition** (12 June 2025) attacks *parallel* model-driven orchestration rather than scripting;
the prescription is a single-threaded linear agent plus a purpose-built context-compression model.
[17]

**The Bitter-Lesson-for-agents argument** circulates widely — hand-built scaffolding as a
depreciating asset — usually relayed via a quote attributed to Boris Cherny that "Scaffolding might
improve performance 10-20%, but those gains get wiped out with the next model generation." [18]
**Flagged: this quote could not be traced to a primary transcript** and is absent from the Root
Access interview. The verifiable adjacent quote from that interview is that users "give it way
overly specific instructions... 'You must do one, then two, then three, then four.' For modern
models, that's actually really not the way to do it." [19] **Use [19], not [18].**

## Decision criteria

Each row traceable to a source. Assembly is ours; no single source states the table.

| Criterion | Favours scripted control flow | Favours model-driven | Source |
|---|---|---|---|
| Are the steps known in advance? | Fixed sequence, known gate conditions | "open-ended problems where it's difficult or impossible to predict the required number of steps" | [1] |
| Task-space enumerability | Ruleset is small and stable | "Difficult-to-maintain rules" — rulesets "unwieldy… making updates costly or error-prone" | [1][3] |
| Nature of the judgement | Deterministic predicates suffice | "nuanced judgment, exceptions, or context-sensitive decisions" | [3] |
| Input modality | Structured records | "Heavy reliance on unstructured data" | [3] |
| Cost of a wrong branch | Write, irreversible, financial — gate it; rate tools "low, medium, or high" on "reversibility… financial impact" | Read-only and cheap to retry | [3] |
| Trajectory length | Beyond ~20 steps, decompose; a million-step task was solved only via extreme decomposition | Short horizons, before per-step accuracy compounds away | [8][13] |
| Reproducibility and auditability | "predictability and consistency"; owning the loop gives logging, tracing, metrics, and pause-before-invoke review | — | [1][12] |
| Latency and cost | "Agentic systems often trade latency and cost for better task performance"; code-side if-statements avoid a model round trip | Accept the trade when performance demands it | [1][14] |
| Is failure detectable? | Programmatic checks between steps (prompt chaining) | Agents suit tasks with verifiable solutions and iterative feedback — verifiability is a precondition either way | [1] |
| Tool surface | ≤~10 overlapping tools: keep one agent | >15 distinct tools, or tool-clarity fixes have not helped | [3] |
| Expected model churn | — | "hardcoding complex, brittle logic… creates fragility"; leave headroom | [15][16] |
| Domain | Software engineering degrades hardest over long horizons (GDS 0.90 → 0.44) | Document processing stays nearly flat (0.74 → 0.71) | [9] |

## Concrete example we can lift

**Dependency-upgrade PRs across a 40-service monorepo.** Chosen because a competent engineer could
genuinely argue it either way, which is what makes it teach rather than demonstrate.

A bot opens a PR bumping a transitive dependency. Something must decide: merge, patch the call
sites, or escalate.

*The scripted reading.* The steps are enumerable — resolve the bump, run the test suite, check the
changelog for breaking changes, merge or escalate. That is prompt chaining with programmatic gates.
[1] Merging to main is a write action with real blast radius, so it lands "high" on OpenAI's tool-risk
rating and wants a code-enforced gate regardless of how good the model is. [3] And at forty services
the trajectory is long: one agent looping over all of them blows past Factor 10's "3-10 steps, maybe
20 steps maximum" [13] into exactly the regime where [5] measures a 39% drop and [7] measures
per-step decay plus self-conditioning on its own earlier errors.

*The model-driven reading.* The hard cases are the interesting ones — a changelog that says
"deprecated, will be removed" in prose, a type error whose fix depends on how *this* service uses
the API. That is "heavy reliance on unstructured data" plus "nuanced judgment, exceptions" [3], and
the rules you would write to cover it are precisely the ruleset that becomes "unwieldy… costly or
error-prone." [3]

*What tips it:* **split on reversibility and horizon, not on difficulty.** A deterministic skeleton
— one pass per service, fixed stages, the test suite as the gate, the merge performed by code [11].
A model-driven *leaf* — a bounded agent invoked only inside the "tests failed, diagnose and patch"
stage, with a step budget inside Factor 10's range [13] and no merge tool in its hands [3]. The loop
stays yours, so you can interrupt between tool selection and invocation for human approval on
anything touching a release branch [12]. Per-service isolation is the decomposition that [8] shows
buys horizon: forty short trajectories rather than one long one.

And the removability test from [16]: if next year's model handles the diagnose-and-patch leaf
without the scaffold, you delete one stage. You do not rewrite the pipeline. A scripted design that
cannot be un-scripted cheaply has failed a test the book should make explicit.

## Contradictions and gaps

- **Anthropic versus Anthropic, and it is not resolvable.** [1] says compounding errors argue for
  guardrails and sandboxes; [15] says hardcoded logic is itself the fragility; [16] splits the
  difference. Record it as a live tension. The reconciliation the book can offer is the removability
  test, not a verdict.
- **The compounding argument runs in both directions.** [7] uses the same multiplicative model to
  argue the *optimistic* case — marginal per-step gains yield exponential horizon growth. [9] adds
  that frontier models have the *highest* meltdown rates (up to 19%) precisely because they attempt
  ambitious strategies. So "better model, therefore safer to hand over control" is not monotonic,
  and any play implying it is will age badly in an embarrassing direction.
- **Domain dependence undercuts any universal rule.** [9]: software-engineering GDS 0.90 → 0.44
  versus document processing 0.74 → 0.71. A criteria table that ignores domain overfits to coding —
  which, for this book, is the relevant domain, but the caveat should be stated once.
- **Unverified, do not use:** the 0.95²⁰ ≈ 36% illustration has no tier-1 source [10]; the Cherny
  "10–20%" quote has no primary transcript [18]; GAIA per-level GPT-4 figures [6]; a claimed OpenAI
  "Agent Builder shuts down 30 Nov 2026" and a "skip the agent when latency must be under 500ms"
  heuristic, both third-party summaries only.
- **A trap worth recording:** the `machinedge/building-effective-agents` GitHub file is a
  **rewritten derivative**, not Anthropic's text. Its plausible-sounding quotes ("10–50× cost", "1–5
  min") are not Anthropic's and must never be attributed to them. This is precisely the failure the
  citation rules in [`cards/research-notes.md`](../../cards/research-notes.md) exist to prevent.
- **Gap:** no source states compliance or audit requirements as an explicit scripted-versus-agentic
  criterion. [1] and [12] get you predictability and traceability; the regulatory leap is ours and
  should be labelled as inference if the book makes it.

## Staleness assessment

| Claim | Why it rots | Hedge |
|---|---|---|
| The Bitter-Lesson position (scaffolding is a depreciating asset) | Depends entirely on the next model release | Frame as the live bet it is; give the removability test rather than a verdict |
| Benchmark figures (pass^8 <25%, 39% drop, 19% meltdown) | Model-generation-specific | Name model and date in the sentence; prefer the *shape* — degradation with horizon — which is robust |
| "≤10 overlapping tools / >15 distinct tools" | An observation about 2025 implementations | Quote OpenAI's hedged phrasing, which already hedges itself |
| Factor 10's "3-10 steps, maybe 20" | A practitioner heuristic, not a measurement | Attribute to 12-Factor Agents; do not present as a finding |
| Anthropic's 98.7% token saving | One reported case | Attribute and date; the mechanism is the point |
| The workflow/agent definitions themselves | December 2024 and still standard vocabulary | Safe. This is the most durable thing in the brief |

Durable for the life of the book: the workflow-versus-agent definitions; the six named patterns;
"own your control flow"; the reversibility-and-horizon split rule; the removability test; and the
finding that per-step reliability degrades with trajectory length regardless of which direction you
argue from it.

## Sources

[1] Building effective agents, Anthropic, 19 December 2024 —
    https://www.anthropic.com/engineering/building-effective-agents — accessed 19 September 2026
[2] Engineering at Anthropic (post index; publication dates verified here) —
    https://www.anthropic.com/engineering — accessed 19 September 2026
[3] A practical guide to building agents, OpenAI, 2025 (PDF) —
    https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf —
    accessed 19 September 2026
[4] τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains, arXiv 2406.12045,
    17 June 2024 — https://arxiv.org/abs/2406.12045 — accessed 19 September 2026
[5] LLMs Get Lost In Multi-Turn Conversation, arXiv 2505.06120, 9 May 2025 —
    https://arxiv.org/abs/2505.06120 — accessed 19 September 2026
[6] GAIA: A Benchmark for General AI Assistants, arXiv 2311.12983, 21 November 2023 —
    https://arxiv.org/abs/2311.12983 — accessed 19 September 2026
[7] The Illusion of Diminishing Returns: Measuring Long Horizon Execution in LLMs, arXiv 2509.09677,
    11 September 2025 — https://arxiv.org/abs/2509.09677 — accessed 19 September 2026
[8] Solving a Million-Step LLM Task with Zero Errors, arXiv 2511.09030, 12 November 2025 —
    https://arxiv.org/abs/2511.09030 — accessed 19 September 2026
[9] Beyond pass@1: A Reliability Science Framework for Long-Horizon LLM Agents, arXiv 2603.29231,
    31 March 2026 — https://arxiv.org/abs/2603.29231 — accessed 19 September 2026
[10] The Compound Accuracy Problem: Why Your 95% Accurate Agent Fails 40% of the Time —
     https://tianpan.co/blog/2026/04/20/compound-accuracy-multi-step-agent-pipelines — accessed
     19 September 2026 — **non-authoritative; illustration only**
[11] 12-Factor Agents, humanlayer — https://github.com/humanlayer/12-factor-agents — accessed
     19 September 2026
[12] Factor 8: Own your control flow —
     https://github.com/humanlayer/12-factor-agents/blob/main/content/factor-08-own-your-control-flow.md
     — accessed 19 September 2026
[13] Factor 10: Small, Focused Agents —
     https://raw.githubusercontent.com/humanlayer/12-factor-agents/main/content/factor-10-small-focused-agents.md
     — accessed 19 September 2026
[14] Code execution with MCP: building more efficient agents, Anthropic, 4 November 2025 —
     https://www.anthropic.com/engineering/code-execution-with-mcp — accessed 19 September 2026
[15] Effective context engineering for AI agents, Anthropic, 29 September 2025 —
     https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents — accessed
     19 September 2026
[16] Harness design for long-running application development, Anthropic, 24 March 2026 —
     https://www.anthropic.com/engineering/harness-design-long-running-apps — accessed
     19 September 2026
[17] Don't Build Multi-Agents, Walden Yan, Cognition, 12 June 2025 —
     https://cognition.com/blog/dont-build-multi-agents — accessed 19 September 2026
[18] The Bitter Lesson of Agentic Coding, Peter Zatloukal, April 2026 —
     https://agent-hypervisor.ai/posts/bitter-lesson-of-agentic-coding/ — accessed
     19 September 2026 — **quote attribution unverified; do not quote the 10–20% figure**
[19] Boris Cherny: Building Claude Code, Root Access, 27 July 2026 —
     https://www.ycrootaccess.com/p/boris-cherny-building-claude-code — accessed 19 September 2026
[20] Measuring AI Ability to Complete Long Software Tasks, METR, 19 March 2025 —
     https://metr.org/blog/2025-03-19-measuring-ai-ability-to-complete-long-tasks/ — accessed
     19 September 2026 — **surfaced via search; see `single-agent-wins.md` for the current
     Time Horizon 1.1 figures**
