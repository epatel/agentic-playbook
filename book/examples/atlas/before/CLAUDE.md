# atlas

Atlas is the billing service. It owns subscriptions, invoices, payment attempts, dunning, and the
ledger that finance reconciles against every month. If money moves, it moved through here. Please
read this file before making changes; it is the only place most of this is written down.

Maintained by the billing team. Add to it when you learn something the hard way.

## What this service does

Atlas sits between the product APIs and the payment processor. Product services tell atlas that a
customer has started, changed, or cancelled a plan. Atlas turns that into a subscription record,
generates invoices on a schedule, attempts payment through Stripe, retries on failure according to
the dunning policy, and emits ledger entries that the finance export picks up nightly.

Atlas does not own customers, plans, or entitlements. Those live in `accounts` and `catalog`
respectively. We hold foreign keys and nothing else. If you find yourself wanting to store a
customer's email address here, stop and ask; we have been burned by that twice. Atlas is also not a
reporting database — finance reads the nightly export, not our tables.

## Repository layout

```
atlas/
  api/            FastAPI routers, request/response schemas, auth dependencies
  billing/        the domain: subscriptions, invoices, proration, dunning
  ledger/         double-entry ledger, journal entries, the nightly export
  providers/      Stripe client wrapper, webhook parsing, retry policy
  migrations/     Alembic revisions, one file per revision, never edited in place
  jobs/           Celery tasks and their schedules
  models/         SQLAlchemy models, one module per aggregate
  settings.py     pydantic-settings config, all env vars declared here
tests/
  unit/           no database, no network, fast
  integration/    real Postgres in docker, no network
  contract/       recorded Stripe fixtures, replayed
scripts/          operational one-offs; see the note about ownership below
docs/             architecture decision records, mostly out of date
```

Anything in `docs/` should be assumed wrong unless it was written this quarter; we keep it because
the ADRs explain why some of the odder decisions were made, not the current state.

## Getting set up locally

You need Python 3.11. Not 3.12 — one of our dependencies pins a C extension that does not build on
3.12 yet, and yes, we have an issue open about it.

```
make venv
source .venv/bin/activate
make install
make db-up
make migrate
make seed
```

`make db-up` starts Postgres 15 and Redis in docker-compose. If the Postgres container exits
immediately, it is almost always a stale volume from an older major version; `make db-nuke` and try
again. You will lose local data, which does not matter, because `make seed` regenerates it.

The app runs with `make dev` (uvicorn, reload, port 8080). The Celery worker is a separate process,
`make worker`, and is only needed if you are touching `jobs/`.

Environment variables are declared in `settings.py` and nowhere else. Do not read `os.environ`
directly. If a new variable is needed, add it to the settings model with a default that is safe in
development, and add it to the deployment template in the infra repo in the same change.

## Running the tests

```
make test          unit + integration
make test-unit     unit only, about four seconds
make test-contract Stripe contract tests against recorded fixtures
```

The integration tests need `make db-up` first. They run against a separate database, `atlas_test`,
which is created and dropped by the fixture, so they will not clobber your development data.

Tests use `pytest`. Fixtures live in `tests/conftest.py` and in per-package `conftest.py` files, but
prefer factory functions over fixtures for domain objects; `tests/factories.py` has them, and a test
that says `make_invoice(status="open")` reads better than one depending on four fixtures.

Do not mock the database. If a test needs a database it belongs in `tests/integration/`. Mocking the
SQLAlchemy session produces tests that pass while the query is wrong, which is the failure mode we
most want to avoid in this service.

Do mock Stripe. Always. There is a `stripe_stub` fixture. A test that reaches the network will be
reverted. Coverage is measured but not enforced; we ask about conspicuous gaps during review.

## Python style

We are not precious about style, but consistency helps review go faster. The following are expected:

