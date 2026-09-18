# Published studies and measured data on agent-assisted developer productivity and code quality

**Question asked:** What has actually been measured — by RCT, telemetry, or survey — about the
effect of AI coding assistance on developer productivity and code quality? Find primary sources,
including results that contradict the optimistic narrative. Record methodology and sample size.
Separate evidence about autocomplete/chat from evidence about *agents*.

**Researched:** 19 September 2026

**Confidence:**

- **High** on the METR RCT, the Google enterprise RCT, the Peng et al. Copilot RCT, and the Borg et
  al. maintainability RCT. All four are primary, published, with stated sample sizes and
  author-written caveats, and I read the abstract or the paper page directly.
- **High** on DORA's headline adoption and trust figures (90%, 30% low trust) — reproduced
  identically across Google's own blog, Google Cloud's blog, and Google Research's publication page.
- **Medium** on DORA's *effect sizes* for throughput and instability in 2025. DORA published the
  direction of the relationship prominently and the 2024-style point estimate much less prominently;
  I could not pull the 2025 coefficient out of a primary page (the PDF exceeds the fetch size
  limit). See **Do not cite**.
- **Medium** on the 2026 agentic telemetry studies (Microsoft CLI, the 2× mandate study, the
  AI-IDEs-vs-agents study). They are recent arXiv preprints, most not yet peer reviewed, and two of
  the three are authored by people with a commercial or employer stake.
- **Low** on all vendor code-quality reports (GitClear, Uplevel, LinearB, Faros). The figures are
  real and published, but none discloses a reproducible methodology or releases underlying data, and
  every one of them sells a product whose pitch the finding supports.
- **Low** on anything labelled "Stack Overflow Developer Survey 2026". It does not exist yet.

---

## Findings

### 1. The METR RCT — the central negative result

- Randomised controlled trial. **16 experienced open-source developers**, **246 real tasks** in
  repositories on which they had **an average of 5 years' prior experience**. Each task randomly
  assigned to allow or disallow AI. [1][2]
- Repositories averaged **22,000+ GitHub stars** and **1M+ lines of code**. Tasks averaged roughly
  two hours. Developers were paid **$150/hour**. [1]
- Tooling: "developers primarily use Cursor Pro, a popular code editor, and Claude 3.5/3.7 Sonnet",
  at the **February–June 2025 frontier**. [2]
- Headline result: **"allowing AI actually increases completion time by 19%"**. [2] METR later gave
  the interval explicitly: the effect was a **19% slowdown, CI +2% to +39%**. [3]
- The perception gap, all four numbers from the abstract: developers **forecast −24%** before
  starting; **estimated −20%** afterwards; economics experts predicted **−39%**; ML experts
  predicted **−38%**. Actual: **+19%**. [2]
- Mechanism, as METR reports it: with AI allowed, developers spend less time actively coding and
  searching, and more time "prompting AI, waiting on/reviewing AI outputs, and idle". [1]
- Authors' own robustness statement, verbatim: *"Although the influence of experimental artifacts
  cannot be entirely ruled out, the robustness of the slowdown effect across our analyses suggests
  it is unlikely to primarily be a function of our experimental design."* [2]
- Authors' own generalisability caveats — METR states the study does **not** provide evidence that
  AI systems do not speed up **most** developers, that AI does not speed up work in **other
  domains**, or that there are **no** more effective ways of using the same systems to get positive
  speedup in their exact setting. [1] This is the single most-abused study in the discourse and its
  authors explicitly disclaim the generalisation it is usually used for.
- Publication: arXiv 2507.09089, submitted 12 July 2025, v2 25 July 2025; authors Joel Becker, Nate
  Rush, Elizabeth Barnes, David Rein. [2]

### 2. METR's own follow-up failed — and this matters more than the original

- METR ran a second study in late 2025 with **57 developers** (10 returning from the original, 47
  newly recruited), **143 repositories**, **800+ tasks**, median **10 years' experience**. [3]
- Results: returning developers **−18% speedup, CI −38% to +9%**; newly-recruited developers **−4%
  speedup, CI −15% to +9%**. Both intervals straddle zero. [3]
- METR abandoned the design because of selection effects. Their words: **"30% to 50% of developers
  told us that they were choosing not to submit some tasks because they did not want to do them
  without AI"**, and **"an increased share of developers say they would not want to do 50% of their
  work without AI"**. [3]
- METR's own verdict on the data: **"our data is only very weak evidence for the size of this
  increase"**, and the estimate is **"likely a lower-bound on the true productivity effects"**. They
  describe it as **"an unreliable signal of the current productivity effect of AI tools"**. [3]
- Published 24 February 2026. The honest summary for the book: *the strongest negative RCT in the
  field has not been replicated, and the people who ran it could not replicate it, because by 2026
  developers would no longer agree to work without AI.* That is itself a finding.

### 3. METR's 2026 self-report survey — deliberately contrasted with its own RCT

- Survey, **349 technical workers** (87 software engineers, 71 researchers, 129 academics and PhD
  students, 48 founders and managers), fielded **February–April 2026**, published 11 May 2026. [4]
- Median **self-reported** change in value of work due to AI: **1.4–2x** for March 2026, with a
  retrospective **1.3x** for March 2025 and a forecast **2.5x** for March 2027. [4]
- METR's own scepticism, verbatim: *"our study in early 2025 found that people overestimated AI's
  effect on their time spent on tasks by 40 percentage points on average"*, and *"public estimates
  of productivity impacts from surveys have tended to be greater than those from field experiments
  or quasi-experiments"*. [4]
- Useful for the book: the same organisation publishes both the pessimistic RCT and the optimistic
  survey, and tells you which to trust less.

### 4. DORA — survey/self-report, near-universal adoption, unresolved instability

Methodology for the 2025 edition: **survey responses from nearly 5,000 technology professionals**
worldwide plus **over 100 hours of qualitative data**; published **23 September 2025**; 14 named
authors including Derek DeBellis, Nathen Harvey, Eirini Kalliamvakou, and Gene Kim. [6][7] It is
self-report throughout; RedMonk's Rachel Stephens makes the obvious methodological objection — the
results are "based on a survey" and it is unclear whether respondents can honestly self-report
individual effectiveness or judge team performance from their vantage point. [10]

