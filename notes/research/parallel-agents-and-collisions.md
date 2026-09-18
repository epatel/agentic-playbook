# Parallel agents and the collision problem — worktrees, isolation, and merge strategy

**Question asked:** how to run several agents against one repository at once without them destroying
each other's work, what actually goes wrong at the merge, and whether the parallelism pays for
itself.

**Researched:** 19 September 2026 **Confidence:** high on git mechanics and vendor isolation
behaviour (official docs throughout); high on the conflict-rate measurements (one large-sample study
with stated confidence intervals); low on whether parallelism is net faster, where the evidence is
thin and contested.

Feeds the **Orchestration** suite, chiefly *Work in parallel without collisions*. This is the brief
with the most lift-ready worked example in the pass.

## Findings

### What `git worktree` actually guarantees

From the official documentation: "A git repository can support multiple working trees, allowing you
to check out more than one branch at a time," and a repository "has one main worktree (if it's not a
bare repository) and zero or more linked worktrees." [1]

The sharing rule, verbatim: "The new worktree is linked to the current repository, **sharing
everything except per-worktree files such as `HEAD`, `index`, etc.**" [1] Note the "etc." The docs
are deliberately vague there, and the vagueness is load-bearing — see the security finding below.

The same-branch constraint, verbatim: "By default, `add` refuses to create a new worktree when
*<commit-ish>* is a branch name and is already checked out by another worktree, or if *<path>* is
already assigned to some worktree but is missing… This option overrides these safeguards." And: "To
add a missing but locked worktree path, specify `--force` twice." [1]

Exact synopses worth having to hand: [1]

```
git worktree add [-f] [--detach] [--checkout] [--lock [--reason <string>]] [--orphan]
                 [(-b | -B) <new-branch>] <path> [<commit-ish>]
git worktree list [-v | --porcelain [-z]]
git worktree remove [-f] <worktree>
git worktree prune [-n] [-v] [--expire <expire>]
git worktree lock [--reason <string>] <worktree>
git worktree move <worktree> <new-path>
```

`-b` "refuses to create a new branch if it already exists"; `-B` "overrides this safeguard,
resetting *<new-branch>* to *<commit-ish>*." `remove` "refuses to remove an unclean worktree unless
`--force` is used." [1]

### Untracked files are the whole point, and the whole cost

Claude Code's docs put it plainly: "A worktree is a fresh checkout, so initialize your development
environment there: ask Claude to install dependencies, or run your project's setup yourself in the
worktree directory," and "untracked files like `.env` or `.env.local` from your main repository are
not present." [2]

