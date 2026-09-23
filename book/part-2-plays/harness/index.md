# Harness

Most arguments about agentic coding are arguments about models: which one is better at Go, which one
shipped last week, which one somebody's colleague swears by. The thing doing the work is a loop
wrapped around the model — something that reads its output, runs the tool calls, feeds the results
back, and decided beforehand which tools existed at all. That loop is the *harness*. Teams change
models the way they change desk chairs, and then run them inside a harness nobody has looked at
since the afternoon it was installed.

The suite is one idea: everything you add to a harness extends what the agent can do and what it can
do wrong, in the same purchase. A tool it can call is a tool it can call at the wrong moment. A
procedure you package is a procedure it will follow while you are at lunch. The design question is
never only what the agent can now reach — it is what still holds when the reach is used badly.

Three plays, the same idea at three layers.

[*Choose your harness*](choose-your-harness.md) — the layer you are already running and mostly did
not choose. What a harness is made of, the three levels of owning one — configure it, choose
another, build your own — and why the lowest level that changes what you need is right.

[*Package repeatable expertise*](package-repeatable-expertise.md) — adding competence. When a
procedure should stop living in your head or in a pasted prompt and become an artefact loaded when
its situation arrives, and how to tell a boundary that will fire from one that will not.

[*Wire in the outside world*](wire-in-the-outside-world.md) — adding reach. Connecting an agent to
systems that are not the filesystem, and the trust boundary that opens on the way in.
