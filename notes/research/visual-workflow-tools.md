# Visual workflow tools — n8n and where the line falls for a developer

**Question asked:** what n8n and its neighbours are for, where they genuinely fit in a developer's
stack, and where the "non-developers can maintain it" pitch stops surviving contact with real
requirements.

**Researched:** 19 September 2026
**Confidence:** high on the licence and the product mechanics (both are primary); medium on the
criticism (individual practitioner posts, honestly reported but thin); low on every adoption and
revenue figure, all of which are press-release-derived or unverifiable.

Feeds the **Orchestration** suite, chiefly *Make the control flow deterministic*, and is the natural
counterweight to the framework material in
[`langchain-langgraph.md`](langchain-langgraph.md).

## Findings

### What it is, and the licence detail most write-ups get wrong

n8n describes itself as "Fair-code workflow automation platform with native AI capabilities. Combine
visual building with custom code, self-host or cloud, 400+ integrations," distributed "under the
Sustainable Use License and n8n Enterprise License." The Code node supports JavaScript, Python and
npm packages. [1]

**n8n is not open source, and says so itself.** The docs are unambiguous: "According to the Open
Source Initiative, open source licenses can't include limitations on use, so we do not call
ourselves open source." [3] Verbatim limitations from `LICENSE.md`: "You may use or modify the
software only for your own internal business purposes or for non-commercial or personal use"; "You
may distribute the software or provide it to others only if you do so free of charge for
non-commercial purposes"; and you may not "alter, remove, or obscure any licensing, copyright, or
other notices." Violations may be cured within 30 days of notice; repeated violations terminate
permanently. Two further traps: "Source code files that contain '.ee.' in their filename or '.ee' in
their dirname are NOT licensed under the Sustainable Use License" — those fall under the Enterprise
License — and "Content of branches other than the main branch (i.e. 'master') are not licensed." [2]

The docs give two concrete prohibited uses: "White-labeling n8n and offering it to your customers
for money" and "Hosting n8n and charging people money to access it." Embedding n8n inside your own
product is "usually yes, as long as the back-end process doesn't use users' own credentials to
access their data." [3]

**Where this bites, concretely:** a consultancy that self-hosts n8n and bills clients for access to
that instance is in breach. The same consultancy building workflows on the *client's own* instance
is fine. Any agency SaaS built by wrapping n8n needs the Enterprise License. This is a licence
compliance question that looks like a technology choice, and it is exactly the sort of thing a
developer discovers late.

### The AI layer is LangChain, and n8n says so

"n8n's AI nodes implement LangChain's JavaScript framework. Each node is configurable: choose your
own agent, LLM, memory, and other components." One stated divergence: "Memory sub-nodes only attach
to the AI Agent root node. Unlike LangChain, none of n8n's chain nodes support memory." [4] Worth a
sentence in the book — the visual tool and the code framework are not alternatives at the bottom of
the stack; one is a canvas over the other.

### Money and adoption, all press-release-derived

Series C, per n8n's own post dated 9 October 2025: "$180 million in Series C funding," total "$240
million" to date, at a "$2.5 billion" valuation, led by Accel, with Meritech, Redpoint, Evantic,
Visionaries Club, NVentures (NVIDIA) and T.Capital. Growth claims: "6x user growth" and "10x revenue
growth" year on year. [5] SAP strategic investment, n8n post dated 12 May 2026: "SAP has invested in
n8n. The investment values n8n at $5.2bn, more than double our valuation from less than a year ago,"
alongside "1.7 million monthly active builders" and "more than 1,400 enterprise customers." [6]
Secondary reporting adds SAP's stake as "more than EUR 60 million for a stake of around 1.3%." [7]

**None of these are audited.** Attribute in the sentence or cut.

### Version control, testing and debugging — what is actually true

- **Git integration exists but is gated and blunt.** Source control is Business and Enterprise only.
  Push "saves a copy of your workflows and tags, as well as credential and variable stubs, to Git."
  The docs carry a hard warning: "If you have made changes to a workflow in n8n, you must push the
  changes to Git before pulling. When you pull, it overwrites any changes you've made if they aren't
  stored in Git." [9]
- A practitioner account (24 January 2026) adds: "n8n limits you to two branches. Saving forces you
  to save *all* workflows at once — you can't save just one." [10] The artefact under review is a
  whole-workflow JSON blob including node coordinates, so a diff mixes "moved a node 40px" with
  "changed the routing condition."
