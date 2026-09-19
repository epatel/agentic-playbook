# `session-cost` — the Economics suite's arithmetic

Backs the Worked example in
[*Understand what you are paying for*](../../part-2-plays/economics/understand-what-you-are-paying-for.md).

That example works a published session summary line by line and claims the arithmetic is
"checkable rather than modelled". `check.py` is the check. It takes the token counts from the sample
session and the per-million prices the play quotes and dates, recomputes every row of the table and
every figure in the paragraph after it, and compares each against what the book prints.

```
python3 book/examples/session-cost/check.py
```

Standard library only, no network, no commands. It exits non-zero and names the offender if any
figure in the play stops following from its inputs.

## What it does not check

That the prices are current. They are dated in the play — 19 September 2026 — and the play says in
print that they will have moved by the time you read it. Update `RATES` and the numbers change;
that is the point of the example, not a failure of it.

## One thing it caught

The cache-expiry figure. 940,000 tokens at $3.75 per million is $3.525 exactly, sitting on a
half-cent, so it rounds to $3.53 under one convention and $3.52 under the other. The play now
prints three places rather than picking a side and being a cent out under the other one.
