def generate_narrative(intel):

    try:
        topic = str(intel.get("topic", ""))
        insight = intel.get("insight", "")
        actors = intel.get("actors", [])
        region = intel.get("region", "global")
        urgency = intel.get("urgency", "low")

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

        elif "ai" in insight:
            nxt = "Expect rapid iteration, competition, and regulatory response."

        elif "economic" in insight:
            nxt = "Monitor capital movement and institutional response."

        else:
            nxt = "Track signal frequency and cross-domain spread."

        # -------------------------
        # TITLE
        # -------------------------
        title = topic[:80]

        # -------------------------
        # CONTENT (REAL NARRATIVE)
        # -------------------------
        content = (
            f"{what}\n\n"
            f"Why it matters:\n{why}\n\n"
            f"Impact:\n{impact}\n\n"
            f"What to watch:\n{nxt}"
        )

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
