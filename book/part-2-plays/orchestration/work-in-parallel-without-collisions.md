# Work in parallel without collisions

## Problem

Three agents, three branches, three green suites. The merges are clean — no markers, nothing to
resolve, a morning that finally felt like leverage. The first error arrives ninety minutes after the
deploy, from a call site that was correct on every branch it existed on and is wrong in the tree you
shipped. What you saved in wall clock you now spend working out which of three tidy diffs is
responsible, and the tidiness is what makes it hard: none of them looks like the one that broke
anything.

## The play

Partition the repository before you start, and treat integration as the part that costs money.

1. **Split by directory, and put the split in every brief.** Each agent owns named paths, and each
   brief ends with the clause that makes the ownership real: if you need to change something outside
   these paths, stop and tell me. Without it, an agent that needs one line elsewhere takes it, and
   the partition you designed is a partition only you observed.
2. **Give each agent its own checkout, and budget for the environment.** `git worktree add
   ../meridian-invoices -b feat/invoices` is the ergonomic option — one repository, one `git
   worktree list`, shared refs. It is not the cheap one: a worktree is a fresh checkout, so
   dependencies install per tree and untracked files such as `.env` are absent. A
   `.worktreeinclude` file copies gitignored files across; a package manager with a global store
   handles the rest. Ports and databases are not isolated by any of this.
3. **Name the landmine files and serialise them.** Migration directories, route tables, barrel and
   index files, translation catalogues, lockfiles. One agent at a time touches these, or you do them
   yourself afterwards. In the measured data they are a small share of conflicted files; in
   practitioners' accounts they are a large share of wasted afternoons.
4. **Check overlap before you merge anything.** Two branches touching one file is a question worth
   asking before git is asked to answer it:

   ```bash
   comm -12 \
     <(git diff --name-only "origin/main...feat/invoices" | sort) \
     <(git diff --name-only "origin/main...feat/rate-limit" | sort)
   ```

5. **Integrate one branch at a time, rebasing each onto the last, and run the full suite on the
   merged tree.** Per-branch green is evidence about each branch in isolation, which is precisely
   the state that no longer exists once the second one lands.
6. **Do not mistake a worktree for a boundary.** Worktrees share refs, config, the stash, and
   `.git/hooks` — so a hook written from inside one runs in the parent repository, as you, the next
   time you trigger it. Harnesses add their own blocks on top of git's silence; Claude Code 2.x
   refuses edits aimed at the main checkout and blocks the redirects an agent would otherwise find —
   `git -C`, `--git-dir`, `GIT_DIR`, `GIT_WORK_TREE`, and a `cd` before running git. If you need a
   real boundary, you need a container or a VM.

The measured conflict rates are the argument for partitioning rather than trusting the merge. Across
roughly 33,600 agent-authored pull requests sampled in mid-2026, branch pairs from the same agent
conflicted textually about 20% of the time and pairs from different agents about 42% — and the
authors call that a conservative lower bound, because the method counts only what git notices
([`parallel-agents-and-collisions.md`](../../../notes/research/parallel-agents-and-collisions.md)).
Whether parallel agents are faster end to end, counting merge and rework, is substantially
unmeasured. The exchange rate is unglamorous: N agents means N environments, a set of files nobody
may touch concurrently, and an integration sequence you perform yourself. Parallelism moves cost
from writing to integrating. It does not remove it.

## Worked example

`meridian`, a Ruby freight-booking platform whose monorepo holds nineteen deployable services, split
three jobs across three worktrees, all branched from `origin/main`:

```bash
$ git worktree add ../meridian-webhooks   -b feat/webhooks
$ git worktree add ../meridian-invoices   -b feat/invoices
$ git worktree add ../meridian-rate-limit -b feat/rate-limit
```

Agent A owned `services/webhooks/`, B owned `services/invoices/`, C owned `engines/rate_limit/`.
Three things then happened, in increasing order of unpleasantness.

All three needed a table, so each wrote a timestamped file into the shared `db/migrate/`. Three
distinct filenames, no conflict of any kind, and a migration order nobody had run. A and B both
added a line to `config/routes.rb`, and git stopped the merge and asked. That was the good case, and
it took four minutes.

Then agent C renamed `check_quota` to `enforce_quota` across the rate-limit engine and fixed every
call site that existed when it started. Agent B, working from the same base, added a fresh call to
`check_quota` in the invoice controller. Both suites passed. The merge was clean. Production raised
`NoMethodError` ninety minutes later, in a code path the invoice tests did not cover because on
`feat/invoices` the method was still there.

The fix was procedural rather than clever: `db/migrate/` and `config/routes.rb` were added to the
brief as files no agent may touch, and integration became one branch at a time with the full suite
run on the merged tree. That would have caught the rename, assuming the suite covers that path —
which, on the day in question, it did not. Partitioning removes the collisions you predicted. The
residue is what your tests are for, which is a less satisfying conclusion than the one where the
tooling saves you.

## Failure mode

**The Clean Merge.** Git reports success, both branches were green, and the tree you now have was
never tested by anyone. One agent renamed a method and fixed the call sites that existed; another,
branched from the same commit, wrote a new one. One tightened a validation rule that another's
feature depended on being loose. Two wrote the same helper under different names, and nothing at all
will tell you about that one. The conflicts git can see are the survivable class — they stop you,
and you fix them in minutes. The class that costs you a deploy is invisible by construction, because
each branch is internally consistent and the inconsistency exists only in the union.

The tell is a merge with no conflicts between branches whose changed-file lists overlap, or that
touch each other's public names. The second tell is a green suite on a tree the suite has not been
run against since the last branch landed.

## Checklist

- [ ] Each agent's owned paths are named in its brief, with the stop-and-tell-me clause
- [ ] Each agent has its own checkout, with its own dependencies and environment file
- [ ] Landmine files — migrations, route tables, index files, lockfiles — are serialised
- [ ] Branch pairs were checked for overlapping changed files before merging
- [ ] Branches were integrated one at a time, each rebased onto the last
- [ ] The full suite ran on the merged tree, not only per branch
- [ ] No hook, config, or ref change was made from inside a worktree
- [ ] Renames and signature changes were checked against branches created before them

**See also:** [*Decompose into subagents*](decompose-into-subagents.md) ·
[*Review code you did not write*](../verification-and-trust/review-code-you-did-not-write.md) ·
[*Make the agent prove it*](../verification-and-trust/make-the-agent-prove-it.md)
