# Before Git, before Scrum, before this

Two developers on the same team, the same repository, the same agent. One writes three sentences of
context and steers in conversation. The other maintains a four-hundred-line brief, fires off a task,
and goes to get coffee. Both ship work that passes review. Neither can tell you why their approach
beats the other's, and if you put them in a room to settle it they would reach for anecdotes,
because anecdotes are what either of them has.

Nothing is wrong here. There is no agreed answer, because nobody has written one down and had it
argued with for long enough. That is a specific condition with a recognisable shape, and this
industry has been in it twice before within living memory.

## The tool was never the hard part

Version control before Git was not absent. It was defensive — built to stop two people touching the
same file rather than to reconcile their work afterwards. Walter Tichy's 1985 RCS paper has a
section titled "Locking: A Controversial Issue", and it is unambiguous: "At most one programmer at a
time may lock a particular revision, and only this programmer may check in the succeeding revision."
Breaking somebody's lock sent them an automatic email. Tichy reports the effect: programmers broke
locks "only in real emergencies, or when a co-worker resigns and leaves locked revisions behind."

A decade later, Microsoft's Visual SourceSafe still allowed "only one user at a time to check out a
file" in its default work style, with concurrent editing a mode an administrator had to switch on.
Subversion shipped in 2000 and did not get automatic merge tracking until version 1.5 in June 2008;
until then, by its own manual's account, a branch left alone too long could be "near-impossible to
merge" back "without a huge number of conflicts". For most of a decade the dominant tool punished
the practice that is now the default.

Git shipped on 7 April 2005, with cheap branches and a three-way merge, under a commit message
describing it as "the information manager from hell". And then, for years, mostly nothing happened.
The Eclipse Community Survey asked developers for their primary source control system; in 2011, six
years in, Subversion was on 51.3%, CVS on 13.3%, and Git and GitHub together on 12.8%. Stack
Overflow's 2018 survey, thirteen years in, put Git at 87.2%. In that same survey, 7.9% of
respondents reported backing work up as zip files.

That decade usually gets told as a story about installing software, which is the least interesting
thing about it. Installing Git took an afternoon. What took ten years was agreeing what a commit was
for, how large a branch should be, and that somebody other than the author reads the diff before it
lands.

The pull request is the clearest case. GitHub shipped it on 23 February 2008, and the announcement
post describes it, in full, as a way to "tell people who forked from you they need to pull". It is a
notification. GitHub did not call it code review until "Pull Requests 2.0" in August 2010, two and a
half years later, and even then the practice was thin: researchers examining 1.9 million pull
requests across 2012 and 2013 found 14% of active repositories using pull requests at all, and 12%
of those carrying a review comment.

The tool was ready in 2005. The discipline arrived by argument rather than by release note. Sources
are in [`notes/research/convergence-history.md`](../../notes/research/convergence-history.md).

## The same shape, over a longer timeline

Takeuchi and Nonaka published "The New New Product Development Game" in the *Harvard Business
Review* in early 1986. They called what they were describing the rugby approach; the word "scrum"
appears exactly once in the article, as a section heading. Ken Schwaber borrowed the metaphor and
named the method at a workshop in 1995 — "we call the approach the SCRUM methodology … after the
SCRUM in rugby". That paper has sprints and a backlog. It has no daily meeting and no retrospective.
The vocabulary a developer now uses without thinking was not delivered; it accreted over fifteen
years, and was first written down in one place by the Scrum Guide in 2010.

For most of that period the field could not agree on a name for itself. The term before Snowbird was
"Light", which nobody liked. Alistair Cockburn, in Jim Highsmith's account, did not want "to be
referred to as a lightweight attending a lightweight methodologists meeting", which "sounds like a
bunch of skinny, feebleminded lightweight people trying to remember what day it is". Seventeen
people from eight named approaches spent three days in Utah in February 2001 and produced four value
statements. Not a method. A vocabulary.

Adoption was slower than the retelling suggests. In the third quarter of 2010 — fifteen years after
Schwaber's paper — Forrester and *Dr. Dobb's* asked 1,023 IT professionals which methodology matched
their process. Scrum came back at 12.3%, and nearly 29% reported using no formal process at all. By
Stack Overflow's 2018 survey, with roughly 59,000 respondents, Agile was at 85.4% and Scrum at
62.7%.

What spread, though, was not the method. When researchers interviewed ten companies running Scrum in
2015, every one had varied it, to the point of "a substantial deviation from Scrum as initially
proposed". What held constant across all ten was sprint length, the events, and team size — the
vocabulary. What varied was roles, estimation, and quality assurance: everything with substance in
it.

That reads like an indictment and is not one. The value was never that Scrum was correct. It was
that a developer could change employer and know, on the first morning, what "sprint", "backlog", and
"retro" meant. Shared words are what let a disagreement be a disagreement rather than two people
talking past each other for a quarter, and they cannot be bought or mandated into existence.

## Where that puts this

The tools work; that is not the open question. Hand a capable agent a described change across a
dozen files and you will usually get back something that compiles and does much of what you asked.

What does not exist is everything around that. Consider how few of these your team could answer out
loud in the same words:

- What belongs in the brief the agent reads, and what is noise that costs attention and money.
- Whether that brief is versioned with the code or lives in one person's home directory.
- Who reviews the diff, against what standard, and whether that standard matches a colleague's.
- Whether the prompt that produced the diff is an artefact worth keeping.
- Whether two people can run agents against the same repository at once without ruining each other's
  afternoon.

None of these are hard in the way a hard algorithm is hard. They are unsettled, which is worse: a
hard question at least has an answer somebody can look up.

The vocabulary is missing too. There is a thing agents do where a run arrives at a correct solution
partway through, keeps going, and overwrites it; it has been measured
([`failure-modes.md`](../../notes/research/failure-modes.md)), and everyone who uses these tools
daily has watched it happen. It has no agreed name, so raising it in a review costs a sentence of
explanation every time, which is roughly why it does not get raised. This book calls it the
Vanishing Fix and collects the others alongside it in [*The failure modes worth
naming*](../part-3-where-it-struggles/the-failure-modes-worth-naming.md).

## Where the analogy breaks

An analogy that only flatters the present is not worth carrying. Three ways this one does not hold.

The direction of pressure is reversed. Git and Scrum were built by practitioners for their own
problems and spread from below, by persuasion. The current tools ship from vendors on a weekly
release cadence, with a commercial interest in adoption arriving ahead of practice: plenty of
developers are told to use them by someone who has not said how, and assessed on the result anyway.
That did not happen with Git.

The substrate moves. Git 1.5 did not get better at merging while you slept. Every convention you
adopt here encodes an assumption about what the model cannot yet do reliably, and some of those
assumptions expire without notice — nothing in your repository will tell you which.

Neither previous interim was a crisis. Teams shipped good software on CVS with locked files and a
process their tech lead invented over a weekend. The decade of argument was not a decade of failure;
it was the decade in which the argument happened, which is the only way a question of this kind gets
settled.

## What this book is, given all that

This book is not the consensus. Nobody has one to offer, and anything claiming otherwise is selling
something. It is one working set of practices, written in enough detail to be disagreed with
precisely.

The reason to write down how your team works with agents is the same reason somebody eventually
wrote down what a good commit message looks like. Not because the answer was obvious. Because
writing it down is what makes disagreeing with it cheap.