- **90% of survey respondents report using AI at work**, described as a 14% increase on the prior
  year (2024 was "roughly 75%"). [7][10]
- Median time working with AI tools: **two hours daily**. [8]
- Reliance: **80%+ believe AI has increased their productivity**; **59% report a positive influence
  on code quality**. [7][8]
- The trust paradox: **24% report high trust** (4% "a great deal", 20% "a lot"); **30% report low
  trust** (23% "a little", 7% "not at all"). [8] Google's blog states the same as "**30% report
  little or no trust in the code generated by AI**". [7]
- Direction of the delivery findings: **higher AI adoption is associated with an increase in both
  software delivery throughput and software delivery instability**. [10] The throughput sign
  **flipped from negative in 2024 to positive in 2025; the instability sign did not flip**. [10]
- 2024 baseline for comparison: the 2024 Accelerate State of DevOps report estimated that a **25%
  increase in AI adoption** was associated with a **1.5% decrease in delivery throughput** and a
  **7.2% reduction in delivery stability**. [9] Note this is the **2024** figure, for
  autocomplete-era tooling.
- DORA's framing sentence, which the book can use directly: AI's primary role is as **an amplifier**
  — "it magnifies the strengths of high-performing organizations and the dysfunctions of struggling
  ones". [6]

**DORA ROI of AI-assisted Software Development report (2026.01)**, published **22 April 2026** on
dora.dev, covered by InfoQ 11 May 2026. [11][12] This is a **modelling exercise, not a survey**: a
value model running seven capabilities through DORA delivery metrics to financial outcomes.

- The **J-curve**: teams take a temporary productivity dip before capturing value. DORA names three
  causes of the dip — the learning curve, the **verification tax**, and pipeline adaptation. [12]
- **Verification tax** is DORA's term for the time developers spend reviewing AI outputs — the
  effort saved on writing is respent on checking. [12]
- Illustrative worked figures for a 500-person organisation (these are DORA's *model outputs*, not
  measurements): first-year ROI **39%**, first-year value **~$11.6 million** against investment
  **~$8.4 million**, payback **~8 months**, fully loaded salary per head **$176,000**, and a
  **$344,000** negative downtime impact driven by change failure rate rising **from 5% to 6%**. [12]
- Productivity gain by task type in the model: **35–40% on simple, greenfield tasks** versus **~10%
  on complex legacy code**. [12]

### 5. The optimistic RCTs — and what they actually measured

**Peng, Kalliamvakou, Cihon, Demirer (2023)**, arXiv 2302.06590, submitted 13 February 2023. [13]

- Controlled experiment. Task: **implement an HTTP server in JavaScript as quickly as possible**.
  Treatment group had GitHub Copilot.
- Result: treatment group **completed the task 55.8% faster** — **1 hour 11 minutes versus 2 hours
  41 minutes**. Reported elsewhere as **95 professional developers**; the abstract itself does not
  state N.
- Experiment ran **15 May – 20 June 2022**, immediately before Copilot's general availability. [13]
- This is the single most-quoted pro-AI number in the industry. It is a **greenfield, single-file,
  no-existing-codebase, speed-only, autocomplete-era** measurement from mid-2022. It is not about
  agents, not about maintenance, and not about a codebase with existing conventions.

**Paradis et al., Google (2024)**, arXiv 2410.12944. [15]

- Enterprise RCT, **96 full-time Google software engineers**, summer 2024, real internal IDE (a
  customised VS Code) and real internal tooling.
- Task: build a logging service on Google's internal infrastructure — **editing 10 files and 474
  lines of code**.
- Three AI features: AI Code Completion, Smart Paste, Natural Language to Code.
- Result: **96 minutes with AI versus 114 minutes without**; best estimate of the effect **~21%**,
  "although the confidence interval is large". [15]
- Authors' caveat, verbatim: *"the effect size obtained in our lab study will not necessarily apply
  more broadly, or that the effect of AI found using internal Google tooling in the summer of 2024
  will translate across tools and over time."* [15]
- This is the enterprise-grade internal RCT the brief asked for. Note it is still **autocomplete and
  inline assistance**, not agentic.

**GitHub's own code-quality RCT (November 2024)** — **vendor-reported**. [14]

- **202 developers** with 5+ years' experience; **104 with Copilot, 98 without**, randomly assigned.
  Task: API endpoints for a restaurant-review web server, graded against **10 unit tests**.
- Copilot group had a **53.2% greater likelihood of passing all 10 unit tests (p<0.01)**.
- Blind review phase: **25 reviewers**, **1,293 reviews**. Readability **+3.62% (p=0.003)**,
  reliability **+2.94% (p=0.01)**, maintainability **+2.47% (p=0.041)**, conciseness **+4.16%
  (p=0.002)**; reviewers **5% more likely to approve** Copilot-written code (p=0.014). Copilot code
  averaged **18.2 lines per readability error versus 16.0**, a 13.6% improvement.
- No limitations section. GitHub sells Copilot. The absolute effect sizes on quality are **2–4%**,
  which is a very different claim from the headline "Copilot improves code quality".

**Borg et al., "Echoes of AI" (2025–2026)**, arXiv 2507.00788, v3 26 February 2026. [16] This is the
most useful quality study because it is a two-phase experiment with an RCT in phase 2.

- **151 participants, 95% professional developers.** Phase 1: add features to a Java web application
  with or without AI. Phase 2: **different** participants evolve the resulting code **without** AI.
- Phase 1 speedup: **30.7% median reduction in completion time**; habitual AI users **55.9%
  estimated speedup**.
- Phase 2 — the point of the study: **"no significant differences in subsequent evolution with
  respect to completion time or code quality"**, with Bayesian analysis indicating potential
  improvements were **"at most small and highly uncertain"**. The authors **"did not detect
  systematic maintainability advantages or disadvantages"**.
- Authors' caveat: they investigated only the tasks and measures employed, and recommend future work
  on **"code bloat from excessive code generation and cognitive debt"**.
- Read carefully, this is the strongest available evidence *against* the "AI code is a maintenance
  time bomb" claim as well as against the "AI code is better" claim. It finds nothing either way
  downstream.

