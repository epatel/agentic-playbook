# Team checklists

Every play ends with a checklist for one person doing one thing. This is the other view: one page
per suite, for a team deciding whether the practice exists at all.

The items were selected by one rule — keep what another person would notice the absence of. Anything
that stays on one developer's machine belongs in the play's own checklist rather than here, on the
same test that [*Build the working agreement*](../part-2-plays/team/build-the-working-agreement.md)
applies to the agreement itself. These pages are therefore shorter than the sum of the plays they
come from, and deliberately so. When an item here fails, the suite it came from has the detail.

Use one page per session rather than all six. A team that reviews everything reviews nothing, and
the six suites fail at different rates.

## Context

Assembled from the four plays in [*Context*](../part-2-plays/context/index.md).

- [ ] One file holds the project brief; the vendor-specific file is an import or a symlink
- [ ] Every line in it traces to a correction somebody would otherwise retype
- [ ] Nothing in it is scoped to one directory, one procedure, or one rare situation
- [ ] Somebody has had the agent state its project instructions back to them this week
- [ ] Conditional instructions load on a trigger rather than at launch, and none needs another
- [ ] Any filtering tool was measured on a paired run against the bill, not its own dashboard
- [ ] Acceptance conditions live in a file, not only in somebody's opening message
- [ ] A stop rule is agreed before long runs, and state for the next session is written down

## Harness

Assembled from the three plays in [*Harness*](../part-2-plays/harness/index.md).

- [ ] Everyone can name what runs the loop, which tools exist, what runs unasked, and what the
      operating system refuses
- [ ] Every safety assumption is written on the layer that enforces it: nothing, the client, or
      the kernel
- [ ] Filesystem and network isolation are on for unattended runs, set to fail rather than degrade
- [ ] Credential files and tokens are denied or masked by name, since nothing is denied by default
- [ ] Rules needing the command text, the branch, or an argument's meaning are hooks, not patterns
- [ ] Shared skills cover one nameable situation each, described in the words a request would use
- [ ] Every connected server crosses a boundary, holds a scoped credential, and is pinned
- [ ] The connected list is short enough to recite from memory, and was pruned this quarter

## Orchestration

Assembled from the three plays in [*Orchestration*](../part-2-plays/orchestration/index.md).

- [ ] Delegated work is read-heavy, and every write in a run happens in one place
- [ ] Read-only workers have their write tools removed rather than discouraged
- [ ] Conventions the workers rely on are in a project file, not in somebody's conversation
- [ ] A single agent with the same token budget was tried before any fan-out was kept
- [ ] Every irreversible action is performed by code, after a check that code ran
- [ ] Each scripted stage names the capability gap it covers, and removing it would be a deletion
- [ ] Each parallel agent's owned paths are in its brief, and landmine files are serialised
- [ ] Branches are integrated one at a time and the full suite runs on the merged tree

## Verification and trust

Assembled from the three plays in
[*Verification and trust*](../part-2-plays/verification-and-trust/index.md).

- [ ] Test files, CI config, linter settings, and type-checker settings are read before the
      implementation
- [ ] No test was deleted, skipped, or weakened, and no pipeline step was removed
- [ ] A send-back threshold on size and file count is agreed in advance, and reviewers use it
- [ ] One critical path is traced end to end and can be explained without the description open
- [ ] The finish condition exists in writing, names a command, and names what must not change
- [ ] A deterministic gate blocks a run's end, rather than a sentence in a brief asking it to
- [ ] Evidence attached to a change is command output rather than a summary of it
- [ ] One named person owns each change, may decline on volume alone, and has done so recently

## Economics

Assembled from the three plays in [*Economics*](../part-2-plays/economics/index.md).

- [ ] Input and output are known as shares of the bill, not only as token counts
- [ ] Turn count is recorded alongside cost for any workflow the team runs repeatedly
- [ ] What invalidates your provider's cache is written down where the team can see it
- [ ] The harness's local figure has been reconciled against the provider's billing view
- [ ] Tier decisions are stated as cost per accepted outcome, each with a named cheap oracle
- [ ] No claim in a tier decision compares per-token prices across model generations
- [ ] The alternative to delegating was costed as typing plus review, not as typing
- [ ] The list of things not worth delegating carries a date and gets re-tested

## Team

Assembled from the three plays in [*Team*](../part-2-plays/team/index.md).

- [ ] The agreement's agenda came from disagreements in real pull requests, not from a blank page
- [ ] Every rule concerns something that leaves a machine; the rest is written down as personal
- [ ] The page is in the repository, fits on a screen, and anyone may amend it
- [ ] It carries a date, a version, and a line saying what last changed and why
- [ ] The next revision is triggered by an event, and experiments have a standing exception
- [ ] Sharing sessions ask for discarded runs first, and somebody senior answers that one first
- [ ] What survives a session leaves as a committed file, described by somebody other than its
      author
- [ ] Day-one setup is a script and a page, and the joiner verifies that the instructions loaded
