#!/usr/bin/env python3
"""Collect the book into one markdown file, and render it as PDF or HTML.

The book is a set of standalone markdown files whose only ordering mechanism is the table of
contents in ``book/README.md``. This script reads that table, concatenates the files it names in
the order it names them, rewrites cross-references into internal anchors, and hands the result to
pandoc.

Nothing here edits the book. Everything is written to ``build/``, which is not committed.

Usage
-----

    python3 scripts/build_book.py              # markdown + PDF (if an engine is installed)
    python3 scripts/build_book.py --format md  # markdown only, no external tools needed
    python3 scripts/build_book.py --check      # report missing and orphaned files, then stop

Run ``--help`` for the rest.
"""

from __future__ import annotations

import argparse
import datetime as _datetime
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOK = ROOT / "book"
TOC_FILE = BOOK / "README.md"
DEFAULT_OUT = ROOT / "build"
METADATA_FILE = Path(__file__).resolve().parent / "book-metadata.yaml"

#: Files in ``book/`` that are instructions to authors rather than book content. They are excluded
#: from the build deliberately, and are not reported as orphans.
NOT_BOOK_CONTENT = {"README.md", "STYLE.md", "TEMPLATE-play.md"}

#: Tried in this order when ``--pdf-engine`` is not given. typst is first because it is a single
#: small binary, unlike a TeX distribution.
PDF_ENGINES = [
    "typst",
    "tectonic",
    "xelatex",
    "lualatex",
    "pdflatex",
    "weasyprint",
    "wkhtmltopdf",
    "prince",
    "pagedjs-cli",
    "context",
]

HTML_PDF_ENGINES = {"weasyprint", "wkhtmltopdf", "prince", "pagedjs-cli"}
TEX_PDF_ENGINES = {"tectonic", "xelatex", "lualatex", "pdflatex"}

#: Pandoc reader. ``smart`` is off: the prose already uses real em dashes and curly quotes where it
#: wants them, and having pandoc guess at the rest changes the author's punctuation silently.
PANDOC_FROM = "markdown+pipe_tables+backtick_code_blocks+fenced_code_attributes-smart"


# --------------------------------------------------------------------------------------------
# Small helpers
# --------------------------------------------------------------------------------------------

def slugify(text: str) -> str:
    """Slugify a heading the way GitHub does, so links written against GitHub still resolve."""
    text = re.sub(r"`([^`]*)`", r"\1", text)
    text = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"[*_~]", "", text)
    text = text.strip().lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"\s+", "-", text)
    return text.strip("-") or "section"


class Fences:
    """Tracks whether a line sits inside a fenced code block.

    Headings and links inside a fence are examples, not markup, and rewriting them would corrupt
    every code sample in the book.
    """

    _OPEN = re.compile(r"^(\s{0,3})(`{3,}|~{3,})\s*(.*)$")

    def __init__(self) -> None:
        self.marker: str | None = None
        self.info: str = ""

    @property
    def inside(self) -> bool:
        return self.marker is not None

    def feed(self, line: str) -> bool:
        """Consume a line. Returns True if this line is itself a fence delimiter."""
        match = self._OPEN.match(line)
        if not match:
            return False
        _, marker, info = match.groups()
        if self.marker is None:
            self.marker, self.info = marker, info.strip()
            return True
        if marker[0] == self.marker[0] and len(marker) >= len(self.marker) and not info.strip():
            self.marker, self.info = None, ""
            return True
        return False


def word_count(text: str) -> int:
    """Count prose words, ignoring fenced code, tables and headings."""
    fences, words = Fences(), 0
    for line in text.splitlines():
        if fences.feed(line) or fences.inside:
            continue
        stripped = line.strip()
        if stripped.startswith(("#", "|", ">")) or not stripped:
            continue
        words += len(stripped.split())
    return words


def log(message: str = "") -> None:
    print(message, file=sys.stderr)


