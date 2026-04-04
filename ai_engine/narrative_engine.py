def generate_narrative(intel):

    topic = str(intel.get("topic", "")).strip()

    if not topic:
        return None

    power = intel.get("power", {})

    dominant = power.get("dominant")
    winners = power.get("winners", [])
    losers = power.get("losers", [])

    title = topic

    content = f"{topic} is emerging as a significant global signal."

    if dominant:
        content += f" {dominant} is gaining strategic advantage."

    if winners:
        content += f" Winners: {', '.join(winners)}."

    if losers:
        content += f" Under pressure: {', '.join(losers)}."

    return {
        "title": title,
        "content": content
    }