### 6. Agentic-specific evidence (2026) — the distinction the book needs

Everything above except the METR follow-up is about autocomplete, inline completion, or chat. These
are the studies that actually measure **agents**.

**Murphy-Hill, Butler, Savelieva — Microsoft CLI agents**, arXiv 2607.01418v1, 1 July 2026. [17]
Telemetry from **tens of thousands of Microsoft engineers** during the early-2026 rollout of
**Claude Code and GitHub Copilot CLI**. Pre-period 1 October 2025 – 4 January 2026; post-period 5
January – 29 April 2026.

- Merged-PR throughput: **+24.0% [95% CI +14.5%, +33.7%], p<0.001**, by Bayesian structural
  time-series (CausalImpact synthetic control).
- Within-person dose-response at **5+ tool-use days per week: +50.1%** (fixed-effects Poisson).
- Authors' caveats, verbatim: *"Merged PRs are an imperfect proxy for throughput and reward small,
  frequent PRs"*; *"The adoption study is cross-sectional, so it cannot rule out several
  confounds"*; *"Both studies draw on one company in a single early-2026 window"*; *"Our 16-week
  window is long enough to surface an early fade but not a long-horizon decline"*.
- And, to their credit, stated positionality: *"The authors are Microsoft employees; Microsoft sells
  AI tools, encourages their use, and owns GitHub."* [17]

**He, Agarwal, Denisov-Blanch, Azaletskiy, Koyejo, Vasilescu — "AI Writes Faster Than Humans Can
Review"**, arXiv 2607.01904v1. [18] Longitudinal study of a documented enterprise **"2×" mandate**
at a mid-sized, AI-forward B2B software company. Panel of **802 developers** and **196,212 pull
requests**, **January 2024 – April 2026**.

- Per-capita throughput rose **2.09× from baseline — 21.2 to 44.3 PRs per developer per month**.
- Within-developer gains were **1.46–1.72×** depending on specification, growing to **1.99× by nine
  months on tool**. The gap between 2.09× and 1.46–1.72× is composition, not individual gain.
- AI-authored PRs rose **from near zero to ~90%** of PRs by study end.
- Review transformation: human review coverage fell **21 percentage points, from 89% to 68%**;
  automated review rose **from ~19% to ~84%** of PRs, overtaking human review; **per-reviewer load
  doubled (2.0×)**; AI-authored PR review latency rose **~20%**; **PR cycle time increased 22%**
  post-mandate.
- Quality indicators: **merge rates essentially flat**; **revert rates declined slightly (−0.067 for
  AI-authored PRs)**.
- Heterogeneity: management tier **+86%**; IC through Principal **+27% to +42%**; **legacy code +12%
  (not significant)**; newer repositories (2022+) **+44%**.
- Authors' caveat, verbatim: *"We therefore read the result as evidence that a near-doubling is
  attainable under favorable conditions and over a long enough horizon, not that it is typical,
  immediate, or free."* Adoption was **not randomised**: *"developers chose when to adopt and how
  heavily to use AI."* [18]

**Agarwal, He, Vasilescu — "AI IDEs or Autonomous Agents?"**, arXiv 2601.13597, 20 January 2026
(revised 27 January 2026). [19] Staggered difference-in-differences with matched controls on the
AIDev dataset; agent adoption defined as a repository's first agent-generated PR.

- **Large, front-loaded velocity gains appear only when agents are the first observable AI tool in a
  project.** Projects already using AI IDEs saw minimal additional throughput.
- Persistent quality risk: **static-analysis warnings up roughly 18%** and **cognitive complexity up
  roughly 39%**.
- Conclusion: heterogeneous effects and **diminishing returns to AI assistance**.
- This is the cleanest published support for a claim the book probably wants to make: *agents do not
  stack on top of an existing AI-assisted baseline the way the marketing implies.*

**Li, Zhang, Hassan — AIDev**, arXiv 2602.09185, 9 February 2026. [20] The dataset most 2026 agentic
studies sit on: **932,791 agent-authored pull requests**, **116,211 repositories**, **72,189
developers**, five agents (OpenAI Codex, Devin, GitHub Copilot, Cursor, Claude Code), cutoff **1
August 2025**; curated subset of **33,596 PRs from 2,807 repositories with 100+ stars**.

**Raida & Hou — "Early Adoption of Agentic Coding Tools by GitHub Projects"**, arXiv 2607.14037v2,
accepted to the KDD 2026 Workshop on Agentic Software Engineering (SE 3.0), 9 August 2026. [21]
**25,264 agent PRs across 2,361 popular GitHub repositories**, May–July 2025.

- **"The median repository generates only one to two agentic PRs during a three-month period."**
- **Over 70% of projects have fewer than 20% of contributors engaged in agent workflows.**
- Only **25 of 2,361 projects (1%)** exceeded their 36-PR-per-participant benchmark.
- **78.9%** of cases show one developer both reviewing and committing the agent's contribution —
  multi-human oversight is uncommon.
- Limitations: popular repositories only (100+ stars), three-month window, three agents;
  productivity measures do not account for PR complexity or quality. [21]
- Useful corrective: agentic adoption in open source in mid-2025 was **shallow and concentrated**,
  not the deluge the discourse implies.

**"Coding Beyond Your Training"**, arXiv 2605.25438v1. [35] Staggered DiD (Callaway–Sant'Anna) on
**5,838 GitHub developers (3,060 treated, 2,778 control)** observed monthly over **28 months**, from
**7.8 million Claude-co-authored commits**, covering the **May 2025 – January 2026** rollout.

- At adoption: monthly commits **+~41 (191% over a baseline of 21.3)**; **+1.5 distinct
  repositories**; **+0.83 programming languages** against a baseline of 0.63; **+0.31 newly-used
  languages**.
- Authors' own identification threat, verbatim: *"Claude adoption is voluntary, and the timing of
  adoption is plausibly correlated with the timing of a developer's decision to start a new project
  in an unfamiliar language."* They frame it as a "sharp, persistent shift in developer behavior
  coincident with adoption" rather than causality. [35]
- Treat the 191% as a **selection-heavy activity count**, not a productivity measurement.

### 7. Rework, review burden, and time-to-merge (not time-to-first-draft)

**"The Fast and Spurious: Developer Productivity with GenAI"**, arXiv 2510.24265. [22] Survey of
**415 software practitioners** using the SPACE framework. Finding: frequent GenAI users report
faster task completion and higher output, but **increased code review burden offsets speed gains**,
**cognitive load from verifying AI output stays high**, and **collaboration shows no improvement**.
Authors' phrasing: perceived gains *"may be spurious — surface-level acceleration, often accompanied
by redistributed effort and hidden costs."* Survey methodology; treat as directional.

**LinearB 2026 Software Engineering Benchmarks Report** — **vendor-reported**. [29] **8.1+ million
pull requests, 4,800+ organisations, 42 countries**.

- **"Acceptance Rates for AI-generated PRs are significantly lower than manual PRs (32.7% vs.
  84.4%)"** — measured as merged within 30 days.