def rel(path: Path) -> str:
    """Path relative to the repo root where possible, for readable output."""
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path)


class Reporter:
    """Two severities, because the book is half-written and will be for a while.

    A *problem* is something a person should fix: a broken cross-reference, a file nobody put in
    the table of contents, a chapter marked done that is not on disk. A *note* is the expected
    consequence of building an unfinished book, and must not fail ``--strict`` — otherwise the
    check target cries wolf until the last chapter lands.
    """

    def __init__(self) -> None:
        self.problems: list[str] = []
        self.notes: list[str] = []

    def warn(self, message: str) -> None:
        self.problems.append(message)

    def note(self, message: str) -> None:
        self.notes.append(message)

    def print(self) -> None:
        for label, messages in (("problem", self.problems), ("note", self.notes)):
            if not messages:
                continue
            log("")
            log(f"{len(messages)} {label}{'s' if len(messages) != 1 else ''}:")
            for message in messages:
                log(f"  - {message}")


# --------------------------------------------------------------------------------------------
# The table of contents
# --------------------------------------------------------------------------------------------

@dataclass
class Chapter:
    path: str            # relative to book/
    title: str
    status: str          # the raw status cell: ✅, 🟡 or ⬜
    part: str            # the part heading it falls under
    anchor: str = ""     # assigned once collisions are known
    text: str = ""
    words: int = 0

    @property
    def file(self) -> Path:
        return BOOK / self.path

    @property
    def written(self) -> bool:
        return "✅" in self.status or "🟡" in self.status

    @property
    def placeholder(self) -> bool:
        """A row that names a directory rather than a file — the part task supplies the rows."""
        return self.path.endswith("/")


@dataclass
class Part:
    title: str
    anchor: str
    chapters: list[Chapter] = field(default_factory=list)


ROW = re.compile(r"^\|(?P<num>[^|]*)\|(?P<path>[^|]*)\|(?P<title>[^|]*)\|(?P<status>[^|]*)\|\s*$")


def parse_toc(markdown: str) -> list[Part]:
    """Read the table of contents. It is the book's only ordering mechanism."""
    lines = markdown.splitlines()
    try:
        start = next(i for i, l in enumerate(lines) if l.strip().lower() == "### table of contents")
    except StopIteration:
        raise SystemExit(f"No '### Table of contents' heading in {TOC_FILE.relative_to(ROOT)}")

    parts: list[Part] = []
    for line in lines[start + 1:]:
        if line.startswith("## "):
            break
        match = ROW.match(line)
        if not match:
            continue
        num = match["num"].strip()
        path = match["path"].strip().strip("`").strip()
        title = match["title"].strip().strip("*").strip()
        status = match["status"].strip()

        if set(num) <= set("-: ") and num:      # the |---|---| separator row
            continue
        if num.lower().strip("*| ") in {"#", ""} and not path and not title:
            continue

        if num.startswith("**"):                # a part row: | **Part I** | | **The Argument** | |
            label = num.strip("*").strip()
            heading = f"{label} — {title}" if title else label
            parts.append(Part(title=heading, anchor=slugify(heading)))
            continue

        if not num.isdigit() or not path:
            continue
        if not parts:
            raise SystemExit(f"Chapter row before any part row in the table of contents: {path}")
        parts[-1].chapters.append(
            Chapter(path=path, title=title, status=status, part=parts[-1].title)
        )
    if not parts:
        raise SystemExit("The table of contents parsed to nothing — has its shape changed?")
    return parts


def assign_anchors(parts: list[Part]) -> dict[str, Chapter]:
    """Give every chapter a stable anchor, keyed by its path so links can be rewritten.

    Filenames are unique across the book with one known exception — each suite has an ``index.md``
    — so the stem is used where it is unique and the full path where it is not.
    """
    chapters = [c for part in parts for c in part.chapters if not c.placeholder]
    stems = [Path(c.path).stem for c in chapters]
    by_path: dict[str, Chapter] = {}
    for chapter in chapters:
        stem = Path(chapter.path).stem
        base = stem if stems.count(stem) == 1 else chapter.path[:-3].replace("/", "-")
        chapter.anchor = slugify(base)
        by_path[chapter.path] = chapter
    return by_path


