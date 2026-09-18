# Style guide

Read this before writing any prose for *The Agentic Playbook*. It defines the voice, the rules
that protect it, and four worked samples to pattern-match against. Structure — where files live,
how they are ordered, how they link to each other — is in [`README.md`](README.md). The shape of
an individual play is in [`TEMPLATE-play.md`](TEMPLATE-play.md).

The book has several authors and one voice. That only works if the voice is described in examples
rather than adjectives, which is what most of this file is.

## Who is talking

An experienced colleague who has been burned and finds it funny in retrospect. Someone who has
shipped this way for a while, is neither impressed nor alarmed by it, and has opinions that came
from consequences rather than from a keynote.

Not a vendor. Not a lecturer. Not a friend who has had one coffee too many.

Three tests before a sentence stays:

1. **Would you say it out loud to a competent peer?** That removes hype in one direction and
   talking down in the other.
2. **Does it survive 16:50 on a Friday?** Someone is copying a command out of this book while
   tired. Where that happens, the prose gets out of the way entirely.
3. **Is it true?** A joke that costs accuracy is cut. Every time. The register is dry because it
   is precise, not in spite of it.

## Where humour is allowed

Humour lives in the framing. It is how the book earns the right to be read end to end, and it is
also the first thing that makes a book untrustworthy when it leaks into the wrong place.

**Allowed:**

- Part and suite openers — the paragraph that establishes why anyone should care.
- The framing sentence of a play's Problem, if the situation is genuinely absurd. The absurdity is
  the joke; do not add a second one.
- The **names** of failure modes. This is the main outlet, and it is a generous one.
- A closing aside after a Worked example, once the reader is out of the procedure.
- Part III throughout. Honest accounting of where agents fail is the funniest material in the book
  and does not need help.

**Not allowed:**

- Inside a numbered step. Ever.
- Inside a Checklist.
- Inside a code block, or in a code comment inside one.
- Inside the Problem paragraph's description of symptoms — state those straight.
- Anywhere the reader is mid-task and cannot skip a line safely.

**Rate:** roughly one dry aside per screen of prose. Two in consecutive paragraphs reads as a bit,
and a bit is a different register from the one we are writing in.

## Banned outright

These are not judgement calls. The editorial pass removes them without discussion.

- **Exclamation marks.** The only exception is inside quoted real output, where they belong to the
  machine.
