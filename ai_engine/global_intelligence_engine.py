import random


def build_headline(topic):

    base = topic.title()

    variations = [
        f"{base}: What is happening?",
        f"{base}: Strategic shift detected",
        f"{base}: Why this matters now",
        f"{base}: Emerging global signal",
        f"{base}: Hidden dynamics revealed",
    ]

    return random.choice(variations)


def build_summary(signal):

    samples = signal.get("samples", [])

    if samples:
        return samples[0]

    return signal.get("topic", "")


def generate_intelligence(signals):

    if not signals:
        return []

    stories = []

    for s in signals[:10]:

        topic = s.get("topic", "")
        keywords = s.get("keywords", [])
        strength = s.get("boost", 1)

        headline = build_headline(topic)
        summary = build_summary(s)

        stories.append({
            "type": "intelligence",
            "headline": headline,
            "summary": summary,
            "keywords": keywords,
            "strength": strength
        })

    print("[INTELLIGENCE]", len(stories))

    return stories
