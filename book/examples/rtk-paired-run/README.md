# `rtk-paired-run` — does the hook lower the bill?

A paired run that re-tests the book's claims about `rtk` on the version people now have installed.
Unlike every other project in this directory, it **calls a paid API and spends money**, and it
writes its results to a directory you name rather than only to a temporary one.

```
python3 book/examples/rtk-paired-run/run.py check-tasks
python3 book/examples/rtk-paired-run/run.py preflight
python3 book/examples/rtk-paired-run/run.py run --out book/examples/rtk-paired-run/results/<date>
python3 book/examples/rtk-paired-run/analyse.py book/examples/rtk-paired-run/results/<date>
```

## What it would update

| Where | The claim today |
|---|---|
| [*Starve the context*](../../part-2-plays/context/starve-the-context.md#worked-example) | "Two independent benchmarks measured `rtk` v0.43.0 in mid-2026; nothing has re-tested it since", and a results table left blank on purpose |
| [`notes/research/token-filtering.md`](../../../notes/research/token-filtering.md) | Under *Contradictions and gaps*: the benchmarks tested v0.43.0, the current version is v0.49.0, and nothing re-tests it |

The published evidence is JetBrains (425 billed trials, Claude Code 2.1.201: cost per task +7.6% at
low effort, +0.1% at high, turns +13.8%, quality tied) and Quesma (1,740 attempts on Terminal-Bench
2.1: 3% cheaper per pass with one model, 7% dearer with another). Both are cited in the research
note. This run adds a third data point on a newer version. It does not overrule either.

## The question, fixed before any run

Everything in this section was written before the first paid run, and the analysis script
implements it as written. Changing it after seeing results is the thing it exists to prevent. If
it has to change, say so in the results and say why.

**Primary outcome.** Cost per task, computed from the token counts each run reports multiplied by
the vendor's dated per-million prices. Not the harness's own dollar figure, and not `rtk gain`.
Reported as the percentage change with the filter against without, per effort level, with a 95%
confidence interval from resampling tasks (10,000 draws).

**Secondary outcomes.** Turns; fresh input, cache reads, cache writes, and output tokens; wall
time; Bash calls; pass rate; cost per passed run; `rtk`'s own tokens-saved figure over the same
runs, set beside the measured change in input tokens; and the number of runs in which `rtk`
recorded the agent re-fetching output it had cut.

**Decision rule.**

- The interval lies entirely above zero: the filter made this task set more expensive, by the
  printed amount.
- The interval lies entirely below zero: it made it cheaper.
- The interval crosses zero: no measurable difference *at this sample size*. This is not "no
  effect", and the interval's width is reported with it.
- Pass rates differing by ten percentage points or more: the costs being compared bought different
  outcomes, so the pass rate is reported first.
- Any "without" run in which `rtk` rewrote a command means the arms leaked into each other.
  Discard that effort level.

## Design

**Tasks.** Twelve bugs seeded into [`more-itertools`](https://github.com/more-itertools/more-itertools)
at tag v11.1.0, commit `64be96ce`, listed in [`tasks.json`](tasks.json). Each one is a one-line
change to library code that breaks at least one existing test. Each prompt is a user's bug report,
checked against what the seeded bug actually does. The agent has to find the cause, fix it, and get
`python3 -m pytest -q tests` passing without touching `tests/`. The library is two modules of 5,500
and 1,600 lines. Finding the bug means searching and reading large files, and confirming the fix
means reading test-runner output. Those are the commands `rtk` rewrites.

**Pass/fail.** After the run, `tests/` is restored from the commit and the original suite runs. A
run passes only if that suite passes. A run that edited the tests is judged against the tests it
edited away from, and is counted.

**Arms.** Identical except for one hook. Every run gets a fresh, empty `CLAUDE_CONFIG_DIR`, so no
user settings, plugins, `CLAUDE.md`, auto-memory, or MCP servers load in either arm (plus
`--strict-mcp-config` and `--setting-sources project`, against a repository with no project
settings). The "with" arm adds exactly the hook `rtk init --global` installs, passed with
`--settings`:

```json
{"hooks": {"PreToolUse": [{"matcher": "Bash",
  "hooks": [{"type": "command", "command": "rtk hook claude"}]}]}}
```

**Isolation check.** `rtk gain -p` reports per working directory, and every run has its own. So
every run records `rtk`'s own claims about that run alone, and a "without" run showing any
rewritten command is a leak the analysis will flag.

**Pairing and order.** A pair is one task, at one effort level, at one repetition, run with and
without the filter back to back. The order of pairs is shuffled with a recorded seed, and so is
which arm goes first inside each pair. That spreads time of day, API load, and cross-run prompt
caching evenly over both arms rather than leaving them to chance.

**Model and effort.** One model, pinned by ID and recorded (`--model`, default `claude-sonnet-5`).
Two effort levels, `low` and `high`, because the JetBrains result depended on effort. Three
repetitions per pair by default. `--max-turns 60` and a twenty-minute timeout per run; a run that
hits either is a failure, not an exclusion.

**Billing.** Run it on an API key created for this test and nothing else. The key's spend in the
provider console is the bill. The script's computed cost is checked against it once, at the end,
before any figure leaves this directory.

## How big a run has to be

The analysis was dry-run on synthetic results with a true 8% cost increase built in — about the
size JetBrains measured — at twelve tasks, three repetitions, and a run-to-run spread like the one
the book cites. The 95% interval came out at −2% to +37%. **At the default size this test can
detect a large effect and cannot resolve one the size already published.** That is not a flaw to
hide. It decides the order you run things in:

1. **Pilot.** `run --tasks tail-off-by-one,rstrip-cache,consecutive-groups-key --reps 2`. That is
   24 runs. It gives you the cost per run and the real spread, which are the two numbers the full
   run's size depends on.
2. **Size the full run from the pilot.** The interval narrows roughly with the square root of the
   number of tasks. Halving it needs about four times the tasks, so extend `tasks.json` rather than
   adding repetitions: repetitions narrow the noise within a task, not the spread between tasks.
3. **Full run**, then analyse. If you cannot afford the size the pilot says is needed, run the
   default anyway. Report the interval as it comes out, and use the sentence below for a result
   that cannot tell.

As a rough scale only: the one published session breakdown the book prints came to $0.55. At that
rate the default 144 runs is about $80. The pilot tells you what your runs actually cost.

## Updating the book from the result

Write the sentence for whichever case applies. These were drafted before any run so that the result
chooses the sentence, not the other way round.

- **More expensive:** "A paired run on `rtk` <version>, <month year>, twelve seeded bugs in a
  public Python library, found cost per task <+x>% at <effort> effort (95% CI <lo> to <hi>),
  while the tool reported saving <n> tokens over the same runs."
- **Cheaper:** the same sentence with the sign changed, and the pass rates alongside.
- **No measurable difference:** "A paired run on `rtk` <version>, <month year>, could not
  distinguish the filter from no filter: <x>%, 95% CI <lo> to <hi>, on twelve tasks. The tool
  reported saving <n> tokens over the same runs."

The last clause, the tool's own figure next to the measured one, goes in whatever the verdict,
because it is the *Flattering Dashboard* claim tested directly. Then:

- Replace "nothing has re-tested it since" in *Starve the context*, and add the run to the research
  note under its own heading, with versions, date, seed, and prices date.
- Decide separately whether the blank table in *Starve the context* gets these numbers. It was left
  blank on the argument that only your own numbers settle it. Filling it with this run's numbers
  changes that argument, so the caption would have to say it is one run on one task set.
- Commit `results/<date>/` alongside: `meta.json`, `results.jsonl`, and the transcripts. A figure
  in the book should be traceable to the run that produced it.

## What it cannot tell you

- **Your workload.** Twelve bugs in one well-tested Python library are not your repository. The
  direction of the effect depended on the model and the task set in both published benchmarks.
- **Other commands.** The seeded bugs exercise search, file reads, `git`, and `pytest`. They do not
  exercise the long `cargo test` and `go test` output where `rtk` claims most of its savings. A
  second task set in a compiled language is the obvious extension.
- **The invoice, exactly.** Token counts come from the harness. They are checked against the
  console in total, not run by run.
- **Anything about the agent's knowledge of `rtk`.** Neither arm's model is told the filter exists,
  which matches how the hook is installed. A setup that also describes `rtk` in a user
  `CLAUDE.md`, as some do, is a third condition this run does not test.
