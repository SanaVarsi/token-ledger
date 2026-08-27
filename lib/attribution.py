def classify_event(event):
    """Look at one clean log entry and decide which bucket it belongs to."""
    content = event.get("message", {}).get("content", [])
    for item in content:
        if item.get("type") != "tool_use":
            continue

        name = item.get("name", "")

        if name == "Skill":
            skill_name = item.get("input", {}).get("skill")
            return {"category": "skill", "name": skill_name}

        if name.startswith("mcp__plugin_"):
            remainder = name[len("mcp__plugin_"):]
            plugin_name = remainder.split("_", 1)[0]
            return {"category": "plugin", "name": plugin_name}

        return {"category": "tool", "name": name}

    return {"category": "general", "name": None}
