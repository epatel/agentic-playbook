#!/usr/bin/env python3
"""Check the book's mechanical conventions: wrapping, whitespace, fences, and the outright bans.

Four writing tasks wrote their own throwaway version of this in /tmp before it was written down
once. The rules it checks are the ones a machine can decide — the column limit, trailing
whitespace, a fenced block with no language tag, the bans in ``book/STYLE.md`` that are a fixed
list of characters or words. Everything about voice stays where it belongs, which is a person
reading the prose.

Nothing here writes to the book. It reports, and with ``--strict`` it exits non-zero.

Usage
-----

    make lint                                      # what `make check` runs: book/, --strict
    python3 scripts/check_style.py                 # the same, without failing on a problem
    python3 scripts/check_style.py book cards plans  # any file or directory, not just the book
    python3 scripts/check_style.py --self-test     # check the checker, after changing a rule

Two severities, the same two the build uses:

* a **problem** is a defect: it fails ``--strict`` and someone should fix it;
* a **note** wants a human's eye, because the rule has legitimate exceptions — a quotation from a
  source that spells things the American way is not a defect in this book's prose.

Two traps this was written around, both found the hard way:

* **Column counts are ``len()`` on a ``str``.** A byte-oriented ``awk length()`` overcounts every
  em dash by two, and this prose is full of them.
* **A fence is not always code.** Mermaid diagrams legitimately run past the column limit, and a
  ``---`` inside a ```` ```markdown ```` fence is sample content rather than YAML frontmatter.
  Fenced blocks are skipped by every rule that would otherwise mangle them.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

# The fence state machine, the two-severity reporter and the path formatting are the build's, so
# that "inside a fenced block" means the same thing to the checker and to the thing that renders
# the book. sys.path[0] is this directory whichever directory the script is run from.
from build_book import BOOK, NOT_BOOK_DIRS, Fences, Reporter, log, rel

#: `cards/standing-defaults.md`. Not a soft target: parallel authors merge into one book, and
#: line-scoped diffs are what makes that survivable.
LIMIT = 100

#: `book/STYLE.md`, *Banned outright*. Each is a fixed string rather than a judgement, which is
#: the only reason they are in here and the rest of that section is not.
HYPE = re.compile(
    r"\b(revolutionary|game[ -]?chang(?:er|ing)|supercharg\w*|seamless\w*|effortless\w*"
    r"|magical|paradigm shift|next[ -]level|superpower\w*|10x|unlock\w*)\b",
    re.IGNORECASE,
)

#: `book/STYLE.md`, *Mechanics*: British English, `-ise` endings. Reported as a note rather than a
#: problem — the book quotes American sources verbatim, and a quotation is not a spelling defect.
IZE = re.compile(r"\b(\w{3,}iz(?:e|es|ed|ing|ation|ations|er|ers))\b", re.IGNORECASE)

#: Spelled with a z in British English too. Anything built on *size* — resize, oversized,
#: unsized — is the whole family, and `assize` is the only other one this book is likely to meet.
IZE_ALLOWED = re.compile(r"(siz(e|es|ed|ing)|assizes?)$", re.IGNORECASE)

#: Emoji and pictographic dingbats. Deliberately narrow: arrows, ×, ², Θ, curly quotes and em
#: dashes are punctuation this book uses on purpose, and a range wide enough to catch them would
#: make the rule unusable.
EMOJI = re.compile("[\U0001f000-\U0001faff☀-➿⬀-⯿️]")

#: The build's table-of-contents status column. These three are protocol rather than prose — the
#: build reads them to decide what is in the book, and `book/README.md`, the cards and the plan
#: all have to print them to explain the table — so they are never reported.
STATUS_MARKERS = "✅🟡⬜"

#: `book/TEMPLATE-play.md`: captured output is marked on the line above its fence, in this shape.
#: The convention became mechanical when milestone 17 backed every capture with a committed
#: project, so it is checked here rather than remembered.
CAPTURED_PREFIX = re.compile(r"^>\s*Captured\b")
CAPTURED = re.compile(r"^>\s+Captured (?:early |mid |late )?[A-Z][a-z]+ \d{4}, .+\.$")

#: A line that is nothing but one link, give or take the punctuation around it. The longest play
#: titles and the deepest suite paths exceed the budget together and neither half can be wrapped,
#: so these are exempt from the column limit by an explicit decision rather than by whoever hit
#: one first switching the rule off. Two links on a line is a different case: that one can be
#: split, so it is not exempt.
LINK = re.compile(r"!?\[[^\]]*\]\([^)\s]+\)")
DECORATION = re.compile(r"^[\s()\[\]{}.,;:!?·—–*_>+-]*$")

#: `book/STYLE.md`: fenced blocks always carry a language tag.
KNOWN_FENCE_INFO = re.compile(r"^[A-Za-z]")

INLINE_CODE = re.compile(r"`[^`\n]*`")
LINK_TARGET = re.compile(r"\]\([^)\s]*\)")
AUTOLINK = re.compile(r"<https?://[^>\s]*>")

#: The document that defines the bans has to quote them. `book/STYLE.md` prints an exclamation
#: mark, an emoji, the whole hype list and four failing sample paragraphs on purpose; running the
#: ban rules over it would report the style guide for being the style guide. The wrapping and
#: whitespace rules still apply to it.
BANS_EXEMPT = {"STYLE.md"}


@dataclass
class Defect:
    path: Path
    line: int
    rule: str
    message: str
    problem: bool = True

    def render(self) -> str:
        return f"{rel(self.path)}:{self.line}: {self.message} [{self.rule}]"


def visible_prose(line: str) -> str:
    """Strip the parts of a line that are not the book's own words.

    Inline code, link targets and autolinks carry identifiers, paths and URLs the author did not
    write as prose — ``optimization`` in somebody else's URL is not an American spelling in this
    book.
    """
    line = INLINE_CODE.sub(" ", line)
    line = AUTOLINK.sub(" ", line)
    return LINK_TARGET.sub("]", line)


def mask_quotations(prose: list[str | None]) -> list[str | None]:
    """Blank out the inside of double-quoted spans, paragraph by paragraph.

    The vocabulary rules are about *this book's* voice. A quotation is somebody else's, and the
    book quotes American sources verbatim on purpose — ``"optimizing single LLM calls"`` and
    Anthropic's ``"…test cases!"`` are both correct as printed, and reporting them would train the
    next author to ignore the checker.

    A quotation wraps across lines, so the state is carried within a paragraph and reset at every
    blank line. If a paragraph's quotes do not balance, nothing in it is masked: guessing where an
    unterminated quotation ends would hide real defects for the rest of the file. Only the
    straight ``"`` is handled, which is the only one the book uses.
    """
    masked = list(prose)
    paragraph: list[int] = []

    def flush() -> None:
        if not paragraph or sum(masked[i].count('"') for i in paragraph) % 2:
            return
        inside = False
        for index in paragraph:
            characters = []
            for character in masked[index]:
                if character == '"':
                    inside = not inside
                    characters.append(" ")
                else:
                    characters.append(" " if inside else character)
            masked[index] = "".join(characters)

    for index, line in enumerate(masked):
        if line is None or not line.strip():
            flush()
            paragraph = []
        else:
            paragraph.append(index)
    flush()
    return masked


def unwrappable(line: str) -> bool:
    """True if no amount of rewrapping would bring the line under the limit.

    A bare URL or a long path is one token: breaking it changes it. A line that is one markdown
    link and nothing but punctuation is the same case — the link text and the target are each
    unbreakable, and together they exceed the budget for the deepest suite paths.
    """
    stripped = line.strip()
    if not stripped:
        return False
    if len(LINK.findall(line)) == 1 and DECORATION.match(LINK.sub("", line)):
        return True
    indent = len(line) - len(line.lstrip())
    return indent + max(len(token) for token in stripped.split()) > LIMIT


def check_text(path: Path, text: str) -> list[Defect]:
    """Every rule for one file. Fenced blocks are classified first; nothing else looks inside."""
    defects: list[Defect] = []

    def problem(line_no: int, rule: str, message: str) -> None:
        defects.append(Defect(path, line_no, rule, message))

    def note(line_no: int, rule: str, message: str) -> None:
        defects.append(Defect(path, line_no, rule, message, problem=False))

    lines = text.split("\n")
    if text and not text.endswith("\n"):
        problem(len(lines), "final-newline", "file does not end with a newline")
    elif text.endswith("\n\n"):
        problem(len(lines) - 1, "final-newline", "file ends with a blank line")
    if not text.strip():
        return defects
    # ``split`` leaves an empty element after the final newline; it is not a line of the file.
    if lines and lines[-1] == "":
        lines.pop()

    if lines[0].strip() == "---":
        problem(1, "frontmatter", "YAML frontmatter: GitHub renders it as a stray table")

    # Pass one: which lines are inside a fence. A mermaid diagram may be 120 columns wide, a
    # ```markdown sample may open with a `---` that is not frontmatter, and captured output is
    # whatever the machine printed. None of the rules below belongs in there.
    fences, fence_opened_at = Fences(), 0
    prose: list[str | None] = []
    for number, line in enumerate(lines, start=1):
        delimiter = fences.feed(line)
        if delimiter and fences.inside:
            fence_opened_at = number
            if not KNOWN_FENCE_INFO.match(fences.info):
                problem(number, "untagged-fence",
                        "fenced block has no language tag (bash, text, markdown, json, python, "
                        "mermaid)")
        prose.append(None if (delimiter or fences.inside) else visible_prose(line))
    if fences.inside:
        defects.append(Defect(path, fence_opened_at, "unclosed-fence",
                              "fenced block is never closed"))

    # Pass two: the book's own words, with quotations taken out of them.
    voice = mask_quotations(prose)
    check_bans = path.name not in BANS_EXEMPT

    # Pass three: the rules.
    for number, line in enumerate(lines, start=1):
        if line != line.rstrip():
            problem(number, "trailing-whitespace", "trailing whitespace")
        if prose[number - 1] is None:
            continue

        stripped = line.strip()
        width = len(line)
        if width > LIMIT and not stripped.startswith("|") and not unwrappable(line):
            problem(number, "long-line", f"{width} columns (limit {LIMIT})")

        if CAPTURED_PREFIX.match(stripped):
            if not CAPTURED.match(stripped):
                problem(number, "captured",
                        "capture line is not `> Captured <Month Year>, <tool> <version>.`")
            following = next((nxt for nxt in lines[number:] if nxt.strip()), "")
            if not following.strip().startswith(("```", "~~~")):
                problem(number, "captured", "capture line does not sit above a fenced block")

        if not check_bans:
            continue
        for match in EMOJI.finditer(line):
            if match.group() in STATUS_MARKERS:
                continue
            problem(number, "emoji", f"emoji {match.group()!r}")
        spoken = voice[number - 1].replace("![", "")
        if "!" in spoken:
            problem(number, "exclamation", "exclamation mark")
        for match in HYPE.finditer(spoken):
            problem(number, "hype", f"hype vocabulary: {match.group()!r}")
        for match in IZE.finditer(spoken):
            if not IZE_ALLOWED.search(match.group()):
                note(number, "ize", f"American spelling: {match.group()!r} (the book uses -ise)")

    return defects


def markdown_files(targets: list[Path]) -> list[Path]:
    """Every markdown file under the targets, minus the apparatus the build also skips.

    ``book/examples/`` holds the scratch projects the worked examples were captured from. One of
    them is a deliberately terrible ``CLAUDE.md``, and another is a rules file whose frontmatter
    is the point, so linting them as prose reports the fixtures for being fixtures. Naming the
    path on the command line checks it anyway.
    """
    files: list[Path] = []
    for target in targets:
        if target.is_file():
            files.append(target)
            continue
        for path in sorted(target.rglob("*.md")):
            if path.relative_to(target).as_posix().startswith(NOT_BOOK_DIRS):
                continue
            files.append(path)
    return files


# --------------------------------------------------------------------------------------------
# Self-test
# --------------------------------------------------------------------------------------------

#: The rules in one file, including every trap that cost somebody an afternoon. Each expectation
#: below is a line number in this fixture, so the fixture is also the documentation.
FIXTURE = '''\
# A fixture

An em dash — and another — on a line that is exactly one hundred columns wide when measured aaaaaaaa
An em dash — and another — on a line that is one hundred and one columns wide when measured aaaaaaaaa
This one has trailing whitespace.\x20
[*A play with a very long title indeed*](../part-2-plays/verification-and-trust/review-code-you-did-not-write.md).
See [*one*](../a/b/c.md) and [*two*](../d/e/f.md), which is two links on one line and could therefore have been split.

```mermaid
graph TD
    A[A mermaid node whose label runs a long way past one hundred columns, which is allowed and must not be reported] --> B[End]
```

```markdown
---
title: sample frontmatter inside a markdown sample, which is content rather than a header
---
```

```
echo "a fenced block with no language tag"
```

This is revolutionary, seamless, and will 10x your workflow!

Anthropic's prompt says "please, do not write dedicated code to pass the test cases!", which is
quoted, so it is not this book's exclamation mark, and "optimizing" here is not a spelling defect.

We should standardize on this, and the emoji 😬 has to go.

> Captured Septembre 2026, git 2.50.1

Prose, not a fence.
'''

#: ``(line, rule)`` for every problem the fixture must produce, and nothing else. What is *not*
#: in here is half the point: line 3 is exactly 100 columns of em-dashed prose, line 6 is a
#: 114-column line that is one link, and line 11 is a 128-column mermaid node. All three are
#: legitimate, and each of them was reported by somebody's throwaway version of this script.
EXPECTED_PROBLEMS = [
    (4, "long-line"),            # 101 columns, counted as characters rather than bytes
    (5, "trailing-whitespace"),
    (7, "long-line"),            # two links on one line: wrappable, so not exempt
    (20, "untagged-fence"),
    (24, "exclamation"),
    (24, "hype"),
    (24, "hype"),
    (24, "hype"),
    (29, "emoji"),
    (31, "captured"),            # the month is not a month
    (31, "captured"),            # and there is no fence under it
]

#: Line 26 quotes an exclamation mark and line 27 quotes an American spelling. Neither is a
#: defect, because neither is the book talking.
EXPECTED_NOTES = [(29, "ize")]


def self_test() -> int:
    """Check the checker. No dependencies, so it runs anywhere the book does."""
    failures = []
    defects = check_text(Path("fixture.md"), FIXTURE)
    problems = sorted((d.line, d.rule) for d in defects if d.problem)
    notes = sorted((d.line, d.rule) for d in defects if not d.problem)
    if problems != sorted(EXPECTED_PROBLEMS):
        failures.append(f"problems: expected {sorted(EXPECTED_PROBLEMS)}, got {problems}")
    if notes != sorted(EXPECTED_NOTES):
        failures.append(f"notes: expected {sorted(EXPECTED_NOTES)}, got {notes}")

    # The em-dash trap, stated as an assertion rather than as a comment: two em dashes are two
    # columns to Python and six bytes to awk, which is how a line that is exactly at the limit
    # gets reported as 104.
    at_limit = FIXTURE.split("\n")[2]
    if len(at_limit) != LIMIT:
        failures.append(f"fixture line 3 is {len(at_limit)} columns, not {LIMIT}")
    if len(at_limit.encode()) <= LIMIT:
        failures.append("fixture line 3 has no multi-byte characters, so it tests nothing")

    frontmatter = check_text(Path("fixture.md"), "---\ntitle: real frontmatter\n---\n\n# Title\n")
    if not any(d.rule == "frontmatter" for d in frontmatter):
        failures.append("frontmatter at the top of a file was not reported")

    for failure in failures:
        log(f"  - {failure}")
    log(f"self-test: {'FAILED' if failures else 'passed'}")
    return 1 if failures else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Check the book's mechanical conventions. Writes nothing.",
        epilog="Voice is not checked here. Read book/STYLE.md for the part that needs a person.",
    )
    parser.add_argument("paths", nargs="*", type=Path, default=[BOOK],
                        help=f"files or directories to check (default: {rel(BOOK)}/)")
    parser.add_argument("--strict", action="store_true",
                        help="exit non-zero if any problem is reported (notes do not count)")
    parser.add_argument("--self-test", action="store_true",
                        help="run the rules against a fixture of known defects and stop")
    args = parser.parse_args(argv)

    if args.self_test:
        return self_test()

    targets = [Path(p) for p in args.paths]
    missing = [t for t in targets if not t.exists()]
    if missing:
        for target in missing:
            log(f"Cannot find {target}")
        return 2

    files = markdown_files(targets)
    if not files:
        log("No markdown files to check.")
        return 2

    reporter = Reporter()
    defects: list[Defect] = []
    for path in files:
        defects.extend(check_text(path, path.read_text(encoding="utf-8")))
    for defect in sorted(defects, key=lambda d: (rel(d.path), d.line)):
        (reporter.warn if defect.problem else reporter.note)(defect.render())

    log(f"Checked {len(files)} markdown file{'s' if len(files) != 1 else ''} against "
        f"{LIMIT} columns and book/STYLE.md.")
    reporter.print()
    if not defects:
        log("No defects.")
    return 1 if (args.strict and reporter.problems) else 0


if __name__ == "__main__":
    sys.exit(main())