- **"AI PRs wait 4.6x longer before review — but are reviewed 2x faster once picked up."**
- **"Agentic AI PRs have a PR Pickup Time 5.3x longer than Unassisted ones"** — reported elsewhere
  as **1,055 versus 201 minutes**.
- Bot acceptance rates vary by tool; LinearB notes Devin's rising since April and Copilot's slipping
  since May (of 2026 — the report does not date these on the summary page).
- The 2.6×-larger and 154%-larger PR-size figures circulate from this report but appear in secondary
  write-ups, not on the primary page I could read. See **Do not cite**.

**Faros AI, "Acceleration Whiplash" / AI Engineering Report 2026** — **vendor-reported**. [30]
**22,000 developers across 4,000 teams**, two years of data; article 21 May 2026.

- High-AI-adoption cohort: average PR size **+51.3%**; files edited per PR **+59.7%**; bugs per PR
  **+54%**; PRs merged with **no review at all +31%**.
- Median time to first PR review **+156.6%**; average time in PR review **+199.6%**; median time in
  PR review **+441.5%**.
- No disclosed control for confounders; no raw data. Directionally consistent with [18], which is
  the reason to take it seriously at all.

**Uplevel (October 2024, updated July 2026)** — **vendor-reported**. [28] **Nearly 800 developers**;
observational, with and without Copilot; measured cycle time, PR throughput, bug rate, and
out-of-hours working.

- **No significant change in efficiency metrics** — Copilot "neither helped nor hurt" PR cycle time
  or throughput.
- **Bug rate up 41%** in the Copilot cohort.
- "Sustained Always On" (out-of-hours working): **28% reduction without Copilot versus 17% reduction
  with**.
- Uplevel does **not** describe randomisation, matching, or group sizes. The 41% figure is quoted
  constantly and rests on an undisclosed methodology. Cite it only with that stated.

### 8. Code quality — GitClear (vendor, commercial interest, flag it)

GitClear sells developer-analytics software whose value proposition is precisely "your code quality
is degrading and you need to measure it". Their reports are the most detailed longitudinal
code-quality data available and are also marketing. Both things are true.

**"AI Copilot Code Quality 2025"** — **211 million changed lines**, **January 2020 – December
2024**, drawn from Google, Microsoft, Meta, and enterprise C-Corp repositories; reported on in
February 2025. [27][37]

- Copy/pasted code rose **from 8.3% to 12.3% of changed lines, 2021–2024**.
- Refactored ("moved") code fell **from 25% of changed lines in 2021 to under 10% in 2024**.
- **"Copy/paste" code exceeded "moved" code for the first time** in the record.

**"The Maintainability Gap: 2026 AI Code Quality Research"** — **623 million analysed code
changes**, **2023–2026**. [26]

- Refactoring / moved code: **21% of changed lines (2022) → 13% (2023) → 3.8% (2026 YTD)**.
- Copy/paste: **9.4% (2022) → 15.7% (2026 H1)**.
- Block duplication: **40.3 (2023) → 73.0 (2026 YTD)**, stated per million changed lines; **highest
  on record**.
- Cross-file function connectivity: **343 method calls per thousand changed lines (2023) → 223 (2026
  YTD)**.
- Legacy code long-term-update percent: **1.7% (2023) → 0.46% (2026 YTD)**.
- Error-masking constructs **+47%**; two-week code churn **+15%**.
- Heavy AI users out-produce non-users **4–10×**, but **against their own pre-AI baseline the gain
  is 25%**. This is GitClear's most honest number and the one least quoted.
- **Derived arithmetic, flagged:** GitClear's headline deltas are baselined on **2023**, not 2022.
  3.8 ÷ 13 = 0.292, i.e. **−70.8%** refactoring, matching their "−70%". 73.0 ÷ 40.3 = 1.81, i.e.
  **+81%** duplication, matching. Their "copy/paste +41%" therefore implies a 2023 base of 15.7 ÷
  1.41 = **~11.1%**, which they do not state. Do not compute a copy/paste delta from the 9.4% (2022)
  figure — 15.7 ÷ 9.4 = 1.67 would give **+67%**, a different and wrong number.
- Methodological limits that GitClear does not state on the page but that reviewers have raised: the
  data shows **code-change trends during the period when AI assistants spread**, not line-level
  attribution of duplicated blocks to AI. GitClear's own documentation notes heavy exclusions — as
  of February 2025, a little under half of the lines a conventional git-stats aggregator would count
  qualified for analysis. [37]

### 9. Security and defects

**Schreiber & Tippe**, arXiv 2510.26103, 30 October 2025. [31] CodeQL static analysis over **7,703
files** from public GitHub repositories explicitly attributed to AI generation tools (ChatGPT
91.52%, GitHub Copilot 7.50%, Amazon CodeWhisperer 0.52%, Tabnine 0.46%).

- **4,241 CWE instances across 77 vulnerability types.**
- **"87.9% of AI-generated code does not contain identifiable CWE-mapped vulnerabilities."**
- By language: Python **16.18%–18.50%**, JavaScript **8.66%–8.99%**, TypeScript **2.50%–7.14%**.
- **39% of collected files** involved AI used for documentation generation.
- Important caveat the book should carry: this is a **self-attributed convenience sample of public
  repositories**, with no human-written control group. It cannot tell you whether AI code is *more*
  vulnerable than human code — only the absolute rate in this sample.

