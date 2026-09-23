# Wire in the outside world

## Problem

The agent can read every line of your repository and cannot see the thing that is actually wrong:
which deploy the latency started climbing after, what the ticket says, what the dashboard has been
doing since Tuesday. So you paste. A stack trace out of the log viewer, a ticket description with
its formatting flattened, your own summary of a graph you are looking at on the second monitor.
Something gets written, so the session counts as a success, and you have spent it working as an
expensive clipboard. Connecting the agent to those systems directly takes one command, which is
exactly the problem.

## The play

Give the agent a connection instead of a paste, and treat adding one as an admission decision rather
than a convenience. The multi-vendor way to do it is the Model Context Protocol: a server exposes
tools (things the agent can do), resources (things it can read), and prompts (templates you can
invoke), and any client speaking the protocol can consume them.

1. **Connect on a boundary, not on availability.** A server earns its machinery when a capability
   crosses one — more than one agent, more than one harness, more than one person. For one developer
   wiring one CLI into one agent, a bash command and a line in the agent file is less machinery
   ([`mcp.md`](../../../notes/research/mcp.md)).
2. **Read the exact command before you approve it, and run it where you run everything else.** A
   local server is a binary executing with your privileges. The specification requires a client
   offering one-click installation to show the command untruncated, for the reason that the command
   is the payload; the isolation you put under the agent's other commands belongs under this one too
   ([*Choose your harness*](choose-your-harness.md)).
3. **Scope the credential down to the job.** Read-only where reading is the job, one project rather
   than the organisation, one repository rather than the account. Broad grants make a leaked token
   maximally useful to whoever now has it, and the protocol's own security guidance names scope
   inflation as an attack class rather than an untidiness.
4. **Treat every tool description as text the server's author writes into your context on every
   turn.** Descriptions are not data the model inspects; they are instructions it acts on. That
   makes your threat model the union of everything connected rather than each server separately — a
   description in one server can steer the agent's use of another, which was demonstrated publicly
   against a pair of connected servers in April 2025.
5. **Pin what you installed, and look at updates rather than taking them.** An audit is a statement
   about a version, not about a package. The known case is `postmark-mcp`, which wore a mail
   vendor's name without being theirs: fifteen releases that did what they said, then one in
   September 2025 that silently copied every sent email to the publisher's address.
6. **Keep the list short enough to recite, and prune it.** Every server is a party you trust, and
   costs context wherever tool definitions load up front. A server nobody has used since the spring
   is still connected, still describing its tools, and still shipping updates.

What you are actually doing when you install a server is granting two things, and teams reliably
notice only the first. The agent gets a capability. The author gets a writable channel into the
agent's context window, for as long as the connection exists, every time its tools are loaded. The
exchange rate follows from that: reach costs context and a standing trust relationship per server,
and what you give up is the reflex to install something because it exists and might be useful later.

## Worked example

`kestrel`, a Go search-indexing service, three days into a latency regression on the product index
that nobody could pin to a change. The sessions had all gone the same way: someone reading a
dashboard aloud into the chat, the agent reasoning competently about a summary of a summary.

The move was one project-scoped server, read-only at both ends, with the token supplied from the
environment rather than committed:

```json
{
  "mcpServers": {
    "metrics": {
      "command": "/usr/local/bin/metrics-mcp",
      "args": ["--read-only"],
      "env": { "METRICS_TOKEN": "${KESTREL_METRICS_RO}" }
    }
  }
}
```

`--read-only` was belt, the read-scoped token was braces, and the reason for both is that the same
server also exposes tools for silencing alerts and editing dashboards. With the connection in place
the agent correlated the p99 climb with a mapping change three deploys earlier — something it could
not have reached through any amount of pasting, because nobody had thought to paste that deploy.

Two things did not go the tidy way. A second server, for the ticket tracker, was proposed in the
same review and dropped: the only token the tracker could issue was organisation-wide and could
write, and the value on offer was saving a paste. And the metrics server was removed from
`.mcp.json` when the investigation closed, because its forty tool descriptions, loaded up front by
the harness, were arriving on every turn of every session, including the several hundred that had
nothing to do with latency. It goes back in when the next regression does.

## Failure mode

**The Instruction You Did Not Write.** The agent does something nobody asked for, and nothing in
your repository explains it: it reaches for a second server's tool in a way that makes no sense, or
attaches a file to a request, or reports a step as done that it did not take. You search the agent
file, the skills, and the transcript for the instruction, and it is in none of them, because it
arrived in a tool description — text controlled by a server's author, reaching the model as
something to act on rather than something to inspect. The publicly demonstrated version of this in
2025 was the cross-server case, where a hidden instruction in one server's tool description
redirected the agent's use of a legitimate messaging server connected to the same session.

The tell is behaviour you cannot trace to anything you wrote, in a session with a server connected.
The second tell is quieter and worth checking on a calm afternoon: you cannot name, from memory,
every server your agent is connected to and who publishes each one.

## Checklist

- [ ] Every connected server crosses a boundary, rather than merely existing and looking useful
- [ ] You have read the exact command or URL for each one, untruncated, before approving it
- [ ] Local servers run inside the same isolation as the agent's other commands
- [ ] Each credential is scoped to the narrowest thing that does the job, read-only where possible
- [ ] Installed versions are pinned, and updates are reviewed rather than taken
- [ ] The connected list is short enough to recite from memory, and was pruned this quarter
- [ ] Unexplained agent behaviour gets checked against tool descriptions, not only your own files

**See also:** [*Choose your harness*](choose-your-harness.md) ·
[*Decide who signs off*](../verification-and-trust/decide-who-signs-off.md)
