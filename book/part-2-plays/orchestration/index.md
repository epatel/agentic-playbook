# Orchestration

The book's third move bites hardest in orchestration: whatever you build around the agent must be
re-tested, and raised or removed, as models move. If you are about to run several agents, or script
one agent's steps, that machinery is yours.

Something in this field rewards adding agents. One run that took nine minutes and worked is a good
afternoon. Five in parallel is a diagram, and a diagram can be shown to people. Oddly, the vendors
counsel restraint. Anthropic published the best multi-agent result anybody has, and noted there that
coding has fewer genuinely parallel parts than research. OpenAI's guidance is to maximise a single
agent's capabilities before splitting it. Cognition published *Don't Build Multi-Agents*. Its update
ten months later allowed exceptions only where writes stay single-threaded. The vendors are more
conservative than their users, and the measured comparisons more conservative still.

Every piece of orchestration is machinery built around a model, and each piece encodes an assumption
about something the model cannot do alone. Those assumptions expire. So the question is rarely
whether to orchestrate. It is whether you can delete the machinery cheaply when the assumption stops
holding, or whether the rest of the system has grown around it.

[*Decompose into subagents*](decompose-into-subagents.md): orchestration across context. When
handing work to a separate window pays, what a summary-only return costs, and when delegation is
ceremony rather than leverage.

[*Make the control flow deterministic*](make-the-control-flow-deterministic.md): orchestration
across steps. Which parts of a sequence belong in code and which belong to the model, and what you
buy when you adopt somebody else's runtime or canvas.

[*Work in parallel without collisions*](work-in-parallel-without-collisions.md): orchestration
across the working tree. Partitioning a repository between several agents, the merges that report
success and are not, and the coordination cost that eats the speedup.
