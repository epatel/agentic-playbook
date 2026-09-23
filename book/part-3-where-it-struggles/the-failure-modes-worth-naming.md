# The failure modes worth naming

A failure you can name is a failure you can raise in a review without spending a paragraph on
preamble first. That is the entire argument for this chapter, and it is not a small one: the
phenomena below are all common, all recognised on sight by people who use these tools daily, and all
routinely left unmentioned because saying them out loud costs more sentences than anyone has
patience for at half past four.

Six of them get their names here, because no play in this book owned the material. Each entry gives
the name, what it is, the tell — the thing you can check today — and the response. Every other name
the book uses is indexed at the end, so this chapter is the one place to look them all up.

## The Confident Wrong Rewrite

A syntactically valid patch that is functionally incorrect, incomplete, or does not address the
problem it was written for. It is not an edge case; it is the dominant failure. In the November 2025
SWE-Bench Pro paper, Claude Opus 4.1's failing runs on the public set split 511 that submitted a
patch against 178 that never got that far. Of the 511, 257 — 50.3% — were classified that way,
against 160 syntax errors. Once the agent got as far as a diff, half of what went wrong went wrong
while compiling cleanly and reading well.

The tell is structural rather than textual, which is why reading the diff line by line does not find
it. The change addresses a restatement of the problem rather than the problem: it handles the
symptom in the ticket and not the condition that produced it, or it implements the first of two
things the issue asked for and summarises as though it did both. A useful probe is to ask what the
change does to the case the ticket did not mention.

The response is to check the change against the requirement rather than against itself, and to do it
before reading the code. That is why [*Review code you did not
write*](../part-2-plays/verification-and-trust/review-code-you-did-not-write.md) puts one traced
path and a reproducer ahead of the diff.

One class of it has a cause outside the model. Where behaviour is attached invisibly — a decorator
that registers a route at import time, a lifecycle hook that writes to a second table — none of it
appears in the file being edited, so the patch is locally correct and globally wrong. [*Refactoring
a codebase for agents*](../part-4-next-waves/refactoring-a-codebase-for-agents.md) argues that back
to the architecture; the response here is narrower: name the mechanism in the agent file when the
change sits near one.

## The Vanishing Fix

The run reaches a correct solution partway through, keeps going, and overwrites it. Everyone who
uses these tools has watched this happen and, until recently, nobody had measured it. A 2026 study
decomposing 16,758 agent trajectories found the rate climbing with run length: 21.7% of the shortest
quartile against 63.7% of the longest. The length dependence comes almost entirely from one
sub-type, the thrashing kind; the other kind — a near-correct patch corrupted in place — is
length-independent, so short runs reduce this and do not abolish it.

The tell is in the transcript rather than the diff, and the transcript is on disk. A test that went
green and later went red, a file edited, reverted, and edited again, or a final change that rewrites
a function the run had already got right. If you only read the summary at the end, this is invisible
by construction.

The response is to shorten the run and to commit at green. A run that stops when the check first
passes cannot overwrite the thing that made it pass, and a commit is cheaper than a diagnosis.
[*Scope a task to fit the window*](../part-2-plays/context/scope-a-task-to-fit-the-window.md) is the
play, and [*Before Git, before Scrum, before
this*](../part-1-argument/before-git-before-scrum-before-this.md) uses this phenomenon as its
example of the vocabulary the field has not settled.

## The Requirement It Can Still Quote

The agent reads the requirements, restates them accurately, and stops meeting them. A 2026 white-box
study varying only context size on a fixed code-audit task found strict success falling from eight
runs in ten to three in ten between a roughly 11,000-character context and a roughly
300,000-character one — a retention ratio of 0.375. Over the same range, requirement-coverage
retention held at 0.933 to 0.949. The information is present the whole way down. The compliance is
not.

The intuitive diagnosis is wrong and leads somewhere useless: it is not that the requirements fell
out of the window. They are still there, and the agent will recite them to you.

The tell is the recital itself. Ask what the requirements were; it answers correctly; the code does
not satisfy them. The failures in that study clustered at compilation, execution, and verification
rather than at reading the files.

