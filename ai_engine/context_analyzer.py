def build_context(signal):
    topic = str(signal.get("topic", "")).lower()
    context = str(signal.get("context", "")).lower()

    return f"{topic} {context}".strip()
