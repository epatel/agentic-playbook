# LangChain and LangGraph — what each is for, and what the complaints actually are

**Question asked:** what LangChain and LangGraph each do, where the boundary between them sits, what
LangGraph genuinely buys you over hand-written code, and what people complain about in production.

**Researched:** 19 September 2026
**Confidence:** high on the architecture and feature set (official documentation is primary and
clear); medium on the criticism (the canonical critique's own site was unreachable this pass); low
on all adoption figures, which are vendor-reported without exception.

Feeds the **Orchestration** suite, chiefly *Make the control flow deterministic*, and supplies the
Economics suite with a build-versus-adopt worked comparison.

## Findings

### The boundary, from the vendor's own words

LangGraph's docs define it as "a low-level orchestration framework and runtime for building,
managing, and deploying long-running, stateful agents." [1] The split is stated explicitly:
LangChain is "the agent framework: abstractions and integrations for models, tools, and agent
loops," LangGraph is "the orchestration runtime: durable execution, streaming, human-in-the-loop,
and persistence." [1]

The layering is one-directional and this is the useful bit for the book. LangChain agents are built
*on* LangGraph, so you "start with LangChain's high-level APIs and seamlessly drop down to LangGraph
when you need more control." [2] The same docs page warns newcomers off LangGraph directly: it is
"very low-level, and focused entirely on agent **orchestration**." [1] LangChain's README puts the
signpost the other way round: "If you're looking for more advanced customization or agent
orchestration, check out LangGraph." [3]

**1.0 shipped 22 October 2025**, covering both libraries. [2] It is billed as the first major stable
release with a commitment to no breaking changes until 2.0. [2] Headline changes: `create_agent`
("the fastest way to build an agent with any model provider"), a middleware system with built-ins
for human-in-the-loop approval, summarisation and PII redaction, provider-agnostic "standard content
blocks" for reasoning traces and citations, and legacy code exiled to `langchain-classic`. [2]

Current versions at time of writing, from PyPI: `langchain` **1.4.2**, `langgraph` **1.2.11**.
[4][5] Their release dates could not be verified and should not be stated.

### What LangGraph actually provides

- **Persistence.** Checkpointers "persist a thread's graph state as checkpoints," enabling
  "short-term, thread-scoped memory, including conversation continuity, human-in-the-loop workflows,
  time travel, and fault tolerance." A `thread_id` identifies a conversation, passed as
  `{"configurable": {"thread_id": "thread-1"}}`. [6] Implementations: `InMemorySaver` (RAM, "does
  not persist between restarts"), `SqliteSaver` ("local file-based storage for development"),
  `PostgresSaver` / `AsyncPostgresSaver`. [6]
- **Human-in-the-loop as a primitive.** `interrupt()` "pause[s] graph execution at specific points
  and wait[s] for external input before continuing"; `Command(resume=...)` feeds the value back in.
  It requires a checkpointer ("use a durable checkpointer in production"), a thread ID, and the call
  itself — and crucially, `interrupt()` can sit *inside a tool function*, gating that tool's
  execution. [7]
- **Durability as a dial, not a switch.** Three modes: `"exit"` (checkpoint only at the end,
  fastest), `"async"` (persist while the next step runs, small risk of losing a checkpoint on
  crash), `"sync"` (persist before the next step starts, with performance overhead). [8]

### Open source versus paid — and a renaming worth noting

The `langgraph` library is MIT-licensed. [9] The commercial layer was **renamed in October 2025**,
within days of the 1.0 launch: LangGraph Platform became **LangSmith Deployment**, LangGraph Studio
became **LangSmith Studio**. [10] Deployment offers four models: Cloud (managed, **requires Plus
plan or above**), self-hosted with control plane (**Enterprise**), hybrid, and a standalone Agent
Server via Docker or Kubernetes with your own PostgreSQL and Redis. [11]

Pricing, from the vendor page: Developer $0/seat/month up to 5k base traces/mo, single seat; Plus
**$39/seat/month** up to 10k base traces/mo, unlimited seats, "1 free Serverless (Small)
deployment"; Enterprise custom. Metered usage is **$1.50 / LCU** (LangChain Compute Unit) and
**$1.00 / LSU** (Storage Unit). Base traces retain 14 days, extended 400 days. [12]

### The honest case for

- **Resumability is the actual product.** A checkpointer plus a `thread_id` means a run can pause
  mid-flight, the process can die, and work continues from the last checkpoint. [6] This is the one
  thing that is genuinely tedious to hand-roll correctly, and the one thing the sceptics tend not to
  have built.
- **Human-in-the-loop is not bolted on.** `interrupt()` inside a tool gates a destructive action,
  surfaces the proposed arguments for a human to edit, and resumes — without you inventing a
  pause/resume protocol. [7]
- **The safety-versus-latency trade is explicit.** `exit` / `async` / `sync` is a dial you set per
  graph rather than an all-or-nothing commitment. [8]
- **The escape hatch is real, and it answers the 2024 complaint directly.** Because `create_agent`
  is built on the runtime, dropping to a hand-built `StateGraph` is a refactor inside one framework
  rather than a rewrite out of it. [2]
- **Observability.** LangSmith tracing is the debugging story for what is otherwise an opaque loop —
  and traces are the metered unit of the paid tier, which is worth noticing. [12]

### The honest case against

- **The canonical critique** is Octomind's "Why we no longer use LangChain for building our AI
  agents" (Fabian Both, Staff Deep Learning Engineer at Octomind, June 2024). **Verified against the
  primary text on 19 September 2026 by the source-verification pass (`57772ad900e3`); the
  quotations below are safe to print and the do-not-cite caveat is lifted.**

  **How, with the bad news first: octomind.dev is gone.** Not refusing connections — **the domain
  has no `A` record at all**, for either the apex or `www`, though its MX records still resolve. So
  the ECONNREFUSED in milestone 5 was the front edge of the site being decommissioned, and there is
  no live primary page to open any more, in a browser or otherwise. The text was recovered from the
  **Internet Archive**, which was reachable this time. [15a] This is therefore verified against a
  *capture* of the primary rather than the primary, which is the best that will ever exist for it.
  Attribute to Octomind and date it in the sentence, exactly as the staleness table already says.

  What the recovered text says, verbatim:

  - The window: "We used LangChain in production for over 12 months, starting in early 2023 then
    removing it in 2024."
  - The abstraction complaint — and note the correction, because this brief had reshaped the clause
    into reported speech and changed a pronoun: "As its inflexibility began to show, we soon found
    ourselves diving into LangChain internals, to improve lower-level behavior of our system. But
    because LangChain intentionally abstracts so many details from you, it often wasn't easy or
    possible to write the lower-level code we needed to."
  - The nested-abstraction complaint, which was not in this brief and is the more quotable one:
    "LangChain also has a habit of using abstractions on top of other abstractions, so you're often
    forced to think in terms of nested abstractions to understand how to use an API correctly. This
    inevitably leads to comprehending huge stack traces and debugging internal framework code you
    didn't write instead of implementing new features."
  - The sub-agent limit, which is what the Orchestration suite cared about: "When we wanted to move
    from an architecture with a single sequential agent to something more complex, LangChain was the
    limiting factor. For example, spawning sub-agents and letting them interact with the original
    agent."
  - The observability complaint, also new here, and arguably the most durable of the lot: "we needed
    to dynamically change the availability of tools our agents could access, based on business logic
    and output from the LLM. But LangChain does not provide a method for externally observing an
    agent's state, resulting in us reducing the scope of our implementation to fit into the limited
    functionality available to LangChain Agents."
  - The line the genre is remembered for: "Once we removed it, we no longer had to translate our
    requirements into LangChain appropriate solutions. We could just code."
  - The replacement, which this brief had roughly right: the components they kept are "A client for
    LLM communication / Functions/Tools for function calling / A vector database for RAG / An
    Observability platform for tracing, evaluation etc.", and "A building block being something
    simple you feel is comprehensively understood and unlikely to change. For example, a vector
    database."
  - The self-aware caveat, which the book should carry if it uses the post at all, because it is
    why the post reads as fair rather than as a hit piece: "I'm sure that If I had attempted to
    build a framework such as LangChain when they did, I wouldn't have done any better." *(sic on
    the capital I in "If")*
- **The Hacker News thread is the more citable artefact** and fetches fine (20 June 2024, 480
  points). Strongest lines: "you have to go through 5 layers of abstraction just to change a minute
  detail"; "Most LLM applications require nothing more than string handling, API calls, loops, and
  maybe a vector DB"; "The documentation is horrible and they explain absolutely zero about the
  methods they use, so the only way to 'learn' is by reading their spaghetti code"; and the
  recurring "death by abstraction." One commenter calls it "an answer in search of a question" — a
  framework built before the patterns had settled. Notably **Harrison Chase (CEO) replied
  in-thread**, conceded the criticisms, and pointed at LangGraph and lower-level abstractions as the
  response. [17]
- **The sharpest *technical* criticism, and the one 1.0 did not answer: checkpoints are not durable
  execution.** Yaron Schneider (CTO, Diagrid — vendor-adjacent, they sell a Dapr-based alternative)
  argues LangGraph saves state but does not *run* your workflow. Named gaps: "no supervisor, no
  watchdog, no heartbeat mechanism" for failure detection; no automatic resumption (you must
  re-invoke with the right `thread_id`); no coordination preventing two processes resuming the same
  `thread_id` concurrently; and "there is no distributed execution, no task queue, no worker pool."
  A checkpoint is "a save point... you, the developer, are responsible for detecting the need to
  use."
  [18] This is the criticism most worth putting in a book, because it survives every version bump.
