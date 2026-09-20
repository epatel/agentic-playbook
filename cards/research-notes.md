# Research notes — the output contract

The book makes claims about tooling conventions, orchestration patterns, productivity evidence,
and token economics. Research passes gather that evidence *before* the writing starts, so
chapters cite reality rather than vibes.

Research output is **notes, not prose**. A research task does not write book chapters. It
produces material that a later writing task draws from. Resist the urge to draft the chapter you
can see forming — a different agent will write it, and pre-written prose in the wrong voice is
harder to use than good notes.

## Where agent files go

One file per research note in `notes/research/`, lowercase and hyphenated, named for the subject:
`mcp-adoption.md`, `token-pricing-tiers.md`. Create the directory if it does not exist.

Several small agent files beat one enormous one. A writer looking for pricing numbers should not have
to read a survey of orchestration frameworks to find them.

## Agent file format

```markdown
# <Subject>

**Question asked:** what this agent file was commissioned to answer.
**Researched:** <date>
**Confidence:** high / medium / low — and why.

## Findings

- Claim, stated plainly. [1]
- Another claim. [2]

## What is standardised vs. one vendor's habit

...

## Contradictions and gaps

Where sources disagree, or where the answer could not be established.

## Sources

[1] Title — URL — accessed <date>
[2] Title — URL — accessed <date>
```

## Citation rules

- **Every factual claim carries a source.** If you cannot source it, it is not a finding — put
  it under gaps, or label it explicitly as inference.
- **Prefer primary sources.** Vendor documentation over a blog post summarising that
  documentation; the published study over the article reporting on it.
- **Date everything.** This subject moves fast, and a 2024 claim about model pricing or context
  limits may be wrong by the time the book ships. An undated finding is unusable.
- **Record the disagreement.** Where sources conflict, say so rather than picking a winner. The
  book's credibility rests more on honest uncertainty than on confident numbers.
- **Separate what is standardised from what is one vendor's convention.** This distinction
  matters throughout the book and is easy to lose once a finding is reduced to a sentence.

## Numbers

Quote figures exactly as the source gives them, with units and date attached. Do not round,
convert, or combine figures from different sources into a derived number without showing the
arithmetic and flagging it as derived.
