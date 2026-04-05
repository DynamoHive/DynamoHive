# -------------------------
# SAFE HELPERS
# -------------------------

def safe_str(x):
    try:
        return str(x)
    except:
        return ""


def safe_list(x):
    if isinstance(x, list):
        return x
    return []


# -------------------------
# MAIN
# -------------------------

def generate_narrative(intel):

    try:
        if not isinstance(intel, dict):
            return None

        topic = safe_str(intel.get("topic"))
        insight = safe_str(intel.get("insight")).lower()
        actors = safe_list(intel.get("actors"))
        region = safe_str(intel.get("region")) or "global"
        urgency = safe_str(intel.get("urgency")) or "low"

        if not topic:
            return None

        # -------------------------
        # WHAT
        # -------------------------
        what = topic

        # -------------------------
        # WHY
        # -------------------------
        if "geopolitical" in insight:
            why = "This reflects rising geopolitical tension and strategic positioning."

        elif "ai" in insight or "technological" in insight:
            why = "This signals acceleration in technological competition and capability shifts."

        elif "economic" in insight:
            why = "This indicates movement in economic power or capital flows."

        elif "social" in insight:
            why = "This reflects underlying social instability or pressure."

        else:
            why = "This is an emerging signal gaining structural relevance."

        # -------------------------
        # IMPACT
        # -------------------------
        if urgency == "high":
            impact = "High probability of escalation or broader systemic effects."

        elif urgency == "medium":
            impact = "Likely to influence regional or sector-level dynamics."

        else:
            impact = "Currently limited, but worth monitoring."

        # -------------------------
        # NEXT
        # -------------------------
        if "geopolitical" in insight:
            nxt = "Watch for escalation, alliances, or counter-actions."

        elif "ai" in insight or "technological" in insight:
            nxt = "Expect rapid iteration, competition, and regulatory response."

        elif "economic" in insight:
            nxt = "Monitor capital movement and institutional response."

        elif "social" in insight:
            nxt = "Watch for escalation in civil response or policy reaction."

        else:
            nxt = "Track signal frequency and cross-domain spread."

        # -------------------------
        # TITLE
        # -------------------------
        title = topic[:80]

        # -------------------------
        # CONTENT
        # -------------------------
        content = (
            f"{what}\n\n"
            f"Why it matters:\n{why}\n\n"
            f"Impact:\n{impact}\n\n"
            f"What to watch:\n{nxt}"
        )

        # -------------------------
        # FINAL OUTPUT
        # -------------------------
        return {
            "title": title,
            "content": content,
            "meta": {
                "actors": actors,
                "region": region,
                "urgency": urgency
            }
        }

    except:
        return None