- **There is no general test framework, and n8n staff conceded the gap.** On the community forum,
  26 November 2024: "We are currently working on a bunch of features related to testing and
  evaluating the output of workflows… I'm not able to give a timeline when those might come out,
  besides 'soon'." Another user in that thread: "I don't think that n8n is good for CI/CD as it is
  mostly the GUI tool." [11]
- **Evaluations shipped since, but check the scope.** The docs frame the feature around
  "LLM-powered workflows" and "AI workflows" — running a test dataset to "compare performance across
  different models or prompts." [12] That is LLM evaluation, not unit testing of deterministic
  branching logic. The gap the forum thread named is still open.

### Two migration accounts, both honest, both thin

- **n8n to Python, 11 May 2026.** The author is explicit that n8n did not fail: "Visual workflow,
  no-code glue, easy HTTP nodes, built-in error routing… when we were validating the core loop, the
  visual canvas was genuinely useful." What forced the move: "Every `if/elif` chain lived in a text
  field, untestable"; "Nothing in the framework *prevents* you from firing off a git commit in any
  arbitrary Code node"; sandbox I/O limits. Post-migration: "106 behavioral tests pass." The thesis
  line is the best single sentence found in this whole pass: **"The moment your AI orchestrator has
  enough opinions to deserve a test suite, it's time to write real code."** [13]
- **34 automations rewritten to DBOS (TypeScript durable workflows).** Complaints: debugging
  failures was "a multi-hour archaeological dig"; "Every change was a prayer"; "as the system grew,
  I started fighting the tooling instead of building." Claims roughly 1.4GB → 150MB memory and
  ~1,167 workflows/second. **Publication date could not be verified** and the benchmarks are
  unaudited. [14]

### The honest case for

- **A connector surface you should not rebuild.** 400+ maintained built-in nodes means OAuth flows,
  pagination, rate limits and API drift are someone else's maintenance burden. [1]
- **Operational plumbing for free.** Scheduling, retries, error branches, execution history, and
  queue mode for horizontal scale. [15]
- **Self-hosting for data residency**, permitted at no cost for unlimited internal business use.
  [2][3]
- **A running artefact non-developers can see.** This is the real differentiator against a code
  framework: LangGraph "lacks a built-in visual representation for execution, making it difficult
  for non-engineering stakeholders to review or audit the system's logic." [16] A canvas the support
  lead can open is a genuine organisational asset, not a toy.
- **Prototyping agent loops.** Both migration authors independently kept n8n for exactly this.
  [13][14]

### The honest case against

- **The review story is weak rather than absent.** Paid-tier, two-branch, all-or-nothing on save,
  and a pull that silently overwrites unpushed work. [9][10] "It's in git" is technically true and
  practically misleading.
- **No general test framework.** Evaluations cover LLM outputs, not deterministic logic. [12][11]
- **Code nodes are the worst of both worlds.** Logic in a textarea: no breakpoints, no stack traces
  into your IDE, no linting, no unit tests — and no structural boundary stopping a Code node doing
  something dangerous. [13][10]
- **Scale failures are design failures.** Monolithic workflows produce "duplicates, timeouts,
  partial writes"; unpruned execution data turns Postgres into "a graveyard of JSON blobs." [17]
- **The licence forecloses a business model** you might not realise you were heading towards. [3]

### Where the neighbours sit

One line each, for situating only. **Zapier** — hosted, no self-host; "9,000+ apps," with Zapier
Agents now GA. [21] **Make** — hosted visual scenario builder, closer to Zapier on branching. [22]
**Windmill** — open-source workflow engine and developer platform; backend AGPLv3 "except any
snippets of code under the compile flag 'enterprise'." [23] **Activepieces** — MIT, "except the
packages/ee/ directories." [23] **Temporal** — code-first durable execution; "workflows as stateful
functions that can run for long periods without breaking." [24] **Dify** — full-stack LLM app
platform with knowledge base and debugging; free Community Edition, Professional $59/month. [22]
**Flowise / Langflow** — LLM-app and RAG prototype builders; Langflow is MIT with LangGraph
multi-agent support and custom Python nodes. [22] **Airflow / Prefect / Dagster** — the
data-engineering orthodoxy that solved DAG orchestration years ago, "purpose-built for data
pipelines," with Airflow named alongside Temporal as a "golden standard… battle-tested." [24]

