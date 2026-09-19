# Building the book — one file, a PDF, and an HTML book

The book is markdown and stays readable without any of this. The build exists for the times a
loose directory of chapters is the wrong shape: reading a whole part end to end, sending a draft
to somebody who does not have the repo, or checking that Part II really is 60% of the words.

```bash
make            # the target list
make html       # build/agentic-playbook.html  — needs only pandoc; one self-contained file
make pdf        # build/agentic-playbook.pdf   — needs pandoc and a PDF engine
make md         # build/agentic-playbook.md    — needs nothing but Python
make open       # build the PDF, then hand it to the default viewer
make open-html  # build the HTML book, then hand it to the default browser
make check      # report problems, write nothing, exit non-zero if any
make lint       # the style half of make check alone, for a quick pass while writing
make clean      # delete build/
```

`make open` and `make open-html` are the read-it-now targets: each depends on its format, so it
rebuilds first and then hands the file to `open` (macOS) or `xdg-open` (Linux). With neither on
`PATH` they print where the file is rather than failing silently.

Everything lands in `build/`, which is gitignored. **Never commit build output**, and never edit
it — it is regenerated from `book/` every run, and the collected markdown is an intermediate for
pandoc rather than a second copy of the book.

## Which format to reach for

**HTML is the cheapest and the one to send someone.** It needs pandoc and nothing else: no PDF
engine, no TeX, no node. `--embed-resources` inlines the stylesheet and every image, so the output
is a single file that survives being emailed, dropped in a chat, or opened from a USB stick, and it
reflows on a phone. The contents list is a sidebar that goes three levels deep, so the five play
headings are navigable rather than just present. `Cmd+P` from the browser gives a decent printed
copy, with page breaks before each part, if a PDF engine is more trouble than it is worth.

**The PDF is the one to print or to read in a page-turning app.** It costs a PDF engine, and its
contents page stops at two levels, because a printed table of contents listing eighteen plays
times five headings is not a table of contents.

Both are derived from the same collected markdown and the same table of contents, so neither can
quietly contain a different book.

## What the build depends on you doing

**The table of contents in [`book/README.md`](../book/README.md) decides what is in the book and
in what order.** The build reads that table and nothing else — not the directory listing, not the
filenames. This is the same contract authors already work under, now with something that checks
it:

- A file that is not in the table is reported as an orphan and is **not in the build**.
- A row marked ✅ or 🟡 whose file is missing is reported as a problem.
- A row marked ⬜ is expected to be missing and is listed on the *About this build* page instead.
- A `#` heading that does not match its table-of-contents title is reported.

`make check` runs those checks, and the style checker below, and exits non-zero if any of them
report a real problem. It is a reasonable last step before finishing a writing task.

## The style checker — the rules a machine can decide

`scripts/check_style.py` reads every markdown file under `book/` and reports, with `file:line`,
what `book/STYLE.md` and the 100-column rule make mechanical. **Do not count columns by hand, and
do not write your own version of this** — four writing tasks each wrote one in `/tmp` before it
was written down once, and two of them shipped defects into the prose.

| Reported | Rule |
|---|---|
| a line over 100 columns | `cards/standing-defaults.md`; counted as characters, so an em dash is one |
| trailing whitespace, a missing final newline, a trailing blank line | `book/STYLE.md`, *Mechanics* |
| a fenced block with no language tag, or one that is never closed | same |
| YAML frontmatter | same |
| an exclamation mark, an emoji, a word from the hype list | `book/STYLE.md`, *Banned outright* |
| a `> Captured` line in the wrong shape, or with no fence under it | `book/TEMPLATE-play.md` |
| an `-ize` spelling — as a **note**, because a quotation may be American | `book/STYLE.md`, *Mechanics* |

What it deliberately does not report matters as much, because each exemption is a decision
somebody already made and a false positive is how a checker gets switched off:

