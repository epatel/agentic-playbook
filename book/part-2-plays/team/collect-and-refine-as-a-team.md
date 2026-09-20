# Collect and refine as a team

## Problem

Three people on the team have each worked out something that makes these tools noticeably better,
and none of the three knows about the other two. One has a skill in their home directory that gets a
fiddly procedure right every time. One stopped letting the agent near the migration folder months
ago and has never said why. One writes agent files in a shape that reliably gets the test written
first, and could not tell you what the shape is. Nobody is hiding anything; it never came up. The
team pays the discovery cost three times and collects the benefit once each.

## The play

Run a recurring harvest: compare how people actually work, promote what wins into a file anyone
loads, and take out as much as you put in.

1. **Compare on one task shape, not in general.** "What are you using?" produces a list of tools.
   Take a job the whole team does — writing an adapter, cutting a release, chasing a flaky test —
   and have two or three people describe how they did it last time, run by run. The question that
   pays is why one person's version worked better than another's on the same job.
2. **Ask for the discarded runs first, and have the most senior person answer first.** On a team
   told to adopt these tools and not told how, "here is what did not work" is an expensive sentence
   until somebody spends the first one. Without it the comparison has nothing to compare: every
   account is a success, and successes do not explain each other.
3. **Promote an artefact, not an anecdote.** Every practice that survives the comparison leaves the
   room as a file — a skill, a line in the shared agent file, an item in the review template. If
   nobody will write the file, the practice was not worth the hour.
4. **Have someone else write the description.** A skill is routed on its `name` and `description`
   alone, never on its body
   ([*Package repeatable expertise*](../harness/package-repeatable-expertise.md)). A skill described
   in its author's vocabulary stays invisible to everyone else. The colleague who did not write it
   writes the description, in the words their own request would use.
5. **Move it to where everyone loads it, then check on someone else's machine.** Shared skills into
   the repository's skills directory, shared conventions into the committed context file, personal
   material out of the repository. Verify on a checkout that is not the author's: instructions that
   silently fail to load are the Agent File That Never Arrived ([*Write the agent file that actually
   gets read*](../context/write-the-agent-file-that-actually-gets-read.md)).
6. **Remove something every time.** A skill nobody has triggered since the last harvest, an agent
   file line about a tool the team replaced, a card describing a service deleted in June. A library
   that only ever grows becomes the Context Landfill ([*Write the agent file that actually gets
   read*](../context/write-the-agent-file-that-actually-gets-read.md#failure-mode)) at team scale.

Everyone has the same tools. What a team can actually differentiate on is the rate at which one
person's discovery becomes everyone's default, and that rate is set by two costs: writing a thing
down, and taking it back out. So write in a form that is cheap to change — small files, one subject
each, dated, none of them depending on another — because a good half of what you record will be
wrong within two model releases, and the only defence available is that being wrong costs a two-line
edit. The exchange rate is a recurring hour nobody looks forward to, plus the loss of some genuinely
good personal practice that turns out not to survive being generalised.

## Worked example

`lodestone`, a claims-processing platform — C# services behind a TypeScript front end — where nine
engineers had been using agents for about a year and had never compared notes on purpose. The first
harvest ran for an hour and covered one job: writing a claims adapter for a new insurer's feed.

Three people described their last one. Two accounts were nearly identical. The third was much
faster, and the difference was a skill sitting in that engineer's home directory that nobody else
had ever seen:

```markdown
---
name: adapter
description: Adapter conventions for claims ingest.
---
```

The skill was good. The description had been written by somebody who already knew the skill existed.
A colleague who had never seen it rewrote the frontmatter from the request end, using sentences they
would actually have typed:

```markdown
---
name: claims-adapter
description: Write or change a claims adapter for an insurer feed — field mapping, the
  required-field policy, and the fixture pair every adapter needs. Use when asked to add
  support for a new insurer, when an insurer changes their file format, or when an adapter
  is dropping fields.
---
```

It moved to `.claude/skills/claims-adapter/`, and the same session removed two things: a skill for a
deployment process retired in the spring, and four lines in `AGENTS.md` describing a linter the team
had replaced.

Not everything survived. The engineer who wrote agent files in a shape that got the test written
first could not reconstruct the shape under questioning, and three attempts at writing it down
produced advice indistinguishable from "write a clear agent file". It was left alone rather than
promoted, and the note from the session says so. A month later the skill had fired for six of the
nine engineers; the other three had not written an adapter.

The two deletions took forty seconds and were the only part of the hour nobody argued about.

## Failure mode

**The Showreel.** The team meets to share what works, and everyone shares what worked. Each person
demonstrates their best run — four files and a passing suite in eleven minutes — and nobody mentions
the three attempts that morning that went nowhere, because the session was called by somebody who
would like adoption to be going well and the room can read a temperature. What comes out is a
library assembled from everyone's best day, which reproduces for nobody on an average one.

The tell is a shared library that grows every session beside a team channel where the same questions
keep getting asked. The second tell is that you cannot remember the last time anyone in the room
described a run that failed, on a technology whose failures are its most-discussed feature.

## Checklist

- [ ] The session compared one named job that several people do, not tools in general
- [ ] Discarded and failed runs were asked for explicitly, and someone senior answered first
- [ ] Every practice that survived left the room as a committed file, not as a note
- [ ] Descriptions and triggers were written by somebody other than the artefact's author
- [ ] Shared material is in the repository; personal material is outside it
- [ ] The shared material was verified to load on a machine other than the author's
- [ ] Something was deleted in the same session as something was added
- [ ] Files are small, single-subject, dated, and do not depend on each other

**See also:** [*Package repeatable expertise*](../harness/package-repeatable-expertise.md) · [*Write
the agent file that actually gets read*](../context/write-the-agent-file-that-actually-gets-read.md)
· [*Build the working agreement*](build-the-working-agreement.md)
