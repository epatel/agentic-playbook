# Code health and agents

**Question asked:** does structural code health (CodeScene's Code Health and similar maintainability
measures) change how well coding agents work, and does feeding a structural signal back to the agent
improve the code it leaves? Which of the evidence is independent, and which is the vendor's?

**Researched:** 7 November 2026
**Confidence:** high that agent adoption raises complexity and that agents regress code over long
maintenance (one independent peer-reviewed study, one independent benchmark). **Low** that code
health changes how often a *frontier* agent breaks code: the one controlled study found no
significant difference for Claude Sonnet 4.5 or Claude Code. **Low** on every token-cost figure:
vendor-only, inconsistent between the vendor's own posts. No study tests the feedback loop itself
(health signal in the loop vs not) on outcomes.

Prompted by Adam Tornhill (CodeScene founder and CTO), *AI-Friendly Code: The Missing Link for
Speed with Quality*, GOTO Copenhagen 2026, uploaded 4 November 2026 [1]. **The talk is a secondary
source for every study it cites.** Several of its figures do not match the papers; see *Talk vs
source* below. Feeds the **Verification and trust** suite (a structural signal), Part III (*Code an
agent keeps extending gets worse on every pass*, *The one direct test of codebase damage*, the
Endless Polish), Part IV (*Refactoring a codebase for agents*, *What would change this position*)
and the Economics suite.

Already covered elsewhere, not repeated here: SlopCodeBench and GitClear in
[`failure-modes.md`](failure-modes.md); Borg et al. *Echoes of AI* and the GitHub Copilot quality
RCT in [`productivity-evidence.md`](productivity-evidence.md).

## Findings

### Independent: adoption raises complexity, and the speed-up fades

- **He, Miller, Agarwal, Kästner and Vasilescu (Carnegie Mellon), MSR 2026**, *Speed at the Cost of
  Quality: How Cursor AI Increases Short-Term Velocity and Long-Term Complexity* (arXiv 2511.04427,
  first titled *Does AI-Assisted Coding Deliver?*), peer-reviewed. [2]
  - Sample: **806 GitHub repositories** (≥10 stars) that adopted Cursor, adoption dates January 2024
    to March 2025, against propensity-matched non-adopters; staggered difference-in-differences.
    (v2 of the preprint says 807.)
  - Velocity: "The only significant development velocity gain is in the first two months post
    Cursor adoption." First month: **+55.4% commits, +281.3% lines added**; second month: +14.5%
    commits, +48.4% lines added. Abstract: "3-5x increases in lines added in the first adoption
    month, but gains dissipate after two months."
  - Quality: static analysis warnings **+30.3%**, code complexity **+41.6%**, sustained beyond the
    adoption period (abstract rounds to 30% and 41%). Duplicate line density: **insignificant**.
  - Mechanism: panel GMM models: "accumulated technical debt subsequently reduces future velocity,
    creating a self-reinforcing cycle." A model of the observational data, not an experiment.
  - Denominators: the percentages are average treatment effects on log-transformed project-level
    outcomes, relative to matched controls. Lines added is a velocity proxy, not delivered value.
  - Scope: open-source projects, Cursor only, adoption detected from configuration files.

- **SWE-CI, Chen et al. (Sun Yat-sen University and Alibaba Group), arXiv 2603.03823, March 2026**,
  preprint. [3] 100 tasks from real repositories, each spanning "an average of 233 days and 71
  consecutive commits"; the agent maintains the code through the sequence. Rationale, quoted: "an
  agent's ability to maintain code can only be revealed through long-term evolution, where the
  consequences of past decisions accumulate over successive changes." Result: "most models achieve
  a zero-regression rate below 0.25, with only two models in the Claude-opus series exceeding 0.5."
  Zero-regression rate = share of tasks with no regression anywhere in the sequence. Alibaba builds
  models (Qwen), so not interest-free, but it sells no code-quality product.

### Vendor research: code health and agent break rates

- **Tornhill and Borg, *Code Red*, TechDebt 2022** (arXiv 2203.04374), peer-reviewed. Tornhill:
  CodeScene; Borg at the time: RISE and Lund University. Data from CodeScene's tool and customers. [4] Pre-dates agents; human developers. 39 proprietary codebases, 30,737
  files, Jira data. Alert code vs Healthy: **15 times more defects**; development time **124%
  longer** (Warning code already **78% longer**); maximum cycle times **9 times longer**. The
  abstract summarises this as "twice the development speed".

