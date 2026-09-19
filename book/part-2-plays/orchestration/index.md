# Orchestration

Something in this field rewards adding agents. One run that took nine minutes and worked is a good
afternoon; five runs in parallel is a diagram, and a diagram can be shown to people. The odd part is
who is counselling restraint. Anthropic published the best multi-agent result anybody has and noted
in the same post that coding has fewer genuinely parallel parts than research does. OpenAI's
guidance is to maximise a single agent's capabilities before splitting it. Cognition published a
piece called *Don't Build Multi-Agents* and spent the next year narrowing the exceptions rather than
widening them. The vendors are more conservative than their users, and the measured comparisons are
more conservative than the vendors.

The suite is one idea: every piece of orchestration is machinery you have built around a model, and
each piece encodes an assumption about something the model cannot do on its own. Those assumptions
have expiry dates. So the useful question is rarely whether to orchestrate. It is whether you can
delete the machinery cheaply when the assumption stops holding, or whether the rest of the system
has grown around it in the meantime.

Three plays, the same idea on three axes.

[*Decompose into subagents*](decompose-into-subagents.md) — orchestration across context. When
handing work to a separate window pays, what a summary-only return costs you, and the shape of
delegation that is ceremony rather than leverage.

[*Make the control flow deterministic*](make-the-control-flow-deterministic.md) — orchestration
across steps. Which parts of a sequence belong in code, which belong to the model, and what you are
buying when you adopt somebody else's runtime or canvas.

[*Work in parallel without collisions*](work-in-parallel-without-collisions.md) — orchestration
across the working tree. Partitioning a repository between several agents, the merges that report
success and are not, and the coordination cost that eats the speedup.