- Use four spaces for indentation, never tabs.
- Keep lines under 100 characters.
- Use double quotes for strings unless the string itself contains a double quote.
- Sort imports: standard library, then third party, then first party, each group separated.
- Do not leave unused imports or unused local variables in committed code.
- Use f-strings rather than `%` formatting or `str.format`.
- Prefer `is None` / `is not None` over `== None`.
- Do not use mutable default arguments.
- Use `except SomeError:` rather than bare `except:`.
- Avoid `l`, `I`, and `O` as variable names.
- End every file with a single trailing newline.

## Type annotations

Annotate public functions. Private helpers can go unannotated if types are obvious from two lines
away. We run mypy in non-strict mode over `atlas/billing/` and `atlas/ledger/` only; the API layer
has too much framework magic for it to be worth the fight. Note that `Decimal` is not
interchangeable with `float` and mypy will not catch it, because both are `SupportsFloat`.

## Error handling

Every error that crosses a module boundary is one of ours. Define it in the owning package's
`errors.py`, inherit from `AtlasError`, give it a stable `code` string that the API layer maps to
an HTTP status.

```python
class InvoiceAlreadyPaid(AtlasError):
    code = "invoice_already_paid"
    http_status = 409
```

Do not raise `ValueError` or `RuntimeError` from domain code. They surface as 500s, page somebody,
and tell them nothing. Do not catch `AtlasError` broadly in the API layer either; the exception
handler in `atlas/api/errors.py` already does that, and a local catch will swallow the code.

Provider errors are different. Anything from Stripe gets wrapped at the boundary in
`atlas/providers/stripe/errors.py` into either `ProviderTransient` or `ProviderPermanent`, because
the retry policy branches on that distinction and nothing else. A new Stripe error code needs
a line in the mapping table; if you leave it out, it defaults to permanent, which means we do not
retry a charge we should have retried. And never swallow an exception to make a test pass; if a
test fails because of an exception, the exception is the finding.

## Logging

Structured logging, via `structlog`. `log = structlog.get_logger()` at module level, then
`log.info("invoice.paid", invoice_id=..., amount_cents=...)`.

Event names are dotted and past tense: `invoice.paid`, `payment.attempt.failed`,
`subscription.cancelled`. This is not decoration; the alerting rules match on event names, so
renaming one is a breaking change to the on-call setup.

Never log a card number, a full email address, a Stripe secret, or a raw webhook body. The redaction
processor catches the obvious shapes, but it is a safety net and not a policy.

Log levels: `info` for things that happened, `warning` for things that will need attention if they
keep happening, `error` for things that already need it. There is no `critical` here; do not start.

## Money and currency

Monetary amounts are integer minor units. Cents, not dollars. The column type is `BigInteger` and
the Python type is `int`. There are no `Decimal` columns in atlas and there will not be any.

Where a calculation needs division — proration, tax splits, percentage discounts — do it in
`Decimal`, then round once, at the end, with `quantize(Decimal(1), rounding=ROUND_HALF_UP)`, and
convert back to `int`. Never round in the middle of a chain. The helpers in `atlas/billing/money.py`
do this correctly; use them rather than importing `Decimal` yourself.

Currency is a three-letter ISO code carried alongside every amount. There is no implicit currency.
Two amounts in different currencies cannot be added and the `Money` helper raises if you try. We do
not do currency conversion in atlas; if a conversion is needed, it happened upstream and the
rate is recorded on the invoice line. Zero-decimal currencies exist (JPY, KRW) and
`minor_units_per_major` knows about them, so never write `amount / 100` anywhere, for any reason.

## The billing domain

A **subscription** has a plan, a customer, a status, and a billing anchor. Statuses are `trialing`,
`active`, `past_due`, `paused`, `cancelled`. The transitions are enumerated in
`atlas/billing/subscriptions/state.py` and that module is the source of truth, not this file.

An **invoice** is generated for a billing period, moves from `draft` to `open` when finalised, and
then to `paid`, `void`, or `uncollectible`. An `open` invoice can still be edited. An invoice
that is `paid` is immutable — if something is wrong with it, you issue a credit note, you do not
change the invoice. This has legal weight, not just architectural weight.