### 10. Stack Overflow Developer Survey — 2025 is the latest published edition

The 2025 survey drew **over 49,000 responses from 177 countries**; the AI section reports N per
question (e.g. **33,662 responses, 68.7% response rate**, for the usage question). [23]

- **84% using or planning to use AI tools** (up from 76% in 2024). [23]
- **51% of professional developers use AI tools daily**; 47.1% of all respondents daily, 17.7%
  weekly, 13.7% monthly or less. [23]
- **46% actively distrust the accuracy of AI tools versus 33% who trust it**; only **3.1% "highly
  trust"** it. Experienced developers trust least: **2.5% highly trust, 20.7% highly distrust**.
  [23]
- Positive sentiment fell **from 70%+ in 2023–2024 to ~60% in 2025** (22.9% very favourable + 36.8%
  favourable = 59.7%). [23]
- Top frustration: **66% cite "AI solutions that are almost right, but not quite"**; second, **45.2%
  "debugging AI-generated code is more time-consuming"**; **20%** report reduced confidence in their
  own problem-solving. [23]
- Agents specifically: **52% of developers either do not use agents or stick to simpler AI tools**,
  and **38% have no plans to adopt them**. [23]
- The **2026 survey opened 23 June 2026** and results were not published as of 19 September 2026.
  Stack Overflow's own June 2026 post says "agent usage has doubled since then" but gives **no
  baseline and no percentage**. [25]

---

## Contested claims

**Does AI speed developers up or slow them down?** Both halves are published, both by credible
sources, and they are not reconcilable by picking one.

- *Slower:* METR's RCT, **+19% completion time, CI +2% to +39%**, 16 developers, 246 tasks, mature
  repositories they knew well, early-2025 tooling. [2]
- *Faster:* Google's enterprise RCT, **~21% faster**, 96 engineers, a 10-file / 474-line task on
  internal infrastructure, summer 2024. [15] And Microsoft's telemetry, **+24.0% merged PRs [CI
  +14.5%, +33.7%]** across tens of thousands of engineers with **agentic CLI tools**, early 2026.
  [17]
- The reconciliation the evidence actually supports is a **task-shape** one, not a winner: DORA's
  model separates **35–40% gains on simple greenfield** from **~10% on complex legacy** [12]; the 2×
  mandate study finds **+44% on repositories created 2022 or later** but **+12%, not significant, on
  legacy code** [18]; GitClear finds heavy AI users gain **25% against their own pre-AI baseline**
  while appearing 4–10× more productive than non-users [26]. Carry all of it.

**Does AI improve or degrade code quality?**

- *Improves:* GitHub's own RCT — **+53.2% likelihood of passing all 10 unit tests**, readability
  **+3.62%**, maintainability **+2.47%**. Vendor-run, greenfield task, effect sizes of 2–4% on the
  quality dimensions. [14]
- *No downstream effect either way:* Borg et al., 151 participants, two-phase, **"no significant
  differences in subsequent evolution with respect to completion time or code quality"**. [16]
- *Degrades:* GitClear's eight-signal deterioration [26]; Uplevel's **+41% bug rate** [28]; Faros's
  **+54% bugs per PR** [30]; Agarwal et al.'s **+18% static-analysis warnings and +39% cognitive
  complexity** [19].
- Note the asymmetry: the "improves" evidence is a controlled experiment on a **greenfield task**;
  the "degrades" evidence is **observational, at repository scale, over time**. They are measuring
  different things and neither refutes the other.

**Does DORA say AI helps or hurts delivery?** It has said both, in consecutive years, about
different tooling generations.

- **2024:** a 25% increase in AI adoption associated with **−1.5% throughput** and **−7.2% delivery
  stability**. [9]
- **2025:** throughput **positive**; instability **still rising**. [10]
- Anyone quoting the 2024 numbers as current is quoting a superseded finding about a superseded
  tooling generation.

**Stack Overflow's own trust figure disagrees with itself.** The 2025 survey results page reports
**33% trust / 46% distrust** [23]; Stack Overflow's February 2026 blog says **"Only 29% of 2025
respondents said they trust AI"**, down 11 percentage points from 2024. [24] Same publisher, same
survey year, two numbers. Likely a different question or a different denominator, but I could not
establish which. Use **33%/46% with the survey page as the citation**, and note the 29% exists.

**Do agent-authored PRs get merged?**

- LinearB (vendor): AI PRs merge within 30 days **32.7%** of the time versus **84.4%** unassisted.
  [29]
- The 2× mandate study (academic, one firm, ~90% AI-authored PRs by the end): **merge rates
  essentially flat, revert rates slightly down**. [18]
- These are both about AI-authored PRs and they point opposite directions. The most likely
  reconciliation is population — LinearB's "AI PR" includes fully autonomous bot PRs raised against
  repositories with no adapted process, while the 2× firm's engineers drove agents inside an adapted
  workflow. Carry both, and say the reconciliation is a hypothesis.

---

## Contradictions and gaps

- **No RCT of agentic coding exists.** Every randomised trial in this brief measures autocomplete,
  inline completion, or chat. The only agentic evidence is telemetry and quasi-experimental
  (Microsoft [17], the 2× mandate [18], DiD on AIDev [19][35]). METR's attempt at a 2026 RCT
  collapsed on selection effects [3]. If the book claims anything causal about agents, hedge it.
- **Nobody has cleanly measured total cost of ownership.** Every study measures an *activity* —
  merged PRs, task completion time, commits. Murphy-Hill et al. say so outright: "Merged PRs are an
  imperfect proxy for throughput and reward small, frequent PRs" [17]. He et al. flag "the
  activity-only nature of the throughput construct and the downstream costs it omits" [18]. There is
  no published study measuring the full cycle from prompt to production incident.
- **No independent replication of the Peng et al. 55.8% result.** I found none. It has been cited
  for three years without one, and the conditions it measured (mid-2022 Copilot, one greenfield
  JavaScript file) no longer exist.
