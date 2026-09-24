# Context

Context is where the book's first move happens. The agent remembers nothing between sessions, so
what it needs has to be written down where it will read it. This suite is for anyone who writes an
agent file or hands an agent a task.

The model is the part of the stack you cannot change this afternoon. The context is the part you
control completely, yet it fills up the way a garage does, one decision at a time.

The suite has one idea: signal over noise. Not less context, but more of what the agent reads
changing what it does. The noise is rarely wrong. It is true, once useful, or nearby, which is what
makes it hard to throw out. Every line competes with every other line, including the twelve that
mattered.

Signal pays three ways. Cost and speed are the same arithmetic: whatever loads every session is
re-read every turn, and a turn spent learning what the context could have said is lost to the task.
Quality is the third, and it fails quietly: as context grows, the agent still covers the
requirements but stops satisfying them all at once.

[*Write the agent file that actually gets read*](write-the-agent-file-that-actually-gets-read.md):
signal in the layer that loads every session, and what belongs in it.

[*Split the agent file into cards*](split-the-agent-file-into-cards.md): signal in the shape of that
layer, and where what it threw out goes.

[*Starve the context*](starve-the-context.md): signal in a single run. No window gets smaller on its
own, and measuring whether a filter helped is harder than installing one.

[*Scope a task to fit the window*](scope-a-task-to-fit-the-window.md): signal in the task itself,
and how much to hand over at once.

None of the four needs a budget or anyone's approval. Mostly they need deleting, the harder skill.
