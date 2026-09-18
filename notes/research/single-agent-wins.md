# When one capable agent beats the orchestration — the credibility material

**Question asked:** where does a single agent, or plain code, demonstrably beat a multi-agent system
or an orchestration framework? The book needs at least two defensible cases so the Orchestration
suite does not read as framework marketing.

**Researched:** 19 September 2026
**Confidence:** high on the empirical comparisons (arXiv papers with stated methods and sample
sizes); high on the vendor quotations; medium on how far the results generalise to coding, which is
the book's domain and is under-represented in the evidence.

Feeds the **Orchestration** suite as the counterweight to every other brief in this pass, and
supplies *Know when not to use an agent* in the **Economics** suite.

**Six cases were found. Five survive scrutiny. They are ranked below with their weaknesses stated,
because a case the reader can puncture is worse than no case.**

## The strongest cases, ranked

### 1. Protocol-matched comparison: five of six multi-agent systems lost to a single agent

Fu et al., "Do More Agents Help? Controlled and Protocol-Aligned Evaluation of LLM Agent Workflows,"
arXiv 2606.05670, submitted **4 June 2026**. Ten benchmarks, GPT-4.1, with a shared "benchmark
loader, tool access, answer contract, usage accounting, and trajectory logging" — which is the
point, because unmatched harnesses are how most multi-agent wins are manufactured. Of **six**
multi-agent systems, **only one** exceeded the single-agent baseline; the other **five
underperformed by 2.56–11.29 percentage points while costing more**. A Claude-Code-style runtime
workflow reached **66.72%** overall accuracy on GAIA. [9]

*Why it is credible:* the controls are the contribution, and the deltas are stated with direction
and magnitude. *Weakness:* GPT-4.1 only, and June 2026 is recent enough to have no citation record
yet.

### 2. Multi-agent failure is structural, not a capability shortfall

"Why Do Multi-Agent LLM Systems Fail?" (MAST), arXiv 2503.13657; v1 **17 March 2025**, v3 **26
October 2025**. The abstract opens with the sentence the book wants: **"Despite enthusiasm for
Multi-Agent LLM Systems (MAS), their performance gains on popular benchmarks are often minimal."**
[6]

The figures: **14** unique failure modes in **3** categories — system design issues, inter-agent
misalignment, task verification. The taxonomy was built from **150** traces with inter-annotator
agreement **kappa = 0.88**; MAST-Data holds **1,642** annotated traces across **7** frameworks
(ChatDev, MetaGPT, HyperAgent, AppWorld, AG2, Magentic-One, OpenManus). [7]

Two things to quote carefully. Category incidence is given as "FC1. System Design Issues
(11.8%-15.7%), FC2. Inter-Agent Misalignment (0.85%-13.2%), FC3. Task Verification (6.2%-9.1%)" —
these are per-failure-mode ranges *within* a category, **not** category totals. Do not write "X% of
failures are coordination." [7] And the intervention result is the genuinely damning one: on
ProgramDev with GPT-4o, "a straightforward system workflow adjustment ensuring the CEO had the final
say contributed to a **+9.4%** increase in overall task success rate" [7] — a targeted structural
fix bought under ten points, which the authors use to argue that MAS needs "structural redesigns"
rather than prompt patches. Their baseline sentence: MAS "performance gains often remain minimal
compared to single-agent frameworks or simple baselines like best-of-N sampling." [7]

*Why it is credible:* 1,642 traces, seven frameworks, a published kappa. *Weakness:* the frameworks
studied are 2023–24-era, so a critic can say it indicts ChatDev and MetaGPT rather than multi-agency
as such. Pre-empt that in the prose rather than waiting for it.

### 3. The benchmark community removed the scaffolding on purpose

The SWE-bench Verified LM-comparison track now states: "We evaluate all LMs using mini-SWE-agent in
a minimal bash environment. **No tools, no special scaffold structure; just a simple ReAct agent
loop.**" [3] Simon Willison's reading: the standardisation means "the quality of the different
harnesses or optimized prompts is not being measured here," and the February 2026 results "weren't
self-reported by the labs." [4]

The February 2026 Bash Only leaderboard, on the 500-sample Verified subset: Claude 4.5 Opus (high
reasoning) **76.8%**; Gemini 3 Flash (high) **75.8%**; MiniMax M2.5 (high) **75.8%**; Claude Opus
4.6 **75.6%**; GLM-5 (high) **72.8%**; GPT-5.2 sixth at **72.8%**. [4]

