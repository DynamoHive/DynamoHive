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

        title = str(item.get("title", "")).lower()
        content = str(item.get("content", "")).lower()

        text = title + " " + content

        category_scores = {}
        matched_keywords = []

        # -------------------------
        # 1. MULTI-KEYWORD SCAN
        # -------------------------
        for keyword, (category, score) in CRISIS_KEYWORDS.items():

            if keyword in text:

                matched_keywords.append(keyword)

                if category not in category_scores:
                    category_scores[category] = 0

                category_scores[category] += score

        if not category_scores:
            continue

        # -------------------------
        # 2. EN GÜÇLÜ KATEGORİ
        # -------------------------
        category = max(category_scores, key=category_scores.get)
        total_score = category_scores[category]

        # normalize (çok uçmasın)
        total_score = min(total_score, 100)

        # -------------------------
        # 3. URGENCY BELİRLE
        # -------------------------
        if total_score > 80:
            urgency = "high"
        elif total_score > 60:
            urgency = "medium"
        else:
            urgency = "low"

        # -------------------------
        # 4. SIGNAL OBJECT
        # -------------------------
        signal = {

            "title": item.get("title"),
            "category": category,
            "score": round(total_score / 100, 2),  # normalize 0-1
            "raw_score": total_score,
            "urgency": urgency,

            "matched_keywords": matched_keywords,

            "source": item.get("source") or "Public Data",
            "timestamp": datetime.utcnow().timestamp(),

            # basit koordinat placeholder
            "lat": 0,
            "lon": 0
        }

        signals.append(signal)

    return signals

    
