# Glossary

Terms are defined where they are first used, and collected here. Several of them are contested,
several are one vendor's word for something the others also do under a different name, and where
that is the case this says so rather than presenting a house definition as a standard.

Named failure modes are a separate vocabulary and are indexed at the end of [*The failure modes
worth naming*](../part-3-where-it-struggles/the-failure-modes-worth-naming.md).

- **Agent.** A model running in a loop with tools, permitted to decide what to do next without being
  asked each time. There is no agreed definition and the word is applied to everything from an
  autocomplete extension to an unsupervised overnight process; this book means the loop-with-tools
  sense throughout. The distinction is load-bearing when reading evidence, because almost all
  published research on "AI coding productivity" measures autocomplete or chat rather than agents.

- **Agent file.** The context file an agent reads at the start of a session: `AGENTS.md`,
  `CLAUDE.md`, or their equivalents. It is context rather than configuration: it competes for the
  model's attention alongside the task and every file opened, and it does not constrain anything.
  See [*Write the agent file that actually gets
  read*](../part-2-plays/context/write-the-agent-file-that-actually-gets-read.md).

- **Cache read.** A token supplied from the provider's prompt cache rather than processed fresh,
  billed at roughly a tenth of the input rate. Since every turn re-sends the whole conversation,
  what the cache is worth and what invalidates it dominate the bill on long sessions. See
  [*Understand what you are paying
  for*](../part-2-plays/economics/understand-what-you-are-paying-for.md).

- **Cache write.** Putting a prefix of the conversation into the provider's prompt cache so later
  turns can read it cheaply. Billed at a premium over fresh input on some vendors, and paid again in
  full whenever the cache has gone cold. That is why an idle session's next message can cost many
  times the one before it.

- **Card.** A short, self-contained markdown file holding one subject's conventions, loaded when its
  situation arrives rather than in every session, indexed from a slim agent file that names its
  trigger. The defining rule is self-containment: loading one card never requires loading another. A
  convention rather than a standard: no tool enforces it, and the directory is called `cards/`
  because somebody chose that. See [*Split the agent file into
  cards*](../part-2-plays/context/split-the-agent-file-into-cards.md).

- **Context window.** The most text a model can consider at once, measured in tokens: agent file,
  conversation, file contents, and tool output together. Everything the agent knows in a given turn
  is inside it, and everything inside it was paid for. Filling it is easy; the plays in
  [*Context*](../part-2-plays/context/index.md) are about not doing so.

- **Exchange rate.** What a play asks you to give up in return for what it buys: a slower first
  pass, four task briefs instead of one, a file somebody has to maintain. Every play states its own
  in *The play*, as [*What this book assumes about
  you*](../part-1-argument/what-this-book-assumes-about-you.md) promises.

- **Fan-out.** Running several agents on parts of one job at the same time. Distinct from a larger
  compute budget, and easy to confuse with one: before concluding a fan-out helped, give a single
  agent the same tokens and compare. See [*Decompose into
  subagents*](../part-2-plays/orchestration/decompose-into-subagents.md).

- **Harness.** The program around the model, in four layers. The loop plans, edits, and decides it
  has finished. The tool surface is what it can call at all. The permission layer governs what runs
  without asking, and the isolation layer decides what the operating system will refuse regardless.
  The model is the part people have opinions about and the harness is the part that decides what
  happens. See [*Choose your harness*](../part-2-plays/harness/choose-your-harness.md).

- **Hook.** A piece of your own code the harness runs at a defined point, typically before a tool
  call. It can inspect the call and refuse it. The mechanism to reach for when a rule depends on
  something a pattern cannot express, such as the current branch or what an argument means.

- **MCP.** The Model Context Protocol: a vendor-neutral protocol by which a server exposes tools
  (things the agent can do), resources (things it can read), and prompts (templates it can invoke)
  to any client that speaks it. It moved to the Linux Foundation's Agentic AI Foundation in December
  2025. Connecting a server is an admission decision rather than a convenience: the tool
  descriptions it supplies are context you did not write. See [*Wire in the outside
  world*](../part-2-plays/harness/wire-in-the-outside-world.md).

