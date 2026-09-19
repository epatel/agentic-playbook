# Review practice for code you did not write

**Question asked:** What is actually known about reviewing code you did not author — the empirical
code-review literature that transfers, the automation-bias literature on rubber-stamping machine
output, what teams and open-source projects are actually doing in 2026 for agent-authored code,
whether AI review tools work, and which concrete review techniques survive scrutiny. Feeds the
play *Review code you did not write* in the Verification & Trust suite.

**Researched:** 19 September 2026

**Confidence:**

- **Classic review research (size, rate, reviewer count, what review actually finds): high.**
  Primary papers and the primary Cisco case-study text were read in full. But see the *Do not
  cite* section — the most-quoted numbers are not the ones the studies actually measured.
- **Automation bias / complacency: medium-high.** The aviation and clinical literature is solid
  and old; the transfer to code review is inference, not measurement. One 2026 study measures
  reviewer habituation on agent PRs directly, and it is a single paper.
- **2026 empirical work on agent-PR review: medium.** Four independent 2026 papers, all on the
  same underlying `AIDev`/`CodAGE` GitHub corpora, so they are not as independent as the count
  suggests. All are descriptive, none establishes causation, several are preprints.
- **Open-source policy landscape: high.** All policies read at the primary source (kernel docs,
  QEMU docs, LLVM docs, Debian vote page, Gentoo wiki, Stenberg's own blog).
- **AI review tool efficacy: low.** Vendor benchmarks measure recall and quietly omit precision;
  the one independent-ish comparison has a disclosed conflict of interest and n=146 PRs on one
  codebase. Treat all numbers here as directional at best.
- **What real teams do: low-medium.** GitHub's own guidance is published and specific. Beyond
  that, most "what teams do in 2026" material traces to podcasts, conference talks, and vendor
  blogs rather than engineering posts with detail.

## Findings

### The classic review-size research, read at source

The famous numbers come from a **vendor case study, not a peer-reviewed paper**: Smart Bear
Software's 10-month study of the Cisco MeetingPlace product group, wrapped up May 2006, published
as an essay in Jason Cohen's book *Best Kept Secrets of Peer Code Review*. [1]

Methodology, exactly as stated: "With 2500 reviews of 3.2 million lines of code written by 50
developers, this is the largest case study ever done on what's known as a 'lightweight' code
review process." Reviews began July 2005 and were conducted in Smart Bear's own Code Collaborator
tool, enforced by a Perforce check-in trigger. [1]

Two methodological facts that almost never travel with the numbers:

- The sample was filtered. Reviews shorter than 30 seconds, faster than 1500 LOC/hour, or larger
  than 2000 lines were discarded: "This attempt at isolating 'interesting' review cases cuts out
  21% of the reviews." [1]
- **The defect analysis is n=300, not n=2500.** The tool's own defect database was judged
  unusable, so: "we took a random sample of 300 reviews and studied the conversations in each one
  to measure the number of true defects as defined above." [1]

And the definition of "defect" is very broad — it includes style and readability: "If the code is
right but unintelligible due to poor documentation, it's a defect. If the code is right but
there's a better way to do it, it's a defect." [1] Every "defect density" figure below is a
density of *review comments that caused a change*, not a density of bugs.

Measured results [1]:

| Finding | Exact figure as stated |
|---|---|
| Average defect density | "Our reviews had an average 32 defects per 1000 lines of code." |
| Reviews finding nothing | "61% of the reviews uncovered no defects" |
| Size effect | "Anything below 200 lines produces a relatively high rate of defects... no review larger than 250 lines produced more than 37 defects per 1000 lines of code" |
| Rate effect | "Reviewers slower than 400 lines per hour were above average... when faster than 450 lines/hour the defect density is below average in 87% of the cases." |
| Defect rate | "The overall defect rate was 13 defects per hour with 85% of the reviews slower than 25 defects per hour." |
| Size vs. rate | "94% of all reviews had a defect rate under 20 defects per hour regardless of review size." |

Stated conclusions, verbatim: "LOC under review should be under 200, not to exceed 400";
"Inspection rates less than 300 LOC/hour result in best defect detection. Rates under 500 are
still good"; "Total review time should be less than 60 minutes, not to exceed 90"; and the summary
advice, "review between 100 and 300 lines of code at a time and spend 30-60 minutes to review
it." [1]

The study carries its own caveat on the size finding, in a footnote: it assumes "true defect
density is constant over both large and small code changes," i.e. that a 400-line change contains
four times the bugs of a 100-line change. If that assumption fails, the "defect density falls with
size" curve is partly an artefact. [1]

### Author preparation — the finding most relevant to agent PRs, and its own counter-argument

Cisco tested whether authors annotating their own diff before review changes outcomes. "For all
reviews with at least one author preparation comment, defects density is never over 30; in fact
the most common case is for there to be no defects at all!" [1]

Crucially, the authors give **two opposed readings and pick one**: either the act of preparing
made the author find and fix their own bugs, or "prepping disables the reviewer's capacity for
criticism. Author comments prime the reviewer for what to expect. As long as the code matches the
prose, the reviewer is satisfied." They say "We believe the first conclusion is more tenable" on
the strength of a qualitative scan of the reviews. [1] This is contested inside the primary source
itself, and it is the single most transferable question for agent PRs: *does requiring the agent's
plan in the PR body help the reviewer, or anchor them?*

### Google's published practice — a different regime entirely

The ICSE-SEIP 2018 case study: "12 interviews, a survey with 44 respondents, and analysis of review
logs for 9 million reviewed changes," from the Critique tool over two years, "created by more than
25,000 authors and reviewers." [2]

Measured [2]:

- "over 35% of the changes under consideration modify only a single file and about 90% modify
  fewer than 10 files. Over 10% of changes modify only a single line of code, and the median
  number of lines modified is 24."
- "fewer than 25% of changes have more than one reviewer, and over 99% have at most five
  reviewers with a median reviewer count of 1."
- "The overall (all code sizes) median latency for the entire review process is under 4 hours."
- "developers spend an average of 3.2 (median 2.6 hours a week) reviewing changes."
- Comment volume peaks with size: "reaching a peak of 12.5 comments per change for changes of
  about 1250 lines."

Google's own published guidance sets a softer bound than Cisco's: "100 lines is usually a
reasonable size for a CL, and 1000 lines is usually too large, but it's up to the judgment of your
reviewer," and "A 200-line change in one file might be okay, but spread across 50 files it would
usually be too large." Reviewers "have discretion to reject your change outright for the sole
reason of it being too large." [3] The reviewer-facing guide orders what to look for as design,
functionality, complexity, tests, then naming/comments/style, and the gate is "Don't accept CLs
that degrade the code health of the system." [4]

### Review does not mainly find bugs — and this is the most important transferable result

Bacchelli and Bird, ICSE 2013, at Microsoft: "Review comments about defects are few, comprising
one-eighth of the total in our sample, and mostly address 'micro' level and superficial concerns."
The most frequent comment category was code improvements, "165 (29%) comments." The paper's
headline conclusion is that "code and change understanding is the key aspect of code reviewing."
[5]

Google's survey echoes it from the other side: of 44 respondents, "Only 2 respondents said the
comments had found a bug," and the interviewed long-time employee said the original motivation was
"to force developers to write code that other developers could understand," with bug-finding
explicitly secondary. [2]

Implication for the play: the historical function of review is *shared understanding*, and the
author is normally the person who already has it. With agent-authored code, nobody has it. The
review is doing a job it was never measured doing.

### Rubber-stamping: measured baseline before AI

ICSME 2024, five large-scale projects: "64.7% of the PRs in these projects exhibited comment-free
reviews," and "Comment-free reviews exhibit the LGTM smell 3.5 times more frequently than the
commented reviews," with more late commits after approval. [6] This is the pre-AI baseline: two
thirds of reviews already left no written trace.

### Automation bias — the transferable literature

- Skitka, Mosier and colleagues (aviation, late 1990s) established the omission/commission split:
  omission errors are failures to act because the automation did not flag; commission errors are
  following an automated directive despite contradictory information from more reliable sources.
  Reported omission error rate around 55%; commission errors from following incorrect automation
  "approached 100%." Accountability for performance or decision accuracy reduced bias rates;
  training reduced commission but not omission errors. [7]
- Goddard, Roudsari and Wyatt, *JAMIA* 19(1), January 2012, systematic review of automation bias
  in clinical decision support. The headline finding relevant here is negative: "there is a paucity
  of deliberate empirical evidence for this effect." Overall performance usually improves with
  decision support, but new error classes are introduced and go unrecognised. [8]
- 2026 replication in a different domain: Rosbach et al., computational pathology, 28 experts,
  online experiment. "7% automation bias rate, defined as accepted negative consultations where
  previously correct independent judgments were overturned by incorrect AI advice," a statistically
  significant anchoring effect on AI output that intensified under time pressure, and — the other
  half — AI assistance improved overall diagnostic performance despite the bias-driven errors.
  Higher confidence during AI-assisted decisions correlated with *more* reliance. [9]

### Automation bias measured on code specifically

Perry, Srivastava, Kumar and Boneh, ACM CCS 2023. 47 participants after exclusions (33
experiment, 14 control), five security-related programming tasks, OpenAI `codex-davinci-002`. [10]

- "Participants with access to an AI assistant wrote insecure solutions more often than those
  without access to an AI assistant for the majority of tasks."
- Q1 (symmetric encryption): "67% of experiment participants provided a correct solution compared
  to 79% of control participants"; experiment group significantly more likely to write an insecure
  solution (p = 0.017) and to use trivial ciphers (p = 0.018).
- Q2 (ECDSA signing): "only 3% of participants with access to an AI writing a secure solution
  compared to 21% of the control group (p = 0.039)," while correctness barely moved (55% vs 64%).
- "Participants with access to an AI assistant were also more likely to believe they wrote secure
  code."
- The protective factor: "participants who trusted the AI less and engaged more with the language
  and format of their prompts... provided code with fewer security vulnerabilities."

Small n, 2022 model. Cite for mechanism, not magnitude.

### Reviewer habituation measured directly on agent PRs (2026)

Yu, Liu and Zhang, arXiv September 2026. 11,429 code reviews from 400 repeat reviewers over 207
days, drawn from the AIDev corpus (Copilot Autofix, Devin, Codex CLI, Cursor, Claude Code PRs,
January–July 2025, repos with ≥100 stars); 10,104 human-authored inline comments. [11]

- Approval rate rose from **30.5% early to 36.6% late** for the same reviewers, Δ = +6.1
  percentage points, Wilcoxon p = 8.6×10⁻⁸, Cohen's d = 0.25; "+14.9 percentage points across
  experience deciles," monotonic.
- Human-authored PR approval over the same months stayed stable, which rules out general reviewer
  leniency as the confound.
- Surface linguistic metrics did **not** detect the drift (all four hand-crafted features
  non-significant after Bonferroni); only sentence-embedding analysis did. So habituation is
  invisible in the obvious metrics.
- Texture of the corpus: "Median comment length: 11 words. 24% of comments contained ≤5 words."

This is the closest thing to a measured attention-decay curve for agent output. It is one paper,
descriptive, and the effect is small.

### What review of agent PRs actually looks like on GitHub (2026)

Duma et al., EASE 2026 (arXiv May 2026), 33,596 agent-authored PRs in repos with ≥100 stars from
the AIDev dataset, plus 9,616 agent-authored and 5,574 human-authored PRs in overlapping repos.
[12]

- "61.38%" of AI-generated PRs receive no recorded review activity at all.
- Among reviewed agent PRs: 58.77% agent-only, 10.14% human-only, 31.09% mixed.
- Human-only review: **8.08% for agent-authored PRs vs 25.21% for human-authored** in the same
  repositories (large effect, V=0.25). Mixed human–agent: 34.29% vs 21.86%.
- Comment composition: on human PRs, "93.56%" of comments are direct human review; on agent PRs,
  65.53%, with 25.92% being *agent-steering commands* rather than evaluation.
- The authors' framing: "Reviews of agent-authored pull requests more often take the form of
  automation-mediated interaction, with human involvement frequently expressed through agent
  steering rather than standalone evaluation."
- Stated limitation, important: "Silent approvals untracked" — PRs approved with no comment are
  classified as "no review," so the 61.38% overstates absence of human eyes.

Huang et al., MSR 2026 (arXiv January 2026), 3,858 Python PRs (repos >500 stars) plus a 617-PR
case study on crewAI: AI agents' Average Max Redundancy 0.2867 vs humans' 0.1532, **1.87× higher
semantic duplication** (p<0.001). Humans removed 25.51 LOC on average vs agents' 16.60 (p<0.001).
And the sentiment result: reviewers "tend to express more neutral or positive emotions towards
AI-generated contributions than human ones" despite the higher redundancy. [13]

Agarwal, Miller, Kästner and Vasilescu, July 2026: coded a stratified random sample of 3,100
documents from 38,709 grey-literature sources into "a causal model of 26 constructs and 67
relationships (64 directed, 3 contested)." Their observational finding is that agent PRs are
"reviewed less frequently, merged several times faster, and discussed less than human-authored
ones" — but they explicitly note "these trends reverse depending on analysis choices." Central
claim: "review is the control point through which a coding agent's effect on software is decided,
and that AI does not fix the sign of that effect: the team sets it." [14]

### Do AI code-review tools work?

**Vendor's own limitations doc first.** GitHub, on Copilot code review: "Copilot code review has a
risk of hallucination—it may highlight problems in reviewed code that do not exist or are based on
misunderstandings of the code"; it "may not identify all of the problems that are present in code,
especially where changes are large or complex"; and "You should always review and verify the
feedback generated by Copilot code review, and supplement Copilot's feedback with careful human
review." **vendor-reported**, but notable because it is the vendor conceding the point. [15]

**Independent-ish measurement.** Chowdhury et al., MSR 2026: 3,109 PRs from AIDev, with 98 closed
CRA-only-reviewed PRs examined in detail. [16]

- CRA-only reviewed PRs merged at **45.20%** vs **68.37%** for human-only reviewed PRs — a 23.17
  percentage-point gap. Abandonment 34.88% vs 21.60%.
- "Among 98 closed CRA-only PRs, 60.2% contained 0-30% actionable feedback; 92.31% of CRAs (12 of
  13) showed average signal ratios below 60%."
