# Accountability for agent-authored code

**Question asked:** Who signs off on code an agent wrote, and how do teams, projects, vendors, and
regulators actually handle that question? Feeds the play *Decide who signs off* (Verification &
Trust suite).

**Researched:** 19 September 2026

**Confidence:**

- **High** — open-source project policies and commit-trailer conventions. These are published,
  dated, and quotable, and several are in version control. The divergence between projects is the
  strongest, most durable finding in this brief.
- **High** — the DCO question. Every project that has written anything down lands in the same
  place: a machine cannot sign off, a human must.
- **Medium-high** — US copyright position. The primary documents exist and are unambiguous on
  the narrow point, but I could not extract text from the Copyright Office PDF and am relying on
  law-firm notes that quote it. See **Do not cite**.
- **Medium** — EU AI Act and liability. Timeline is well sourced; the "is developer tooling in
  scope" question is answered by inference from Annex III rather than by an official statement.
- **Low-medium** — vendor indemnities. The marketing is loud and the terms are thin, moving, and
  partly behind PDFs I could not parse. Treat every number here as needing a re-check.
- **Low** — safety-critical sector rules. There is, as far as I can establish, *no* published
  regulator position anywhere on who may sign off on AI-*authored* code in aviation, automotive,
  or medical devices. The published guidance is all about AI *inside* the product. That absence is
  itself the finding, but it is an absence, and absences are hard to source.
- **Low** — enterprise policy. Almost everything published is consultancy content marketing. Two
  real corporate artefacts found (Amazon internal docs via CNBC, PagerDuty engineering blog).

> **This brief is not legal advice, and neither is the book.** Every legal and regulatory item
> below should be presented in the chapter as *"here is what the document says, on this date"* —
> never as *"so you should…"*. Several of these documents are drafts, pre-publication versions, or
> under active amendment. The book should say so each time.

---

## Findings

### The DCO is the sharpest edge, and every project lands the same way

The Developer Certificate of Origin 1.1 is a certification a human makes, in the first person. Its
clause (a) has the contributor certify the contribution "created in whole or in part by me and I
have the right to submit it under the open source license indicated in the file", and clause (d)
acknowledges the contribution and sign-off are public and kept "indefinitely". [4]

That first-person structure is why the DCO has become the hinge of the whole AI-contribution
debate: `Signed-off-by:` is not a statement that the code is good, it is a statement about
*provenance and right to submit*. Projects have split on whether you can truthfully make that
statement about model output — but not one of them has concluded that the model can make it.

The Linux kernel's `Documentation/process/coding-assistants.rst` states it flatly: [1][2]

```
AI agents MUST NOT add Signed-off-by tags. Only humans can legally
certify the Developer Certificate of Origin (DCO). The human submitter
is responsible for:

* Reviewing all AI-generated code
* Ensuring compliance with licensing requirements
* Adding their own Signed-off-by tag to certify the DCO
* Taking full responsibility for the contribution
```

The file was committed by Sasha Levin on 23 December 2025 with Jonathan Corbet's approval, and
shipped in the mainline tree. [3] It grew out of Levin's July 2025 RFC to add AI-assistant
configuration to the tree, which was contested at the time. [3]

QEMU reached the *opposite* conclusion from the *same* premise. Its `code-provenance.html` says
current policy "is to DECLINE any contributions which are believed to include or derive from AI
generated content", and reasons from the DCO: because the copyright and licence status of
generator output is unsettled, a contributor cannot credibly certify the DCO over it. [5] Same
clause, same logic, opposite answer — the kernel says *a human can certify if they review it*,
QEMU says *nobody can currently certify it at all*.

### The kernel trailer: `Assisted-by:`, not `Co-Authored-By:`

The kernel's Attribution section, as rendered on kernel.org on 19 September 2026: [1][2]

```
Assisted-by: LLM [TOOL1] [TOOL2]
```

with `[TOOL1] [TOOL2]` being "optional specialized analysis tools used (e.g., coccinelle, sparse,
smatch, clang-tidy)", the instruction that "Basic development tools (git, gcc, make, editors)
should not be listed", and the example `Assisted-by: LLM coccinelle sparse`. [2]

**Contested — see below.** The December 2025 patch version of the same file specified
`Assisted-by: AGENT_NAME:MODEL_VERSION [TOOL1] [TOOL2]` with the example
`Assisted-by: Claude:claude-3-opus coccinelle sparse`. [3] Secondary write-ups as late as August
2026 still quote the `AGENT_NAME:MODEL_VERSION` form. [50] Verify against the live file before
printing either.

### `Co-authored-by:` was never meant for this, and that is the root of the fight

GitHub's own documentation defines `Co-authored-by: name <name@example.com>` and instructs you to
"use an email address associated with their account on GitHub.com", or the co-author's
GitHub-provided no-reply address. There is no mention of AI or Copilot anywhere in it. [16] The
trailer is a *human* attribution primitive with an identity mapping behind it.

Git itself imposes no registry. `git interpret-trailers` accepts any `key: value` pair; the
convention set (`Reported-by`, `Reviewed-by`, `Helped-by`, `Suggested-by`) is documented in the
kernel's SubmittingPatches, not standardised anywhere, and projects are explicitly told they may
invent their own. [52] So there is **no standard**, only convergence.

Kubernetes reads the semantics strictly and forbids the usage outright: its June 2026 policy post
prohibits "Listing AI as a co-author on commits". [15]

### The real attribution incident: VS Code, April–May 2026

The cleanest documented case of accountability metadata being contested. On 27 April 2026 a user
reported that VS Code silently appended `Co-authored-by: Copilot <copilot@github.com>` to commits
*after* the user had deleted Copilot's generated message and written their own: "the final Git
history still contained the Copilot co-author line". [17] The setting responsible was
`git.addAICoAuthor`, which shipped **on by default**; a VS Code team member later confirmed the
behaviour was changed to opt-in in version 1.119. [17] The Register covered it on 4 May 2026 as
Microsoft reverting the default after developers found the trailer appeared even with AI features
disabled. [18]

