#!/usr/bin/env python3
"""Check the book's mechanical conventions: wrapping, whitespace, fences, bans, and word budgets.

Four writing tasks wrote their own throwaway version of this in /tmp before it was written down
once. The rules it checks are the ones a machine can decide — the column limit, trailing
whitespace, a fenced block with no language tag, the bans in ``book/STYLE.md`` that are a fixed
list of characters or words, and the word budgets in ``book/STYLE.md`` and
``book/TEMPLATE-play.md``. Everything about voice stays where it belongs, which is a person
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

Three traps this was written around, all found the hard way:

* **Column counts are ``len()`` on a ``str``.** A byte-oriented ``awk length()`` overcounts every
  em dash by two, and this prose is full of them.
* **A fence is not always code.** Mermaid diagrams legitimately run past the column limit, and a
  ``---`` inside a ```` ```markdown ```` fence is sample content rather than YAML frontmatter.
  Fenced blocks are skipped by every rule that would otherwise mangle them.
* **Words are counted by the build's own counter**, imported rather than reimplemented. ``wc -w``
  and counting by eye both run 1–4% high against it, because it excludes fenced blocks, headings,
  table rows and block quotes — which at these margins is the difference between "48 over" and
  "67 over".
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

# The fence state machine, the word counter, the two-severity reporter and the path formatting
# are the build's, so that "inside a fenced block" and "a word" each mean the same thing to the
# checker and to the thing that renders the book. ``word_count`` in particular is the counter
# ``make check`` reports per part, and a second one would disagree with it by a percent or two —
# which is exactly the margin the budgets are decided on. sys.path[0] is this directory whichever
# directory the script is run from.
from build_book import BOOK, NOT_BOOK_DIRS, Fences, Reporter, log, rel, word_count

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

# --------------------------------------------------------------------------------------------
# Word budgets
# --------------------------------------------------------------------------------------------

STYLE_MD = "book/STYLE.md"
TEMPLATE_MD = "book/TEMPLATE-play.md"


@dataclass(frozen=True)
class Budget:
    """One range from `book/STYLE.md`'s *Length* or `book/TEMPLATE-play.md`.

    The numbers are copied here rather than parsed out of the prose that states them: both
    documents write their budgets in sentences, and a regular expression over English is a worse
    contract than a constant with its source named. What keeps the copy honest is ``--self-test``,
    which checks that every range below is still printed by the file it came from — so moving a
    number in `book/STYLE.md` fails the self-test instead of silently leaving this script
    enforcing last month's budget.
    """

    what: str        # how the thing is named in a report
    low: int
    high: int
    source: str
    unit: str = "words"

    @property
    def span(self) -> str:
        """The range as the source document prints it: an en dash, and thousands separated."""
        return f"{self.low:,}–{self.high:,}"


#: `book/STYLE.md`, *Length*: "a Part I chapter runs 800–1,500 words, a suite opener 150–300, a
#: Part III chapter 800–1,500". Part IV, the appendices and the preface are deliberately absent —
#: no budget is stated for them anywhere, and inventing one here would be this script legislating
#: rather than checking.
CHAPTER = Budget("the chapter", 800, 1500, STYLE_MD)
OPENER = Budget("the suite opener", 150, 300, STYLE_MD)

#: `book/TEMPLATE-play.md`, *Length*: "A play runs 600–1,200 words including its example." It is
#: named "the whole play" rather than "the play" because a play also has a section called *The
#: play*, and the two are reported one line apart when a play is over on both.
PLAY = Budget("the whole play", 600, 1200, TEMPLATE_MD)

#: `book/TEMPLATE-play.md`, *The contract, heading by heading*. The keys are the five headings
#: verbatim and in order — the template forbids rewording or reordering them, so this dict is
#: also the check that they are all there. *Checklist* is the one counted in items rather than
#: words ("**4–8 items.**"), and *Worked example*'s "plus blocks" is free: ``word_count`` does
#: not count fenced blocks in the first place.
PLAY_SECTIONS = {
    "Problem": Budget("*Problem*", 60, 120, TEMPLATE_MD),
    "The play": Budget("*The play*", 200, 500, TEMPLATE_MD),
    "Worked example": Budget("*Worked example*", 150, 400, TEMPLATE_MD),
    "Failure mode": Budget("*Failure mode*", 80, 200, TEMPLATE_MD),
    "Checklist": Budget("*Checklist*", 4, 8, TEMPLATE_MD, unit="items"),
}

#: Which directory under ``book/`` means which budget. Everything else — `book/part-4-next-waves`,
#: `book/appendices`, `preface.md`, and the three constraint documents — has no stated budget and
#: is not counted.
CHAPTER_DIRS = {"part-1-argument", "part-3-where-it-struggles"}
PLAYS_DIR = "part-2-plays"

HEADING = re.compile(r"^##\s+(\S.*?)\s*$")
CHECKLIST_ITEM = re.compile(r"^\s*- \[[ xX]\]")


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


def budget_role(path: Path) -> str | None:
    """Which budget a file is under, from where it sits in ``book/``, or None for no budget.

    The book's own layout is the only signal there is: a chapter of Part I or Part III, a suite
    opener, or a play. A file outside ``book/`` — a card, this plan, a research brief — has no
    stated budget and is never counted, so pointing the checker at a path outside the book still
    does the right thing.
    """
    try:
        parts = path.resolve().relative_to(BOOK).parts
    except ValueError:
        return None
    if len(parts) == 2 and parts[0] in CHAPTER_DIRS:
        return "chapter"
    if len(parts) == 3 and parts[0] == PLAYS_DIR:
        return "opener" if parts[2] == "index.md" else "play"
    return None


def overrun(count: int, budget: Budget) -> str | None:
    """How far outside the budget, phrased for a report, or None if it is inside it."""
    if count > budget.high:
        return f"{count - budget.high:,} over"
    if count < budget.low:
        return f"{budget.low - count:,} under"
    return None


def budget_message(count: int, budget: Budget) -> str | None:
    distance = overrun(count, budget)
    if distance is None:
        return None
    return (f"{budget.what} is {count:,} {budget.unit}, {distance} the "
            f"{budget.span} budget ({budget.source})")


def play_sections(lines: list[str], prose: list[str | None]) -> list[tuple[int, str, list[str]]]:
    """Split a play on its ``##`` headings. Returns (line number, heading, body lines).

    ``prose`` carries the fence mask from the caller, so a ``##`` inside a fenced sample is
    sample content rather than a section of the play. That is not hypothetical: *Build the
    working agreement* prints a whole one-page agreement with seven ``##`` headings in it, and
    counting those as sections would report the best-behaved play in the book for having the
    wrong headings.
    """
    starts = []
    for number, line in enumerate(lines, start=1):
        heading = HEADING.match(line) if prose[number - 1] is not None else None
        if heading:
            starts.append((number, heading.group(1)))
    sections = []
    for index, (number, title) in enumerate(starts):
        end = starts[index + 1][0] - 1 if index + 1 < len(starts) else len(lines)
        sections.append((number, title, lines[number:end]))
    return sections


def budget_defects(path: Path, lines: list[str], prose: list[str | None]) -> list[Defect]:
    """Every word budget that applies to this file, counted with the build's own counter.

    All of these are **problems**, and that is the second half of a decision taken in two steps.
    `023ba519cdd0` reported them as notes because eleven overruns already existed and making them
    problems would have handed every unrelated edit a red build it had inherited. `bfc99c593aeb`
    trimmed all eleven, and promoted them here: the book is inside every budget, so an overrun is
    now something an edit introduced rather than something it found. The regression this catches is
    the one that filed the trim — 45 words of legitimate cross-reference added to a section already
    at its ceiling, by a task that had no reason to suspect it. A note would not have stopped it.

    The cost is real and was accepted: the trimmed plays sit 1–7 words under a 500-word ceiling, so
    a clarifying clause reddens the build. That is the point — the clause still goes in, and
    something else comes out in the same edit.
    """
    role = budget_role(path)
    if role is None:
        return []
    defects: list[Defect] = []

    def note(line_no: int, message: str, rule: str = "budget") -> None:
        defects.append(Defect(path, line_no, rule, message, problem=True))

    text = "\n".join(lines)
    whole = {"chapter": CHAPTER, "opener": OPENER, "play": PLAY}[role]
    message = budget_message(word_count(text), whole)
    if message:
        note(1, message)
    if role != "play":
        return defects

    sections = play_sections(lines, prose)
    if [title for _, title, _ in sections] != list(PLAY_SECTIONS):
        note(1, "headings are not the five in `book/TEMPLATE-play.md`, verbatim and in order, "
                "so the per-section budgets were not counted", rule="play-headings")
        return defects

    for number, title, body in sections:
        budget = PLAY_SECTIONS[title]
        if budget.unit == "items":
            count = sum(1 for offset, line in enumerate(body)
                        if prose[number + offset] is not None and CHECKLIST_ITEM.match(line))
        else:
            count = word_count("\n".join(body))
        message = budget_message(count, budget)
        if message:
            note(number, message)
    return defects


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

    # Pass two: the book's own words, with quotations taken out of them, and the word budgets —
    # which need the fence mask from pass one and nothing from the line-by-line rules below.
    voice = mask_quotations(prose)
    defects.extend(budget_defects(path, lines, prose))
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

# The budget fixtures are generated rather than written out, because a fixture that trips a
# 500-word ceiling has to contain 501 words and nobody would read it. ``word`` is one word to
# ``word_count``; ``- [ ] an item`` is one checklist item.


def filler(words: int) -> str:
    return " ".join(["word"] * words)


def play_fixture(problem: int, play: int, example: int, failure: int, items: int,
                 play_heading: str = "The play") -> str:
    """A play whose five sections are exactly the sizes asked for."""
    return "\n".join([
        "# A fixture play", "",
        "## Problem", "", filler(problem), "",
        f"## {play_heading}", "", filler(play), "",
        "## Worked example", "", filler(example), "",
        "## Failure mode", "", filler(failure), "",
        "## Checklist", "", *["- [ ] an item"] * items, "",
    ])


#: Where each budget fixture has to live for ``budget_role`` to give it a budget at all. None of
#: these files exists; the role comes from the path, and the text is passed in.
PLAY_PATH = BOOK / PLAYS_DIR / "suite" / "a-fixture-play.md"
OPENER_PATH = BOOK / PLAYS_DIR / "suite" / "index.md"
CHAPTER_PATH = BOOK / "part-1-argument" / "a-fixture-chapter.md"
NO_BUDGET_PATH = BOOK / "appendices" / "a-fixture-appendix.md"


def budget_self_test() -> list[str]:
    """The word budgets, including the two cases that decide whether the rule is usable.

    A section one word outside its budget is reported (the margins are the whole point), and a
    file the book states no budget for is not (Part IV, the appendices and the preface are not
    silently given one). Since `bfc99c593aeb` a budget defect is a **problem**, so this also
    asserts the severity: a note would leave the check advisory and the regression it exists to
    catch would land green.
    """
    failures = []

    def budget_notes(path: Path, text: str) -> list[tuple[int, str]]:
        defects = check_text(path, text)
        if any(not d.problem and d.rule in ("budget", "play-headings") for d in defects):
            failures.append(f"{rel(path)}: a budget defect was reported as a note, not a problem")
        return sorted((d.line, d.rule) for d in defects
                      if d.rule in ("budget", "play-headings"))

    # One under the 60-word floor, one over the 500-word ceiling, one over the 8-item ceiling,
    # and two sections comfortably inside. The whole play is 905 words, inside its 600–1,200.
    expected = [(3, "budget"), (7, "budget"), (19, "budget")]
    got = budget_notes(PLAY_PATH, play_fixture(59, 501, 200, 100, 9))
    if got != expected:
        failures.append(f"play budgets: expected {expected}, got {got}")

    # Exactly on both ends of every budget is inside it, which is what "150–400" means.
    got = budget_notes(PLAY_PATH, play_fixture(60, 500, 400, 80, 8))
    if got:
        failures.append(f"a play on its budget boundaries was reported: {got}")

    # A reworded heading means the sections cannot be identified, so they are not counted — and
    # the reader is told that rather than left with a play that quietly checks nothing.
    got = budget_notes(PLAY_PATH, play_fixture(59, 501, 200, 100, 9, play_heading="The Play"))
    if got != [(1, "play-headings")]:
        failures.append(f"a play with a reworded heading: expected one note, got {got}")

    for path, text, expected_lines in (
        (OPENER_PATH, f"# An opener\n\n{filler(100)}\n", [(1, "budget")]),
        (OPENER_PATH, f"# An opener\n\n{filler(200)}\n", []),
        (CHAPTER_PATH, f"# A chapter\n\n{filler(1501)}\n", [(1, "budget")]),
        (CHAPTER_PATH, f"# A chapter\n\n{filler(1200)}\n", []),
        (NO_BUDGET_PATH, f"# An appendix\n\n{filler(4000)}\n", []),
    ):
        got = budget_notes(path, text)
        if got != expected_lines:
            failures.append(f"{rel(path)} at this length: expected {expected_lines}, got {got}")
    return failures


def budget_source_test() -> list[str]:
    """Every budget above is still printed by the document it was copied from.

    This is the whole reason the numbers may be hard-coded. `book/STYLE.md` and
    `book/TEMPLATE-play.md` state their budgets in sentences; parsing them would be a regular
    expression over English. Checking that the range still appears verbatim costs four lines and
    turns "somebody moved a number and this script is now enforcing last month's budget" into a
    failing self-test.
    """
    failures = []
    for budget in (CHAPTER, OPENER, PLAY, *PLAY_SECTIONS.values()):
        source = BOOK.parent / budget.source
        if not source.exists():
            failures.append(f"{budget.source} is missing, so its budgets cannot be confirmed")
        elif budget.span not in source.read_text(encoding="utf-8"):
            failures.append(f"{budget.source} no longer says {budget.span} for {budget.what}: "
                            f"update the constant in this file, or the document")
    return failures


def self_test() -> int:
    """Check the checker. No dependencies, so it runs anywhere the book does."""
    failures = budget_self_test() + budget_source_test()
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
        f"{LIMIT} columns, book/STYLE.md, and the word budgets in book/STYLE.md and "
        f"book/TEMPLATE-play.md.")
    reporter.print()
    if not defects:
        log("No defects.")
    return 1 if (args.strict and reporter.problems) else 0


if __name__ == "__main__":
    sys.exit(main())