- **Orchestration.** Machinery built around one or more models to control what happens in what
  order: subagents, scripted stages, graph frameworks, visual workflow canvases. Every piece of it
  encodes an assumption about something the model cannot do on its own, which makes "can this be
  deleted cheaply when the assumption expires" the most useful question to ask of any of it. See
  [*Orchestration*](../part-2-plays/orchestration/index.md).

- **Permission rule.** A client-enforced pattern deciding whether a given tool call runs, asks, or
  is refused. Enforced before the call, which makes it real, and matched on the spelling of a
  command rather than on its effect, which makes it narrower than it reads. Best treated as
  prompt-volume tuning and a record of intent rather than as a boundary.

- **Play.** This book's unit: a named, self-contained move under five fixed headings: Problem, The
  play, Worked example, Failure mode, Checklist. There is no required order and no play assumes you
  have read another.

- **Preparation and execution.** The two modes of working with an agent. *Preparation* makes the
  project legible without you in the room: the agent file, the cards, the conventions written down,
  the checks a change must pass. *Execution* hands a prepared project a task and reads what comes
  back. Most of Part II is preparation. See [*The four areas,
  re-weighted*](../part-1-argument/the-four-areas-reweighted.md).

- **Reasoning effort.** A dial exposed by several providers controlling how much the model thinks
  before answering, billed as output tokens. A first-order cost control, and one worth setting per
  class of work rather than leaving at its default everywhere.

- **Run.** One agent session against one task, from the opening task brief to the point where it
  stops. Composed of turns; the thing a checkpoint lets you discard.

- **Sandbox.** Operating-system isolation of the filesystem and network, enforced by the kernel
  against the agent's process and everything it spawns. The only layer in the stack that survives a
  bad decision rather than merely shaping a good one, and the only one worth calling a boundary.

- **Skill.** A folder holding a `SKILL.md` of metadata plus instructions, alongside any scripts and
  reference files it needs, loaded when its situation arrives rather than in every session.
  Discovery matches on the `name` and `description` fields alone, which makes the description a
  routing table rather than documentation. The two-field frontmatter is the portable part; extended
  frontmatter is one vendor's. See [*Package repeatable
  expertise*](../part-2-plays/harness/package-repeatable-expertise.md).

- **Subagent.** A second agent invoked by the first, with its own context window and its own tool
  set, which returns a summary rather than its working. The isolation is the point and the summary
  is the risk: it reads the same whether the work was thorough or partial.

- **Task brief.** The instructions for one run: what to do, where the boundary is, what counts as
  done, and what not to touch. Written per task and discarded with it, which is the difference from
  the agent file, loaded by every session. See [*Scope a task to fit the
  window*](../part-2-plays/context/scope-a-task-to-fit-the-window.md).

- **Token.** The unit a model reads, writes, and is billed in: roughly a short word. Models of
  different generations tokenise differently, so per-token prices do not compare across generations.
  Both the currency and the capacity constraint.

- **Tool call.** The mechanism by which a model acts: it emits a structured request to run
  something, such as reading a file, executing a command, or querying a server. The harness runs it,
  and the result comes back into the context window as text. Everything an agent does that is not
  producing prose is a tool call, and every result it receives is something it must then be trusted
  to have read correctly.

- **Turn.** One exchange within a run: your message, the model's reply, and any tool calls between.
  Cost grows with the square of the turn count on a long session, because each turn re-sends
  everything before it.

- **Verification tax.** DORA's term, adopted here, for effort that relocates from writing code to
  checking it when agents are introduced. The consistent finding across the available evidence is
  that throughput rises while review coverage falls. The cost lands as displaced review capacity,
  not as defects. See [*Where the time actually
  goes*](../part-3-where-it-struggles/where-the-time-actually-goes.md).

- **Worktree.** A second checkout of the same repository sharing one `.git` directory, which lets
  several agents work in parallel without overwriting each other's files. Ergonomics rather than
  isolation: the branches still merge into one tree, and the collisions worth fearing live in the
  union. See [*Work in parallel without
  collisions*](../part-2-plays/orchestration/work-in-parallel-without-collisions.md).