- **Nothing inside a fenced block.** A mermaid node may be 128 columns wide, a ```` ```markdown ````
  sample may contain a `---` that is not frontmatter, and captured output is whatever the machine
  printed.
- **Table rows**, which are not wrappable.
- **A line that is one markdown link and some punctuation**, which is how the longest play titles
  and the deepest suite paths reach 114 columns with nothing to break. Two links on one line is
  not exempt: that one can be split.
- **Anything inside double quotes**, for the vocabulary rules only. The book quotes American
  sources verbatim, and a quotation is not this book's voice.
- **`book/STYLE.md`** for the bans, because the document that defines them has to print them.
- **`book/examples/`**, which is apparatus: one fixture is a deliberately terrible `CLAUDE.md`,
  and another is a rules file whose frontmatter is the point. Name the path to check it anyway.

It writes nothing, it takes about a tenth of a second, and it is not a judgement on the prose —
voice, humour and everything else in `book/STYLE.md` still needs a person. Point it at anything:

```bash
make lint                                        # book/, the same as make check runs
python3 scripts/check_style.py book/part-3-where-it-struggles cards plans
python3 scripts/check_style.py --self-test       # check the checker against its own fixture
```

If you change a rule, run `--self-test`. The fixture encodes the traps — a 100-column line made
of em dashes, a 128-column mermaid node, a `---` inside a sample, a quoted exclamation mark — and
each of them was reported as a defect by somebody's throwaway version.

## Two severities, because the book is half-written

A **problem** is something a person should fix. A **note** is the expected consequence of building
an unfinished book — a forward link to a chapter nobody has written, a diagram left as source — or,
from the style checker, a rule with legitimate exceptions that wants a human's eye.
Only problems fail `--strict`, so `make check` does not cry wolf for the months in which most of
the table of contents is ⬜.

Forward references are allowed by the cross-reference convention, so the build unlinks the ones
whose target is absent and leaves the link text as prose. Left in place they are a hard error in
typst, and a silently broken link everywhere else.

## Installing the pieces

| Tool | Needed for | Install |
|---|---|---|
| Python 3 | everything | already there |
| pandoc | HTML and PDF | `brew install pandoc` |
| typst | PDF | `brew install typst` — one 45 MB binary, and the default engine |
| node | diagrams **in the PDF** | already there if you have npm; the build calls `npx` |

`make html` needs the first row and the second. Any of `typst`, `tectonic`, `xelatex`, `lualatex`,
`pdflatex`, `weasyprint`, `wkhtmltopdf`, `prince` or `pagedjs-cli` will do for the PDF; the first
one found on `PATH` wins, and `--pdf-engine` forces the choice. With none of them installed the
build still writes the collected markdown and tells you what to install.

## Diagrams

Authors write mermaid and change nothing for either format. The two builds draw it differently, on
purpose.

**The HTML book draws its own diagrams.** A browser can render mermaid, so each ```mermaid``` block
becomes a `<pre class="mermaid">` and [mermaid.js](https://cdn.jsdelivr.net/npm/mermaid@11/) turns
it into vector output that matches the reader's colour scheme, at whatever width their window is.
That means **the HTML book needs no node and no mermaid-cli**, and that the diagrams want a network
connection the first time the file is opened. Offline, they degrade to their own source, styled as
a code block — the same thing the PDF does without a renderer — and the build says so as a note
either way.

**The PDF has no such luxury** and shells out to mermaid-cli for PNGs. The rest of this section is
about that path.

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
you want a diagram checked — the HTML book defers to the browser, so it will not catch a syntax
error either.

`--no-mermaid` turns both paths off and leaves every diagram as source. `--mermaid-cmd` overrides
how mermaid-cli is invoked, and applies to the PDF only.

## Useful flags

```bash
python3 scripts/build_book.py --help
make html ARGS='--repo-url https://github.com/<owner>/<repo>/blob/main'
```

`--repo-url` turns links that leave the book — research briefs, the plans — into absolute URLs,
so they still work for someone reading the built book without the repo. It is worth passing
whenever you are sending the HTML to somebody. `--no-draft-note` drops the *About this build*
page. `--verbose` echoes the pandoc and mermaid commands.

## If you are changing the build

`scripts/build_book.py` is a single dependency-free file, per
[`cards/standing-defaults.md`](standing-defaults.md). Page breaks and link colours are the only
engine-specific parts, and nothing about how the book *looks* lives in the Python:

| File | Owns |
|---|---|
| `scripts/book-metadata.yaml` | Title, language, page size, margins, link colour — the PDF's typography. |
| `scripts/book.css` | The HTML book: reading measure, the contents sidebar, code, tables, diagrams, dark mode, and the print rules a browser uses for `Cmd+P`. |

Changing either is a data edit, not a code edit. That is the point of them.