- **The Stanford 100k-developer work is not published as a paper.** Yegor Denisov-Blanch's widely
  repeated figures — median productivity lift **10–15%**, roughly **half of gross gains consumed by
  rework** — circulate through conference talks, podcasts, and slide decks. The Stanford SWEPR group
  site lists four papers; the only relevant one is "Predicting Expert Evaluations in Software Code
  Reviews" (2024, arXiv 2409.15152, **70 Java commits**, r = 0.82 for coding time, r = 0.86 for
  implementation time) — a methods paper, not the productivity result. [33] The group states it has
  worked with **600+ organisations and 120,000+ engineers since 2022**, but the productivity figures
  are not in a citable publication. Denisov-Blanch is a co-author on [18], which **is** citable.
- **DORA 2025's effect sizes are not on any page I could reach.** The PDF at services.google.com
  exceeded the fetch size limit; the landing pages and both Google blogs give direction, not
  coefficients. If the book needs a 2025 number for the throughput/instability relationship, someone
  must open the PDF.
- **No published second edition of DORA's "State of AI-assisted Software Development".** The 2026
  publication is the **ROI** report, which is a model, not a survey. Do not present its illustrative
  financial figures as measurements.
- **Perceived-vs-actual is now only measured for autocomplete.** The famous METR gap (developers
  believed −20%, reality +19%) is a 2025 autocomplete-era finding [2]. METR's 2026 self-report
  survey [4] shows the perception has grown to 1.4–2× but has **no paired objective measurement**.

### Do not cite

- **"Stack Overflow Developer Survey 2026" figures (84% adoption, 3% trust, etc.).** Multiple 2026
  articles (byteiota, BuildApps, various aggregators) present these under a 2026 headline. They are
  the **2025** figures. The 2026 survey opened 23 June 2026 and had not reported as of 19 September
  2026. [25] *Reason: mislabelled year on real data.*
- **Code Ninety "AI Coding Assistant Benchmarks 2026"** — PR lead time **−32.4%** (14.2 → 9.6 hrs),
  defect injection **+50.0%** (3.2 → 4.8 bugs per 1,000 LOC), security flags **+61.1%**, PR review
  lead time **+41.5%**, from "84 organisations and 14,200+ developers". [34] *Reason: published by a
  software consultancy as part of its own marketing research series; no peer review, no raw data, no
  independent validation, no disclosed sampling frame. The figures are suspiciously clean and are
  starting to circulate as if they were research.*
- **"AI-assisted PRs are 2.6x larger (408 vs 157 lines)" and "AI PRs are 154% larger than human
  PRs".** These trace to secondary write-ups of the LinearB 2026 report; neither appears on
  LinearB's own summary page, which carries the merge-rate and pickup-time figures but not the size
  figures. [29] *Reason: vendor figure laundered through third parties; unverified against the
  vendor's own text.* (Faros's **+51.3% PR size** [30] is directly on the vendor's page and can be
  used instead, with the vendor flag.)
- **"96% of developers don't fully trust AI-generated code accuracy."** Attributed to LinearB in
  secondary coverage; not on LinearB's own page, and inconsistent with Stack Overflow's 3.1% "highly
  trust" / 33% "trust" split. *Reason: unsourced to primary, and probably a restatement of "not 100%
  trust", which is not a meaningful statistic.*
- **"Roughly a quarter of commits now show measurable AI assistance" (GitClear 2026).** Appears in
  search summaries of the GitClear report but I could not find it in the page text. *Reason:
  unverified against primary; and GitClear does not publish its AI-detection method, so the
  denominator is unknowable.*
- **"46.41% of agent-proposed fixes are rejected" (arXiv 2606.13468, AIDev-based).** Real paper, but
  I verified this only from a search snippet, not the paper text. *Reason: not read at source. Fetch
  the paper before using.*
- **Baz "State of Rework 2026" and similar single-vendor rework benchmarks.** Not fetched, not
  verified, vendor-authored. *Reason: unverified; and the category is saturated with vendors whose
  product is rework measurement.*
- **Any figure presenting the METR 19% as "AI makes developers slower" without qualification.** The
  authors explicitly disclaim that generalisation [1], their own follow-up could not reproduce it
  [3], and it measured Cursor Pro with Claude 3.5/3.7 in early 2025 — two model generations ago.

### Where autocomplete evidence gets quoted as agent evidence

This is the most common failure in the discourse and the book should call it out by name.

| Finding | What it actually measured | How it gets quoted |
|---|---|---|
| Peng et al. **55.8% faster** [13] | Copilot autocomplete, one greenfield JS HTTP server, May–June 2022 | "AI agents make developers 56% faster" |
| METR **+19% slower** [2] | Cursor Pro + Claude 3.5/3.7, Feb–Jun 2025, mature repos | "AI agents slow developers down" |
| Google **~21% faster** [15] | Three inline features in an internal IDE, summer 2024 | "Google proved AI-assisted dev is faster" |
| DORA 2024 **−7.2% stability** [9] | 2024 survey, autocomplete-era adoption | "Agents destabilise delivery" |
| GitHub **+53.2% unit-test pass** [14] | Copilot autocomplete, greenfield API task, 2024 | "AI improves code quality" |

Genuinely agentic measurements, as of September 2026: Microsoft CLI telemetry [17], the enterprise
2× mandate study [18], the AI-IDEs-vs-agents DiD [19], AIDev-derived open-source studies [20][21],
and the Claude Code adoption panel [35]. That is the whole list, and none of them is an RCT.

---

## Staleness assessment

