#!/usr/bin/env python3
"""Paired run: the same seeded-bug tasks with and without a token-filtering tool.

The filter is any settings fragment passed to Claude Code with --settings. `rtk` is the built-in
preset (--filter rtk, the default); any other tool is --filter path/to/settings.json.

Three modes, in the order you should use them:

    python3 run.py check-tasks          # free: every seeded bug applies and breaks the suite
    python3 run.py preflight            # cents: the hook fires in one arm and not the other
    python3 run.py run --out results/2026-09-23

`run` resumes: a run id already in results.jsonl is skipped, so an interrupted
matrix picks up where it stopped. See README.md for the protocol this implements.
Python 3 standard library only.
"""

import argparse
import json
import os
import random
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
TASKS = json.loads((HERE / "tasks.json").read_text())
CACHE = Path(os.environ.get("FILTER_PAIRED_CACHE", Path.home() / ".cache" / "filter-paired-run"))
PRESETS = {
    # Exactly what `rtk init --global` installs. `report` is the tool's own per-directory account
    # of what it saved, kept beside the measured bill; a custom filter has none.
    "rtk": {
        "settings": {"hooks": {"PreToolUse": [
            {"matcher": "Bash", "hooks": [{"type": "command", "command": "rtk hook claude"}]}]}},
        "mcp": None,
        "report": ["rtk", "gain", "-p", "-f", "json"],
        "recalls": ["rtk", "gain", "-p", "--recalls"],
    },
}


def load_filter(name):
    if name in PRESETS:
        return {"name": name, **PRESETS[name]}
    path = Path(name)
    if not path.exists():
        sys.exit(f"--filter {name}: not a preset ({', '.join(PRESETS)}) and not a settings file")
    spec = json.loads(path.read_text())
    # Either a bare settings fragment, or {"settings": {...}, "mcpServers": {...}} for a tool that
    # runs as an MCP server. The server is passed with --mcp-config, so --strict-mcp-config still
    # keeps every other server out of both arms.
    if "settings" in spec or "mcpServers" in spec:
        return {"name": path.stem, "settings": spec.get("settings", {}),
                "mcp": spec.get("mcpServers"), "report": None, "recalls": None}
    return {"name": path.stem, "settings": spec, "mcp": None, "report": None, "recalls": None}
