# Agentic Developer Playbook – Outline

## Introduction
- Why this Playbook?  
- The changing landscape of software development
- How to use this resource

## 1. Foundations of Agentic Tools in Software Development
- What are agentic tools?  
- Brief history: From source versioning to agent orchestration
- The emergence of AI-assisted development

## 2. The Four Areas of Modern Software Work
- Computer Science: What you still need to know
- Software Engineering: Collaboration in the Age of Agents
- Craftsmanship: Mastering modern tools
- Innovation: Creativity and problem-solving with agents

## 3. The Rise of Agentic Development
- How agentic tools shift the developer role
- Comparing past and present: Pre-Git, Pre-Scrum, Pre-Agentic Workflows
- Where agentic methods are winning (and where they still struggle)

## 4. Building Team Practices for Agentic Success
- Establishing new ways of working together
- Transparency and documentation in fast-moving contexts
- The importance of humble experimentation

## 5. Practical Playbook: Patterns, Practices & Examples
- Team working agreements: collecting and refining
- Examples:
  - “CLAUDE.md”: Agent usage documentation
  - “AGENTS.md”: Skill libraries and modular agent design
  - Token filtering with tools like “rtk”
  - Agent orchestration: LangChain, LangGraph, n8n workflow automations
- Case studies: workflow transformations

## 6. Next Waves: What’s Coming
- Refactoring for full agent development
- Optimizing for agent/AI-enhanced outcomes
- Enabling designers and non-coders as co-pilots

## 7. Guiding Principles for Ongoing Evolution
- Fostering a culture of experimentation
- Balancing speed and quality with continual learning
- Evaluating and integrating new agentic tools

## Appendices
- Glossary of key terms
- Further reading & resources
- Templates and checklists for teams

## Closing Reflections
- The human side of agentic software engineering
- Paths forward for developers and teams

---

## Outline Assessment – Verdict

**Verdict: Solid skeleton, but currently a taxonomy rather than a playbook. Ship it as the spine, then rebalance toward practice.**

**Strengths**
- The historical framing (pre-Git, pre-Scrum → pre-Agentic) is the strongest idea in the book and earns its place early.
- The Four Areas model gives the reader a durable mental map that survives tool churn.
- Chapters 4–6 carry a real thesis: the engineering layer is unsettled, and teams must build it themselves.

**Weaknesses**
- Chapter 5 is doing too much. It holds the entire practical payload — agreements, four tool examples, and case studies — while Chapters 1–3 are all framing. A book called *Playbook* should be roughly half plays.
- Tool-named sections (LangChain, n8n, rtk) will age fastest. They need to sit under durable problem headings, not product names.
- Missing entirely: context engineering, harnesses, and tool-calling — named in the source idea, absent from the outline. Also missing: evaluation/verification (how do you know the agent was right?), cost and token economics, security and trust boundaries, and failure modes.
- "Where agentic methods struggle" is one bullet. It deserves a chapter; credibility depends on it.
- No stated reader. A staff engineer and a curious designer need different books.

**Recommended revisions**
1. Split Chapter 5 into *Individual Practice* (context engineering, harnesses, prompt and repo hygiene) and *Team Practice* (agreements, review of agent output, shared skill libraries).
2. Add a chapter on **Verification & Trust**: review practices for agent-authored code, testing strategy, and the accountability question.
3. Reframe tool sections as problems: "Documenting agent context" (→ CLAUDE.md/AGENTS.md), "Controlling token cost" (→ rtk), "Composing multi-step work" (→ LangChain/LangGraph/n8n). Tools become examples, not headings.
4. Pull one concrete case study forward into the Introduction. Show the transformation before explaining it.
5. Put a "What this book assumes about you" box in the Introduction.
6. Add per-chapter takeaway boxes and a one-page team checklist per practice chapter — a playbook should be skimmable under deadline.

**Priority if only three changes are made:** split Chapter 5, add Verification & Trust, de-name the tool sections.

