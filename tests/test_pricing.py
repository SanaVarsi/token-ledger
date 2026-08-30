from lib.pricing import estimate_cost


def test_estimates_cost_for_known_model():
    cost = estimate_cost(
        model="claude-sonnet-5",
        input_tokens=1_000_000,
        output_tokens=1_000_000,
        cache_creation_tokens=0,
        cache_read_tokens=0,
    )

    assert cost == 12.0


def test_returns_zero_for_unknown_model():
    cost = estimate_cost(
        model="some-future-model-we-dont-know",
        input_tokens=1000,
        output_tokens=1000,
        cache_creation_tokens=0,
        cache_read_tokens=0,
    )

    assert cost == 0.0


def test_estimates_cost_for_fable_model():
    cost = estimate_cost(
        model="claude-fable-5",
        input_tokens=1_000_000,
        output_tokens=1_000_000,
        cache_creation_tokens=0,
        cache_read_tokens=0,
    )

    assert cost == 60.0