- **Borg, Hagatulah, Tornhill and Söderberg, *Code for Machines, Not Just Humans*, arXiv
  2601.02200, 5 January 2026.** [5] Borg: CodeScene and Lund University; Tornhill: CodeScene.
  - Task: LLM refactoring "for maintainability" of **5,000 Python solutions** from DeepMind's
    CodeContests; "break" = the problem's tests fail afterwards. Bands: Healthy CH ≥ 9, Warning
    4–9, Alert < 4.
  - Medium open-weight models (about 20–30B: Qwen3-Coder-30B, gpt-oss-20b, Gemma, GLM, Granite):
    all break Healthy code significantly less often. Risk differences −8.58 pp (Qwen) to −15.12 pp
    (Gemma); relative risk 0.692 (Qwen) to 0.852 (Granite). Abstract: "risk reductions of 15-30%".
  - **Frontier models, 1,000-sample runs: no significant difference.** Claude Sonnet 4.5: tests
    passed 86.77% Healthy vs 84.03% Unhealthy, RR 0.828 [0.613, 1.120]. Claude Code (v2.0.13, with
    Sonnet 4.5): "breaks only about 5% of the test suites regardless of whether the code is Healthy
    or Unhealthy – again, no statistically significant difference." Authors: "the same direction,
    but the effects are smaller and do not reach statistical significance."
  - Scope: single-file competitive-programming code, one task type (refactoring), Python only.

- **The *Echoes of AI* RCT the book already cites** (Borg et al., arXiv 2507.00788 v3, February
  2026) [6]: **first author Markus Borg lists CodeScene** as an affiliation (with Lund University);
  co-authors from Equal Experts and Lund. It uses CodeScene's Code Health as one of its quality
  measures. Its null result ("no significant differences in subsequent evolution") runs *against*
  the vendor's commercial interest, which if anything strengthens it; but the book currently prints
  it without the affiliation, while it names GitClear's.

### Vendor claims: tokens

- CodeScene blog, Tornhill, 28 May 2026 [7]: "agents working on unhealthy codebases consume 35-45%
  more tokens to complete the same tasks". The instrumented task described is **single-prompt unit
  test generation by Qwen3-Coder-30B** on 10k C++, 10k Java and 5k Python competitive-programming
  files. Not agentic feature work.
- The same blog links a separate post headed "Healthy code needs 22 to 35% fewer tokens for agentic
  code review", described as pre-registered. [7] Not opened.
- The talk says features in healthy code take **40–45% fewer tokens** [1]. A Product Hunt post by
  the vendor says "up to ~50%". **Four different ranges from one vendor**; none on frontier agents
  doing feature work.

### The case study (vendor)

- Street Fighter III: 3rd Strike, open-source decompilation, about 300,000 lines of C. Reported by
  InfoQ, 2026-09 [8]: three weeks, roughly **$4,000** in tokens, 2,903 commits across 726 files,
  252,055 lines modified, Code Health **5.6 → 10.0**. InfoQ: "The $4,000 and the three weeks were
  measured." The **~70% fewer AI-induced defects and ~45% less token waste** are "extrapolated from
  its earlier research rather than measured here." A Lund University study comparing feature work
  on the 5.6 and 10.0 versions is planned, not done.

### The feedback loop, as products ship it

- CodeScene's Code Health MCP server [9]: runs locally, needs an access token; tools include
  `code_health_review` (score plus the specific issues), a pre-commit safeguard and a change-set
  analysis. The product page describes a "self-correcting refactoring loop": the agent reviews its
  change, and refactors while the score is low. Tool list partly from a vendor comment, not docs.
- The author's `aihealth` (github.com/epatel/ai-health, v0.1.0, November 2026) implements the same
  loop without a service: `aihealth delta` scores the working tree against `HEAD`, lists new or
  worsened smells with `path:line` and a fix hint, and **exits 1 when health degraded**, so it can
  gate a hook or CI. Thirteen smells modelled on CodeScene's published biomarkers; calibration is
  the author's own, documented in the repository's `cards/code-health-model.md`. A tool, not
  evidence.

## What is standardised vs. one vendor's habit

- **Standard and old:** cyclomatic complexity (McCabe), cognitive complexity (SonarSource's
  published spec), nesting depth, duplication, file and function size, LCOM cohesion. Any linter
  family computes some of them.
- **One vendor's:** the 1–10 Code Health scale, its bands (9 and 4), its weights (not public), and
  the claim that ≥ 9.5 is the target for AI-touched code. `aihealth` copies the model, not the
  calibration.
- **Not standard anywhere:** a delta gate on structure per agent change. Two implementations exist
  (CodeScene MCP, `aihealth`); no study measures what the gate itself is worth.

## Talk vs source

| The talk says | The source says |
|---|---|
| Healthy code: up to 10× faster tasks, 15× fewer defects (*Code Red*) | 15× defects holds; time is 124% longer in Alert code, "twice the development speed", not 10× |
| At Code Health 9 an agent's break risk is up ~60% (*Code for Machines*) | Not found in the paper. Paper: 15–30% lower risk on Healthy code for medium models; **no significant difference for Sonnet 4.5 or Claude Code** |
| 41% more defects after AI adoption (unnamed, late 2025) | Most likely He et al.: **41.6% more complexity**, 30.3% more static-analysis warnings. Not defects |
| 1,000+ projects, +200% velocity, cancelled after two months | He et al.: 806 projects, +281.3% lines added in month one, gains gone after two months |
| Alibaba: six months of maintenance | SWE-CI: 233 days on average, 71 commits per task; quote matches |
| Street Fighter III: 17% fewer AI defects, features ~45% cheaper in tokens | InfoQ: ~70% fewer defects and ~45% less token waste, both **projected**, not measured |