# --------------------------------------------------------------------------------------------
# Rewriting one chapter
# --------------------------------------------------------------------------------------------

HEADING = re.compile(r"^(?P<hashes>#{1,6})\s+(?P<text>.*?)\s*#*\s*$")
LINK = re.compile(r"\]\(\s*(?P<target><[^>]*>|[^)\s]+)(?P<rest>\s+\"[^\"]*\")?\s*\)")


class ChapterRewriter:
    """Shift a chapter's headings down a level, give them ids, and localise its links."""

    def __init__(self, chapter: Chapter, chapters_by_path: dict[str, Chapter], repo_url: str | None,
                 reporter: Reporter) -> None:
        self.chapter = chapter
        self.by_path = chapters_by_path
        self.repo_url = repo_url.rstrip("/") if repo_url else None
        self.warn = reporter.warn
        self.seen_ids: set[str] = set()

    # -- headings ----------------------------------------------------------------------------

    def _unique(self, ident: str) -> str:
        candidate, n = ident, 1
        while candidate in self.seen_ids:
            n += 1
            candidate = f"{ident}-{n}"
        self.seen_ids.add(candidate)
        return candidate

    def _heading(self, line: str, first_seen: list[bool]) -> str:
        match = HEADING.match(line)
        if not match:
            return line
        level = len(match["hashes"])
        text = match["text"]
        if level == 1 and not first_seen[0]:
            first_seen[0] = True
            ident = self._unique(self.chapter.anchor)
            if slugify(text) != slugify(self.chapter.title):
                self.warn(f"{self.chapter.path}: title heading '{text}' does not match its table-"
                          f"of-contents title '{self.chapter.title}'")
        else:
            ident = self._unique(f"{self.chapter.anchor}--{slugify(text)}")
        new_level = level + 1
        if new_level > 6:
            self.warn(f"{self.chapter.path}: heading '{text}' is nested too deep to shift; "
                      f"kept at level 6")
            new_level = 6
        return f"{'#' * new_level} {text} {{#{ident}}}"

    # -- links -------------------------------------------------------------------------------

    def _target(self, target: str) -> str:
        if target.startswith("<") and target.endswith(">"):
            return f"<{self._target(target[1:-1])}>"
        if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target) or target.startswith("//"):
            return target                                  # external URL, mailto:, etc.

        path_part, _, fragment = target.partition("#")
        if not path_part:                                  # same-file link: #failure-mode
            return f"#{self.chapter.anchor}--{fragment}" if fragment else target

        source_dir = (BOOK / self.chapter.path).parent
        resolved = (source_dir / path_part).resolve()
        try:
            relative = resolved.relative_to(BOOK).as_posix()
        except ValueError:
            relative = None

        if relative and relative in self.by_path:          # another chapter → internal anchor
            anchor = self.by_path[relative].anchor
            return f"#{anchor}--{fragment}" if fragment else f"#{anchor}"

        if resolved.is_file() and resolved.suffix.lower() in {".png", ".jpg", ".jpeg", ".svg",
                                                              ".pdf", ".gif"}:
            return str(resolved)                           # images: absolute, so build/ can find

        if self.repo_url:
            try:
                repo_relative = resolved.relative_to(ROOT).as_posix()
            except ValueError:
                return target
            suffix = "/" if resolved.is_dir() else ""
            return f"{self.repo_url}/{repo_relative}{suffix}" + (f"#{fragment}" if fragment else "")

        if relative is not None and path_part.endswith(".md"):
            self.warn(f"{self.chapter.path}: links to '{path_part}', which is not in the table of "
                      f"contents and so is not in this build")
        return target

    # -- the pass ----------------------------------------------------------------------------

    def run(self, text: str) -> str:
        fences, first_seen, out = Fences(), [False], []
        for line in text.splitlines():
            if fences.feed(line) or fences.inside:
                out.append(line)
                continue
            if line.lstrip().startswith("#"):
                out.append(self._heading(line, first_seen))
                continue
            out.append(LINK.sub(lambda m: f"]({self._target(m['target'])}{m['rest'] or ''})", line))
        if not first_seen[0]:
            self.warn(f"{self.chapter.path}: no level-1 title heading")
        return "\n".join(out)