PYTEST = [sys.executable, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", "tests"]


def sh(cmd, cwd=None, env=None, check=True, timeout=None):
    return subprocess.run(
        cmd, cwd=cwd, env=env, check=check, timeout=timeout, text=True, capture_output=True
    )


def source_tree():
    """A pristine checkout of the pinned commit, cloned once and reused."""
    src = CACHE / "source"
    if not src.exists():
        CACHE.mkdir(parents=True, exist_ok=True)
        sh(["git", "clone", "--quiet", TASKS["repo"], str(src)])
    sh(["git", "checkout", "--quiet", TASKS["commit"]], cwd=src)
    head = sh(["git", "rev-parse", "HEAD"], cwd=src).stdout.strip()
    if head != TASKS["commit"]:
        sys.exit(f"source is at {head}, expected {TASKS['commit']}")
    return src


def make_workdir(parent, task):
    """Copy the tree without its history, seed the bug, commit it as the only commit.

    No history means `git log -p` cannot hand the agent the fix.
    """
    repo = Path(parent) / "repo"
    shutil.copytree(source_tree(), repo, ignore=shutil.ignore_patterns(".git"))
    if task and task.get("old"):
        path = repo / task["file"]
        text = path.read_text()
        if text.count(task["old"]) != 1:
            sys.exit(f"{task['id']}: seed string found {text.count(task['old'])} times, need 1")
        path.write_text(text.replace(task["old"], task["new"]))
    stamp = "2026-01-01T00:00:00"
    env = {**os.environ, "GIT_AUTHOR_DATE": stamp, "GIT_COMMITTER_DATE": stamp}
    sh(["git", "init", "--quiet"], cwd=repo)
    sh(["git", "add", "-A"], cwd=repo)
    sh(["git", "-c", "user.name=bench", "-c", "user.email=bench@example.invalid",
        "commit", "--quiet", "-m", "initial"], cwd=repo, env=env)
    return repo


def suite_passes(repo):
    return sh(PYTEST, cwd=repo, check=False, timeout=600).returncode == 0


def check_tasks(_args):
    with tempfile.TemporaryDirectory() as tmp:
        base = make_workdir(Path(tmp) / "baseline", None)
        if not suite_passes(base):
            sys.exit("the unmodified suite fails; nothing below would mean anything")
        print(f"baseline  {TASKS['ref']} suite passes")
    bad = 0
    for task in TASKS["tasks"]:
        with tempfile.TemporaryDirectory() as tmp:
            repo = make_workdir(tmp, task)
            broken = not suite_passes(repo)
            print(f"{'ok  ' if broken else 'FAIL'}      {task['id']}: seeded bug "
                  f"{'breaks' if broken else 'does NOT break'} the suite")
            bad += not broken
    sys.exit(1 if bad else 0)


def claude_cmd(prompt, arm, args):
    cmd = [
        "claude", "-p", prompt,
        "--output-format", "stream-json", "--verbose",
        "--model", args.model,
        "--effort", args.effort_level,
        "--max-turns", str(args.max_turns),
        "--dangerously-skip-permissions",   # throwaway copy in a temp dir, nothing else reachable
        "--strict-mcp-config",
        "--setting-sources", "project",
    ]
    if arm == "on":
        cmd += ["--settings", json.dumps(args.filter_spec["settings"])]
        if args.filter_spec["mcp"]:
            cmd += ["--mcp-config", json.dumps({"mcpServers": args.filter_spec["mcp"]})]
    return cmd


def run_one(task, arm, effort, rep, args, out):
    run_id = f"{task['id']}__{effort}__r{rep}__{arm}"
    with tempfile.TemporaryDirectory(prefix="filterpair-") as tmp:
        repo = make_workdir(tmp, task)
        config = Path(tmp) / "config"
        config.mkdir()
        env = {k: v for k, v in os.environ.items() if not k.startswith("CLAUDE_CODE_")}
        env["CLAUDE_CONFIG_DIR"] = str(config)   # no user settings, plugins, CLAUDE.md or memory
        args.effort_level = effort
        prompt = task.get("prompt") or TASKS["prompt_template"].format(report=task["report"])
        started = time.time()
        try:
            proc = sh(claude_cmd(prompt, arm, args), cwd=repo, env=env, check=False,
                      timeout=args.timeout)
            stdout, timed_out = proc.stdout, False
        except subprocess.TimeoutExpired as exc:
            stdout, timed_out = (exc.stdout or ""), True
        wall = time.time() - started
        (out / "transcripts" / f"{run_id}.jsonl").write_text(stdout)

        events = [json.loads(l) for l in stdout.splitlines() if l.strip().startswith("{")]
        result = next((e for e in reversed(events) if e.get("type") == "result"), {})
        bash_calls = sum(
            1 for e in events if e.get("type") == "assistant"
            for block in e.get("message", {}).get("content", [])
            if block.get("type") == "tool_use" and block.get("name") == "Bash"
        )

        tests_touched = bool(sh(["git", "status", "--porcelain", "--", "tests"], cwd=repo).stdout)
        sh(["git", "checkout", "--quiet", "HEAD", "--", "tests"], cwd=repo)
        sh(["git", "clean", "-fdq", "--", "tests"], cwd=repo)
        passed = suite_passes(repo)                # judged against the original tests only

        spec = args.filter_spec
        report, recalls = None, ""
        if spec["report"]:
            raw = sh(spec["report"], cwd=repo, check=False).stdout
            try:
                report = json.loads(raw)["summary"]
            except (ValueError, KeyError):
                report = {"unparsed": raw}
            recalls = sh(spec["recalls"], cwd=repo, check=False).stdout

    return {
        "run_id": run_id, "task": task["id"], "arm": arm, "effort": effort, "rep": rep,
        "model_requested": args.model, "passed": passed, "tests_touched": tests_touched,
        "timed_out": timed_out, "wall_s": round(wall, 1), "bash_calls": bash_calls,
        "num_turns": result.get("num_turns"), "subtype": result.get("subtype"),
        "harness_cost_usd": result.get("total_cost_usd"),
        "usage": result.get("usage"), "model_usage": result.get("modelUsage"),
        "filter": args.filter_spec["name"], "filter_report": report, "filter_recalls": recalls,
        "finished": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
    }


def versions():
    def v(cmd):
        return sh(cmd, check=False).stdout.strip() or sh(cmd, check=False).stderr.strip()
    return {
        "claude": v(["claude", "--version"]), "rtk": v(["rtk", "--version"]),
        "python": sys.version.split()[0], "pytest": v([sys.executable, "-m", "pytest", "--version"]),
        "platform": sys.platform, "task_commit": TASKS["commit"],
    }


def require_key():
    if not os.environ.get("ANTHROPIC_API_KEY"):
        sys.exit("set ANTHROPIC_API_KEY — ideally a key created for this test alone, so the "
                 "console's per-key spend is the bill to reconcile against")


def preflight(args):
    """One trivial run per arm: the hook must fire in 'on' and must not fire in 'off'."""
    require_key()
    if not args.filter_spec["report"]:
        sys.exit(f"filter '{args.filter_spec['name']}' has no self-report, so the preflight cannot "
                 "see whether it fired. Check one transcript from each arm by hand instead.")
    task = {"id": "preflight",
            "prompt": "Nothing is broken. Run `git status` and `ls more_itertools`, then reply DONE."}
    args.max_turns, failures = 5, 0
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp)
        (out / "transcripts").mkdir()
        for arm in ("off", "on"):
            rec = run_one(task, arm, args.efforts[0], 0, args, out)
            cmds = (rec["filter_report"] or {}).get("total_commands", 0)
            ok = (cmds > 0) if arm == "on" else (cmds == 0)
            failures += not ok
            print(f"{'ok  ' if ok else 'FAIL'}  arm={arm:3}  filter rewrote {cmds} command(s), "
                  f"turns={rec['num_turns']}, harness cost=${rec['harness_cost_usd']}")
    sys.exit(1 if failures else 0)


