# Agent context files — `CLAUDE.md`, `AGENTS.md`, rules, cards

**Question asked:** what each file actually is, who supports which, how much is genuine convention
versus one vendor's habit, and where the `AGENTS.md` standardisation effort currently stands.

**Researched:** 18 September 2026
**Confidence:** high on mechanics and precedence (primary vendor docs); medium on adoption counts;
low on anything about relative effectiveness, for which no independent evidence was found.

Feeds the **Context** suite, chiefly *Write the brief the agent actually reads* and *Starve the
context*.

## Findings

### What each file is

- **`AGENTS.md`** is a plain markdown file of project instructions for AI coding agents, with **no
  required sections and no schema**. The spec is explicit: "AGENTS.md is just standard Markdown. Use
  any headings you like; the agent simply parses the text you provide." [1] Suggested topics are
  project overview, build/test commands, code style, testing, and security — recommendations only.
- **`CLAUDE.md`** is Anthropic's equivalent filename, with a documented four-scope precedence chain
  and a set of behaviours (`@path` imports, HTML-comment stripping, `/init`, `/memory`) that the
  `AGENTS.md` spec says nothing about. [2]
- **`.claude/rules/`** is a Claude Code directory of topic-scoped markdown files. Rules with a
  `paths:` YAML frontmatter glob load **only when Claude reads a matching file**; rules without one
  load unconditionally at launch, at the same priority as `.claude/CLAUDE.md`. [2]
- **Auto memory** is a separate, machine-local mechanism where the agent writes its own notes to
  `~/.claude/projects/<project>/memory/`. Only the first 200 lines or 25 KB of its `MEMORY.md` index
  loads each session. [2]

### Where standardisation stands

- `AGENTS.md` is **stewarded by the Agentic AI Foundation under the Linux Foundation** — not by a
  vendor. [1] The AAIF was announced on **9 December 2025**, anchored by MCP from Anthropic, goose
  from Block, and `AGENTS.md` from OpenAI. [3][4]
- agents.md claims the file is "used by over 60k open-source projects" and lists 25+ supporting
  tools, noting the list is not exhaustive. [1] No date is attached to that count on the page.
- The only cross-tool *behavioural* rule in the spec is nearest-file-wins: "The closest AGENTS.md to
  the edited file wins; explicit user chat prompts override everything." [1]

### What Claude Code actually does with `AGENTS.md`

This is the section most secondary sources get wrong. From the primary documentation: [2]

- Claude Code reads `AGENTS.md` **natively**, requiring **v2.1.277 or later**.
- Default mode is `claude-md-or-agents-md`: if any `CLAUDE.md`, `.claude/CLAUDE.md`, or
  `CLAUDE.local.md` exists in the working directory or above it, Claude reads that and **ignores
  every `AGENTS.md`**. With none of those, it reads every `AGENTS.md` and `.claude/AGENTS.md` up the
  tree and prints a line such as `no CLAUDE.md found; AGENTS.md loaded: /home/you/repo/AGENTS.md`.
- Four settable values: `claude-md-or-agents-md` (default), `claude-md-and-agents-md`, `claude-md`,
  `managed-only`. Set via `/config` or in `pluginConfigs` under `agents-md@builtin`; the setting is
  **ignored in project and local settings files**.
- Support is unavailable in several real situations: versions before v2.1.277, sessions that cannot
  fetch feature flags (Amazon Bedrock, other third-party providers, telemetry disabled), the first
  session after an upgrade, and sessions with `disableAllHooks` or `allowManagedHooksOnly` set.
- The cross-tool workaround still works and is still recommended for those sessions: put
  `@AGENTS.md` at the top of a `CLAUDE.md`, or `ln -s AGENTS.md CLAUDE.md`.

### Size and loading mechanics worth quoting

- **"target under 200 lines per CLAUDE.md file. Longer files consume more context and reduce
  adherence."** [2]
- Claude Code loads a CLAUDE.md of **up to 4 MiB in full and skips a larger file**. [2]
- `@path` imports are expanded **at launch**, recurse to a **maximum depth of four hops**, and —
  critically — "Splitting into `@path` imports helps organization but doesn't reduce context, since
  imported files load at launch." [2] Path-scoped rules are the mechanism that actually reduces
  context; imports are not.
- All discovered `CLAUDE.md` files up the tree are **concatenated, not overridden**, ordered from
  filesystem root down, with `CLAUDE.local.md` appended after `CLAUDE.md` at each level. [2]
- `claudeMdExcludes` (glob patterns against absolute paths, merged across settings layers) exists
  specifically because monorepos pick up other teams' files. [2]
- Block-level HTML comments are stripped before injection — free maintainer notes that cost no
  tokens. [2]
- Project-root CLAUDE.md **survives `/compact`**: it is re-read from disk and re-injected. Nested
  files and path-scoped rules reload only when a matching file is next read. [2]

### The cards pattern

A practitioner pattern, in use in this repo: a lean `CLAUDE.md` (~15 lines) holding a project
overview and an index of triggers, plus self-contained `cards/` files loaded on demand. Index
entries are natural-language triggers — *"[auth](cards/auth.md) — when touching login, sessions, or
permissions"*. The stated rule is **"The only real rule is self-containment. One card, one load, no
chains."** Cards never link to cards; shared context is hoisted into a third card. [5]