# --------------------------------------------------------------------------------------------
# Mermaid
# --------------------------------------------------------------------------------------------

MERMAID_OPEN = re.compile(r"^(\s{0,3})(`{3,}|~{3,})\s*\{?\.?mermaid\b")


def render_mermaid(text: str, out_dir: Path, prefix: str,
                   reporter: Reporter) -> tuple[str, int, int]:
    """Replace ```mermaid blocks with rendered images, if mermaid-cli is installed.

    Returns the text, the number rendered, and the number left as source.
    """
    mmdc = shutil.which("mmdc")
    lines, out = text.splitlines(), []
    rendered = skipped = 0
    index = 0
    i = 0
    while i < len(lines):
        match = MERMAID_OPEN.match(lines[i])
        if not match:
            out.append(lines[i])
            i += 1
            continue
        marker = match.group(2)
        body, j = [], i + 1
        while j < len(lines) and not re.match(rf"^\s{{0,3}}{marker[0]}{{{len(marker)},}}\s*$",
                                              lines[j]):
            body.append(lines[j])
            j += 1
        index += 1
        if not mmdc:
            skipped += 1
            out.extend(lines[i:j + 1])
        else:
            source = out_dir / f"{prefix}-{index}.mmd"
            image = out_dir / f"{prefix}-{index}.png"
            source.write_text("\n".join(body) + "\n", encoding="utf-8")
            command = [mmdc, "-i", str(source), "-o", str(image), "-b", "white", "-s", "3"]
            try:
                subprocess.run(command, check=True, capture_output=True)
            except (subprocess.CalledProcessError, OSError) as error:
                skipped += 1
                reporter.warn(f"mermaid render failed for {prefix}-{index}: {error}")
                out.extend(lines[i:j + 1])
            else:
                rendered += 1
                out.append("")
                out.append(f"![]({image})")
                out.append("")
        i = j + 1
    return "\n".join(out), rendered, skipped


# --------------------------------------------------------------------------------------------
# Assembling
# --------------------------------------------------------------------------------------------

def page_break_for(engine: str | None) -> str:
    """A page break the chosen engine understands, or nothing.

    Every chapter and every play is meant to be opened on its own, so each one starting on a fresh
    page is worth the small amount of engine-specific output. Raw blocks are only emitted when the
    engine is known, which means ``--format md`` and ``--format html`` stay clean.
    """
    if engine == "typst":
        return "```{=typst}\n#pagebreak(weak: true)\n```\n"
    if engine in TEX_PDF_ENGINES:
        return "```{=latex}\n\\clearpage\n```\n"
    return ""