Useful for the play because the objection was not "AI does not deserve credit" — it was that the
tool wrote a claim about authorship into an audit record without the signer's consent.

Anthropic's Claude Code appends `Co-Authored-By: Claude <noreply@anthropic.com>` by default and
this is disablable; I could not confirm the exact setting key from primary docs (see **Do not
cite**). **vendor-reported / community-reported.** [53]

### Copyright: the US position is narrower than "AI output is uncopyrightable"

The Copyright Office published *Copyright and Artificial Intelligence, Part 2: Copyrightability*
on **29 January 2025**. [20] Its conclusions, as quoted in contemporaneous law-firm notes (I could
not extract text from the PDF — see **Do not cite**): copyright law "protects only [original]
works of human creation"; "selection of a single output is not itself a creative act" sufficient
for protection; but copyright can cover "the selection, coordination, and arrangement of the
human-authored and AI-generated material", and using AI assistively does not forfeit protection
for the human-authored expression. The Office **declined to recommend new legislation** or a sui
generis right. [21]

So the accurate framing for the book is: *prompting alone is not authorship; the human-authored
parts, the modifications, and the arrangement are still protectable; it is case-by-case.* Not "you
lose your copyright".

Part 3 (*Generative AI Training*) was released on 9 May 2025 as a **pre-publication version** and
as of 19 September 2026 the final version has still not been published; the copyright.gov/ai
listing shows no 2026 documents at all. [20] Its status is unusually murky — the Librarian of
Congress was dismissed the day before release and Register Shira Perlmutter the day after.

The human-authorship requirement is now settled at the top of the US system: on **2 March 2026**
the Supreme Court denied certiorari in *Thaler v. Perlmutter*, leaving the D.C. Circuit's holding
that the Copyright Act requires a human author intact. [22] Narrow case — Thaler listed the
machine as *sole* author and never claimed human contribution — so it does not reach the mixed
case that actually describes agent-assisted code.

**UK:** the government published its *Report on Copyright and Artificial Intelligence* on **18
March 2026**. On outputs, the headline is that protection for computer-generated works under s.9(3)
of the Copyright, Designs and Patents Act 1988 **should be removed**, with the government
continuing to monitor. [23][24] If enacted, the UK would move *towards* the US human-authorship
position rather than away from it.

### Liability and regulation: the constraint is mostly not where people think

**EU AI Act.** Ordinary coding assistants are almost certainly **not** high-risk. Annex III
enumerates biometrics, critical infrastructure, education, employment, essential services, law
enforcement, migration, and justice — software development and code generation appear nowhere.
[59] Two edges where it changes: using an AI tool to *evaluate or rank developers* is an
employment use case under Annex III, and agentic tooling that autonomously acts on regulated
products can reach Annex I. [59] **This is inference from the text, not an official statement.**

The timeline moved. The Digital Omnibus on AI was approved by Parliament on 16 June 2026, adopted
by Council on 29 June 2026, signed 8 July 2026, and entered into force **27 July 2026**. It defers
Annex III high-risk obligations from 2 August 2026 to **2 December 2027**, and Annex I product-
embedded ones to **2 August 2028**. Article 50 transparency was not deferred and bites from **2
August 2026**; the Article 50(2) machine-readable marking deadline is 2 December 2026. [26]

Article 50(4) is the one clause a documentation-writing agent can touch. Deployers of a system
generating or manipulating text "which is published with the purpose of informing the public on
matters of public interest shall disclose that the text has been artificially generated or
manipulated" — **unless** "the AI-generated content has undergone a process of human review or
editorial control and where a natural or legal person holds editorial responsibility for the
publication of the content". [25]

That exception is the single most quotable line in this brief for a play about sign-off: **a
named human taking editorial responsibility is what discharges the labelling duty.** The Apache
Software Foundation has already written it into its own guidance: "Under the EU AI Act (in force
since 2 August 2026), such text must be labeled as AI-generated unless a person reviewed it before
publication and takes responsibility for it." [13]

**AI Liability Directive: dead.** Listed in the withdrawals annex of the Commission's 2025 Work
Programme presented 11 February 2025, with formal withdrawal published in the Official Journal on
**6 October 2025**. The Commission reserved the right to table a different proposal. [27][28] So
the EU's harmonised civil-liability route for AI harm does not exist; national law applies.

**US state law.** California **AB 316** (Ch. 2025, adding Civil Code §1714.46, approved 13 October
2025, effective **1 January 2026**) prohibits a defendant who "developed, modified, or used"
an AI system from asserting a defence that the AI autonomously caused the harm. [29] It does not
limit other defences, including causation and foreseeability arguments. [29] Blunt but directly on
point for "the agent did it".

Colorado's AI Act was amended by SB 189, signed 14 May 2026, pushing the effective date from 30
June 2026 to **1 January 2027** and removing the deployer risk-management and impact-assessment
duties. [30] Texas TRAIGA (HB 149) effective 1 January 2026; California SB 53 effective 1 January
2026 but aimed at frontier model developers above 10^26 FLOPs, not at code. [30]

**Where the real regulatory constraint on sign-off lives.** Not in AI law. In the pre-existing
process standards:

- **ISO 26262-8 clause 11** already governs software tools used in safety-related development. A
  Tool Confidence Level is derived from tool impact and tool error detection, and where TCL
  demands it the tool must be qualified by one of four methods: increased confidence from use,
  evaluation of the development process, validation of the tool, or development to a safety
  standard. The clause explicitly covers compilers and code generators. [56] A generative
  assistant is, on the face of the text, a software tool in scope — and none of the four
  qualification methods obviously works for a stochastic model.
- **DO-330** provides the domain-independent tool-qualification process referenced from DO-178C
  and usable by ISO 26262, requiring tool operational requirements, a tool verification plan,
  anomaly reporting, and configuration management. [Gap — see below; I did not verify DO-330
  clause text to a primary source.]