**Proration** happens on mid-period plan changes. The rule is that we credit the unused portion of
the old plan and charge the used portion of the new one, both calculated by day, with the day of the
change counted toward the new plan. Half-day arithmetic was tried and abandoned in 2024; the ADR is
in `docs/adr/0011-proration.md` and is one of the documents that is still accurate.

**Dunning** is the retry schedule for failed payments: day 1, day 3, day 7, day 14, then mark
`uncollectible` and emit `subscription.dunning.exhausted`. The schedule lives in settings so that
finance can change it without a deploy. Do not hard-code the intervals anywhere.

The **ledger** is double-entry and append-only. Every entry has a matching counter-entry and the sum
of a journal is always zero. There is a test that asserts this across the whole test database and it
has caught real bugs three times. If it fails, do not adjust the test.

Credit notes, refunds, and chargebacks each produce ledger entries with different account pairs; the
mapping is in `atlas/ledger/accounts.py` and finance owns it, which in practice means Priya signs
off on the pull request.

## Database and models

Postgres 15. SQLAlchemy 2.0 style — `select()` statements, not the legacy `Query` API. If you see
`session.query(...)` it is old code and may be modernised opportunistically.

One module per aggregate under `atlas/models/`. Relationships are declared with explicit
`back_populates`, never `backref`. Lazy loading is off by default; if you need a relationship,
say so at the query site with `selectinload`. This is deliberate and it is why we do not have N+1
problems in the invoice list endpoint any more.

Every table has `id` (UUID, generated in Python, not in the database), `created_at`, and
`updated_at`. Soft deletes are used only on `customers_mirror` and nowhere else; if you are adding a
`deleted_at` column, you are probably solving the wrong problem.

Money columns are `BigInteger`. Timestamps are `TIMESTAMP WITH TIME ZONE`, always UTC in the
database, converted at the edges. Enum columns are native Postgres enums, which is why adding a
status value is a migration and not a Python constant.

Transactions are managed by the request scope and by the task decorator. Do not call
`session.commit()` inside domain code; a domain function that commits cannot be composed.

## Migrations

Alembic. Revisions live in `atlas/migrations/versions/`, one file per revision, and the linear
history is enforced in CI — branch it and the build fails until you rebase.

Generate a revision with `make migration m="short description"`, which runs `alembic revision
--autogenerate`. That is a starting point, not an answer: read the generated file, because
autogenerate misses server defaults, index changes, and anything involving an enum.

Every migration must be reversible. Write the `downgrade()` even when it is a no-op, and if it truly
cannot be reversed — a destructive data change, say — raise there with a message explaining why,
because an empty `downgrade()` looks like a migration that reverses cleanly and is not one.

Never edit a migration that has landed on `main`, even if it is wrong. Someone has run it locally,
their database now disagrees with the file, and the next person to pull gets a confusing error.

Schema migrations and data migrations are separate revisions, always: a schema change that also
backfills is two files, and the backfill goes second. Schema changes run inside the release gate and
data migrations run after it, so mixing them holds the gate open.

Data migrations are written with the ORM models imported from a frozen snapshot in
`atlas/migrations/snapshots/`, not from `atlas/models/`, because the live models drift and a
migration that imports them will break the moment someone renames a column. The snapshot is
regenerated by `scripts/freeze_models.py` when a migration needs a model the current snapshot does
not have; check the generated file in, and never hand-edit it. A migration that imports from
`atlas/models/` passes review and CI and fails six months later, which is the only reason this
paragraph is as emphatic as it is.

Long-running backfills go in a Celery task, not in a migration, and the migration enqueues the task.
Anything expected to touch more than about fifty thousand rows counts as long-running.

Adding a `NOT NULL` column is three steps: add it nullable, backfill it, then add the constraint in
a later release. In one step it locks the table for the backfill, which on `invoices` is an outage.

