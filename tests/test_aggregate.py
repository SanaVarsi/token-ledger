from lib.aggregate import aggregate_usage
from lib.pricing import estimate_cost


def test_sums_single_event_into_its_bucket():
    events = [
        {
            "message": {
                "model": "claude-sonnet-5",
                "content": [{"type": "tool_use", "name": "Bash", "input": {}}],
                "usage": {"input_tokens": 10, "output_tokens": 20},
            }
        }
    ]

    result = aggregate_usage(events)
    expected_cost = estimate_cost("claude-sonnet-5", 10, 20, 0, 0)

    assert result == [
        {
            "category": "tool",
            "name": "Bash",
            "input_tokens": 10,
            "output_tokens": 20,
            "cost": expected_cost,
        }
    ]


def test_combines_matching_buckets_and_keeps_others_separate():
    events = [
        {
            "message": {
                "model": "claude-sonnet-5",
                "content": [{"type": "tool_use", "name": "Bash", "input": {}}],
                "usage": {"input_tokens": 10, "output_tokens": 20},
            }
        },
        {
            "message": {
                "model": "claude-sonnet-5",
                "content": [{"type": "tool_use", "name": "Bash", "input": {}}],
                "usage": {"input_tokens": 5, "output_tokens": 7},
            }
        },
        {
            "message": {
                "model": "claude-sonnet-5",
                "content": [{"type": "text", "text": "just a reply"}],
                "usage": {"input_tokens": 1, "output_tokens": 2},
            }
        },
    ]

    result = aggregate_usage(events)
    bash_cost = estimate_cost("claude-sonnet-5", 15, 27, 0, 0)
    general_cost = estimate_cost("claude-sonnet-5", 1, 2, 0, 0)

    assert len(result) == 2
    assert {
        "category": "tool", "name": "Bash",
        "input_tokens": 15, "output_tokens": 27, "cost": bash_cost,
    } in result
    assert {
        "category": "general", "name": None,
        "input_tokens": 1, "output_tokens": 2, "cost": general_cost,
    } in result