- **Medical devices:** FDA's draft guidance *Artificial Intelligence-Enabled Device Software
  Functions: Lifecycle Management and Marketing Submission Recommendations* was published **7
  January 2025** (comments closed 7 April 2025) and points manufacturers at recognised consensus
  standards including IEC 62304. [57] It concerns AI *in* the device, not AI that *wrote* the
  device software.
- **Aviation:** EASA's AI Concept Paper Issue 2 covers Level 1 and Level 2 ML applications and
  introduces human-AI teaming; a proposed Issue 03 is out for comment under AI Roadmap 2.0. [58]
  Again: AI *in* the aircraft, not AI *writing the certified software*.

**The finding to carry into the play:** in regulated domains the constraint on who signs off is
*regulatory* and pre-dates AI entirely — a named, qualified person with design authority, an audit
trail, and tool qualification. In unregulated domains it is *cultural*. No regulator has yet
published a position on who may sign off on code that a model wrote.

**Finance:** SR 11-7 model risk management and EU DORA (Regulation (EU) 2022/2554, applicable from
17 January 2025) both impose change-control, documentation, and ownership duties that attach to
whoever the institution names — again, structurally, not because of AI. Secondary sourcing only;
flagged as weak.

### Vendor indemnities: real, conditional, and narrower than the press release

All of these are **vendor-reported** — they are primary for what the vendor promises, and they are
also written by the party that would be paying.

- **Microsoft / GitHub.** The Customer Copyright Commitment is "a provision in the Microsoft
  Product Terms that describes Microsoft's obligation to defend customers against certain
  third-party intellectual property claims relating to Output Content." [31] Coverage is
  conditional on implementing the Required Mitigations. Notably, **as of 3 April 2026 there are no
  additional required mitigations for GitHub Offerings**, and "Use of the Duplicate Detection
  filter feature is no longer required for CCC coverage." [31] For Azure OpenAI code-generation use
  cases the protected-material code model must still be on in annotate or filter mode, and if in
  annotate mode the customer "must comply with any cited license provided for Output Content that
  is the subject of the claim." [31] Customers "will be required to demonstrate compliance with all
  relevant requirements" when tendering a claim. [31]
- **GitHub terms.** The GitHub Copilot Product Specific Terms were **deprecated effective 5 March
  2026**; new subscriptions and renewals from that date are governed by the GitHub Generative AI
  Services Terms. [33] Those terms say "GitHub does not own Inputs or Outputs. You retain any
  ownership you already have in your Inputs", and — the load-bearing conditional — **"If your
  Agreement provides for the defense of third party claims, that provision will apply to your use
  of Generative AI Services, including to Outputs."** [32] Defence is inherited from the
  underlying agreement; it is not granted by the AI terms. And: "You are solely responsible for
  any application or agent you create using (or for use with) Generative AI Services, including
  complying with any legal, regulatory, or licensing requirements applicable to the resulting
  application or agent or its use." [32]
- **Google Cloud.** Two-part indemnity: training-data claims, and claims that "an unmodified
  Generated Output" from an indemnified service infringes third-party IP. [34] The word
  **unmodified** is the whole game for code — a developer who edits the suggestion may be outside
  it. Eligibility also requires using Google's filters as designed. [34] I could not extract the
  full exclusions list — see **Do not cite**.
- **OpenAI.** Copyright Shield covers ChatGPT Enterprise and API customers, not free or Plus tiers,
  and is conditioned on staying within the terms and applicable content policies; Beta Services are
  excluded. [35][36] Secondary sourcing for the exclusions.
- **AWS.** Standard IP indemnity for "Indemnified Generative AI Services" at Service Terms §50.10;
  Amazon Q Developer Pro reported as covered. I could not retrieve §50.10 — see **Do not cite**.
  [37]

The structural point for the book: **none of these indemnities transfers accountability.** They
are a promise to defend an IP claim under conditions. They say nothing about a defect, an outage,
a breach, or a regulator. The engineer who merged it still owns the failure mode that matters most
of the time.

### Supply chain: nothing tracks model provenance for code

- **CycloneDX v1.7** (released late October 2025) adds a root-level `Citations` element letting an
  SBOM author declare where BOM data came from — build system, generation tool, artifact
  repository, or manual input — to enable "verifiable chains of provenance". [38] It also carries
  an ML-BOM capability for describing models as components. [39]
- **SPDX 3.0** (16 April 2024) shipped AI and Dataset profiles; 3.0.1 current, 3.1 in release
  candidate.
- But these describe **the model as a component of a system**, not **the model as the origin of a
  line of code**. I found no standard that records "this function was produced by model X at
  version Y" in a way a build system emits and a verifier checks. The only mechanism in production
  for that is the commit trailer — an unstandardised, unverifiable, self-asserted string. That gap
  is the honest answer and is worth stating plainly in the play.
- OpenSSF and CNCF published *Securing Open Source in the Age of AI: A Practical Guide for
  Maintainers, Security Engineers, and Researchers* in May 2026, covering handling of AI-generated
  contributions and AI-generated vulnerability reports. [41]

### How teams actually assign it

- **Kubernetes** (26 June 2026, Kevin Hannon, Red Hat): "Contributors must disclose when AI tools
  have been used to assist with a pull request"; "the human contributor remains fully responsible
  for every change"; "Contributors cannot rely on AI to respond to review comments. If you cannot
  personally explain changes that AI helped generate, your PR will be closed." The project enabled
  **the CLA check for co-authors**, precisely because "AI agents are not able to solve these
  contributor license agreements" — turning the co-author trailer into a merge blocker. [15]
- **PagerDuty** (27 August 2026, Ralph Bird): responsibility stays with the human operator —
  "Ownership used to flow from authorship", and now "you will still Own It". Also, candidly: "At
  PagerDuty, we are not letting agents ship code yet, but we are working towards it." [43]
  **Company-reported.**