- The paper is framed explicitly against industry claims that CRAs can handle a large share of PRs
  without human input.

**One team's three-week bake-off**, n=146 merged PRs on one PHP/React backend SaaS codebase,
default configuration, author works at Sentry (disclosed conflict — Sentry makes one of the four
tools). [17] Findings/PR and false-positive rate: CodeRabbit 281 findings, 2.3% FP; Sentry Seer
158, 10.0% overall; Greptile 120, 0% FP on verdicted findings; Cursor BugBot 128, 4.8% FP. The
result worth carrying is the **non-overlap**: "93.4% of flagged coordinates flagged by exactly one
reviewer" — four tools on the same 146 PRs essentially never agreed on a line.

**AI reviewing AI, at scale.** Selvanayagam and Ghaleb, arXiv August 2026, CodAGE corpus
2024-01-01 to 2026-04-15: "248,641 unique AI-attributed PRs that received at least one
AI-attributed review," growth "more than two orders of magnitude from 2025-Q1 to 2025-Q3." Modal
pairing: Codex authored, Copilot reviewed (18,114 pairs). Median review latency **1.2 minutes**
cross-product, 4.7 minutes same-product. Same-product pairs received 58–65% more comments per PR,
though effect sizes were "small or negligible." The paper reports no precision, recall, or merge
outcomes. [18]

