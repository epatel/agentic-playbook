---
paths:
  - "atlas/migrations/**/*.py"
---

# Migrations

- Every migration is reversible; write the `reverse_sql` even when it is a no-op.
- Never edit a migration that exists on `main`. Add a new one.
- Data migrations use the frozen models in `atlas/migrations/snapshots/` and never raw SQL —
  no `op.execute("...")`, no `session.execute(text(...))`. The deploy promotes a replica, so two
  schema versions are live at once and a raw statement is not portable across both. (This line
  came back two days after the prune, having been deleted with the old deployment section.)
