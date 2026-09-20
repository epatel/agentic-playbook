# atlas — worked example

Backs the worked example in
[*Write the agent file that actually gets read*](../../part-2-plays/context/write-the-agent-file-that-actually-gets-read.md).
`atlas` is a fictional Python billing service, eighteen months old, four contributors.

## The two trees

`before/` holds the agent file as it stood at eighteen months: a single 412-line `CLAUDE.md` containing
the three piles the play sorts it into — stale material (a CI runner decommissioned last spring, a
deploy script replaced in January), generic material (eleven lines of Python style that `ruff`
already enforces), and scoped material (forty lines of migration workflow that matter only under
`atlas/migrations/`).

`after/` holds the result of the prune: a 34-line `AGENTS.md` carrying the content, a 4-line
`CLAUDE.md` that is nothing but an `@AGENTS.md` import plus one Claude-specific line, and
`.claude/rules/migrations.md`, the path-scoped rule the migration pile moved into. That rule also
carries the raw-SQL prohibition that went back in two days after the prune, once deleting it had
shown it was load-bearing.

## Reproducing the counts

```
python3 reproduce.py
```

It copies each tree into a temporary directory, runs `wc -l` there, echoes the command and its
stdout, prints the kernel the capture ran on, cleans up, and exits non-zero if any command fails.
Standard library only; nothing to install.

## Not reproduced

The agent behaviour is not reproduced — whether a shorter agent file is actually followed more often is
the play's claim, not this example's, and only the line counts are mechanically checkable here.
