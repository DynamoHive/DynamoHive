from ai_engine.memory_engine import MemoryEngine
from ai_engine.context_analyzer import ContextAnalyzer
from ai_engine.reasoning_engine import ReasoningEngine
from ai_engine.prediction_engine import PredictionEngine

# SENİN FONKSİYON
from ai_engine.narrative_engine import generate_narrative


class GlobalIntelligenceEngine:

    def __init__(self):
        self.memory = MemoryEngine()
        self.context = ContextAnalyzer()
        self.reasoning = ReasoningEngine()
        self.prediction = PredictionEngine()

    def run(self, signals):

        results = []

        for signal in signals:

            try:
                topic = str(signal.get("topic", "")).strip()

                # -------------------------
                # MEMORY
                # -------------------------
                mem = self.memory.load(signal) or {}

                # -------------------------
                # CONTEXT
                # -------------------------
                ctx = self.context.build(signal, mem) or {}

                # -------------------------
                # REASONING
                # -------------------------
                reasoning = self.reasoning.analyze(signal, ctx) or {}

                # -------------------------
                # PREDICTION
                # -------------------------
                prediction = self.prediction.forecast(signal, ctx) or {}

                # -------------------------
                # INTEL OBJECT (MERKEZ)
                # -------------------------
                intel = {
                    "topic": topic,
                    "signal": signal,

                    # CORE
                    "context": ctx,
                    "reasoning": reasoning,
                    "prediction": prediction,

                    # NARRATIVE INPUT (KRİTİK)
                    "insight": reasoning.get("insight", ""),
                    "actors": ctx.get("actors", []),
                    "region": ctx.get("region", "global"),
                    "urgency": prediction.get("urgency", "low"),
                }

                # -------------------------
                # NARRATIVE (SENİN SİSTEM)
                # -------------------------
                narrative = generate_narrative(intel)

                intel["narrative"] = narrative

                # -------------------------
                # GUARD (boşları at)
                # -------------------------
                if not topic or not narrative:
                    continue

                results.append(intel)

            except Exception:
                continue

        return results
