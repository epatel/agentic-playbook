# What this book assumes about you

You have run an agent on real work this week. Not a demo and not a toy repository — something with a
deadline attached and colleagues who will read the result. At least one of those runs produced
something you shipped. At least one produced something you deleted, and you are not entirely certain
what the difference was.

That is the reader. Everything that follows assumes it, and a book that assumes something different
would be a different book.

## What is assumed

- **You write code for a living**, and have for long enough to have preferences. Nothing here
  explains what a pull request is, why tests are useful, or what a language server does.
- **You have one of these tools installed and use it most days.** Which one matters less than the
  vendors would like. The plays are written against the shape these tools share, and name specific
  products only inside worked examples.
- **You can read a diff you did not write**, and tell a good one from a plausible one. This turns
  out to be the load-bearing assumption of the entire book.
- **You have already formed opinions from experience**, and some of them contradict the opinions of
  the person sitting two desks away. That disagreement is the situation this book is written into,
  not a problem to be resolved before reading.

## What is not assumed

- **That you like any of this.** Enthusiasm is not a prerequisite, and in a reviewer it is closer to
  a liability.
- **That your team has a position.** Most do not have one they could state in the same words twice.
- **That you have budget authority, a sanctioned tool, or a platform team who has thought about this
  on your behalf.** Several plays are written to be run by one person without asking permission, and
  they say so where that is true.
- **That you know what MCP stands for**, what a skill is, or how a subagent differs from a workflow.
  Terms are defined where they are first used and collected in the
  [*Glossary*](../appendices/glossary.md).
- **That you work on greenfield.** Most examples here are in code that already exists and that
  somebody will be upset about if it breaks.
- **That you are behind.** There is a genre of writing about this subject whose function is to make
  the reader anxious enough to keep reading. This is not that genre. Nobody is ahead, because there
  is no agreed direction in which to be ahead.

## The situation you are probably in

Most readers of this book have been told to use these tools and have not been told how. The mandate
arrives from somewhere above; the method does not arrive at all; the assessment happens anyway. What
counts as good use, what changes about review, what changes about estimates, who is accountable when
an agent-authored change causes an incident — those questions are usually left with the person
holding the keyboard.

This book takes that as the reader's condition rather than as something to escalate. It is not
addressed to your manager and contains nothing worth forwarding to them. What it contains is a set
of moves an individual developer or a team lead can make without waiting for direction.
[*Team*](../part-2-plays/team/index.md) adds the material for a conversation with colleagues, which
is more productive than a conversation with a mandate.

## What this book will not do

It will not sell you anything. There is no vendor relationship behind any tool named here, and no
claim that any of this is inevitable: that claim cannot be checked, and the people making it are
usually also selling the remedy.

It will not give you a number it cannot source. That constraint costs more than it sounds like it
should, because the published evidence on AI-assisted development is considerably worse than the
discourse implies. Nearly all of it measures autocomplete or chat rather than agents. The most
careful randomised trial of recent tools had its follow-up abandoned by its own authors, once too
many developers declined to do tasks without AI. That collapse is itself the most interesting result
in the field, and [*Where the time actually
goes*](../part-3-where-it-struggles/where-the-time-actually-goes.md) reports it in full. Where this
book hedges, that is why. Where it gives a figure, the figure is dated in the sentence and traceable
to a research note in [`notes/research/`](../../notes/research/).

## Read the plays in any order

Not front to back, and not in one sitting.

The plays are the point. Six suites, each play self-contained under the same five headings. Plays
link to each other where the dependency is real. There is no required order. Most of them are
preparation work, in the sense [*The four areas, re-weighted*](the-four-areas-reweighted.md) gives
the word.

*Where It Struggles* is where the book argues against itself: [*What agents are reliably bad
at*](../part-3-where-it-struggles/what-agents-are-reliably-bad-at.md), [*The failure modes worth
naming*](../part-3-where-it-struggles/the-failure-modes-worth-naming.md), [*Where the time actually
goes*](../part-3-where-it-struggles/where-the-time-actually-goes.md), and [*What is genuinely
contested*](../part-3-where-it-struggles/what-is-genuinely-contested.md). If you are sceptical,
start there. It is the part that decides whether the rest is worth your week.

## What it costs

Several plays ask you to give something up. Speed on the first pass. A habit that currently feels
productive. The specific pleasure of watching a very large diff appear in under a minute. Where a
play has an exchange rate, it states it, because a play that only lists benefits is an advertisement
with a checklist attached.

## What will go stale, and how to tell

Parts of this book will be wrong within a year, and which parts is predictable: anything carrying a
model name, a price, a context-window size, or a benchmark score. Those are dated in the sentence
wherever they appear, so that you can discount them yourself rather than trusting a publication date
and hoping.

What is meant to survive is the shape. "Roughly an order of magnitude cheaper per token" outlives a
price change; a pricing table does not. "Split the task at the first boundary where both halves
would be needed at once" outlives the tool it was first written for. Where a figure and a shape
disagree in this book, trust the shape and go and check the figure.

Your own practice goes stale the same way. When the model changes, re-test the parts that rest on
it, and retry one thing the team still does the easy way, because the ceiling may have moved too. A
team that only re-tests keeps up. One that also retries climbs.

## Where to start

The tools are installed, you are already using them, and whatever purchase decision existed was made
somewhere above your head a while ago. What is missing is the practice.

The rest of this book is one attempt at it. Start wherever your week hurts.
