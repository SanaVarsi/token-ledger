import json

from lib.parser import parse_session_file


def test_reads_one_valid_assistant_line(tmp_path):
    fake_line = {
        "type": "assistant",
        "message": {
            "id": "msg_1",
            "usage": {
                "input_tokens": 10,
                "output_tokens": 20,
                "cache_creation_input_tokens": 0,
                "cache_read_input_tokens": 0,
            },
        },
        "timestamp": "2026-01-01T00:00:00Z",
    }
    log_file = tmp_path / "session.jsonl"
    log_file.write_text(json.dumps(fake_line) + "\n")

    events = parse_session_file(log_file)

    assert len(events) == 1
    assert events[0]["message"]["usage"]["input_tokens"] == 10


def test_skips_a_line_that_isnt_valid_json(tmp_path):
    good_line = {
        "type": "assistant",
        "message": {
            "id": "msg_2",
            "usage": {
                "input_tokens": 5,
                "output_tokens": 7,
                "cache_creation_input_tokens": 0,
                "cache_read_input_tokens": 0,
            },
        },
        "timestamp": "2026-01-01T00:00:00Z",
    }
    log_file = tmp_path / "session.jsonl"
    log_file.write_text("this is not valid json at all\n" + json.dumps(good_line) + "\n")

    events = parse_session_file(log_file)

    assert len(events) == 1
    assert events[0]["message"]["usage"]["input_tokens"] == 5


def test_skips_non_assistant_entries(tmp_path):
    noise_line = {
        "type": "queue-operation",
        "operation": "enqueue",
        "timestamp": "2026-01-01T00:00:00Z",
    }
    good_line = {
        "type": "assistant",
        "message": {
            "id": "msg_3",
            "usage": {
                "input_tokens": 3,
                "output_tokens": 4,
                "cache_creation_input_tokens": 0,
                "cache_read_input_tokens": 0,
            },
        },
        "timestamp": "2026-01-01T00:00:00Z",
    }
    log_file = tmp_path / "session.jsonl"
    log_file.write_text(json.dumps(noise_line) + "\n" + json.dumps(good_line) + "\n")

    events = parse_session_file(log_file)

    assert len(events) == 1
    assert events[0]["message"]["usage"]["input_tokens"] == 3


def test_deduplicates_same_message_id(tmp_path):
    line_one = {
        "type": "assistant",
        "message": {
            "id": "msg_dup",
            "usage": {
                "input_tokens": 100,
                "output_tokens": 200,
                "cache_creation_input_tokens": 0,
                "cache_read_input_tokens": 0,
            },
        },
        "timestamp": "2026-01-01T00:00:00Z",
    }
    line_two = {
        "type": "assistant",
        "message": {
            "id": "msg_dup",
            "usage": {
                "input_tokens": 100,
                "output_tokens": 200,
                "cache_creation_input_tokens": 0,
                "cache_read_input_tokens": 0,
            },
        },
        "timestamp": "2026-01-01T00:00:01Z",
    }
    log_file = tmp_path / "session.jsonl"
    log_file.write_text(json.dumps(line_one) + "\n" + json.dumps(line_two) + "\n")

    events = parse_session_file(log_file)

    assert len(events) == 1
