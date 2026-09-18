# Standing defaults

One-time decisions that should never be reconsidered project by project. Agents and people alike
tend to take the fastest path to the immediate problem, and the fastest path quietly accrues
debt. These are the defaults; deviating from one is a decision to record, not a judgement call to
make silently.

## Diagrams: mermaid, never ASCII art

Any diagram in a chapter, a plan, a card, or a message uses a fenced ```mermaid``` block. Mermaid
renders as a real diagram; ASCII art does not, and it degrades further every time someone reflows
the paragraph around it.

This applies to the book's own content. A play explaining a subagent topology gets a mermaid
graph, not a box-drawing sketch.

## Tooling scripts: Python, not Node

If this repo ever grows a build, lint, link-check, word-count, or site-render script, write it in
Python. Not Node, not a shell script that has outgrown itself.

The book does not currently need a toolchain, and it should stay that way as long as possible —
a markdown book that requires `npm install` before you can read it has failed at being a markdown
book. Add tooling only when a real, repeated need appears.

## Python: always use a virtual environment

If tooling does appear and needs dependencies, never install them into system or user Python.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

- Commit `requirements.txt`; add `.venv/` to `.gitignore`
- In scripts and any scheduled job, call the interpreter by full path rather than relying on
  shell activation
- If a tool genuinely must be system-wide, document that as an explicit exception

Dependency sets differ per project and drift over time. A venv makes the set explicit,
reproducible on another machine, and disposable when it breaks.

## Databases: always ship a migration path

The moment anything here persists data, establish a defined upgrade path from any older schema to
the current one. Add the mechanism with the first table, not during the first crisis.

- Track schema version in a single-row table or equivalent
- Keep migrations as ordered, immutable, forward-only steps
- On startup, read the current version and apply pending steps in order, inside a transaction
- Never modify a migration that has been deployed; add a new one

Without a migration path, the only ways to change a schema are to lose the data or to hand-edit
production.

## Prose files: wrap at 100 columns

Markdown in this repo is hard-wrapped at 100 columns. This keeps diffs line-scoped, so a
one-sentence edit shows up as a one-line change rather than a reflowed paragraph — which matters
a great deal when several agents write into the same book in parallel and their work has to be
merged.

Do not wrap inside a table row, a URL, or a fenced code block.