- **Amazon** — the closest thing to a contested-accountability incident. CNBC reported on 10 March
  2026 that Amazon convened an internal "deep dive" meeting after a string of outages including one
  tied to AI-assisted coding errors; internal documents described a "trend of incidents" linked to
  "Gen-AI assisted changes" and "novel GenAI usage for which best practices and safeguards are not
  yet fully established", and **those references were deleted from the meeting documents before the
  discussion**. Amazon's position was that only one incident involved AI tools directly and that the
  root cause was an engineer acting on "inaccurate advice that an AI agent inferred from an
  outdated internal wiki". [42] Both halves belong in the book: the internal documents attributed a
  trend to AI-assisted change, and the company attributed the specific failure to a human acting on
  bad context. That *is* the moral-crumple-zone argument playing out in public.
- **curl** — accountability for *reports* rather than code. The project shut its HackerOne bug
  bounty in early 2026 after AI-generated "slop" reports overwhelmed triage; it returned to
  HackerOne in March 2026. [44] Relevant because it shows the cost lands on the reviewer, not the
  submitter.
- **DORA 2025** (Google, **vendor-reported**): ~90% of respondents use AI at work and >80% report
  productivity gains, but ~30% report little or no trust in AI-generated code. [48] Use lightly —
  the *productivity-evidence* brief owns this ground.

### The organisational-psychology thread

- **Madeleine Clare Elish, "Moral Crumple Zones: Cautionary Tales in Human-Robot Interaction"**
  (WeRobot 2016; published in *Engaging Science, Technology, and Society*, 2019). The concept:
  responsibility for automated-system failure collapses onto the nearest human operator; where a
  car's crumple zone protects the human, the moral crumple zone protects the *system* at the
  human's expense. [45] This is the sharpest available critique of "the human who ran the agent
  owns the diff" and the book should carry it rather than dodge it.
- **Andreas Matthias, "The responsibility gap: Ascribing responsibility for the actions of
  learning automata"**, *Ethics and Information Technology* 6(3): 175–183, 2004. The originating
  paper: where the operator cannot predict machine behaviour, traditional responsibility ascription
  breaks, and society must either abandon the machines or accept a gap. [46]
- Santoni de Sio & Mecacci (2021) later split this into four gaps — culpability, moral
  accountability, public accountability, and active responsibility. Reported secondhand via a 2026
  *Digital Society* article; I did not read the 2021 paper. [55]

---

## What is standardised vs. one project's policy

Nothing here is standardised. There is no RFC, no ISO document, and no registry for commit
trailers; `git interpret-trailers` accepts any `key: value` pair [52], and the only thing
approaching a convention is that `Assisted-by:` appears in more published policies than anything
else. Every row below is one body's own rule.

| Project/body | Position | Status | Source |
|---|---|---|---|
| Linux kernel | AI assistance permitted. Agents **MUST NOT** add `Signed-off-by`; only humans certify the DCO. Attribution via `Assisted-by:` trailer. Human takes "full responsibility". | In tree; committed 23 Dec 2025, shipped mainline | [1][2][3] |
| QEMU | **Declines** any contribution "believed to include or derive from AI generated content", reasoning that the DCO cannot credibly be certified over generator output. Relaxation proposed May 2026 and again Sept 2026 (`AI-used-for:` trailer, size-capped bugfixes, humans must write commit messages and review replies) — **not merged as of 19 Sep 2026**; master docs still say DECLINE. | Ban in force; amendment under review | [5][6][7] |
| Gentoo | "It is expressly forbidden to contribute to Gentoo any content that has been created with the assistance of Natural Language Processing artificial intelligence tools." Explicitly revisitable. | Council vote 14 Apr 2024; unchanged as of Sept 2026 | [8] |
| NetBSD | LLM output "is presumed to be tainted code, and must not be committed without prior written approval by core." Case-by-case, not absolute. | In commit guidelines; undated on page | [9] |
| Fedora | Permitted with accountability and disclosure. "The contributor is always the author and is fully accountable for their contributions." Disclosure required "when the significant part of the contribution is taken from a tool without changes"; recommended mechanism `Assisted-by: <name of code assistant>`. AI may not be the sole arbiter of subjective judgements about people. | Council approved 22 Oct 2025 | [10][11][54] |
| Debian | "Responsible Use of Generative AI" — neither endorses nor prohibits. Disclosure **encouraged, not required**. Contributors must "understand, review, test, and, where appropriate, modify AI-assisted output"; "use of a generative AI tool does not diminish the contributor's responsibility." | GR adopted; vote 15–28 Aug 2026, Option 5 won | [12] |
| Apache Software Foundation | Permitted subject to three conditions tied to ICLA §4 ("legally entitled to grant the above license"). Recommends a `Generated-by: ` token in the commit message. Requires reasonable certainty about third-party material via tool-provided similarity info or scanning. | Guidance, last updated August 2026 | [13] |
| OpenInfra Foundation | Permitted with two-tier disclosure: `Generated-By:` for substantial generated artefacts, `Assisted-By:` for predictive assistance. Both **supplement** `Signed-Off-By:`. Reviewers apply heightened scrutiny; labels removed if the reviewer substantially reworks it. | Policy v0.11.2, updated 8 July 2025 | [14] |
| Kubernetes | Permitted with mandatory PR-description disclosure. **Prohibits listing AI as a commit co-author.** CLA check enabled for co-authors so agent co-authorship blocks merge. "If you cannot personally explain changes that AI helped generate, your PR will be closed." | Policy post 26 June 2026 | [15] |
| GitHub (the platform) | `Co-authored-by:` documented purely as a human mechanism tied to a GitHub account email. No AI provision at all. | Current docs | [16] |
| Git (the tool) | No trailer registry, no semantics enforced, projects told to invent their own. | Current docs | [52] |
| US Copyright Office | Human authorship required; prompting alone insufficient; human-authored expression, modifications, and selection/arrangement remain protectable; no new legislation recommended. | Part 2 report, 29 Jan 2025; Part 3 still pre-publication | [20][21] |
| US Supreme Court | Cert denied in *Thaler v. Perlmutter*, leaving the human-authorship requirement standing. | 2 March 2026 | [22] |
| UK Government | Recommends **removing** s.9(3) CDPA protection for computer-generated works. | Report published 18 March 2026 | [23][24] |
| EU (AI Act) | Coding assistants not enumerated in Annex III. Art. 50(4) labelling duty for public-interest text is discharged by "human review or editorial control" with a person holding "editorial responsibility". | Art. 50 applies from 2 Aug 2026; high-risk deferred to 2 Dec 2027 | [25][26] |
| EU (liability) | AI Liability Directive **withdrawn**; OJ notice 6 Oct 2025. | Dead | [27][28] |
| California | AB 316 / Civil Code §1714.46: no defence that the AI autonomously caused the harm. | Effective 1 Jan 2026 | [29] |
| CycloneDX / SPDX | Describe models as components and data provenance for the BOM itself. Neither records "model X wrote this function". | CycloneDX 1.7 Oct 2025; SPDX 3.0 Apr 2024 | [38][39] |

