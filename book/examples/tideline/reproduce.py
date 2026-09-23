#!/usr/bin/env python3
"""Rebuild the `tideline` scratch repository and run the commands the book shows.

`tideline` is the fictional TypeScript service that carries the Verification and Trust
suite's worked examples. This script materialises two commits — `main/` as it stood, and
`agent/` as the agent left it — into a throwaway git repository, then runs the exact
commands printed in the book and echoes their real output.

Nothing here writes outside a temporary directory. Run it from anywhere:

    python3 book/examples/tideline/reproduce.py

Exit status is non-zero if any command fails or if a shape the book asserts is no longer
true.
"""

from __future__ import annotations

import os
import shutil
import stat
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent

# A fixed identity and a fixed date, so commit hashes are the same on every machine.
GIT_ENV = {
    **os.environ,
    "GIT_CONFIG_GLOBAL": os.devnull,
    "GIT_CONFIG_SYSTEM": os.devnull,
    "GIT_AUTHOR_NAME": "tideline",
    "GIT_AUTHOR_EMAIL": "tideline@example.invalid",
    "GIT_COMMITTER_NAME": "tideline",
    "GIT_COMMITTER_EMAIL": "tideline@example.invalid",
    "GIT_AUTHOR_DATE": "2026-09-01T09:00:00+00:00",
    "GIT_COMMITTER_DATE": "2026-09-01T09:00:00+00:00",
    "LC_ALL": "C",
}

FAILURES: list[str] = []


def run(cmd: str, cwd: Path, *, check: bool = True) -> str:
    """Run a shell command and return its combined output."""
    proc = subprocess.run(
        cmd,
        cwd=cwd,
        shell=True,
        env=GIT_ENV,
        capture_output=True,
        text=True,
    )
    if check and proc.returncode != 0:
        FAILURES.append(f"{cmd} exited {proc.returncode}: {proc.stderr.strip()}")
    return (proc.stdout + proc.stderr).rstrip("\n")


def show(cmd: str, cwd: Path, *, check: bool = True) -> str:
    """Run a command and print it as a transcript the way the book prints it."""
    for i, line in enumerate(cmd.split("\n")):
        print(f"$ {line}" if i == 0 else line)
    out = run(cmd, cwd, check=check)
    if out:
        print(out)
    return out


def heading(text: str) -> None:
    print()
    print(f"--- {text} " + "-" * max(0, 78 - len(text)))


def copy_tree(src: Path, dst: Path) -> None:
    for entry in src.iterdir():
        target = dst / entry.name
        if entry.is_dir():
            shutil.copytree(entry, target, dirs_exist_ok=True)
        else:
            shutil.copy2(entry, target)


def build_repo(repo: Path) -> None:
    """Two commits: `origin/main`, then the agent's branch on top of it."""
    repo.mkdir(parents=True, exist_ok=True)
    run("git init -q -b main", repo)
    run("git config user.name tideline", repo)
    run("git config user.email tideline@example.invalid", repo)

    copy_tree(HERE / "main", repo)
    run("git add -A", repo)
    run('git commit -q -m "Stage rollouts by battery eligibility"', repo)
    base = run("git rev-parse HEAD", repo)

    # The book's commands use `origin/main...HEAD`. Point a remote-tracking ref at the
    # base commit rather than inventing a network remote.
    run(f"git update-ref refs/remotes/origin/main {base}", repo)

    run("git switch -q -c feat/percentage-cohorts", repo)
    for entry in repo.iterdir():
        if entry.name == ".git":
            continue
        shutil.rmtree(entry) if entry.is_dir() else entry.unlink()
    copy_tree(HERE / "agent", repo)
    run("git add -A", repo)
    run('git commit -q -m "Add percentage-gated cohorts"', repo)


def build_trailer_history(repo: Path) -> None:
    """400 commits whose trailers were written by an editor default, not by a person.

    This backs *Decide who signs off*, where the first move is to ask what the history
    is already asserting about authorship.
    """
    repo.mkdir(parents=True, exist_ok=True)
    run("git init -q -b main", repo)
    run("git config user.name tideline", repo)
    run("git config user.email tideline@example.invalid", repo)

    log = repo / "CHANGELOG.md"
    lines: list[str] = []
    for i in range(400):
        lines.append(f"- change {i:03d}\n")
        log.write_text("".join(lines))
        run("git add -A", repo)
        # Two commits in three carry the editor's default co-author trailer; a handful
        # carry a hand-written one; the rest carry nothing.
        if i % 3 != 2:
            trailer = "\n\nCo-authored-by: Cursor Agent <agent@cursor.com>"
        elif i % 17 == 0:
            trailer = "\n\nReviewed-by: Priya Raman <priya@tideline.example>"
        else:
            trailer = ""
        run(f'git commit -q -m "change {i:03d}{trailer}"', repo)


def main() -> int:
    scratch = Path(tempfile.mkdtemp(prefix="tideline-example-"))
    try:
        heading("environment")
        show("git --version", scratch)
        show("rg --version | head -1", scratch)

        repo = scratch / "tideline"
        build_repo(repo)

        heading("play: review-code-you-did-not-write")
        print("\nThe whole change, before anything is read:")
        whole = show("git diff --stat origin/main...HEAD", repo)

        print("\nStep 1 — the things that check the code, read before the code:")
        stat_out = show(
            "git diff --stat origin/main...HEAD -- tests/ tsconfig.json .github/", repo
        )

        print("\nStep 2 — what the pipeline lost:")
        show("git diff origin/main...HEAD -- .github/workflows/ci.yml", repo)

        print("\nStep 3 — what happened to an existing test:")
        show(
            "git diff origin/main...HEAD -- tests/rollout.spec.ts | rg '^[-+] *it[.(]'",
            repo,
        )

        print("\nStep 4 — one search, before reading the new module:")
        rg_out = show("rg -l --sort path --type ts 'bucketFor|hashToBucket' src/", repo)

        heading("play: make-the-agent-prove-it")
        print("\nThe deterministic stop gate, run by hand against this change:")
        show(
            "git diff --name-only --diff-filter=DM origin/main -- tests/",
            repo,
        )
        print("\nMaking the suite read-only for the run:")
        show("chmod -R a-w tests/ && ls -ld tests/", repo)
        run("chmod -R u+w tests/", repo)

        heading("play: decide-who-signs-off")
        trailers = scratch / "tideline-history"
        build_trailer_history(trailers)
        print("\nWhat the repository is already asserting about authorship:")
        trailer_out = show(
            "git log --format='%(trailers:only)' -n 400 | grep . | sort | uniq -c | sort -rn",
            trailers,
        )

        heading("assertions")
        checks = [
            ("nine files in the change", "9 files changed" in whole),
            ("three rows in the gate-first stat", "3 files changed" in stat_out),
            (
                "both bucketing helpers present in src/",
                "assign.ts" in rg_out and "schedule.ts" in rg_out,
            ),
            (
                "an editor default dominates the trailers",
                "Co-authored-by: Cursor Agent" in trailer_out,
            ),
        ]
        ok = True
        for label, passed in checks:
            print(f"{label}: {'ok' if passed else 'FAILED'}")
            ok = ok and passed

        for failure in FAILURES:
            print(f"command failed: {failure}", file=sys.stderr)

        return 0 if ok and not FAILURES else 1
    finally:
        def force_writable(func, path, _exc):
            os.chmod(path, stat.S_IWUSR | stat.S_IRUSR | stat.S_IXUSR)
            func(path)

        shutil.rmtree(scratch, onexc=force_writable)


if __name__ == "__main__":
    sys.exit(main())
