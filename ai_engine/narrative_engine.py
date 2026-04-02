class NarrativeEngine:

    def generate(self, intelligence):

        # 1. REALITY
        reality = intelligence.get("summary", "")

        # 2. CONTEXT
        context = self._build_context(intelligence)

        # 3. CONTRADICTIONS
        contradictions = self._detect_contradictions(intelligence)

        # 4. POWER
        power = self._analyze_power(intelligence)

        # 5. TRAJECTORY
        trajectory = self._build_trajectory(intelligence)

        # 6. ARTICLE (SENİN ESKİ SİSTEMİN YERİNE)
        title = self._build_headline(intelligence.get("topic"), trajectory)
        content = self._build_article(
            reality,
            context,
            contradictions,
            power,
            trajectory
        )

        return {
            "title": title,
            "content": content,
            "topic": intelligence.get("topic")
        }

    # -------------------------
    # INTERNAL METHODS
    # -------------------------

    def _build_context(self, data):
        topic = data.get("topic")
        return (
            f"{topic} is embedded within broader systemic transformations, "
            f"shaped by economic pressure, political realignment, and structural shifts."
        )

    def _detect_contradictions(self, data):
        topic = data.get("topic")
        return [
            f"Public narratives around {topic} diverge from actual policy outcomes.",
            f"Institutional actions contradict declared intentions regarding {topic}."
        ]

    def _analyze_power(self, data):
        return {
            "winners": ["state actors", "dominant institutions"],
            "losers": ["marginalized groups", "independent actors"]
        }

    def _build_trajectory(self, data):
        trend = data.get("trend", "emerging")

        if trend == "surging":
            return "This development is accelerating and becoming systemic."
        elif trend == "rising":
            return "This trend is expanding and stabilizing."
        else:
            return "The trajectory remains uncertain but structurally relevant."

    def _build_headline(self, topic, trajectory):

        if "accelerating" in trajectory:
            return f"{topic.capitalize()} rapidly escalates across global systems"

        if "stabilizing" in trajectory:
            return f"{topic.capitalize()} expands its structural influence"

        return f"Emerging dynamics reshape narratives around {topic}"

    def _build_article(self, reality, context, contradictions, power, trajectory):

        contradictions_text = " ".join(contradictions)

        winners = ", ".join(power.get("winners", []))
        losers = ", ".join(power.get("losers", []))

        return " ".join([
            reality,
            context,
            contradictions_text,
            f"Power dynamics reveal asymmetry. Winners: {winners}. Losers: {losers}.",
            trajectory
        ])
