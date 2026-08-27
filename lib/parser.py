import json


def parse_session_file(path):
    """Read a Claude Code session .jsonl file and return its parsed lines."""
    events = []
    seen_ids = set()
    with open(path) as f:
        for line in f:
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue

            if entry.get("type") != "assistant":
                continue
            if "usage" not in entry.get("message", {}):
                continue

            message_id = entry["message"].get("id")
            if message_id in seen_ids:
                continue
            seen_ids.add(message_id)

            events.append(entry)
    return events
