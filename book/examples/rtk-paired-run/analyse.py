#!/usr/bin/env python3
"""Analyse a paired run. Implements the analysis README.md fixes in advance.

    python3 analyse.py results/2026-09-23

Cost is computed from token counts and the dated per-million prices in PRICES, not taken from
the harness's own estimate, which is printed alongside for comparison only. Every model that
appears in the results must have a PRICES row, or the script stops and names it.
Python 3 standard library only.
"""

import json
import random
import sys
from collections import defaultdict
from pathlib import Path
from statistics import mean

# USD per million tokens. Fill in from the vendor's pricing page and date it; the date goes into
# the book next to any figure derived from it. Cache writes are priced at the five-minute rate.
PRICES_DATE = "2026-09-19"
PRICES = {
    "claude-sonnet-4-6": {"input": 3.00, "output": 15.00, "cache_write": 3.75, "cache_read": 0.30},
    # "claude-sonnet-5": {...},   # add before analysing a run made with it
}
BOOTSTRAP = 10_000
METRICS = ["cost", "fresh_input", "cache_read", "cache_write", "output", "turns", "wall_s",
           "bash_calls"]


def tokens(rec):
    """Per-model token counts, preferring modelUsage (it splits out subagent models)."""
    mu = rec.get("model_usage") or {}
    if mu:
        return {m: {"input": u.get("inputTokens", 0), "output": u.get("outputTokens", 0),
                    "cache_read": u.get("cacheReadInputTokens", 0),
                    "cache_write": u.get("cacheCreationInputTokens", 0)} for m, u in mu.items()}
    u = rec.get("usage") or {}
    return {rec["model_requested"]: {
        "input": u.get("input_tokens", 0), "output": u.get("output_tokens", 0),
        "cache_read": u.get("cache_read_input_tokens", 0),
        "cache_write": u.get("cache_creation_input_tokens", 0)}}


def price_for(model):
    for key, p in PRICES.items():
        if model == key or model.startswith(key):
            return p
    return None


def flatten(rec):
    per_model = tokens(rec)
    missing = [m for m in per_model if price_for(m) is None]
    if missing:
        sys.exit(f"no PRICES row for {', '.join(missing)} — add it, dated, and re-run")
    row = {"fresh_input": 0, "cache_read": 0, "cache_write": 0, "output": 0, "cost": 0.0}
    for model, t in per_model.items():
        p = price_for(model)
        row["fresh_input"] += t["input"]
        row["cache_read"] += t["cache_read"]
        row["cache_write"] += t["cache_write"]
        row["output"] += t["output"]
        row["cost"] += sum(t[k] * p[k] for k in ("input", "output", "cache_read", "cache_write")) / 1e6
    row.update(turns=rec.get("num_turns") or 0, wall_s=rec["wall_s"],
               bash_calls=rec["bash_calls"], passed=bool(rec["passed"]),
               harness_cost=rec.get("harness_cost_usd") or 0.0,
               rtk_saved=(rec.get("rtk") or {}).get("total_saved", 0),
               rtk_commands=(rec.get("rtk") or {}).get("total_commands", 0),
               recalled="No recall activity" not in (rec.get("rtk_recalls") or "No recall activity"),
               tests_touched=rec.get("tests_touched", False), timed_out=rec.get("timed_out", False))
    return row


def change(on, off, tasks, metric):
    """Percentage change of the summed metric, on relative to off, across a set of tasks."""
    a = sum(on[t][metric] for t in tasks)
    b = sum(off[t][metric] for t in tasks)
    return (a / b - 1) * 100 if b else float("nan")


def bootstrap_ci(on, off, metric, rng):
    tasks = sorted(on)
    draws = sorted(change(on, off, [rng.choice(tasks) for _ in tasks], metric)
                   for _ in range(BOOTSTRAP))
    return draws[int(0.025 * BOOTSTRAP)], draws[int(0.975 * BOOTSTRAP) - 1]


