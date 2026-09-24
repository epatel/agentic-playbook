# Refactoring a codebase for agents

The second wave is the suspicion that how well agents work in a codebase is a property of the
codebase, that the property is nameable, and that it can be changed on purpose. This chapter is a
forecast, for teams deciding whether to restructure for agents. Agents seem noticeably better in
some codebases than in others. In practitioners' accounts the difference tracks less than you would
expect: not obviously the age, or whether the team is any good. The same model, given the same
quality of agent file, will produce a clean change in one repository and a plausible mess in another
down the corridor.

## The constraint behind code organisation has swapped ends

Most of what a working developer believes about organising code assumes that reading and writing
code is expensive, and for an agent that constraint sits at the other end. The old rule was to
arrange things to do less of both. That is where abstraction comes from, and it was correct. A layer
you can learn once and then stop reading is a layer you have stopped paying for.

For an agent, writing is cheap: it will produce four hundred lines about as readily as forty. The
expensive thing is behaviour it cannot see. The agent has no memory of last Tuesday's session, no
accumulated feel for which module is load-bearing, and no way to notice the convention that lives in
everyone's head. What it has is whatever it can pull into one window, and it pays for the assembly
every single time.

Almost everything else in this chapter follows from that one swap. The moves are not new; the reason
for them is.

## An agent works in features, so organise by feature

An agent's unit of work is a capability, not a layer. The task arrives as "add a discount code to
checkout", never as "add a row to the service layer". A codebase organised by layer fights that. All
the controllers sit in one directory, the services in another, the repositories in a third, and a
single feature is scattered across six files in three trees. A developer with jump-to-definition
crosses that in a keystroke and stops noticing the cost. An agent reassembles the feature from
fragments at the start of every run. It spends a meaningful share of its window rebuilding a flow
that could have lived in one directory.

Organised feature-first, one capability is one folder: the handler through to the response, the
logic beside its test. Three things follow. The behaviour is visible in one place, which is what
makes a task briefable at all, in the sense [*Scope a task to fit the
window*](../part-2-plays/context/scope-a-task-to-fit-the-window.md) means. The blast radius of a
change is legible: this feature, these files, nothing else claims them. And duplication between
features becomes cheaper than the wrong shared abstraction, because two similar functions in two
folders can diverge without a meeting.

That last one is the part to argue with. Duplication has a cost that arrives later than the saving:
the bug fixed in one copy and not the other, the security patch applied four times out of five. The
claim is not that duplication is free. It is that the exchange rate has moved. What duplication used
to buy, less code to read, is worth less to a reader that reads fast and in bulk, if not for free.
What abstraction charges, behaviour somewhere else, is worth more to a reader that cannot see
somewhere else.

## Hidden control flow makes a locally correct change globally wrong

The other half is control flow that does not appear in the code an agent is reading. Decorators that
register routes at import time. A dependency-injection container assembling the object graph from
type hints. Lifecycle hooks on the ORM that write to a second table. Middleware chains, metaclasses,
signals, anything configured by convention over a directory scan. Each was adopted to remove
repetition from a human's reading. Each removes the evidence an agent needs to predict what its
change will do.

The tell is a change that is locally correct and globally wrong. The function does what it says, the
tests for that function pass, and something three frames up the stack that nobody mentioned now
behaves differently. That is the Confident Wrong Rewrite, described in [*The failure modes worth
naming*](../part-3-where-it-struggles/the-failure-modes-worth-naming.md), with a specific cause. The
cause is in your architecture, not in the model.

This is not an argument for deleting your framework. Cross-cutting concerns such as authentication,
persistence, logging, and transactions still belong in shared infrastructure. Rewriting them per
feature would make a worse codebase by every measure, including this one. The distinction worth
holding is between a trustworthy black box and the magic kind. A black box you call explicitly,
whose contract is stated where you call it, costs an agent one line of context. The same capability
applied invisibly, because of where a file sits or what a class inherits, costs an agent the whole
mechanism, and the agent will guess.

## Four properties besides layout do as much work, for less

Layout gets the attention, but four other properties do at least as much work, and all four are
cheaper to change.

- **A check that says whether the result is wrong.** Types, a fast suite, a linter with teeth. This
  is the single most valuable thing in an agent-friendly repository, because it converts an agent's
  confidence into a fact. See [*Make the agent prove
  it*](../part-2-plays/verification-and-trust/make-the-agent-prove-it.md).
- **A build and a test loop that run in one command, quickly.** An agent will run the suite far more
  often than you do. A ten-minute suite is not merely slow; it is a suite the run cannot afford to
  use.
- **Names that describe what a thing does rather than where it sits.** `PaymentRetryPolicy` carries
  its own documentation into the window; `Helper2` requires a reading session to recover.
- **Dead code and dead configuration removed.** An agent has no way to know that the second
  implementation is the one nobody calls any more. It will find both and may build on either.

## A popular part arrives already documented

The model's familiarity is now one more reason for the boring, popular component. Choosing one is
the old COTS decision, commercial off-the-shelf against built in-house, and people used to settle
it: who knows it, who can hire for it. A widely published design system, framework, or convention is
a part with a public datasheet. The agent file names it and its version and describes only your
departures. A home-grown equivalent must be documented in full and still arrives unfamiliar. The
catch is the edition: a popular part in a version the model saw less of is the Wrong Edition,
described in [*The failure modes worth
naming*](../part-3-where-it-struggles/the-failure-modes-worth-naming.md), waiting to happen.

## What would change this position

Nobody has measured most of it. There is no published comparison of agent success rates between
feature-first and layer-first versions of the same codebase. Nobody has measured what explicit
control flow is worth in tokens or in correctness. No study of context files as such establishes
that a shorter one produces better output. The nearest measurement is of context size in general, in
[*The failure modes worth naming*](../part-3-where-it-struggles/the-failure-modes-worth-naming.md).
The mechanism is plausible and the direct evidence is an absence.

Two things would settle it, and a team with a spare week could run both without a laboratory. Take a
real repository and restructure one subsystem feature-first. Run the same twenty tasks against both
versions with the same model and the same agent files, counting accepted changes rather than diffs
produced. Separately, count how much of a run's input goes on reassembling the same feature across
sessions. If that number is small, the whole argument is smaller than it sounds.

The signal to watch in the other direction is model capability, because this entire wave is a bet on
something staying hard. Every restructuring here encodes an assumption about what the model cannot
do. [*Make the control flow
deterministic*](../part-2-plays/orchestration/make-the-control-flow-deterministic.md) warns that
exactly that assumption expires. A year from now, "agents cannot follow behaviour across six files"
may read the way "agents cannot use a terminal" reads today. A quarter-long reorganisation justified
on that basis is the Load-Bearing Scaffold at the scale of a repository, a considerably more
expensive place to have one.

## Do it on contact, whether or not the wave arrives

Nothing above requires a migration project, and a migration project is the wrong response to a
forecast.

Do it on contact. The next feature you touch for other reasons, move into one folder with its tests.
The next invisible mechanism that burns an afternoon, replace with an explicit call at the site that
needs it. The next slow check, make fast. Each of those is defensible on its own merits to somebody
who thinks this whole chapter is speculation. Apply that test before starting any of it.

And note what survives if the wave never arrives: a codebase where one capability lives in one
place, behaviour is visible where it happens, names mean something, and a check runs in under a
minute. People were asking for that when the only reader was human. The argument has acquired a
second beneficiary, not a new conclusion.