- **Migration cost is the live practitioner gripe.** A production upgrade write-up notes that
  `create_agent` "drops support for Pydantic models and dataclasses in agent state," requiring a
  hand-written Pydantic-to-TypedDict converter that must preserve LangChain's custom metadata on
  type annotations because `get_type_hints()` strips them. [19]
- **Naming churn outlived the stability promise.** The paid product was renamed within days of 1.0.
  [10] Docs and third-party writing still use both names — the old "docs drift" complaint in a new
  outfit.

### Adoption, all vendor-reported

At Series B (20 October 2025): **$125M raised at a $1.25B valuation**, led by IVP with Sequoia,
Benchmark, Amplify, CapitalG and Sapphire Ventures. The same post claims **90M combined monthly
downloads**, **35 percent** of the Fortune 500 using their services, and LangSmith monthly trace
volume up **12x year-over-year**. [13] GitHub: `langchain` **146.6k stars / 24.5k forks**,
`langgraph` **41.9k stars / 7.1k forks**, both MIT. [3][9]

Named production users come from LangChain's own case-study page and the outcome figures are
marketing: **Klarna** — "handles customer support tasks for 85 million active users — reducing
customer resolution time by 80%"; **Uber** — agents to "automate unit test generation" for
large-scale code migrations; **LinkedIn** — an AI recruiter with "a hierarchal agent system";
**Elastic** — SecOps threat detection; **AppFolio** — "response accuracy increased 2x — and they've
saved 10+ hours a week." [14] The `langgraph` PyPI page independently names Klarna, Replit and
Elastic. [5]