def collect(parts: list[Part], out_dir: Path, repo_url: str | None, mermaid: bool,
            reporter: Reporter, page_break: str = "") -> tuple[str, list[Chapter], list[Chapter]]:
    by_path = assign_anchors(parts)
    warn = reporter.warn
    written: list[Chapter] = []
    unwritten: list[Chapter] = []
    diagrams_rendered = diagrams_skipped = 0
    chunks: list[str] = []

    for part in parts:
        part_body: list[str] = []
        for chapter in part.chapters:
            if chapter.placeholder:
                unwritten.append(chapter)
                continue
            if not chapter.file.is_file():
                if chapter.written:
                    warn(f"{chapter.path}: marked '{chapter.status}' in the table of contents but "
                         f"the file does not exist")
                unwritten.append(chapter)
                continue
            raw = chapter.file.read_text(encoding="utf-8")
            chapter.words = word_count(raw)
            body = ChapterRewriter(chapter, by_path, repo_url, reporter).run(raw)
            if mermaid:
                body, rendered, skipped = render_mermaid(
                    body, out_dir / "diagrams", chapter.anchor, reporter
                )
                diagrams_rendered += rendered
                diagrams_skipped += skipped
            chapter.text = body
            written.append(chapter)
            # No break before the first chapter of a part: it follows the part heading.
            prefix = page_break if part_body else ""
            part_body.append(prefix + body.strip() + "\n")
        if not part_body:
            continue                                  # a part with nothing written yet is omitted
        chunks.append(page_break + f"# {part.title} {{#{part.anchor}}}\n")
        chunks.extend(part_body)

    if diagrams_skipped:
        reporter.note(f"{diagrams_skipped} mermaid diagram(s) left as source — install "
                      f"mermaid-cli to render them: npm install -g @mermaid-js/mermaid-cli")
    if diagrams_rendered:
        log(f"Rendered {diagrams_rendered} mermaid diagram(s).")

    return "\n\n".join(chunks).rstrip() + "\n", written, unwritten


def draft_note(written: list[Chapter], unwritten: list[Chapter], date: str) -> str:
    if not unwritten:
        return ""
    lines = [
        "# About this build {#about-this-build}",
        "",
        f"This is a draft build of *The Agentic Playbook*, assembled on {date} from the "
        f"repository's own markdown.",
        f"{len(written)} of {len(written) + len(unwritten)} entries in the table of contents are "
        f"written; the rest are listed below and are simply absent from this PDF rather than "
        f"stubbed.",
        "",
    ]
    lines += [f"- {c.title} (`{c.path}`)" for c in unwritten]
    return "\n".join(lines) + "\n"


ANCHOR_ID = re.compile(r"\{#(?P<id>[^}\s]+)\}")
ANCHOR_REF = re.compile(r"\]\(#(?P<id>[^)\s]+)\)")


def dangling_anchors(markdown: str) -> list[str]:
    """Internal links whose target is not in this build — usually a chapter nobody has written."""
    defined: set[str] = set()
    referenced: set[str] = set()
    fences = Fences()
    for line in markdown.splitlines():
        if fences.feed(line) or fences.inside:
            continue
        if line.lstrip().startswith("#"):
            defined.update(match["id"] for match in ANCHOR_ID.finditer(line))
        referenced.update(match["id"] for match in ANCHOR_REF.finditer(line))
    return sorted(referenced - defined)


def unlink(markdown: str, anchors: list[str]) -> str:
    """Turn links to absent anchors back into plain text.

    Forward references to chapters that are not written yet are explicitly allowed in this repo,
    and nine authors work in parallel, so a draft build always has some. Left in place they are a
    hard error in typst and a silently broken link everywhere else; unlinked they read as ordinary
    prose and the reader loses nothing that exists.
    """
    for anchor in anchors:
        markdown = re.sub(rf"\[([^\[\]]*)\]\(#{re.escape(anchor)}\)", r"\1", markdown)
    return markdown


def find_orphans(parts: list[Part]) -> list[str]:
    known = {c.path for part in parts for c in part.chapters}
    orphans = []
    for path in sorted(BOOK.rglob("*.md")):
        relative = path.relative_to(BOOK).as_posix()
        if relative in known or relative in NOT_BOOK_CONTENT:
            continue
        orphans.append(relative)
    return orphans


# --------------------------------------------------------------------------------------------
# Pandoc
# --------------------------------------------------------------------------------------------

def choose_engine(requested: str | None) -> str | None:
    if requested:
        return requested if shutil.which(requested) else None
    return next((engine for engine in PDF_ENGINES if shutil.which(engine)), None)


