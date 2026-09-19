# Token pricing and model tiering

**Question asked:** what does agentic coding actually cost — the per-million-token prices across
vendor tiers, the caching and batching levers, the subscription-versus-API choice, what really
drives spend inside an agent loop, and where cheap models are a false economy.

**Researched:** 19 September 2026

**Confidence:**

- **Absolute prices — high, for today only.** Every figure below was fetched from the vendor's own
  live pricing page on 19 September 2026. None of it is from memory. All of it will be wrong within
  months; see *Staleness assessment*, which is the most important table in this brief.
- **Price ratios and mechanism — high and durable.** The output:input multiple, the 0.1x cache-read
  multiplier, the two-tier long-context step, and the 50% batch discount have held their *shape*
  across every vendor and every model generation on the page today. These are what the book should
  build on.
- **Subscription terms — medium.** Plan prices verified from vendor pages; per-plan allowances are
  patchily published and two vendors changed billing model within the last six months.
- **What drives spend in a loop — high.** Converging evidence from Anthropic's own docs, a peer-
  reviewed-style arXiv study of eight frontier models on SWE-bench Verified, and gateway telemetry.
- **Cost-per-task figures — low to medium.** This is the weakest area. Most published numbers are
  either vendor-reported, modelled rather than measured, or lack model versions. Flagged throughout.
- **Model-tiering evidence — medium.** One good controlled study (Tessl, 10 PRs, 4 models); the rest
  is assertion. The headline routing-savings numbers in circulation come from chat routing, not
  agentic coding, and should not be transferred.

Feeds the **Economics** suite: *Understand what you are paying for*, *Match the model to the job*,
and *Know when not to use an agent*.

**Cross-reference:** [`token-filtering.md`](token-filtering.md) is the companion brief and carries
the cautionary tale — a tool whose dashboard reported "96.2 million tokens saved" over trials in
which the measured bill rose 7.6%. That brief explains *why* a token-counting dashboard lies: most
of a session's input arrives as cached re-reads billed at a tenth of list, so a filter that scores
itself in raw tokens grades against a counterfactual the billing system never applies. This brief
supplies the pricing arithmetic that makes that explanation concrete, and the two should be read as
a pair. Where that brief says "measure the bill, not the dashboard," this one says what the bill is
made of.

## Findings

### The tier ladder is the durable fact; the rungs move

Every vendor runs a three-to-four rung ladder, and on 19 September 2026 the ladders look like this
(input price per million tokens, USD):

- **Anthropic** [1]: Fable 5.1 $10 → Opus 5 $5 → Sonnet 5 $2 → Haiku 4.5 $1. Top-to-bottom spread
  **10x** (*derived*: 10 ÷ 1).
- **OpenAI** [3]: gpt-6-astra $10.00 → gpt-5.6-sol $4.00 → gpt-5.6-terra $2.00 → gpt-5.6-luna
  $0.20. Spread **50x** (*derived*: 10.00 ÷ 0.20).
- **Google** [7]: Gemini 3.1 Pro Preview $2.00 → Gemini 3.8 Flash $0.75 → Gemini 3.1 Flash-Lite
  $0.25. Spread **8x** (*derived*: 2.00 ÷ 0.25).

The book's usable claim is not any of these numbers. It is: **a frontier token costs roughly an
order of magnitude more than a small-tier token, and the gap between adjacent rungs is roughly
2–3x.** That has been true at every snapshot, across every vendor, for as long as there have been
three rungs.

### The output:input multiple is between 4x and 8x, and Anthropic's is uniform

*All ratios derived from the list prices in the Price table.*

- **Anthropic: exactly 5.0x on every single model.** Fable 5.1 $50/$10, Opus 5 $25/$5, Sonnet 5
  $10/$2, Sonnet 4.6 $15/$3, Haiku 4.5 $5/$1. [1] The uniformity is itself worth noting: Anthropic
  prices the whole catalogue off one multiplier, so switching Claude tiers never changes the
  input/output trade-off, only the absolute level.
- **OpenAI: 5.0x to 8.0x, and it varies by generation.** gpt-6-astra and gpt-5.6-sol are 5.0x;
  gpt-5.6-terra, gpt-5.6-luna, gpt-5.5, and gpt-5.4 are 6.0x; gpt-5, gpt-5.1, gpt-5.2, gpt-5-mini,
  and gpt-5-nano are 8.0x. [3] Newer OpenAI generations have moved *down* the output multiple.
- **Google: 4.0x to 8.33x, the widest spread.** Gemini 2.5 Flash-Lite 4.0x ($0.40/$0.10); Gemini 3.1
  Pro Preview 6.0x ($12.00/$2.00); Gemini 2.5 Pro 8.0x ($10.00/$1.25); Gemini 3.5 Flash-Lite and
  Gemini 2.5 Flash 8.33x ($2.50/$0.30). [7]

**Why this matters less than it looks.** In an agentic loop the output multiple is nearly irrelevant
to the bill, because output is a rounding error in the token mix. Measured shares below.

### Long-context surcharges: a cliff, not a ramp — and Anthropic has removed theirs

Two of three vendors charge a step above a context threshold, and both use the *same* shape:

| Vendor | Threshold | Input multiplier | Output multiplier | Repriced |
|---|---|---|---|---|
| OpenAI | **272K input tokens** | **2x** (and 2x on cached input) | **1.5x** | whole request [4] |
| Google (Pro tiers only) | **200k tokens** | **2x** | **1.5x** | whole request [7] |
| Anthropic | none | — | — | — [1] |

OpenAI's own model page states the rule verbatim for gpt-6-astra: requests above 272K input tokens
are "priced at 2x input and cache rates and 1.5x output for the full request." [4] Verified against
the price table: astra $10.00 → $20.00 input, $1.00 → $2.00 cached, $50.00 → $75.00 output; sol
$4.00 → $8.00 and $20.00 → $30.00; terra $2.00 → $4.00 and $12.00 → $18.00. [3] Google's Pro rows
show the identical arithmetic: Gemini 3.1 Pro Preview $2.00 → $4.00 input and $12.00 → $18.00
output at the 200k line; Gemini 2.5 Pro $1.25 → $2.50 and $10.00 → $15.00. [7] Google's Flash and
Flash-Lite tiers have **no** step.

**The cliff is the point.** It is not a marginal rate on the tokens above the line — the *entire*
request reprices. A 273,000-token prompt to gpt-6-astra costs twice as much on input as a
272,000-token one, for 1,000 extra tokens. In an agent loop that accretes context turn by turn,
this is a step function you cross without noticing.

**Anthropic went the other way.** "Claude 4.6 and later models … include the full 1M token context
window at standard pricing. (A 900k-token request is billed at the same per-token rate as a
9k-token request.)" [1] This is a change from earlier Claude generations, which did carry a
long-context premium — so a book claim of the form "all vendors surcharge long context" is now
false, and a claim of the form "check whether your vendor surcharges long context, because two of
three currently do" is right.

### Prompt caching is the single biggest lever, and all three vendors converged on 0.1x

**The cache-read multiplier is 0.1x of base input on all three vendors, for almost every model.**
*Derived* from the list prices: Anthropic Opus 5 $0.50 ÷ $5 = 0.1x [1]; OpenAI gpt-6-astra $1.00 ÷
$10.00 = 0.1x [3]; Gemini 3.1 Pro Preview $0.20 ÷ $2.00 = 0.1x [7]. Anthropic states the multiplier
explicitly, and notes one exception: "0.1x base input price (0.025x on Claude Fable 5.1 and Claude
Mythos 5.1)." [1] OpenAI describes it as "discounted up to 90%" and, for GPT-5.6 and later, "0.1×
the uncached input-token rate." [5]

