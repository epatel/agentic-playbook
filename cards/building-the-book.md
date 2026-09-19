# Building the book — one file, and a PDF

The book is markdown and stays readable without any of this. The build exists for the times a
loose directory of chapters is the wrong shape: reading a whole part end to end, sending a draft
to somebody who does not have the repo, or checking that Part II really is 60% of the words.

```bash
make            # the target list
make pdf        # build/agentic-playbook.pdf   — needs pandoc and a PDF engine
make md         # build/agentic-playbook.md    — needs nothing but Python
make html       # build/agentic-playbook.html  — needs pandoc
make open       # build the PDF, then hand it to the default viewer
make check      # report problems, write nothing, exit non-zero if any
make clean      # delete build/
```

`make open` is the read-it-now target: it depends on `pdf`, so it rebuilds first and then hands
the file to `open` (macOS) or `xdg-open` (Linux). With neither on `PATH` it prints where the PDF
is rather than failing silently.

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
| node | rendered diagrams | already there if you have npm; the build calls `npx` |

Any of `typst`, `tectonic`, `xelatex`, `lualatex`, `pdflatex`, `weasyprint`, `wkhtmltopdf`,
`prince` or `pagedjs-cli` will do; the first one found on `PATH` wins, and `--pdf-engine` forces
the choice. With none of them installed the build still writes the collected markdown and tells
you what to install.

## Diagrams

```mermaid``` blocks are rendered to PNGs and embedded in the PDF. **You do not have to install
anything for this**: the build uses `mmdc` if it is on `PATH`, and otherwise runs
`npx --yes @mermaid-js/mermaid-cli`, which fetches the package on first use and caches it. If you
build often, `npm install -g @mermaid-js/mermaid-cli` makes each diagram a few seconds faster.

Renders are cached in `build/diagrams/` against the diagram source, so only diagrams you actually
changed are re-rendered. `make clean` throws the cache away.

Each diagram is sized to its natural width, capped at the text width of the page. Pandoc would
otherwise read the PNG's pixel width, assume 96 dpi, and lay the 3×-scaled image out three times
too wide — which is how a diagram ends up running off the side of the page.

Two failures are told apart, because they need different reactions:

- **The renderer could not run** — no node, no network on first use, no browser for puppeteer.
  Every diagram is left as source and you get a *note*. `--strict` still passes, because this is
  a fact about the machine rather than about the book.
- **A diagram is wrong** — a syntax error mermaid rejects. That one diagram is left as source and
  you get a *problem* naming the chapter and quoting mermaid's error, so `--strict` fails. The
  other diagrams still render.

`make check` does not render diagrams at all; it writes nothing and stays fast. Build the PDF if
you want a diagram checked.

`--no-mermaid` skips rendering entirely, and `--mermaid-cmd` overrides how mermaid-cli is invoked.

## Useful flags

```bash
python3 scripts/build_book.py --help
make pdf ARGS='--repo-url https://github.com/<owner>/<repo>/blob/main'
```

`--repo-url` turns links that leave the book — research briefs, the plans — into absolute URLs,
so they still work for someone reading the PDF without the repo. `--no-draft-note` drops the
*About this build* page. `--verbose` echoes the pandoc and mermaid commands.

## If you are changing the build

`scripts/build_book.py` is a single dependency-free file, per
[`cards/standing-defaults.md`](standing-defaults.md). Page breaks and link colours are the only
engine-specific parts; typography lives in `scripts/book-metadata.yaml` so that tuning it does not
mean editing Python.
