# Hold the structure, not just the behaviour

## Problem

The run added hold-back rules to the rollout planner. The tests passed, the diff was a single new
function, and the review took ten minutes. Four changes later, the same function decides seven
things, takes nine arguments, and nests five deep. Every one of those changes passed every check you
have, because every check you have asks whether the code works. None asks whether it can still be
changed. You find out when a two-line fix takes an afternoon, from you and from the agent, which
now spends most of its run reading the function before it touches it.

## The play

Measure what each change does to the structure, and give the result to the agent before the turn
ends, not to a reviewer afterwards.

1. **Score the change, not the codebase.** Run a structural delta over the files the run touched,
   against `HEAD`: complexity, nesting depth, argument count, duplication, each reported with a
   path and a line. A project-wide score averages new damage into old health and moves too slowly
   to see one change.
2. **Put it in the loop.** Report after each edit, and gate the end of the turn: if health fell,
   the run gets the findings and one more turn. CodeScene ships this as an MCP server; `aihealth`,
   an open-source tool written by this book's author, ships it as a CLI with Claude Code hooks.
   Both narrow the run's options rather than removing them. The `aihealth` stop hook never fires
   twice in a row, so a run can still finish degraded.
3. **Ratchet, do not target.** Fail on any fall in a file the change touched, and hold new files to
   the healthy band. An absolute threshold on a legacy file at 4 blocks every change to it, and the
   team switches the check off within a week.
4. **Keep the behaviour checks in front.** Run the structural check only after the suite and the
   type checker pass. A refactor that improves the score and changes behaviour is the worse result.
5. **Read the findings, not the number.** The score summarises; the smells with line numbers are
   what the agent fixes and what you review.

```mermaid
graph LR
    E["Edit"] --> T{"Tests and<br/>types pass?"}
    T -->|"no"| E
    T -->|"yes"| D{"Structure fell in<br/>a touched file?"}
    D -->|"yes: findings"| E
    D -->|"no"| R["Turn ends;<br/>review starts"]
```

This works because structural decay arrives one passing step at a time, so only a check that
compares each step to the last can see it. The evidence is about what agents produce. In a 2026
study of 806 open-source projects that adopted Cursor, code complexity rose by 41.6% and stayed up,
while the speed-up was gone after two months. The claim that agents themselves work better on
healthy code is weaker than it is usually told: the one controlled study found no significant
difference for a frontier model ([`code-health.md`](../../../notes/research/code-health.md)). Hold
the structure for whoever changes the code next, person or agent. The exchange rate is an extra turn
on most changes, refactors you would have waved through, and a metric somebody must calibrate and
sometimes overrule.

## Worked example

`tideline`, a TypeScript service that stages firmware rollouts to field devices, needed hold-back
rules: a device is kept out of a stage for low battery, an unlisted model, a stale check-in, a
firmware gap, or a regional freeze. The team had the `aihealth` hooks in `.claude/settings.json`.
The stop half, as the tool's install guide gives it:

```json
{
  "hooks": {
    "Stop": [
      { "hooks": [{ "type": "command",
          "command": "command -v aihealth >/dev/null 2>&1 && aihealth hook stop || true" }] }
    ]
  }
}
```

The run's first pass was one function, `enrolDevice`, and the suite passed. Before the turn ended,
the hook ran the delta, and what came back became the run's next turn:

> Captured November 2026, aihealth 0.1.0 (commit `abfdd17`).

```text
$ aihealth delta; echo "exit $?"
aihealth delta: working tree vs HEAD: DEGRADED

  degraded  src/rollout/holdback.ts  new file, 7.89
    + new     L12    High Cognitive Complexity: enrolDevice has cognitive complexity 40
                     → Hard to follow: flatten with early returns/guard clauses and extract nested blocks.
    + new     L12    Complex Method: enrolDevice has cyclomatic complexity 25
    + new     L26    Bumpy Road: enrolDevice has 3 separate nested chunks (L26-32, L34-47, L62-72)
    + new     L12    Excess Arguments: enrolDevice takes 8 parameters (weighted 8)
    + new     L42    Deep Nesting: enrolDevice nests 4 levels deep at line 42
    + new     L59    Complex Conditional: enrolDevice has 1 complex boolean expression(s) (up to 2 operators: L59)
    # … one fix hint per finding, five omitted
exit 1
```

The project score at the same moment read healthy:

```text
$ aihealth scan .
…
project score: 9.64 (healthy)  (8 files, 405 LoC, LoC-weighted)
files: 7 healthy, 1 warning, 0 alert
…
```

The run replaced the eight arguments with one context object and the branches with five small rule
functions, checked in order. The suite still passed, and the delta came back clean:

```text
$ aihealth delta; echo "exit $?"
aihealth delta: working tree vs HEAD: UNCHANGED

  unchanged src/rollout/holdback.ts  new file, 10.00
exit 0
```

The check has a blind spot, and `tideline` already contained it. The cohort module merged the month
before holds two bucketing helpers that round a boundary device in opposite directions. Scored on
its own, `src/cohort/` comes back at 10.00. The check measures shape, not meaning, and two tidy
functions that disagree are perfectly shaped.

## Failure mode

**The Healthy Average.** The dashboard is green, the trend line is flat, and the newest code is the
worst in the repository. A project score weights each file by its size, so one new function at 7.89
barely moves a mean held up by years of settled code. In `tideline` it moved the project to 9.64,
still labelled healthy. The team watching the number sees stability while the files the agent
writes every day sit a band lower than the files nobody touches.

The tell is a project score that has not moved in a month of heavy agent work, beside a list of
the worst files that keeps gaining recent ones. The check that settles it is to score only the files
changed in the last month, and compare.

## Checklist

- [ ] A structural delta runs on every change, scoped to the files it touched
- [ ] The delta's findings reach the agent before its turn ends, not only the reviewer
- [ ] The gate fails on a fall in a touched file, not on an absolute project threshold
- [ ] New files are held to the healthy band
- [ ] The structural check runs after the suite and the type checker, never instead of them
- [ ] Recently changed files are scored separately from the project average

**See also:** [*Make the agent prove it*](make-the-agent-prove-it.md) ·
[*Review code you did not write*](review-code-you-did-not-write.md) ·
[*Collect and refine as a team*](../team/collect-and-refine-as-a-team.md)
