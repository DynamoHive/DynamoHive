class NarrativeEngine:

    def generate(self, intelligence):

        if not intelligence or not isinstance(intelligence, dict):
            return None

        topic = str(intelligence.get("topic", "")).strip()

        if not topic or len(topic) < 3:
            return None

        # 1. REALITY
        reality = intelligence.get("summary", "") or f"{topic} is showing emerging systemic signals."

        # 2. CONTEXT
        context = self._build_context(intelligence)

        # 3. CONTRADICTIONS
        contradictions = self._detect_contradictions(intelligence)

        # 4. POWER
        power = self._analyze_power(intelligence)

        # 5. TRAJECTORY
        trajectory = self._build_trajectory(intelligence)

        # 6. BUILD
        title = self._build_headline(topic, trajectory)
        content = self._build_article(
            reality,
            context,
            contradictions,
            power,
            trajectory
        )

        # FINAL SAFETY
        if not title or not content or len(content) < 120:
            return None

        return {
            "title": title.strip(),
            "content": content.strip(),
            "topic": topic
        }

    # -------------------------
    # CONTEXT
    # -------------------------
    def _build_context(self, data):
        topic = data.get("topic", "This issue")
        return (
            f"{topic} is embedded within broader systemic transformations, "
            f"shaped by economic pressure, political realignment, and structural shifts."
        )

    # -------------------------
    # CONTRADICTIONS
    # -------------------------
    def _detect_contradictions(self, data):
        topic = data.get("topic", "this issue")

        return [
            f"Public narratives around {topic} diverge from observable outcomes.",
            f"Institutional responses often conflict with stated objectives regarding {topic}."
        ]

    # -------------------------
    # POWER ANALYSIS
    # -------------------------
    def _analyze_power(self, data):

        score = data.get("score", 1.0)

        if score > 4:
            return {
                "winners": ["state actors", "global institutions"],
                "losers": ["local populations", "independent actors"]
            }

        return {
            "winners": ["established entities"],
            "losers": ["emerging or vulnerable groups"]
        }

    # -------------------------
    # TRAJECTORY
    # -------------------------
    def _build_trajectory(self, data):

        trend = data.get("trend", "emerging")

        if trend == "surging":
            return "This development is accelerating and becoming systemic."

        if trend == "rising":
            return "This trend is expanding and stabilizing."

        return "The trajectory remains uncertain but structurally relevant."

    # -------------------------
    # HEADLINE
    # -------------------------
    def _build_headline(self, topic, trajectory):

        topic = topic.capitalize()

        if "accelerating" in trajectory:
            return f"{topic} rapidly escalates across global systems"

        if "stabilizing" in trajectory:
            return f"{topic} expands its structural influence"

        return f"Emerging dynamics reshape narratives around {topic}"

    # -------------------------
    # ARTICLE
    # -------------------------
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


# -------------------------
# 🔥 GLOBAL FUNCTION (CRITICAL)
# -------------------------
_engine_instance = NarrativeEngine()

def generate_narrative(intelligence):
    try:
        return _engine_instance.generate(intelligence)
    except Exception as e:
        print("[NARRATIVE ERROR]", e)
        return None
