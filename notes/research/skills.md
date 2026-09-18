# Skills — packaging repeatable expertise

**Question asked:** what a Skill is, how it differs from a prompt and from a tool, when it earns its
keep, and how much of the format is genuinely standard.

**Researched:** 18 September 2026
**Confidence:** high on format, mechanics, and token costs (primary spec and vendor docs); medium on
the extent of cross-vendor frontmatter compatibility; low on catalogue sizes.

Feeds the **Harness** suite, chiefly *Package repeatable expertise*, and the Team suite's
shared-skill-library play.

## Findings

### What a Skill is

A skill is **a folder containing a `SKILL.md` file** — metadata plus instructions — that may bundle
scripts, references, and assets. [1] The canonical layout:

```
my-skill/
├── SKILL.md          # Required: metadata + instructions
├── scripts/          # Optional: executable code
├── references/       # Optional: documentation
├── assets/           # Optional: templates, resources
└── ...
```

Required frontmatter is `name` and `description` only. Field constraints from the platform docs: [2]

- `name`: maximum 64 characters, lowercase letters, numbers and hyphens only, no XML tags, and
  **cannot contain the reserved words "anthropic" or "claude"**.
- `description`: non-empty, maximum 1024 characters, no XML tags. It "must include both what the
  Skill does and when Claude should use it," because it is what the request is matched against.

### Progressive disclosure, with the token costs

This is the entire design, and the numbers are published: [2]

| Level | When loaded | Token cost | Content |
|---|---|---|---|
| 1: Metadata | Always, at startup | **~100 tokens per Skill** | `name` and `description` from frontmatter |
| 2: Instructions | When the Skill is triggered | **Under 5k tokens** | The `SKILL.md` body |
| 3+: Resources | As needed | **None until accessed** | Bundled files; scripts run via bash, only output enters context |

The spec states the same three stages in vendor-neutral terms: **discovery** (name and description
only), **activation** (full `SKILL.md` read in), **execution** (bundled code or referenced files
loaded as needed). [1]

Two consequences the docs draw out explicitly, both of which are good play material: [2]

- **"There's no context penalty for bundled content that isn't used."** A skill can ship a full API
  reference and a large dataset and cost 100 tokens until the day it is needed.
- **A script's code never enters context.** "When Claude runs `validate_form.py`, the script's code
  never loads into the context window. Only its output... consumes tokens, which makes scripts far
  more efficient than having Claude generate equivalent code on the fly."

### How a Skill differs from a prompt and from a tool

The distinction the book needs, drawn from the primary docs rather than invented:

- **vs. a prompt.** "Unlike prompts (conversation-level instructions for one-off tasks), Skills load
  on demand, so you don't have to repeat the same guidance across conversations." [2] A prompt is a
  thing you say; a skill is a thing that is *there*, costing ~100 tokens, waiting for its situation.
- **vs. a context file.** Claude Code's memory docs draw the line at shape and scope: "If an entry
  is a multi-step procedure or only matters for one part of the codebase, move it to a skill or a
  path-scoped rule instead" of `CLAUDE.md`. [3] Rules "load into context every session or when
  matching files are opened. For task-specific instructions that don't need to be in context all the
  time, use skills instead." [3]
- **vs. a tool / MCP server.** The cleanest formulation found is secondary but sharp: MCP is the
  plumbing — how an agent connects to a database or an API — while Agent Skills are the manual,
  teaching the agent how to navigate those connections to achieve a goal. [4] A tool adds a
  *capability*; a skill adds *competence with a capability you already had*. A skill whose whole
  content is "call this HTTP endpoint" should probably have been a tool; a tool whose description
  runs to four paragraphs of procedure should probably have been a skill.
- **vs. a subagent.** Orthogonal, and a thing the Orchestration suite owns — though note Claude Code
  lets a skill declare `execution: context: fork + agent` to run as a subagent, which blurs the line
  in exactly one vendor. [5]

### Standard vs. vendor habit

- The format was **originally developed by Anthropic, released as an open standard** on **18
  December 2025**, and is open to outside contribution, with governance discussion on GitHub and
  Discord. [1][6] It was subsequently associated with the Agentic AI Foundation. [6]
- The client showcase on agentskills.io lists roughly 45 products, including Claude Code, ChatGPT &
  Codex, GitHub Copilot, VS Code, Cursor, Gemini CLI, Amp, Goose, OpenCode, OpenHands, Factory, Roo
  Code, Kiro, JetBrains Junie, Laravel Boost, Spring AI, and Databricks. [1]
- **The frontmatter beyond `name` and `description` is where portability stops.** Claude Code
  supports extended fields — `when_to_use`, `allowed-tools` (pre-approved tools while the skill is
  active), `model`, `argument-hint`, `disable-model-invocation`, `user-invocable`, and the
  `execution` block — and an open issue reports the standard `SKILL.md` validator rejecting them as
  non-standard. [5][7] A skill written against the standard is portable; a skill written against
  Claude Code's frontmatter is not.
- **Skills do not sync across surfaces, even within one vendor.** Claude Code skills are
  filesystem-based (`~/.claude/skills/` personal, `.claude/skills/` project); claude.ai skills are
  per-user zip uploads with no org-wide admin management; API skills are workspace-wide uploads.
  "Skills uploaded to one surface are not automatically available on others." [2]