*Why it is credible:* it is an institutional decision by the people who run the benchmark, not an
opinion. *Weakness, and it is a real one:* this is a methodological choice about comparing *models*
fairly. It shows the community concluded scaffolding differences were noise obscuring the signal —
it does not, by itself, show that simple loops beat complex ones at doing work. Use it for the first
claim only.

### 4. Single-agent matches or beats multi-agent at equal thinking-token budget

Tran & Kiela, "Single-Agent LLMs Outperform Multi-Agent Systems on Multi-Hop Reasoning Under Equal
Thinking Token Budgets," arXiv 2604.02460, submitted **2 April 2026**, revised 11 April 2026.
Verbatim: "SAS consistently match or outperform MAS on multi-hop reasoning tasks when reasoning
tokens are held constant." Three model families: Qwen3, DeepSeek-R1-Distill-Llama, Gemini 2.5. The
authors attribute reported multi-agent advantages to "unaccounted computation and context effects
rather than inherent architectural superiority." [8]

*Why it is credible:* it isolates the confound — most multi-agent wins are a bigger compute budget
wearing a hat. *Weakness:* multi-hop reasoning, not coding; it does not transfer without hedging.

### 5. mini-SWE-agent — great rhetoric, needs one qualification

The repo tagline: "The 100 line AI agent that solves GitHub issues… scores >74% on SWE-bench
verified!" and the body claims "Just some 100 lines of python for the agent class," plus roughly
"100 total for env, model, script." [1] The docs site news item reads "Nov 19: Gemini 3 Pro reaches
74% on SWE-bench verified with mini-swe-agent!" [2] The repo positions mini as "100x simpler, and
still worked nearly as well" than the original SWE-agent, with "no tools other than bash,"
`subprocess.run` per action, and "completely linear history." [1]

**Do not repeat "mini-SWE-agent is 100 lines" unqualified.** The researching agent verified against
source at commit `04d809c` (2026-09-03): `src/minisweagent/agents/default.py` is **190 lines** (171
non-blank, non-comment); `src/minisweagent/` is **5,349 lines**; the full repo including tests is
**15,028 lines**. Simon Willison describes it as "approximately 9,000 lines of Python" [4] — a
fourth figure. All are defensible depending on what you count. **The honest framing is "a ~190-line
agent loop inside a ~5,000-line package," and the load-bearing claim is the loop.**

*Why it is credible:* the score is real and the loop genuinely is tiny. *Weakness:* the line count
is exactly the sort of claim a reviewer checks, and the book loses more from getting it wrong than
it gains from the rhetorical punch.

### 6. Agentless — the original version of the question

"Agentless: Demystifying LLM-based Software Engineering Agents," Xia, Deng, Dunn, Zhang; v1 **1 July
2024**, v2 29 October 2024. Verbatim: "the simplistic Agentless is able to achieve both the highest
performance (**32.00%**, 96 correct fixes) and low cost (**$0.70**) compared with all existing
open-source software agents!" It uses "a simplistic three-phase process of localization, repair, and
patch validation, **without letting the LLM decide future actions or operate with complex tools**."
[5]

*Why it is credible:* it is the paper that framed the question, and the phrasing is quotable.
*Weakness, and it is disqualifying for any performance claim:* SWE-bench Lite, mid-2024, and 32% is
far below current numbers. **Use it as a historical argument about scaffolding versus models, never
as a current performance claim.**

## Anthropic and OpenAI, arguing for simplicity in their own words

The most useful citations in the whole pass, because they come from the vendors who benefit from
complexity. All from "Building effective agents," **19 December 2024**: [11]

> Frameworks "often create extra layers of abstraction that can obscure the underlying prompts ​​and
> responses, making them harder to debug."

> "We suggest that developers start by using LLM APIs directly: many patterns can be implemented
> in a few lines of code."

> "If you do use a framework, ensure you understand the underlying code. Incorrect assumptions about
> what's under the hood are a common source of customer error."

> "For many applications, however, optimizing single LLM calls with retrieval and in-context
> examples is usually enough."

That last one is the *Know when not to use an agent* play's epigraph, and it is Anthropic's.

## Latency and cost — a real measurement that cuts both ways

