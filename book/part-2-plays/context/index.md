# Context

Everything else in this book is downstream of what the agent could see. The model is the part of the
stack you cannot change this afternoon; the context is the part you control completely, and almost
nobody treats it as a design surface — it fills up the way a garage does, one reasonable decision at
a time.

The suite is one idea: signal over noise. Not less context for its own sake, but a higher
proportion of what the agent reads changing what it does. The noise is rarely wrong — true, once
useful, nearby — which is what makes it hard to throw out. Every line competes for attention with
every other line, including the twelve that mattered.

Three things get claimed for this, and these plays support them unevenly. Quality is the strong
one, and it fails oddly: as context grows the agent still covers the requirements and stops
satisfying them at once. Cost is contested, speed weakest — the measurement here has turns going
up. The case is quality; the rest is why to measure.

Four plays, the same move at four layers.

[*Write the agent file that actually gets read*](write-the-agent-file-that-actually-gets-read.md) —
signal in the layer that loads every session, and what belongs in it.

[*Split the agent file into cards*](split-the-agent-file-into-cards.md) — signal in the shape of
that layer, and where what it threw out goes.

[*Starve the context*](starve-the-context.md) — signal in a single run, and why measuring
whether a filter helped is harder than installing one.

[*Scope a task to fit the window*](scope-a-task-to-fit-the-window.md) — signal in the task itself.
How much can be handed over at once, and how to hand state on.

None of the four needs a budget line, a procurement cycle, or anyone's approval. They mostly need
deleting things, the harder skill.
