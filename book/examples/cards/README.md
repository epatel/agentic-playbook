# cards — worked example

Backs the worked example in
[*Split the agent file into cards*](../../part-2-plays/context/split-the-agent-file-into-cards.md). Unlike
every other project in this directory, the subject is not fictional: it is this repository, whose
root [`CLAUDE.md`](../../../CLAUDE.md) is a real two-tier index and whose
[`cards/`](../../../cards/) directory holds the real cards. There is no tree to ship, so there is
none here.

## Reproducing the blocks

```
python3 reproduce.py
```

It copies `CLAUDE.md` and `cards/` out of the checkout into a temporary directory, runs the two
commands the play prints — `wc -l` over both tiers, and a `grep` for links from one card to another
— echoes each command and its stdout, cleans up, and exits non-zero if a command fails or if either
block no longer matches what the play prints. Standard library only; nothing to install.

## This makes `cards/` load-bearing

Both blocks are asserted verbatim, because the play prints them verbatim. **Editing a card, adding
one, or adding a link between two will fail this script.** That is the intended behaviour and not a
trap to route around: re-run it, and paste the new output into the play. The alternative was to
assert nothing and let the book quietly drift from a directory that changes.

## Not reproduced

The judgement, which is the point of the second block. The script counts links between cards; the
play's claim is that all four of the current ones are signposts rather than chains, and no command
can decide that. If a fifth link appears, the script will report it and somebody has to read it.
