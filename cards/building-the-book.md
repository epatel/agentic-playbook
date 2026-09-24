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
- The root `README.md` repeats the table as a numbered list for readers arriving on GitHub,
  and that copy is checked against the table: a chapter it omits or invents, a title or an
  order that disagrees, numbering that has slipped, and the "N plays in six suites" count.
  **Add a play and this reports the README before anyone reads it wrong.**

`make check` runs those checks, and the style checker below, and exits non-zero if any of them
report a real problem. It is a reasonable last step before finishing a writing task.

## The style checker — the rules a machine can decide

`scripts/check_style.py` reads every markdown file under `book/` and reports, with `file:line`,
what `book/STYLE.md`, `book/TEMPLATE-play.md` and the 100-column rule make mechanical. **Do not
count columns or words by hand, and do not write your own version of this** — four writing tasks
each wrote one in `/tmp` before it was written down once, and two of them shipped defects into
the prose.

| Reported | Rule |
|---|---|
| a line over 100 columns | `cards/standing-defaults.md`; counted as characters, so an em dash is one |
| trailing whitespace, a missing final newline, a trailing blank line | `book/STYLE.md`, *Mechanics* |
| a fenced block with no language tag, or one that is never closed | same |
| YAML frontmatter | same |
| an exclamation mark, an emoji, a word from the hype list | `book/STYLE.md`, *Banned outright* |
| a `> Captured` line in the wrong shape, or with no fence under it | `book/TEMPLATE-play.md` |
| an `-ize` spelling — as a **note**, because a quotation may be American | `book/STYLE.md`, *Mechanics* |
| a chapter, suite opener, play or play section outside its word budget | `book/STYLE.md`, *Length*; `book/TEMPLATE-play.md` |
| a play whose five `##` headings are not the template's, verbatim and in order — as a **note** | `book/TEMPLATE-play.md` |

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

### The word budgets

**Do not count words by hand either.** The checker counts every budget the two constraint
documents state, using `word_count` from the build — the same counter `make check` reports per
part, which excludes fenced blocks, headings, table rows and block quotes. `wc -w` and counting by
eye both run a few percent high against it, and at these margins that is the difference between
"48 over" and "67 over".

| Where it sits | Budget | From |
|---|---|---|
| `book/part-1-argument/*.md`, `book/part-3-where-it-struggles/*.md` | 800–1,500 words | `book/STYLE.md`, *Length* |
| `book/part-2-plays/<suite>/index.md` | 150–300 words | same |
| any other file in `book/part-2-plays/<suite>/` | 600–1,200 words, then *Problem* 60–120, *The play* 200–500, *Worked example* 150–400, *Failure mode* 80–200, *Checklist* 4–8 items | `book/TEMPLATE-play.md` |

A play is split on its `##` headings, and a play whose headings are not the template's — verbatim
and in order — gets one note saying so and no section counts, because the sections cannot be
identified. Part IV, the appendices and the preface have no stated budget and are not counted.
Neither is anything outside `book/`, so pointing the checker at `cards` or `plans` still works.

Every budget report is a **problem**, and it fails `make check`. It was a note for exactly as long
as the book had overruns in it: reporting eleven inherited ones as problems would have handed every
unrelated edit a red build it did not cause. They were trimmed, and **the book is now inside every
budget it states**, so an overrun is something your edit introduced rather than something it found.

**This means a play you are editing has single-digit headroom.** Nine of them sit 1–7 words under
the 500-word ceiling in *The play*. Add a clarifying clause or a cross-reference and the build goes
red — which is the intended behaviour, and the answer is not to argue with the count. Take
something out in the same edit: a restated summary, a frame around a quotation, a sentence of
mechanics the section already covers. Two constraints bound what may go — every play states its
exchange rate, and every *Checklist* item has to trace to something in *The play*.

A red build is also cheap to clear while you are mid-draft: the count is exact, so `make lint`
tells you the distance in words, not a direction to go in.

The budgets are hard-coded in the script, each one naming the document it came from, and
`--self-test` checks that the range is still printed there — which is the only reason they may be
hard-coded at all. **Move a number in `book/STYLE.md` or `book/TEMPLATE-play.md` and the self-test
fails until the script agrees with it.**