Patel et al., "Results and Retrospective Analysis of the CODS 2025 AssetOpsBench Challenge," arXiv
2605.08518, submitted **8 May 2026**: "Despite requiring orchestration across multiple domain
agents, their token consumption (63K) is lower than single-agent WO scenarios. Yet their wall-clock
duration (203 seconds) is the highest of any domain, substantially exceeding the WO duration (145
seconds). This dissociation between token count and wall-clock duration exposes an orchestration
latency cost that token counts alone do not capture." [10]

**Report the other half or the citation is dishonest:** "Single-agent executions consume nearly
twice the tokens of multi-agent executions on average (121K vs. 63K, t = 7.18, p < 0.001)" — which
the authors attribute to scenario-pool composition rather than architecture. [10] So in this study
multi-agent was roughly **40% slower in wall-clock** but **cheaper in tokens**. Use it as a latency
point only, and say both halves. A book that quotes the convenient half of a two-sided result has
forfeited the credibility this brief exists to buy.

## The trend line

METR Time Horizon 1.1, published **29 January 2026**: best model Claude Opus 4.5 at a 50% time
horizon of **320 [170,729] minutes**; doubling time **196.5 days** all-time, **88.6 days** from 2024
onward. [12] The honest inference is modest: tasks that needed decomposition last year increasingly
do not, so scaffolding built to work around a capability gap has a depreciation schedule.

**Do not overstate this with Anthropic's help, because Anthropic declines to give it.** "Effective
harnesses for long-running agents" (26 November 2025) says plainly: "it's still unclear whether a
single, general-purpose coding agent performs best across contexts, or if better performance can be
achieved through a multi-agent architecture." [13] Cite it as an open question. It is the fairest
sentence either side has produced.

## The two cases the book should actually lead with

The commission asked for at least two. These are the two, chosen for being both defensible and
*legible to a working developer*:

**Case one — the framework you removed was doing less than you thought.** Anthropic's own advice is
to start with the API directly [11]; Octomind removed LangChain after twelve months in production
and shipped modular components instead (see [`langchain-langgraph.md`](langchain-langgraph.md) — and
note its primary page was unreachable this pass); and the measured comparison says five of six
multi-agent systems lost to a single agent under matched protocol [9]. The play is not "frameworks
are bad." It is that the abstraction is only worth its debugging cost when it is buying you
something you would otherwise have to build — which, for LangGraph, is resumability, and for most
teams is nothing.

**Case two — the fan-out was a compute budget in a costume.** Multi-agent advantages shrink or
disappear when thinking tokens are held constant [8]; five of six systems cost more *and* scored
worse under matched accounting [9]; multi-agent orchestration ran 40% slower in wall clock in the
one study that measured latency separately [10]; and the largest failure taxonomy finds gains "often
minimal" with 14 named ways the coordination itself breaks [6][7]. Before adding an agent, spend the
same tokens on one and measure. That is a checklist item, and it is cheap.

A third is available if a play needs it: **parallel coding agents are unmeasured**, and the merge
cost is real and under-counted — see
[`parallel-agents-and-collisions.md`](parallel-agents-and-collisions.md) for the 19.8%/41.7%
conflict rates and their author's "conservative lower bound" caveat.

## Contradictions and gaps

- **Anthropic does not endorse "single agent wins."** The December 2024 post argues for *simplicity*
  [11]; the November 2025 harness post leaves single-versus-multi explicitly open [13]. Quoting the
  first without the second would be exactly the selective-citation move this brief is meant to guard
  against.
- **AssetOpsBench contradicts the naive cost story** — multi-agent used *fewer* tokens there. [10]
  Latency only.
- **mini-SWE-agent's line count has four published values.** [1][4] Qualify it.
- **The framework-removal genre has no credible successor to Octomind.** Everything found from
  2025–26 in that genre is SEO content or unattributed posts. The book should either lean on
  Octomind alone *and say the genre is thin*, or drop the claim that removal is a trend. It should
  not imply a movement that the sourcing does not support.
- **Explicitly unusable, flagged so nobody re-finds it and trusts it:** the dev.to post "Why We
  Ripped Out Our Orchestration Frameworks" [14] — unnamed author, unnamed company, and claims
  ("codebase shrank by thousands of lines," "inference latency dropped by nearly thirty percent")
  with no data. **Do not cite.** Likewise a 2026 Databricks "327% increase in multi-agent workflow
  usage" figure that could not be confirmed at primary source.
