class NarrativeEngine:

    def generate(self, intelligence):

        topic = intelligence.get("topic", "")

        reality = intelligence.get("summary", "") or topic
        trend = intelligence.get("trend", "emerging")
        score = intelligence.get("score", 1.0)

        context = self._build_context(topic)
        power = self._analyze_power(topic)
        cause = self._analyze_cause(topic)
        trajectory = self._build_trajectory(trend, score)

        title = self._build_headline(topic, trend)
        content = self._build_article(
            reality,
            context,
            cause,
            power,
            trajectory
        )

        return {
            "title": title,
            "content": content,
            "topic": topic
        }

    # -------------------------
    # CONTEXT (GERÇEK)
    # -------------------------
    def _build_context(self, topic):

        return (
            f"{topic} is not an isolated event. "
            f"It reflects broader structural changes across economic, technological, "
            f"and political systems shaping global dynamics."
        )

    # -------------------------
    # CAUSE (NEDEN)
    # -------------------------
    def _analyze_cause(self, topic):

        return (
            f"The emergence of {topic} is driven by underlying pressures such as "
            f"market competition, geopolitical instability, and systemic inefficiencies."
        )

    # -------------------------
    # POWER ANALYSIS (KRİTİK)
    # -------------------------
    def _analyze_power(self, topic):

        return (
            f"Power asymmetry is visible around {topic}. "
            f"Institutional actors and dominant platforms consolidate advantage, "
            f"while smaller actors and independent entities face increasing pressure."
        )

    # -------------------------
    # TRAJECTORY
    # -------------------------
    def _build_trajectory(self, trend, score):

        if score > 4:
            return "This development is accelerating rapidly and may become structurally dominant."

        if trend == "surging":
            return "The trend is intensifying and expanding across multiple domains."

        if trend == "rising":
            return "The trend is gaining stability and widening its influence."

        return "The trajectory remains uncertain but structurally relevant."

    # -------------------------
    # HEADLINE (TEMİZ)
    # -------------------------
    def _build_headline(self, topic, trend):

        topic = topic.capitalize()

        if trend == "surging":
            return f"{topic} accelerates across global systems"

        if trend == "rising":
            return f"{topic} expands its structural impact"

        return f"{topic} signals emerging systemic shift"

    # -------------------------
    # ARTICLE (AKICI)
    # -------------------------
    def _build_article(self, reality, context, cause, power, trajectory):

        return " ".join([
            reality,
            context,
            cause,
            power,
            trajectory
        ])


# 🔥 ENTRY POINT (KRİTİK)
def generate_narrative(intelligence):
    engine = NarrativeEngine()
    return engine.generate(intelligence)
