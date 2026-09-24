# Decide who signs off

## Problem

The change shipped on Thursday and broke something on Sunday. The commit carries your name on the
author line, and a trailer crediting a model that you did not add and cannot remember configuring.
You read the diff; you remember reading the diff. You cannot now reconstruct which parts you
understood and which you accepted because the pipeline was green. The incident review asks who
approved it. There is an answer. The trouble is that the approval and the understanding were two
separate events, and only one of them is recorded.

## The play

Decide it in advance, in writing, as a team. The question does not get easier during an incident.

1. **State that a named person owns every change, and say what owning it means.** Every project with
   a written policy lands here. The Linux kernel's `coding-assistants.rst` says agents must not add
   `Signed-off-by` tags, only humans can certify the Developer Certificate of Origin, and the human
   takes "full responsibility". The test worth stealing is Kubernetes's, because it is checkable:
   if you cannot personally explain the change, the pull request is closed
   ([`accountability.md`](../../../notes/research/accountability.md)).
2. **Write the argument against your own rule into the same document.** "The human owns the diff" is
   unanimous in policy and contested in the literature. Elish's moral-crumple-zone argument is that
   responsibility for an automated system's failure collapses onto the nearest human operator,
   protecting the system at that person's expense. Which of the two is happening here is still open.
   A team that privately reads the rule as a scapegoating device routes around it.
3. **Give the owner the right to refuse on volume alone.** Sign-off without standing to decline is a
   signature, not a decision. Google's review guidance grants reviewers that authority explicitly,
   and LLVM's version is a test anyone can apply: a contribution should be worth more than the time
   it takes to review it.
4. **Pick a disclosure string, check what your tools already write, and stop arguing about it.**
   There is no standard. Git accepts any `key: value` trailer and enforces nothing. The field
   carries `Assisted-by:` at the kernel and Fedora, `Generated-by:` at Apache, and prose in the pull
   request at Kubernetes. Several agree on something narrower and more useful: the model is not a
   co-author, because co-authorship implies a rights certification it cannot make. Check your own
   history first. VS Code shipped a setting appending a Copilot co-author trailer by default in
   2026, and reverted it to opt-in after people found it on commits they had written
   ([`accountability.md`](../../../notes/research/accountability.md)).
5. **Find out what your domain already requires before inventing a policy.** As of September 2026 no
   aviation, automotive, or medical-device regulator had published a position on who may sign off on
   code a model wrote. Where sign-off is genuinely constrained, the constraint predates all of this.
   ISO 26262-8 clause 11 already governs software tools used in safety-related development and
   covers code generators explicitly. A vendor indemnity is not that. It is a conditional promise to
   defend an intellectual-property claim, silent on defects, outages, and regulators. None of this
   is legal advice; it is what those documents say, on the date they were read.

What you are assigning is not blame but the obligation to explain the change to somebody else.
Nothing else can hold it: no standard records which model produced which hunk. The exchange rate is
throughput. An owner who can answer for a change is slower than the generation of changes, so the
team's rate becomes that person's rate, chosen deliberately rather than discovered later.

## Worked example

`tideline`, a TypeScript service that stages firmware rollouts to field devices, had shipped
agent-authored changes for four months before anyone wrote a rule. The first move was to find out
what the repository was already asserting:

> Captured September 2026, git 2.50.1.

```bash
$ git log --format='%(trailers:only)' -n 400 | grep . | sort | uniq -c | sort -rn
 267 Co-authored-by: Cursor Agent <agent@cursor.com>
   8 Reviewed-by: Priya Raman <priya@tideline.example>
```

Two thirds of the recent history carried a co-author trailer naming an assistant. Nobody on the team
had chosen it; an editor default had. For four months the audit trail had been making an
authorship claim on the strength of a checkbox. They turned it off and wrote five bullets into
`CONTRIBUTING.md`:

```markdown
## Sign-off

- One named person approves every change and is its author of record, whatever
  produced the diff.
- Approving means you can explain the change without the agent in the room. If you
  cannot, send it back. That is a normal outcome and not an escalation.
- You may decline a change on size alone. A change must be worth more than the time
  it takes to review it.
- Disclosure is a commit trailer: `Assisted-by: <tool>`. The agent does not sign off
  and is not a co-author.
- Reviewed when our tooling changes, and at least once a quarter.
```

Six weeks later the rule was working and the team was not. Two of five reviewers were doing most of
the approvals, and the queue had grown to a fortnight. The first correction, adding reviewers,
spread the same problem across more people. What actually moved was the third bullet, which nobody
had used yet. Once declining on size became ordinary, happening eleven times in a month, the changes
arriving got smaller and the queue drained.

The throughput they gave up was throughput they had never been able to verify, which is easier to
write in a book than to say in a planning meeting.

## Failure mode

**The Accountable Bystander.** The policy names an owner, the owner is a real person who takes it
seriously, and that person approved forty changes this week and could describe four of them. When
something breaks, the review finds the name and stops there. From the inside it does not feel like
negligence, because it is not. They did read them, in the time available, at the rate the work
arrived.

The tell is a document with a paragraph about who is responsible and none about what they may
refuse. That gap is the whole difference between accountability and a nominated recipient for it.
The second tell is an incident review that ends at a name rather than at the point where the change
stopped being understood. This is not the Drifting Yes
([*Review code you did not write*](review-code-you-did-not-write.md#failure-mode)). There a
reviewer's standard slips without them noticing; here the standard holds and the authority to act
on it was never granted.

## Checklist

- [ ] One named person owns each change, and "owns" is defined by what they must be able to do
- [ ] The rule states the objection to itself, rather than being sold as settled
- [ ] The owner may decline on size or volume alone, and has done so recently
- [ ] Disclosure convention chosen, checked against the live policy of anywhere you contribute
- [ ] Commit history checked for authorship claims your tooling added without being asked
- [ ] The agent is not listed as a co-author or a signer anywhere
- [ ] Any regulated-domain requirement identified before the policy was written, and dated
- [ ] The rule has a review trigger and a date

**See also:** [*Review code you did not write*](review-code-you-did-not-write.md) ·
[*Make the agent prove it*](make-the-agent-prove-it.md) ·
[*Build the working agreement*](../team/build-the-working-agreement.md)