Beyond the shared read multiplier, the three mechanics differ substantially.

**Anthropic — explicit, priced writes, two TTLs.** [1][2]

| Cache operation | Multiplier on base input | Duration |
|---|---|---|
| 5-minute cache write | **1.25x** | 5 minutes |
| 1-hour cache write | **2x** | 1 hour |
| Cache read (hit) | **0.1x** (0.025x on Fable 5.1 / Mythos 5.1) | same as preceding write |

Anthropic states the break-even directly: "caching pays off after one cache read for the 5-minute
duration (1.25x write), or after two cache reads for the 1-hour duration (2x write)." [1]
*Derived* from those multipliers: the same prefix costs **12.5x more on a miss-then-write than on a
hit** (1.25 ÷ 0.1), which is the number that makes cache invalidation expensive rather than merely
annoying.

Other Anthropic specifics worth having:

- **Minimum cacheable prompt**: 512 tokens (Fable 5.1, Mythos 5.1, Opus 5, Fable 5, Mythos 5);
  1,024 (Opus 4.8, Sonnet 5, Sonnet 4.6, Sonnet 4.5); 2,048 (Mythos Preview, Opus 4.7, Haiku 3.5);
  4,096 (Opus 4.6, Opus 4.5, Haiku 4.5). "Shorter prompts cannot be cached, even if marked with
  `cache_control` … and no error is returned." [2]
- **TTL is measured from request start, not response end**: "if a response takes 4 minutes to
  stream, a follow-up request that reuses the same cached prefix must start within about 1 minute of
  that response completing." [2] For a slow reasoning model on a 5-minute TTL this is brutal.
- **Up to 4 cache breakpoints.** [2]
- **What invalidates the cache**: modifying *tool definitions* invalidates the entire cache;
  toggling web search or citations rewrites the system prompt and invalidates system and message
  caches; switching between fast and standard speed does too; thinking and effort parameter changes
  always invalidate message blocks. [2] An MCP server that mutates its tool list mid-session is
  therefore a cache bomb.
- **Caching can be automatic**: "Add a single `cache_control` field at the top level of your
  request. The system automatically manages cache breakpoints as conversations grow." [1]

**OpenAI — automatic, free writes, prefix-matched.** [5]

- "Prompt caching is enabled by default for supported OpenAI models." There is **no write premium**
  — the cheapest structural difference from Anthropic. You pay $1.00/MTok instead of $10.00/MTok on
  gpt-6-astra for reused prefix, and nothing extra to put it there.
- Minimum cacheable prompt: **1,024 tokens** for GPT-5.6 and later; "varies by request settings for
  earlier models."
- Retention: "A cached prefix remains eligible for reuse for **30 minutes** after its most recent
  write or reuse" on GPT-5.6+. Earlier models: in-memory retention (5–10 minutes inactive) or a
  24-hour extended-retention option.
- Matching: "Cache reuse requires the entire rendered prefix to match. If content or a relevant
  setting changes before a breakpoint, the prefix after that change cannot match the existing cache
  entry."

**Google — implicit is free and automatic; explicit charges rent.** [7][8]

- "Implicit caching is enabled by default for all Gemini 2.5 and newer models." "There is nothing
  you need to do in order to enable this." "We automatically pass on cost savings if your request
  hits caches." [8]
- Minimum tokens for an implicit hit: 2,048 for Gemini 2.5 models, rising to 4,096 for newer
  models. [8]
- "The **Interactions API** only supports implicit caching. Explicit caching (manually creating and
  managing cache objects) is not supported in the Interactions API." [8]
- **Google is the only vendor that bills cache *storage* by the hour**, and the rate is not small:
  $0.50 per 1M tokens per hour (Gemini 3.8 Flash, through 31 December 2026), $1.00 (Gemini 3.5
  Flash, Gemini 2.5 Flash, Gemini 3.1 Flash-Lite), **$4.50** (Gemini 3.1 Pro Preview and Gemini 2.5
  Pro). [7] *Derived*: holding a 200,000-token explicit cache on Gemini 3.1 Pro Preview across an
  8-hour working day costs 0.2 × $4.50 × 8 = **$7.20 in rent alone**, whether or not you read it
  once. On Anthropic and OpenAI, storage is free and you pay only at write and read.

### Batch is a flat 50% on all three vendors

- Anthropic: "a 50% discount on both input and output tokens"; every batch row is exactly half the
  standard row. [1] "Batch API and prompt caching discounts can be combined." [1]
- OpenAI: every batch row is exactly half the standard row (gpt-6-astra $5.00/$0.50/$25.00 against
  $10.00/$1.00/$50.00). [3]
- Google: "Batch API provides 50% cost reduction"; verified row by row. [7]

Google additionally publishes a **Flex** tier priced identically to Batch, and a **Priority** tier
at *1.8x* standard (*derived*: Gemini 3.8 Flash $1.35 ÷ $0.75 = 1.8; $6.75 ÷ $3.75 = 1.8; Gemini 3.1
Pro Preview $3.60 ÷ $2.00 = 1.8). [7] OpenAI's fast mode is 2x standard. [3] Anthropic's fast mode
for Opus 5 / Opus 4.8 is $10/MTok input and $50/MTok output — *derived*: exactly **2x** the standard
$5/$25, and "not available with the Batch API." [1]

**Batch is irrelevant to interactive agentic coding** and the book should say so plainly. Anthropic
spells out why in the Managed Agents pricing table: the Batch API discount does not apply because
"Sessions are stateful and interactive. There is no batch mode." [1] Batch is for the offline work
*around* the agent — bulk classification, migration sweeps, eval runs — not the loop itself.

### Subscription versus API: three vendors, three billing philosophies, all changed this year

**Anthropic — seat allowances with a metered overflow.** [9]

| Plan | Price | Notes |
|---|---|---|
| Free | $0 | Claude Code not included |
| Pro | **$17/month annual, $20/month monthly** | Claude Code "shares the same usage limits as the rest of your plan" |
| Max 5x | **$100/month** | "5x more usage per 5-hour session than Pro" |
| Max 20x | see *Do not cite* | "20x more usage per 5-hour session than Pro" |
| Team standard seat | **$20/month annual, $25/month monthly** | |
| Team premium seat | **$100/month annual, $125/month monthly** | "5x more usage than standard seats" |
| Enterprise | **$20/seat/month, billed annually** | "Usage cost scales with model and task" |

"Every plan has usage limits that reset on a rolling five-hour session window, and paid plans add
weekly limits on top." "When you reach a limit, you can wait for it to reset, move to a higher plan,
or, on paid plans, turn on usage credits to keep working at standard API rates." [9]

Two details from the Claude Code docs that matter more than the plan prices:

- **The cache TTL you get depends on how you are billed.** "The lifetime is an hour on a
  subscription and drops to five minutes once you're drawing on usage credits; on an API key or
  cloud provider, it's five minutes by default." [10] So the *same session* becomes materially more
  expensive to resume after a break the moment you tip over your plan allowance — a discontinuity
  almost nobody anticipates.
- **Reported cost figures are list-price estimates, not invoices.** "Claude Code computes the dollar
  figure locally from token counts at list price, unless a `modelPricing` table is in effect." [10]
  The docs also record two historical bugs where the local figure diverged from the bill: before
  v2.1.239 the 1.1x data-residency rate was not applied to the session cost figure, "so the session
  cost figure was lower than the bill"; before v2.1.211 totals kept accumulating across `/clear`.
  [10] This is the same lesson as `token-filtering.md`, from the first party: the local dashboard is
  an estimate, the Console is the bill.

