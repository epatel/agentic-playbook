#!/usr/bin/env python3
"""Check that a rewrite kept every fact: each figure, quotation, link and code block that a chapter
had at a git ref must still be in it now.

Written for the consolidated rewrite of September 2026, which reshapes sentences across the whole
book and must not move a single number. The 23 September figure re-check spent a day re-opening
sources by hand; this replaces the part of that job a machine can do. It does not judge whether a
figure is still attached to the right claim. It only proves that nothing disappeared, which is the
failure a sentence-level rewrite actually produces.

Nothing here writes to the book. It reports, and with ``--strict`` it exits non-zero.

Usage
-----

    make facts                                   # every chapter against main, --strict
    make facts REF=pre-consolidated-rewrite      # against the tag taken before the rewrite
    python3 scripts/check_facts.py --ref main book/preface.md   # one file

What it compares, per file, between ``REF`` and the working tree:

* a **problem**, which fails ``--strict``:
  - a number written in digits (``51.3%``, ``1,023``, ``2005``), outside links and code;
  - a quotation in double quotes, compared with its whitespace collapsed, so rewrapping is free;
  - a link target;
  - a fenced block other than a diagram, compared verbatim.
* a **note**, which never fails:
  - a number written as a word (``fifteen``, ``a dozen``). Those legitimately vanish when a
    sentence is recast ("three ways" becomes a heading), so a person decides;
  - a changed mermaid diagram. Its labels are prose, and the sentence rules apply to them.

A file that did not exist at ``REF`` is skipped: it has nothing to lose.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_book import BOOK, ROOT, Fences, Reporter, rel  # noqa: E402

#: Spelled-out numbers worth a second look. "one" is left out: it is a pronoun far more often than
#: a count, and flagging it would bury the notes that matter.
NUMBER_WORDS = (
    "two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen "
    "sixteen seventeen eighteen nineteen twenty thirty forty fifty sixty seventy eighty ninety "
    "hundred thousand million dozen half quarter"
).split()

LINK_TARGET = re.compile(r"\]\(\s*(<[^>]*>|[^)\s]+)")
INLINE_CODE = re.compile(r"`[^`]*`")
QUOTE = re.compile(r"[\"“]([^\"“”]{2,600})[\"”]")
NUMBER = re.compile(r"(?<![\w.])\d+(?:[.,]\d+)*%?")
NUMBER_WORD = re.compile(r"\b(" + "|".join(NUMBER_WORDS) + r")\b", re.IGNORECASE)


def split(text: str) -> tuple[str, list[str]]:
    """Return the prose with fenced blocks removed, and the fenced blocks themselves."""
    fences, prose, blocks, current = Fences(), [], [], []
    for line in text.splitlines():
        edge = fences.feed(line)
        if edge or fences.inside:
            current.append(line)
            if edge and not fences.inside:             # the closing fence
                blocks.append("\n".join(current))
                current = []
            continue
        prose.append(line)
    return "\n".join(prose), blocks


def facts(text: str) -> dict[str, set[str]]:
    """Everything in one version of a chapter that a rewrite must not lose."""
    prose, blocks = split(text)
    flat = " ".join(prose.split())                      # rewrapping never counts as a change
    links = set(LINK_TARGET.findall(flat))
    bare = INLINE_CODE.sub(" ", LINK_TARGET.sub("](", flat))
    return {
        "number": set(NUMBER.findall(bare)),
        "quotation": {" ".join(q.split()) for q in QUOTE.findall(bare)},
        "link": links,
        "code block": set(blocks),
        "number word": {w.lower() for w in NUMBER_WORD.findall(bare)},
    }


def at_ref(ref: str, path: Path) -> str | None:
    """The file's text at ``ref``, or None if it did not exist there."""
    result = subprocess.run(["git", "show", f"{ref}:{path.relative_to(ROOT).as_posix()}"],
                            cwd=ROOT, capture_output=True, text=True)
    return result.stdout if result.returncode == 0 else None


def chapters(paths: list[str]) -> list[Path]:
    found: list[Path] = []
    for name in paths or [str(BOOK)]:
        path = Path(name).resolve()
        found.extend(sorted(path.rglob("*.md")) if path.is_dir() else [path])
    return [p for p in found if "examples" not in p.relative_to(ROOT).parts]


def check(path: Path, ref: str, reporter: Reporter) -> None:
    before = at_ref(ref, path)
    if before is None:
        return
    old, new = facts(before), facts(path.read_text(encoding="utf-8"))
    for kind, items in old.items():
        for item in sorted(items - new[kind]):
            diagram = kind == "code block" and "mermaid" in item.splitlines()[0]
            shown = item if kind != "code block" else item.splitlines()[0] + " …"
            message = f"{rel(path)}: {kind} at {ref} is gone: {shown}"
            (reporter.note if kind == "number word" or diagram else reporter.warn)(message)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("paths", nargs="*", help="files or directories to check (default: book/)")
    parser.add_argument("--ref", default="main", help="git ref to compare against (default: main)")
    parser.add_argument("--strict", action="store_true",
                        help="exit non-zero if anything was lost (notes do not count)")
    args = parser.parse_args()

    reporter = Reporter()
    files = chapters(args.paths)
    for path in files:
        check(path, args.ref, reporter)
    print(f"Compared {len(files)} markdown files against {args.ref}: numbers, quotations, links "
          f"and code blocks.")
    reporter.print()
    if not reporter.problems and not reporter.notes:
        print("Nothing lost.")
    return 1 if (args.strict and reporter.problems) else 0


if __name__ == "__main__":
    sys.exit(main())