That last one is the circularity finding in numbers: a quarter of a million PRs in which a machine
wrote the code and a machine signed off on it, with a median of about seventy seconds between.

### Open-source policy: three camps, and they are not converging

| Project | Position | Primary wording |
|---|---|---|
| QEMU | Ban | "Current QEMU project policy is to DECLINE any contributions which are believed to include or derive from AI generated content." Reason: "the copyright and license status of the output is ill-defined," so DCO clauses (b)/(c) cannot be satisfied. [19] |
| Gentoo | Ban | Council voted 14 April 2024 to forbid contributing "any content created with the assistance of Natural Language Processing artificial intelligence tools." Rationale: copyright, quality, ethics. [20] |
| NetBSD | Presumed tainted | AI-generated code presumed "tainted"; no commit without explicit core approval. [21] |
| Linux kernel | Disclose + human accountable | "AI agents MUST NOT add Signed-off-by tags. Only humans can legally certify the Developer Certificate of Origin (DCO)." Tag format `Assisted-by: LLM [TOOL1] [TOOL2]`. Human is responsible for "Reviewing all AI-generated code" and "Taking full responsibility for the contribution." [22] |
| LLVM | Disclose + reviewer-time test | "Contributors can use whatever tools they would like to craft their contributions, but there must be a human in the loop." "Contributors must read and review all LLM-generated code or text before they ask other project members to review it." "The contributor is always the author and is fully accountable for their contributions." "A contribution should be worth more to the project than the time it takes to review it." "AI tools must not be used to fix GitHub issues labelled 'good first issue.'" [23] |
| Debian | Allowed, labelling explicitly optional | GR vote 15–28 August 2026, 1,045 eligible developers; winner was option 5, "Responsible Use of Generative AI," which "neither endorses nor prohibits" AI tools. On labelling: "We encourage our contributors to disclose whether a contribution was made with AI assistance, but do not require them to do so." [24] |

The trailer convention that is spreading is `Assisted-by:` (light assistance) escalating to
`Generated-by:` (substantial AI output), deliberately chosen over `Co-authored-by:` because
co-authorship implies a rights certification an AI cannot make — the human who ran the agent stays
the sole author and signer. Adopters include the Linux kernel, LLVM, Fedora, Rocky Linux,
OpenTelemetry, and the OpenInfra Foundation; the Apache Software Foundation uses `Generated-by:`
in machine-parsable Tooling-Provenance files. [25]