**GitHub Copilot — abandoned "premium requests" for dollar-denominated credits on 1 June 2026.**
[11][12]

Announced 27 April 2026: "Starting June 1, your Copilot usage will consume GitHub AI Credits," and
"premium request units (PRUs) will be replaced by GitHub AI Credits." [11]

| Plan | Price | Included credits |
|---|---|---|
| Copilot Pro | **$10/month** | **$10 in monthly AI Credits** |
| Copilot Pro+ | **$39/month** | **$39 in monthly AI Credits** |
| Copilot Business | **$19/user/month** | **$19 in monthly AI Credits** |
| Copilot Enterprise | **$39/user/month** | **$39 in monthly AI Credits** |

"1 AI credit = $0.01 USD." [12] Credits are consumed "based on token usage, including input, output,
and cached tokens, according to the published API rates for each model." [11] "Code completions and
next edit suggestions are not billed in AI credits. They remain unlimited for all paid Copilot
plans." [12]

The **legacy multiplier table** survives only for annual plans that stayed on request-based billing
after 1 June 2026, and is worth keeping as a historical artefact because it shows how badly a
request-count proxy distorts real cost: [13]

| Model | Multiplier | | Model | Multiplier |
|---|---|---|---|---|
| MAI-Code-1.1-Flash | 0.25 | | GPT-5.4 | 6 |
| Claude Haiku 4.5 | 0.33 | | GPT-5.4 mini | 6 |
| GPT-4o / GPT-4o mini | 0.33 | | Gemini 3 Pro | 6 |
| GPT-5 mini | 0.33 | | Claude Sonnet 4.6 | 9 |
| GPT-5.1-Codex-Mini | 0.33 | | Gemini 3.5 Flash | 14 |
| GPT-5.1 / -Codex / -Codex-Max | 3 | | Claude Opus 4.7 / 4.8 | 27 |
| GPT-5.3-Codex | 6 | | GPT-5.5 | 57 |

Copilot code review carries a multiplier of **13**; auto model selection gets a 10% discount. [13]
Additional premium requests on the legacy scheme cost **$0.04/request**. [14] *Derived*: the
multiplier spread from MAI-Code-1.1-Flash (0.25) to GPT-5.5 (57) is **228x**, against an API list
spread between the cheapest and dearest models on the same table of well under 100x. A
request-count proxy is not a cost model, and GitHub replacing it with dollar-denominated credits is
the industry conceding that.

**OpenAI / Codex — retired per-message pricing on 2 April 2026 for token-based credits.** [17]

| Plan | Price |
|---|---|
| Free | $0/month |
| Go | $8/month |
| Plus | $20/month |
| Pro | From $100/month |
| Business | $20/user/month annual ($25 monthly) |

Published 5-hour-window allowances, in "local messages" — and the ranges are enormous, which is
itself the finding: [17]

| Model | Plus | Pro 5x | Pro 20x | Business |
|---|---|---|---|---|
| GPT-6 Astra | 5–45 | 25–225 | 100–900 | 5–45 |
| GPT-5.6 Sol | 10–100 | 50–500 | 200–2,000 | 10–100 |
| GPT-5.6 Luna | 250–2,000 | 1,250–10,000 | 5,000–40,000 | 250–2,000 |

These are "not fixed message limits." A **9x spread** between the low and high end of the same
allowance (*derived*: 45 ÷ 5) is the plainest published admission that an agentic "message" has no
fixed cost.

Rate card: GPT-6 Astra **250 credits per 1M input tokens, 1,250 per 1M output**; GPT-5.6 Luna **5
credits per 1M input, 30 per 1M output**. [17] *Derived*: against the API list prices [3], one Codex
credit equals exactly **$0.04** of list-price tokens — 250 credits ↔ $10.00 and 1,250 ↔ $50.00 on
Astra; 5 ↔ $0.20 and 30 ↔ $1.20 on Luna. Four independent checks, all $0.04. Note this is *not* the
same unit as a GitHub AI Credit ($0.01), and the two are frequently conflated.

**Cursor — token-metered at API rates with a published per-token markup.** [15][16]

Hobby free; **Pro $20/month**; **Pro+ $60/month** ("3x Pro limits on Agent"); **Ultra $200/month**
("20x Pro limits on Agent"). [16] Billing: "When you select a specific third-party model, usage is
drawn from the **Other Models** pool at that model's API rate." [15] On Teams and Enterprise, Cursor
adds a **"Cursor Token Rate" of $0.25 per million tokens** on third-party models, "on top of model
API pricing for included usage, on-demand usage, and BYOK usage"; first-party models (Grok,
Composer) are exempt. [15] Auto mode routes in Cost, Balance, or Intelligence modes and bills "at
the list price of the model each request is routed to." [15]

*Derived*: $0.25/MTok on top of, say, Sonnet 5's $2.00 input is a **12.5% markup on input**; on top
of Haiku 4.5's $1.00 it is **25%**. The flat per-token surcharge is regressive — it costs
proportionally more the cheaper the model you route to, which quietly erodes the case for tiering
down inside Cursor.

**The one comparison that matters for a team.** Anthropic's own enterprise figure is "around **$13
per developer per active day** and **$150–250 per developer per month**, with costs remaining below
**$30 per active day for 90% of users**." [10] *Derived*: Copilot Pro's entire $10/month credit
allowance is less than one active day of that. The subscription tiers on all three vendors are
priced for assisted editing; agentic coding at volume lands in metered overflow more or less
immediately, which is why every vendor shipped a metered overflow mechanism this year.

### The pricing detail nobody expects: a token is not a token

"Claude 4.7 and later models and Claude Mythos Preview use a newer tokenizer that contributes to
their improved performance … **This tokenizer produces approximately 30% more tokens for the same
text.** The exact increase depends on the content and workload shape. Claude Sonnet 4.6 and earlier
models use the previous tokenizer." [1]

This makes cross-generation per-token price comparison unsound. *Derived illustration*: Sonnet 4.6
at $3/MTok versus Sonnet 5 at $2/MTok looks like a 33% price cut, but Sonnet 5 is a 4.7-era model,
so on the same source text the effective cost ratio is closer to $2 × 1.30 = $2.60 against $3.00 —
a **13% cut, not 33%**. Any table that compares prices per million tokens across a tokenizer change
is comparing different units with the same name. This deserves a callout box.

Related trap in the same family: the per-request fixed overheads. Anthropic publishes the tool-use
system prompt cost per model — 286 tokens (Opus 5, `auto`) up to 804 (Opus 4.7, `any`) — plus about
**4,500 input tokens** to declare the computer-use toolset and about **6,600** for the browser-use
toolset, per request. [1] Those ride on every turn, and they are what tool-definition churn
invalidates.

### Thinking and reasoning tokens are billed as output, and the default budget is large

- Anthropic: "Thinking tokens are billed as output tokens, and the default budget can be tens of
  thousands of tokens per request depending on the model." Extended thinking is "enabled by
  default." "You can't turn off thinking on Fable models, which always use extended thinking." [10]
- OpenAI: "While reasoning tokens are not visible via the API, they still occupy space in the
  model's context window and are billed as output tokens." [6] For GPT-5.6 models the default is to
  render "available reasoning from earlier turns" into the next sample, so reasoning can persist
  across turns rather than being discarded. [6]

