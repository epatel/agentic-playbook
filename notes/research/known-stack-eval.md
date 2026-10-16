# Known stack — naming what the model already knows, measured once

**Question asked:** does it pay to name, in one line each, the frameworks and patterns a model
already knows, and to card only what neither the code nor the model's prior can supply?

**Researched:** 16 October 2026
**Confidence:** medium on efficiency (turns and cost moved the same way in every task); low on
quality (n=3 per cell, and the eval's own caveat puts differences under about 1 point inside noise).
This is one A/B test, run by the book's author on their own repository, unpublished and not
independently replicated. It is the only measurement of this question the book has.

Feeds the **Context** suite: *Write the agent file that actually gets read* (step 3) and *Split the
agent file into cards*.

## Findings

### The pattern

- A **Known stack** section in the agent file names each standard concept in one line, with the
  file where it lives and any local twist ("all routes in `lib/app/router.dart`", "Coordinator is
  scaffolding; no page dispatches events yet"). Cards are written only for what the model cannot
  know: a private library or DSL, custom build tooling, state outside the repository, invariants
  the code does not make obvious, known current defects. [1][2]
- The test repository's own Known stack pins one version, `pocketbase` 0.18, because it decides
  the SDK calls the agent writes against. It pins nothing else. [5]

### The test

- Repository: `blory_stok`, a Flutter + PocketBase translation-string editor, about 700 lines of
  Dart. [1]
- Four copies, differing only in agent docs: **none** (0 KB); **cardsonly**, a lean agent file
  without the Known stack section plus 3 specialised cards (8.4 KB); **lean**, the same plus the
  Known stack section (10.0 KB); **standard**, a full 12-card set written by a separate agent to the
  ai.memention.net setup procedure, including the same 3 cards (34.9 KB). [1]
- `cardsonly` vs `lean` isolates the Known stack section (about 1.6 KB of text). `lean` vs `standard`
  tests naming against describing. [1]
- Each cell a fresh headless session: `claude -p --model sonnet` (Sonnet 5.5), project settings
  only, read-only tools, no edits. 3 tasks (two code tasks, one ops question) × 4 conditions × 3
  repetitions = 36 runs, $4.44 in total. Scored by a regex rubric and by one blind judge per task,
  with condition-revealing words masked. Run 16 October 2026. [1]

### Efficiency (mean of 9 runs per condition) [1]

| Condition | Turns | Output tokens | Seconds | Cost (9 runs) |
|---|---|---|---|---|
| none | 9.6 | 5,011 | 43 | $0.93 |
| cardsonly | 8.2 | 6,001 | 50 | $1.11 |
| lean | 4.9 | 4,019 | 36 | $0.81 |
| standard | 7.6 | 7,992 | 64 | $1.58 |

- The Known stack lines alone took turns from 8.2 to 4.9 and cost from $1.11 to $0.81, a 27%
  saving as the source states it. Turn and cost differences held in every task. [1]
- The full card set read 190–246k input tokens on the code tasks against about 100k for `lean`,
  wrote about twice the output, and took about 1.8× as long. [1]

### Correctness and quality [1]

- Every condition followed the project's conventions (dialog shape, barrel exports, router
  location, all-languages rename). The one rubric miss: all 3 `none` rename runs built PocketBase
  filters by string interpolation; every carded run used the parameterised form, which came from a
  specialised card. In the source's words, the docs "did not change *whether* it followed the
  conventions, only how fast it got there."
- Blind-judge means (1–10): none 6.22, cardsonly 7.56, lean 7.44, standard 6.78. The judge cited
  scope creep and diff defects against `standard`, not convention errors.
- The clearest quality gains over `none` came from specialised cards: the ops question scored 5.3
  with no docs and 8.7 with `lean`, because the no-docs answers missed that a build-toggle script
  breaks `pubspec.yaml`.

### Side findings [1]

- A maintenance rule ("update or add the card in the same change") made agents add doc edits to
  9/9 carded rename diffs and 6/9 carded stats diffs. The judge marked them as scope creep. The rule
  was afterwards scoped to commits. [1][4]
- Some weaknesses appeared in every condition and no card prevented them: closing a dialog before
  the async write finished, unhandled errors, re-fetching inside `build()`. General craft, not
  project knowledge.
- The eval exposed a card that understated a real defect. The author first called one agent's
  claim about it a hallucination; the agent was right.

## Contradictions and gaps

- **The quality claim does not survive the caveat.** The blog post [2] and the setup card [3] say
  `lean` scored higher than `standard` (7.44 vs 6.78). The eval itself says differences under about
  1 point are within run-to-run variance. Treat the quality ordering as unestablished; the cost and
  turn differences are the finding.
- Small n (3 per cell), one model, one small repository (where reading everything is cheap, so
  `none` is unusually strong), one judge per task from the same model family as the agents. The
  source expects a weaker model to need the cards more and a larger repository to show larger
  savings from naming. Neither has been tested. [1]
- No independent study of this question was found (see [`agent-context-files.md`](agent-context-files.md),
  which records low confidence on relative effectiveness generally).

## Sources

[1] `KNOWN_STACK_EVAL.md` in the `blory_stok` repository (private; github.com/epatel/blory_stok,
    commit `e317d77`) — read 16 October 2026
[2] Edward Patel, "Known stack", memention.com blog, 16 October 2026 — read 16 October 2026
[3] "Known Stack" pattern card — https://ai.memention.net/cards/known-stack.md — read 16 October 2026
[4] `blory_stok` commit `0e8f9b1`, "Scope card maintenance rule to commits" — read 16 October 2026
[5] `CLAUDE.md` in the `blory_stok` repository, section "Known stack" — read 16 October 2026
