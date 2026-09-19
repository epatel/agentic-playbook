# Building the book — one file, and a PDF

The book is markdown and stays readable without any of this. The build exists for the times a
loose directory of chapters is the wrong shape: reading a whole part end to end, sending a draft
to somebody who does not have the repo, or checking that Part II really is 60% of the words.

```bash
make            # the target list
make pdf        # build/agentic-playbook.pdf   — needs pandoc and a PDF engine
make md         # build/agentic-playbook.md    — needs nothing but Python
make html       # build/agentic-playbook.html  — needs pandoc
make check      # report problems, write nothing, exit non-zero if any
make clean      # delete build/
```

Everything lands in `build/`, which is gitignored. **Never commit build output**, and never edit
it — it is regenerated from `book/` every run, and the collected markdown is an intermediate for
pandoc rather than a second copy of the book.

## What the build depends on you doing

**The table of contents in [`book/README.md`](../book/README.md) decides what is in the book and
in what order.** The build reads that table and nothing else — not the directory listing, not the
filenames. This is the same contract authors already work under, now with something that checks
it:

- A file that is not in the table is reported as an orphan and is **not in the PDF**.
- A row marked ✅ or 🟡 whose file is missing is reported as a problem.
- A row marked ⬜ is expected to be missing and is listed on the *About this build* page instead.
- A `#` heading that does not match its table-of-contents title is reported.

`make check` runs those checks and exits non-zero if any of them are real problems. It is a
reasonable last step before finishing a writing task.

## Two severities, because the book is half-written

A **problem** is something a person should fix. A **note** is the expected consequence of building
an unfinished book — a forward link to a chapter nobody has written, a diagram left as source.
Only problems fail `--strict`, so `make check` does not cry wolf for the months in which most of
the table of contents is ⬜.

Forward references are allowed by the cross-reference convention, so the build unlinks the ones
whose target is absent and leaves the link text as prose. Left in place they are a hard error in
typst, and a silently broken link everywhere else.

## Installing the pieces

| Tool | Needed for | Install |
|---|---|---|
| Python 3 | everything | already there |
| pandoc | PDF and HTML | `brew install pandoc` |
| typst | PDF | `brew install typst` — one 45 MB binary, and the default engine |
| mermaid-cli | rendered diagrams | `npm install -g @mermaid-js/mermaid-cli` |

Any of `typst`, `tectonic`, `xelatex`, `lualatex`, `pdflatex`, `weasyprint`, `wkhtmltopdf`,
`prince` or `pagedjs-cli` will do; the first one found on `PATH` wins, and `--pdf-engine` forces
the choice. With none of them installed the build still writes the collected markdown and tells
you what to install.

Without mermaid-cli, mermaid blocks print as source in the PDF. That is a note rather than a
problem: the diagrams are still correct in the markdown, which is the deliverable.

## Useful flags

```bash
python3 scripts/build_book.py --help
make pdf ARGS='--repo-url https://github.com/<owner>/<repo>/blob/main'
```

`--repo-url` turns links that leave the book — research briefs, the plans — into absolute URLs, so
they still work for someone reading the PDF without the repo. `--no-draft-note` drops the *About
this build* page. `--verbose` echoes the pandoc command.

## If you are changing the build

`scripts/build_book.py` is a single dependency-free file, per
[`cards/standing-defaults.md`](standing-defaults.md). Page breaks and link colours are the only
engine-specific parts; typography lives in `scripts/book-metadata.yaml` so that tuning it does not
mean editing Python.
