# Agent context and tooling landscape

**Question asked:** what is actually standardised in agent context files, Skills, MCP, token
filtering, and harness-level safety controls — as against what is one vendor's habit — and what
should the Context and Harness play suites be able to claim without dating themselves badly?

**Researched:** 18 September 2026
**Confidence:** high on mechanics (primary vendor and spec documentation throughout); medium on
adoption counts and incident histories (SEO-farm secondary sources dominate); low on anything
projected forward past about twelve months.

This is the hub brief. Each subject has its own file so a writer chasing one thing does not have to
read the other four:

| Brief | Feeds | Covers |
|---|---|---|
| [`agent-context-files.md`](agent-context-files.md) | Context suite | `CLAUDE.md`, `AGENTS.md`, `.claude/rules/`, the cards pattern |
| [`skills.md`](skills.md) | Harness suite | `SKILL.md`, progressive disclosure, skill vs. prompt vs. tool |
| [`mcp.md`](mcp.md) | Harness suite | What a server exposes, the 2026-07-28 spec, trust boundaries |
| [`token-filtering.md`](token-filtering.md) | Context suite | `rtk`, context editing, compaction, measuring savings honestly |
| [`permissions-and-sandboxing.md`](permissions-and-sandboxing.md) | Harness suite | Permission rules, OS-level sandboxing, what is enforced |

---

## The one finding that shapes everything else

There are now three genuinely multi-vendor artefacts in this space — `AGENTS.md`, `SKILL.md`, and
MCP — and all three were donated to the same body on the same day. The Linux Foundation announced
the **Agentic AI Foundation (AAIF) on 9 December 2025**, anchored by Anthropic's contribution of
MCP, Block's contribution of goose, and OpenAI's contribution of `AGENTS.md`. [1][2] Anthropic
published Agent Skills as an open standard nine days later, on 18 December 2025. [3][4]

So the honest framing for the book is not "vendor lock-in versus open standards." It is that the
*file formats* converged and were handed to a neutral body within a single month, while the
*behaviour around those files* — precedence, loading order, extended frontmatter, permission syntax,
sandboxing — remains entirely per-harness and entirely undocumented across vendors. A team that
standardises on the formats is portable. A team that standardises on the behaviour is not, and will
not find out until it switches tools.

## What is standardised vs. one vendor's habit

| Thing | Status | Notes |
|---|---|---|
| `AGENTS.md` as a filename and markdown format | **Standard.** AAIF-stewarded, 25+ tools listed as supporting it, "over 60k open-source projects" per agents.md | [5] |
| Required sections inside `AGENTS.md` | **Not specified at all.** "AGENTS.md is just standard Markdown. Use any headings you like" | [5] |
| Nearest-file-wins for nested `AGENTS.md` | **Standard, loosely.** agents.md states "The closest AGENTS.md to the edited file wins" | [5] |
| `CLAUDE.md` | **One vendor.** Anthropic-only filename, with its own four-scope precedence chain | [6] |
| Which file wins when both exist | **Vendor habit.** Claude Code prefers `CLAUDE.md` and offers three other modes via a setting | [6] |
| `SKILL.md` folder format, `name` + `description` frontmatter | **Standard.** agentskills.io spec, ~45 client products listed | [3][7] |
| Skill frontmatter beyond `name`/`description` (`allowed-tools`, `model`, invocation controls) | **Vendor extension.** Claude Code's own validator issue reports the standard validator rejecting these fields | [8] |
| MCP wire protocol, tools/resources/prompts, OAuth 2.1 authorization | **Standard.** Versioned by date, 2026-07-28 current, 12-month minimum deprecation window | [9][10] |
| Which MCP servers are safe to install | **Nobody's standard.** Entirely on the operator | [11] |
| Permission rule syntax (`Bash(git push *)`, allow/ask/deny) | **One vendor.** No cross-tool equivalent | [12] |
| OS-level sandboxing (Seatbelt, bubblewrap) | **One vendor's implementation of a general idea.** Every harness rolls its own | [13] |
| Token-filtering proxies like `rtk` | **Third-party, unstandardised, and unvalidated.** See the brief | [14][15][16] |

## Cross-cutting gotchas worth a named failure mode

Three patterns recur across all five subjects, and each is a candidate for the failure-mode registry
in `plans/agentic-playbook.md`:

1. **Instructions are context, not configuration.** Claude Code's own docs say it plainly: CLAUDE.md
   is "delivered as a user message after the system prompt," and to block an action "regardless of
   what Claude decides, use a PreToolUse hook instead." [6] The same distinction appears in
   permissions (a `deny` rule "isn't a security boundary around the program" [12]) and in skills (a
   `description` is a hint that a skill *might* be relevant, not a router). Teams routinely write a
   rule in prose and believe they have built an enforcement layer.

2. **The tool's own scoreboard is not the bill.** `rtk` reported 96.2 million tokens saved — 99.8%
   of everything it touched — over the same trials in which the measured spend went *up* 7.6%. [14]
   This is the sharpest single anecdote in the whole research pass, and it generalises: any tool
   that measures its own benefit against a counterfactual the billing system never applies will
   flatter itself indefinitely.

3. **A silent precedence rule beats a loud config file.** Adding a `CLAUDE.local.md` for private
   notes silently stops Claude Code reading your `AGENTS.md`, and the loaded `AGENTS.md` never
   appears in `/memory` or `/context`. [6] Nothing errors. The instructions simply stop arriving.

## Contradictions and gaps

- **Secondary sources are confidently wrong about AGENTS.md support in Claude Code.** Multiple
  mid-2026 posts — including one gist explicitly framed as a correction — state that Claude Code
  does not read `AGENTS.md` and that "the 'reads it as a fallback' claim is wrong." [17] The primary
  documentation says the opposite: native reading landed in v2.1.277, with a four-valued
  `instructionFiles` setting. [6] The secondary sources are stale rather than lying, but the book
  should cite vendor docs here and nothing else.
- **Adoption counts are unreliable.** Server totals for MCP range from ~2,000 to 10,000+ depending
  on registry and counting method; the official registry API reportedly returned 9,652 latest server
  records on 24 May 2026. [18] Every enterprise-adoption percentage found traced back to
  vendor-adjacent blogs. Treat all of these as shape, not figure.
- ~~**NSA/CISA published MCP security guidance dated June 2026**… worth a manual download.~~
  **Done, 19 September 2026 (`57772ad900e3`).** It is **NSA alone, not NSA/CISA**, and dated
  **May 2026 Ver. 1.0**, titled *Model Context Protocol (MCP): Security Design Considerations for
  AI-Driven Automation*. It is as good a Harness-suite citation as hoped: it argues for explicit
  trust boundaries between agent, plugin, model and user, and for OS-level sandboxing of every tool
  execution, from outside the industry. **The quotable extracts are in [`mcp.md`](mcp.md)** and are
  not duplicated here. [19a] Both mirrors still 403 to `curl` and `WebFetch` at any header
  combination; it opens normally in a browser.
- **No independent measurement exists of whether context-file discipline improves outcomes.** Every
  claim about CLAUDE.md length, cards, or progressive disclosure is vendor guidance or practitioner
  assertion. The book can describe mechanisms confidently and must hedge on effect sizes.

## Flagged as likely stale within twelve months

Rank-ordered by how fast it will rot.

| Claim | Why it rots | Hedge |
|---|---|---|
| Any Claude Code `v2.1.x` behaviour | Point releases changed permission and memory semantics repeatedly through 2026 | Name the version in the sentence, or describe the mechanism and not the flag |
| `rtk` v0.49.0 numbers, and the benchmark dispute | Actively contested; issue #3157 was still open and unanswered on 22 July 2026 [16] | Use it as a *method* lesson (measure the bill) rather than a verdict on one binary |
| MCP spec details | Date-versioned; legacy versions sunset on a 12-month clock from 28 July 2026 [9] | Cite the spec date every time; prefer the trust-boundary argument, which is durable |
| Adoption counts (60k repos, 10k servers, ~45 skill clients) | Growing monthly | Round hard and date the sentence, or cut |
| "Claude Code is the holdout on AGENTS.md" | Already false | Do not repeat it under any circumstance |
| Model names, context limits, prices | Obvious | `book/STYLE.md` already governs this |

Durable for the life of the book: the instructions-are-not-enforcement distinction, progressive
disclosure as a design pattern, the confused-deputy and tool-poisoning attack shapes, and the
observation that a filtering tool's self-reported savings are a marketing metric.

## Related reading the commissioner supplied

Two posts by the repo owner inform the Context suite's framing and are worth citing as practitioner
sources rather than evidence:

