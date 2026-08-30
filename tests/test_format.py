from lib.format import format_status_line


def test_formats_single_bucket():
    results = [
        {"category": "tool", "name": "Bash", "input_tokens": 10, "output_tokens": 20, "cost": 2.0}
    ]

    line = format_status_line(results)

    assert line == "💰 $2.00 this session · Bash 100%"


def test_sorts_buckets_by_cost_descending():
    results = [
        {"category": "general", "name": None, "input_tokens": 1, "output_tokens": 2, "cost": 1.0},
        {"category": "tool", "name": "Bash", "input_tokens": 10, "output_tokens": 20, "cost": 3.0},
    ]

    line = format_status_line(results)

    assert line == "\U0001F4B0 $4.00 this session · Bash 75% · general 25%"
