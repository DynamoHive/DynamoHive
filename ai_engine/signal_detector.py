def detect_signals(analysis):

    signals = []

    for item in analysis:

        score = item.get("score", 0)
        keywords = item.get("keywords", [])

        # basit trend filtresi
        if score > 10 or len(keywords) >= 3:

            signals.append({

                "text": item.get("text", ""),
                "keywords": keywords,
                "score": score

            })

    print("signals detected:", len(signals))

    return signals