| Claim | Why it rots | Suggested hedge |
|---|---|---|
| METR's 19% slowdown | Measured Cursor Pro + Claude 3.5/3.7, Feb–Jun 2025. Two model generations old by late 2026. METR's own follow-up could not reproduce it. | "In the only published RCT of its kind, run on early-2025 tooling…" and always pair with METR's 2026 retraction of confidence. |
| Peng et al. 55.8% | Mid-2022 Copilot on a greenfield single-file task. Never independently replicated. | "An early-Copilot experiment, on a greenfield task, in 2022…" Never present as an agent result. |
| DORA adoption at 90% | Adoption is asymptoting; the interesting number is shifting from *whether* to *how*. | "By the 2025 survey, adoption was effectively universal — the live question is no longer adoption." |
| DORA's throughput sign | Flipped negative→positive between 2024 and 2025. It can flip again. | Quote the year explicitly every time. Never say "DORA found" without the edition. |
| Stack Overflow trust figures | 2026 edition was in the field as of September 2026 and will supersede these. | "As of the 2025 edition, the most recent published…" |
| GitClear's trend lines | Vendor dataset, AI-detection method undisclosed, "YTD" figures move every quarter. | "GitClear — a developer-analytics vendor — reports…" plus the year-to-date caveat. |
| Microsoft's +24% merged PRs | One company, one 16-week window, authors employed by a vendor that owns GitHub. Authors themselves note the window cannot surface a long-horizon decline. | "In a single-company telemetry study over sixteen weeks in early 2026…" |
| The 2× mandate 2.09× throughput | One AI-forward mid-sized firm, non-randomised adoption, activity-only construct. Authors say it is "not typical, immediate, or free". | Quote their caveat sentence alongside the number. It does the hedging for you. |
| "Agents are not mainstream" (52% not using) | From the 2025 Stack Overflow survey. Stack Overflow's own June 2026 post says agent usage has doubled. | Date it to 2025 and note the direction of travel. |
| Any model-specific figure | Frontier models turn over in months. | Name the model and date in the same sentence as the number. |

---

## Concrete example we can lift

**Worked example — the team that doubled output and slowed down**

A mid-sized B2B software company with an R&D organisation of several hundred engineers set a
documented "2×" mandate in mid-2025: double merged pull requests per engineer. It was an AI-forward,
permissive shop — commercial AI coding tools provisioned without per-seat caps or token budgets.
Researchers tracked **802 developers and 196,212 pull requests** from January 2024 to April 2026.
[18]

By the end of the window the mandate had, on its own terms, worked. AI-authored pull requests went
from near zero to **about 90%** of all PRs. Per-capita throughput reached **2.09× the baseline —
21.2 to 44.3 PRs per developer per month**. Within a given developer, holding composition fixed, the
gain was smaller but still real: **1.46× to 1.72×** depending on specification, rising to **1.99× by
nine months on the tool**.

Then look at where the work went.

Human review coverage fell **21 percentage points, from 89% of PRs to 68%**. Automated review rose
from about **19% to about 84%** of PRs and overtook human review entirely. The load on each
remaining human reviewer **doubled**. Review latency on AI-authored PRs rose about **20%**. And
end-to-end **PR cycle time went up 22%** after the mandate — the thing the mandate was meant to
compress.

The quality signals were the surprise: **merge rates stayed essentially flat** and **revert rates
declined slightly** (−0.067 for AI-authored PRs). Nothing visibly broke. The cost did not show up as
defects; it showed up as **displaced review capacity and longer cycle time**.

The gains were also not evenly distributed. Managers gained most, **+86%**. Individual contributors
through Principal gained **+27% to +42%**, statistically indistinguishable from one another.
Repositories created in 2022 or later gained **+44%**. **Legacy code gained +12%, and that result
was not statistically significant.**

The authors' own summary is the line to end on: *"We therefore read the result as evidence that a
near-doubling is attainable under favorable conditions and over a long enough horizon, not that it
is typical, immediate, or free."* [18]

Two caveats the book must carry with this example. Adoption was **not randomised** — developers
chose when and how heavily to use AI, so this is a quasi-experiment, not a trial. And throughput
here is an **activity construct**: merged PRs, which as Microsoft's researchers put it in a parallel
study, "are an imperfect proxy for throughput and reward small, frequent PRs". [17]

---

## Sources

