# Book structure and the play contract

*The Agentic Playbook* is a markdown book for working developers who already use agentic coding
tools daily and want to get good at them. It is deliberately **plays-first**: the argument is
compressed so the usable material dominates.

## Proportions — these are the point

| Part | Share | Contents |
|---|---|---|
| **I — The Argument** | ~15% | Three short chapters: the pre-Git/pre-Scrum historical analogy; the Four Areas re-weighted; what the book assumes about the reader. |
| **II — The Plays** | ~60% | Six suites of named, self-contained plays. The bulk of the book. |
| **III — Where It Struggles** | ~15% | Failure modes, tasks agents are reliably bad at, honest accounting of where time goes. |
| **IV — Next Waves** | ~10% | Refactoring projects for agent-first development; inviting designers and non-coders in as co-pilots. Then the appendices. |

If a section of Part I is growing past its share, that is a signal to cut it, not to expand the
book. The original outline this plan replaced failed review for being "a taxonomy rather than a
playbook" — Part I is exactly where that failure recurs.

## The six suites of Part II

| Suite | Plays (working titles) |
|---|---|
| **Context** | Write the brief the agent actually reads · Starve the context · Scope a task to fit the window |
| **Harness** | Choose your harness · Package repeatable expertise · Wire in the outside world |
| **Orchestration** | Decompose into subagents · Make the control flow deterministic · Work in parallel without collisions |
| **Verification & Trust** | Review code you did not write · Make the agent prove it · Decide who signs off |
| **Economics** | Understand what you are paying for · Match the model to the job · Know when not to use an agent |
| **Team** | Build the working agreement · Collect and refine as a team · Onboard someone into all this |

## The play template

Every play in Part II uses the same five headings, in this order, so the book is skimmable under
deadline:

> **Problem** — one paragraph, no preamble. State the situation the reader is actually in.
> **The play** — what to actually do.
> **Worked example** — real files, real commands, real output.
> **Failure mode** — how this goes wrong, named and described.
> **Checklist** — the skimmable version, for someone who has read the play once already.

A play is self-contained. A reader who opens the book at one play and reads only that play
should be able to act on it.

## Tools are examples, never headings

Product names age fastest. A section called "LangChain" is a section with a shelf life, so tools
appear *inside* plays as worked examples under durable problem headings. `CLAUDE.md`, `AGENTS.md`,
`rtk`, MCP servers, Skills, LangGraph, n8n, and git worktrees all appear this way.

Concretely: "Controlling token cost" is a heading; "rtk" is an example inside it.

## Prose style

The register is dry and wry — an experienced colleague who has been burned and finds it funny in
retrospect. Humour lives in framing and examples, never inside a numbered procedure: when the
reader is copying a command at 16:50 on a Friday, the prose gets out of the way.

The full style guide — voice rules, worked examples of the register, formatting conventions — is
a separate deliverable and lands at `book/STYLE.md`. Read it before writing prose. Until it
exists, `PLAN.md` section 1 holds the short version.
