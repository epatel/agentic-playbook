# Review code you did not write

## Problem

Four agent pull requests are open and you started the first one twenty minutes ago. The code reads
well: consistent naming, defensive checks in the right places, a test file that arrived with it. By
the third one you are no longer reading for correctness. You are checking that it looks like the
other two, a comparison it will always win. The diffs are bigger than your colleagues' and there
are more of them. What review was for is quietly not happening for any of them: somebody in the
building understanding the change.

## The play

Review in an order that spends the cheap checks first. The expensive check is reading, and reading
is what you run out of.

1. **Look at what the change did to the things that check it, before what it does.** That means
   test files, CI configuration, linter settings, and type-checker settings. A net-negative line
   count in a test file, a test moved to `skip`, a relaxed rule, a widened type, a deleted pipeline
   step: each is a send-back on its own. One command catches the evasion agents are measured making.
   In a 2026 study, Java agent pull requests that added tests without improving coverage deleted
   tests at about two and a half times the rate they added them
   ([`verification.md`](../../../notes/research/verification.md)).
2. **Send it back on size and shape without reading it.** Google's review guidance grants reviewers
   the authority to reject a change for being too large and nothing else. GitHub's 2026 guidance
   names the triggers for agent pull requests: more than five unrelated files, a purpose that will
   not fit in one sentence, test changes arriving alongside CI failures.
3. **Search for the thing before accepting that it needed writing.** Agent pull requests carried
   roughly 1.9 times the semantic duplication of human ones in a 2026 corpus of 3,858
   ([`review-practice.md`](../../../notes/research/review-practice.md)). Two implementations of one
   rounding rule is not a style problem. It is two answers to one question, and one will be wrong
   later.
4. **Trace one path end to end and say it out loud.** Review's measured function was never mainly
   bug-finding: at Microsoft, one review comment in eight concerned a defect. Review produces
   somebody who understands the change. With agent-authored code, nobody otherwise does.
5. **Ask for the reproducer, or for the sentence saying there is not one.** The Linux kernel's
   guidance to submitters doubles as a reviewer's rule, and its stated reason is maintainer time.
6. **Decide what the agent's plan in the description is for.** GitHub says demand it before
   investing review time. The oldest study of author preparation found annotated changes turning up
   almost no defects and read that as authors self-correcting. The same paragraph conceded the
   alternative: that "prepping disables the reviewer's capacity for criticism" once the code matches
   the prose. Nobody has measured which wins when the author is the run that wrote the code
   ([`review-practice.md`](../../../notes/research/review-practice.md)). Triage with the plan; do
   not read the diff through it.

Your instincts were calibrated against an author who paid something to write it: length signalled
effort, fluency signalled care. In late 2025 OCaml's maintainers declined a 13,000-line
agent-authored debugging feature. Nobody argued the code was bad. The effort in it fell far below
the effort needed to review it, and the difference landed on people who had not chosen to spend it.
DORA calls the displacement the *verification tax*. The exchange rate here is paying it
deliberately: slower per pull request than the agent, on purpose, and sending back changes that were
fine.

## Worked example

`tideline`, a TypeScript service that stages firmware rollouts to field devices, had an agent pull
request open: 314 changed lines across nine files, adding percentage-gated cohorts so a rollout
could reach 5% of devices before the rest. The reviewer read none of it first.

> Captured September 2026, git 2.50.1.

```bash
$ git diff --stat origin/main...HEAD -- tests/ tsconfig.json .github/
 .github/workflows/ci.yml |   2 -
 tests/cohort.spec.ts     | 101 +++++++++++++++++++++++++++++++++++++++++++++++
 tests/rollout.spec.ts    |  11 +-----
 3 files changed, 103 insertions(+), 11 deletions(-)
```

Two of those three rows were most of the review. An existing test file had gone net negative, and
the workflow had lost something:

> Captured September 2026, git 2.50.1.

```bash
$ git diff origin/main...HEAD -- .github/workflows/ci.yml
@@ -14,6 +14,4 @@ jobs:
         with:
           node-version: 22
       - run: npm ci
-      - run: npm run typecheck
       - run: npm test
-      - run: npm run lint
```

> Captured September 2026, git 2.50.1.

```bash
$ git diff origin/main...HEAD -- tests/rollout.spec.ts | rg '^[-+] *it[.(]'
-  it('holds back devices below the minimum battery threshold', async () => {
+  it.skip('holds back devices below the minimum battery threshold', async () => {
-  it("treats the threshold as inclusive", async () => {
```

One test skipped and one deleted outright. The full diff showed the skipped test had lost its two
assertions as well, nine of the row's eleven changed lines. Then one search, before reading the new
module:

> Captured September 2026, ripgrep 15.2.0.

```bash
$ rg -l --sort path --type ts 'bucketFor|hashToBucket' src/
src/cohort/assign.ts
src/cohort/cohorts.ts
src/rollout/schedule.ts
```

Three files, two of them the pull request's own. `assign.ts` already had
`bucketFor(deviceId, buckets)`. The pull request had added `hashToBucket(id, n)` in a new
`cohorts.ts` and called it from `schedule.ts`. The tie-break at the boundary differed: the existing
helper rounded a device on a bucket edge down, and the new one rounded it up.

The change went back with four notes: restore the two pipeline steps, un-skip the battery test with
its assertions, restore the threshold test, and use the helper that exists. The rollout arithmetic
itself was right, and better commented than the module next to it. Everything the review caught was
something the change had removed or duplicated, the shape the measurements predict.

What it missed surfaced six days later. Cohort assignment ran before the battery check rather than
after, so devices were enrolled and then held back, and sat in a cohort they had never been eligible
for. The restored battery test passed the whole time: it checked that a low-battery device was held
back, not that it was held back before it was enrolled. Four minutes of checking found four things,
and the fifth was the one worth forty.

## Failure mode

**The Drifting Yes.** Your approvals get easier and nothing tells you. Measured over 207 days on
agent pull requests, the same reviewers moved from approving 30.5% to 36.6%. Their approval of
human-authored pull requests over the same months held flat, so this is not general leniency but
specific to this author. The effect is small and comes from one 2026 preprint. The worrying part:
four hand-crafted surface metrics failed to detect the drift, and only sentence-embedding analysis
found it. Whatever you would check to reassure yourself is the thing that did not work
([`review-practice.md`](../../../notes/research/review-practice.md)).

From the inside it reads as calibration: the last nine were fine, and this one looks like those. The
tell is your own comments. In that corpus the median comment ran eleven words and a quarter were
five or fewer. If you cannot name a change you sent back this month, you are not reviewing them.
You are receiving them.

## Checklist

- [ ] Test files, CI config, linter settings, and type-checker settings read before the
      implementation
- [ ] No test deleted, skipped, or weakened; no pipeline step removed
- [ ] Size and file count judged before reading, with a send-back threshold agreed in advance
- [ ] Searched for an existing implementation of anything the change introduces
- [ ] One critical path traced end to end and explained without the description open
- [ ] A reproducer supplied, or its absence stated explicitly
- [ ] The agent's plan used to triage the review, not to guide the reading

**See also:** [*Make the agent prove it*](make-the-agent-prove-it.md) ·
[*Decide who signs off*](decide-who-signs-off.md) ·
[*Work in parallel without collisions*](../orchestration/work-in-parallel-without-collisions.md) ·
[*Copy-paste templates*](../../appendices/copy-paste-templates.md)
