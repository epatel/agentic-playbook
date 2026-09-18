# Permissions, sandboxing, and harness-level safety controls

**Question asked:** what safety controls a harness actually offers, which of them are enforcement
and which are suggestion, when each earns its keep, and the sharpest way each goes wrong.

**Researched:** 18 September 2026
**Confidence:** high on mechanics — Claude Code's documentation is unusually candid about the limits
of its own permission rules, and states them normatively. Medium on generalisability: no other
harness's permission model was examined, so claims should be framed as "one harness's answer," which
is also the honest framing for the book.

Feeds the **Harness** suite, chiefly *Choose your harness*, and sits next to [`mcp.md`](mcp.md) for
the *Wire in the outside world* play.

## Findings

### There are three distinct layers, and only two of them enforce anything

| Layer | Mechanism | Enforced by | Binds the model? |
|---|---|---|---|
| Instructions | `CLAUDE.md`, rules, skill bodies | Nothing | No — advisory |
| Permission rules | allow / ask / deny on tool calls | The client, before the call runs | Yes, for the invocation shape it matches |
| OS sandbox | Seatbelt (macOS), bubblewrap + socat (Linux/WSL2) | The kernel | Yes, for every process and child process |

The memory documentation says the first row out loud: CLAUDE.md content is "delivered as a user
message after the system prompt," and "to block an action regardless of what Claude decides, use a
PreToolUse hook instead." [1] The managed-settings table repeats it: "Settings rules are enforced by
the client regardless of what Claude decides to do. CLAUDE.md instructions shape Claude's behavior
but are not a hard enforcement layer." [1]

### Permission rules

Rules are `Tool(specifier)`, in `allow`, `ask`, or `deny` arrays, configurable at managed, user,
project, and local scopes. [2] Bash rules match **the whole command text**, with `*` standing for
any text:

| Rule | Matches | Does not match |
|---|---|---|
| `Bash(npm run build)` | `npm run build` | `npm run build --watch` |
| `Bash(npm run *)` | `npm run build`, `npm run test --watch`, `npm run` | `npm install` |
| `Bash(git * main)` | `git merge main`, `git push origin main` | `git log` |
| `Bash(ls *)` | `ls -la`, `ls` | `lsof` |
| `Bash(ls*)` | `ls -la`, `lsof` | — |

Behaviours worth knowing, all from the primary docs: [2]

- **Compound commands are split.** Recognised separators are `&&`, `||`, `;`, `|`, `|&`, `&`, and
  newlines; a rule must match each subcommand independently, so `Bash(safe-cmd *)` does not approve
  `safe-cmd && other-cmd`. Deny and ask rules fire if *any* subcommand matches, including inside a
  subshell, a command substitution, or a `for` body.
- **A fixed wrapper list is stripped before matching**: `timeout`, `time`, `nice`, `nohup`,
  `stdbuf`, the builtins `command` and `builtin`, zsh's `noglob`, and bare `xargs`. The list "is
  built in and is not configurable."
- **Environment-runner wrappers are not stripped**, and this is a trap: `npx`, `docker exec`,
  `devbox run`, `direnv exec`, `mise exec`. Because they execute their arguments, "a rule like
  `Bash(devbox run *)` matches whatever comes after `run`, including `devbox run rm -rf .`."
- **A built-in read-only set runs without prompting in every mode** and is not configurable: `ls`,
  `cat`, `echo`, `pwd`, `head`, `tail`, `grep`, `find`, `wc`, `which`, `diff`, `stat`, `du`, `cd`,
  and read-only forms of `git`.
- **Redirect targets are checked separately** against `Edit`/`Read` rules — `> file`, `>> file`, `2>
  file`, `< file`, and `tee` destinations including inside a pipeline.
- **Path rules only work on `Read` and `Edit`.** A path rule written for `Write`, `NotebookEdit`,
  `Glob`, or `MultiEdit` "is accepted but never consulted," with a startup warning.