*Derived*: on Opus 5 at $25/MTok output, a 30,000-token thinking budget spent on a single turn is
**$0.75** before a word of answer is written. At 40 turns that is $30 — more than twice Anthropic's
published average whole-day cost per developer. Effort level is therefore a first-order cost
control, not a tuning knob, and this is the strongest argument in the pricing data for *Match the
model to the job* extending to *match the effort to the job*.

### Cost per task: what is actually published

Ranked by how much weight the book can put on it.

**1. Anthropic's own enterprise aggregate** — **vendor-reported**, but first-party and specific:
"around $13 per developer per active day and $150-250 per developer per month, with costs remaining
below $30 per active day for 90% of users." [10]

**2. Gateway telemetry (Requesty, May 2026)** — **vendor-reported**, from "anonymized, aggregated
monthly metrics from the Requesty production gateway": [18]

- "average cost per active user (those with at least two active days per month) is **$92/month**";
  Claude Code users **$108/month**; "**P95 users spending $291/month**"
- Claude Code **$0.050/call** (April 2026); OpenCode $0.061/call
- "Claude Code users averaged **1,549 API calls per month** by April 2026"
- "platform-wide cache hit rates rising from **52% to 86%**"; Claude Code **92%**
- "effective cost of input tokens is roughly **7x lower than list price**"
- "Claude models power **92% of all coding agent spend**, up from 68% twelve months prior"
- "prompt context size YoY" increased **4x**

*Derived sanity check*: 1,549 calls × $0.050 = **$77.45/month**, against a reported $108/month
average for Claude Code users. The two figures are from the same post but do not reconcile
directly, so treat them as separate order-of-magnitude anchors rather than a consistent model.

**3. The arXiv study — the strongest independent evidence, and it is about variance, not level.**
"How Do AI Agents Spend Your Money? Analyzing and Predicting Token Consumption in Agentic Coding
Tasks," Bai, Huang, Wang, Sun, Mihalcea, Brynjolfsson, Pentland, and Pei; arXiv v2, 30 April 2026;
trajectories from **eight frontier LLMs on SWE-bench Verified**. Verbatim from the abstract: [21]

- "agentic tasks are uniquely expensive, consuming **1000x more tokens** than code reasoning and
  code chat, with **input tokens rather than output tokens driving the overall cost**"
- "token usage is highly variable and inherently stochastic: **runs on the same task can differ by
  up to 30x** in total tokens, and **higher token usage does not translate into higher accuracy**;
  instead, **accuracy often peaks at intermediate cost and saturates at higher costs**"
- "models vary substantially in token efficiency: on the same tasks, **Kimi-K2 and
  Claude-Sonnet-4.5, on average, consume over 1.5 million more tokens than GPT-5**"
- "task difficulty rated by human experts only **weakly aligns** with actual token costs"
- "frontier models **fail to accurately predict their own token usage** (with weak-to-moderate
  correlations, up to 0.39) and **systematically underestimate** real token costs"

That last point is a play in itself: asking the agent to budget its own task does not work.

**4. Modelled, not measured** — Vantage, 15 April 2026: a representative 50-turn agentic session at
**$6.00** on Claude Opus 4.6 and **$0.60** on Composer 2 Standard, scaling to $7,200–$72,000 a year
for a 25-person team at ~1,000 sessions a month. [19] These are the author's estimates from a token
model, not instrumented runs. Useful for shape, not for citation as measurement.

### Model tiering: the one controlled study, and it cuts against the cheap tier

**Tessl, 28 August 2026** — four models, **10 merged pull requests from a monorepo**, identical code
review harness, independent grading by a separate model: [20]

| | Baseline (gpt-5.6-terra) | Worst alternative |
|---|---|---|
| Turns per review | **42** | **156** |
| Input tokens per review | **0.6 million** | **5 million** |

- "One was almost three times cheaper per token and **2.8 times more expensive on the same pull
  request**." [20]
- Promised token-price savings across the alternatives: **46–84%**. Actual consumption: **2.3x to
  7.6x** the baseline. [20]
- Their formula, which is the most liftable sentence in the whole pass:
  **cost per verified outcome = (price per token) × (tokens consumed) × (1 / validity rate)**. [20]
- The authors acknowledge the sample size prevented measuring run-to-run variance — and given the
  arXiv finding of up to 30x run-to-run variation on the same task [21], a 10-PR sample is thin.
  Present the mechanism, hedge the magnitude.

This is the direct empirical statement of the false economy: **a model that is 3x cheaper per token
and takes 3.7x more turns (156 ÷ 42) is not cheaper.** It complements `token-filtering.md`'s
+13.8%-turns finding exactly — both are cases where an intervention optimises tokens-per-turn while
silently inflating turns, and cost is the product of the two.

**What the cheap tier is still good for.** Anthropic's own guidance, which is unsurprising but
first-party: "Choose Haiku for simple tasks, Sonnet for most production workloads, and Opus for the
most complex reasoning" [1]; and for agent teams, "Use Sonnet for teammates. It balances capability
and cost for coordination tasks" and "For simple subagent tasks, specify `model: haiku` in your
subagent configuration." [10] The pattern that is defensible on the evidence is **tier down the
fan-out, not the reasoning** — cheap models on bounded, well-specified, verifiable subtasks where a
wrong answer is caught cheaply, frontier models on the planning and the judgement.

**The routing numbers in circulation do not transfer.** The widely cited "75–85% cost cut" from
routing comes from RouteLLM (Ong et al., ICLR 2025), which "kept roughly 95% of GPT-4 quality while
sending only about 14-26% of calls to the strong model" — **chat routing, single-turn, not agentic
coding**. [23] The same piece's "30-40%" deployment savings is presented as a scenario, not a
controlled measurement. [23] Its one first-party measurement is about context, not routing: "the
same prompt on the same model with **curated context** used **42% fewer tokens**, ran **27%
faster**, and made **64% fewer tool calls**." [23] That is a better argument for scoping than for
routing, and it agrees with `token-filtering.md`'s conclusion that scoping beats filtering.

## Price table

> **SNAPSHOT — 19 SEPTEMBER 2026.** Every figure below was fetched from the vendor's live pricing
> page on that date and is USD per million tokens. **These numbers rot faster than anything else in
> this book.** Three of them were already flagged as scheduled to change: Gemini 3.x Flash pricing
> doubles on 1 January 2027, and Anthropic's Sonnet 5 introductory price was made permanent only
> after a scheduled increase was cancelled. Do not reprint this table in the book without a date
> stamp and a "check before you rely on this" line. See *Staleness assessment*.

### Anthropic — Claude API, first-party, global inference [1]

| Model | Input | 5m cache write | 1h cache write | Cache read | Output | Out:In |
|---|---|---|---|---|---|---|
| Claude Fable 5.1 | $10 | $12.50 | $20 | $0.25 | $50 | 5.0x |
| Claude Mythos 5.1 *(limited)* | $10 | $12.50 | $20 | $0.25 | $50 | 5.0x |
| Claude Fable 5 | $10 | $12.50 | $20 | $1 | $50 | 5.0x |
| **Claude Opus 5** | **$5** | $6.25 | $10 | $0.50 | **$25** | 5.0x |
| Claude Opus 4.8 / 4.7 / 4.6 / 4.5 | $5 | $6.25 | $10 | $0.50 | $25 | 5.0x |
| **Claude Sonnet 5** | **$2** | $2.50 | $4 | $0.20 | **$10** | 5.0x |
| Claude Sonnet 4.6 / 4.5 | $3 | $3.75 | $6 | $0.30 | $15 | 5.0x |
| **Claude Haiku 4.5** | **$1** | $1.25 | $2 | $0.10 | **$5** | 5.0x |