- **Cards** [20] — a two-tier context pattern: a ~15-line `CLAUDE.md` holding an index with
  natural-language triggers, plus self-contained `cards/` files loaded on demand. "The only real
  rule is self-containment. One card, one load, no chains." This repo uses the pattern, which makes
  it a viable answer to the open appendix-templates question in `plans/agentic-playbook.md`.
- **The unit of work** [21] — argues codebases should be organised feature-first because an agent's
  unit of work is a capability, not a layer: "For us, reading and writing code was the expensive
  part... For an agent writing is cheap, and the expensive thing is behavior it can't see." Sits
  next to *Scope a task to fit the window* in the Context suite.

## Sources

[1] Linux Foundation Announces the Formation of the Agentic AI Foundation (AAIF) —
    https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation
    — accessed 18 September 2026
[2] MCP joins the Agentic AI Foundation — https://blog.modelcontextprotocol.io/posts/2025-12-09-mcp-joins-agentic-ai-foundation/
    — accessed 18 September 2026
[3] Agent Skills Overview (agentskills.io) — https://agentskills.io/home — accessed 18 September 2026
[4] Anthropic makes agent Skills an open standard, SiliconANGLE, 18 December 2025 —
    https://siliconangle.com/2025/12/18/anthropic-makes-agent-skills-open-standard/ — accessed 18 September 2026
[5] AGENTS.md — https://agents.md/ — accessed 18 September 2026
[6] How Claude remembers your project, Claude Code docs — https://code.claude.com/docs/en/memory
    — accessed 18 September 2026
[7] Agent Skills, Claude Platform docs —
    https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview — accessed 18 September 2026
[8] anthropics/claude-code issue #25380, "SKILL.md validator only recognizes Agent Skills standard
    fields, rejects Claude Code extended frontmatter" — https://github.com/anthropics/claude-code/issues/25380
    — accessed 18 September 2026
[9] The 2026-07-28 Specification, MCP blog — https://blog.modelcontextprotocol.io/posts/2026-07-28/
    — accessed 18 September 2026
[10] MCP Security Best Practices — https://modelcontextprotocol.io/specification/2026-07-28/basic/security_best_practices
     — accessed 18 September 2026
[11] MCP Security: Risks, Real Incidents & Controls (2026), Checkmarx —
     https://checkmarx.com/learn/mcp-security-risks-real-world-incidents-and-security-controls/ — accessed 18 September 2026
[12] Configure permissions, Claude Code docs — https://code.claude.com/docs/en/permissions — accessed 18 September 2026
[13] Configure the sandboxed Bash tool, Claude Code docs — https://code.claude.com/docs/en/sandboxing
     — accessed 18 September 2026
[14] rtk Claude Code Token Savings: A Skill Trial Benchmark, JetBrains AI blog, July 2026 —
     https://blog.jetbrains.com/ai/2026/07/rtk-claude-code-token-savings/ — accessed 18 September 2026
[15] RTK reports huge token savings, but our cost benchmarks disagree, Quesma —
     https://quesma.com/blog/does-rtk-make-ai-coding-cheaper/ — accessed 18 September 2026
[16] rtk-ai/rtk issue #3157 — https://github.com/rtk-ai/rtk/issues/3157 — accessed 18 September 2026
[17] "Does Claude Code read AGENTS.md? No — it reads CLAUDE.md" (gist, mid-2026) —
     https://gist.github.com/yurukusa/d36197848911f025add142abefcde685 — accessed 18 September 2026 —
     **cited as an example of a stale claim, not as evidence**
[18] MCP Ecosystem H1 2026 Retrospective: Adoption Data Points —
     https://www.digitalapplied.com/blog/mcp-ecosystem-h1-2026-retrospective-adoption-data-points — accessed 18 September 2026
[19] ~~Model Context Protocol (MCP) Security, NSA CSI, June 2026~~ — **superseded by [19a]**
[19a] *Model Context Protocol (MCP): Security Design Considerations for AI-Driven Automation*, National Security Agency, **May 2026 Ver. 1.0** —
     https://media.defense.gov/2026/Jun/02/2003943289/-1/-1/0/CSI_MCP_SECURITY.PDF — **retrieved in a browser and read 19 September 2026 by `57772ad900e3`**; extracts in [`mcp.md`](mcp.md) [8a]
[20] Cards — https://memention.com/blog/2026/05/25/Cards.html — accessed 18 September 2026
[21] The Unit of Work — https://memention.com/blog/2026/05/29/The-unit-of-work.html — accessed 18 September 2026
