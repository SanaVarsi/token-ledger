"""
Pricing table for Claude models — last verified 2026-08-30.
Prices can change; check https://www.anthropic.com/pricing before trusting
these numbers long-term. If a number here looks stale, update it directly —
this is the one file that needs occasional manual refreshing.
"""

PRICING_PER_MILLION = {
    "claude-opus-5": {"input": 5.00, "output": 25.00},
    "claude-sonnet-5": {"input": 2.00, "output": 10.00},
    "claude-haiku-4-5": {"input": 1.00, "output": 5.00},
    "claude-fable-5": {"input": 10.00, "output": 50.00},
}

CACHE_WRITE_MULTIPLIER = 1.25  # writing to cache costs ~1.25x normal input price
CACHE_READ_MULTIPLIER = 0.1    # reading from cache costs ~0.1x normal input price


def estimate_cost(model, input_tokens, output_tokens, cache_creation_tokens, cache_read_tokens):
    """Estimate the dollar cost of one entry, given its token counts."""
    rates = PRICING_PER_MILLION.get(model)
    if rates is None:
        return 0.0

    input_rate = rates["input"] / 1_000_000
    output_rate = rates["output"] / 1_000_000
    cache_write_rate = input_rate * CACHE_WRITE_MULTIPLIER
    cache_read_rate = input_rate * CACHE_READ_MULTIPLIER

    return (
        input_tokens * input_rate
        + output_tokens * output_rate
        + cache_creation_tokens * cache_write_rate
        + cache_read_tokens * cache_read_rate
    )
