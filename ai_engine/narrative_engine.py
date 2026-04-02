import random


def build_headline(topic, trend, category):

    if trend == "surging":
        return f"{topic.capitalize()} rapidly escalates in global {category} landscape"

    if trend == "rising":
        return f"{topic.capitalize()} gains traction across {category} sectors"

    return f"Early signals emerge around {topic} in {category}"


def build_context(signal):

    topic = signal.get("text")
    category = signal.get("category")
    count = signal.get("count", 0)

    return (
        f"Recent data indicates that {topic} is becoming increasingly visible "
        f"within the {category} domain, with {count} independent signals detected."
    )


def build_implication(signal):

    risk = signal.get("risk")
    topic = signal.get("text")

    if risk == "high":
        return f"The acceleration of {topic} may lead to significant global consequences."

    if risk == "medium":
        return f"The development of {topic} suggests a potentially important shift."

    return f"{topic} remains in an early stage but warrants monitoring."


def build_forward(signal):

    trend = signal.get("trend")
    topic = signal.get("text")

    if trend == "surging":
        return f"If momentum continues, {topic} could dominate upcoming global narratives."

    if trend == "rising":
        return f"{topic} is expected to expand its influence in the near term."

    return f"Further signals are required to confirm the trajectory of {topic}."


def generate_narrative(signal):

    topic = signal.get("text")
    category = signal.get("category", "global")
    trend = signal.get("trend", "emerging")

    title = build_headline(topic, trend, category)

    paragraphs = [
        build_context(signal),
        build_implication(signal),
        build_forward(signal)
    ]

    content = " ".join(paragraphs)

    return {
        "title": title,
        "content": content,
        "topic": topic
    }
