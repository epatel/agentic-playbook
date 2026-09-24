# Inviting non-developers in

The third wave is the suspicion that the request queue between developers and everyone else was a
consequence of typing, and that typing has stopped being the expensive part. This chapter is a
forecast, for teams weighing whether to let colleagues who do not write code make changes. A
designer notices that the empty state on the settings page says something slightly wrong. They know
exactly what it should say. They also know that saying so costs a ticket, a grooming session,
somebody's sprint, and three weeks. So a good proportion of the time they decide it is fine. This is
the normal operation of a healthy team, and everyone has made peace with it.

## Co-pilots make the change; developers make it safe

Most teams treat their non-developer colleagues as a request queue, and the queue loses fidelity in
translation. Somebody describes what they want in their own vocabulary. A developer translates it
into the system's vocabulary. The result comes back weeks later slightly different from what was
asked for, whereupon everybody negotiates. The translation is expensive at both ends.

A co-pilot arrangement is the other shape: the person who wants the change makes it. The developer
is the one who built the conditions under which that is safe. Not a gatekeeper, not absent, and
definitely not the person who reviews forty unfamiliar diffs a week. The work moves from doing the
change to making the change adjudicable.

The difference matters more than it sounds, because the first thing most teams try is the other
thing. They hand a designer an agent, wish them luck, and discover a fortnight later that nobody can
tell whether the eleven changes they shipped were good.

## The agent removed the typing and nothing else

The agent removed the typing. None of the rest went, and the rest is where the difficulty always
was.

What a developer contributes to a one-line copy change is not the line. It is knowing that the
string is also used in the onboarding email, that the settings page is the one screen with its own
translation pipeline, and that the component was rewritten last month by somebody who has since
left. None of that is in the repository in a form anybody can read. [*Write the agent file that
actually gets read*](../part-2-plays/context/write-the-agent-file-that-actually-gets-read.md)
addresses the same problem for the agent; now it arrives for a colleague.

So the honest question for this wave is not "can a designer ship a change". They could always have
learned to, and some of them did. It is "what has to be true before their change is safe to merge
without a developer reading it line by line". A yes to the first question and a no to the second is
how a team acquires a second review queue and no extra reviewers.

## Four conditions make somebody else's change safe

Four conditions make it safe, in rough order of how much they buy.

1. **A surface narrow enough to own.** Copy strings, design tokens, feature-flag configuration,
   content, the contents of one screen. A surface has a boundary somebody can be shown, and the
   boundary is what makes "this is yours" a sentence rather than a sentiment. Widening it later is
   cheap. Narrowing it after an incident is not.
2. **A check that adjudicates without a developer.** A build that fails, a visual-diff that flags a
   layout change, a schema that rejects an unknown token, a preview environment that either renders
   or does not. This is the same requirement as [*Make the agent prove
   it*](../part-2-plays/verification-and-trust/make-the-agent-prove-it.md). Here it does double
   duty: it tells the contributor they are done, and it lets the reviewer be brief.
3. **An agent file written in their vocabulary, not yours.** The project context file that serves
   your team is full of words like "migration" and "handler". A contributor working on copy needs to
   know where strings live, what the tone rules are, and which three files they must not touch. That
   is a second agent file scoped to their surface, and writing it is the actual work of this wave.
4. **A named person who signs off.** Not a process, a person, in the sense [*Decide who signs
   off*](../part-2-plays/verification-and-trust/decide-who-signs-off.md) means it: somebody who can
   explain the change, and who may decline it on volume alone without owing an explanation.

Nothing on that list is new technology. A team could do all four this quarter, and a good team
already does three of them for its own developers.

## Review capacity and accountability carry the cost

The first cost lands on review capacity. It is always review capacity.

The evidence in this book is consistent about one thing. Agent-assisted work moves effort from
writing to checking, the verification tax, and teams hit the wall there, not at the keyboard.
Inviting more contributors in without adding anything that can adjudicate their work does not
distribute the load. It concentrates it, on the same three people, in a less familiar form. A change
from somebody who does not know which parts of the system are load-bearing is harder to review, not
easier, and it arrives looking entirely reasonable. That is [*Onboard someone into all
this*](../part-2-plays/team/onboard-someone-into-all-this.md)'s Fluent Stranger, with one
difference. A new engineer acquires the missing sense with time. A colleague from another discipline
may never acquire it, because acquiring it is not their job.

The second cost is accountability, and it goes wrong in a specific way. The obvious arrangement is
that the contributor owns their change. That makes somebody responsible for a diff they cannot fully
read, in a system they cannot fully model. A developer approves it, assuming the contributor
understood it. Both parties have a reason to believe the other one checked. That is the Accountable
Bystander from [*Decide who signs
off*](../part-2-plays/verification-and-trust/decide-who-signs-off.md) with two people in it instead
of one. The fix is the boring one: state who is accountable for what, in writing, before the first
change rather than after the first incident.

## Low-code left no evidence worth quoting

The obvious historical analogy, low-code and citizen development, turns out to be nearly unusable,
for reasons worth reporting. It promised roughly this and delivered something more complicated.

The two figures everybody reaches for to argue that it failed do not survive being looked up. The
widely-circulated claim that 43% of citizen-developer initiatives were scaled back, paused, or
discontinued appears only in secondary aggregator posts with no primary citation. The 25–30% rewrite
rate for no-code projects traces to vendor marketing. Both are quoted constantly and neither is
evidence. What is left is an unquantified impression that these initiatives tend to succeed narrowly
and fail broadly. That is, at least, consistent with the four conditions above.

Take that as a description of the available evidence, not as a verdict. The last time the industry
tried to let non-developers ship software, nobody measured the result well enough to argue about it
afterwards.

## What would change this position

The measurement that would settle this does not exist. It would compare defect and revert rates
between changes authored by developers and by colleagues from other disciplines, within the same
narrow surface, on the same review process. Until somebody runs it, the case for this wave is a
mechanism and the case against it is an anecdote.

The signal to watch is what happens to review load in teams that try it. If review time per change
falls across the second and third quarter of a co-pilot arrangement as the checks improve, the wave
is real. If review time per change holds flat while the number of changes rises, the arrangement is
a throughput increase paid for out of the same three people. That is the shape [*Where the time
actually goes*](../part-3-where-it-struggles/where-the-time-actually-goes.md) describes.

## Build the four conditions for your own team first

Every one of the four conditions is worth building for your own team first, and none of them depends
on this wave arriving.

A surface with a stated boundary, a check that adjudicates without a person, an agent file written
for whoever actually works on that surface, and a named owner make your own agent-authored changes
reviewable. Build them for the developers, notice how much easier the first outside contribution
turns out to be, and let the wave arrive on its own schedule. The version that goes badly issues the
invitation first and retrofits the conditions around whatever has already been merged.