Batch: exactly 50% of the above on input and output. Long context: none — full 1M window at
standard rates on 4.6 and later. Data residency `inference_geo: "us"`: 1.1x on every category
(4.6+). Fast mode (Opus 5 / 4.8 only): $10 input, $50 output = 2x standard, no batch. [1]

### OpenAI — API standard tier [3]

| Model | Input | Cached input | Output | Out:In | Long-context input / output |
|---|---|---|---|---|---|
| **gpt-6-astra** | **$10.00** | $1.00 | **$50.00** | 5.0x | $20.00 / $75.00 |
| **gpt-5.6-sol** | **$4.00** | $0.40 | **$20.00** | 5.0x | $8.00 / $30.00 |
| **gpt-5.6-terra** | **$2.00** | $0.20 | **$12.00** | 6.0x | $4.00 / $18.00 |
| **gpt-5.6-luna** | **$0.20** | $0.02 | **$1.20** | 6.0x | $0.40 / $1.80 |
| gpt-5.5 | $5.00 | $0.50 | $30.00 | 6.0x | $10.00 / $45.00 |
| gpt-5.5-pro | $30.00 | — | $180.00 | 6.0x | — |
| gpt-5.4 | $2.50 | $0.25 | $15.00 | 6.0x | $5.00 / $22.50 |
| gpt-5.4-mini | $0.75 | $0.075 | $4.50 | 6.0x | — |
| gpt-5.4-nano | $0.20 | $0.02 | $1.25 | 6.25x | — |
| gpt-5.4-pro | $30.00 | — | $180.00 | 6.0x | $60.00 / $270.00 |
| gpt-5.2 | $1.75 | $0.175 | $14.00 | 8.0x | — |
| gpt-5.1 / gpt-5 | $1.25 | $0.125 | $10.00 | 8.0x | — |
| gpt-5-mini | $0.25 | $0.025 | $2.00 | 8.0x | — |
| gpt-5-nano | $0.05 | $0.005 | $0.40 | 8.0x | — |
| gpt-5-pro | $15.00 | — | $120.00 | 8.0x | — |

Long context triggers above **272K input tokens** and reprices the whole request at 2x input, 2x
cached input, 1.5x output. [4] Batch: 50%. Fast mode (formerly Priority processing): 2x standard.
[3] Out:In column *derived*.

### Google — Gemini API, paid tier [7]

| Model | Input | Output | Cache read | Cache storage/hr | Out:In |
|---|---|---|---|---|---|
| **Gemini 3.1 Pro Preview** | **$2.00** ≤200k / **$4.00** >200k | **$12.00** / **$18.00** | $0.20 / $0.40 | $4.50 | 6.0x |
| Gemini 2.5 Pro | $1.25 / $2.50 | $10.00 / $15.00 | $0.125 / $0.25 | $4.50 | 8.0x |
| **Gemini 3.8 Flash** † | **$0.75** | **$3.75** | $0.075 | $0.50 | 5.0x |
| Gemini 3.7 / 3.6 Flash † | $0.75 | $3.75 | $0.075 | $0.50 | 5.0x |
| Gemini 3.5 Flash | $1.50 | $9.00 | $0.15 | $1.00 | 6.0x |
| Gemini 2.5 Flash | $0.30 (text/image/video) | $2.50 | $0.03 | $1.00 | 8.33x |
| **Gemini 3.5 Flash-Lite** | **$0.30** | **$2.50** | not available | — | 8.33x |
| Gemini 3.1 Flash-Lite | $0.25 (text/image/video) | $1.50 | $0.025 | $1.00 | 6.0x |
| Gemini 2.5 Flash-Lite | $0.10 (text/image/video) | $0.40 | not available | — | 4.0x |

† "through 12/31/26"; then $1.50 input / $7.50 output / $0.15 cache read / $1.00 storage. [7]

Batch: 50%. Flex: same as batch. Priority: 1.8x standard (*derived*). Long context: 2x input /
1.5x output above 200k tokens, **Pro tiers only**. Storage is billed per 1M tokens per hour on
explicit caches. [7]

## What drives spend in an agentic loop

Ranked by how much of a real bill each one moves, with the mechanism.

**1. Re-sending the conversation on every turn — cost is Θ(n²) in turns.** Anthropic states the
mechanism in its own docs: "Claude Code sends your full conversation with every request, and each
time Claude uses tools it sends another request carrying that batch of tool results … so a one-line
question in a session that has been open all day still draws usage for the whole conversation."
[10] *Derived from the standard arithmetic*: an n-turn loop that adds t tokens per turn bills
∑(k=1..n) k·t = t·n(n+1)/2 input tokens, not n·t. For n=20 and t=1,000 that is **210,000 tokens,
not 20,000 — 10.5x the naive estimate**. The corollary is the play: *doubling the turn count
roughly quadruples the input bill.* This is why `/clear` between unrelated tasks is a cost control
and not hygiene.

**2. The input side is ~85% of the bill, and most of it is cache reads.** Input tokens outnumber
output by 20–25x in agentic sessions, with input at "~85% of the total." [19] The arXiv study
agrees from measurement: "input tokens rather than output tokens driving the overall cost." [21]
Anthropic's own `/usage` example resolves to **94.3% of tokens being cache reads** (*derived*, see
*Concrete example*). This inverts the intuition people bring from chat, where the expensive thing is
what the model writes.

**3. Cache misses — a 10x cliff on every token you have to re-send.** A miss costs 10x a hit on all
three vendors; on Anthropic, a miss *plus* the 5-minute rewrite costs **12.5x** a hit (*derived*:
1.25 ÷ 0.1). [1] The triggers are unglamorous and frequent: a break longer than the TTL [10];
"modifying tool definitions (names, descriptions, parameters) invalidates the entire cache" [2];
toggling web search, citations, speed, thinking, or effort [2]. Claude Code now instruments this
directly — the `Prompt cache (main)` line reports "the share of input tokens served from cache,
cache misses, and whether the cache is warm right now," counting a request as a miss when it
"re-processed more than 5% and at least 2,000 tokens of what it could have read from cache." [10]
**Reading that line is the cheapest diagnostic in this whole subject.**

**4. Subagent and teammate fan-out — a multiplier on everything above.** Anthropic's measured
figures: "agents typically use about **4× more tokens** than chat interactions" and "multi-agent
systems use about **15× more tokens** than chats." [22] For Claude Code specifically: "Agent teams
use approximately **7x more tokens** than standard sessions when teammates run in plan mode, because
each teammate maintains its own context window and runs as a separate Claude instance." [10] Each
teammate pays its own Θ(n²) history bill, and none of them share a cache. Anthropic's own
economic test: "For economic viability, multi-agent systems require tasks where the value of the
task is high enough to pay for the increased performance." [22] That sentence belongs in *Know when
not to use an agent*.

**5. Thinking tokens billed as output, at a 5x-to-8x multiple.** Default-on, "tens of thousands of
tokens per request" on Anthropic [10], "billed as output tokens" on OpenAI [6], and on GPT-5.6 the
default is to render earlier turns' reasoning into the next sample [6]. *Derived*: 30,000 thinking
tokens on Opus 5 = $0.75 per turn.

**6. Long-context threshold cliffs.** Crossing 272K input tokens (OpenAI) or 200k (Gemini Pro)
doubles the input price **on the whole request**, not the excess. [4][7] An agent that accretes
context monotonically crosses this silently.

