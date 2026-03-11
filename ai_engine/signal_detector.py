def signal_detector(trends):

    signals = []

    for t in trends:

        if len(t["topic"]) > 4:

            signals.append({
                "topic": t["topic"],
                "signal": "active"
            })

    print("Signals:", signals)

    return signals