- **Emoji.** Especially as a punchline. Describing one in prose is fine; typing one is not.
- **The "unless…?" gag** and its relatives: rhetorical bait-and-switch ("AI won't take your job…
  unless?"), "plot twist:", "narrator voice:", "(spoiler: it didn't)".
- **Hype vocabulary:** revolutionary, game-changer, unlock, supercharge, 10x, seamless,
  effortless, magical, paradigm shift, next-level, superpower.
- **"Simply", "just", "obviously", "of course"** applied to the reader's work. If it were obvious
  they would not be reading the play.
- **The LLM cadence:** "It's not just X — it's Y", "Let's dive in", "In today's fast-paced world",
  "The key takeaway is", "At the end of the day", and rule-of-three lists that exist for rhythm
  rather than because there are three things.
- **Rhetorical questions as section transitions.** "So how do you fix this?" is a sentence that
  costs a line and delivers nothing.
- **Second-person scolding.** "You're doing it wrong" and "most developers make this mistake"
  both assume a reader who is not the one described in Part I.
- **Anthropomorphised moods.** The agent has behaviour, not feelings. "Output quality degrades
  once the window is roughly three-quarters full", not "the agent gets tired". "It will confidently
  produce X" is fine — that is a description of output, not an inner life.
- **The knowing wink.** "(ask me how I know)" is allowed once in the entire book, and it probably
  should not be.

## Passes / does not pass

| Does not pass | Passes | Why |
|---|---|---|
| "This will supercharge your workflow!" | "This removes about a third of the review load, in exchange for a slower first pass." | Claims a shape you can check |
| "Just scope the task properly." | "Split at the first boundary where the agent would need both halves in mind at once." | Actionable rather than aspirational |
| "The agent gets confused by long files." | "Past a few thousand lines, edits start contradicting earlier edits in the same run." | Behaviour, not mood |
| "Context rot 😬" | "**The Context Landfill**" | The name carries it; nothing else has to |
| "Let's dive into verification!" | "Verification is the part teams skip, and it is the part that decides whether any of this was worth it." | Opens with the argument, not with throat-clearing |
| "AI won't replace developers… unless?" | *(cut entirely)* | The gag has no second half worth writing |

## Mechanics

- **British English**, `-ise` endings: *standardise*, *recognise*, *behaviour*, *humour*.
- **Oxford comma**, always.
- **Present tense.** Second person for the reader — "you". "The agent" for the tool, never "the
  AI", "it" as a bare subject across sentences, or "your AI pair". No authorial "we"; the book
  does not narrate itself.
- **Sentence case for every heading**, including the fixed template headings.
- **Heading levels.** One `#` per file, matching its table-of-contents title. `##` for the five
  template headings in a play, or for top-level sections in a non-play chapter. `###` for
  subsections inside *The play*. Never `####` — needing it means the play should be two plays.
- **Backticks** for file paths, filenames, commands, flags, identifiers, and config keys.
- **Fenced blocks** always carry a language tag: `bash`, `text`, `markdown`, `json`, `python`,
  `mermaid`.
- **Wrap at 100 columns.** Never wrap inside a table row, a URL, or a fenced block.
- **Lists:** `-` for bullets, `1.` for ordered steps, `- [ ]` for checklist items so a reader can
  paste them into an issue.
- **Emphasis:** *italics* for the first use of a term and for play titles in cross-references;
  **bold** for a named failure mode on first use. Do not bold for general emphasis — it reads as
  shouting in a book that does not shout.
- **No YAML frontmatter.** GitHub renders it as a stray table at the top of the page.
- One blank line between blocks, no trailing whitespace, every file ends with a newline.
- **Diagrams are mermaid**, in fenced ```mermaid``` blocks, never ASCII art. See
  [`cards/standing-defaults.md`](../cards/standing-defaults.md).

## Volatile facts

Model names, prices, context-window sizes, and benchmark figures make prose concrete and give the
book an expiry date. The working line:

- Use a specific figure only when the point collapses without it.
- When you use one, date it in the sentence: "as of early 2026", or a parenthetical month.
- Prefer shape to figure. "Roughly an order of magnitude cheaper per token" survives a price
  change; a pricing table does not.
- **Never invent a measurement.** Timings, token counts, percentages, and study results are
  measured, cited to a brief in [`notes/research/`](../notes/research/), or not stated. A
  precise-looking number that came from nowhere is the single fastest way to lose this reader.

This is a working default rather than a locked decision; the editorial pass owns the final call on
how much the book dates itself.

## Naming failure modes

Failure modes are recurring characters, and the names are where most of the book's humour lives.
They are also load-bearing: a reader who can name a thing can raise it in a code review.

- **Title Case, with the definite article, as a noun phrase:** **the Context Landfill**, **the
  Confident Wrong Rewrite**, **the Green Suite That Tests Nothing**.
- **Bold on first use** in a play; plain thereafter.
- **Name the symptom, not the cause.** The reader recognises the thing before they understand it.
  "The Merged Hand" beats "Improper Working Tree Hygiene".
- **One name per phenomenon across the whole book.** Before coining one, check the running log in
  [`plans/agentic-playbook.md`](../plans/agentic-playbook.md); after coining one, append it there
  so the other authors see it. Two names for one failure is the defect the editorial pass is
  least able to fix cheaply.
- **The name carries the humour; the description does not.** Once you have named it, describe it
  straight: what it looks like, what the tell is, what it costs.

## Four samples

Each sample gives a passing paragraph, then a failing rewrite of the same material, then the
diagnosis. Pattern-match against these rather than re-deriving the register from the adjectives
above.

### Sample 1 — a suite opener

> Nobody reads the bill. It arrives, somebody posts a screenshot in the team channel with a
> raised-eyebrow reaction, and everyone resolves to be more careful, a resolution that historically
> lasts nine days. This is not a discipline problem. Token cost is the first line item most
> engineering teams have ever had that moves with how a developer chooses to phrase a sentence,
> and nobody has an intuition for it yet. These plays are about building one: what you are
> actually paying for, which jobs justify the expensive model, and how to recognise the tasks
> where the cheapest correct move is to close the laptop and write the code yourself.

**Passes:** the joke is an observed detail ("nine days"), not a gag; the paragraph still tells you
exactly what the suite contains; the last clause is the suite's actual thesis.

> Let's dive into the exciting world of token economics! Cost management is a game-changer for
> AI-powered teams. It's not just about saving money — it's about unlocking your team's full
> potential. Ready to take control of your spend?

**Diagnosis:** exclamation mark, three hype words, the "not just X — it's Y" cadence, a rhetorical
question as a transition, and after four sentences the reader knows nothing they did not know
before.

### Sample 2 — a Problem paragraph

> You hand the agent a task spanning eleven files and it does the first four well. Around the
> fifth it starts making changes that contradict the second, and by the ninth it is re-implementing
> a helper it wrote forty minutes earlier. Nothing errors. The diff is large, internally plausible,
> and wrong in three places you will find on Tuesday.

**Passes:** no joke at all — the situation carries itself. Concrete, escalating, and it ends on
the cost rather than on a summary.

> We've all been there! You give your AI buddy a big task and it goes off the rails. But don't
> worry — in this play we'll dive into how to scope tasks properly. Sound familiar?

**Diagnosis:** preamble instead of a problem, chumminess, an exclamation mark, a rhetorical
question, and a play that announces itself instead of starting. The Problem paragraph has one job:
put the reader in the room.

### Sample 3 — a step inside *The play*

> 3. Split the task at the first boundary where the agent would need to hold both halves in mind
>    at once. In practice that is a module edge or a change of data format: the migration script
>    and the code that reads the new format are two tasks, not one. Write the boundary into the
>    brief, so the second task does not re-derive it and disagree.

**Passes:** zero humour, imperative, one transferable heuristic, one concrete instance, and it
says what to do with the result. This is what the whole book reads like inside a procedure.

> 3. Split the task somewhere sensible (the agent will thank you). Just pick a natural boundary —
>    you'll know it when you see it!

**Diagnosis:** a joke inside a numbered step, an anthropomorphised mood, "just", an exclamation
mark, and an instruction that cannot be followed or checked. The reader is mid-task; nothing here
helps them act.

### Sample 4 — a named failure mode

> **The Context Landfill.** Every useful fact about the project goes into `CLAUDE.md`, because each
> one was useful on the day it was added and nothing has ever been removed. Eighteen months later
> the file opens with a note about a CI runner decommissioned last spring, and the convention that
> actually matters is on line 340. The agent reads all of it and weights it roughly evenly, which
> is the part people find surprising: the file did not become wrong, it became flat. The tells are
> a brief that has only ever grown, two instructions that contradict each other and have gone
> unnoticed because nobody reads the file end to end, and an agent that follows the current
> convention about half the time.

**Passes:** the name is the joke and it is delivered in three words; everything after it is
diagnostic. It ends on symptoms the reader can check against their own repo this afternoon.

> **Context Overload** is when you put too much stuff in your context file, which confuses the
> agent. Try to keep it short!

**Diagnosis:** the name describes an abstract cause rather than a recognisable symptom; "confuses"
gives the agent a mood; there are no tells, so the reader cannot self-diagnose; and the advice
belongs in *The play*, not here. Also an exclamation mark.

## Length

Budgets for the sections of a play are in [`TEMPLATE-play.md`](TEMPLATE-play.md). For everything
else: a Part I chapter runs 800–1,500 words, a suite opener 150–300, a Part III chapter 800–1,500.
Part I is the section most likely to sprawl, and the proportions in
[`cards/book-structure.md`](../cards/book-structure.md) are the point of the book, not a guideline.

## When in doubt

Cut the joke and keep the sentence. A dry book with a dozen good asides is the target; a book that
is visibly trying is the failure. The reader has been sold to enough this year.
