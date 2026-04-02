def signal_to_intelligence(signal):

    return {
        "topic": signal.get("text"),
        "summary": f"{signal.get('text')} is gaining visibility with {signal.get('count', 0)} detected signals.",
        "trend": signal.get("trend", "emerging")
    }
