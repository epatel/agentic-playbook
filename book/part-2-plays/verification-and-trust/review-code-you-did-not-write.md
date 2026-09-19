# Review code you did not write

## Problem

Four agent pull requests are open and you started the first one twenty minutes ago. The code reads
well: consistent naming, defensive checks in the right places, a test file that arrived with it. By
the third one you are no longer reading for correctness, you are checking that it looks like the
other two, which is a comparison it will always win. The diffs are bigger than the ones your
colleagues send and there are more of them, and the thing review was actually for — somebody in the
building understanding this change — is quietly not happening for any of them.

## The play

Review in an order that spends the cheap checks first, because the expensive one is reading, and
reading is what you run out of.

1. **Look at what the change did to the things that check it, before what it does.** Test files, CI
   configuration, linter settings, and type-checker settings. A net-negative line count in a test
   file, a test moved to `skip`, a relaxed rule, a widened type, a deleted pipeline step: each is a
   send-back on its own. One command, and it catches the evasion agents are measured making: across
   roughly 4,900 agent pull requests in 2026, those adding tests without improving coverage deleted
   tests at about two and a half times the rate they added them
   ([`verification.md`](../../../notes/research/verification.md)).
2. **Send it back on size and shape without reading it.** Google's review guidance grants reviewers
   the authority to reject a change for being too large and nothing else, and GitHub's 2026 guidance
   names the triggers for agent pull requests: more than five unrelated files, a purpose that will
   not fit in one sentence, test changes arriving alongside CI failures. You are declining a review
   that does not fit in your day, not judging the work.
3. **Search for the thing before accepting that it needed writing.** Agent pull requests carried
   roughly 1.9 times the semantic duplication of human ones in the largest 2026 corpus
   ([`review-practice.md`](../../../notes/research/review-practice.md)). Two implementations of one
   rounding rule is not a style problem; it is two answers to one question, one of which will be
   wrong later.
4. **Trace one path end to end and say it out loud.** Review's measured function was never mainly
   bug-finding — at Microsoft, one review comment in eight concerned a defect. What it produces is
   somebody who understands the change, and with agent-authored code nobody otherwise does.
5. **Ask for the reproducer, or for the sentence saying there is not one.** The Linux kernel's
   guidance to submitters doubles as a reviewer's rule, and its stated reason is maintainer time.
6. **Decide what the agent's plan in the description is for.** GitHub says demand it before
   investing review time. The oldest study of author preparation found annotated changes turning up
   almost no defects, read that as authors self-correcting, and conceded the alternative in the same
   paragraph — that "prepping disables the reviewer's capacity for criticism" once the code matches
   the prose. Nobody has measured which wins when the author is the run that wrote the code
   ([`review-practice.md`](../../../notes/research/review-practice.md)). Triage with the plan; do
   not read the diff through it.

Your instincts were calibrated against an author who paid something to write it: length signalled
effort, fluency signalled care, and both were proxies that worked only because writing was
expensive. When OCaml's maintainers declined a 13,000-line agent-authored debugging feature in late
2025, nobody argued the code was bad — the effort in it fell far below the effort needed to review
it, and that difference landed on people who had not chosen to spend it. DORA calls the displacement
the *verification tax*, and the exchange rate here is paying it deliberately: slower per pull
request than the agent, on purpose, and sending back changes that were fine.

## Worked example

`tideline`, a TypeScript service that stages firmware rollouts to field devices, had an agent pull
request open — 480 lines across nine files, adding percentage-gated cohorts so a rollout could reach
5% of devices before the rest. The reviewer read none of it first.

```bash
$ git diff --stat origin/main...HEAD -- tests/ tsconfig.json .github/
 .github/workflows/ci.yml |  2 --
 tests/cohort.spec.ts     | 41 ++++++++++++++++++++++++++++++++++++++
 tests/rollout.spec.ts    | 18 ++---------------
 3 files changed, 44 insertions(+), 17 deletions(-)
```

Two of those three rows were most of the review. An existing test file had gone net negative, and
the workflow had lost something:

```bash
$ git diff origin/main...HEAD -- .github/workflows/ci.yml
       - run: npm ci
-      - run: npm run typecheck
       - run: npm test
-      - run: npm run lint
```

```bash
$ git diff origin/main...HEAD -- tests/rollout.spec.ts | head -4
-  it('holds back devices below the minimum battery threshold', async () => {
+  it.skip('holds back devices below the minimum battery threshold', async () => {
```

Then one search, before reading the new module:

```bash
$ rg -l --type ts 'bucketFor|hashToBucket' src/
src/cohort/assign.ts
src/rollout/schedule.ts
```

`assign.ts` already had `bucketFor(deviceId, buckets)`. The pull request had added
`hashToBucket(id, n)` beside it, with a different tie-break at the boundary.

The change went back with three notes: restore the two pipeline steps, un-skip the battery test, use
the helper that exists. The rollout arithmetic itself was right, and better commented than the
module next to it. Everything the review caught was about what the change had removed and what it
had duplicated, which is the shape the measurements predict.

What it missed surfaced six days later. Cohort assignment ran before the battery check rather than
after, so devices were enrolled and then held back, and sat in a cohort they had never been eligible
for. The restored battery test passed the whole time: it tested the predicate, not where the
predicate was called. Four minutes of checking found three things, and the fourth was the one worth
forty.

## Failure mode

**The Drifting Yes.** Your approvals get easier and nothing tells you. Measured over 207 days on
agent pull requests, the same reviewers moved from approving 30.5% to 36.6%, while their approval of
human-authored pull requests over the same months held flat — so it is not general leniency, it is
specific to this author. The effect is small and comes from one 2026 preprint. The part worth
worrying about is that four hand-crafted surface metrics failed to detect the drift and only
sentence-embedding analysis found it: whatever you would check to reassure yourself is the thing
that did not work ([`review-practice.md`](../../../notes/research/review-practice.md)).

From the inside it reads as calibration — the last nine were fine, this one looks like those. The
tell is your own comments. In that corpus the median comment ran eleven words and a quarter were
five or fewer. If you cannot name a change you sent back this month, you are not reviewing them, you
are receiving them.

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