That last entry deserves more than a line in the book. The visual-workflow discourse is largely
rediscovering scheduling, retries, backfills and DAG observability, which data engineering shipped a
decade ago. A developer who reaches for n8n to orchestrate a nightly pipeline is often reaching past
a tool that already does it with a code-first interface and a real test story.

## Concrete example we can lift

**A support-triage automation, and the exact point where it outgrows the canvas.**

A four-person team ships it in an afternoon: Zendesk ticket arrives → classify urgency with an LLM →
enrich from the CRM → route to Slack, or open a Linear issue if it looks like a bug. Roughly nine
nodes. The Zendesk, HubSpot, Slack and Linear nodes handle auth and pagination; retries and the
error branch are configuration rather than code; the support lead can open the canvas and change the
urgency keywords without a PR. Every one of those is a real win and the book should say so before it
says anything else.

Three months later the routing rules have grown. Enterprise-tier customers skip triage. Anything
mentioning a security keyword pages on-call. Repeat tickets from the same account within 24 hours
get merged — and *that* rule needs state. The logic now lives in a 120-line Code node nobody can
unit test, the canvas has eleven branches, and a mis-routed security ticket takes two hours to
diagnose because the only record is an execution log in a web UI.

**The line falls at the state-plus-conditionals boundary.** Keep in n8n: the Zendesk trigger, the
credentialed API calls, the Slack and Linear writes, the schedule, the retry policy — everything
whose maintenance cost you would otherwise inherit. Move to code: the routing decision, exposed as
one endpoint, `POST /triage`, taking a ticket and returning a routing decision, called from an HTTP
Request node. That endpoint gets a test suite, a debugger and a code review. The support lead keeps
a visible workflow; the developers get the eleven branches into a file where `git diff` means
something.

Both migration authors converged on this split independently, which is the strongest evidence
available for it. [13][14] The play writes itself: **the canvas owns the edges of the system, the
code owns the judgement.**

## Contradictions and gaps

- **Valuation timeline conflict, unreconciled.** Bloomberg reported Accel leading "at a $2.3
  Billion Valuation" on 7 August 2025 [18]; n8n's own post of 9 October 2025 says "$2.5 billion."
  [5] Likely pre- versus post-money, or a round that grew, but the sources disagree and primary
  material did not settle it.
- **Integration count contradicts inside n8n's own README** — the tagline says "400+ integrations,"
  the body says "1,500+." [1] Third-party counts reconcile this as 400+ built-in plus 600+ community
  npm packages. [8] Treat "400+ built-in nodes" as the defensible number.
- **ARR is unverified.** getlatka lists "$40M Est. ARR"; a newsletter claims "$100M+ ARR." [19]
  Neither is company-confirmed. **Do not use either.**
- **Two widely-repeated low-code statistics did not survive verification and must not be used.** The
  "43% of citizen developer initiatives scaled back, paused or discontinued" figure attributed to
  Gartner appears only in secondary aggregator blogs with no primary citation; the "25–30% rewrite
  rate for no-code projects" traces to vendor marketing. [20] Both are exactly the kind of number a
  book about honest engineering should not launder.
- **The real gap: there is no rigorous, named enterprise case study of migrating off n8n at
  scale.** The best available evidence is two individual practitioner blog posts. [13][14] The book
  should say the evidence is thin rather than dress two blog posts as a trend.

## Staleness assessment

| Claim | Why it rots | Hedge |
|---|---|---|
| Valuation and funding figures | Two rounds in nine months already | Attribute and date, or cut — the argument never depends on them |
| Node/integration counts | Growing monthly, and n8n's own README disagrees with itself | Say "several hundred built-in connectors" |
| "No general test framework" | Actively being worked on; Evaluations already shipped for the LLM case | Name the *scope* of what shipped and date it; the claim is about coverage, not effort |
| Source-control limitations (two branches, all-or-nothing save) | A single-practitioner report on a paid feature | Attribute; verify before publication |
| Pricing of the neighbours (Dify $59/mo etc.) | Obvious | Cut from prose; keep here for orientation |
| The Sustainable Use License terms | Stable since v1.0 and central to n8n's identity | Safe to quote, with the licence version named |

Durable for the life of the book: "n8n is not open source and says so"; the state-plus-conditionals
boundary; the observation that the AI layer *is* LangChain; the JSON-blob review problem; and the
point that data engineering solved DAG orchestration first.

## Sources

[1] n8n-io/n8n — https://github.com/n8n-io/n8n — accessed 19 September 2026
[2] n8n `LICENSE.md` (Sustainable Use License v1.0) —
    https://github.com/n8n-io/n8n/blob/master/LICENSE.md — accessed 19 September 2026
