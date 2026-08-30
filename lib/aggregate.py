from lib.attribution import classify_event
from lib.pricing import estimate_cost

def aggregate_usage(events):
    """Group events by bucket (skill/plugin/tool/general) and sum their tokens + cost."""
    buckets = {}

    for event in events:
        classification = classify_event(event)
        key = (classification["category"], classification["name"])

        message = event.get("message", {})
        usage = message.get("usage", {})
        model = message.get("model")

        input_tokens = usage.get("input_tokens", 0)
        output_tokens = usage.get("output_tokens", 0)
        cache_creation_tokens = usage.get("cache_creation_input_tokens", 0)
        cache_read_tokens = usage.get("cache_read_input_tokens", 0)

        cost = estimate_cost(
            model=model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cache_creation_tokens=cache_creation_tokens,
            cache_read_tokens=cache_read_tokens,
        )

        if key not in buckets:
            buckets[key] = {"input_tokens": 0, "output_tokens": 0, "cost": 0.0}

        buckets[key]["input_tokens"] += input_tokens
        buckets[key]["output_tokens"] += output_tokens
        buckets[key]["cost"] += cost

    result = []
    for (category, name), totals in buckets.items():
        result.append({
            "category": category,
            "name": name,
            "input_tokens": totals["input_tokens"],
            "output_tokens": totals["output_tokens"],
            "cost": totals["cost"],
        })
    return result
