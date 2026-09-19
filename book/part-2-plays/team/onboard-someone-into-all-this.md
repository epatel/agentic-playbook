# Onboard someone into all this

## Problem

The new engineer starts on Monday. The repository clones, the tests run, and the architecture note
is three years old but still roughly true — that part of onboarding works. What it no longer covers
is everything beside it: the committed context file, five shared skills, a one-page working
agreement, a review convention nobody wrote down, and a collective sense of which tasks this team
does not hand to an agent. They will be producing plausible pull requests by Wednesday. The cost is
that plausible now arrives before understanding, and nobody has built a check for the gap.

## The play

Put everything transferable in the repository, then spend the week transferring the part that will
not go in a file.

1. **Make the checkout the setup.** Everything the team shares is in the repository, so day one is
   clone, install the harness, and verify. Verification is a step rather than an assumption: ask the
   agent what the project instructions say and check the answer against the file. A precedence rule
   above the checkout can stop the team's brief loading with no error at all
   ([*Write the brief the agent actually reads*](../context/write-the-brief-the-agent-actually-reads.md#failure-mode)),
   and a joiner is the person least equipped to notice.
2. **Hand over the agreement before the codebase.** It is one page, and it is the shortest accurate
   description of how this team works that exists. A joiner who reads it on Monday stops inferring
   four conventions from whichever pull request they opened first.
3. **Let them watch a run before they drive one.** Pair on a task you drive, narrated, then on one
   they drive. What transfers is not the commands, which are in the documentation. It is where you
   stopped the run, what you declined to delegate and why, and which piece of output you did not
   believe.
4. **Give them a first task where being wrong is cheap to detect.** A new joiner cannot yet tell a
   good diff from a plausible one in this codebase, and for a few weeks the agent will produce
   plausible faster than they can build the judgement to catch it. Pick work a test suite or a type
   checker can adjudicate without them.
5. **Make them the reader of the shared material, not its author.** Their first contribution to it
   is a list of what it assumes: the card naming a service that no longer exists, the setup note
   missing a step, the skill description that means nothing to anyone not already on the team. That
   window is about three weeks wide. Ask for the list in writing before it closes.
6. **For the first few reviews, ask what they turned down.** Not "is this right" but "what did the
   run produce that you did not keep". A joiner who can answer has started building the judgement;
   one who kept everything is worth knowing about in week two rather than month four.

Onboarding used to transfer knowledge about a codebase, and files are good at that. The surface that
has grown beside it transfers judgement about a tool, which is what files are worst at and what
sitting next to someone is best at. The compensation is that a joiner is the only free audit of the
shared material the team will get, and only while they still do not know anything. The exchange rate
is a week of an experienced engineer's attention, most of it spent watching somebody else work, and
the appearance of a fast ramp: a joiner shipping agent-authored pull requests on day three is
evidence about the tools, not about the joiner.

## Worked example

`lodestone`, a claims-processing platform — C# services behind a TypeScript front end — took on a
tenth engineer in September. Day one was a page in the repository, not somebody's memory:

```bash
$ git clone git@github.com:lodestone/lodestone.git && cd lodestone
$ ./scripts/dev-setup.sh          # toolchain, database, seed data
$ claude
> What do my project instructions say about this repository?
```

The answer described nothing specific to `lodestone`. Following a setup note from a blog post, the
joiner had created a `CLAUDE.local.md` for their own sandbox URLs, which took precedence and stopped
the team's committed `AGENTS.md` loading. Nothing errored and the loaded-file list looked the same
either way. That is the Brief That Never Arrived, described in
[*Write the brief the agent actually reads*](../context/write-the-brief-the-agent-actually-reads.md),
and it surfaced within the hour only because asking the question was a step.

The pairing was the part nobody had budgeted for and the part that mattered. On the first run the
joiner watched an engineer stop the agent twice: once because it had begun rewriting a class that
was about to be deleted, and once because the plan it proposed was right and the reasoning given for
the plan was wrong. Neither stop was in any document, and neither needed saying again. By the end of
week three the joiner's list of things the shared material assumed ran to eleven items, seven of
which were fixed.

The first-task rule held badly. The first task was a small change to the claims-status endpoint,
which had tests, and the pull request was fine. The second was a front-end change, where the
equivalent check did not exist; it was approved on Thursday and reverted the following Tuesday. The
rule was right and half the codebase could not support it, which nobody had noticed because nobody
had joined in eighteen months.

It is a slightly humiliating way to find out the state of your own test suite, and cheaper than the
alternatives.

## Failure mode

**The Fluent Stranger.** The new joiner is productive immediately and the output is good. They know
the harness better than half the team, their pull requests are the right size, and the code follows
conventions they picked up from the shared context file on Monday. What they do not have, and cannot
have yet, is any sense of which parts of this system are load-bearing, which tests lie, and which of
the agent's confident suggestions are wrong in a way specific to this codebase. Nobody notices,
because the work looks like everyone else's work, which is precisely what an agent is good at
producing.

The tell is a joiner whose first three pull requests contain no questions. The second is a review
where "why did you put it here?" gets an answer about the code rather than the system, and the
reviewer accepts it, because the code is fine.

## Checklist

- [ ] Day-one setup is a script and a page in the repository, not a colleague's memory
- [ ] The joiner verified that the project instructions loaded, rather than assuming they had
- [ ] They read the working agreement before opening their first pull request
- [ ] They watched an experienced engineer drive a run, including the points where it was stopped
- [ ] Their first task had a check — tests, types, a reproducer — that adjudicates it without them
- [ ] They were asked, in writing, for the list of things the shared material assumes
- [ ] The list was asked for inside the first month, and something on it was fixed
- [ ] The first few reviews asked what they declined to keep from the run

**See also:** [*Build the working agreement*](build-the-working-agreement.md) ·
[*Make the agent prove it*](../verification-and-trust/make-the-agent-prove-it.md) ·
[*Collect and refine as a team*](collect-and-refine-as-a-team.md)