### Sentence shape

Three more checks, added 24 September 2026, measure how sentences are built. All three are
**notes**: they report and never fail the build, because a long sentence or a dash can be the right
choice and only a person can say so. Each reports once per file where it can, so the list shows
which files to work on first and shrinks as they improve.

| Note | Reports | Threshold |
|---|---|---|
| `long-sentence` | how many sentences in a file run over the limit, and on which lines | over 40 words |
| `dash-density` | em dashes per 1,000 words of prose, for files of 300 words or more | over 10 |
| `heading-review` | a Part I, III or IV heading that points back at the prose — ends on a pronoun, or opens *Where that…* — instead of saying what the section holds | — |

They measure running prose only: headings, tables, block quotes and fenced blocks are left out,
every list item is measured as its own paragraph, and the constraint documents at the top of
`book/` are not measured. Sentences are split the way the read-aloud script splits them. A run
with notes and no problems ends **No problems; the notes above are for a person to judge**, which
is a clean run — "No defects" only appears when there are no notes at all.

## Two severities, because the book is half-written

A **problem** is something a person should fix. A **note** is the expected consequence of building
an unfinished book — a forward link to a chapter nobody has written, a diagram left as source — or,
from the style checker, a rule that is exact about its count and soft about its threshold: an
`-ize` spelling that may be sitting inside a quotation. Only problems fail `--strict`, so
`make check` does not cry wolf for the months in which most of the table of contents is ⬜.

A note is not a licence to ignore it. Read the ones against the file you are editing before you
finish. The word budgets were notes until the book met them and are problems now; a rule earns that
promotion by being one the book can actually hold to.

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

`--repo-url` turns links that leave the book — research notes, the plans — into absolute URLs,
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
| `scripts/read-aloud.html` | A play button on every chapter and section heading of the HTML book, injected with `--include-after-body`. HTML only; the PDF never sees it. |
| `scripts/favicon.svg` | The tab icon. Inlined into `<head>` as a base64 data URI at build time, so the HTML book stays one file; edit the SVG, never the generated link. |

Changing either is a data edit, not a code edit. That is the point of them.

## Reviewing the book, and acting on a review

`make review` serves the book at `http://127.0.0.1:8777` and lets a reader select any passage and
attach a comment to it. Several people can read at once over a WebSocket, and a comment appears in
every open window as it is made.

Each heading carries a play button that reads that section aloud, for catching by ear what the
eye skips. It uses the Web Speech API and prefers Edge's `Microsoft Andrew Online (Natural)`,
falling back to any natural en-US voice and then to whatever the browser has — in Chrome that is a
system voice, so it works and sounds worse. Code blocks, tables, diagrams and the
`> Captured <month> <year>` provenance lines are not read: they are not prose.

A word the synthesiser mispronounces is fixed in the `SAY` list at the top of the read-aloud
script, which rewrites the string handed to the speech engine and leaves the page alone. It is the
one place where the book's text and the book's sound are allowed to differ.

**If you are the agent acting on a review, read [`review/REVIEW.md`](../review/REVIEW.md).** It is
the open annotations as a task list, in the book's own reading order, each one giving
`book/<path>:<line>` and the passage that was quoted. It is generated from the event log on every
change, so do not edit it — resolve the annotation in the browser instead, or fix the book and
resolve it.

Two properties are deliberate and worth keeping if this is ever rewritten:

- **Annotations anchor to the markdown source, not to rendered HTML.** The server renders the book
  itself, with markdown-it's line map, so every block carries the source line it came from. The
  built HTML is a better page and cannot do this: pandoc discards the mapping. An annotation that
  cannot say which line it is about is not actionable by an agent.
- **`review/annotations.jsonl` is an append-only event log.** Create, resolve, reopen and delete
  are all appends; nothing is rewritten. Two reviewers cannot lose each other's work, a deletion is
  recoverable, and the store needs no database and so no migration path
  ([`cards/standing-defaults.md`](standing-defaults.md)).

This is the only part of the repo with dependencies. They live in `.venv/`, which `make review`
creates from `requirements.txt` on first run; `make html`, `make pdf` and `make check` never touch
them.
