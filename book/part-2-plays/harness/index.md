# Harness

The *harness* is where the agent's work starts being checked from outside the agent. It is the loop
wrapped around the model: it reads the output, runs the tool calls, feeds the results back, and
decided beforehand which tools existed at all. This suite is for anyone who configures that loop or
adds to it.

Most arguments about agentic coding are about models: which one is better at Go, which one shipped
last week, which one somebody's colleague swears by. Teams change models the way they change desk
chairs. Then they run them inside a harness nobody has looked at since the afternoon it was
installed.

The suite has one idea: everything you add to a harness extends what the agent can do and what it
can do wrong, in the same purchase. A tool it can call is a tool it can call at the wrong moment. A
procedure you package is one it will follow while you are at lunch. The design question is not only
what the agent can now reach, but what still holds when that reach is used badly.

[*Choose your harness*](choose-your-harness.md): the layer you already run and mostly did not
choose. What a harness is made of, the three levels of owning one (configure it, choose another,
build your own), and why the lowest level that changes what you need is right.

[*Package repeatable expertise*](package-repeatable-expertise.md): adding competence. When a
procedure should stop living in your head or a pasted prompt and become an artefact loaded when its
situation arrives. How to tell a boundary that will fire from one that will not.

[*Wire in the outside world*](wire-in-the-outside-world.md): adding reach. Connecting an agent to
systems that are not the filesystem, and the trust boundary that opens on the way in.