def pandoc_command(source: Path, output: Path, fmt: str, engine: str | None, date: str,
                   extra: list[str]) -> list[str]:
    command = [
        "pandoc", str(source), "-o", str(output),
        f"--from={PANDOC_FROM}",
        "--standalone",
        "--toc", "--toc-depth=2",
        f"--resource-path={BOOK}:{source.parent}:{ROOT}",
        "--metadata", f"date={date}",
    ]
    if METADATA_FILE.is_file():
        command.append(f"--metadata-file={METADATA_FILE}")
    if fmt == "pdf" and engine:
        command.append(f"--pdf-engine={engine}")
        if engine in TEX_PDF_ENGINES:
            command += ["--top-level-division=chapter",
                        "-V", "documentclass=report",
                        "-V", "geometry:margin=1in",
                        "-V", "colorlinks=true",
                        "-V", "linkcolor=RoyalBlue",
                        "-V", "urlcolor=RoyalBlue"]
        # typst and the HTML engines are configured from book-metadata.yaml instead: typst's
        # `margin` is a map, which the -V flag cannot express.
    return command + extra


def run_pandoc(command: list[str], verbose: bool) -> bool:
    if verbose:
        log("$ " + " ".join(command))
    try:
        result = subprocess.run(command, capture_output=True, text=True)
    except OSError as error:
        log(f"Could not run pandoc: {error}")
        return False
    if result.returncode != 0 and not verbose:
        log("$ " + " ".join(command))          # on failure, show what was actually run
    if result.stderr.strip():
        log(result.stderr.strip())
    return result.returncode == 0


def engine_advice() -> str:
    return (
        "pandoc needs a PDF engine on PATH. Any of these will do:\n"
        "  typst        brew install typst          (recommended — one small binary)\n"
        "  tectonic     brew install tectonic       (self-contained LaTeX)\n"
        "  weasyprint   pipx install weasyprint     (HTML/CSS route)\n"
        "  xelatex      brew install --cask mactex  (full TeX, several GB)\n"
        "Or build HTML instead and print it from a browser:\n"
        "  python3 scripts/build_book.py --format html"
    )


# --------------------------------------------------------------------------------------------
# Reporting
# --------------------------------------------------------------------------------------------

def report(parts: list[Part], written: list[Chapter], unwritten: list[Chapter]) -> None:
    total = sum(c.words for c in written) or 1
    log("")
    log(f"{'Part':<34}{'files':>7}{'words':>9}{'share':>8}")
    log("-" * 58)
    for part in parts:
        files = [c for c in part.chapters if c in written]
        if not files:
            continue
        words = sum(c.words for c in files)
        log(f"{part.title[:33]:<34}{len(files):>7}{words:>9}{words / total:>7.0%}")
    log("-" * 58)
    log(f"{'Total':<34}{len(written):>7}{total:>9}")
    if unwritten:
        log(f"{len(unwritten)} table-of-contents entries are not written yet.")