[1] Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity (METR
blog) — https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/ — accessed 19
September 2026
[2] Becker, Rush, Barnes, Rein — *Measuring the Impact of Early-2025 AI on Experienced Open-Source
Developer Productivity*, arXiv:2507.09089 (submitted 12 July 2025, v2 25 July 2025) —
https://arxiv.org/abs/2507.09089 — accessed 19 September 2026
[3] We are Changing our Developer Productivity Experiment Design (METR, 24 February 2026) —
https://metr.org/blog/2026-02-24-uplift-update/ — accessed 19 September 2026
[4] Measuring the Self-Reported Impact of Early-2026 AI on Technical Worker Productivity (METR, 11
May 2026) — https://metr.org/blog/2026-05-11-ai-usage-survey/ — accessed 19 September 2026
[5] DORA | State of AI-assisted Software Development 2025 (landing page) —
https://dora.dev/dora-report-2025/ — accessed 19 September 2026
[6] DORA 2025 State of AI-assisted Software Development Report (Google Research publication record;
authors and methodology) —
https://research.google/pubs/dora-2025-state-of-ai-assisted-software-development-report/ — accessed
19 September 2026
[7] Announcing the 2025 DORA Report (Google Cloud Blog, 23 September 2025) —
https://cloud.google.com/blog/products/ai-machine-learning/announcing-the-2025-dora-report —
accessed 19 September 2026
[8] How are developers using AI? Inside Google's 2025 DORA report (blog.google, 23 September 2025) —
https://blog.google/innovation-and-ai/technology/developers-tools/dora-report-2025/ — accessed 19
September 2026
[9] DORA | Accelerate State of DevOps Report 2024 — https://dora.dev/research/2024/dora-report/ —
accessed 19 September 2026
[10] Rachel Stephens, *DORA 2025: Measuring Software Delivery After AI* (RedMonk, 18 December 2025)
— https://redmonk.com/rstephens/2025/12/18/dora2025/ — accessed 19 September 2026
[11] DORA | ROI of AI-assisted Software Development report (published 22 April 2026) —
https://dora.dev/ai/roi/report/ — accessed 19 September 2026
[12] New DORA Report Claims Strong Engineering Foundations Drive AI Return on Investment (InfoQ, 11
May 2026) — https://www.infoq.com/news/2026/05/dora-roi-ai-assisted-dev-report/ — accessed 19
September 2026
[13] Peng, Kalliamvakou, Cihon, Demirer — *The Impact of AI on Developer Productivity: Evidence from
GitHub Copilot*, arXiv:2302.06590 (13 February 2023) — https://arxiv.org/abs/2302.06590 — accessed
19 September 2026
[14] Does GitHub Copilot improve code quality? Here's what the data says (GitHub Blog, 18 November
2024, updated 6 February 2025) — **vendor-reported** —
https://github.blog/news-insights/research/does-github-copilot-improve-code-quality-heres-what-the-data-says/
— accessed 19 September 2026
[15] Paradis et al. — *How much does AI impact development speed? An enterprise-based randomized
controlled trial*, arXiv:2410.12944 — https://arxiv.org/abs/2410.12944 — accessed 19 September 2026
[16] Borg, Hewett, Hagatulah, Couderc, Söderberg, Graham, Kini, Farley — *Echoes of AI:
Investigating the Downstream Effects of AI Assistants on Software Maintainability*, arXiv:2507.00788
(1 July 2025, v3 26 February 2026) — https://arxiv.org/abs/2507.00788 — accessed 19 September 2026
[17] Murphy-Hill, Butler, Savelieva (Microsoft) — *Adoption and Impact of Command-Line AI Coding
Agents: A Study of Microsoft's Early 2026 Rollout of Claude Code and GitHub Copilot CLI*,
arXiv:2607.01418v1 (1 July 2026) — **authors are Microsoft employees; Microsoft owns GitHub** —
https://arxiv.org/html/2607.01418v1 — accessed 19 September 2026
[18] He, Agarwal, Denisov-Blanch, Azaletskiy, Koyejo, Vasilescu — *AI Writes Faster Than Humans Can
Review: A Longitudinal Study of an Enterprise 2x Mandate*, arXiv:2607.01904v1 —
https://arxiv.org/html/2607.01904v1 — accessed 19 September 2026
[19] Agarwal, He, Vasilescu — *AI IDEs or Autonomous Agents? Measuring the Impact of Coding Agents
on Software Development*, arXiv:2601.13597 (20 January 2026, rev. 27 January 2026) —
https://arxiv.org/abs/2601.13597 — accessed 19 September 2026
[20] Li, Zhang, Hassan — *AIDev: Studying AI Coding Agents on GitHub*, arXiv:2602.09185 (9 February
2026); also MSR 2026 — https://arxiv.org/abs/2602.09185 — accessed 19 September 2026
[21] Raida & Hou (Rochester Institute of Technology) — *Early Adoption of Agentic Coding Tools by
GitHub Projects*, arXiv:2607.14037v2, KDD 2026 Workshop on Agentic Software Engineering (SE 3.0), 9
August 2026 — https://arxiv.org/html/2607.14037 — accessed 19 September 2026
[22] *The Fast and Spurious: Developer Productivity with GenAI*, arXiv:2510.24265 —
https://arxiv.org/abs/2510.24265 — accessed 19 September 2026
[23] 2025 Stack Overflow Developer Survey — AI section — https://survey.stackoverflow.co/2025/ai —
accessed 19 September 2026
[24] Mind the gap: Closing the AI trust gap for developers (Stack Overflow blog, 18 February 2026) —
https://stackoverflow.blog/2026/02/18/closing-the-developer-ai-trust-gap/ — accessed 19 September
2026
[25] The 2026 Developer Survey is now open (for human developers only) (Stack Overflow blog, 23 June
2026) —
https://stackoverflow.blog/2026/06/23/the-2026-developer-survey-is-now-open-for-human-developers-only/
— accessed 19 September 2026
[26] The Maintainability Gap: 2026 AI Code Quality Research (GitClear) — **vendor-reported** —
https://www.gitclear.com/the_ai_code_quality_maintainability_gap — accessed 19 September 2026
[27] AI Copilot Code Quality: 2025 Data Suggests 4x Growth in Code Clones (GitClear) —
**vendor-reported** — https://www.gitclear.com/ai_assistant_code_quality_2025_research — accessed 19
September 2026
[28] AI for Developer Productivity: What Now? (Uplevel, 18 October 2024, updated 21 July 2026) —
**vendor-reported** — https://uplevelteam.com/blog/ai-for-developer-productivity — accessed 19
September 2026
[29] 2026 Software Engineering Benchmarks Report (LinearB) — **vendor-reported** —
https://linearb.io/resources/software-engineering-benchmarks-report — accessed 19 September 2026
[30] How AI-Generated Code Is Increasing Code Review Burden (Faros AI, 21 May 2026; figures from the
"Acceleration Whiplash" AI Engineering Report 2026) — **vendor-reported** —
https://www.faros.ai/blog/ai-code-quality-senior-engineer-review-burden — accessed 19 September 2026
[31] Schreiber & Tippe — *Security Vulnerabilities in AI-Generated Code: A Large-Scale Analysis of
Public GitHub Repositories*, arXiv:2510.26103 (30 October 2025) — https://arxiv.org/abs/2510.26103 —
accessed 19 September 2026
[32] Butler, Suh, Haniyur, Hadley — *Dear Diary: A randomized controlled trial of Generative AI
coding tools in the workplace*, arXiv:2410.18334 (24 October 2024) —
https://arxiv.org/abs/2410.18334 — accessed 19 September 2026
[33] Stanford Software Engineering Productivity Research (SWEPR) group —
https://softwareengineeringproductivity.stanford.edu/ — accessed 19 September 2026
[34] AI Coding Assistant Benchmarks 2026: Developer Velocity vs. Technical Debt (Code Ninety, 11
February 2026, updated August 2026) — **vendor-reported, DO NOT CITE** —
https://codeninety.com/research/developer-productivity-and-ai-tech-debt-2026 — accessed 19 September
2026
[35] *Coding Beyond Your Training: Claude Code and the Technological Frontier of Software
Developers*, arXiv:2605.25438v1 — https://arxiv.org/html/2605.25438v1 — accessed 19 September 2026
[36] Pinna, Gong, Williams, Sarro — *Comparing AI Coding Agents: A Task-Stratified Analysis of Pull
Request Acceptance*, arXiv:2602.08915, MSR '26 (13–14 April 2026, Rio de Janeiro) —
https://arxiv.org/pdf/2602.08915 — accessed 19 September 2026
[37] AI is eroding code quality states new in-depth report (DevClass, 20 February 2025; reporting on
and contextualising GitClear's 2025 dataset and exclusions) —
https://www.devclass.com/ai-ml/2025/02/20/ai-is-eroding-code-quality-states-new-in-depth-report/1626250
— accessed 19 September 2026
