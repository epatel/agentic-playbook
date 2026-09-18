# Project-local agent skills

The two entries beside this file are **symlinks** into a local checkout of
<https://github.com/epatel/agent-skills>, not vendored copies. Git stores them as symlinks with an
absolute target, so they resolve on the machine that created them and dangle anywhere else.

That is the tradeoff on purpose: the skills stay current with their upstream repo instead of
drifting as stale copies. The cost is one setup step on a fresh clone.

## Recreating them

```bash
git clone https://github.com/epatel/agent-skills ~/Development/claude/agent-skills

cd <this-repo>/.claude/skills
ln -sfn ~/Development/claude/agent-skills/backward-planning .
ln -sfn ~/Development/claude/agent-skills/review-agentic-setup .
```

Skills load at session start, so start a new Claude Code session afterwards.

## What is linked, and why these two

| Skill | Use it when |
|---|---|
| `backward-planning` | Scoping a part, a suite, or the book's arc — reasoning back from the finished outcome to what must be true to get there. Useful because the destination here is clearer than the path. |
| `review-agentic-setup` | Auditing or refreshing this repo's own agentic setup: `CLAUDE.md`, the cards in `cards/`, the shared plan, these skills. Run it before making structural changes to any of them. |

Deliberately **not** linked: `ste-writing`. It rewrites prose into ASD-STE100 Simplified Technical
English, which would sand off exactly the dry-and-wry register this book commits to. The remaining
skills in the upstream repo target code structure — state machines, module boundaries, abstract
data types — and there is no code here for them to act on.
