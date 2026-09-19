# Package repeatable expertise

## Problem

You are walking the agent through the same eleven-step procedure for the third time this month, from
a scratch file kept open in another window because the order of the steps matters and two of them
are easy to get backwards. It works every time you do it. It also means the procedure exists in one
place — your window — and the colleague who joined in June does it slightly differently, which
nobody has noticed because both versions pass review. The problem is not that the knowledge is
missing. It is that the only copy of it that reaches the agent is the one you type.

## The play

Move the procedure into a *skill*: a folder holding a `SKILL.md` of metadata plus instructions,
alongside any scripts and reference files it needs, which the agent loads when its situation arrives
rather than in every session.

1. **Wait for the third time, then convert.** Two corrections of the same kind is a line in the
   project brief. A multi-step procedure you have walked the agent through three times is a skill.
   Below that threshold you are writing artefacts for a situation you cannot yet describe.
2. **Cut the boundary at a situation, not a subject.** "What we do when a search index mapping
   changes" is a skill: it has a trigger, so something can decide when to load it. "Search" is not.
   A subject-shaped skill has no moment at which it applies, so it either never loads or loads
   constantly, and it grows until it is a second brief. The test is whether you can finish the
   sentence "use this when…" in one clause, without the word "and".
3. **Write the `description` before the body, as when-plus-what.** Discovery matches on `name` and
   `description` alone; the body is never consulted when deciding whether the skill is relevant
   ([`skills.md`](../../../notes/research/skills.md)). Put the words a real request would use into
   it, not the words you would use in a directory listing.
4. **Put determinism in a script and bulk in a reference.** Anything you would rather have run than
   reasoned about — a validator, a count check, a query — goes in `scripts/`, because a script's
   code never enters the context window and only its output does. Long material goes in
   `references/` and costs nothing until a step reads it.
5. **Point at references from a specific step.** "See `references/analysers.md`" invites the agent
   to read nine hundred lines; "for fields with custom analysers, read the custom-analyser section
   of `references/analysers.md`" does not.
6. **Stay on `name` and `description` if anyone outside your harness will use it.** Those two fields
   are the standard. The extended frontmatter one vendor offers — pre-approved tools, a model
   choice, invocation controls — is that vendor's, and a skill written against it does not travel.

The arithmetic underneath this is progressive disclosure. A skill costs only its metadata until it
fires — roughly a hundred tokens each, in the published figures — so thirty of them is a few
thousand tokens of permanent context carrying an arbitrary amount of procedure behind it. The same
thirty procedures written into the always-loaded brief are tens of thousands of tokens, nearly all
of them irrelevant to whatever you are doing today, and competing for attention with the part that
is not. The exchange rate is certainty of delivery. A brief always arrives and is always competing
with itself; a skill arrives only when its description matched a request you did not write, and you
cannot verify that match in advance.

## Worked example

`kestrel`, a Go search-indexing service, where changing an index mapping has a procedure: reindex
into a new alias, dual-write both indices, verify document counts, cut the alias over, and only then
drop the old index. It lived in a wiki page last edited in February and in one engineer's terminal
history.

The first version of the skill was written in four minutes and did nothing for two weeks:

```markdown
---
name: index-mapping
description: Index mapping utilities for kestrel.
---
```

Nothing errored. The agent kept writing reasonable reindex code that skipped the dual-write, which
is the step that makes the cutover reversible. The rewrite changed the frontmatter more than the
body:

```markdown
---
name: index-mapping-change
description: Change a search index mapping safely by reindexing into a new alias, dual-writing,
  verifying counts, and cutting over. Use when asked to add or change a field in an index
  mapping, reindex an index, or resolve a mapping conflict.
---

# Changing an index mapping

1. Run `scripts/mapping_diff.py <index>` and read its output.
2. Create the new index and alias, then dual-write until `scripts/count_check.py` reports
   parity.
3. Cut the alias over. Drop the old index only after the cutover has held for one deploy.
4. For fields with a custom analyser, read the custom-analyser section of
   `references/analysers.md` before writing the mapping.
```

Saved as `.claude/skills/index-mapping-change/SKILL.md`, it fired the same afternoon, on a request
that never used the word skill — somebody asked to add a `language` field to the product index.

It was not clean. Step 4 originally said "see `references/analysers.md`", and the agent read all
nine hundred lines of it into the session before writing four lines of mapping; naming the section
fixed that. The wiki page also still exists, and is still wrong, which is a problem the skill did
nothing about.

## Failure mode

**The Unsummoned Skill.** The skill is written, reviewed, and committed, and the agent does the job
the long way every time. Nothing errors, because from the harness's point of view nothing went
wrong: the metadata loaded exactly as designed, the request did not match it, and a non-match is not
an event anyone logs. This is not the Brief That Never Arrived
([*Write the brief the agent actually reads*](../context/write-the-brief-the-agent-actually-reads.md#failure-mode))
— there the file never arrived; here it arrived and lost a match. The cause is almost always the
`description`, which is the entire routing table and the field people write last, in ten words,
describing what the skill is rather than when to reach for it.

The tell is that you can say out loud when you would use the skill, and that sentence does not
appear in its description. The second tell is catching yourself typing the procedure into the chat
window while the skill sits in the same repository, unmentioned.

## Checklist

- [ ] The procedure has been walked through at least three times, so it is worth an artefact
- [ ] It covers one situation with a nameable trigger, not a subject area
- [ ] `description` says both what it does and when to use it, in the words a request would use
- [ ] Deterministic steps are scripts under `scripts/`, not prose for the agent to re-derive
- [ ] Bulk material is in `references/` and is pointed at by a specific step, naming a section
- [ ] The body is short enough to follow in one pass, with detail pushed down a level
- [ ] Frontmatter is `name` and `description` only, if anyone outside your harness will use it
- [ ] It has fired at least once on a request that did not name it

**See also:**
[*Write the brief the agent actually reads*](../context/write-the-brief-the-agent-actually-reads.md) ·
[*Starve the context*](../context/starve-the-context.md)
