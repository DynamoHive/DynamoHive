from ai_engine.memory_engine import MemoryEngine
from ai_engine.context_analyzer import ContextAnalyzer
from ai_engine.reasoning_engine import ReasoningEngine
from ai_engine.prediction_engine import PredictionEngine
from ai_engine.narrative_engine import generate_narrative


class GlobalIntelligenceEngine:

    def __init__(self):
        self.memory = MemoryEngine()
        self.context = ContextAnalyzer()
        self.reasoning = ReasoningEngine()
        self.prediction = PredictionEngine()

    def run(self, signals):

        if not isinstance(signals, list) or not signals:
            return []

        results = []

        for signal in signals:

            try:
                # =================================================
                # 1. TOPIC EXTRACTION (SAFE + BETTER FALLBACK)
                # =================================================
                topic = str(
                    signal.get("topic")
                    or signal.get("title")
                    or signal.get("text")
                    or "unknown signal"
                ).strip()

                # =================================================
                # 2. MEMORY
                # =================================================
                try:
                    mem = self.memory.load(signal) or {}
                except:
                    mem = {}

                # =================================================
                # 3. CONTEXT
                # =================================================
                try:
                    ctx = self.context.build(signal, mem) or {}
                except:
                    ctx = {}

                # =================================================
                # 4. REASONING (ENHANCED SAFETY)
                # =================================================
                try:
                    reasoning = self.reasoning.analyze(signal, ctx) or {}
                except:
                    reasoning = {}

                insight = reasoning.get("insight") or ""
                ctx["insight"] = insight

                # =================================================
                # 5. PREDICTION
                # =================================================
                try:
                    prediction = self.prediction.forecast(signal, ctx) or {}
                except:
                    prediction = {}

                urgency = prediction.get("urgency", "low")
                if urgency not in ["low", "medium", "high"]:
                    urgency = "low"

                # =================================================
                # 6. SIGNAL ENRICHMENT (CRITICAL FIX)
                # =================================================
                signal_strength = float(signal.get("score", 0.5))
                if "crisis" in insight.lower():
                    signal_strength = min(signal_strength + 0.2, 1.0)

                # =================================================
                # 7. INTEL OBJECT (MORE STABLE SEMANTICS)
                # =================================================
                intel = {
                    "topic": topic,
                    "signal": signal,
                    "context": ctx,
                    "reasoning": reasoning,
                    "prediction": prediction,
                    "insight": insight,
                    "actors": ctx.get("actors") or [],
                    "region": ctx.get("region") or "global",
                    "urgency": urgency,
                    "strength": signal_strength
                }

                # =================================================
                # 8. NARRATIVE (ROBUST FALLBACK)
                # =================================================
                try:
                    narrative = generate_narrative(intel)
                except:
                    narrative = None

                if not narrative:
                    narrative = {
                        "title": topic[:80],
                        "content": (
                            f"{topic}\n\n"
                            f"Insight: {insight or 'No deep analysis available'}\n\n"
                            f"Region: {intel['region']}\n"
                            f"Urgency: {urgency}"
                        ),
                        "meta": {
                            "fallback": True,
                            "strength": signal_strength
                        }
                    }

                intel["narrative"] = narrative

                results.append(intel)

            except Exception:
                continue

        return results
