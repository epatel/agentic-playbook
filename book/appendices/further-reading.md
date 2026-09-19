# Further reading

This book stands on twenty-one research briefs in [`notes/research/`](../../notes/research/), each
one a set of findings with numbered sources, a list of what the pass could *not* establish, a
do-not-cite list, and an assessment of how fast its material is rotting. The briefs are where a
disputed sentence in this book should be checked first; what follows is the shortest path into them,
plus the primary documents worth reading directly.

Everything here was accessed in September 2026. A fair number of these links will have moved by the
time you follow them, which is the subject rather than an apology.

## Context files, skills, and connected tools

Start at [`tooling.md`](../../notes/research/tooling.md), the hub for this pass, which carries a
table separating what is standardised from what is one vendor's habit. Beneath it:
[`agent-context-files.md`](../../notes/research/agent-context-files.md),
[`skills.md`](../../notes/research/skills.md), [`mcp.md`](../../notes/research/mcp.md),
[`permissions-and-sandboxing.md`](../../notes/research/permissions-and-sandboxing.md), and
[`token-filtering.md`](../../notes/research/token-filtering.md).

- **AGENTS.md** — https://agents.md/ — the multi-vendor context-file convention, stewarded by the
  Linux Foundation's Agentic AI Foundation since December 2025.
- **How Claude remembers your project**, Claude Code documentation —
  https://code.claude.com/docs/en/memory — the precedence rules, including the local-file trap that
  silently stops a shared `AGENTS.md` loading.
- **Agent Skills overview**, Claude Platform documentation —
  https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview — what the two standard
  frontmatter fields are, and what is one vendor's extension.
- **Model Context Protocol, the 2026-07-28 specification** —
  https://blog.modelcontextprotocol.io/posts/2026-07-28/ — and its **Security Best Practices**
  document, https://modelcontextprotocol.io/specification/2026-07-28/basic/security_best_practices,
  which is normative and unusually direct about trust boundaries.
- **The `rtk` pair** — JetBrains' benchmark,
  https://blog.jetbrains.com/ai/2026/07/rtk-claude-code-token-savings/, read next to Quesma's cost
  comparison, https://quesma.com/blog/does-rtk-make-ai-coding-cheaper/. Two competent measurements
  of the same tool reaching opposite conclusions, which is the most instructive thing in the pass.

## Orchestration

Start at [`orchestration.md`](../../notes/research/orchestration.md). Beneath it:
[`subagents.md`](../../notes/research/subagents.md),
[`control-flow.md`](../../notes/research/control-flow.md),
[`langchain-langgraph.md`](../../notes/research/langchain-langgraph.md),
[`visual-workflow-tools.md`](../../notes/research/visual-workflow-tools.md),
[`parallel-agents-and-collisions.md`](../../notes/research/parallel-agents-and-collisions.md), and
[`single-agent-wins.md`](../../notes/research/single-agent-wins.md).

- **Building effective agents**, Anthropic, December 2024 —
  https://www.anthropic.com/engineering/building-effective-agents — still the best short statement
  of the case for less machinery, from a vendor with every incentive to argue the other way.
- **How we built our multi-agent research system**, Anthropic, June 2025 —
  https://www.anthropic.com/engineering/multi-agent-research-system — the case for more, by the same
  people. Read them together; the tension is real and is not resolved.
- **Don't build multi-agents**, Cognition, June 2025 —
  https://cognition.com/blog/dont-build-multi-agents — and its successor, **Multi-agents: what's
  actually working**, April 2026, https://cognition.com/blog/multi-agents-working, in which the same
  author revises the position without abandoning it.
- **A practical guide to building agents**, OpenAI —
  https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf
- **Do more agents help? Controlled and protocol-aligned evaluation of LLM agent workflows**, arXiv
  2606.05670 — https://arxiv.org/abs/2606.05670 — the protocol-matched comparison in which five of
  six multi-agent systems lost to a single-agent baseline.

## Evidence, failure modes, and economics

Start at [`evidence.md`](../../notes/research/evidence.md), which consolidates the contested claims
and the do-not-cite list across six subjects. Beneath it:
[`productivity-evidence.md`](../../notes/research/productivity-evidence.md),
[`failure-modes.md`](../../notes/research/failure-modes.md),
[`review-practice.md`](../../notes/research/review-practice.md),
[`verification.md`](../../notes/research/verification.md),
[`accountability.md`](../../notes/research/accountability.md), and
[`token-economics.md`](../../notes/research/token-economics.md).