---

## Contested claims

**1. The kernel's `Assisted-by:` format.** Live kernel.org rendering shows `Assisted-by: LLM
[TOOL1] [TOOL2]` with example `Assisted-by: LLM coccinelle sparse` [1][2]. The December 2025 patch
posting and multiple 2026 write-ups show `Assisted-by: AGENT_NAME:MODEL_VERSION [TOOL1] [TOOL2]`
with example `Assisted-by: Claude:claude-3-opus coccinelle sparse` [3][50]. Either the file was
amended after merge, or the rendering I retrieved is degraded. **The book must not print a trailer
syntax without checking the live file.** Both halves should be noted if the play shows the trailer.

**2. Can you certify the DCO for model output?** Kernel and Fedora and Debian: yes, provided a
human reviews and takes responsibility. QEMU and (in effect) Gentoo and NetBSD: no, because the
licence status of the output is unresolved. Neither side has a court ruling. Carry both.

**3. Whether `Assisted-by:` is converging into a standard.** One survey article claims it appears
in five of seven major foundations' policies and calls it "ecosystem-wide consensus" [50]. Against
that: ASF uses `Generated-by:` [13], OpenInfra uses both with *different meanings* [14], QEMU's
proposal deliberately uses neither and invents `AI-used-for:` [6][7], and Kubernetes requires
disclosure in the PR description rather than a trailer [15]. "Converging" is defensible;
"standard" is not.

**4. Did AI-generated code cause the Amazon outages?** Internal documents (via CNBC) linked a
"trend of incidents" to "Gen-AI assisted changes"; Amazon says only one incident involved AI tools
and the cause was a human acting on bad AI-inferred advice from a stale wiki. [42] Both halves.

**5. Does the human-owns-the-diff norm actually distribute responsibility fairly, or does it just
create a moral crumple zone?** Every published policy says the human owns it [1][10][12][15][43].
Elish's argument is that this is exactly how responsibility gets misallocated onto the operator
closest to a system they could not fully control. [45] The play should not resolve this by
assertion.

**6. Whether AI-authored code weakens a company's copyright position.** The Copyright Office's
logic implies unmodified generated portions may be unprotectable [21]; how much that matters for a
codebase that is also protected by trade secret, contract, and the human-authored surrounding work
is genuinely unsettled, and the sources I found arguing it strongly were marketing. Present the
Office's words; do not extrapolate.

---

## Contradictions and gaps

- **QEMU's current state is genuinely ambiguous.** The rendered master docs (built 2026, version
  11.1.50) still say DECLINE [5], while an RFC v2 dated 1 September 2026 is under active review
  with maintainer pushback [7]. Anything the book says about QEMU must be dated to the day and
  should note the ban is under review.
- **Fedora's canonical policy page** (`docs.fedoraproject.org/en-US/council/policy/
  ai-assisted-contributions/`) is behind an Anubis anti-scraping challenge and I could not read it.
  All Fedora quotes here come from the Council's own proposal post [10], LWN [11], and The Register
  [54]. The final approved text may differ from the proposal.
- **No AI-specific provenance standard for code exists.** Searched CycloneDX 1.7, SPDX 3.0/3.1,
  SLSA, in-toto. Model-as-component, yes; model-as-author-of-this-hunk, no.
- **No regulator anywhere has published a position on who signs off on AI-authored code in a
  safety-critical domain.** FDA, EASA, and the functional-safety standards all address AI *in* the
  product. I searched specifically for it and found nothing. This is an absence, and absences can
  be disproved by one document I missed — hedge it as "I could not find" rather than "there is no".
- **Almost all "enterprise AI code policy" material is content marketing.** I found exactly two
  first-party artefacts: Amazon's internal documents as reported by CNBC [42] and PagerDuty's
  engineering blog [43]. The book should say the published corpus is thin rather than dress up
  consultancy listicles as practice.

### Do not cite

- **Direct quotations from the Copyright Office Part 2 report.** The PDF would not extract to text
  through WebFetch. Everything attributed to it here is via Jones Day's client alert [21], which
  quotes it in quotation marks. Before printing any sentence as the Office's words, open the PDF.
- **GitHub Copilot Product Specific Terms (March 2026 PDF) clause text.** Retrieved but not
  parseable. Do not quote its indemnity, exclusion, or ownership language.
- **AWS Service Terms §50.10.** The terms page truncated long before §50. The claims that Amazon Q
  Developer Pro is an Indemnified Generative AI Service, and the conditions attached, are from
  secondary sources only. Unverified.
- **Google Cloud's specific indemnity exclusions.** The Generative AI Indemnified Services page
  truncated. The "unmodified Generated Output" wording and the filter condition are from
  secondary reporting and an older archived Service Specific Terms page. Verify before quoting.
- **OpenAI Copyright Shield exclusions** (fine-tuned models, Beta Services, content-policy
  categories). Law-firm and consultancy secondary sources only; I did not read the operative
  clause in OpenAI's Service Terms.
- **The exact Claude Code setting name for disabling the co-author trailer.** Not found in
  Anthropic's settings documentation; the `includeCoAuthoredBy` name circulating in community posts
  is unverified against primary docs. Do not print a setting key.
- **DO-330 clause-level requirements.** I have only a secondary description of the tool
  operational requirements / verification plan / anomaly reporting / configuration management set.
  Do not quote DO-330 or DO-178C clause numbers.
- **"A Fortune 500 company found 40 lines of GPL code in a Copilot-generated payments module and
  paid for a six-figure rewrite."** Appears in consultancy blog content with no named party, no
  date, and no primary source. Almost certainly fabricated or unfalsifiable. Do not use.
- **Aggregated Amazon outage figures** (6.3 million lost orders, 1.6 million errors, "four Sev-1s
  in 90 days"). These come from AI-content aggregator sites recycling CNBC. Use CNBC's own framing
  [42] and do not repeat the numbers unless you can find them in the original reporting.
- **"I read the AI policies of 120 open source projects"** and similar Medium survey posts. Useful
  as leads only; every project claim must be checked against that project's own policy.
- **DORA 2025 figures** beyond the two cited — and even those belong to the *productivity-evidence*
  brief, which should own them.
- **Santoni de Sio & Mecacci's four-gap taxonomy.** Reported here secondhand from a 2026 *Digital
  Society* article [55]; I did not read the 2021 original.
- **SR 11-7 / DORA financial-services claims.** Secondary sourcing throughout. Structurally
  plausible, not verified to the supervisory letter or the Regulation.

---

## Staleness assessment

| Claim | Why it rots | Suggested hedge |
|---|---|---|
| QEMU declines AI-generated contributions | Relaxation patches posted May 2026 and Sept 2026; maintainers appear to be converging on `AI-used-for:`. Could land any release. | "As of September 2026 QEMU's published policy was to decline, with a disclosure-based relaxation under review." |
| Kernel trailer is `Assisted-by: …` | Merged Dec 2025, already possibly amended once; the kernel edits its process docs freely. | Show it as an example of the *shape* of a trailer, and tell the reader to check `Documentation/process/coding-assistants.rst`. |
| `Assisted-by:` is the emerging convention | Four competing spellings in the field right now (`Assisted-by`, `Generated-by`, `AI-used-for`, PR-description disclosure). One could win or none. | "Several projects have converged on trailers of this shape; none is standardised." |
| Vendor indemnity terms | GitHub already deprecated a whole terms document in March 2026; Microsoft dropped the Duplicate Detection requirement in April 2026. These change quarterly. | Name the document and version date in the sentence itself; describe the *structure* (conditional, IP-only, mitigation-gated), not the specifics. |
| EU AI Act dates | Already deferred once by the Digital Omnibus in July 2026; further amendment is plausible. | Always attach "under the Act as amended by the Digital Omnibus, in force 27 July 2026". |
| Copyright Office Part 3 is pre-publication | A final version is expected; institutional turmoil makes the timing unpredictable. | "still a pre-publication version as of September 2026". |
| UK s.9(3) removal | A *recommendation* in a March 2026 report, not law. Requires legislation. | "the government's March 2026 report recommended removing…" — never "the UK has removed". |
| Colorado / state AI law dates | Colorado already slipped twice; state AI bills are amended constantly. | Give the citation and the date the source was read. |
| No standard tracks model provenance for code | Active area; CycloneDX ships roughly annually and AIBOM work is busy. | "I could not find one as of September 2026" rather than "none exists". |
| No regulator has ruled on AI-authored code sign-off | The most likely thing on this list to change. | Frame as an open question the reader's compliance function should be asked, not as settled. |

---

## Concrete example we can lift

**Worked example — the same commit, under four projects' rules.**

A developer uses an agent to produce a twelve-line fix to a buffer-length check, reads it, writes
a reproducer, builds it, and runs the test suite. The diff is identical in all four cases. What
they are required to put in the commit message is not.

**Linux kernel** — permitted; attribute the assistance, sign off personally. The policy is explicit
that the agent must not sign: "AI agents MUST NOT add Signed-off-by tags. Only humans can legally
certify the Developer Certificate of Origin (DCO)." [1]

```
net: fix length check in frob_header()