- Runtime environments differ enough to break a skill on transfer: on the Claude API, skills run in
  a sandboxed container with **no network access and no runtime package installation**; in Claude
  Code they have **full network access, the same as any other program on the user's computer**. [2]

## When it earns its keep

When a procedure is long enough that it would bloat the always-loaded brief, specific enough that it
only applies sometimes, and repeated often enough that re-explaining it is a tax. The
progressive-disclosure arithmetic is the argument: a library of thirty skills costs roughly 3,000
tokens of permanent context and delivers an arbitrarily large body of procedure on demand. The same
thirty procedures pasted into `CLAUDE.md` would be tens of thousands of always-loaded tokens, most
of them irrelevant to any given session, which is precisely the *Context Landfill* failure mode
already registered in `plans/agentic-playbook.md`.

The second case is determinism. Anything you would rather the agent *ran* than *reasoned about* —
validation, formatting, a migration check — belongs in a bundled script, because script code costs
nothing in context and produces the same answer every time.

## Sharpest real-world gotcha

**The `description` is the whole routing table, and it is the field people write last.** A skill is
discovered only by its name and description; the body is not consulted when deciding whether the
skill is relevant. [1][2] The docs are explicit that the description "must say both what the Skill
does and when to use it." A skill described as "PDF utilities" will sit unloaded next to a request
about extracting a table from a form, and the failure is silent — no error, no missed-match warning,
just an agent that did the thing the long way. Every skill that "doesn't work" should have its
description checked before its body.

Runner-up, and the one that matters for a team library: **skills are executable code you are
installing.** The docs put it plainly — "Treat like installing software" — and warn that a malicious
skill "can direct Claude to invoke tools or execute code in ways that don't match the Skill's stated
purpose," with skills that fetch external URLs called out as particularly risky because "fetched
content may contain malicious instructions." [2] Community catalogues are enormous; one directory
reportedly indexes around 1.9 million public skills scraped from GitHub. [8] That number is
unverified and probably wrong in detail, but the shape of the risk is not.

## Concrete example we can lift

A minimal, standard-compliant skill that demonstrates all three disclosure levels in about fifteen
lines. The `description` is the part to draw the reader's eye to:

```markdown
---
name: release-notes
description: Draft release notes from the commit range since the last tag. Use when the user
  asks for release notes, a changelog entry, or "what shipped since <version>".
---

# Release notes

1. Run `scripts/commit_range.sh` to get the commits since the last tag. Its output is the
   only thing that enters context; the script itself never does.
2. Group commits by the conventional-commit prefix.
3. Format against `references/house-style.md`. Read that file only if the user asks for
   the customer-facing variant.
```

Saved as `.claude/skills/release-notes/SKILL.md`, this costs ~100 tokens at startup. The body loads
only when the description matches. `references/house-style.md` costs nothing unless step 3 needs it,
and `scripts/commit_range.sh` contributes only its output. [2]

The contrast that makes the play land: the same procedure in `CLAUDE.md` costs its full length in
every session, including the several hundred sessions that have nothing to do with releases.

## Contradictions and gaps

- **Catalogue and client counts are unreliable.** "~40 skills-compatible products" (June 2026) and
  "~1.9 million public skills" both come from secondary aggregators. [8] The agentskills.io showcase
  is countable and primary but is a curated list, not a census. [1]
- **The extended-frontmatter incompatibility is documented only by an issue title.** [7] Before the
  book asserts that Claude Code's fields are rejected by the standard validator, someone should read
  the issue thread and the published specification's field list directly.
- **No independent evidence that skills improve outcomes.** The token arithmetic is published and
  checkable; the claim that on-demand loading produces better results than always-loaded instruction
  is a plausible mechanism with no study behind it. Hedge accordingly.
- **Skill discovery reliability is unmeasured.** Nothing found quantifies how often a well-described
  skill fails to trigger. This matters, because the whole pattern rests on that match working.

## Sources

[1] Agent Skills Overview (agentskills.io) — https://agentskills.io/home — accessed 18 September 2026
[2] Agent Skills, Claude Platform docs —
    https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview — accessed 18 September 2026
[3] How Claude remembers your project, Claude Code docs — https://code.claude.com/docs/en/memory
    — accessed 18 September 2026
[4] Anthropic Launches "Agent Skills" Open Standard, FinancialContent, 24 December 2025 —
    https://www.financialcontent.com/article/tokenring-2025-12-24-anthropic-launches-agent-skills-open-standard-the-new-universal-language-for-ai-interoperability
    — accessed 18 September 2026
[5] The SKILL.md Frontmatter Reference, Introduction to Agent Skills —
    https://www.anthropiccertifications.com/courses/introduction-to-agent-skills/skill-frontmatter-reference
    — accessed 18 September 2026
[6] Anthropic makes agent Skills an open standard, SiliconANGLE, 18 December 2025 —
    https://siliconangle.com/2025/12/18/anthropic-makes-agent-skills-open-standard/ — accessed 18 September 2026
[7] anthropics/claude-code issue #25380 — https://github.com/anthropics/claude-code/issues/25380
    — accessed 18 September 2026
[8] The Agent Skills Ecosystem in 2026, Agentman —
    https://agentman.ai/blog/agent-skills-ecosystem-report-2026 — accessed 18 September 2026
