def add_reasoning(items):

    try:
        if not isinstance(items, list):
            return []

        for i in items:

            topic = str(i.get("topic", "")).lower()

            # -------------------------
            # INSIGHT (ASLA DIŞARIDAN ALMA)
            # -------------------------
            if any(x in topic for x in ["war", "military", "nato"]):
                insight = "geopolitical"

            elif any(x in topic for x in ["ai", "technology"]):
                insight = "technological"

            elif any(x in topic for x in ["market", "economy"]):
                insight = "economic"

            else:
                insight = "social"

            # -------------------------
            # REASON TEXT
            # -------------------------
            if insight == "geopolitical":
                reason = "Rising geopolitical tension with potential escalation risk."

            elif insight == "technological":
                reason = "Acceleration in technological competition and capability shift."

            elif insight == "economic":
                reason = "Movement in capital and economic power structures."

            else:
                reason = "Emerging pattern with unclear trajectory."

            # -------------------------
            # IMPORTANCE LINK
            # -------------------------
            level = i.get("importance_level", "low")

            if level == "critical":
                reason += " High impact expected."

            elif level == "high":
                reason += " Likely to influence broader systems."

            # -------------------------
            # OUTPUT (KRİTİK STRUCTURE)
            # -------------------------
            i["insight"] = insight
            i["reasoning"] = {
                "text": reason,
                "confidence": 0.6
            }

        return items

    except:
        return items if isinstance(items, list) else []