The Linux kernel doc also contains a direct instruction to submitters that doubles as a reviewer
heuristic: "If the fix could not be built or tested, or if no reproducer could be produced, say so
explicitly: maintainers currently waste too much time analyzing unverified reports and untested
fixes." [22]

### The curl bug-bounty arc — verified at source, and it does not end where people think it does

Daniel Stenberg, 26 January 2026: the curl bug-bounty ran April 2019 to 31 January 2026, paid out
"87 confirmed vulnerabilities and over 100,000 USD." The confirmation rate was "somewhere north of
15% of the submissions ending up confirmed vulnerabilities"; then "Starting 2025, the
confirmed-rate plummeted to below 5%. Not even one in twenty was *real*." Stenberg describes
"mind-numbing AI slop" that takes "a serious mental toll." Monetary rewards were eliminated
entirely; reporting moved off HackerOne. [26]

The part the coverage mostly dropped: 25 February 2026, curl returned to HackerOne from 1 March
2026 because GitHub's private vulnerability reporting was inadequate — but "The reward money is
still gone, *there is no bug-bounty*, no money for vulnerability reports." And: "Since we dropped
the bounty, the inflow tsunami has dried out *substantially*." [27]

And then, 22 April 2026: report volume was "about double the rate we had through 2025," the
confirmation rate had recovered to "somewhere in the 15-16% range" — 2024 pre-AI levels — "The
slop situation is not a problem anymore," and "Almost every security report now uses AI to various
degrees." Stenberg projected "closer to 50 curl vulnerabilities in 2026." [28]

So the honest version of the curl story is: **the money, not the AI, was the slop vector.** Once
the bounty was removed, more reports arrived, they were more likely to be real, and nearly all of
them were AI-assisted. Anyone citing curl as proof that AI submissions are worthless is citing
January 2026 and stopping.

**Do not extend that into a claim about the recovery. Added 19 September 2026 by `3884b4f3fc82`,
which re-read all three posts.** "The money was the slop vector" is supported for the *January*
diagnosis — Stenberg suspected "the idea of getting money for it is a big part of the explanation"
for the volume. It is **not** supported as the explanation for the April turnaround, and the arc
recorded above is why: **two variables moved, not one.** Reporting left HackerOne on 1 February and
came back on 1 March, and post [28] dates the change from the second, in consecutive sentences:
"In March 2026, the curl project went back to Hackerone again once we had figured out that GitHub
was not good enough. / From that day, the nature of the security report submissions have changed. /
The slop situation is not a problem anymore." Stenberg also names tooling as a driver — "The tools
are still improving" — and his February post immediately hedges the tsunami quote ("Perhaps partly
because of our switch over to GitHub?"). Part III printed "the variable that changed was the money,
not the tooling" and has been rewritten to carry both changes and Stenberg's own attribution.

Two smaller fixes made at the same time, both now corrected in Part III: the bounty was
**announced** ended on 26 January and **stopped on 31 January**, and the post pairs "87 confirmed
vulnerabilities and over 100,000 USD" rather than saying a bounty was paid out on each of the 87.
Every quotation Part III prints from these three posts is verbatim, italics included.

### Team practice in 2026

GitHub's own published guidance (7 May 2026) is the most specific thing in the open. Vendor
figures first, **vendor-reported**: "GitHub Copilot code review has processed over 60 million
reviews, growing 10x in less than a year" and "More than 1 in 5 code reviews on GitHub now involve
an agent." [29]

Their stated triggers for sending an agent PR back before reviewing it: diffs touching more than
five unrelated files; a purpose that cannot be described in one sentence; no implementation plan
provided; only test-file changes accompanying CI failures. Their five named failure modes are CI
gaming ("Any CI weakening is a hard stop"), code-reuse blindness, hallucinated correctness,
"agentic ghosting" (request the implementation plan before investing review time in a large
unstructured PR), and untrusted input reaching workflow prompts. The published review order is:
classify the task, check CI changes first, scan for duplicated utilities, trace one critical path
end to end, review security boundaries, require evidence via tests. Their framing: "Judgment is
the bottleneck, and that's fine." [29]

Telemetry on what the load actually looks like — Faros AI, "AI Engineering Report 2026," analysis
as of March 2026, approximately two years of telemetry from 22,000 developers and 4,000 teams,
comparing each team's two lowest-AI-adoption quarters against its two highest, Spearman rank
correlation, p<0.05, ≥6 companies per reported metric. **Vendor-reported**, but with a stated
methodology. [30]

- "+156.6% median time to first PR review"
- "+199.6% average time in PR review"
- "+441.5 [%] median time in PR review"
- "+51.3% average PR size"
- "+31.3% PRs merged without any review" — which the report calls "the most urgent finding in
  this section"
- "+25% average review comments per PR"; "+22.7% average length of PR review comments"
- "25% of PRs are reviewed by AI agents (up from zero in prior dataset)"

The report flags its own confound on the comment metrics: agentic review went from zero to 25% of
PRs in the same window, so rising comment counts may be agents, not humans.

DORA's 2025 State of AI-assisted Software Development, "nearly 5,000 technology professionals":
"90% of survey respondents report using AI at work. More than 80% believe it has increased their
productivity," while "30% report little or no trust in the code generated by AI." The delivery
finding: a positive relationship with throughput and product performance, but "AI adoption does
continue to have a negative relationship with software delivery stability." [31]

And the counterweight on speed — METR's RCT, July 2025: 16 experienced open-source developers, 246
issues, repositories averaging "22k+ stars and 1M+ lines of code" they had contributed to for
years. "When developers are allowed to use AI tools, they take 19% longer to complete issues,"
against a 24% forecast speedup and a 20% *post hoc* believed speedup. METR state explicitly that
they do **not** claim "AI systems do not currently speed up many or most software developers." [32]
METR changed the experiment design in February 2026. [33]

### Concrete review techniques with some evidential basis

- **Read against a stated purpose, not for style.** Google's ordering puts design and functionality
  above naming and style, and the gate is code health, not correctness alone. [4] Bacchelli and
  Bird's result that only one-eighth of comments concern defects, and that understanding is the
  real activity, argues the same way. [5]