def run(args):
    require_key()
    out = Path(args.out)
    (out / "transcripts").mkdir(parents=True, exist_ok=True)
    results = out / "results.jsonl"
    done = set()
    if results.exists():
        done = {json.loads(l)["run_id"] for l in results.read_text().splitlines() if l.strip()}
    meta = out / "meta.json"
    if not meta.exists():
        meta.write_text(json.dumps({**versions(), "filter": args.filter_spec["name"],
                                    "filter_settings": args.filter_spec["settings"],
                                    "model": args.model, "efforts": args.efforts,
                                    "reps": args.reps, "seed": args.seed,
                                    "max_turns": args.max_turns, "started": time.strftime("%F %T %z")},
                                   indent=2) + "\n")

    wanted = [t for t in TASKS["tasks"] if not args.tasks or t["id"] in args.tasks]
    units = [(t, e, r) for t in wanted for e in args.efforts for r in range(1, args.reps + 1)]
    rng = random.Random(args.seed)
    rng.shuffle(units)                       # spread every task across the whole session
    plan = []
    for t, e, r in units:
        arms = ["off", "on"]
        rng.shuffle(arms)                    # neither arm always goes first
        plan += [(t, a, e, r) for a in arms]

    todo = [p for p in plan if f"{p[0]['id']}__{p[2]}__r{p[3]}__{p[1]}" not in done]
    print(f"{len(plan)} runs planned, {len(plan) - len(todo)} already done, {len(todo)} to go")
    for i, (task, arm, effort, rep) in enumerate(todo, 1):
        rec = run_one(task, arm, effort, rep, args, out)
        with results.open("a") as f:
            f.write(json.dumps(rec) + "\n")
        print(f"[{i}/{len(todo)}] {rec['run_id']:45} pass={rec['passed']!s:5} "
              f"turns={rec['num_turns']} ${rec['harness_cost_usd']} {rec['wall_s']}s")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="mode", required=True)
    sub.add_parser("check-tasks")
    for name in ("preflight", "run"):
        s = sub.add_parser(name)
        s.add_argument("--filter", default="rtk",
                       help="a preset name (rtk) or a settings JSON file that installs the filter")
        s.add_argument("--model", default="claude-sonnet-5")
        s.add_argument("--efforts", default="low,high", type=lambda v: v.split(","))
        s.add_argument("--max-turns", type=int, default=60)
        s.add_argument("--timeout", type=int, default=1200, help="seconds per run")
        if name == "run":
            s.add_argument("--out", required=True)
            s.add_argument("--reps", type=int, default=3)
            s.add_argument("--seed", type=int, default=20260923)
            s.add_argument("--tasks", type=lambda v: v.split(","), default=None,
                           help="comma-separated task ids; default all twelve")
    args = p.parse_args()
    if args.mode != "check-tasks":
        args.filter_spec = load_filter(args.filter)
    {"check-tasks": check_tasks, "preflight": preflight, "run": run}[args.mode](args)


if __name__ == "__main__":
    main()
