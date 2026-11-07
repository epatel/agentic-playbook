# Verification and trust

Anyone merging agent-written code meets the book's second move at its plainest: check the agent's
work outside the agent.

A 2026 study of a quarter of a million pull requests found a machine writing the code and a machine
reviewing it, a median of 1.2 minutes apart. The study reports no precision, no recall, and no merge
outcomes, because nobody has established whether any of it catches anything. It is the fastest
review process ever measured, and there is no evidence it is a review. The human numbers in the same
2026 corpora are little comfort. Humans alone review 8% of agent-authored pull requests, against 25%
of human-authored ones in the same repositories.

The suite has one idea: everything the agent produces about its own work is a claim, and the signals
worth acting on come from outside its turn. The green suite it wrote, the summary it composed, and
the second model it consulted all come from the same run. Trust has to be bought somewhere the run
could not reach.

[*Review code you did not write*](review-code-you-did-not-write.md): the diff. What to read first
when reading time is scarce, and why instincts tuned to a tired human author stop working on this
one.

[*Make the agent prove it*](make-the-agent-prove-it.md): the harness. Turning "it says it works"
into evidence: finish conditions with a check in them, gates the run cannot talk past, and signals
ranked by how hard each is to fake.

[*Hold the structure, not just the behaviour*](hold-the-structure-not-just-the-behaviour.md): the
codebase. A structural check on every change, because working code can stop being changeable.

[*Decide who signs off*](decide-who-signs-off.md): the team. Who answers for agent-authored code
that ships, what the published policies agree on and the argument against them, and what a team
must write down.
