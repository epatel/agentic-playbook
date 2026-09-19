# Repo layout — what lives where

A markdown book repo. No application code and no package manager; the one build target collects
the book into a PDF and is never needed to read it. Every directory has one job, and two of them
are read-only.

## The map

| Path | Holds | Writable? |
|---|---|---|
| `PLAN.md` | The authoritative design document: locked decisions, book outline, play template, build sequence. | Rarely — see below |
| `plans/agentic-playbook.md` | The shared execution plan: goal, non-goals, milestones, decision log, handoff note, open questions. | **Yes — every task updates it** |
| `book/` | The book itself. Chapter and play files, one file per unit. | Yes |
| `notes/research/` | Cited research briefs. Evidence the chapters draw from. | Yes |
| `notes/raw/` | Original scattered ideation, superseded by `PLAN.md`. | **No — frozen** |
| `cards/` | These reference cards. | Yes, when a convention changes |
| `scripts/`, `Makefile` | The book build: collect the chapters, render a PDF. See [building-the-book](building-the-book.md). | Yes |
| `build/` | Build output. | **No — generated, gitignored, never committed** |
| `.claude/skills/` | Symlinked agent skills. | Rarely |

## The two frozen things

`notes/raw/` is source material that has already been mined and consolidated. It is kept for
provenance — so a later reader can check what an idea looked like before it was shaped. Do not
edit, tidy, reformat, or "improve" these files. If something in them is wrong or outdated, that
is fine; they are a record, not a spec.

`PLAN.md` holds decisions that were made deliberately and are expensive to reopen — the
deliverable format, the intended reader, the tone, the plays-first proportions. Do not change
them on your own initiative. If your task genuinely cannot proceed under a locked decision, stop
and ask rather than quietly working around it.

## Where new work goes

- Writing a chapter or a play → a new file in `book/`
- Producing research → a cited brief in `notes/research/`
- Discovering a constraint or making a call that affects other tasks → append it to the
  execution plan at `plans/agentic-playbook.md`
- Establishing a repo-wide convention that future agents must follow → a new card in `cards/`,
  plus an index line in the root `CLAUDE.md`

## Creating directories

`book/` and `notes/research/` both exist. The part directories under `book/` mostly do not —
they are created by the first task that needs one. If you are that task, create the directory and
put your file in it. Do not add placeholder or `.gitkeep` files to directories you are not
otherwise filling.

## Naming

Lowercase, hyphenated, descriptive of content rather than position: `starve-the-context.md`,
not `play-03.md`. Ordering is expressed in the book's table of contents, not in filenames —
because plays get inserted, reordered, and dropped, and renumbering a directory is a merge
conflict waiting to happen.
