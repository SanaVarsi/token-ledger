def format_status_line(results):
    """Turn aggregated bucket results into one display line."""
    total_cost = sum(r["cost"] for r in results)

    parts = []
    for r in sorted(results, key=lambda r: -r["cost"]):
        name = r["name"] or "general"
        percent = round(r["cost"] / total_cost * 100) if total_cost else 0
        parts.append(f"{name} {percent}%")

    line = f"\U0001F4B0 ${total_cost:.2f} this session"
    if parts:
        line += " · " + " · ".join(parts)
    return line
