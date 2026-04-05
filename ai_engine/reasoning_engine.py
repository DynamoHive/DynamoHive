def add_reasoning(items):

    try:
        if not isinstance(items, list):
            return []

        for i in items:

            insight = i.get("insight", "")
            level = i.get("importance_level", "low")

            reason = ""

            if "geopolitical" in insight:
                reason = "Rising geopolitical tension with potential escalation risk."

            elif "ai" in insight:
                reason = "Indicates acceleration in AI competition and capability shift."

            elif "economic" in insight:
                reason = "Signals movement in capital or economic power structures."

            else:
                reason = "Emerging pattern with unclear trajectory."

            # önemle bağla
            if level == "critical":
                reason += " High impact expected."

            elif level == "high":
                reason += " Likely to influence broader systems."

            i["reasoning"] = reason

        return items

    except:
        return items if isinstance(items, list) else []
