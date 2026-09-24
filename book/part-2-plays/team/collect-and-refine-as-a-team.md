# Collect and refine as a team

## Problem

Three people on the team have each worked out something that makes these tools noticeably better,
and none of the three knows about the other two. One has a skill in their home directory that gets a
fiddly procedure right every time. One stopped letting the agent near the migration folder months
ago and has never said why. One writes task briefs in a shape that reliably gets the test written
first, and could not tell you what the shape is. Nobody is hiding anything; it never came up. The
team pays the discovery cost three times and collects the benefit once each.

## The play

Run a recurring harvest: compare how people actually work, promote what wins into a file anyone
loads, take out as much as you put in, and raise one bar each time.

1. **Compare on one task shape, not in general.** "What are you using?" produces a list of tools.
   Take a job the whole team does, such as writing an adapter or chasing a flaky test, and have two
   or three people describe how they did it last time, run by run. Ask why one version beat another.
2. **Ask for the discarded runs first, and have the most senior person answer first.** On a team
   told to adopt these tools and not told how, "here is what did not work" is an expensive sentence
   until somebody spends the first one. Without it every account is a success, and successes do not
   explain each other.
3. **Promote an artefact, not an anecdote.** Every practice that survives leaves the room as a file:
   a skill, a line in the shared agent file, an item in the review template. If nobody will write
   the file, the practice was not worth the hour.
4. **Have someone else write the description.** A skill is routed on its `name` and `description`
   alone, never on its body ([*Package repeatable
   expertise*](../harness/package-repeatable-expertise.md)). One described in its author's
   vocabulary stays invisible to everyone else. The description comes from a colleague, in the words
   their own request would use.
5. **Move it to where everyone loads it, then check on someone else's machine.** Shared skills go in
   the repository's skills directory, shared conventions in the committed agent file, personal
   material outside it. Instructions that silently fail to load are the Agent File That Never
   Arrived ([*Write the agent file that actually gets
   read*](../context/write-the-agent-file-that-actually-gets-read.md)).
6. **Take one thing out and raise one bar, every time.** Delete a skill nobody has triggered since
   the last harvest, or an agent file line about a tool the team replaced. A library that only grows
   becomes the Context Landfill ([*Write the agent file that actually gets
   read*](../context/write-the-agent-file-that-actually-gets-read.md#failure-mode)) at team scale.
   Then tighten one check the saved time can pay for: a compiler setting, a lint rule, a security
   scan. Enforce it in CI, where nobody has to remember it, and date it in the session note.

Everyone has the same tools. What a team can differentiate on is the rate at which one person's
discovery becomes everyone's default, and two costs set that rate: writing a thing down, and taking
it back out. So keep files small, single-subject, dated, and independent, because half of what you
record will be wrong within two model releases. Easy output makes today's practice feel like the
top. It is a local one, and everyone else keeps moving: the Comfortable Peak ([*The failure modes
worth
naming*](../../part-3-where-it-struggles/the-failure-modes-worth-naming.md#the-comfortable-peak)).
The exchange rate is a recurring hour nobody looks forward to, some good personal practice that
does not survive being generalised, and builds that fail on code that passed last week.

## Worked example

`lodestone`, a claims-processing platform with C# services behind a TypeScript front end, had nine
engineers who had used agents for about a year and had never compared notes on purpose. The first
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

The skill was good. Somebody who already knew the skill existed had written the description. A
colleague who had never seen it rewrote the frontmatter from the request end, using sentences they
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

It also raised one bar. Adapters were now quick, and the last two ingest bugs had both been nulls
from an insurer's file. So the ingest project turned nullable warnings into errors:

```xml
<PropertyGroup>
  <Nullable>enable</Nullable>
  <WarningsAsErrors>nullable</WarningsAsErrors>
</PropertyGroup>
```

CI already built that project, so nobody had to remember the rule. The session note got a dated
line: what was raised, and why. The first build failed on months of old warnings, and fixing them
took the next day.

Not everything survived. The engineer who wrote task briefs in a shape that got the test written
first could not reconstruct the shape under questioning. Three attempts at writing it down
produced advice indistinguishable from "write a clear task brief". It was left unpromoted, and the
session note says so. A month later the skill had fired for six of the nine engineers; the other
three had not written an adapter.

The two deletions took forty seconds and were the only part of the hour nobody argued about.

## Failure mode

**The Showreel.** The team meets to share what works, and everyone shares what worked. Each person
demonstrates their best run: four files and a passing suite in eleven minutes. Nobody mentions the
three attempts that morning that went nowhere. Somebody who would like adoption to be going well
called the session, and the room can read a temperature. What comes out is a library
assembled from everyone's best day, which reproduces for nobody on an average one.

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
- [ ] Every session deleted something and raised one check, enforced in CI and dated
- [ ] Files are small, single-subject, dated, and do not depend on each other

**See also:** [*Package repeatable expertise*](../harness/package-repeatable-expertise.md) · [*Write
the agent file that actually gets read*](../context/write-the-agent-file-that-actually-gets-read.md)
· [*Build the working agreement*](build-the-working-agreement.md)
