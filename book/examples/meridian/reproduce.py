#!/usr/bin/env python3
"""Capture the real command output behind two plays in Part II.

Builds a throwaway git repository from ``tree/`` and runs, for real:

  * the independent ``rg | awk`` call-site count from *Decompose into subagents*
  * the three ``git worktree add`` commands from *Work in parallel without collisions*
  * the ``comm -12`` overlap preflight from step 4 of the same play

Everything printed below the transcript rules is verbatim process output. Python 3 stdlib
only; ``git``, ``rg``, ``awk`` and ``bash`` must be on PATH.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
TREE = HERE / "tree"

EXPECTED_TOTAL = 52
EXPECTED_WITHOUT_VENDOR = 47

# Fixed identity and timestamps so the commit hash -- which git worktree add echoes -- is
# the same on every machine and every run.
FIXED_ENV = {
    "GIT_AUTHOR_NAME": "Meridian Platform",
    "GIT_AUTHOR_EMAIL": "platform@meridian.example",
    "GIT_AUTHOR_DATE": "2026-07-14T09:00:00+00:00",
    "GIT_COMMITTER_NAME": "Meridian Platform",
    "GIT_COMMITTER_EMAIL": "platform@meridian.example",
    "GIT_COMMITTER_DATE": "2026-07-14T09:00:00+00:00",
    "GIT_CONFIG_GLOBAL": os.devnull,
    "GIT_CONFIG_SYSTEM": os.devnull,
    "LC_ALL": "C",
    "TZ": "UTC",
}

COUNT_PIPELINE = (
    "rg --count-matches 'Billing::Client\\.new' services/ engines/ \\\n"
    "    | awk -F: '{ total += $2 } END { print total }'"
)
BREAKDOWN = "rg --count-matches 'Billing::Client\\.new' services/ engines/ --sort path"
NO_VENDOR_PIPELINE = (
    "rg --count-matches 'Billing::Client\\.new' services/ engines/ \\\n"
    "    -g '!services/tracking/vendor/**' \\\n"
    "    | awk -F: '{ total += $2 } END { print total }'"
)

# Step 4 of *Work in parallel without collisions*. Process substitution needs bash or zsh,
# not plain sh, so this one is run through bash explicitly.
OVERLAP_PREFLIGHT = (
    "comm -12 \\\n"
    '  <(git diff --name-only "origin/main...feat/invoices" | sort) \\\n'
    '  <(git diff --name-only "origin/main...feat/rate-limit" | sort)'
)
OVERLAP_PREFLIGHT_SCRIPT = OVERLAP_PREFLIGHT.replace("\\\n", "")
EXPECTED_OVERLAP = "config/routes.rb"

FAILURES: list[str] = []


def env() -> dict[str, str]:
    merged = dict(os.environ)
    merged.update(FIXED_ENV)
    return merged


def rule(title: str) -> None:
    prefix = f"--- {title} "
    print(prefix + "-" * max(3, 80 - len(prefix)))


def run(argv: list[str], cwd: Path, *, check: bool = True) -> str:
    """Run a command quietly and return its combined output."""
    proc = subprocess.run(
        argv,
        cwd=str(cwd),
        env=env(),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    if check and proc.returncode != 0:
        FAILURES.append(f"{' '.join(argv)} exited {proc.returncode}:\n{proc.stdout}")
    return proc.stdout


def transcript(display: str, argv: list[str], cwd: Path, *, check: bool = True) -> str:
    """Print a shell-style transcript of one command and return its combined output."""
    for i, line in enumerate(display.splitlines()):
        print(f"$ {line}" if i == 0 else line)
    out = run(argv, cwd=cwd, check=check)
    if out:
        sys.stdout.write(out if out.endswith("\n") else out + "\n")
    return out


def shell(display: str, script: str, cwd: Path) -> str:
    return transcript(display, ["/bin/sh", "-c", script], cwd)


def bash(display: str, script: str, cwd: Path) -> str:
    """Same, but through bash — process substitution is not in POSIX sh."""
    return transcript(display, ["/bin/bash", "-c", script], cwd)


def require_tools() -> None:
    missing = [t for t in ("git", "rg", "awk", "bash") if shutil.which(t) is None]
    if missing:
        sys.exit(
            "missing required tool(s) on PATH: "
            + ", ".join(missing)
            + "\ninstall ripgrep (rg) and git, then re-run."
        )
    if not TREE.is_dir():
        sys.exit(f"missing example tree: {TREE}")


def build_repo(root: Path) -> Path:
    repo = root / "meridian"
    shutil.copytree(TREE, repo)
    run(["git", "init", "-q", "-b", "main"], cwd=repo)
    run(["git", "config", "user.name", "Meridian Platform"], cwd=repo)
    run(["git", "config", "user.email", "platform@meridian.example"], cwd=repo)
    run(["git", "config", "commit.gpgsign", "false"], cwd=repo)
    run(["git", "add", "-A"], cwd=repo)
    run(["git", "commit", "-q", "-m", "Round tariff surcharges at the journal boundary"], cwd=repo)
    return repo


def main() -> int:
    require_tools()

    rule("environment")
    for tool, flag in (("git", "--version"), ("rg", "--version"), ("awk", "--version")):
        out = run([tool, flag], cwd=HERE, check=False)
        print(f"$ {tool} {flag}")
        print(out.splitlines()[0] if out.strip() else "(no version output)")
    print()

    root = Path(tempfile.mkdtemp(prefix="meridian-example-"))
    repo = build_repo(root)
    worktrees: list[Path] = []

    try:
        rule("the repository under test")
        transcript("git log --oneline -1", ["git", "log", "--oneline", "-1"], repo)
        transcript(
            "ls services/ | wc -l", ["/bin/sh", "-c", "ls services/ | wc -l"], repo
        )
        print()

        rule("play: decompose-into-subagents -- the independent count")
        total = shell(COUNT_PIPELINE, COUNT_PIPELINE.replace("\\\n", ""), repo).strip()
        print()

        print("Per-file breakdown (path:matches):")
        shell(BREAKDOWN, BREAKDOWN, repo)
        print()

        print("The same count with the vendored directory excluded -- what the four")
        print("scouts between them reported:")
        without_vendor = shell(
            NO_VENDOR_PIPELINE, NO_VENDOR_PIPELINE.replace("\\\n", ""), repo
        ).strip()
        print()

        rule("play: work-in-parallel-without-collisions -- three worktrees")
        for name, branch in (
            ("../meridian-webhooks", "feat/webhooks"),
            ("../meridian-invoices", "feat/invoices"),
            ("../meridian-rate-limit", "feat/rate-limit"),
        ):
            pad = " " * (len("../meridian-rate-limit") - len(name))
            transcript(
                f"git worktree add {name}{pad} -b {branch}",
                ["git", "worktree", "add", name, "-b", branch],
                repo,
            )
            worktrees.append((repo / name).resolve())
        print()
        transcript("git worktree list", ["git", "worktree", "list"], repo)
        print()

        rule("play: work-in-parallel-without-collisions -- the overlap preflight")
        # Give two of the branches a real overlap to find: both touch the shared route
        # table, which is exactly the landmine file the play tells you to serialise.
        run(["git", "update-ref", "refs/remotes/origin/main", "HEAD"], cwd=repo)
        for branch, own_file, line in (
            ("feat/invoices", "services/invoices/README.md", "invoice webhooks"),
            ("feat/rate-limit", "engines/rate_limit/README.md", "rate-limit buckets"),
        ):
            tree = repo.parent / f"meridian-{branch.split('/', 1)[1]}"
            target = tree / own_file
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(f"# {line}\n")
            routes = tree / "config" / "routes.rb"
            routes.write_text(routes.read_text() + f"  # {line}\n")
            run(["git", "add", "-A"], cwd=tree)
            run(["git", "commit", "-q", "-m", f"Add {line}"], cwd=tree)

        overlap = bash(OVERLAP_PREFLIGHT, OVERLAP_PREFLIGHT_SCRIPT, repo).strip()
        print()

        rule("assertions")
        for label, got, want in (
            ("total call sites", total, str(EXPECTED_TOTAL)),
            ("excluding vendor", without_vendor, str(EXPECTED_WITHOUT_VENDOR)),
            ("overlapping file between two branches", overlap, EXPECTED_OVERLAP),
        ):
            ok = got == want
            print(f"{label}: expected {want}, got {got or '(empty)'} -- {'ok' if ok else 'FAIL'}")
            if not ok:
                FAILURES.append(f"{label}: expected {want}, got {got!r}")
        print(f"worktrees created: {len(worktrees)} -- {'ok' if len(worktrees) == 3 else 'FAIL'}")
    finally:
        for path in worktrees:
            run(["git", "worktree", "remove", "--force", str(path)], cwd=repo, check=False)
        shutil.rmtree(root, ignore_errors=True)

    if FAILURES:
        print()
        rule("failures")
        for failure in FAILURES:
            print(failure)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