Dropping a column is two releases as well: stop writing to it, deploy, then drop it. The app and
the schema are never the same age in production.

Before opening the pull request, run `make migrate`, `make migrate-down`, and `make migrate` again
against a seeded database. A third of the migration bugs we have shipped would have been caught.

Migrations are reviewed by someone who did not write them; the only place we insist on that.

## Stripe

All Stripe access goes through `atlas/providers/stripe/client.py`; never import the `stripe` package
anywhere else; the wrapper adds idempotency keys, timeouts, and the error mapping, and code that
bypasses it will work in development and fail interestingly in production.

Idempotency keys are derived, not random: `f"{invoice.id}:{attempt_number}"`. This is what makes a
retried payment attempt safe. If you generate a fresh key on retry you will double-charge somebody.

Webhooks arrive at `/webhooks/stripe`, are signature-verified, written to `provider_events`, and
processed asynchronously. The HTTP handler does no domain work; it stores and returns 200. Stripe
retries aggressively on non-2xx and a slow handler turns into a retry storm.

Webhook processing is idempotent by event id. Stripe delivers duplicates, routinely, and not only
after a failure. The dedupe check is a unique constraint on `provider_events.external_id` and the
handler catching `IntegrityError` is the intended path, not an error.

Events we do not handle are stored and ignored, not rejected. The set we act on is in
`atlas/providers/stripe/handlers.py`.

Contract tests replay recorded fixtures from `tests/contract/fixtures/`. Re-record with
`make record-fixtures`, which needs `STRIPE_TEST_KEY`, and check the diff: a re-record that changes
twenty files usually means the pinned API version moved, and bumping that is its own pull request.

## The HTTP API

FastAPI. Routers in `atlas/api/routers/`, one per resource. Request and response models are explicit
pydantic models in `atlas/api/schemas/`; never return an ORM object from a route.

Authentication is service-to-service, signed tokens verified in `atlas/api/auth.py`. There are no
end-user sessions in atlas. If a request needs to know which human triggered it, that comes through
as an actor claim in the token and is recorded on the audit trail, not used for authorisation.

Pagination is cursor-based, opaque cursor, `limit` capped at 100. Offset pagination was removed in
2024 after the invoice list started timing out; do not reintroduce it.

Every mutating endpoint takes an `Idempotency-Key` header and it is required, not optional. The
middleware in `atlas/api/idempotency.py` handles storage and replay.

List endpoints filter, they do not search; there is no full-text search in atlas. Errors are
returned as `{"error": {"code": ..., "message": ...}}`, where `code` is stable and clients match on
it and `message` is for humans and may change.

## Background jobs

Celery, Redis broker. Tasks in `atlas/jobs/`, schedules in `atlas/jobs/schedule.py`.

Every task is idempotent and every task is retryable. Assume any task may run twice, and may run
twice concurrently, because during a deploy it will.

Task names are explicit: `@app.task(name="atlas.invoices.finalise")`. Auto-generated names come from
the module path, so moving a file renames the task and orphans anything already queued.

The nightly export runs at 02:15 UTC and finance notices within the hour if it does not. If you are
changing `atlas/ledger/export.py`, say so in the pull request so on-call knows to watch it. Long
tasks report progress by updating a row, not by logging a line per invoice.

## Continuous integration

CI runs on the self-hosted runner pool. There are four runners; `atlas-ci-3` was decommissioned last
spring after the disk kept filling, so if a job is queued against it, that is the stale label in
`.github/workflows/test.yml` and it needs removing — we have been meaning to do that for a while.
Until then, if the build hangs in the queue for more than ten minutes, cancel it and re-run, and it
will usually pick up one of the other three.

The pipeline is lint, unit, integration, contract, migrations-linear-history. Integration and
contract run in parallel. A full run is about seven minutes on a warm runner and about fourteen on a
cold one, because the cold one rebuilds the docker layer with the Python dependencies.

