#!/usr/bin/env python3
"""Re-derive every figure in the session-cost table in *Understand what you are paying for*.

The play works one published session summary line by line and says the arithmetic is
"checkable rather than modelled". This is the check. It takes the token counts from the
sample session and the per-million prices quoted in the play, recomputes each row, and
compares against the figures printed in the book.

    python3 book/examples/session-cost/check.py

Exits non-zero if any figure in the book no longer follows from the inputs. It does not
check that the prices are current — they are dated in the play, and they will move.
"""

from __future__ import annotations

import sys

# The sample session Anthropic prints in its Claude Code cost documentation.
TOKENS = {
    "Fresh input": 1_200,
    "Output, thinking included": 5_300,
    "Cache reads": 940_000,
    "Cache writes": 50_000,
}

# Per million tokens, as quoted in the play and dated there: 19 September 2026.
RATES = {
    "Fresh input": 3.00,
    "Output, thinking included": 15.00,
    "Cache reads": 0.30,
    "Cache writes": 3.75,
}

# What the play prints. Every one of these is recomputed below.
EXPECTED = {
    "vendor_total": 0.55,
    "row_cost": {
        "Fresh input": 0.0036,
        "Output, thinking included": 0.0795,
        "Cache reads": 0.2820,
        "Cache writes": 0.1875,
    },
    "token_share": {
        "Fresh input": 0.1,
        "Output, thinking included": 0.5,
        "Cache reads": 94.3,
        "Cache writes": 5.0,
    },
    "cost_share": {
        "Fresh input": 0.7,
        "Output, thinking included": 14.4,
        "Cache reads": 51.0,
        "Cache writes": 33.9,
    },
    "total_tokens": 996_500,
    "total_cost": 0.5526,
    "input_share_of_bill": 85.6,
    "uncached_input_tokens": 991_200,
    "uncached_total": 3.0531,
    "caching_saving": 81.9,
    # One message after the cache expires writes the conversation back. Its size is
    # bounded by what the session ever wrote to the cache, not by the cache reads, which
    # are summed over every turn.
    "cold_message": 0.1875,
    "warm_message": 0.015,
    "cold_over_warm": 12.5,
    "cold_share_of_session": 33.9,
}

INPUT_ROWS = ("Fresh input", "Cache reads", "Cache writes")


def main() -> int:
    problems: list[str] = []

    def check(label: str, got: float, want: float, places: int) -> None:
        if round(got, places) != round(want, places):
            problems.append(f"{label}: book says {want}, arithmetic says {round(got, places)}")

    cost = {row: TOKENS[row] * RATES[row] / 1_000_000 for row in TOKENS}
    total_cost = sum(cost.values())
    total_tokens = sum(TOKENS.values())

    print(f"{'Line':<28}{'Tokens':>10}{'Rate':>8}{'Cost':>10}{'Tok %':>8}{'Cost %':>8}")
    for row in TOKENS:
        tok_share = TOKENS[row] / total_tokens * 100
        cost_share = cost[row] / total_cost * 100
        print(
            f"{row:<28}{TOKENS[row]:>10,}{RATES[row]:>8.2f}"
            f"{cost[row]:>10.4f}{tok_share:>8.1f}{cost_share:>8.1f}"
        )
        check(f"{row} cost", cost[row], EXPECTED["row_cost"][row], 4)
        check(f"{row} token share", tok_share, EXPECTED["token_share"][row], 1)
        check(f"{row} cost share", cost_share, EXPECTED["cost_share"][row], 1)

    print(f"{'Total':<28}{total_tokens:>10,}{'':>8}{total_cost:>10.4f}{100.0:>8.1f}{100.0:>8.1f}")
    check("total tokens", total_tokens, EXPECTED["total_tokens"], 0)
    check("total cost", total_cost, EXPECTED["total_cost"], 4)
    check("rounds to the printed total", round(total_cost, 2), EXPECTED["vendor_total"], 2)

    input_share = sum(cost[r] for r in INPUT_ROWS) / total_cost * 100
    check("input as a share of the bill", input_share, EXPECTED["input_share_of_bill"], 1)

    uncached_input_tokens = sum(TOKENS[r] for r in INPUT_ROWS)
    uncached_total = (
        uncached_input_tokens * RATES["Fresh input"] / 1_000_000
        + cost["Output, thinking included"]
    )
    saving = (1 - total_cost / uncached_total) * 100
    check("uncached input tokens", uncached_input_tokens, EXPECTED["uncached_input_tokens"], 0)
    check("the same session uncached", uncached_total, EXPECTED["uncached_total"], 4)
    check("saving from caching", saving, EXPECTED["caching_saving"], 1)

    conversation = TOKENS["Cache writes"]
    cold = conversation * RATES["Cache writes"] / 1_000_000
    warm = conversation * RATES["Cache reads"] / 1_000_000
    check("one message after the cache expires", cold, EXPECTED["cold_message"], 4)
    check("the same message warm", warm, EXPECTED["warm_message"], 4)
    check("cold over warm", cold / warm, EXPECTED["cold_over_warm"], 1)
    check("cold message as a share of the session", cold / total_cost * 100,
          EXPECTED["cold_share_of_session"], 1)

    print()
    print(f"Input in all its forms:            {input_share:.1f}% of the bill")
    print(f"Tokens the model had already seen: "
          f"{TOKENS['Cache reads'] / total_tokens * 100:.1f}%")
    print(f"The same session with no caching:  ${uncached_total:.4f} "
          f"— a saving of {saving:.1f}%")
    print(f"One message after the cache expires: ${cold:.4f}, against ${warm:.4f} warm")
    print()

    if problems:
        for problem in problems:
            print(f"MISMATCH {problem}", file=sys.stderr)
        return 1

    print("every figure in the play follows from the inputs above")
    return 0


if __name__ == "__main__":
    sys.exit(main())