Note the relationship worth drawing out in the prose: cards are the manual, model-driven version of
what `.claude/rules/` with `paths:` frontmatter does mechanically, and what Skills do with
`description` matching. Three vendors, three mechanisms, one idea — load the instruction when its
situation arrives, not before.

## When it earns its keep

A context file pays when the same correction would otherwise be retyped. The vendor guidance is
usefully concrete: add to `CLAUDE.md` when Claude makes the same mistake a second time, when a code
review catches something it should have known, when you type last session's correction again, or
when a new teammate would need the same context. [2] Everything else — multi-step procedures,
anything scoped to one part of the codebase — belongs in a skill or a path-scoped rule, because it
does not need to be in every session's context.

## Sharpest real-world gotcha

**A `CLAUDE.local.md` for private notes silently switches off your `AGENTS.md`.** The precedence
check looks for *any* of `CLAUDE.md`, `.claude/CLAUDE.md`, or `CLAUDE.local.md` in the working
directory or above. Add one for your sandbox URLs, and Claude stops reading the `AGENTS.md` the
whole team maintains. [2]

It compounds. When Claude reads `AGENTS.md` directly, it **does not appear in `/memory` or in the
Memory files list in `/context`**, and **`InstructionsLoaded` hooks do not fire**. [2] So the
standard debugging move — run `/context`, check the file loaded — reports the same empty list
whether your instructions are loading or not. The documentation's own advice is to look for the
`AGENTS.md loaded` line or simply ask Claude what its project instructions say.

Runner-up gotcha, for the *Starve the context* play: splitting a 600-line `CLAUDE.md` into six
`@path` imports feels like housekeeping and changes the token count by zero. [2]

## Concrete example we can lift

A worked example for *Write the brief the agent actually reads* — the four-line portable setup, and
then the check that it worked:

```bash
# AGENTS.md is the source of truth every tool reads.
# CLAUDE.md exists only to wire the import and hold Claude-specific overrides.
cat > CLAUDE.md <<'EOF'
@AGENTS.md

## Claude Code
Use plan mode for changes under `src/billing/`.
EOF
```

The verification step is the interesting half, and it is what the play should insist on:

```bash
claude --version          # v2.1.277+ reads AGENTS.md directly; below that, the import is required
```

Then in-session, `/context` and look under **Memory files**. With the import above, `CLAUDE.md`
appears. Without it — relying on native `AGENTS.md` reading — nothing appears there even on success,
and you check the `AGENTS.md loaded:` line in the conversation instead. [2]

A second example, for *Starve the context*, contrasting a rule that always loads against one that
does not:

```markdown
---
paths:
  - "src/api/**/*.ts"
---

# API Development Rules

- All API endpoints must include input validation
- Use the standard error response format
```

Saved as `.claude/rules/api.md`, this costs zero tokens until Claude reads a file under `src/api/`.
The same text pasted into `CLAUDE.md` costs its tokens in every session for the rest of the
project's life. [2]

## Contradictions and gaps

- **Widespread stale claim.** Multiple mid-2026 secondary sources — including a gist framed
  explicitly as debunking the opposite view — assert that Claude Code does not read `AGENTS.md`,
  that a repository with only an `AGENTS.md` "loads zero project instructions," and that requests
  for dual reads remained "open and unshipped as of August 2026." [6] The primary documentation
  contradicts all three. [2] The book must cite vendor docs here and should probably say out loud
  that this is a subject where a year-old blog post will actively mislead you.
- **The 60k-repos figure is undated** on agents.md itself. [1] Other sources give 20,000 repos at an
  August 2025 formalisation growing to 60k+ by mid-2026, but none is primary.
- **No evidence on effectiveness.** Nothing found measures whether shorter context files, cards, or
  path-scoped rules produce better agent output. The "under 200 lines" figure is vendor guidance
  with no published study behind it. Treat as a convention with a plausible mechanism, not a
  finding.
- **Cross-tool behaviour beyond Claude Code was not verified from primary sources.** How Cursor,
  Codex, or Copilot resolve nested `AGENTS.md`, or what they do when both files exist, was not
  established. If a play claims portable behaviour, that gap needs closing first.

## Sources

[1] AGENTS.md — https://agents.md/ — accessed 18 September 2026
[2] How Claude remembers your project, Claude Code docs — https://code.claude.com/docs/en/memory
    — accessed 18 September 2026
[3] Linux Foundation Announces the Formation of the Agentic AI Foundation (AAIF) —
    https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation
    — accessed 18 September 2026
[4] MCP joins the Agentic AI Foundation — https://blog.modelcontextprotocol.io/posts/2025-12-09-mcp-joins-agentic-ai-foundation/
    — accessed 18 September 2026
[5] Cards — https://memention.com/blog/2026/05/25/Cards.html — accessed 18 September 2026
[6] "Does Claude Code read AGENTS.md? No — it reads CLAUDE.md" (gist) —
    https://gist.github.com/yurukusa/d36197848911f025add142abefcde685 — accessed 18 September 2026 —
    **cited as an example of a stale claim, not as evidence**