- **Scenario/perspective reading beats ad-hoc reading; checklists are roughly as good.**
  Perspective-Based Reading assigns reviewers a role (tester, developer, user) and gives each a
  scenario to work through. PBR reliably beats ad-hoc review for individual and team defect
  detection. Against checklist-based reading the results are mixed: one controlled experiment with
  59 student subjects found effectiveness essentially equal (PBR 69%, CBR 70%), with PBR taking
  less time but CBR having lower cost per defect. [34] The transferable point is that *any*
  structure beats unstructured reading; the choice of structure matters less.
- **Require a reproducer or an explicit admission that there isn't one.** Kernel policy, stated as
  a fix for maintainer time waste. [22]
- **Cap the diff and send it back on size alone.** Google grants reviewers that authority
  explicitly [3]; GitHub names concrete triggers for agent PRs [29]; Faros recommends encoding PR
  size constraints into agent instructions [30].
- **Search for the duplicate before accepting the new utility.** Justified by the measured 1.87×
  redundancy in agent code [13] and named as a distinct failure mode by GitHub [29].
- **Check what the change does *not* do — particularly what it removed.** Agents removed 16.60 LOC
  on average where humans removed 25.51 (p<0.001) [13]; GitHub's "CI gaming" hard stop is the same
  instinct applied to test and lint configuration [29].
- **Author preparation / the agent's plan in the PR body.** Supported by Cisco's data, and
  undermined by Cisco's own alternative explanation — see *Contested claims*. [1]

## What is established practice vs. one team's habit

| Practice | Status | Basis |
|---|---|---|
| Review small changes; large diffs get less scrutiny per line | **Established** — replicated across Cisco, Google, Microsoft/Rigby-Bird | [1][2][3] |
| Exact bound of "200–400 lines" | **One vendor's study, 2006, n=300 for the defect analysis** | [1] |
| "100 lines reasonable, 1000 too large, reviewer's judgment" | **One company's published convention** (Google) | [3] |
| Review is mostly about understanding, not defect-finding | **Established** across Microsoft and Google | [2][5] |
| One reviewer is enough | **One company's convention** (Google: median 1) — contradicts Rigby & Bird's cross-company "two" | [2] |
| Automation bias is real in high-stakes human–machine loops | **Established** (aviation, clinical) | [7][8][9] |
| Automation bias is real and quantified *in code review* | **One 2026 preprint**, effect size small | [11] |
| Human is the author and signer; AI is disclosed, not credited | **Converging cross-project norm** (kernel, LLVM, Fedora, Rocky, OpenTelemetry, OpenInfra) | [22][23][25] |
| Mandatory labelling of AI contributions | **Contested** — Debian voted explicitly *not* to require it | [24] |
| Outright ban on AI contributions | **Minority position** (QEMU, Gentoo, NetBSD) | [19][20][21] |
| Requiring the agent's implementation plan in the PR | **One vendor's guidance** (GitHub), theoretically undercut by Cisco's priming hypothesis | [29][1] |
| Diff-size caps encoded into agent instructions | **One vendor's recommendation** (Faros); no measured before/after | [30] |
| AI review tools reliably catch real bugs | **Not established.** Vendor recall claims; independent signal ratios below 60% for 12 of 13 agents | [16][17] |
| "The human who ran the agent is the author" | **Established in policy across the major camps**, including permissive Debian | [22][23][24] |

## Contested claims

**1. Does putting the agent's plan in the PR help the reviewer, or anchor them?**
Cisco's data shows author-prepared reviews have near-zero defect density, and the authors read this
as the author having self-corrected. Their own alternative reading, in the same paragraph: "prepping
disables the reviewer's capacity for criticism... As long as the code matches the prose, the
reviewer is satisfied." [1] GitHub in 2026 recommends demanding the implementation plan before
reviewing. [29] Nobody has measured which effect dominates when the "author" is a model that
produces fluent, confident prose about its own work. Carry both halves; this is the sharpest open
question in the play.

**2. Two reviewers or one?**
Rigby and Bird found convergence on two reviewers across AMD, Chrome OS, and three Microsoft
projects, and concluded "two reviewers find an optimal number of defects." Google measured "a
median reviewer count of 1" with fewer than 25% of changes having more than one, and found that
"A greater number of reviewers results in a greater average number of comments on a change" — the
opposite of Rigby and Bird's diminishing return. [2]

**3. Is AI-generated submission volume a quality problem?**
January 2026 curl: confirmation rate "below 5%," bounty killed, "mind-numbing AI slop." [26] April
2026 curl: volume doubled, confirmation rate back to "15-16%," "The slop situation is not a problem
anymore," "Almost every security report now uses AI to various degrees." [28] Both are Stenberg,
three months apart, primary. The variable that changed was the money.

**4. Does AI assistance make reviewers/operators worse or better overall?**
Perry et al.: significantly less secure code, and higher confidence in it. [10] Rosbach et al.: a
measurable 7% automation-bias rate *and* improved overall diagnostic performance. [9] Goddard et
al.: overall performance usually improves, but new errors are introduced and go unrecognised. [8]
The honest summary is that the aggregate can improve while a specific new failure mode appears —
and the new failure mode is exactly the one a reviewer is supposed to catch.

**5. Are agent PRs under-reviewed?**
Duma et al. measure 61.38% with no recorded review activity and human-only review at 8.08% vs
25.21%. [12] But they state that silent approvals are untracked and counted as "no review." Agarwal
et al. find agent PRs "reviewed less frequently, merged several times faster" — and then say
"these trends reverse depending on analysis choices." [14] The direction is probably right; the
magnitude is not settled.

## Contradictions and gaps

- **No study measures whether a human reviewing agent-authored code catches the bugs a human
  reviewing human code would catch.** Everything in the 2026 corpus is observational on GitHub
  metadata — merge rates, comment counts, approval rates. Nobody has run the controlled
  experiment. This is the biggest gap and the play should say so.
- **No measured attention-decay curve for code review.** The habituation paper measures drift over
  *months* of repeated exposure [11], not decay within a sitting. The within-sitting claim is
  asserted, not measured — see below.
