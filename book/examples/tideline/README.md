# `tideline` — the Verification and Trust scratch project

`tideline` is the TypeScript service that stages firmware rollouts to field devices, and it
carries the worked examples in three plays:

- [*Review code you did not write*](../../part-2-plays/verification-and-trust/review-code-you-did-not-write.md)
- [*Make the agent prove it*](../../part-2-plays/verification-and-trust/make-the-agent-prove-it.md)
- [*Decide who signs off*](../../part-2-plays/verification-and-trust/decide-who-signs-off.md)

## What is here

| Path | Is |
|---|---|
| `main/` | The tree as it stood on `origin/main`: battery-gated rollout staging, nine files. |
| `agent/` | The same tree after the agent's pull request, which adds percentage-gated cohorts. |
| `reproduce.py` | Builds a throwaway git repository from the two trees and runs the book's commands. |

The two trees are the *contents* of two commits, not a git repository. `reproduce.py` turns them
into one — `main/` committed on `main` with a `refs/remotes/origin/main` pointed at it, then
`agent/` committed on `feat/percentage-cohorts` — so that `origin/main...HEAD` in the book means
what it says.

## Running it

```
python3 book/examples/tideline/reproduce.py
```

Python 3 standard library only, plus `git` and `rg` on the path. It writes nothing outside a
temporary directory, cleans up after itself, and exits non-zero if a command fails or if one of the
shapes the book asserts — nine changed files, three rows in the gate-first `--stat`, two bucketing
helpers in `src/` — is no longer true. Commit identity and dates are pinned, so the output is the
same on every machine.

## The defect the example turns on

`main/src/cohort/assign.ts` already exports `bucketFor(deviceId, buckets)`, which rounds a boundary
device *down*. The agent's branch adds `hashToBucket(id, n)` in a new `cohorts.ts`, which rounds the
same boundary *up*. Both are reasonable; having both is the problem, and one `rg` finds it. The
branch also drops two steps from the CI workflow and skips an existing battery test, which is what
the play's read-the-gates-first order catches.

## What is deliberately not reproduced

The agent run itself, and the ordering bug the review missed — cohort assignment running before the
battery check rather than after. Both trees are real TypeScript but the project has no installed
toolchain here, so `npm test` is not part of the reproduction; the point of the example is the
review, which is entirely a matter of reading the diff.