### The sandbox

OS-level, so it holds regardless of what the command text looks like. [3]

- macOS uses the built-in **Seatbelt** framework with nothing to install; Linux and WSL2 need
  **`bubblewrap`** for filesystem isolation and **`socat`** to relay network traffic through the
  sandbox proxy, plus an optional seccomp filter that adds Unix-domain-socket blocking. Native
  Windows is unsupported.
- Two independent layers: **filesystem isolation** (which paths can be read and written) and
  **network isolation** (which domains can be reached). Either can be switched off without the
  other. By default sandboxed commands may write the working directory, the session temp directory,
  and any `--add-dir` additions.
- Two modes, same restrictions: **auto-allow** (sandboxed commands run without prompting) and
  **regular permissions** (everything still prompts). In auto-allow, explicit deny rules are still
  respected, `rm`/`rmdir` against critical paths still prompt, and content-scoped ask rules like
  `Bash(git push *)` still force a prompt.
- **Credential protection** is a first-class block: `sandbox.credentials.files` and `envVars` with
  `mode: "deny"` (blocked / unset) or `mode: "mask"` — the command sees a per-session sentinel and
  the proxy substitutes the real value on outbound requests to hosts listed in `injectHosts`,
  requiring `network.tlsTerminate` so the proxy can see request contents. Masking is honoured only
  from user, managed, or `--settings` scope, never from a repository's own settings file.
- **The escape hatch is real and on by default.** When a command cannot run sandboxed, Claude may
  retry it with `dangerouslyDisableSandbox`, which drops it back to the normal permission flow. Set
  `allowUnsandboxedCommands: false` for strict mode, surfaced in `/sandbox` as **Strict sandbox
  mode**.

### Settings-source hardening

A pattern worth naming in the prose, because it is the thing that makes a checked-out repository
safe to open: **the settings sources that can widen access are deliberately restricted**. [3]

- `sandbox.filesystem.disabled` cannot be set from `.claude/settings.json` or `settings.local.json`,
  "so a checked-out project can't switch filesystem isolation off."
- Credential `mask` entries, `network.tlsTerminate`, and `credentials.allowPlaintextInject` are
  ignored in project and local settings.
- `deny` entries merge across every scope: "A `deny` entry only ever narrows access, so any scope
  can add one, but no scope can remove one that another scope added."
- The `AGENTS.md` instruction-file setting is likewise ignored in project and local settings. [1]

## When each earns its keep

- **Permission rules** earn their keep as *ergonomics* — cutting the prompt volume for the commands
  you run constantly — and as a speed bump for the destructive ones. They are a good record of team
  intent and a poor security boundary.
- **The sandbox** earns its keep the moment an agent runs unattended, or on a repository you did not
  write, or with credentials on the machine. It is the only layer that holds against a command you
  did not anticipate the shape of.
- **Hooks** earn their keep when a rule needs to inspect something the pattern language cannot see —
  the full command text, an argument's semantics, the current branch.
- **Instructions** earn their keep for everything else, which is most things, provided nobody
  mistakes them for the first three.

## Sharpest real-world gotcha

**A deny rule is not a boundary around a program. It is a boundary around a spelling.** The
documentation states this plainly and then tabulates it, which makes it perfect for the book: [2]

| Rule | Stops | Doesn't stop |
|---|---|---|
| `Bash(curl *)` | `curl https://example.com` | `/usr/bin/curl https://example.com`, `sh -c 'curl https://example.com'` |
| `Bash(rm *)` | `rm -rf build/` | `/bin/rm -rf build/`, `bash -c 'rm -rf build/'` |
| `Bash(git push *)` | `git push origin main` | `git -C . push origin main`, `git -c push.default=current push origin main`, `git 'push' origin main` |

The docs' own conclusion: a Bash rule "covers the invocation Claude usually produces and isn't a
security boundary around the program." [2] The `git push` row is the one that will land with
readers, because `git 'push' origin main` is not an exotic evasion — it is the same command with
quotes.