- **The AIDev/CodAGE monoculture.** Four of the 2026 papers [11][12][13][16] and the fifth's
  observational half [14] draw on the same one or two GitHub corpora, sharing their agent-labelling
  errors and their bias towards public repos with ≥100 stars. Treat "four independent studies
  agree" with suspicion.
- **No published engineering post from a named non-vendor company with before/after numbers on an
  agent-PR review policy.** Stripe's widely-repeated "1,300 agent PRs a week, all human-reviewed"
  traces to a podcast appearance by an engineer, not to a Stripe engineering post; it is
  directionally interesting and not citable as measurement.
- **Precision is systematically unreported by AI review vendors.** Greptile's own benchmark page
  publishes catch rates and states that "false positives, style suggestions, and unrelated comments
  did not affect the catch rate" — i.e. it measures recall and excludes precision by construction.
- **Nobody has published a defensible position on the circularity problem.** There are 248,641
  measured instances of a machine reviewing a machine's code at a 1.2-minute median latency [18],
  and no study of whether that catches anything. The MSR 2026 signal-ratio result [16] is the
  closest proxy and it is about noise, not about circularity.

### Do not cite

- **"A review of 200–400 LOC over 60 to 90 minutes should yield 70–90% defect discovery."** This
  does not appear anywhere in the primary Cisco case study. [1] It appears on SmartBear's marketing
  "Best Practices for Code Review" page, self-attributed to that study. [35] The study measured
  defect *density*, not the fraction of existing defects found — it could not have measured the
  latter, because it was conducted in situ and the true defect count was unknown. The study says so:
  "because this was a study in situ and not in a laboratory, we don't know how each of these reviews
  would have fared with a different process." [1]
- **"Defect detection rates plummet after 60 minutes."** Present in the Cisco study's conclusions,
  but as an inherited premise, not a result: "Another explanation comes from the well-established
  fact that after 60 minutes reviewers 'wear out' and stop finding additional defects," footnoted to
  another essay in the same vendor book. [1] Not measured by the Cisco data. If the book uses it,
  hedge it as an old, widely-repeated rule of thumb from the inspection era, not a finding.
- **"AI-assisted pull requests run 408 changed lines at the 75th percentile against 157 for
  unassisted work"** and **"AI-assisted PRs run 2.5× larger... wait roughly 16 hours for a first
  reviewer versus 200 minutes."** Circulate attached to the Faros 2026 report. The report's own text
  says "+51.3% average PR size" and gives review timing only as percentage changes. [30] The
  absolute figures are not in the report as fetched.
- **"65% of pull requests get rubber stamped with LGTM"** and **"90% of reviews at Fortune 500
  companies are approved in under 3 minutes."** Blog/Substack claims with no traceable study. The
  citable adjacent number is the ICSME 2024 "64.7% of PRs exhibited comment-free reviews" [6] —
  which is a different claim.
- **"15–25% false positive rate for GitHub Copilot code review."** Attributed to unnamed "third
  party research" in secondary coverage. GitHub's own docs concede hallucination risk without
  quantifying it. [15] No primary found.
- **Greptile "82% catch rate, 41% higher than Bugbot (58%)"** and **Signal65 "Bugbot 95.95%
  precision."** Vendor and vendor-commissioned benchmarks; the first publishes no per-tool
  false-positive counts. **vendor-reported**; do not present as measurement.
- **"Vendors claim code review agents handle 80% of pull requests without human input."** This is
  the MSR 2026 paper's characterisation of industry marketing [16]; I did not locate a vendor
  actually making that claim in those words.
- **The cluster of figures in Addy Osmani's January 2026 essay** — "75% higher error rate,"
  "1.75× higher logic errors and 2.74× more XSS," "~18% larger PRs (Jellyfish)," "~24% increase in
  incidents per PR and ~30% higher change failure rates (Cortex 2026)," "70–80% of low-hanging
  fruit caught (Graphite)" — are reported second hand without linked primaries in the piece. [36]
  The essay is worth citing for its framing lines; the numbers need chasing to source first. The one
  I did verify is Veracode's 45%, which is real but is about *generated* code security, not review:
  over 100 LLMs, 80 coding tasks across Java, Python, C# and JavaScript, four OWASP-aligned CWEs,
  five task instances per language–CWE pair, SAST-detected; "AI-generated code introduced risky
  security flaws in 45% of tests," Java worst at 72%. [37] **vendor-reported.**
- **"Amazon issued an escalation memo requiring extra senior review for AI-assisted production
  changes."** Found only in aggregator content. No primary.

## Staleness assessment

| Claim | Why it rots | Suggested hedge |
|---|---|---|
| "Review under 200 lines, not to exceed 400" | 2006 data, Perforce-era tooling, 50 developers at one company, defect analysis n=300, and "defect" includes style | "The most-quoted number in code review comes from a single vendor case study at Cisco in 2005–06; it says under 200 lines, not to exceed 400. Treat it as a well-worn rule of thumb rather than a law." |
| 61.38% of agent PRs get no recorded review | Measured on 2025 GitHub data during the steepest part of the adoption curve; silent approvals miscounted | "As of the 2026 measurements — and the authors warn silent approvals are counted as no review —" |
| Approval rate drifts 30.5% → 36.6% with exposure | Single 2026 preprint on one corpus; small effect | "One 2026 study found reviewer approval of agent PRs drifting upward with exposure while approval of human PRs held steady." |
| Faros review-time and merged-without-review percentages | Vendor telemetry, single platform, self-selected customers, "analysis as of March 2026" | "One engineering-analytics vendor's 2026 telemetry across 22,000 developers reported..." |
| 25% of PRs reviewed by AI agents; 1 in 5 GitHub reviews involve an agent | Rising fast; both figures are already old by publication | Give the date in the sentence, or state it as a direction rather than a level. |
| AI review tool precision/recall figures | Model versions change quarterly; benchmarks are not reproducible | Do not give numbers. Say the tools disagree with each other almost completely and that vendors publish recall, not precision. |
| curl bug-bounty "confirmation rate below 5%" | Already superseded by curl's own April 2026 figure of 15–16% | Always carry both halves of the arc, or don't use curl at all. |
| Open-source AI policies | Debian voted August 2026; the kernel doc shipped in 2026; more projects moving | "As of late 2026, the camps are ban, disclose-and-hold-the-human-accountable, and permissive." |
| METR "19% slower" | Early-2025 models, 16 developers, and METR themselves changed the design in Feb 2026 | Cite for the perception gap (forecast +24%, felt +20%, measured −19%), not as a claim about current tools. |
| Perry et al. insecure-code figures | 2022 Codex model, n=47 | Cite the mechanism (trust correlates with insecurity; confidence rises while security falls), not the percentages. |

