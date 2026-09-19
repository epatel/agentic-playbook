# Convergence history — source control and team process

**Question asked:** how long did it actually take for Git and for Scrum to go from "the tool
exists" to "the discipline is shared"? What did the pre-consensus period look like, concretely
enough that a reader who was there does not put the book down?

**Researched:** September 2026.

**Confidence:** high on the primary-document timeline and on the survey figures marked primary
below; medium on the Eclipse Community Survey's later years, which are partly secondary; low on
anything in the *Do not cite* section, which is there precisely because it did not survive.

This brief was produced for Part I, chapter *Before Git, before Scrum, before this*. It exists so
that the chapter's historical claims are checkable, and so the next author who reaches for the
same analogy does not re-run the same searches or fall into the same three traps.

---

## Findings — source control

### Git's release

- Git's initial commit is `e83c516`, Linus Torvalds, **7 April 2005**, message *"Initial revision
  of 'git', the information manager from hell"*. [1]
- The precipitating event is the day before: Torvalds's "Kernel SCM saga.." post to linux-kernel,
  **6 April 2005**, announcing the BitKeeper break. [2]
- `v1.0.0` was tagged by Junio C Hamano on **21 December 2005**. [1]

### What "before" actually looked like

The load-bearing point is that pre-Git version control was not absent. It was present, and
*defensive* — designed around preventing two people from touching the same file rather than around
reconciling their work afterwards.

- **RCS enforced exclusive locks.** Tichy's RCS paper (*Software—Practice & Experience* 15(7),
  July 1985) has a section titled **"Locking: A Controversial Issue"**. Verbatim: *"At most one
  programmer at a time may lock a particular revision, and only this programmer may check in the
  succeeding revision. Thus, while a revision is locked, it is the exclusive responsibility of the
  locker."* [3]
- The social machinery around breaking a lock is the best single detail in the pass. Verbatim:
  *"Breaking a lock leaves a highly visible trace, namely an electronic mail message that is sent
  automatically to the holder of the lock… Experience has shown that the automatic mail message
  attaches a high enough stigma to lock breaking, such that programmers break locks only in real
  emergencies, or when a co-worker resigns and leaves locked revisions behind."* [3]
- **Microsoft's own Visual SourceSafe glossary** says exclusive checkout was the default, and that
  concurrent editing had to be switched on by an administrator. Verbatim: *"In the default work
  style, Visual SourceSafe allows only one user at a time to check out a file."* And: *"The
  database administrator must enable multiple checkouts to create a Copy-Modify-Merge work style in
  a team environment."* [4]
- **Subversion shipped in 2000 and did not get automatic merge tracking until 1.5, released
  19 June 2008.** The Subversion book, written by the Subversion developers: *"Subversion 1.5
  introduced the merge tracking feature to Subversion. Prior to this feature keeping track of
  merges required cumbersome manual procedures or the use of external tools."* [5] [6]
- The same book on long-lived branches, first-party: *"one of the problems with the 'crawl in a
  hole' strategy is that by the time you're finished with your branch, it may be near-impossible to
  merge your changes back into the trunk without a huge number of conflicts."* [5]
- **Source control was still a discriminating question in 2000.** Item 1 of 12 on the Joel Test,
  9 August 2000, is *"Do you use source control?"* [7] Do not stretch this into "most teams did not
  use source control" — the essay does not support that.

### Adoption

Two survey series, and they are **not comparable to each other**. Eclipse asks for one primary SCM;
Stack Overflow is multi-select. Eclipse's population is Eclipse- and Java-leaning.

Eclipse Community Survey, *"What is your primary source code management system?"*:

| Year | Subversion | CVS | Git (+GitHub) | Mercurial | n | Primacy |
|---|---|---|---|---|---|---|
| 2009 | 57.5% | 20% | not reported | — | 1,365 completed | Primary [8] |
| 2010 | 58.3% | 12.6%* | 6.8% | 3% | 1,696 completed | Primary except CVS* [9] |
| 2011 | 51.3% | 13.3% | 12.8% | 4.6% | 624 completed | Primary [9] |
| 2012 | 46% | — | 27.6% (Git 23 + GitHub 4.5) | 2.6% | 732 completed | Near-primary |
| 2013 | 37.8% | 4.5% | 36.3% (Git 30.3 + GitHub 6.0) | 3.6% | 920 completed | Near-primary |
| 2014 | 30.7% | — | 33.3% Git (+9.6% GitHub) | — | 876 completed | **Secondary — see gaps** |

