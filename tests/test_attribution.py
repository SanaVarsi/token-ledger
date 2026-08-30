from lib.attribution import classify_event


def test_classifies_skill_usage():
    event = {
        "message": {
            "content": [
                {
                    "type": "tool_use",
                    "name": "Skill",
                    "input": {"skill": "superpowers:brainstorming"},
                }
            ]
        }
    }

    result = classify_event(event)

    assert result == {"category": "skill", "name": "superpowers:brainstorming"}


def test_classifies_plain_tool_usage():
    event = {
        "message": {
            "content": [
                {
                    "type": "tool_use",
                    "name": "Bash",
                    "input": {"command": "ls"},
                }
            ]
        }
    }

    result = classify_event(event)

    assert result == {"category": "tool", "name": "Bash"}


def test_classifies_plugin_tool_usage():
    event = {
        "message": {
            "content": [
                {
                    "type": "tool_use",
                    "name": "mcp__plugin_claude-mem_mcp-search__search",
                    "input": {"query": "something"},
                }
            ]
        }
    }

    result = classify_event(event)

    assert result == {"category": "plugin", "name": "claude-mem"}


def test_classifies_plain_text_as_general():
    event = {
        "message": {
            "content": [
                {"type": "text", "text": "Just a plain reply, no tool used."}
            ]
        }
    }

    result = classify_event(event)

    assert result == {"category": "general", "name": None}