## Concrete example we can lift

**Worked example — the OCaml DWARF pull request (November 2025).**

Joel Reymont set out to add DWARF debugging support to OCaml's native compiler. He did not write
the code; by his own description he directed, shaped, cajoled, and reviewed Claude Code until it
produced the feature. The result was `ocaml/ocaml` PR #14369: more than 13,000 lines. [38]

The maintainers closed it. Their reasons, in the order that matters for this play:

1. **Provenance.** Many source files credited Mark Shinwell at Jane Street Europe as author.
   Shinwell works on OxCaml, an OCaml variant that already has DWARF support. Nobody could
   establish what the change was derived from.
2. **No prior design discussion.** The implementation arrived before the argument for it.
3. **No reviewer.** Gabriel Scherer, closing it: "none of the people who could plausibly be
   interested in reviewing and supporting a DWARF-support PR seem willing to consider doing the
   work." A 13,000-line change needs a reviewer who understands both DWARF and the native compiler,
   and OCaml has very few, all of them already committed elsewhere.
4. **The asymmetry itself.** Scherer noted that submitting very large, relatively-low-effort PRs
   risks halting the pull-request system, and that in his experience reviewing AI-generated code is
   more taxing than reviewing human-written code. [38]

The follow-on community thread, `discuss.ocaml.org/t/rejecting-ai-generated-code`, ran through July
2026 and produced the sentence that generalises the problem — gasche, 22 July 2026: reviewing such
contributions on their merit is "more work" because "the effort put in them is much lower than the
produced output needing review." The same thread concluded that detection is not a way out:
"reliably distinguishing human-generated content from AI-generated content is impossible." [39]

Why it works as a worked example: nothing here is about the code being bad. Nobody in the thread
claims the DWARF implementation didn't work. The change was rejected because the *review* was
unaffordable — provenance could not be established, the design argument had never been made, and
the cost of understanding 13,000 lines nobody wrote fell entirely on people who had not chosen to
spend it. That is the shape of the reader's problem in miniature: when generation is cheap and
comprehension is not, the review is the whole cost, and it lands on somebody else unless the
author pays it down first.

## Sources