**7. Fixed per-request overheads that ride on every turn.** Tool-use system prompt 286–804 tokens by
model; bash tool +244–325; text editor +700; computer-use toolset ~4,500; browser-use toolset
~6,600. [1] Individually trivial; multiplied by turns and by teammates, not trivial — and all of it
is exactly the content that tool-definition churn forces you to re-cache.

**8. Tool result payloads and file re-reads.** This is where `token-filtering.md` lives, and the
finding there is that attacking it with output filters is unreliable. [`token-filtering.md`]
Anthropic's own remedies are structural rather than compressive: delegate verbose operations to
subagents so "the verbose output stays in the subagent's context while only a summary returns";
install code-intelligence plugins so "a single 'go to definition' call replaces what might
otherwise be a grep followed by reading multiple candidate files"; prefer CLI tools to MCP servers,
which "are still more context-efficient … because they don't add any per-tool listing." [10]

**9. Idle and background burn.** Scheduled tasks fire "on its interval even while the session is
idle, sending your full context each time"; cross-session messages deliver "as a new turn when this
session sits idle, sending your full context each time"; goal check-ins start "a new turn that sends
your full context" up to three times per goal. And "`/compact` reads the conversation it summarizes,
so compacting a large context is itself a large request. When you want a fresh start instead of
continuity, `/clear` costs nothing." [10] Ordinary background summarisation is small — "typically
under $0.04 per session" [10] — but the idle-turn mechanisms above are full-context requests.

**10. Variance, which is not a driver but defeats every estimate.** "Runs on the same task can
differ by up to **30x** in total tokens." [21] Any cost-per-task figure without a distribution
attached is decoration.

## Contested claims

- **"Claude Code achieves a 92% cache hit rate" and "platform-wide cache hit rates rising from 52%
  to 86%."** [18] **Vendor-reported**, from an LLM gateway vendor whose product markets itself on
  cost optimisation. Directionally corroborated by Anthropic's own docs example (94.3% of tokens as
  cache reads, *derived*) and by the docs' own sample `/usage` line showing "91% of input tokens
  from cache" [10], so the order of magnitude is probably right. The precise number is not
  independent.
- **"Prompt caching delivers up to 90% cost reduction and up to 85% latency reduction."** This is
  the most-repeated caching claim in circulation and I could **not** find it on Anthropic's own
  pricing or caching pages today; the caching page says only that "Cache reads cost significantly
  less than uncached input tokens" and gives the 0.1x multiplier. [1][2] The 90% follows
  arithmetically from 0.1x *on the cached portion only* and is not a 90% saving on a bill. See *Do
  not cite*.
- **Cursor's effective cost.** Cursor publishes the $0.25/MTok Cursor Token Rate for Teams and
  Enterprise [15] but does not state the dollar value of included usage on individual plans; the
  page says only that "different models have different API costs, your model selection affects how
  quickly your included usage is consumed." [15] Any claim about what a Cursor Pro seat buys in
  tokens is inference, not fact.
- **GitHub's margin.** GitHub says credits are consumed "according to the published API rates for
  each model" and that it "has absorbed much of the escalating inference cost," but "provides no
  specific markup percentages over API rates." [11] Do not claim Copilot is at-cost or above-cost.
- **Tessl's magnitudes.** The mechanism (cheap tokens, more turns, higher total) is well
  demonstrated; the specific "2.8x" and "156 vs 42 turns" come from 10 pull requests with no
  run-to-run variance measurement, by the authors' own admission [20], against a background of up
  to 30x run-to-run variance [21]. Cite the mechanism and the formula; hedge the multiple.
- **Model-routing savings of 30–40% / 75–85%.** The first is a scenario, the second is RouteLLM on
  chat routing at ICLR 2025 [23]. Neither is evidence about agentic coding.
- **The Vantage 50-turn session costs ($6.00 Opus 4.6 / $0.60 Composer 2 Standard).** [19] Modelled
  from a token estimate, not instrumented. Present as illustration only, and prefer the worked
  example below, which is arithmetically verifiable against a vendor's own published figure.
- **Whether tiering down is net cheaper at all.** Anthropic recommends it [1][10]; Tessl measured a
  case where it was 2.8x worse [20]; the arXiv study found "higher token usage does not translate
  into higher accuracy" and that "accuracy often peaks at intermediate cost" [21], which cuts both
  ways. The honest book position is that the answer is task-shaped and must be measured on your own
  workload, exactly as `token-filtering.md` concludes for filtering.

## Contradictions and gaps

- **Requesty's own numbers do not reconcile.** 1,549 calls/month × $0.050/call = $77.45, against a
  stated $108/month average for Claude Code users (*derived*). [18] Possibly different cohorts or
  months; the post does not say. Use one or the other, never both in the same sentence.
- **Anthropic's $150–250/developer/month [10] versus Requesty's $108/month [18].** Roughly a 2x gap.
  Plausibly explained by "active day" definitions, enterprise versus self-serve mix, and model
  choice, but nothing published reconciles them. The book should give a range, not a number.
- **No independent, instrumented, published cost-per-task benchmark for agentic coding was found.**
  The closest are Tessl's 10 PRs [20] and the arXiv trajectory study [21], and the latter reports
  tokens rather than dollars. This is a real hole: the two independently run cost benchmarks that
  *do* exist are the ones in `token-filtering.md` (JetBrains on SkillsBench, Quesma on
  Terminal-Bench 2.1), and both were measuring a filtering tool, not model tiers.
- **Nothing found measures cache hit rate against outcome quality.** Every caching figure is a cost
  figure. Whether a warmer cache correlates with better or worse work is unmeasured.
- **Subscription allowances are deliberately unquantified.** No vendor publishes a token allowance
  per plan. OpenAI publishes "local message" ranges spanning 9x [17]; Anthropic publishes
  multiples of a Pro baseline that is itself not quantified [9]; Cursor publishes multiples of a Pro
  baseline that is not quantified [16]. This is not an oversight — it is the product.
- **Two vendors changed billing model within six months of this date** (Copilot on 1 June 2026,
  Codex on 2 April 2026). Treat "how teams pay" as a moving target in the prose, not a fact.

### Do not cite

- **Any SWE-bench per-instance dollar figure.** A search surfaced "$0.75 per instance" for Claude
  4.5 Opus, "$0.07" for MiniMax M2.5, "$0.22" with a context engine, and "$4.60 average" derived
  from a $2,300 CodeMonkeys run over 500 instances. **I could not open a primary leaderboard or
  paper carrying a cost column** — Epoch AI's SWE-bench Verified page contains **no cost figures at
  all**. These numbers came only from a search engine's synthesis of secondary blogs. Do not use
  them.
- **"Routing cheap implementers under expensive reviewers cut benchmark costs by up to 14x."** A
  search summary produced this; no primary source located. Discard.
- **tokencalculator's "~$2.50 Claude Code / ~$2.04 Codex" per coding task.** Self-described as an
  "Observed reference point" from "a cited controlled comparison," with **no model versions and no
  identified source**, and with session parameters (8 turns, 70% cache hit rate) that are stated
  assumptions rather than measurements. Not usable.
- **Claude Max 20x at $200/month.** claude.com/pricing rendered "From $100" for **both** Max 5x and
  Max 20x when fetched today [9]; the $200 figure appears only in secondary sources. Either verify
  in a browser before printing, or write "Max 5x at $100/month, with a higher Max tier above it."
- **Per-plan AI Credit allowances for Copilot beyond the four in the announcement blog.** The docs
  page "only notes that 'Individual plans … include GitHub AI Credits allowances that vary by
  plan'" without enumerating them [12]; use the blog's four figures [11] and nothing else.