Assisted-by: LLM
Signed-off-by: A. Developer <dev@example.org>
```

**QEMU (policy in force as of September 2026)** — do not send it. "Current QEMU project policy is
to DECLINE any contributions which are believed to include or derive from AI generated content."
[5] Under the relaxation proposed in May and September 2026 — **not merged at the time of
writing** — the same patch would be inside the allowed "small bugfix" lane and would carry a
disclosure trailer before the sign-off [6][7]:

```
AI-used-for: code
Signed-off-by: A. Developer <dev@example.org>
```

**Apache project** — permitted subject to ICLA §4; the recommended token is different: [13]

```
Generated-by: <tool>
Signed-off-by: A. Developer <dev@example.org>
```

**Kubernetes** — disclose in the pull-request description, **not** as a co-author. The project
prohibits "Listing AI as a co-author on commits" and has the CLA bot check co-authors, so an
agent co-author trailer blocks the merge. And the reviewer may ask you to explain the change:
"If you cannot personally explain changes that AI helped generate, your PR will be closed." [15]

To check what a repository actually expects before you send anything:

```
git log --format='%(trailers:only)' -n 200 | sort | uniq -c | sort -rn
```

And to see whether your own tooling is writing an authorship claim you did not intend — the VS
Code default that shipped on and was reverted to opt-in in 1.119 [17][18]:

```
git log -1 --format=%B
git config --get-regexp 'addAICoAuthor'
```

The point of the example for the play: the diff is the same, the review is the same, the human
who takes responsibility is the same — and four serious projects require four different strings
in the commit message, one of them requiring that you do not send it at all. There is no standard
to comply with. There is only the local rule, and a human name on the sign-off line.

---

## Sources

[1] AI Coding Assistants — The Linux Kernel documentation — https://docs.kernel.org/process/coding-assistants.html — accessed 19 September 2026
[2] AI Coding Assistants — kernel.org latest HTML docs — https://www.kernel.org/doc/html/latest/process/coding-assistants.html — accessed 19 September 2026
[3] [PATCH v2] docs: add AI Coding Assistants documentation (LKML, December 2025) — https://lkml.iu.edu/hypermail/linux/kernel/2512.2/04871.html — accessed 19 September 2026
[4] Developer Certificate of Origin 1.1 — https://developercertificate.org/ — accessed 19 September 2026
[5] Code provenance — QEMU documentation (master, v11.1.50) — https://www.qemu.org/docs/master/devel/code-provenance.html — accessed 19 September 2026
[6] [PATCH] docs/devel: relax policy on AI-generated contributions (P. Bonzini, 28 May 2026) — https://lists.nongnu.org/archive/html/qemu-devel/2026-05/msg07614.html — accessed 19 September 2026
[7] [RFC PATCH v2 0/4] docs/devel, AGENTS.md (qemu-devel, 1 September 2026) — https://ratatoskr.run/qemu-devel/2026/09/17492844/t — accessed 19 September 2026
[8] Project:Council/AI policy — Gentoo wiki (motion 14 April 2024; page last edited 11 September 2026) — https://wiki.gentoo.org/wiki/Project:Council/AI_policy — accessed 19 September 2026
[9] NetBSD Commit Guidelines — https://www.netbsd.org/developers/commit-guidelines.html — accessed 19 September 2026
[10] Council Policy Proposal: Policy on AI-Assisted Contributions — Fedora Community Blog, 25 September 2025 — https://communityblog.fedoraproject.org/council-policy-proposal-policy-on-ai-assisted-contributions/ — accessed 19 September 2026
[11] Fedora Council approves AI-assisted contributions policy — LWN, 22 October 2025 — https://lwn.net/Articles/1042947/ — accessed 19 September 2026
[12] General Resolution: LLM usage in Debian (vote 15–28 August 2026) — https://www.debian.org/vote/2026/vote_002 — accessed 19 September 2026
[13] ASF Generative Tooling Guidance (last updated August 2026) — https://www.apache.org/legal/generative-tooling.html — accessed 19 September 2026
[14] OpenInfra Foundation Policy for AI Generated Content, v0.11.2, 8 July 2025 — https://openinfra.org/legal/ai-policy/ — accessed 19 September 2026
[15] Open source maintainership in the age of AI — Kubernetes Contributors blog, Kevin Hannon, 26 June 2026 — https://www.kubernetes.dev/blog/2026/06/26/open-source-maintainership-in-the-age-of-ai/ — accessed 19 September 2026
[16] Creating a commit with multiple authors — GitHub Docs — https://docs.github.com/en/pull-requests/committing-changes-to-your-project/creating-and-editing-commits/creating-a-commit-with-multiple-authors — accessed 19 September 2026
[17] GitHub Copilot silently inserts itself as a co-author… — GitHub community discussion #194075, 27 April 2026 — https://github.com/orgs/community/discussions/194075 — accessed 19 September 2026
[18] Microsoft fixes VS Code after Copilot credited human code — The Register, 4 May 2026 — https://www.theregister.com/software/2026/05/04/microsoft-fixes-vs-code-after-copilot-credited-human-code/5223936 — accessed 19 September 2026
[19] Copyright and Artificial Intelligence, Part 2: Copyrightability (PDF, 29 January 2025) — https://www.copyright.gov/ai/Copyright-and-Artificial-Intelligence-Part-2-Copyrightability-Report.pdf — accessed 19 September 2026 (retrieved but not text-extractable)
[20] Copyright and Artificial Intelligence — U.S. Copyright Office landing page — https://www.copyright.gov/ai/ — accessed 19 September 2026
[21] Copyrightability of AI Outputs: U.S. Copyright Office Analyzes Human Authorship Requirement — Jones Day, February 2025 — https://www.jonesday.com/en/insights/2025/02/copyrightability-of-ai-outputs-us-copyright-office-analyzes-human-authorship-requirement — accessed 19 September 2026
[22] Supreme Court Declines to Hear Thaler v. Perlmutter — Finnegan, March 2026 — https://www.finnegan.com/en/insights/ip-updates/supreme-court-declines-to-hear-thaler-v-perlmutter-leaving-human-authorship-requirement-intact.html — accessed 19 September 2026
[23] Report on Copyright and Artificial Intelligence (UK Government, 18 March 2026) — https://assets.publishing.service.gov.uk/media/69ba692226909a14239612e4/CP2602959_-_Report_on_Copyright_and_Artificial_Intelligence_web.pdf — accessed 19 September 2026 (not fetched; cited via [24])
[24] Copyright & AI in the UK: The Debate Rolls On — Bird & Bird, 2026 — https://www.twobirds.com/en/insights/2026/uk/copyright-,-a-,-aiin-the-uk-the-debate-rolls-on — accessed 19 September 2026
[25] Article 50: Transparency Obligations for Providers and Deployers of Certain AI Systems — EU Artificial Intelligence Act — https://artificialintelligenceact.eu/article/50/ — accessed 19 September 2026
[26] EU AI Act Omnibus Agreement — Postponed High-Risk Deadlines and Other Key Changes — Gibson Dunn, 2026 — https://www.gibsondunn.com/eu-ai-act-omnibus-agreement-postponed-high-risk-deadlines-and-other-key-changes/ — accessed 19 September 2026
[27] Proposed EU AI liability rules withdrawn — Bird & Bird, 2025 — https://www.twobirds.com/en/insights/2025/proposed-eu-ai-liability-rules-withdrawn — accessed 19 September 2026
[28] AI liability directive — European Parliament Legislative Train Schedule — https://www.europarl.europa.eu/legislative-train/theme-a-europe-fit-for-the-digital-age/file-ai-liability-directive — accessed 19 September 2026
[29] AB-316 Artificial intelligence: defenses — California Legislative Information — https://leginfo.legislature.ca.gov/faces/billTextClient.xhtml?bill_id=202520260AB316 — accessed 19 September 2026
[30] Colorado AI Act Amended and Effective Date Delayed — Hunton, 2026 — https://www.hunton.com/privacy-and-cybersecurity-law-blog/colorado-ai-act-amended-and-effective-date-delayed — accessed 19 September 2026
[31] Customer Copyright Commitment Required Mitigations — Microsoft Learn (updated 13 July 2026) — https://learn.microsoft.com/en-us/azure/foundry/responsible-ai/openai/customer-copyright-commitment — accessed 19 September 2026 — **vendor-reported**
[32] GitHub Generative AI Services Terms (March 2026) — https://github.com/customer-terms/github-generative-ai-services-terms — accessed 19 September 2026 — **vendor-reported**
[33] GitHub Copilot Product Specific Terms (deprecated effective 5 March 2026) — https://github.com/customer-terms/github-copilot-product-specific-terms — accessed 19 September 2026 — **vendor-reported**
[34] Generative AI Indemnified Services — Google Cloud — https://cloud.google.com/terms/generative-ai-indemnified-services — accessed 19 September 2026 — **vendor-reported** (page truncated on retrieval)
[35] Service terms — OpenAI — https://openai.com/policies/service-terms/ — accessed 19 September 2026 — **vendor-reported** (not fetched directly)
[36] OpenAI's "Copyright Shield" Broadens User IP Indemnities for AI-created Content — Proskauer — https://www.proskauer.com/blog/openais-copyright-shield-broadens-user-ip-indemnities-for-ai-created-content — accessed 19 September 2026
[37] AWS Service Terms — https://aws.amazon.com/service-terms/ — accessed 19 September 2026 — **vendor-reported** (§50.10 not retrievable)
[38] CycloneDX v1.7 Delivers Advanced Cryptography, Intellectual Property, and Data Provenance Transparency — CycloneDX, October 2025 — https://cyclonedx.org/news/cyclonedx-v1.7-released/ — accessed 19 September 2026
[39] Machine Learning Bill of Materials (AI/ML-BOM) — CycloneDX — https://cyclonedx.org/capabilities/mlbom/ — accessed 19 September 2026
[41] Securing Open Source in the Age of AI: A Practical Guide — OpenSSF / CNCF, May 2026 — https://openssf.org/resources/securing-open-source-in-the-age-of-ai-a-practical-guide/ — accessed 19 September 2026
[42] Amazon convenes 'deep dive' internal meeting to address outages — CNBC, 10 March 2026 — https://www.cnbc.com/2026/03/10/amazon-plans-deep-dive-internal-meeting-address-ai-related-outages.html — accessed 19 September 2026
[43] AI Coded It, AI Shipped It, Who Owns It? — PagerDuty Engineering, Ralph Bird, 27 August 2026 — https://www.pagerduty.com/eng/ai-coded-it-ai-shipped-it-who-owns-it/ — accessed 19 September 2026 — **company-reported**
[44] Curl shutters bug bounty program to stop AI slop — The Register, 21 January 2026 — https://www.theregister.com/security/2026/01/21/curl-shutters-bug-bounty-program-to-stop-ai-slop/5063039 — accessed 19 September 2026
[45] Elish, M.C., "Moral Crumple Zones: Cautionary Tales in Human-Robot Interaction" — Engaging Science, Technology, and Society (2019); WeRobot 2016 — https://estsjournal.org/index.php/ests/article/view/260 — accessed 19 September 2026
[46] Matthias, A., "The responsibility gap: Ascribing responsibility for the actions of learning automata", Ethics and Information Technology 6(3): 175–183 (2004) — https://dl.acm.org/doi/10.1007/s10676-004-3422-1 — accessed 19 September 2026
[48] DORA — State of AI-assisted Software Development 2025 — https://dora.dev/dora-report-2025/ — accessed 19 September 2026 — **vendor-reported** (Google)
[49] melissawm/open-source-ai-contribution-policies — a collected list of project AI policies — https://github.com/melissawm/open-source-ai-contribution-policies — accessed 19 September 2026
[50] Assisted-by: How open source projects are drawing the line on AI contributions — All Things Open, James Fredley, 11 May 2026 — https://allthingsopen.org/articles/open-source-ai-contributions-assisted-by-git-trailer-standard — accessed 19 September 2026
[51] Artificial Intelligence Playbook for the UK Government (10 February 2025) — https://assets.publishing.service.gov.uk/media/67aca2f7e400ae62338324bd/AI_Playbook_for_the_UK_Government__12_02_.pdf — accessed 19 September 2026
[52] git-interpret-trailers Documentation — https://git-scm.com/docs/git-interpret-trailers — accessed 19 September 2026
[53] Claude Code settings — Anthropic — https://code.claude.com/docs/en/settings — accessed 19 September 2026 — **vendor-reported** (co-author setting key not located)
[54] Fedora agrees policy allowing AI-assisted contributions — The Register, 23 October 2025 — https://www.theregister.com/2025/10/23/fedora_agrees_policy_allowing_ai_assisted_code_contribs/ — accessed 19 September 2026
[55] The Responsibility Cascade: Moral Attribution and Governance Challenges in Agentic AI Systems — Digital Society (Springer), 2026 — https://link.springer.com/article/10.1007/s44206-026-00288-w — accessed 19 September 2026
[56] Tool Qualification (ISO 26262) — itemis AG glossary — https://www.itemis.com/en/glossary/tool-qualification/ — accessed 19 September 2026
[57] Artificial Intelligence-Enabled Device Software Functions: Lifecycle Management and Marketing Submission Recommendations; Draft Guidance — Federal Register, 7 January 2025 — https://www.federalregister.gov/documents/2025/01/07/2024-31543/artificial-intelligence-enabled-device-software-functions-lifecycle-management-and-marketing — accessed 19 September 2026
[58] EASA Artificial Intelligence Concept Paper Issue 2 — https://www.easa.europa.eu/en/document-library/general-publications/easa-artificial-intelligence-concept-paper-issue-2 — accessed 19 September 2026
[59] What Open Source Developers Need to Know about the EU AI Act — Linux Foundation Europe — https://linuxfoundation.eu/newsroom/ai-act-explainer — accessed 19 September 2026