- **Measuring the impact of early-2025 AI on experienced open-source developer productivity**, METR,
  arXiv 2507.09089 — https://arxiv.org/abs/2507.09089 — the famous slowdown result. Read the
  February 2026 follow-up at https://metr.org/ in the same sitting, or do not cite the first.
- **The impact of AI on developer productivity: evidence from GitHub Copilot**, arXiv 2302.06590 —
  https://arxiv.org/abs/2302.06590 — and the enterprise randomised trial at
  https://arxiv.org/abs/2410.12944. Both measure autocomplete, which is the distinction most of the
  discourse drops.
- **These aren't the reviews you're looking for: how humans review AI-generated pull requests**,
  EASE 2026, arXiv 2605.02273 — https://arxiv.org/html/2605.02273v1
- **Beyond lexical metrics: sentence-embedding detection of reviewer habituation in AI code
  review**, arXiv 2609.06213 — https://arxiv.org/html/2609.06213 — the measurement behind the
  Drifting Yes.
- **DORA's annual reports** — https://dora.dev/ — the source of the *verification tax*, and the
  largest recurring survey in the field. Self-report, and says so.

## The history behind Part I

[`convergence-history.md`](../../notes/research/convergence-history.md) sources the pre-Git,
pre-Scrum analogy. It is the least perishable brief in the project.

- **Walter F. Tichy, "RCS — a system for version control"**, 1985 —
  https://www.gnu.org/software/rcs/tichy-paper.pdf — locking as the default assumption, stated
  without embarrassment because there was not yet an alternative.
- **"Oh yeah, there's pull requests now"**, GitHub, February 2008 —
  https://github.blog/2008-02-23-oh-yeah-there-s-pull-requests-now/ — and **"Pull requests 2.0"**,
  August 2010, https://github.blog/2010-08-31-pull-requests-2-0/. Two and a half years between the
  tool and the discipline.
- **Gousios, Pinzger and van Deursen, "An exploratory study of the pull-based software development
  model"**, ICSE 2014 — https://pure.tudelft.nl/ws/files/7416754/TUD_SERG_2014_005.pdf
- **Jim Highsmith, "History: the Agile Manifesto"** — https://agilemanifesto.org/history.html — and
  **Martin Fowler, "Semantic diffusion"**,
  https://martinfowler.com/bliki/SemanticDiffusion.html, on what happens to a word once it wins.

## The two posts this book is developed from

Its arguments about two-tier context and about organising a codebase around capabilities were made
first, and shorter, here.

- **Cards** — https://memention.com/blog/2026/05/25/Cards.html
- **The unit of work** — https://memention.com/blog/2026/05/29/The-unit-of-work.html

## What does not survive being looked up

The most useful artefact in the research is the part that lists what had to be thrown away. Roughly
forty widely-circulated figures across the six subjects trace only to vendor marketing, to a
mislabelled survey year, to a laundered secondary write-up, or to a search engine's synthesis of
blogs. Several are the first result a search returns. The consolidated list is in
[`evidence.md`](../../notes/research/evidence.md), with per-subject lists in each brief; the five
worth knowing before you next quote something in a meeting:

- **Every published SWE-bench per-instance dollar figure.** The leaderboard carries no cost column.
- **The "200–400 lines in under 60 minutes" code-review rule.** It appears nowhere in the study it
  is attributed to, whose design could not have measured it.
- **Any "Stack Overflow Developer Survey 2026" figure.** That survey had not reported; the numbers
  in circulation are 2025 data under a 2026 headline.
- **The Standish CHAOS figures** — the 1994 success split and the 189% average cost overrun, the
  most quoted numbers in the history of software process. Two peer-reviewed demolitions exist, and
  are worth reading as a case study in how this happens: Eveleens and Verhoef,
  https://www.cs.vu.nl/~x/the_rise_and_fall_of_the_chaos_report_figures.pdf, and Jørgensen and
  Moløkken, https://cms.simula.no/sites/default/files/publications/Jorgensen.2006.4.pdf.
- **Both of the low-code statistics** used to argue that citizen development failed: the 43%
  scaled-back figure attributed to Gartner, and the 25–30% no-code rewrite rate. Neither has a
  primary source.
