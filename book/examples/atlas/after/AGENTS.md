# atlas

Python billing service. Owns subscriptions, invoices, payment attempts, dunning, and the ledger.
Customers, plans, and entitlements live in `accounts` and `catalog`; we hold foreign keys only.

## Money

- Amounts are integer minor units (`BigInteger` in the schema, `int` in Python), never `Decimal`.
- Divide in `Decimal`, round once at the end, convert back — the helpers in
  `atlas/billing/money.py` do this. Never round mid-chain and never write `amount / 100`.
- Every amount carries an ISO currency code. Atlas does no currency conversion.

## Invariants

- A `paid` invoice is immutable. Corrections are credit notes, not edits.
- The ledger is double-entry and append-only; every journal sums to zero. If the journal test
  fails, the test is right.
- Dunning intervals come from settings and are never hard-coded.

## Errors

- Domain errors subclass `AtlasError` and carry a stable `code`. Never raise `ValueError` or
  `RuntimeError` out of `atlas/billing/` or `atlas/ledger/`.
- Stripe errors are wrapped at the boundary as `ProviderTransient` or `ProviderPermanent`. The
  retry policy branches on nothing else, and an unmapped code defaults to permanent.

## Conventions we keep re-correcting

- All Stripe access goes through `atlas/providers/stripe/client.py`. Idempotency keys are derived
  (`f"{invoice.id}:{attempt_number}"`), never random.
- Never return an ORM object from a route; use the schemas in `atlas/api/schemas/`.
- Log event names are dotted and past tense. Alerting matches on them, so a rename is breaking.
- Every Celery task is idempotent; assume it runs twice concurrently during a deploy.
- Read configuration through `settings.py`, never `os.environ` directly.