### Where the rest of the landscape sits

One line each, for situating only. **OpenAI Agents SDK** — "build agentic AI apps in a lightweight,
easy-to-use package with very few abstractions"; primitives are Agents, Handoffs, Guardrails;
OpenAI-default rather than provider-neutral. [21] **CrewAI** — "the leading open-source framework
for orchestrating autonomous AI agents," splitting Flows (structure, state, control) from Crews
(autonomous teams). [22] **Microsoft Agent Framework** — .NET, Python and Go; "the direct successor"
to both Semantic Kernel and AutoGen, combining AutoGen's abstractions with SK's enterprise features
plus graph workflows. [23] **AG2** — community fork of AutoGen by its original creators after they
left Microsoft; the AutoGen lineage is now split three ways. [25] **Pydantic AI** — typed end-to-end
agents with "first-party, co-maintained durable execution on Temporal, DBOS, Prefect, and Restate."
[20] **Mastra** — "a TypeScript framework for building AI agents and applications." [24] Note that
**Temporal appears not as a competitor but as the durability substrate other frameworks integrate
with** [20] — which is itself the answer to the Diagrid criticism above.

## Concrete example we can lift

**A refund agent for a support desk**, written both ways, because the trade is the point.

A customer emails about a duplicate charge. The agent reads the ticket, queries the billing API, and
proposes a refund. Policy: refunds over $500 need a manager's sign-off. Managers work business
hours, so the request may sit for fourteen hours. The service deploys twice a day.