- **The domain gap is the real weakness of this brief.** The two strongest controlled comparisons
  [8][9] are multi-hop reasoning and mixed benchmarks. The best coding-specific evidence is
  institutional [3][4] or historical [5]. A play making a coding claim should hedge to the shape of
  the finding, not the figure.

## Staleness assessment

| Claim | Why it rots | Hedge |
|---|---|---|
| SWE-bench leaderboard scores | Recomputed continuously; these are February 2026 | Date the sentence and name the subset, or describe the ranking's shape |
| METR time-horizon figures | Doubling time of 88.6 days since 2024 — this is the single fastest-rotting number in the pass | Cite the *doubling*, not the horizon; the trend is the argument |
| "Five of six MAS underperformed" | GPT-4.1, June 2026 | Attribute with model and date; the matched-protocol *method* is the durable contribution |
| mini-SWE-agent line counts | Repo under active development | Say "a ~190-line agent loop at the commit we checked," or describe it qualitatively |
| MAST's frameworks | 2023–24-era systems | Name them; let the reader judge the generalisation |
| Agentless's 32.00% / $0.70 | Mid-2024, SWE-bench Lite | Use only as history, always with the date |
| Anthropic's "start with the API directly" | December 2024 vendor advice, unretracted | Safe, and the most quotable thing here |

Durable for the life of the book: the compute-confound argument (hold tokens constant before
believing a fan-out win); coordination as a distinct failure surface with a named taxonomy; the
vendors' own preference for simplicity; and the removability test from
[`control-flow.md`](control-flow.md), which is what turns all of this into advice rather than
scepticism.

## Sources

[1] SWE-agent/mini-swe-agent — https://github.com/SWE-agent/mini-swe-agent — accessed
    19 September 2026 — line counts independently verified at commit `04d809c`, 2026-09-03
[2] mini-SWE-agent documentation — https://mini-swe-agent.com/latest/ — accessed 19 September 2026
[3] SWE-bench Verified — https://www.swebench.com/verified.html — accessed 19 September 2026
[4] SWE-bench February 2026 leaderboard update, Simon Willison —
    https://simonwillison.net/2026/Feb/19/swe-bench/ — accessed 19 September 2026
[5] Agentless: Demystifying LLM-based Software Engineering Agents, arXiv 2407.01489, v1 1 July 2024 —
    https://arxiv.org/abs/2407.01489 — accessed 19 September 2026
[6] Why Do Multi-Agent LLM Systems Fail?, arXiv 2503.13657, v1 17 March 2025 —
    https://arxiv.org/abs/2503.13657 — accessed 19 September 2026
[7] Same paper, full text v3, 26 October 2025 — https://arxiv.org/html/2503.13657v3 — accessed
    19 September 2026
[8] Single-Agent LLMs Outperform Multi-Agent Systems on Multi-Hop Reasoning Under Equal Thinking
    Token Budgets, arXiv 2604.02460, 2 April 2026 — https://arxiv.org/abs/2604.02460 — accessed
    19 September 2026
[9] Do More Agents Help? Controlled and Protocol-Aligned Evaluation of LLM Agent Workflows,
    arXiv 2606.05670, 4 June 2026 — https://arxiv.org/abs/2606.05670 — accessed 19 September 2026
[10] Results and Retrospective Analysis of the CODS 2025 AssetOpsBench Challenge, arXiv 2605.08518,
     8 May 2026 — https://arxiv.org/abs/2605.08518 — accessed 19 September 2026 — figures from
     Appendix G
[11] Building effective agents, Anthropic, 19 December 2024 —
     https://www.anthropic.com/engineering/building-effective-agents — accessed 19 September 2026
[12] Time Horizon 1.1, METR, 29 January 2026 — https://metr.org/blog/2026-1-29-time-horizon-1-1/ —
     accessed 19 September 2026
[13] Effective harnesses for long-running agents, Anthropic, 26 November 2025 —
     https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents — accessed
     19 September 2026
[14] Why We Ripped Out Our Orchestration Frameworks, dev.to —
     https://dev.to/alaikrm/why-we-ripped-out-our-orchestration-frameworks-4o3j — accessed
     19 September 2026 — **flagged unusable: unattributed, no data. Do not cite**
[15] Why we no longer use LangChain for building our AI agents, Octomind, June 2024 —
     https://octomind.dev/blog/why-we-no-longer-use-langchain-for-building-our-ai-agents —
     **primary unreachable; see `langchain-langgraph.md`**
