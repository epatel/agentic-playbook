# Verification and trust

In a 2026 study of a quarter of a million pull requests, a machine wrote the code and a machine
approved it, with a median of 1.2 minutes between the two events. The study reports no precision, no
recall, and no merge outcomes, because nobody has established whether any of it catches anything. It
is the fastest review process ever measured and there is no evidence it is a review. The human
numbers in the same 2026 corpora are not much more comforting: humans alone review 8% of
agent-authored pull requests, against 25% of human-authored ones in the same repositories.

The suite is one idea: everything the agent produces about its own work is a claim, and the signals
worth acting on come from outside its turn. The green suite it wrote, the summary it composed, and
the second model it consulted are all downstream of the same run. Trust has to be bought somewhere
the run could not reach.

Three plays, the same idea at three layers.

[*Review code you did not write*](review-code-you-did-not-write.md) — the diff. What to look at
first when reading time is the scarce thing, and why instincts calibrated on a tired human author
stop discriminating when the author is neither tired nor wrong in the usual places.

[*Make the agent prove it*](make-the-agent-prove-it.md) — the harness. Turning "it says it works"
into evidence: finish conditions with a check in them, gates the run cannot talk its way past, and a
ranking of verification signals by how hard each one is to fake.

[*Decide who signs off*](decide-who-signs-off.md) — the team. Who is answerable for agent-authored
code that ships, what every published policy agrees on, the argument against all of them, and what a
team has to write down for the answer to mean anything.
