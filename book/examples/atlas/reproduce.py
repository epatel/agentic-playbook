#!/usr/bin/env python3
"""Recapture the `wc -l` output quoted in *Write the brief the agent actually reads*.

Each tree is copied into a throwaway temporary directory before anything is measured, so the
commands below are the same ones a reader would type inside a checkout of `atlas` and nothing here
depends on where this repository happens to live. Python 3 standard library only.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent


class CommandFailed(RuntimeError):
    """A captured command exited non-zero; the capture is not trustworthy."""


def run(argv: list[str], cwd: Path) -> None:
    """Echo the command the way the book prints it, then echo its stdout verbatim."""
    print("$ " + " ".join(argv))
    result = subprocess.run(argv, cwd=cwd, capture_output=True, text=True)
    sys.stdout.write(result.stdout)
    sys.stdout.flush()
    if result.stderr:
        sys.stderr.write(result.stderr)
    if result.returncode != 0:
        raise CommandFailed(f"{' '.join(argv)} exited {result.returncode}")


def capture(tree: str, argv: list[str]) -> None:
    """Copy `tree` into a temp directory and run `argv` there, cleaning up afterwards."""
    source = HERE / tree
    if not source.is_dir():
        raise CommandFailed(f"missing tree: {source}")
    scratch = Path(tempfile.mkdtemp(prefix=f"atlas-{tree}-"))
    try:
        work = scratch / "atlas"
        shutil.copytree(source, work)
        run(argv, work)
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


def platform_line() -> str:
    """`wc` ships no version flag, so date the capture by the kernel it ran on."""
    result = subprocess.run(["uname", "-sr"], capture_output=True, text=True)
    if result.returncode != 0:
        raise CommandFailed(f"uname -sr exited {result.returncode}")
    uname = result.stdout.strip()
    flavour = "BSD wc" if uname.startswith("Darwin") else "GNU coreutils wc"
    return f"# captured on {uname} using {flavour}; column padding differs between the two"


def main() -> int:
    try:
        print("before/ — the brief as it stood at 18 months\n")
        capture("before", ["wc", "-l", "CLAUDE.md"])
        print("\nafter/ — the same brief pruned, plus the vendor import shim\n")
        capture("after", ["wc", "-l", "AGENTS.md", "CLAUDE.md"])
        print()
        print(platform_line())
    except CommandFailed as exc:
        print(f"reproduce.py: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