[3] Sustainable Use License / n8n Community license, n8n docs —
    https://docs.n8n.io/n8n-community-license/ — accessed 19 September 2026
[4] LangChain in n8n, n8n docs — https://docs.n8n.io/build/integrate-ai/langchain-in-n8n.md —
    accessed 19 September 2026
[5] n8n raises $180m to get AI closer to value with orchestration, 9 October 2025 —
    https://blog.n8n.io/series-c/ — accessed 19 September 2026 — **press release**
[6] Announcing SAP's strategic investment in n8n, 12 May 2026 — https://blog.n8n.io/n8n-sap/ —
    accessed 19 September 2026 — **press release**
[7] SAP invests in AI workflow orchestration company n8n at $5.2bn valuation, Verdict —
    https://www.verdict.co.uk/sap-invests-n8n/ — accessed 19 September 2026
[8] How Many Integrations Does n8n Have in 2026? — https://vps.us/blog/how-many-n8n-integrations/ —
    accessed 19 September 2026 — **secondary**
[9] Use Git in n8n, n8n docs —
    https://docs.n8n.io/administer/use-source-control-and-environments/use-git-in-n8n — accessed
    19 September 2026
[10] n8n's Engineering Limitations: Testing, Version Control, Licensing, PageLines,
     24 January 2026 — https://www.pagelines.com/blog/n8n-engineering-limitations — accessed
     19 September 2026
[11] Testing capabilities, n8n community forum, November 2024 —
     https://community.n8n.io/t/testing-capabilities/62714 — accessed 19 September 2026
[12] Understand why to test, n8n docs —
     https://docs.n8n.io/build/integrate-ai/test-and-improve-ai-workflows/understand-why-to-test —
     accessed 19 September 2026
[13] We Didn't Migrate from n8n to Python Because n8n Failed, 11 May 2026 —
     https://dev.to/josephyeo/we-didnt-migrate-from-n8n-to-python-because-n8n-failed-k9j — accessed
     19 September 2026
[14] I Deleted My No-Code Automation Platform and Rewrote 34 Workflows in TypeScript —
     https://dev.to/achiya-automation/i-deleted-my-no-code-automation-platform-and-rewrote-34-workflows-in-typescript-emh
     — accessed 19 September 2026 — **date unverified; benchmarks unaudited**
[15] Scaling n8n Without Losing Your Mind —
     https://medium.com/@Quaxel/scaling-n8n-without-losing-your-mind-829c950d9176 — accessed
     19 September 2026
[16] LangGraph vs n8n: Choosing the Right Framework for Agentic AI, ZenML —
     https://www.zenml.io/blog/langgraph-vs-n8n — accessed 19 September 2026
[17] n8n at Scale: Workflows Fail by Design —
     https://medium.com/@bhagyarana80/n8n-at-scale-workflows-fail-by-design-951becd948e3 — accessed
     19 September 2026
[18] Accel Leading Round for AI Startup n8n at $2.3 Billion Valuation, Bloomberg, 7 August 2025 —
     https://www.bloomberg.com/news/articles/2025-08-07/accel-leading-round-for-ai-startup-n8n-at-2-3-billion-valuation
     — accessed 19 September 2026 — **headline only; paywalled**
[19] n8n.io Revenue 2025, getlatka — https://getlatka.com/companies/n8nio — accessed
     19 September 2026 — **unverified; do not use**
[20] No-Code Transformations Usage Trends, Integrate.io —
     https://www.integrate.io/blog/no-code-transformations-usage-trends/ — accessed
     19 September 2026 — **vendor content; figures unverified, do not use**
[21] Zapier Agents: Combine AI agents with automation —
     https://zapier.com/blog/zapier-agents-guide/ — accessed 19 September 2026
[22] Dify vs Flowise vs Langflow: Best AI App Builder? (2026), ToolHalla —
     https://toolhalla.ai/blog/dify-vs-flowise-vs-langflow-2026 — accessed 19 September 2026
[23] Best Open Source AI Automation Tools 2026, scored.tools —
     https://scored.tools/blog/best-open-source-ai-automation-tools-2026/ — accessed
     19 September 2026
[24] Managed Airflow vs Dagster vs Prefect vs Temporal, Astronomer —
     https://llms.astronomer.io/managed-airflow-vs-dagster-vs-temporal — accessed 19 September 2026