The docker layer cache lives on the runner, not in a registry, which is why a run that lands on a
runner that has not seen this branch before is slower. There is a ticket to move it.

Lint is `ruff check` and `ruff format --check`. Both are configured in `pyproject.toml`. If the
formatter and your editor disagree, the formatter is right.

## Deploying

Deploys go out through `scripts/deploy.sh`, which builds the image, pushes it, runs the schema
migrations against the release database, waits for the health check, and then shifts traffic. Run it
from the repository root with the environment as the first argument:

```
./scripts/deploy.sh staging
./scripts/deploy.sh production
```

The production deploy asks for confirmation and requires you to be on `main` with a clean tree. It
will refuse if the migration history is not linear, which is the same check CI runs, and it will
refuse if there is an open incident flagged in the deploy channel.

If the health check fails, the script rolls back automatically and leaves the migrations applied —
which is why, since the rolled-back application still reads the newer schema, data migrations must
not use raw SQL — and it is also why the two-release rule for dropping columns exists.

Rollback by hand is `./scripts/deploy.sh production --to <sha>`. It does not reverse migrations and
should not be asked to.

Deploys are blocked between 16:00 Friday and 09:00 Monday, and during the first three days of the
month, when finance closes the previous month. Watch `#atlas-deploys` for the health check output,
and if you have changed `providers/`, watch the payment success rate dashboard for twenty minutes.

## Observability

Metrics are Prometheus, via `atlas/telemetry/metrics.py`. Counter and histogram names are prefixed
`atlas_`. New metrics need a label cardinality sanity check — no customer ids as labels, ever.

The dashboards that matter are payment success rate, invoice finalisation lag, dunning queue depth,
and export completion time; they are linked from the team page. Alerts route to the billing on-call
rotation, and one that has fired twice without action should be fixed or deleted.

## Security and data handling

Atlas holds no card data. Stripe holds it, we hold tokens. If a change would make atlas store a PAN,
a CVV, or a full card expiry, it is out of scope and needs a conversation with security first.

Customer PII in atlas is limited to a customer id, a country code, and a tax identifier. That is the
whole set. The mirror table is populated by an event consumer and is never written to by hand.

Secrets come from the environment, injected by the platform. There are no secrets in the repository
and no `.env` files checked in; `.env.example` lists names and never values. Audit entries are
written for every mutating operation, are append-only, and are retained for seven years.

## Code review

Pull requests are small. A pull request that changes more than about four hundred lines will get a
request to split it, not because the number is meaningful, but because review quality falls off a
cliff somewhere around there.

Describe the behaviour change in the description, not the diff. The diff is visible; the reason is
not. One approval is enough, except for migrations and anything in `ledger/`, which need two, one
from the billing team. Review comments are suggestions unless they say "blocking".

## Known rough edges

`atlas/billing/proration.py` has a function called `_adjust` that nobody fully understands. It is
correct — there is a property test over it — but rewriting it is a standing invitation.

The `provider_events` table is large and growing and there is no retention policy. There should be.
`atlas/api/routers/invoices.py` is the longest file in the repository and has three endpoints that
could reasonably be their own router; nobody has wanted to touch it because of the idempotency
interactions. The seed data does not include a chargeback, so that path is covered only by unit
tests. Timezone handling at the invoice period boundary is correct for UTC and has never been
tested for a customer whose billing anchor sits in a zone with a half-hour offset.

## Glossary

- **Anchor** — the day of the month a subscription bills on, fixed at creation.
- **Dunning** — the retry process after a failed payment.
- **Finalise** — the transition from `draft` to `open`; after it, the invoice has a number.
- **Journal** — a set of ledger entries that sum to zero and share a transaction id.
- **Minor units** — cents, or the equivalent smallest unit for the currency.
- **Proration** — the mid-period adjustment when a plan changes.
- **Provider** — Stripe, currently the only one; the abstraction exists because it was not always.
- **Uncollectible** — an invoice we have stopped trying to collect. Not the same as void.