Eclipse Foundation, 2011 report, verbatim: *"The dominant source code management system continues
to be Subversion, used by 51.3% of respondents (compared with 58.3% in 2010). CVS is second at
13.3%. The distributed code management systems, Git and Mercurial, continue to increase in
popularity."* [9]

Stack Overflow Developer Survey, version control (multi-select):

| Year | Git | Subversion | Zip-file back-ups | Network shares | No version control | n |
|---|---|---|---|---|---|---|
| 2015 | 69.3% | 36.9% | not asked | not asked | not asked | 26,086 (whole survey) [10] |
| 2017 | 69.2% | 9.1% | 2.0% | 1.7% | 4.8% | 30,730 [11] |
| 2018 | 87.2% | 16.1% | 7.9% | 7.9% | 4.8% | 74,298 [12] |
| 2022 | 93.87% | 5.18% | not asked | not asked | 4.31% | 71,379 [13] |

Caution: the 2017→2018 jump in zip-file and network-share figures is almost certainly a
question-wording or population artefact between survey years. **Do not narrate it as a trend.**

**Defensible summary:** the tool shipped in 2005; Git first took the plurality of "primary SCM" in
the Eclipse series in 2014 (nine years); it first measured above half of developers in Stack
Overflow 2015 (ten years, and a floor rather than a crossing point, since the question was not
asked earlier); it reached 87–88% in 2018 (thirteen years) and 93.87% in 2022 (seventeen years).

### The tool arrived years before the discipline

This is the part of the pass that most changes what the chapter can say.

- **The pull request shipped on 23 February 2008 as a notification, not as review.** Chris
  Wanstrath's entire announcement post: *"Last night I pushed out a feature Tom and I have been
  talking about since day one: pull requests… You can use it to tell people who forked from you
  they need to pull, or they can use it to ask you to pull."* No review, no diff discussion, no
  approval. [14]
- **GitHub itself did not describe pull requests as code review until 31 August 2010**, in "Pull
  Requests 2.0": *"As of today, pull requests are living discussions about the code you want merged.
  They're our take on code review."* The same post reports *"200 thousand pull requests in just over
  two years"* across the entire platform. [15]
- **Seven years after GitHub launched, pull requests were still a minority practice.** Gousios,
  Pinzger and van Deursen (ICSE 2014) studied 1.9 million pull requests over February 2012 – August
  2013 and found *"14% of repositories are using pull requests on Github"*, and that *"only 12% of
  the pull requests in our sample"* received a code review comment. [16]
- **As late as 2013, a top-tier conference paper still had to define modern code review as a new
  thing.** Bacchelli and Bird, ICSE 2013: *"Nowadays many organizations are adopting more
  lightweight code review practices… we define Modern Code Review, as review that is (1) informal
  (in contrast to Fagan-style), (2) tool-based, and that (3) occurs regularly in practice
  nowadays."* [17]

GitHub launched publicly in **April 2008** — GitHub's own retrospective says *"In April, we got out
of beta"*. [18] See gaps for why the chapter should not say "10 April".

---

## Findings — team process

### Timeline