The isolation you wanted (agent A's build artefacts cannot confuse agent B) and the tax you did not
(three `node_modules`, three `.venv`, three copies of a 400MB build cache, three missing `.env`
files) are the same property viewed from two sides. Say that once in the play and the reader will
stop being surprised by it.

Two documented mitigations rather than folklore:

- **A `.worktreeinclude` file** at project root using `.gitignore` syntax: "Only files that match a
  pattern and are also gitignored are copied, so tracked files are never duplicated." [2]
- **pnpm ships a first-party answer** for `node_modules`: set `virtualStoreType: global` in
  `pnpm-workspace.yaml` (before 11.23.0 the key was `enableGlobalVirtualStore: true`), after which
  "each worktree's `node_modules` contains only symlinks into a single content-addressable store on
  disk," giving "Near-zero per-worktree overhead" and "Instant installs for new worktrees." [3]

Hand-symlinking `node_modules` is the anti-pattern: it is only safe when the lockfile is
byte-identical across worktrees, and concurrent installs into a shared symlinked directory can
corrupt it. [4] Note this is *not* the same thing as pnpm's global virtual store, and the two are
easy to conflate.

### A worktree is not a security boundary

This is the finding most likely to surprise a reader who has been using worktrees happily for
months.

A worktree shares more than the object store: "Refs and branches (`refs/heads`, `packed-refs`). One
namespace for every worktree. The config (`.git/config`). The stash (`refs/stash`). **Hooks**
(`.git/hooks`), which is where a shared directory becomes arbitrary code execution." [5] The
consequence: "A hook installed from inside a worktree is therefore installed for the parent
repository, and it runs as you, in the parent, the next time you run the triggering command." [5]

The same source benchmarks `git clone --shared` against `git worktree add` and finds them
indistinguishable: "58.7 to 58.9 MB, 826 to 982 ms. They are the same operation as far as your disk
is concerned." [5] **This directly contradicts the most common stated reason for choosing
worktrees.** If the disk-and-time argument is not real, the actual argument is ergonomics — one
repository, one `git worktree list`, shared refs — and the book should say so rather than repeat the
folklore.

Because git provides no enforcement here, Claude Code adds its own layer: it blocks `Edit`/`Write`/
`NotebookEdit` targeting the main checkout, blocks Bash commands whose working directory resolves to
the main checkout, and blocks "git redirects" — "The redirect can come through `git -C`,
`--git-dir`, a `GIT_DIR` or `GIT_WORK_TREE` variable, or a `cd` into the main checkout before
running git." [2] That list is worth quoting: it is a catalogue of the ways an agent will find its
way home if you do not stop it.

### The tooling, verified and unverified

Stated bluntly because several widely-cited tools are dead or dying.

| Tool | Status | Detail |
|---|---|---|
| **Claude Code** | **Verified, primary** | `claude --worktree <name>` (`-w`); worktree at `.claude/worktrees/<name>/` on branch `worktree-<name>`; `worktree.baseRef` is `"fresh"` (default, branches from remote default) or `"head"`; subagents take `isolation: worktree` in frontmatter; `claude --worktree "#1234"` branches from a PR. It "holds a `git worktree lock` on its worktree so that concurrent cleanup can't remove it" [2] |
| **Cursor Cloud Agents** | **Verified, primary** | "isolated VMs in the cloud with full development environments"; Cursor "manages VM provisioning, isolation, snapshots, startup, artifacts, and capacity"; you "can run as many agents as you want in parallel"; agents "clone your repo… and work on a separate branch" [6] |
| **GitHub Copilot coding agent** | **Verified, primary** | "its own ephemeral development environment, powered by GitHub Actions"; "a maximum execution time of 59 minutes"; one PR per task; single repository only [7] |
| **OpenAI Codex cloud** | **Partially verified** | Markets "Run work in parallel," "Delegate several tasks." The docs do not state the isolation substrate (container versus VM) [8] |
| **Google Jules** | **Verified, primary** | "runs in a virtual machine where it clones your code, installs dependencies, and modifies files" [9]. Concurrency limits not stated |
| **container-use (Dagger)** | **Verified, active, experimental** | "Containerized environments for coding agents… an open-source MCP server… Powered by Dagger"; agent gets a container *and* an isolated git branch, reviewed via `git checkout <branch_name>`. Badged "stability-experimental" [10] |
| **Claude Squad** | **Verified, active** | "manages multiple Claude Code, Codex, Gemini (and other local agents including Aider) in separate workspaces"; "git worktrees to isolate codebases so each session works on its own branch" plus tmux. AGPL-3.0 [11] |
| **Conductor** | **Product verified; worktree claim not** | "Run parallel Claude Code, Codex, and Cursor agents in isolated workspaces on your Mac." Mac-only. The site does not say it uses worktrees — that claim appears only in third-party roundups [12] |
| **Crystal** | **DEAD** | The repo is a deprecation notice; the project is now Nimbalyst. **Do not present as current** [13] |
| **Vibe Kanban** | **SUNSETTING** | The repo carries "Vibe Kanban is sunsetting" [14] |
| **uzi** | **Low confidence** | "CLI for running large numbers of coding agents in parallel with git worktrees," worktrees + tmux + a port allocator driven by `uzi.yaml`. Verified via search metadata only [15] |
| **Charlie** | **NOT FOUND** | No source located in this pass. Do not assert it exists |

The Cursor "8 parallel agents via worktrees" figure that circulates in blog posts **could not be
confirmed** in Cursor's documentation. Do not use it.

The table above is itself an argument for the book's non-goal about tool-named chapters: two of the
best-known tools in this category died or announced sunset within a year of being widely
recommended.

### What actually goes wrong at the merge — with numbers

The strongest empirical result in this brief. Across **33,596 PRs in 2,807 repositories** (AIDev-pop
dataset), testing **747 unique co-active pairs** with in-memory three-way merges via `git
merge-tree`: [16]

- Intra-agent pairs: **"19.8% textual conflict rate (119/601, 95% CI [16.8%, 23.2%])"**
- Cross-agent pairs: **"41.7% textual conflict rate (48/115, 95% CI [33.1%, 50.9%])"**

Where conflicts land, which cuts against folklore: "84.4% of the files involved in conflicts are
source files"; dependency and lockfiles are only **3.9%**; "Config & CI (4.0%), Other/assets (5.1%),
Docs & text (2.6%)." [16] Conflict shape: "57.6% of conflict reports are content-conflicts," "26.8%"
modify/delete, "15.1%" add/add. [16]

Co-activity is the norm rather than an edge case: "40.2% of repositories contain co-active
agent-authored PR pairs" at exact temporal overlap, 53.4% within a one-week window, and co-active
pairs are "79.4% of all PRs generated by an AI agent." [16]

**And the paper's own limitation is the headline for the book:** "this captures only the surface
layer; no tracking is done for deeper build or semantic conflicts. Our results therefore provide a
conservative lower bound." [16] So 19.8% and 41.7% are the conflicts git *noticed*. The ones that
matter are underneath.

### Is parallelism actually faster?

The only controlled measurement found is **CodeCRDT** (600 trials, 6 tasks, 50 runs per mode), which
reports **"up to 21.1% speedup on some tasks"** and **"up to 39.4% slowdown on others"**, with "100%
convergence with zero merge failures" but a semantic conflict rate of **"5-10%."** Its framing
sentence: "Multi-agent LLM systems fail to realize parallel speedups due to costly coordination."
[17]

**State this gap honestly in the book:** no study was found measuring wall-clock end-to-end time for
N human-supervised coding agents *including* merge and rework cost. CodeCRDT is the closest and it
is a bespoke CRDT-based system, not a worktree workflow. The absence is itself the finding — the
parallelism claim is, as of September 2026, substantially unmeasured.

## The collision taxonomy

Concrete named types, each with a shape a reader will recognise. Types 1–3 are the dangerous ones
because git reports success.

1. **Rename/add-call-site** — *semantic, merges clean.* Agent A renames `formatPrice` to
   `formatMoney` and fixes every call site it knows about; Agent B, on the old base, adds three
   fresh calls to `formatPrice`. Both branches pass. The merged tree breaks. [18]
2. **Migration ordering** — *semantic, zero git conflict.* Two agents each add a timestamped
   migration: "different filenames, clean merge, and now they run in an order nobody has tested."
   [18]
3. **Duplicated helper** — *semantic, invisible.* Two agents independently write the same utility
   under different names in different files. No test fails. You now own two. [18]
4. **Tightened validation** — *semantic.* One agent makes a rule stricter; another agent's feature
   depended on the looser rule, undocumentedly. [18]
5. **Lockfile divergence** — *textual, noisy, usually trivial.* Two worktrees each run `npm
   install`; the lockfile is tracked, so branches diverge. [4] Empirically only 3.9% of conflicted
   files. [16]
6. **Barrel / index / route-table / translation-catalog files** — *textual, frequent.* Named
   explicitly as "landmine files" that must be serialised. [18]
7. **Add/add on the same new file** — 15.1% of conflict reports. [16]
8. **Modify/delete** — 26.8%; one agent edits a file the other deleted. [16]
9. **Frozen-base drift** — agents started at different times branch from different tips, so conflict
   risk is invisible until integration. [19]
10. **Shared-`.git` escape** — an agent writes `.git/hooks/pre-commit` inside a worktree and it
    executes in the parent repo, as you. [5]
11. **Runtime, not code** — worktrees "isolate code but not the runtime environment": shared ports,
    databases, services. [4] uzi ships a port allocator precisely for this. [15]

## Concrete example we can lift

A Rails-ish API. Three agents split by directory, `worktree.baseRef` left at `"fresh"` so all three
branch from `origin/main`:

```bash
git worktree add ../api-webhooks   -b feat/webhooks
git worktree add ../api-invoices   -b feat/invoices
git worktree add ../api-rate-limit -b feat/rate-limit
git worktree list
```

Agent A owns `app/webhooks/`, B owns `app/invoices/`, C owns `app/middleware/`. Each brief carries
the escape clause that makes the partition real: **"if you need to change something outside them,
stop and tell me."** [18]

Where it goes wrong — three failures of increasing nastiness, which is what makes this worth a whole
*Worked example* heading:

1. All three need a database table, so each writes `db/migrate/2026091912####_*.rb`. Three distinct
   filenames, three clean merges, **no git conflict at all** — and an execution order nobody has
   tested. [18]
2. A and B both add a line to `config/routes.rb`. Git reports a conflict you can see and fix. This
   is the *good* case.
3. C renames `check_quota` to `enforce_quota` across middleware. B, on the old base, adds a call to
   `check_quota` in the invoice controller. Both branches are green. The merge is clean. Production
   is a `NoMethodError`.

The guards, each from a source:

```bash
# preflight: which files do two branches both touch?
comm -12 \
  <(git diff --name-only "origin/main...feat/invoices" | sort) \
  <(git diff --name-only "origin/main...feat/rate-limit" | sort)
```

Integrate one branch at a time onto main, rebasing each onto the last (`git rebase origin/main`
inside each worktree) [21]; serialise `db/migrate/` and `config/routes.rb` as landmine files [18];
and run the **full** suite on the merged tree rather than per branch — "the worst conflicts never
announce themselves." [18] One practitioner reports that test-gating at the worktree ("Nothing
merges until the test suite passes in the agent's worktree") cut "agent broke something" incidents
by 80%, with the residual 20% blamed on coverage gaps. [22] Attribute that figure; it is a single
self-report.

## Contradictions and gaps

- **The disk-and-speed rationale for worktrees appears to be false.** Most advocacy claims cheapness
  versus clones; the one source that benchmarked it found them identical and recommends plain clones
  for autonomous agents. [5] Record both positions — but the book should not repeat the cheapness
  claim uncritically, because it is the reason most readers believe they chose worktrees.
- **Lockfiles: practitioners versus measurement.** Practitioners rank lockfiles a top-three problem
  [18][4]; the measured data puts dependency manifests at 3.9% of conflicted files. [16] A plausible
  resolution is that lockfile conflicts are frequent-but-trivial while source conflicts are
  rarer-but-expensive — **but no source states this**, so present it as an open question rather than
  a tidy answer.
- **Symlinking `node_modules`** is condemned by one source [4] and endorsed in a different form by
  pnpm's own docs [3]. They are not the same mechanism. Do not let a play blur them.
- **No end-to-end speed measurement exists** for supervised parallel coding agents including merge
  cost. [17] is the closest and is not the same workflow.
- **Date anomaly:** the "Integration Guard" article renders a publication date of 26 August 2024
  while discussing Vibe Kanban internals. The date looks wrong and could not be resolved. [20]
- **Unverified:** Charlie (no source at all); Conductor's use of worktrees (product page silent);
  Cursor's "8 parallel agents" cap (secondary only); uzi (search metadata only).

## Staleness assessment

| Claim | Why it rots | Hedge |
|---|---|---|
| The entire tooling table | Two entries died or sunset within a year; this is the fastest-rotting thing in the pass | Name tools only as instances of a pattern, per the book's non-goal on tool-named sections; date the sentence |
| Claude Code worktree flags and paths | Point-release surface | Describe the behaviour; show the flag once with a version |
| Conflict rates (19.8%, 41.7%) | Tied to a mid-2026 dataset and that generation of agents | Quote with the sample size and date; the *ratio* (cross-agent roughly double intra-agent) is the durable shape |
| CodeCRDT's 21.1% / 39.4% | One bespoke system, small task count | Use it only to support "unmeasured and contested," never as a headline number |
| The 80% incident-reduction self-report | Single practitioner, no method | Attribute explicitly, or drop |
| `git worktree` mechanics and `--force` semantics | Core git, stable for years | Safe. The most durable material here |
| Worktrees share `.git/hooks` | A property of git's design | Safe, and the sharpest thing in the brief |

Durable for the life of the book: the collision taxonomy (types 1–4 especially), the
shared-hooks/not-a-security-boundary finding, the "conservative lower bound" caveat on conflict
measurement, and the partition-plus-escape-clause briefing pattern.

## Sources

[1] git-worktree documentation — https://git-scm.com/docs/git-worktree — accessed 19 September 2026
[2] Run parallel sessions with worktrees, Claude Code docs —
    https://code.claude.com/docs/en/worktrees — accessed 19 September 2026
[3] pnpm + Git Worktrees for Multi-Agent Development — https://pnpm.io/git-worktrees — accessed
    19 September 2026
[4] Git Worktree Isolation Patterns for Parallel AI Agent Development, Zylos Research —
    https://zylos.ai/research/2026-02-22-git-worktree-parallel-ai-development/ — accessed
    19 September 2026 — **secondary; verify before quoting**
[5] Git worktrees are not an isolation boundary for coding agents, Fletch, 30 July 2026 —
    https://fletch.sh/blog/git-worktrees-vs-clones-for-ai-agents/ — accessed 19 September 2026
[6] Cloud Agents, Cursor docs — https://cursor.com/docs/cloud-agent — accessed 19 September 2026
[7] About Copilot coding agent, GitHub docs —
    https://docs.github.com/en/copilot/concepts/agents/coding-agent/about-coding-agent — accessed
    19 September 2026
[8] Codex cloud docs — https://learn.chatgpt.com/docs/cloud — accessed 19 September 2026
[9] Jules documentation — https://jules.google/docs — accessed 19 September 2026
[10] dagger/container-use — https://github.com/dagger/container-use — accessed 19 September 2026
[11] smtg-ai/claude-squad — https://github.com/smtg-ai/claude-squad — accessed 19 September 2026
[12] Conductor — https://conductor.build/ — accessed 19 September 2026
[13] stravu/crystal (deprecated; now Nimbalyst) — https://github.com/stravu/crystal — accessed
     19 September 2026
[14] BloopAI/vibe-kanban (sunsetting) — https://github.com/BloopAI/vibe-kanban — accessed
     19 September 2026
[15] devflowinc/uzi — https://github.com/devflowinc/uzi — accessed 19 September 2026 — **search
     metadata only; not fetched directly**
[16] AI Agent Pull Requests on GitHub: Frequency, Structure, and Merge Conflict Rates (Xu,
     Subramanian, Karthik), submitted 6 July 2026, revised 7 July 2026 —
     https://arxiv.org/html/2607.04697v2 — accessed 19 September 2026
[17] CodeCRDT: Observation-Driven Coordination for Multi-Agent LLM Code Generation (Pugachev),
     18 October 2025 — https://arxiv.org/abs/2510.18893 — accessed 19 September 2026
[18] Merge conflicts with parallel AI agents: partition first, SanuDesk, 5 August 2026 —
     https://sanudesk.com/blog/merge-conflicts-parallel-ai-agents — accessed 19 September 2026
[19] 5 Ways to Stop AI Agents Stepping on Each Other, Autonoma, April 2026 —
     https://getautonoma.com/blog/parallel-ai-agent-prs — accessed 19 September 2026
[20] Integration Guard: Safely Merging Parallel Concurrent AI Agents from Git Worktrees into Main —
     https://dev.to/evertonkozloski/integration-guard-safely-merging-parallel-concurrent-ai-agents-from-git-worktrees-into-main-4l7m
     — accessed 19 September 2026 — **stated date 26 August 2024 appears incorrect**
[21] Parallel Worktrees + Clash-Style Conflict Prediction, codeongrass, 14 May 2026 —
     https://codeongrass.com/blog/parallel-worktrees-conflict-prediction/ — accessed
     19 September 2026
[22] 5 Lessons from Running AI Coding Agents in Parallel, 4 April 2026 —
     https://dev.to/battyterm/5-lessons-from-running-ai-coding-agents-in-parallel-53on — accessed
     19 September 2026 — **single self-report; attribute the 80% figure**
[23] Stacked PRs and AI Worktrees, Georg Heiler, 17 March 2026 —
     https://georgheiler.com/2026/03/17/stacked-prs-and-ai-worktrees/ — accessed 19 September 2026
