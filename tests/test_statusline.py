import json
import subprocess
import sys


def run_statusline(payload):
    result = subprocess.run(
        [sys.executable, "hooks/statusline.py"],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def test_shows_cost_from_transcript(tmp_path):
    fake_line = {
        "type": "assistant",
        "message": {
            "model": "claude-sonnet-5",
            "id": "msg_1",
            "content": [{"type": "tool_use", "name": "Bash", "input": {}}],
            "usage": {"input_tokens": 1_000_000, "output_tokens": 0},
        },
    }
    transcript = tmp_path / "session.jsonl"
    transcript.write_text(json.dumps(fake_line) + "\n")

    output = run_statusline({"transcript_path": str(transcript)})

    assert "Bash" in output
    assert "$2.00" in output
