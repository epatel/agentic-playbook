# Before Git, before Scrum, before this

Agentic coding tools work, but nobody has an agreed way of working with them yet. That is normal.
The industry has been here twice within living memory, with version control and with process. Both
times the tool was ready years before the discipline, and the discipline arrived by argument, not by
release note. Knowing that shape tells you what to expect, and what is worth writing down now.

Two developers on the same team, the same repository, the same agent. One writes three sentences of
context and steers in conversation. The other maintains a four-hundred-line *agent file*, the
`AGENTS.md` or `CLAUDE.md` every session loads, fires off a task, and goes to get coffee. Both ship
work that passes review. Neither can tell you why their approach beats the other's. Put them in a
room to settle it and they would reach for anecdotes, because anecdotes are all either of them has.
Neither is wrong. Nobody has yet written an answer down and had it argued with for long enough.

## Git took a decade to become a discipline

The tool was ready in 2005. Agreeing how to use it took another ten years.

Version control before Git existed, but it was defensive: built to stop two people touching the same
file, not to reconcile their work afterwards. Walter Tichy's 1985 RCS paper has a section titled
"Locking: A Controversial Issue", and it is unambiguous: "At most one programmer at a time may lock
a particular revision, and only this programmer may check in the succeeding revision." Breaking
somebody's lock sent them an automatic email. Tichy reports the effect: programmers broke locks
"only in real emergencies, or when a co-worker resigns and leaves locked revisions behind."

Git's first commit landed on 7 April 2005, describing it as "the information manager from hell".
Version 1.0 followed that December. Then, for years, little changed. The Eclipse Community Survey
asked developers for their primary source control system. In 2011, six years in, Subversion was on
51.3%, CVS on 13.3%, and Git and GitHub together on 12.8%. Stack Overflow's 2018 survey, a different
question to a different population, put Git at 87.2%. In that same survey, 7.9% of respondents
reported backing work up as zip files.

Installing Git took an afternoon. The ten years went on agreeing what a commit was for, how large a
branch should be, and that somebody other than the author reads the diff before it lands.

The pull request shows this most clearly. GitHub shipped it on 23 February 2008, and the
announcement post describes it, in full, as a way to "tell people who forked from you they need to
pull". It is a notification. GitHub did not call it code review until "Pull Requests 2.0" in August
2010, two and a half years later. Even then few teams reviewed. Researchers examining 1.9 million
pull requests across 2012 and 2013 found 14% of active repositories using pull requests at all, and
12% of pull requests carrying a review comment. Sources are in
[`notes/research/convergence-history.md`](../../notes/research/convergence-history.md).

## Scrum took fifteen years, and what spread was the vocabulary

Takeuchi and Nonaka published "The New New Product Development Game" in the *Harvard Business
Review* in early 1986. They called what they described the rugby approach. The word "scrum" appears
exactly once in the article, as a section heading. Ken Schwaber borrowed the metaphor and named the
method at a workshop in 1995: "we call the approach the SCRUM methodology … after the SCRUM in
rugby". That paper has sprints and a backlog. It has no daily meeting and no retrospective. The
words a developer now uses without thinking accreted over fifteen years, and the Scrum Guide first
collected them in one place in 2010.

For most of that period the field could not agree on a name for itself. The term before Snowbird was
"Light", which nobody liked. Alistair Cockburn, in Jim Highsmith's account, did not want "to be
referred to as a lightweight attending a lightweight methodologists meeting", which "sounds like a
bunch of skinny, feebleminded lightweight people trying to remember what day it is". Seventeen
people from eight named approaches spent three days in Utah in February 2001 and produced four value
statements. Not a method. A vocabulary.

Teams took it up more slowly than the retelling suggests. In the third quarter of 2010, fifteen
years after Schwaber's paper, Forrester and *Dr. Dobb's* asked 1,023 IT professionals which
methodology matched their process. Scrum came back at 12.3%, and nearly 29% reported using no formal
process at all. By Stack Overflow's 2018 survey, with roughly 59,000 respondents, Agile was at 85.4%
and Scrum at 62.7%.

In a study published in 2015, researchers interviewed ten companies running Scrum. Every one had
varied it, to the point of "a substantial deviation from Scrum as initially proposed". What varied
least was sprint length, the events, team size, and requirements engineering: mostly the vocabulary.
What varied was roles, estimation, and quality assurance, which is everything with substance in it.

That reads like an indictment, and it is not one. Scrum's value was never that it was correct. It
was that a developer could change employer and know, on the first morning, what "sprint", "backlog",
and "retro" meant. Shared words let two people disagree, instead of talking past each other for a
quarter. Nobody can buy them or mandate them.

## The practice around the tools is unsettled, and so are the words

The tools work. Hand a capable agent a described change across a dozen files and you will usually
get back something that compiles and does much of what you asked. What nobody agrees on is
everything around that. Few teams could answer these out loud, in the same words:

- What belongs in the agent file the agent reads, and what is noise that costs attention and money.
- Whether that agent file is versioned with the code or lives in one person's home directory.
- Who reviews the diff, against what standard, and whether that standard matches a colleague's.
- Whether the prompt that produced the diff is an artefact worth keeping.
- Whether two people can run agents against the same repository at once without ruining each other's
  afternoon.

None of these are hard the way an algorithm is hard. They are unsettled, which is worse: a hard
question at least has an answer somebody can look up.

The words are missing too. A run sometimes reaches a correct solution partway through, keeps going,
and overwrites it. This has been measured
([`failure-modes.md`](../../notes/research/failure-modes.md)), and everyone who uses these tools
daily has watched it happen. But it has no agreed name, so raising it in a review costs a sentence
of explanation every time, and mostly nobody raises it. This book calls it the Vanishing Fix, and
collects the others alongside it in [*The failure modes worth
naming*](../part-3-where-it-struggles/the-failure-modes-worth-naming.md).

## The analogy breaks in three places

An analogy that only flatters the present is not worth carrying, and this one fails three ways.

The pressure runs the other way. Practitioners built Git and Scrum for their own problems, and both
spread from below, by persuasion. The current tools ship from vendors every week, and the vendors
gain when teams adopt them before anyone knows how to use them well. Plenty of developers are told
to use them by someone who has not said how, and are judged on the result anyway. That did not
happen with Git.

The ground moves. Git 1.5 did not get better at merging while you slept. Every convention you adopt
here assumes something about what the model cannot yet do reliably, and some of those assumptions
expire without notice.

Neither earlier wait was a crisis. Teams shipped good software on CVS with locked files and a
process their tech lead invented over a weekend. The decade of argument was not a decade of failure.
It was the decade in which people argued, and arguing is the only way a question like this gets
settled.

## What will converge is a habit, not a set of conventions

Git's practices settled because Git held still long enough to argue about. The model does not hold
still, so a practice built on what it cannot yet do may never get that long. What can settle is a
habit. Write down what the team does. Check the work somewhere other than the agent's account of it.
Date the parts that rest on the model, so you know to re-test them when it changes. And keep raising
the bar, because nothing else around you holds still either. This book practises the habit, and
[*What this book assumes about you*](what-this-book-assumes-about-you.md) says how.

This book is not the consensus; nobody has one to offer. It is one working set of practices, written
in enough detail to disagree with precisely. The reason to write it down is the same reason somebody
eventually wrote down what a good commit message looks like. Not because the answer was obvious.
Because writing it down makes disagreeing with it cheap, and lets you notice when it stops being
true.