The response is a requirement list that lives outside the conversation and gets checked
mechanically. In the same study a generic "check your work" self-review recovered five runs in ten,
and an external requirement list recovered ten in ten. That list is step 3 of
[*Scope a task to fit the window*](../part-2-plays/context/scope-a-task-to-fit-the-window.md).

## The Endless Polish

Each pass improves something, and the file is worse than it was five passes ago. Nothing fails, so
nothing stops. Verbosity, complexity concentration, and cost all climb across a trajectory with no
gain in solve rate, while human repositories hold the same metrics flat; the measurement is in
[*What agents are reliably bad at*](what-agents-are-reliably-bad-at.md).

It is a different animal from the Permanent Near Miss ([*Scope a task to fit the
window*](../part-2-plays/context/scope-a-task-to-fit-the-window.md#failure-mode)), which is about a
run that never arrives. This one arrives repeatedly and leaves sediment each time.

The tell is a file that has grown on every iteration, a run of recent passes with no behavioural
change to show for them, and near-duplicate boilerplate sitting in adjacent branches of the same
function rather than factored out.

The response is to diff against the state five passes ago rather than against the last one, and to
cap iterations in advance. The comparison that matters is not "is this better than the previous
attempt" but "is this better than where this started".

## The Immaculate Surface

Every check you have automated is clean, and the defect is in a class you have not automated a check
for. One vendor's 2025 telemetry across tens of thousands of repositories reported syntax errors
down 76% and logic bugs down more than 60%, against privilege-escalation paths up 322% and
architectural design flaws up 153%. It prints no baseline and no window for those four figures and
its definition of "security issue" is broad, so hold the magnitudes lightly. The shape is the point:
the error classes that got cheap to catch went away, and the ones that were always expensive to
catch went up.

The tell is a review in which every comment you raised was about naming or formatting, on a change
whose effects you could not draw. This is not the Drifting Yes ([*Review code you did not
write*](../part-2-plays/verification-and-trust/review-code-you-did-not-write.md#failure-mode)),
where the standard slips with exposure. Here the standard holds and it is pointed at the wrong class
of defect.

The response is to review the blast radius rather than the lines. What can this change now reach
that it could not reach before — which credentials, which tables, which callers? That question is
cheap to ask and has no automated substitute.

## The Instant Concession

You push back on something the agent got right, and it agrees immediately and replaces it with
something worse. The measured version of this is conversational rather than agentic, and the
distinction matters: in a 2026 benchmark where a proxy user applied sustained pressure to items
resting on a false presupposition, collapse rates at 25 turns ran from 65% to 97% depending on the
model, on an average of six to fifteen turns of pressure. Emotional appeals worked better than
logical ones — a 44.3% drop rate against 20.0%. Among the four models that expose reasoning traces,
collapse "typically occurs while the correct position remains represented rather than after it
disappears". It did not lose the answer. It stopped asserting it.

Nobody has published a measurement of an agent abandoning a correct patch after a reviewer pushes
back. This name is given on recognition rather than on evidence, and that is stated here rather than
hidden, because the alternative is a book that quietly upgrades an extrapolation into a citation.

The tell is a rewrite with no argument attached, arriving faster than a considered disagreement
would.

The response is to make disagreeing cheap. Ask it to defend the original before replacing it, and
phrase the pushback as a question rather than a correction — "what happens at zero elements here?"
rather than "this is wrong".

## The index

Every name this book uses, and where it is described — the six above plus the twenty-two the plays
coined. The convention throughout is one name per phenomenon, Title Case, naming the symptom rather
than the cause: a reader should recognise the thing before they understand it.

| Name | What you see | Described in |
|---|---|---|
| **the Confident Wrong Rewrite** | A patch that compiles, reads well, and addresses a restatement of the problem | This chapter |
| **the Vanishing Fix** | A correct solution reached mid-run and overwritten before the run ends | This chapter |
| **the Requirement It Can Still Quote** | The agent recites the requirements accurately and stops meeting them | This chapter |
| **the Endless Polish** | Every pass improves something and the file is worse than five passes ago | This chapter |
| **the Immaculate Surface** | Every automated check clean, the defect in the class you never automated | This chapter |
| **the Instant Concession** | Pushback on a correct answer, agreed to instantly and replaced with a worse one | This chapter |
| **the Context Landfill** | An agent file that only ever grew; the current convention followed about half the time | [*Write the agent file that actually gets read*](../part-2-plays/context/write-the-agent-file-that-actually-gets-read.md) |
| **the Agent File That Never Arrived** | Instructions written, committed, and never loaded; nothing errors | [*Write the agent file that actually gets read*](../part-2-plays/context/write-the-agent-file-that-actually-gets-read.md) |
| **the Reassembled Agent File** | Short cards, a short index, and every run still loading most of the material through links between them | [*Split the agent file into cards*](../part-2-plays/context/split-the-agent-file-into-cards.md) |
| **the Adequate Answer** | Output nobody objects to, from a context nobody examines, because only a bad result prompts a look | [*Starve the context*](../part-2-plays/context/starve-the-context.md) |
| **the Flattering Dashboard** | A tool reports large savings while the bill goes up | [*Starve the context*](../part-2-plays/context/starve-the-context.md) |
| **the Permanent Near Miss** | Every run ends just short, including the ones that continue the last one | [*Scope a task to fit the window*](../part-2-plays/context/scope-a-task-to-fit-the-window.md) |
| **the Paper Fence** | A rule that forbids something and does not stop it | [*Choose your harness*](../part-2-plays/harness/choose-your-harness.md) |
| **the Unsummoned Skill** | A skill written, committed, and never triggered; a non-match is not an event | [*Package repeatable expertise*](../part-2-plays/harness/package-repeatable-expertise.md) |
| **the Instruction You Did Not Write** | Behaviour that traces to nothing in your repository | [*Wire in the outside world*](../part-2-plays/harness/wire-in-the-outside-world.md) |
| **the Tidy Summary** | A delegated worker's report that reads the same whether the work was thorough or partial | [*Decompose into subagents*](../part-2-plays/orchestration/decompose-into-subagents.md) |
| **the Load-Bearing Scaffold** | A workaround for a gap that closed, now impossible to remove | [*Make the control flow deterministic*](../part-2-plays/orchestration/make-the-control-flow-deterministic.md) |
| **the Clean Merge** | Git succeeded, both branches were green, the merged tree was never tested | [*Work in parallel without collisions*](../part-2-plays/orchestration/work-in-parallel-without-collisions.md) |
| **the Drifting Yes** | Approval of agent changes getting easier with exposure; your own comments getting shorter | [*Review code you did not write*](../part-2-plays/verification-and-trust/review-code-you-did-not-write.md) |
| **the Green Suite That Tests Nothing** | The suite passes and the green is a fact about the suite | [*Make the agent prove it*](../part-2-plays/verification-and-trust/make-the-agent-prove-it.md) |
| **the Accountable Bystander** | A named owner who approved more than anyone could have understood | [*Decide who signs off*](../part-2-plays/verification-and-trust/decide-who-signs-off.md) |
| **the Expensive Nothing** | A cost spike on a message you could have sent by nodding | [*Understand what you are paying for*](../part-2-plays/economics/understand-what-you-are-paying-for.md) |
| **the Long Way Round** | Cheaper per token, larger invoice, several times as many turns | [*Match the model to the job*](../part-2-plays/economics/match-the-model-to-the-job.md) |
| **the Errand That Became a Project** | A one-line request returning a defensible diff across nine files | [*Know when not to use an agent*](../part-2-plays/economics/know-when-not-to-use-an-agent.md) |
| **the Founding Document** | A working agreement nobody amends, everyone has drifted from, and people quote | [*Build the working agreement*](../part-2-plays/team/build-the-working-agreement.md) |
| **the Nodded-Through Agreement** | Every item agreed first time, and nothing anyone does on Monday is different | [*Settle what the team cannot agree*](../part-2-plays/team/settle-what-the-team-cannot-agree.md) |
| **the Showreel** | A shared library assembled from everyone's best day | [*Collect and refine as a team*](../part-2-plays/team/collect-and-refine-as-a-team.md) |
| **the Fluent Stranger** | Correctly-shaped work from someone with no sense yet of what is load-bearing | [*Onboard someone into all this*](../part-2-plays/team/onboard-someone-into-all-this.md) |