- **Codex credit allowances per plan. STILL UNPUBLISHED — and now confirmed as a choice rather than
  a retrieval failure.** **Re-checked 19 September 2026 by the source-verification pass
  (`57772ad900e3`).** The help-centre article still returns HTTP 403, but it is no longer the only
  route: OpenAI's own documentation site serves the whole pricing page, and serves it as clean
  markdown if you append `.md` to the URL. [17a] Everything this brief says about Codex reproduces
  from it exactly — the plan prices, the five-hour local-message ranges for every model, and the
  credits per million tokens. **What is not there, on any page, is a number of included credits per
  plan.** The docs say only "After you reach your included limits, available credits let you
  continue working", and "Credit purchase prices and applicable discounts depend on your plan or
  agreement." [17a] The allowance is deliberately expressed as an unquantified threshold. **Do not
  print a Codex per-plan credit allowance. The honest sentence is that OpenAI does not publish
  one** — which is the sentence this brief already makes about Anthropic and Cursor, and is now
  three-for-three rather than two-for-three-and-a-403.
- **Anthropic's "up to 90% cost reduction / up to 85% latency reduction" for prompt caching.** Found
  only in secondary blogs today, not on Anthropic's own pricing or caching pages. [1][2] If the
  book wants a caching saving figure, derive it as in the worked example below.
- **`o1` and `gpt-4o-mini` rows.** A first pass at OpenAI's pricing page returned rows for these; a
  second, fuller pass of the same page did not. Likely a retrieval artefact. Do not print them.
- **Gemini 3.5 Flash "input complimentary" and the audio-input split prices.** A first fetch garbled
  the Gemini 3.5 Flash row; the confirming fetch gives $1.50 input / $9.00 output, which is what is
  tabled above. Audio-modality input prices across the Gemini range were inconsistently returned
  across fetches and are not tabled here.
- **Any claim that Copilot, Cursor, or Codex resell tokens at cost, above cost, or below cost.** No
  vendor publishes a margin.

## Staleness assessment

**This brief is the fastest-rotting material in the book.** Not "will need updating" — *rotting*.
Between the research date and publication, expect at minimum one new frontier model per vendor, one
mid-tier price cut, and one billing-model change. Two of the three subscription schemes described
here were introduced within the six months before this brief was written.

**Suggested global hedging strategy, in priority order:**

1. **Never print an absolute price in body prose.** Put every dollar figure in a single, clearly
   dated table or worked example, with a one-line "verified 19 September 2026; check the vendor's
   page before relying on it" immediately above it. One place to update, not forty.
2. **Write the ratio, cite the price.** "Frontier tokens cost roughly ten times small-tier tokens"
   survives; "$10 versus $1" does not. Where the argument needs a number, make it a *multiple*.
3. **Never name a current model in a sentence that carries an argument.** "Opus-class" and
   "Haiku-class" survive a release; "Opus 5" does not.
4. **State mechanisms as rules, prices as examples.** "A cache read costs about a tenth of a fresh
   input token" has held across three vendors and several generations. The specific $0.50 has not.
5. **Give the reader the check, not the answer.** Every economics play should end with how to
   measure the thing on their own bill this week — the `/usage` line, the Console usage page, the
   paired run from `token-filtering.md`. A book that teaches measurement does not go stale.

| Claim | Why it rots | Suggested hedge |
|---|---|---|
| Any absolute $/MTok figure | New models ship monthly; introductory prices expire; Gemini 3.x Flash doubles on 1 Jan 2027 [7] | Confine to the dated table; in prose use multiples only |
| Specific model names (Opus 5, gpt-6-astra, Gemini 3.8 Flash) | Renamed or superseded within months | Write "frontier tier", "mid tier", "small tier"; name models only inside the dated table |
| Tier spread ≈ 10x top to bottom | Vendors differ today (10x / 50x / 8x, *derived*) and spreads widen as small tiers get cheaper | "roughly an order of magnitude"; give the per-vendor spread only in the dated table |
| Output:input multiple of 5x | Vendor- and generation-specific (4.0x–8.33x today) | "output costs several times input — between four and eight times at the last check" |
| Cache read = 0.1x input | Most durable number here: identical on all three vendors, several generations. Anthropic already has a 0.025x exception on Fable 5.1 [1] | Safe to state as a rule of thumb with "at the time of writing, on all three major vendors" |
| Anthropic's 1.25x / 2x cache-write premium | Anthropic-specific; OpenAI and Google charge nothing to write | "some vendors charge a premium to write the cache, some do not — check" |
| Long context step = 2x input / 1.5x output | Shape held across two vendors today; Anthropic removed its step entirely on 4.6+ [1] | "two of the three major vendors currently charge a step change above a context threshold, and it reprices the whole request" |
| Thresholds: 272K (OpenAI), 200k (Google) | Will move with context windows | Name the *mechanism* (whole-request repricing at a cliff); put the thresholds in the table |
| Batch = 50% | Has held at exactly 50% on all three vendors for years | Reasonably safe; still say "currently" |
| All subscription prices and allowances | Copilot changed 1 June 2026, Codex 2 April 2026, Anthropic cancelled a scheduled Sonnet rise [1][11][17] | Describe the three *philosophies* (seat allowance + metered overflow; dollar-denominated credits; token pass-through with markup) and date any figure |
| Copilot premium-request multipliers | Already legacy — annual request-based plans only [13] | Present as a worked historical example of why a request-count proxy misprices, not as current pricing |
| "$13/developer/active day" [10] | Vendor aggregate, moves with model defaults and adoption | "first-party figures in late 2026 put it in the low tens of dollars per active developer-day" |
| "$92–$108/month per active user" [18] | Gateway telemetry, single vendor, single month | Give as a range alongside Anthropic's, note they disagree by ~2x |
| Claude tokenizer produces ~30% more tokens from 4.7 [1] | Will change again at the next tokenizer change | Excellent as a *permanent* warning that per-token prices are not comparable across generations |
| Cache TTL: 1h on subscription, 5m on credits/API [10] | Product detail, changes without notice | State as "the TTL you get can depend on how you are billed — check yours" |
| Agent teams ≈ 7x, multi-agent ≈ 15x [10][22] | Harness-specific and version-specific | "fan-out multiplies token use by roughly an order of magnitude" |
| Any cost-per-task dollar figure | Up to 30x run-to-run variance on the same task [21] | Always attach the variance finding; never give a point estimate without it |

## Concrete example we can lift