# --------------------------------------------------------------------------------------------
# Entry point
# --------------------------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Collect the book into one file and render it.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="The table of contents in book/README.md decides what is included, and in what "
               "order. A file that is not in it is not in the build.",
    )
    parser.add_argument("--format", choices=["pdf", "html", "md"], default="pdf",
                        help="output format (default: pdf; md needs no external tools)")
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT,
                        help=f"where to write (default: {DEFAULT_OUT.relative_to(ROOT)}/)")
    parser.add_argument("--name", default="agentic-playbook", help="output filename stem")
    parser.add_argument("--pdf-engine", help=f"force an engine ({', '.join(PDF_ENGINES)})")
    parser.add_argument("--repo-url", metavar="URL",
                        help="rewrite links that leave the book (research briefs, plans) to this "
                             "base URL instead of leaving them relative")
    parser.add_argument("--no-mermaid", action="store_true",
                        help="never shell out to mermaid-cli; leave diagrams as source")
    parser.add_argument("--no-draft-note", action="store_true",
                        help="omit the 'About this build' page listing unwritten chapters")
    parser.add_argument("--check", action="store_true",
                        help="report missing and orphaned files and stop, writing nothing")
    parser.add_argument("--strict", action="store_true",
                        help="exit non-zero if any problem is reported (notes do not count)")
    parser.add_argument("--pandoc-arg", action="append", default=[], metavar="ARG",
                        help="pass an extra argument through to pandoc (repeatable)")
    parser.add_argument("--verbose", action="store_true", help="echo the pandoc command")
    args = parser.parse_args(argv)

    if not TOC_FILE.is_file():
        log(f"Cannot find {TOC_FILE}")
        return 2

    building_pdf = args.format == "pdf" and not args.check
    if building_pdf and not shutil.which("pandoc"):
        log("pandoc is not installed: brew install pandoc")
        log("Build the collected markdown instead: python3 scripts/build_book.py --format md")
        return 2

    # Chosen before the markdown is written, because page breaks are engine-specific raw blocks.
    engine = choose_engine(args.pdf_engine) if building_pdf else None
    if building_pdf and engine is None:
        if args.pdf_engine:
            log(f"Requested PDF engine '{args.pdf_engine}' is not on PATH.")
        log(engine_advice())
        return 2

    parts = parse_toc(TOC_FILE.read_text(encoding="utf-8"))
    reporter = Reporter()
    out_dir: Path = args.out_dir
    (out_dir / "diagrams").mkdir(parents=True, exist_ok=True)

    body, written, unwritten = collect(
        parts, out_dir, args.repo_url, not args.no_mermaid, reporter, page_break_for(engine)
    )
    for orphan in find_orphans(parts):
        reporter.warn(f"{orphan}: not in the table of contents, so not in the book")

    if not written:
        log("Nothing to build: no chapter named in the table of contents exists yet.")
        return 1

    date = _datetime.date.today().strftime("%-d %B %Y")
    front = "" if args.no_draft_note else draft_note(written, unwritten, date)
    markdown = (front + "\n" + body) if front else body

    # A link into a chapter nobody has written yet is expected; anything else is a typo.
    pending = {chapter.anchor for chapter in unwritten if chapter.anchor}
    dangling = dangling_anchors(markdown)
    for anchor in dangling:
        if anchor.split("--")[0] in pending:
            reporter.note(f"link to '#{anchor}' points at a chapter that is not written yet; "
                          f"rendered as plain text")
        else:
            reporter.warn(f"link to '#{anchor}' resolves to nothing — check the cross-reference")
    markdown = unlink(markdown, dangling)

    source = out_dir / f"{args.name}.md"
    if not args.check:
        source.write_text(markdown, encoding="utf-8")
        log(f"Wrote {rel(source)} ({len(written)} chapters).")

    report(parts, written, unwritten)
    reporter.print()

    status = 1 if (args.strict and reporter.problems) else 0

    if args.check or args.format == "md":
        return status

    if args.format == "html":
        if not shutil.which("pandoc"):
            log("pandoc is not installed: brew install pandoc")
            return 2
        output = out_dir / f"{args.name}.html"
        command = pandoc_command(source, output, "html", None, date, args.pandoc_arg)
        if not run_pandoc(command, args.verbose):
            return 2
        log(f"Wrote {rel(output)}")
        return status

    output = out_dir / f"{args.name}.pdf"
    log(f"Rendering PDF with {engine}.")
    command = pandoc_command(source, output, "pdf", engine, date, args.pandoc_arg)
    if not run_pandoc(command, args.verbose):
        log("pandoc failed. The collected markdown is still at "
            f"{rel(source)}; try --format html, or another --pdf-engine.")
        return 2
    log(f"Wrote {rel(output)}")
    return status


if __name__ == "__main__":
    sys.exit(main())