| Event | Date | Source | Primacy |
|---|---|---|---|
| Takeuchi & Nonaka, "The New New Product Development Game", *HBR* | **Jan–Feb 1986** | [19] | Primary |
| Sutherland's first Scrum team, Easel Corporation | **1993** (self-reported in 2007) | [20] | Participant self-report |
| Schwaber, "SCRUM Development Process", OOPSLA '95 workshop | **16 October 1995**, Austin; proceedings 1997 | [21] | Primary |
| Agile Manifesto, Snowbird, Utah | **11–13 February 2001**, seventeen people | [22] | Primary |
| First Scrum Guide | **2010** (month unverified) | [23] | Primary (authors' own statement) |

### The vocabulary accreted; it was not delivered

Three checkable facts, in ascending order of usefulness:

1. **The word "scrum" appears exactly once in the 1986 HBR article** — as the section heading
   "MOVING THE SCRUM DOWNFIELD". Takeuchi and Nonaka consistently call it the *"rugby"* approach;
   "rugby" appears ten times. Verbatim: *"Instead, a holistic or 'rugby' approach—where a team tries
   to go the distance as a unit, passing the ball back and forth—may better serve today's
   competitive requirements."* [19]
2. **Schwaber names the method in 1995**, citing them: *"We call the approach the SCRUM methodology
   (see Takeuchi and Nonaka, 1986), after the SCRUM in rugby -- a tight formation of forwards who
   bind together in specific positions when a scrumdown is called."* [21]
3. **The 1995 paper contains "Sprint" (19 occurrences) and "backlog", and zero occurrences of
   "daily", "retrospective", "Daily Scrum", or "stand-up".** There is a sprint review meeting;
   there is no daily meeting and no retrospective. [21] The vocabulary a developer now takes for
   granted took another fifteen years to assemble, and was only frozen in writing by the 2010
   Scrum Guide.

### The field could not agree on a name for itself

- Jim Highsmith's eyewitness history, written in 2001: *"A number [of] these articles referred to
  'Light methodologies, such as Extreme Programming, Adaptive Software Development, Crystal, and
  SCRUM'. In conversations, no one really liked the moniker 'Light', but it seemed to stick for the
  time being."* [22]
- Alistair Cockburn, quoted in the same: *"I don't mind the methodology being called light in
  weight, but I'm not sure I want to be referred to as a lightweight attending a lightweight
  methodologists meeting. It somehow sounds like a bunch of skinny, feebleminded lightweight people
  trying to remember what day it is."* [22]
- The Snowbird group came from **eight named approaches**, not seventeen: *"Representatives from
  Extreme Programming, SCRUM, DSDM, Adaptive Software Development, Crystal, Feature-Driven
  Development, Pragmatic Programming, and others…"* Seventeen is the number of **people**. [22]
  This is a common error; check it before repeating it.
- Martin Fowler, "The New Methodology" (first published July 2000, revised to December 2005): *"At
  that time there was no common name for these approaches, but the moniker 'lightweight' had grown
  up around them."* [24]
- Fowler, "Semantic Diffusion" (14 December 2006), directly on the vocabulary point: *"software
  development still lacks much useful jargon. One of the problems with building a jargon is that
  terms are vulnerable to losing their meaning, in a process of semantic diffusion."* [25]

### Adoption

The State of Agile series (VersionOne → CollabNet → Digital.ai) is a **vendor survey of agile
practitioners**, and says so itself. The 2008 edition: *"This survey was not intended to gauge the
overall adoption of Agile development practices within the software development industry. Its goal
was to report on the status of organizations currently implementing or practicing Agile methods."*
[26] Cite it for "what agile teams do", never for "what the industry does".

| Edition | Fieldwork | n | Scrum | Notes |
|---|---|---|---|---|
| 1st | 2006 | 722 | 40% | XP 23%; average company had practised agile 1.9 years [27] |
| 3rd | Jun–Jul 2008 | 3,061 | 49.1% | + Scrum/XP hybrid 22.3%; XP 8.0% [26] |
| 7th | 2012 | — | 72% "Scrum or Scrum variants" | [28] |
| 9th | Jul–Oct 2014 | 3,925 | 56% | *"pure XP… was virtually non-existent in 2014 (<1%)"* [29] |
| 15th | Feb–Apr 2021 | 1,382 | 66% | + 15% Scrum derivations [30] |
| 17th | 2023 | 788 | 63% of team-level agile users | 71% use agile in their SDLC [31] |

The independent counterweight, and the more useful number for the chapter, because it samples IT
professionals rather than agile practitioners:

- **Forrester + Dr. Dobb's, Q3 2010, n = 1,023 IT professionals**, asked which methodology most
  closely reflected their current process: **Scrum 12.3%** (10.9% in 2009); all agile methods
  combined 38.6%; **"do not use a formal process methodology" 28.8%**; waterfall 9.4%; RUP 1.9%;
  XP 2.9%. Published as "Water-Scrum-Fall Is The Reality Of Agile For Most Organizations Today",
  26 July 2011. [32]
- **Stack Overflow 2018, n = 58,981** (multi-select): Agile 85.4%, Scrum 62.7%, Kanban 35.2%,
  XP 15.7%, "formal standard (waterfall)" 15.1%. [12]

**Defensible summary:** 1993 first team → 1995 first paper → 2001 shared label → 2010 first written
canonical definition → 2018 Scrum at 62.7% of all developers surveyed. Roughly fifteen years from
first articulation to a written definition; roughly twenty-five to default vocabulary. And in 2010,
fifteen years after the paper, Scrum was the process of 12.3% of surveyed IT professionals.

### What actually spread was the vocabulary, not the method

- Diebold, Ostberg, Wagner and Zendler, "What Do Practitioners Vary in Using Scrum?" (XP 2015,
  Springer): *"All companies vary Scrum in some way. The least variations are in the Sprint length,
  events, team size and requirements engineering. Many users varied the roles, effort estimations
  and quality assurance… Many variations constitute a substantial deviation from Scrum as initially
  proposed."* [33] Ten German companies, interview study — present as illustrative, not
  representative. Note the shape: what held constant were the vocabulary items; what varied was
  everything with substance in it.
- Forrester's "water-Scrum-fall" is the same finding from an analyst house: the label spread ahead
  of the practice. [32]
- Martin Fowler, "Flaccid Scrum", 29 January 2009: *"They want to use an agile process, and pick
  Scrum / They adopt the Scrum practices, and maybe even the principles / After a while progress is
  slow because the code base is a mess."* And: *"XPers often joke, with some justification, that
  Scrum is just XP without the technical practices that make it work."* [34]
- Dave Thomas, a manifesto signatory, "Agile is Dead (Long Live Agility)", 4 March 2014: *"The word
  'agile' has been subverted to the point where it is effectively meaningless."* [35] Carry this
  alongside the framing rather than against it — it is the strongest available objection.

---

## What is durable vs. what is an artefact of one survey

| Finding | Durability |
|---|---|
| The primary-document timeline (release dates, paper dates, quoted text) | Durable. These do not change. |
| "About a decade from tool to default, in both cases" | Durable as a shape. Do not print it as a single precise figure — it depends on which survey defines "default". |
| The pull-request two-step (Feb 2008 notification → Aug 2010 review) | Durable, and the single best illustration in the pass. |
| Gousios's 14% / 12% | Durable as published, but it is one corpus over one 18-month window. Say so. |
| Any single survey percentage | Fragile. Eclipse and Stack Overflow measure different populations with different question types and are not comparable. Always name the survey and the year in the sentence. |

---

## Contradictions and gaps

- **The two survey series disagree by construction.** Eclipse 2011 has Git at 12.8%; Stack Overflow
  2015 has it at 69.3%. Both are correct for their question and population. Never place them in one
  sequence as if they were a time series.
- **Eclipse 2014 figures are secondary.** Ian Skerrett's original post returns HTTP 410; the Eclipse
  blog copy is gone; archive.org was unreachable from the research environment. The numbers are
  consistent across two syndicated reposts. If used, attribute explicitly or fall back to 2013.
- **Eclipse 2012 CVS figure is contested** — InfoQ says 8%, the Eclipse 2013 deck says 6.1%. Not
  resolved. Do not state it.
- **Eclipse 2010 CVS = 12.6%** exists only on an Eclipse Foundation blog post; the official 2010
  PDF has no SCM section at all. The SVN/Git/Mercurial figures for 2010 *are* corroborated, because
  the official 2011 PDF restates them.
- **2005–2009 Git adoption is unmeasured.** No survey found. Treat it as unknown rather than
  interpolating.
- **Scrum Alliance's founding year is genuinely disputed.** Scrum Alliance's own site says 2001;
  every secondary source says 2002 and names founders. No incorporation record found. Omit, or
  state as disputed.
- **The first Scrum Guide's month is unverified.** The commonly repeated "February 2010" could not
  be confirmed; the Wayback capture shows the guides page live in January 2010 but the PDF itself
  404s in the CDX index. Say "2010".
- **XP (March 1996), RUP (1998 vs 1999) and FDD (1997) founding dates are secondary only.** The
  RUP year is actively contested between catalogues. Do not state RUP's year.
- **1990s shared network drives, floppies and emailed patches as normal practice: no citable
  source.** Everything surfaced is forum anecdote. The legitimate substitutes are the Stack Overflow
  figures above, where zip-file back-ups and network shares survive as named answer options into
  2018, and the Joel Test's item 1 in 2000.
- **Alan De Smet's "Visual SourceSafe: Microsoft's Source Destruction System"** exists but the
  host's TLS certificate has expired and the text could not be verified. Use Microsoft's own KB
  Q133054, which documents corruption causes and recommends running the repair tool *"every one to
  three months"*, plus Fowler's 2010 ThoughtWorks survey, in which VSS drew 64 "Dangerous" ratings
  of 77 responses — with Fowler's own caveat that it is *"a survey of opinion of ThoughtWorkers who
  follow our internal software development discussion list, nothing more"*. [36] [37]
- **SCCS's locking model** was not verified at source. RCS and Visual SourceSafe carry the point;
  SCCS is not needed.

## Do not cite

- **The Standish Group CHAOS figures** — the 1994 16% / 53% / 31% success split and the 189%
  average cost overrun. Two peer-reviewed demolitions. Eveleens and Verhoef, *IEEE Software* 2010:
  *"the Standish definitions of successful and challenged projects have four major problems: they're
  misleading, one-sided, pervert the estimation practice, and result in meaningless figures."* [38]
  Jørgensen and Moløkken, *IST* 48(4), 2006: *"there are reasons to doubt the validity of the
  Standish Group's 1994 cost overrun results and that a continued use of these results may hinder
  progress."* [39] If the book touches CHAOS at all, it should be as an example of a number the
  industry repeated for twenty years without checking.
- **"87% of teams use Scrum", attributed to the 17th State of Agile (2023).** The string "87%" does
  not appear anywhere in that report. Its actual figures are 63% and 71%. [31]
- **"GitHub launched 10 April 2008."** The month is confirmed by GitHub; the specific day traces to
  Wikipedia. Say "April 2008".
- **Any year in which "pull request" *became* standard vocabulary.** No survey measures term
  adoption. The defensible construction is the timeline: Feb 2008 notification → Aug 2010 review →
  2012–13, 14% of active repos. Do not assert a year.
- **Stack Overflow 2015 "I don't use source control" figures.** The 2015 section has seven bars, no
  "don't use" option, and no per-question response count. Any such figure is fabricated.
- **JetBrains State of Developer Ecosystem version-control percentages.** Charts render
  client-side; no numbers retrievable. Only the qualitative line *"Git is the de facto standard"* is
  confirmed.
- **"Over 1,000 brand-named methodologies" (Jayaratna, 1994).** A superb line for the
  methodology-wars section, and unverified — the usual conduit (Avison & Fitzgerald, *CACM* 46(1),
  2003) returned HTTP 403 to every attempt. Needs someone with ACM DL access.
- **2nd State of Agile (2007) Scrum percentage.** Exists only as a chart image with no text layer.
  The series runs 2006 (40%) → gap → 2008 (49.1%).

## Sources

[1] `git/git` repository, initial commit `e83c516` and tag `v1.0.0` — https://github.com/git/git/commit/e83c5163316f89bfbde7d9ab23ca2e25604af290 — accessed September 2026
[2] Linus Torvalds, "Kernel SCM saga..", linux-kernel, 6 April 2005 — https://marc.info/?l=linux-kernel&m=111280216717070&w=4 — accessed September 2026
[3] Walter F. Tichy, "RCS—A System for Version Control", *Software—Practice & Experience* 15(7), July 1985 — https://www.gnu.org/software/rcs/tichy-paper.pdf — accessed September 2026
[4] "Visual SourceSafe Glossary", Microsoft (ms.date 2007-05-01) — https://learn.microsoft.com/en-us/previous-versions/0b11a65t(v=vs.80) — accessed September 2026
[5] Collins-Sussman, Fitzpatrick and Pilato, *Version Control with Subversion*, 1.7 — https://svnbook.red-bean.com/en/1.7/svn.branchmerge.basicmerging.html — accessed September 2026
[6] Apache Subversion 1.5 release notes, merge tracking — https://subversion.apache.org/docs/release-notes/1.5.html#merge-tracking — accessed September 2026
[7] Joel Spolsky, "The Joel Test: 12 Steps to Better Code", 9 August 2000 — https://www.joelonsoftware.com/2000/08/09/the-joel-test-12-steps-to-better-code/ — accessed September 2026
[8] Eclipse Foundation, "Eclipse Community Survey 2009" — https://www.eclipse.org/org/press-release/Eclipse_Survey_2009_final.pdf — accessed September 2026
[9] Eclipse Foundation, "Eclipse Community Survey 2011 Report" — https://www.eclipse.org/org/community-survey/Eclipse_Survey_2011_Report.pdf — accessed September 2026
[10] Stack Overflow Developer Survey 2015, "Source Control" — https://survey.stackoverflow.co/2015/ — accessed September 2026
[11] Stack Overflow Developer Survey 2017, "Version Control" — https://survey.stackoverflow.co/2017/ — accessed September 2026
[12] Stack Overflow Developer Survey 2018 — https://survey.stackoverflow.co/2018/ — accessed September 2026
[13] Stack Overflow Developer Survey 2022, "Version control" — https://survey.stackoverflow.co/2022/#technology-version-control — accessed September 2026
[14] Chris Wanstrath, "Oh yeah, there's pull requests now", GitHub Blog, 23 February 2008 — https://github.blog/2008-02-23-oh-yeah-there-s-pull-requests-now/ — accessed September 2026
[15] Ryan Tomayko, "Pull Requests 2.0", GitHub Blog, 31 August 2010 — https://github.blog/2010-08-31-pull-requests-2-0/ — accessed September 2026
[16] Gousios, Pinzger and van Deursen, "An Exploratory Study of the Pull-based Software Development Model", ICSE 2014 — https://pure.tudelft.nl/ws/files/7416754/TUD_SERG_2014_005.pdf — accessed September 2026
[17] Bacchelli and Bird, "Expectations, Outcomes, and Challenges of Modern Code Review", ICSE 2013 — https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/ICSE202013-codereview.pdf — accessed September 2026
[18] GitHub, "Only the beginning", 2 January 2009 — https://github.blog/news-insights/only-the-beginning/ — accessed September 2026
[19] Takeuchi and Nonaka, "The New New Product Development Game", *Harvard Business Review*, January–February 1986 — https://hbr.org/1986/01/the-new-new-product-development-game — accessed September 2026
[20] Jeff Sutherland, "Origins of Scrum", 5 July 2007 — http://jeffsutherland.com/scrum/2007/07/origins-of-scrum.html — accessed September 2026
[21] Ken Schwaber, "SCRUM Development Process", OOPSLA '95 workshop, 16 October 1995 — http://www.jeffsutherland.org/oopsla/schwapub.pdf — accessed September 2026
[22] Jim Highsmith, "History: The Agile Manifesto", 2001 — https://agilemanifesto.org/history.html — accessed September 2026
[23] *The Scrum Guide*, November 2020 edition, "Purpose of the Scrum Guide" — https://scrumguides.org/docs/scrumguide/v2020/2020-Scrum-Guide-US.pdf — accessed September 2026
[24] Martin Fowler, "The New Methodology", July 2000, revised 13 December 2005 — https://martinfowler.com/articles/newMethodology.html — accessed September 2026
[25] Martin Fowler, "Semantic Diffusion", 14 December 2006 — https://martinfowler.com/bliki/SemanticDiffusion.html — accessed September 2026
[26] VersionOne, "3rd Annual State of Agile Development Survey", 2008 — https://www.eg.bucknell.edu/~cs479/common-files/resources/versionone-state-of-agile/3rd-annual-state-of-agile-report.pdf — accessed September 2026
[27] VersionOne, "The State of Agile Development", 1st annual, 2006 — https://www.stickyminds.com/sites/default/files/article/file/2013/XDD11660filelistfilename1_0.pdf — accessed September 2026
[28] VersionOne, "7th Annual State of Agile Development Survey" — https://www.se.rit.edu/~swen-356/resources/7th-Annual-State-of-Agile-Development-Survey.pdf — accessed September 2026
[29] VersionOne, "9th Annual State of Agile Survey" — https://www.watermarklearning.com/downloads/state-of-agile-development-survey.pdf — accessed September 2026
[30] Digital.ai, "15th State of Agile Report" press release — https://digital.ai/press-releases/15th-state-of-agile-report-shows-notable-rise-in-agile-adoption-across-the/ — accessed September 2026
[31] Digital.ai, "17th Annual State of Agile Report", 2023 — https://info.digital.ai/rs/981-LQX-968/images/RE-SA-17th-Annual-State-Of-Agile-Report.pdf — accessed September 2026
[32] Dave West et al., "Water-Scrum-Fall Is The Reality Of Agile For Most Organizations Today", Forrester Research, 26 July 2011 — https://www.verheulconsultants.nl/water-scrum-fall_Forrester.pdf — accessed September 2026
[33] Diebold, Ostberg, Wagner and Zendler, "What Do Practitioners Vary in Using Scrum?", XP 2015 — https://arxiv.org/abs/1703.10361 — accessed September 2026
[34] Martin Fowler, "FlaccidScrum", 29 January 2009 — https://martinfowler.com/bliki/FlaccidScrum.html — accessed September 2026
[35] Dave Thomas, "Agile is Dead (Long Live Agility)", 4 March 2014 — https://pragdave.me/thoughts/active/2014-03-04-time-to-kill-agile.html — accessed September 2026
[36] Microsoft KB Q133054, "HOWTO: Detect and Fix Database Corruption Errors in SSafe", last modified 24 March 2002 — https://jeffpar.github.io/kbarchive/kb/133/Q133054/ — accessed September 2026
[37] Martin Fowler, "VcsSurvey", ThoughtWorks developer survey, 23 February – 3 March 2010, 99 responses — https://www.martinfowler.com/bliki/VcsSurvey.html — accessed September 2026
[38] Eveleens and Verhoef, "The Rise and Fall of the Chaos Report Figures", *IEEE Software*, 2010 — https://www.cs.vu.nl/~x/the_rise_and_fall_of_the_chaos_report_figures.pdf — accessed September 2026
[39] Jørgensen and Moløkken, "How Large Are Software Cost Overruns? A Review of the 1994 CHAOS Report", *Information and Software Technology* 48(4), 2006 — https://cms.simula.no/sites/default/files/publications/Jorgensen.2006.4.pdf — accessed September 2026

## Staleness assessment

Unusually low, by the standards of this project. Almost everything here is a primary document with
a fixed date, and the historical record does not rot. Two qualifications:

- **The link rot is real and already visible.** Two Eclipse-hosted reports and one Eclipse blog post
  have disappeared during the life of this research; the State of Agile PDFs survive mainly because
  universities mirror them. Anything cited here should be archived locally before publication.
- **The analogy itself has a shelf life, though a different kind.** If the agentic engineering layer
  does converge, a later edition will need to say what it converged on, and the chapter's "we are in
  the middle of this" framing will read as dated in the way that a weather forecast reads as dated.
  That is a good problem and the chapter should be written so that it is a cheap edit.

## Concrete example we can lift

The single strongest sequence in the pass, ready to drop into prose:

> GitHub shipped the pull request on 23 February 2008. The announcement describes it as a way to
> "tell people who forked from you they need to pull". It is a notification. GitHub itself did not
> describe pull requests as code review until "Pull Requests 2.0" on 31 August 2010 — two and a half
> years later — and even then, researchers studying 1.9 million pull requests over 2012 and 2013
> found that 14% of active repositories used pull requests at all, and that 12% of pull requests
> carried a review comment.

Nothing else in the pass makes the tool-before-discipline point as economically, and every figure
in it is primary or peer-reviewed.