[1] Jason Cohen, "Code Review at Cisco Systems," in *Best Kept Secrets of Peer Code Review*, Smart Bear Software (study wrapped May 2006) — https://static1.smartbear.co/support/media/resources/cc/book/code-review-cisco-case-study.pdf — accessed 19 September 2026
[2] Caitlin Sadowski, Emma Söderberg, Luke Church, Michal Sipko, Alberto Bacchelli, "Modern Code Review: A Case Study at Google," ICSE-SEIP 2018 — https://sback.it/publications/icse2018seip.pdf — accessed 19 September 2026
[3] Google, "Small CLs," *Google Engineering Practices Documentation* — https://google.github.io/eng-practices/review/developer/small-cls.html — accessed 19 September 2026
[4] Google, "What to Look For In a Code Review," *Google Engineering Practices Documentation* — https://google.github.io/eng-practices/review/reviewer/looking-for.html — accessed 19 September 2026
[5] Alberto Bacchelli, Christian Bird, "Expectations, Outcomes, and Challenges of Modern Code Review," ICSE 2013 (Microsoft Research) — https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/ICSE202013-codereview.pdf — accessed 19 September 2026
[6] "Towards Unmasking LGTM Smells in Code Reviews: A Comparative Study of Comment-Free and Commented Reviews," ICSME 2024 — https://conf.researchr.org/details/icsme-2024/icsme-2024-papers/17/ — accessed 19 September 2026
[7] Linda J. Skitka, Kathleen L. Mosier et al., "Accountability and automation bias," *International Journal of Human-Computer Studies* (1999); and "Automation bias and errors: are crews better than individuals?" *International Journal of Aviation Psychology* 10(1) — https://pubmed.ncbi.nlm.nih.gov/11543300/ — accessed 19 September 2026
[8] Kate Goddard, Abdul Roudsari, Jeremy C. Wyatt, "Automation bias: a systematic review of frequency, effect mediators, and mitigators," *JAMIA* 19(1), January 2012 — https://pubmed.ncbi.nlm.nih.gov/21685142/ — accessed 19 September 2026
[9] Emely Rosbach et al., "Stuck on Suggestions: Automation Bias, the Anchoring Effect, and the Factors That Shape Them in Computational Pathology," arXiv:2603.11821, March 2026 — https://arxiv.org/abs/2603.11821 — accessed 19 September 2026
[10] Neil Perry, Megha Srivastava, Deepak Kumar, Dan Boneh, "Do Users Write More Insecure Code with AI Assistants?", ACM CCS 2023 — https://arxiv.org/pdf/2211.03622 — accessed 19 September 2026
[11] Haoran Yu, Lifei Liu, Danping Zhang, "Beyond Lexical Metrics: Sentence-Embedding Detection of Reviewer Habituation in AI Code Review," arXiv:2609.06213, September 2026 — https://arxiv.org/html/2609.06213 — accessed 19 September 2026
[12] Kacper Duma, Patryk Wróblewski, Jagoda Bobińska, Julia Winiarska, Piotr Przymus, "These Aren't the Reviews You're Looking For: How Humans Review AI-Generated Pull Requests," EASE 2026, arXiv:2605.02273, May 2026 — https://arxiv.org/html/2605.02273v1 — accessed 19 September 2026
[13] Haoming Huang et al., "More Code, Less Reuse: Investigating Code Quality and Reviewer Sentiment towards AI-generated Pull Requests," MSR 2026, arXiv:2601.21276, January 2026 — https://arxiv.org/html/2601.21276 — accessed 19 September 2026
[14] Shyam Agarwal, Courtney Miller, Christian Kästner, Bogdan Vasilescu, "3100 Opinions on Code Review in an AI World: Building Causal Theory from Practitioner Discourse," arXiv:2607.07980, July 2026 — https://arxiv.org/abs/2607.07980 — accessed 19 September 2026
[15] GitHub, "Responsible use of GitHub Copilot code review" — https://docs.github.com/en/copilot/responsible-use/code-review — accessed 19 September 2026 — **vendor-reported**
[16] Kowshik Chowdhury, Dipayan Banik, K M Ferdous, Shazibul Islam Shamim, "From Industry Claims to Empirical Reality: An Empirical Study of Code Review Agents in Pull Requests," MSR 2026, arXiv:2604.03196, April 2026 — https://arxiv.org/html/2604.03196v1 — accessed 19 September 2026
[17] "Best AI Code Reviewer in 2026? We Ran 4 in Parallel for 3 Weeks (146 PRs, 679 Findings)," DEV Community, May 2026 (author employed by Sentry; conflict disclosed in the post) — https://dev.to/_vjk/best-ai-code-reviewer-in-2026-we-ran-4-in-parallel-for-3-weeks-146-prs-679-findings-1c0f — accessed 19 September 2026
[18] Niruthiha Selvanayagam, Taher A. Ghaleb, "AI-to-AI Code Reviews of GitHub Pull Requests," arXiv:2608.21311, August 2026 — https://arxiv.org/html/2608.21311v1 — accessed 19 September 2026
[19] QEMU, "Code provenance" (QEMU 11.1.50 docs) — https://www.qemu.org/docs/master/devel/code-provenance.html — accessed 19 September 2026
[20] Gentoo, "Project:Council/AI policy" (Council vote 14 April 2024) — https://wiki.gentoo.org/wiki/Project:Council/AI_policy — accessed 19 September 2026
[21] "Linux distros ban 'tainted' AI-generated code — NetBSD and Gentoo lead the charge," Tom's Hardware — https://www.tomshardware.com/software/linux/linux-distros-ban-tainted-ai-generated-code — accessed 19 September 2026 — *secondary; NetBSD's own commit guidelines not read directly*
[22] Linux kernel, "AI Coding Assistants," `Documentation/process/coding-assistants.rst` — https://docs.kernel.org/process/coding-assistants.html — accessed 19 September 2026
[23] LLVM, "AI Tool Use Policy" — https://llvm.org/docs/AIToolPolicy.html — accessed 19 September 2026
[24] Debian, "General Resolution: LLM usage in Debian," vote 002/2026 (voting 15–28 August 2026) — https://www.debian.org/vote/2026/vote_002 — accessed 19 September 2026
[25] "Assisted-by: How open source projects are drawing the line on AI contributions," All Things Open — https://allthingsopen.org/articles/open-source-ai-contributions-assisted-by-git-trailer-standard — accessed 19 September 2026
[26] Daniel Stenberg, "The end of the curl bug-bounty," 26 January 2026 — https://daniel.haxx.se/blog/2026/01/26/the-end-of-the-curl-bug-bounty/ — accessed 19 September 2026
[27] Daniel Stenberg, "curl security moves again," 25 February 2026 — https://daniel.haxx.se/blog/2026/02/25/curl-security-moves-again/ — accessed 19 September 2026
[28] Daniel Stenberg, "High-Quality Chaos," 22 April 2026 — https://daniel.haxx.se/blog/2026/04/22/high-quality-chaos/ — accessed 19 September 2026
[29] Andrea Griffiths, "Agent pull requests are everywhere. Here's how to review them," The GitHub Blog, 7 May 2026 — https://github.blog/ai-and-ml/generative-ai/agent-pull-requests-are-everywhere-heres-how-to-review-them/ — accessed 19 September 2026 — **vendor-reported**
[30] Faros AI, "AI Engineering Report 2026: The Acceleration Whiplash" (analysis as of March 2026) — https://pages.faros.ai/hubfs/AI_Engineering_Report_2026_The_Acceleration_Whiplash_Faros.pdf — accessed 19 September 2026 — **vendor-reported**
[31] Google Cloud / DORA, "Announcing the 2025 DORA Report" (2025 State of AI-assisted Software Development) — https://cloud.google.com/blog/products/ai-machine-learning/announcing-the-2025-dora-report — accessed 19 September 2026 — **vendor-reported**
[32] METR, "Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity," 10 July 2025 — https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/ — accessed 19 September 2026
[33] METR, "We are Changing our Developer Productivity Experiment Design," 24 February 2026 — https://metr.org/blog/2026-02-24-uplift-update/ — accessed 19 September 2026
[34] Victor R. Basili et al., "The Empirical Investigation of Perspective-Based Reading," University of Maryland; and the replicated PBR-vs-CBR experiments summarised in *Empirical Software Engineering* — https://www.cs.umd.edu/~mvz/handouts/emp_pbr.pdf — accessed 19 September 2026
[35] SmartBear, "Best Practices for Code Review" — https://smartbear.com/learn/code-review/best-practices-for-peer-code-review/ — accessed 19 September 2026 — **vendor-reported**
[36] Addy Osmani, "Code Review in the Age of AI," 5 January 2026 — https://addyo.substack.com/p/code-review-in-the-age-of-ai — accessed 19 September 2026
[37] Veracode, "2025 GenAI Code Security Report" (October 2025 update) — https://www.veracode.com/resources/analyst-reports/2025-genai-code-security-report/ — accessed 19 September 2026 — **vendor-reported**
[38] "OCaml maintainers reject massive AI-generated pull request," DevClass, 27 November 2025, reporting on `ocaml/ocaml` PR #14369 — https://devclass.com/2025/11/27/ocaml-maintainers-reject-massive-ai-generated-pull-request/ — accessed 19 September 2026
[39] OCaml Discuss, "Rejecting AI-generated code" (thread, July 2026) — https://discuss.ocaml.org/t/rejecting-ai-generated-code/18360 — accessed 19 September 2026