*With LangGraph:* a `StateGraph` with nodes `triage → lookup_charge → propose_refund →
execute_refund`, a `PostgresSaver` checkpointer, `durability="sync"`, and `thread_id = ticket_id`.
Inside the `execute_refund` tool, an `interrupt()` returns the proposed amount and reason. The graph
stops. The process can be redeployed twice over. When the manager clicks approve, a webhook calls
the graph with `Command(resume=True)` on the same `thread_id` and execution continues *from inside
the tool* — not from the top of the graph. [6][7][8] Roughly twenty lines of framework surface.

*Rolling your own:* a `runs` table (ticket_id, message history, status, updated_at), a write after
every tool call, an idempotency key on the refund API call so a crashed-then-resumed run cannot
double-refund, a `pending_approval` row, and a resume endpoint that rehydrates the message list and
re-enters the loop at the right point. Call it 150–250 lines plus a migration. What you get back:
the state is your schema, greppable in `psql`, and a junior engineer can read the loop top to
bottom.

**The beat that makes this honest, and the reason to use this example rather than a cleaner one:
neither version detects the crash.** If the box dies mid-`lookup_charge`, LangGraph has the
checkpoint but nothing wakes up and resumes it — you still need a cron or a queue scanning for stale
threads. [18] The framework buys you the pause/resume *protocol*. It does not buy you the
*supervisor*. Most build-versus-buy arguments in this space quietly assume it does.

## Contradictions and gaps

- **Did 1.0 fix the 2024 complaints?** LangChain says yes — stable API, no breaking changes until
  2.0. [2] Practitioners report a real migration tax *inside* 1.0 (state typing) and continued
  minor-version feature churn. [19] Both are true. The accurate summary is that the churn moved from
  "imports break" to "state contracts break," which is progress but not the end of it.
- **"Durable execution" means two different things.** LangGraph uses it for checkpoint-and-resume
  [1][8]; Temporal, Dapr and DBOS use it for a runtime that guarantees completion. [18] Same phrase,
  materially different guarantees. Pydantic AI sidesteps the ambiguity by integrating *with* those
  runtimes rather than reimplementing them. [20] If the book uses the phrase at all, it must say
  which meaning.
- **Every adoption figure is vendor-reported.** 90M monthly downloads, 35% of the Fortune 500, 12x
  trace growth, and all case-study outcomes come from langchain.com. [13][14] No independent
  verification was found. Use shape, not figures, or attribute in the sentence.
- **Unverified:** release dates for `langchain` 1.4.2 and `langgraph` 1.2.11. ~~the Octomind primary
  page~~ — **recovered from the Internet Archive 19 September 2026 (`57772ad900e3`); quotations are
  now verbatim.** Still unverified, and now unverifiable: **any post-1.0 first-party rebuttal or
  update from Octomind**, because the domain no longer resolves. The critique is over two years old,
  its subject has had a major release since, and its author's site has gone dark — the book should
  say the first two rather than deploying it as current reporting, and has no reason to say the
  third.

## Staleness assessment

| Claim | Why it rots | Hedge |
|---|---|---|
| Package version numbers (1.4.2, 1.2.11) | Minor releases land continuously | Cut them; say "1.x" and name the 1.0 date |
| Pricing ($39/seat, $1.50/LCU) | Vendor pricing changes without notice | Date it in the sentence or omit; the *existence* of per-trace metering is the durable point |
| Product names (LangSmith Deployment, LangSmith Studio) | Renamed once already within days of 1.0 | Describe the thing ("the hosted deployment tier"), name it once parenthetically |
| Adoption and funding figures | Vendor-reported and growing | Round hard, date, attribute — or cut |
| "1.0 has no breaking changes until 2.0" | A promise, not an observation | Report as a stated commitment, not a property |
| Octomind's critique as current | June 2024, pre-1.0, primary source unreachable | Use it as the origin of a genre, dated in the sentence |

Durable for the life of the book: the LangChain-as-framework versus LangGraph-as-runtime split; the
observation that resumability is the real product; **checkpoints are not durable execution**; and
the refund-agent trade, which does not depend on any version number.

