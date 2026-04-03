# =========================
# NARRATIVE ENGINE
# =========================

def generate_narrative(intel):

    topic = str(intel.get("topic", "")).strip()

    if not topic:
        return None

    # -------------------------
    # POWER INFO (VARSA)
    # -------------------------
    power = intel.get("power", {})
    dominant = power.get("dominant")
    winners = power.get("winners", [])
    losers = power.get("losers", [])

    # -------------------------
    # CONTENT BUILD
    # -------------------------
    title = topic

    content = f"{topic} is emerging as a significant global signal."

    if dominant:
        content += f" {dominant} appears to be gaining strategic advantage."

    if winners:
        content += f" Key winners include: {', '.join(winners)}."

    if losers:
        content += f" Under pressure: {', '.join(losers)}."

    content += " This may indicate a broader systemic shift."

    return {
        "title": title,
        "content": content
    }
⚠️ ÇOK ÖNEMLİ
