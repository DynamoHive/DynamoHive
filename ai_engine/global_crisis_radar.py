from datetime import datetime

CRISIS_KEYWORDS = {

    "war": ("military_conflict", 80),
    "conflict": ("military_conflict", 70),
    "invasion": ("military_conflict", 90),

    "sanction": ("economic_warfare", 65),
    "trade war": ("economic_warfare", 75),

    "energy": ("energy_instability", 60),
    "oil": ("energy_instability", 65),
    "gas": ("energy_instability", 65),

    "inflation": ("economic_instability", 60),
    "bank": ("financial_instability", 55),

    "ai": ("technology_competition", 50),
    "chip": ("technology_competition", 60),
    "semiconductor": ("technology_competition", 60),

    "supply chain": ("supply_chain_risk", 55)
}


def detect_crisis_signals(items):

    signals = []

    for item in items:

        title = item.get("title", "").lower()
        content = item.get("content", "").lower()

        text = title + " " + content

        for keyword, (category, score) in CRISIS_KEYWORDS.items():

            if keyword in text:

                signal = {

                    "title": item.get("title"),
                    "category": category,
                    "score": score,
                    "source": item.get("source"),
                    "timestamp": datetime.utcnow().timestamp(),

                    # varsayılan koordinatlar (dashboard haritası için)
                    "lat": 0,
                    "lon": 0
                }

                signals.append(signal)

                break

    return signals
