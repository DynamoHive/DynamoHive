def detect_signals(analysis):

    signals = []

    for item in analysis:

        if item["score"] > 20:
            signals.append(item)

    return signals