## Sources

[1] LangGraph overview — https://docs.langchain.com/oss/python/langgraph/overview — accessed
    19 September 2026
[2] LangChain and LangGraph Agent Frameworks Reach v1.0 Milestones, 22 October 2025 —
    https://www.langchain.com/blog/langchain-langgraph-1dot0 — accessed 19 September 2026
[3] langchain-ai/langchain — https://github.com/langchain-ai/langchain — accessed 19 September 2026
[4] langchain on PyPI — https://pypi.org/pypi/langchain/json — accessed 19 September 2026
[5] langgraph on PyPI — https://pypi.org/pypi/langgraph/json — accessed 19 September 2026
[6] LangGraph persistence — https://docs.langchain.com/oss/python/langgraph/persistence — accessed
    19 September 2026
[7] LangGraph interrupts — https://docs.langchain.com/oss/python/langgraph/interrupts — accessed
    19 September 2026
[8] Durability, LangChain reference —
    https://reference.langchain.com/python/langgraph/types/Durability — accessed 19 September 2026
[9] langchain-ai/langgraph — https://github.com/langchain-ai/langgraph — accessed 19 September 2026
[10] Product naming changes: LangSmith Deployment and LangSmith Studio —
     https://changelog.langchain.com/announcements/product-naming-changes-langsmith-deployment-and-langsmith-studio
     — accessed 19 September 2026
[11] LangSmith Deployment overview — https://docs.langchain.com/langgraph-platform/index — accessed
     19 September 2026
[12] LangChain pricing — https://www.langchain.com/pricing — accessed 19 September 2026
[13] LangChain Series B, 20 October 2025 — https://www.langchain.com/blog/series-b — accessed
     19 September 2026 — **vendor-reported throughout**
[14] Built with LangGraph — https://www.langchain.com/built-with-langgraph — accessed
     19 September 2026 — **vendor case studies; outcome figures are marketing**
[15] Why we no longer use LangChain for building our AI agents, Fabian Both, Octomind, June 2024 —
     https://octomind.dev/blog/why-we-no-longer-use-langchain-for-building-our-ai-agents —
     **dead: octomind.dev has no DNS `A` record as of 19 September 2026. Use [15a]**
[15a] **The one to cite** — Internet Archive capture of [15] —
     https://web.archive.org/web/2024/https://www.octomind.dev/blog/why-we-no-longer-use-langchain-for-building-our-ai-agents
     — **retrieved and read 19 September 2026 by `57772ad900e3`**; all quotations in this brief are
     verbatim from it. A capture of the primary, not the primary; cite as Octomind, dated June 2024
[16] GeekNews summary of the Octomind post — https://news.hada.io/topic?id=15459 — accessed
     19 September 2026 — **secondary; superseded by [15a] and no longer needed**
[17] Hacker News discussion of the Octomind post, 20 June 2024, 480 points —
     https://news.ycombinator.com/item?id=40739982 — accessed 19 September 2026
[18] Checkpoints Are Not Durable Execution, Yaron Schneider, Diagrid —
     https://www.diagrid.io/blog/checkpoints-are-not-durable-execution-why-langgraph-crewai-google-adk-and-others-fall-short-for-production-agent-workflows
     — accessed 19 September 2026 — **vendor-adjacent; the technical argument stands on its own**
[19] Lessons Learnt from Upgrading to LangChain 1.0 in Production —
     https://towardsdatascience.com/lessons-learnt-from-upgrading-to-langchain-1-0-in-production/ —
     accessed 19 September 2026
[20] Pydantic AI overview — https://pydantic.dev/docs/ai/overview/ — accessed 19 September 2026
[21] OpenAI Agents SDK (Python) — https://openai.github.io/openai-agents-python/ — accessed
     19 September 2026
[22] CrewAI introduction — https://docs.crewai.com/en/introduction — accessed 19 September 2026
[23] Microsoft Agent Framework overview —
     https://learn.microsoft.com/en-us/agent-framework/overview/agent-framework-overview — accessed
     19 September 2026
[24] Mastra docs — https://mastra.ai/docs — accessed 19 September 2026
[25] ag2ai/ag2 — https://github.com/ag2ai/ag2 — accessed 19 September 2026
