# meridian — scratch project behind two orchestration plays

This directory backs the worked examples in [*Decompose into subagents*][decompose] and [*Work in
parallel without collisions*][parallel]. Both plays tell a story about `meridian`, a Ruby
freight-booking monorepo, and both quote a command. This is the tree those commands were actually
run against, so the numbers in the prose are measured rather than illustrative.

[decompose]: ../../part-2-plays/orchestration/decompose-into-subagents.md
[parallel]: ../../part-2-plays/orchestration/work-in-parallel-without-collisions.md

## What the tree is

`tree/` is a skeleton, not an application — it is valid-looking Ruby that a reader could clone and
grep, and nothing more. It will not boot. It holds nineteen service directories under `services/`,
of which four have real content (`booking`, `tariffs`, `tracking`, and the shared `engines/billing`
engine), plus the two files the parallel-agents play calls landmines: `config/routes.rb` and a
`db/migrate/` directory with two timestamped migrations.

The call sites of `Billing::Client.new` are distributed deliberately. There are **52** in total,
across a mix of argument shapes — positional `(url, opts)`, splatted `(url, **opts)`, and keyword
`(url:, timeout:)` — because the play's scout classifies by shape. **Five** of the 52 live under
`services/tracking/vendor/parcelgrid/`, a checked-in, deployed fork that a scout would plausibly
read as third-party and skip. That is the 47-versus-52 gap in the play, and it is materially true
here: excluding that one directory really does yield 47.

## Running it

```bash
python3 book/examples/meridian/reproduce.py
```

Python 3 standard library only. `git`, `rg` (ripgrep), `awk` and `bash` must be on PATH; the script
checks and exits with a clear message if one is missing. It copies `tree/` to a temporary directory,
initialises a git repository with a fixed author and timestamp — so the commit hash echoed by `git
worktree add` is the same on every machine — runs the two plays' commands, prints each as a
transcript with its exact output, reports the versions of the tools used, then removes the
worktrees and the temporary directory. It exits non-zero if any command fails or if the count is
not 52.

`bash` is on that list because of step 4 of the parallel play, the `comm -12` overlap preflight:
process substitution is a bash and zsh feature, and the same line is a syntax error in `sh`. The
script gives two of the three branches a real overlap — both append to `config/routes.rb` — so the
preflight has something to find, and asserts that what it finds is that file.

## What is deliberately not reproduced

The subagent fan-out itself — four scouts returning four tables that sum to 47 — is a property of an
agent harness rather than of this tree, and the Ruby runtime collision at the end of the parallel
play (`NoMethodError` from a renamed `check_quota`) needs a running application with a suite to run
against it. The stale call survives here as source in `services/invoices/` for a reader to see, not
as a failure you can trigger.
