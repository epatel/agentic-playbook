#!/usr/bin/env python3
"""Recapture the two blocks quoted in *Split the brief into cards*.

The odd one out in this directory: the project is this repository. The play's worked example is the
book's own two-tier setup, so there is no fictional tree to ship — `CLAUDE.md` and `cards/` are
copied out of the checkout into a throwaway temporary directory and the commands run there, which
keeps the invocation identical to the one a reader would type at the repository root.

Both blocks in the play are printed verbatim, so both are asserted verbatim. Editing a card or
adding one will fail this script; that is the point, and the fix is to re-run it and paste the new
output into the play. Python 3 standard library only.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]

#: `wc -l CLAUDE.md cards/*.md`, as the play prints it.
EXPECTED_COUNTS = {
    "CLAUDE.md": 62,
    "cards/book-structure.md": 70,
    "cards/building-the-book.md": 316,
    "cards/repo-layout.md": 65,
    "cards/research-notes.md": 65,
    "cards/standing-defaults.md": 76,
}

#: `grep -oE '\\]\\([a-z-]+\\.md\\)' cards/*.md`, as the play prints it. Five links, three files —
#: and the play's claim is that all five are signposts rather than chains, which is a judgement the
#: command cannot make and this script does not pretend to.
EXPECTED_LINKS = [
    "cards/building-the-book.md:](standing-defaults.md)",
    "cards/building-the-book.md:](standing-defaults.md)",
    "cards/repo-layout.md:](building-the-book.md)",
    "cards/standing-defaults.md:](building-the-book.md)",
    "cards/standing-defaults.md:](building-the-book.md)",
]


class CommandFailed(RuntimeError):
    """A captured command exited non-zero, or the book and the tree have drifted apart."""


def run(command: str, cwd: Path) -> str:
    """Echo the command the way the book prints it, echo its stdout verbatim, return it."""
    print("$ " + command)
    result = subprocess.run(command, cwd=cwd, capture_output=True, text=True, shell=True)
    sys.stdout.write(result.stdout)
    sys.stdout.flush()
    if result.stderr:
        sys.stderr.write(result.stderr)
    if result.returncode != 0:
        raise CommandFailed(f"{command} exited {result.returncode}")
    return result.stdout


def scratch_checkout() -> Path:
    """Copy the two tiers out of the repository into a temporary directory."""
    index = REPO / "CLAUDE.md"
    cards = REPO / "cards"
    if not index.is_file() or not cards.is_dir():
        raise CommandFailed(f"no two-tier setup under {REPO}")
    work = Path(tempfile.mkdtemp(prefix="cards-"))
    shutil.copy2(index, work / "CLAUDE.md")
    shutil.copytree(cards, work / "cards")
    return work


def check_counts(output: str) -> None:
    """The play prints these line counts, so a card that changed length invalidates the capture."""
    seen = {}
    for line in output.splitlines():
        count, _, name = line.strip().partition(" ")
        if name and name != "total":
            seen[name] = int(count)
    if seen != EXPECTED_COUNTS:
        raise CommandFailed(f"line counts moved: {seen} != {EXPECTED_COUNTS}")
    index = EXPECTED_COUNTS["CLAUDE.md"]
    cards = sum(v for k, v in EXPECTED_COUNTS.items() if k != "CLAUDE.md")
    if index * 8 > cards:
        raise CommandFailed(f"the two tiers are no longer a tenth and the rest: {index} vs {cards}")


def check_links(output: str) -> None:
    """The self-containment audit. Four links between cards, in three files."""
    found = output.split()
    if found != EXPECTED_LINKS:
        raise CommandFailed(f"links between cards moved: {found} != {EXPECTED_LINKS}")


def main() -> int:
    work = None
    try:
        work = scratch_checkout()
        print("The two tiers, measured\n")
        check_counts(run("wc -l CLAUDE.md cards/*.md", work))
        print("\nThe self-containment audit\n")
        check_links(run(r"grep -oE '\]\([a-z-]+\.md\)' cards/*.md", work))
        print("\n# both blocks match the play")
    except CommandFailed as exc:
        print(f"reproduce.py: {exc}", file=sys.stderr)
        return 1
    finally:
        if work is not None:
            shutil.rmtree(work, ignore_errors=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