> ### Worked example: where the money actually goes in one Claude Code session
>
> *All prices verified on Anthropic's published pricing page on 19 September 2026 and will have
> changed by the time you read this. The token counts are Anthropic's own published `/usage` sample,
> not a measurement we took.*
>
> Anthropic's Claude Code documentation prints this sample session summary: [10]
>
> ```
> Total cost:            $0.55
> Usage by model:
>    claude-sonnet-4-6:  1.2k input, 5.3k output, 940.0k cache read, 50.0k cache write ($0.55)
> ```
>
> Claude Sonnet 4.6 on 19 September 2026 lists at $3 per million input tokens, $15 per million
> output, $3.75 per million 5-minute cache writes, and $0.30 per million cache reads. [1] Working
> the bill line by line:
>
> | Line | Tokens | Rate | Cost | Share of tokens | Share of cost |
> |---|---|---|---|---|---|
> | Fresh input | 1,200 | $3.00 / MTok | $0.0036 | 0.12% | **0.7%** |
> | Output (incl. thinking) | 5,300 | $15.00 / MTok | $0.0795 | 0.53% | **14.4%** |
> | Cache reads | 940,000 | $0.30 / MTok | $0.2820 | **94.3%** | **51.0%** |
> | Cache writes | 50,000 | $3.75 / MTok | $0.1875 | 5.02% | **33.9%** |
> | **Total** | **996,500** | | **$0.5526** | 100% | 100% |
>
> Which rounds to the $0.55 Anthropic prints. The arithmetic checks out against the vendor's own
> figure, which is why this example is worth more than a modelled estimate.
>
> **Three things fall out of that table, and all three are counter-intuitive.**
>
> **One: you did not pay for what the model wrote.** Output is 14.4% of the bill. Input in all its
> forms is 85.6%. Every instinct carried over from chatting with an LLM points at the wrong end of
> the invoice.
>
> **Two: 94.3% of the tokens were things the model had already seen.** Nearly a million tokens of
> cache reads against 1,200 tokens of genuinely new input. That is the conversation being re-sent,
> turn after turn, at a tenth of list price. The whole session is dominated by re-reading itself.
>
> **Three: caching is doing almost all the work.** Without it, those 991,200 input tokens would all
> bill at the full $3 per million:
>
> ```
> 991,200 × $3.00 / 1,000,000 = $2.9736   input
>   5,300 × $15.00 / 1,000,000 = $0.0795   output
>                                 -------
>                                 $3.0531   uncached total
> ```
>
> Against the actual $0.5526, prompt caching saved **$2.50 on this session — an 81.9% reduction**
> *(derived; both figures computed from the published token counts and the 19 September 2026 list
> prices)*. That is the single largest lever available, it was on by default, and it cost nothing to
> obtain.
>
> **And here is the trap.** The same structure that makes caching so effective makes it fragile.
> A cache read costs $0.30/MTok; a miss followed by a fresh 5-minute write costs $3.75/MTok — **12.5
> times more**. Modifying a tool definition invalidates the entire cache. So does letting the
> session sit idle past the TTL, which on an API key is five minutes by default. [1][2] Take a
> coffee break in the middle of this session and the next message reprocesses close to a million
> tokens at full price: 940,000 × $3.75 / 1,000,000 = **$3.53 for one message**, against the $0.55
> the entire session cost up to that point.
>
> That is the economics play in one number. The expensive thing in an agentic session is not the
> model you chose, or how much it wrote. It is how many times the conversation gets re-sent, and
> whether it is warm when it does.

## Sources

[1] Pricing — Claude Platform Docs (Anthropic) —
    https://platform.claude.com/docs/en/about-claude/pricing — accessed 19 September 2026
[2] Prompt caching — Claude Platform Docs (Anthropic) —
    https://platform.claude.com/docs/en/build-with-claude/prompt-caching
    — accessed 19 September 2026
[3] Pricing — OpenAI API docs — https://developers.openai.com/api/docs/pricing — accessed
    19 September 2026
[4] gpt-6-astra model page — OpenAI API docs —
    https://developers.openai.com/api/docs/models/gpt-6-astra — accessed 19 September 2026
[5] Prompt caching — OpenAI API docs —
    https://developers.openai.com/api/docs/guides/prompt-caching — accessed 19 September 2026
[6] Reasoning — OpenAI API docs — https://developers.openai.com/api/docs/guides/reasoning —
    accessed 19 September 2026
[7] Gemini Developer API pricing — Google — https://ai.google.dev/gemini-api/docs/pricing —
    accessed 19 September 2026
[8] Context caching — Gemini API docs — https://ai.google.dev/gemini-api/docs/caching — accessed
    19 September 2026
[9] Pricing — Claude (Anthropic) — https://claude.com/pricing — accessed 19 September 2026
[10] Manage costs effectively — Claude Code Docs (Anthropic) — https://code.claude.com/docs/en/costs
     — accessed 19 September 2026
[11] GitHub Copilot is moving to usage-based billing — The GitHub Blog, 27 April 2026 —
     https://github.blog/news-insights/company-news/github-copilot-is-moving-to-usage-based-billing/
     — accessed 19 September 2026
[12] Models and pricing for GitHub Copilot — GitHub Docs —
     https://docs.github.com/en/copilot/reference/copilot-billing/models-and-pricing — accessed
     19 September 2026
[13] Model multipliers for annual plans on request-based billing (legacy) — GitHub Docs —
     https://docs.github.com/en/copilot/reference/copilot-billing/
     request-based-billing-legacy/model-multipliers-for-annual-plans (path wrapped for width)
     — accessed 19 September 2026
[14] Requests in GitHub Copilot — GitHub Docs —
     https://docs.github.com/en/copilot/concepts/billing/copilot-requests — accessed
     19 September 2026
[15] Pricing — Cursor Docs — https://cursor.com/docs/account/pricing — accessed 19 September 2026
[16] Pricing — Cursor — https://cursor.com/pricing — accessed 19 September 2026
[17] Pricing — ChatGPT Learn (Codex) — https://learn.chatgpt.com/docs/pricing (redirected from
     https://developers.openai.com/codex/pricing) — accessed 19 September 2026
[17a] **PRIMARY, and the retrieval route that works** — the same page as `.md` —
     https://developers.openai.com/codex/pricing.md — **fetched 19 September 2026 by `57772ad900e3`**
     (45,854 bytes of markdown, HTTP 200 to plain `curl`). OpenAI states on the page that "Markdown
     versions of documentation pages are available by appending `.md` to the page URL", which is the
     general trick: **`openai.com` and `help.openai.com` 403 scripted fetches;
     `developers.openai.com` does not, and `.md` gives the content without the navigation chrome.** Re-verified from it:
     the GPT-6 Astra rate (250 credits / 1M input, 1,250 / 1M output), the GPT-5.6 Luna rate (5 and
     30), and every cell of the local-message allowance table this brief prints
[18] The Coding Agent Economy — Requesty, May 2026 — https://www.requesty.ai/coding-agent-economy —
     accessed 19 September 2026 — **vendor-reported** (gateway telemetry)
[19] The Hidden Cost Driver in Agentic Coding Sessions in 2026 — Vantage, 15 April 2026 —
     https://www.vantage.sh/blog/agentic-coding-costs — accessed 19 September 2026
[20] Cheaper Tokens, Bigger Bills: Token Price Isn't Agent Cost — Tessl, 28 August 2026 —
     https://tessl.io/blog/cheaper-tokens-bigger-bills-token-price-isnt-agent-cost — accessed
     19 September 2026
[21] How Do AI Agents Spend Your Money? Analyzing and Predicting Token Consumption in Agentic Coding
     Tasks — Bai, Huang, Wang, Sun, Mihalcea, Brynjolfsson, Pentland, Pei; arXiv:2604.22750v2,
     30 April 2026 — https://arxiv.org/abs/2604.22750 — accessed 19 September 2026
[22] How we built our multi-agent research system — Anthropic —
     https://www.anthropic.com/engineering/multi-agent-research-system — accessed 19 September 2026
     — **vendor-reported**
[23] Model Routing for Coding Agents: Real Savings? — Unblocked, 9 June 2026 —
     https://getunblocked.com/blog/model-routing-coding-agents/ — accessed 19 September 2026 —
     **vendor-reported**
[24] AI Coding Cost Analysis: Where Token Spend Really Goes in an Agent Loop — Augment Code —
     https://www.augmentcode.com/guides/ai-coding-cost-analysis-agent-token-spend — accessed
     19 September 2026 — **vendor-reported**
[25] SWE-bench Verified — Epoch AI — https://epoch.ai/benchmarks/swe-bench-verified — accessed
     19 September 2026 — checked for cost-per-instance figures; **contains none**
</content>
</invoke>