def main():
    out = Path(sys.argv[1] if len(sys.argv) > 1 else "results")
    meta = json.loads((out / "meta.json").read_text())
    recs = [json.loads(l) for l in (out / "results.jsonl").read_text().splitlines() if l.strip()]
    rng = random.Random(meta.get("seed", 0))

    runs = defaultdict(dict)                    # (task, effort, rep) -> arm -> row
    for r in recs:
        runs[(r["task"], r["effort"], r["rep"])][r["arm"]] = flatten(r)
    pairs = {k: v for k, v in runs.items() if {"on", "off"} <= v.keys()}

    print(f"# rtk paired run — {out.name}\n")
    print(f"claude {meta['claude']} · rtk {meta['rtk']} · model {meta['model']} · "
          f"tasks at {meta['task_commit'][:12]} · prices dated {PRICES_DATE}")
    print(f"{len(pairs)} complete pairs; {len(runs) - len(pairs)} unpaired runs ignored\n")

    for effort in sorted({k[1] for k in pairs}):
        on, off = defaultdict(list), defaultdict(list)
        for (task, eff, _rep), arms in pairs.items():
            if eff == effort:
                on[task].append(arms["on"])
                off[task].append(arms["off"])
        n_tasks = len(on)
        reps = min(len(v) for v in on.values())
        per_task = lambda side: {t: {m: mean(r[m] for r in rows) for m in METRICS}
                                 for t, rows in side.items()}
        on_m, off_m = per_task(on), per_task(off)

        print(f"## Effort: {effort} — {n_tasks} tasks × {reps}+ reps per arm")
        if n_tasks < 12 or reps < 3:
            print("\n> Pilot-sized. Use it to estimate variance and cost, not to update the book.")

        print("\n| Condition | Fresh input | Cache reads | Output | Turns | Tasks passed |")
        print("|---|---|---|---|---|---|")
        for label, side, rows in (("Without filter", off_m, off), ("With filter", on_m, on)):
            passed = sum(r["passed"] for v in rows.values() for r in v)
            total = sum(len(v) for v in rows.values())
            print(f"| {label} | {mean(s['fresh_input'] for s in side.values()):,.0f} | "
                  f"{mean(s['cache_read'] for s in side.values()):,.0f} | "
                  f"{mean(s['output'] for s in side.values()):,.0f} | "
                  f"{mean(s['turns'] for s in side.values()):.1f} | {passed}/{total} |")
        print("\nMeans per task. The table has the columns *Starve the context* leaves blank.\n")

        print("| Measure, with filter vs without | Change | 95% CI (tasks resampled) |")
        print("|---|---|---|")
        cis = {}
        for m in METRICS:
            lo, hi = bootstrap_ci(on_m, off_m, m, rng)
            cis[m] = (change(on_m, off_m, sorted(on_m), m), lo, hi)
            print(f"| {m} | {cis[m][0]:+.1f}% | {lo:+.1f}% to {hi:+.1f}% |")

        flat_on = [r for v in on.values() for r in v]
        flat_off = [r for v in off.values() for r in v]
        pass_on = mean(r["passed"] for r in flat_on) * 100
        pass_off = mean(r["passed"] for r in flat_off) * 100
        cpp = lambda rows: sum(r["cost"] for r in rows) / max(1, sum(r["passed"] for r in rows))
        rtk_saved = sum(r["rtk_saved"] for r in flat_on)
        measured = sum(r["fresh_input"] + r["cache_read"] + r["cache_write"] for r in flat_on) - \
            sum(r["fresh_input"] + r["cache_read"] + r["cache_write"] for r in flat_off)

        print(f"\n- Pass rate: {pass_off:.0f}% without, {pass_on:.0f}% with")
        print(f"- Cost per passed run: ${cpp(flat_off):.4f} without, ${cpp(flat_on):.4f} with")
        print(f"- rtk's own report over the 'with' runs: {rtk_saved:,} tokens saved, "
              f"{sum(r['rtk_commands'] for r in flat_on)} commands rewritten")
        print(f"- Measured change in input tokens of every kind, with minus without: "
              f"{measured:+,}")
        print(f"- 'With' runs where rtk recorded an agent re-fetching elided output: "
              f"{sum(r['recalled'] for r in flat_on)}/{len(flat_on)}")
        print(f"- Harness cost estimate, summed: ${sum(r['harness_cost'] for r in flat_off):.2f} "
              f"without, ${sum(r['harness_cost'] for r in flat_on):.2f} with — reconcile the "
              f"total against the console before quoting any of this")
        leaks = sum(r["rtk_commands"] > 0 for r in flat_off)
        touched = sum(r["tests_touched"] for r in flat_on + flat_off)
        if leaks:
            print(f"- **Isolation failed:** rtk rewrote commands in {leaks} 'without' runs. "
                  f"Discard this effort level.")
        if touched:
            print(f"- {touched} runs edited tests/; they were judged against the original tests")

        # The decision rule, fixed in README.md before any run.
        pct, lo, hi = cis["cost"]
        print("\n**Verdict on cost:** ", end="")
        if lo > 0:
            print(f"more expensive with the filter, {pct:+.1f}% (95% CI {lo:+.1f}% to {hi:+.1f}%).")
        elif hi < 0:
            print(f"cheaper with the filter, {pct:+.1f}% (95% CI {lo:+.1f}% to {hi:+.1f}%).")
        else:
            print(f"no measurable difference on this task set; {pct:+.1f}%, "
                  f"95% CI {lo:+.1f}% to {hi:+.1f}%.")
        if abs(pass_on - pass_off) >= 10:
            print("Pass rates differ by ten points or more, so the cost comparison is between "
                  "unequal outcomes; lead with the pass rate.")
        print()


if __name__ == "__main__":
    main()