## Contradictions and gaps

- **The agent-sensitivity claim is contradicted by its own source for frontier tools.** The book's
  reader uses frontier agents. For them, the measured break-rate gap is not significant.
- **What still stands without that claim:** agents *produce* complexity (He et al.; SlopCodeBench),
  regress code over long maintenance (SWE-CI), and the human cost of unhealthy code is measured
  (*Code Red*). The case for a structural check rests on those, not on agent sensitivity.
- **No study tests the loop.** Nobody has compared agent runs with and without a structural gate on
  downstream outcomes. Tornhill says refactoring with the MCP feedback improved sharply; no number
  was spoken and no paper found.
- **Token savings unproven for feature work.** The planned Lund study on the two Street Fighter
  versions is the first that could measure it.
- **Not traced to any primary source:** the "AI Whiplash" report (bugs +54%, incidents +242%);
  "deep nesting causes ~20% of programming mistakes"; agents fixing ~50% / ~20% of issues unaided;
  "average codebase Code Health 5.15".

## Do not cite

- Any talk figure in the left column of *Talk vs source* as the talk states it.
- "AI break risk up ~60% at Code Health 9."
- "Agents are more sensitive to code quality than humans" as a finding. It is the talk's
  interpretation; the frontier-model data do not show it.
- Street Fighter III defect or token figures. Only the $4,000, three weeks and 5.6 → 10.0 were
  measured, and only by the vendor.
- Any token-saving percentage, until a study on agentic feature work exists.
- The four untraced claims under gaps.

## Safest to print

1. He et al.: after adopting Cursor, 806 open-source projects saw velocity gains only in the first
   two months, and a persistent **41.6%** rise in code complexity and **30.3%** in static-analysis
   warnings (MSR 2026, independent).
2. SWE-CI: across 100 maintenance sequences averaging 71 commits, most models kept a regression-free
   record on fewer than a quarter of them; two Claude Opus models exceeded half (preprint, 2026).
3. *Code Red*: in 39 proprietary codebases, low-health code had **15 times** more defects and took
   **124%** longer to develop (human developers, vendor-authored, peer-reviewed 2022).
4. *Code for Machines*: healthier code lowered refactoring break rates for mid-size open models by
   15–30%, and showed **no significant difference** for Claude Sonnet 4.5 or Claude Code
   (vendor-authored preprint, 2026). Print the second half with the first, or neither.

## Sources

[1] Adam Tornhill, *AI-Friendly Code: The Missing Link for Speed with Quality*, GOTO Copenhagen
2026 — https://youtu.be/ciRTdOIhNCc — slides https://gotocph.com/2026/sessions/3981 — transcript
(auto-captioned) accessed 7 November 2026
[2] He, Miller, Agarwal, Kästner, Vasilescu, *Speed at the Cost of Quality*, MSR 2026, DOI
10.1145/3793302.3793349 — https://arxiv.org/abs/2511.04427 (v3, 26 January 2026) — accessed 7
November 2026
[3] Chen, Xu, Wei, Chen, Zhao, *SWE-CI: Evaluating Agent Capabilities in Maintaining Codebases via
Continuous Integration* — https://arxiv.org/abs/2603.03823 (v2, 17 March 2026) — accessed 7
November 2026
[4] Tornhill and Borg, *Code Red: The Business Impact of Code Quality*, TechDebt 2022, DOI
10.1145/3524843.3528091 — https://arxiv.org/abs/2203.04374 — accessed 7 November 2026
[5] Borg, Hagatulah, Tornhill, Söderberg, *Code for Machines, Not Just Humans: Quantifying
AI-Friendliness with Code Health Metrics* — https://arxiv.org/abs/2601.02200 (v1, 5 January 2026)
— accessed 7 November 2026
[6] Borg et al., *Echoes of AI* — https://arxiv.org/abs/2507.00788 (v3, February 2026), author
affiliations — accessed 7 November 2026
[7] Adam Tornhill, "Unhealthy Code is Burning Your Token Usage — Here's the Data", CodeScene blog,
28 May 2026, **vendor** —
https://codescene.com/blog/unhealthy-code-is-burning-your-token-usage-heres-the-data — accessed 7
November 2026
[8] Steef-Jan Wiggers, InfoQ, September 2026, on CodeScene's agentic refactoring case study —
https://www.infoq.com/news/2026/09/agentic-refactoring-case-study/ — accessed 7 November 2026
[9] CodeScene, Code Health MCP server product page, **vendor** —
https://codescene.com/product/mcp-server — accessed 7 November 2026