There is a second, quieter gotcha on the sandbox: **by default, if the sandbox cannot start —
missing dependencies, unsupported platform — Claude Code warns and runs commands unsandboxed.** [3]
A team that installs sandboxing on macOS and assumes their Linux CI inherited it has a warning in a
log and no isolation. `sandbox.failIfUnavailable: true` makes it a hard failure, and the docs note
this is "intended for managed deployments that require sandboxing as a security gate."

## Concrete example we can lift

The play is *the rule you wrote is not the rule you got*, and the worked example is a three-step
demonstration the reader can run in five minutes.

**Step 1 — write the rule you think protects you.**

```json
{
  "permissions": {
    "deny": ["Bash(rm *)", "Bash(curl *)"]
  }
}
```

**Step 2 — observe what it does not stop.** Per the documented matching table, `/bin/rm -rf build/`
and `bash -c 'rm -rf build/'` are both outside it, and neither is an unusual thing for an agent to
write. [2]

**Step 3 — put the boundary where the kernel can hold it.**

```json
{
  "sandbox": {
    "enabled": true,
    "failIfUnavailable": true,
    "allowUnsandboxedCommands": false,
    "filesystem": {
      "denyRead": ["~/"],
      "allowRead": ["."]
    },
    "network": {
      "allowedDomains": ["github.com", "*.npmjs.org"]
    },
    "credentials": {
      "files": [
        { "path": "~/.aws/credentials", "mode": "deny" },
        { "path": "~/.ssh", "mode": "deny" }
      ],
      "envVars": [
        { "name": "GITHUB_TOKEN", "mode": "deny" }
      ]
    }
  }
}
```

Three caveats the play should carry, all documented: the `denyRead`/`allowRead` pair above only
resolves `.` to the project root when it lives in *project* settings [3]; `failIfUnavailable` and
`allowUnsandboxedCommands: false` are both non-default and both necessary for the configuration to
mean what it looks like it means [3]; and **"There is no built-in credential deny list, so only the
files and variables you list are restricted."** [3]

A neat second example for the same play, on read-deny precedence, because it is the rare case where
the intuitive answer is also the correct one: [3]

| Rules | Result |
|---|---|
| `"denyRead": ["~/"]` with `"allowRead": ["~/projects"]` | `~/projects` readable, rest of home blocked |
| `"allowRead": ["~/"]` with `"denyRead": ["~/.env"]` | `~/.env` blocked, rest of home readable — "a broad allow can't silently re-expose a secret" |

## Contradictions and gaps

- **Only one harness was examined.** Every specific in this brief is Claude Code's. Cursor, Codex,
  Copilot, Aider, and Amp all have permission and isolation stories that were not researched. The
  *Choose your harness* play should either scope its claims explicitly or commission a comparison
  pass, because "harnesses differ in what they enforce" is exactly the kind of claim the book needs
  and cannot currently support.
- **Everything here is version-pinned to Claude Code v2.1.x** and the docs are dense with "before
  v2.1.2xx, this behaved differently" notes. Any lifted configuration should name the version.
- **No incident data.** Nothing found quantifies how often a deny-rule bypass is actually exercised
  in practice, accidentally or otherwise. The bypasses are documented as facts about matching, not
  as observed events, and the prose should not imply the latter.
- **Sandbox performance and friction are unmeasured.** No source establishes how often the
  unsandboxed-retry escape hatch fires in ordinary work, which is the number that would tell a team
  whether strict mode is livable.

## Sources

[1] How Claude remembers your project, Claude Code docs — https://code.claude.com/docs/en/memory
    — accessed 18 September 2026
[2] Configure permissions, Claude Code docs — https://code.claude.com/docs/en/permissions
    — accessed 18 September 2026
[3] Configure the sandboxed Bash tool, Claude Code docs — https://code.claude.com/docs/en/sandboxing
    — accessed 18 September 2026
