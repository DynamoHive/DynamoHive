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

        results = []

        for signal in signals:

            try:
                topic = str(signal.get("topic", "")).strip()

                mem = self.memory.load(signal) or {}

                ctx = self.context.build(signal, mem)

                reasoning = self.reasoning.analyze(signal, ctx)

                # 🔥 insight context'e yaz
                ctx["insight"] = reasoning.get("insight", "")

                prediction = self.prediction.forecast(signal, ctx)

                intel = {
                    "topic": topic,
                    "signal": signal,
                    "context": ctx,
                    "reasoning": reasoning,
                    "prediction": prediction,
                    "insight": reasoning.get("insight", ""),
                    "actors": ctx.get("actors", []),
                    "region": ctx.get("region", "global"),
                    "urgency": prediction.get("urgency", "low"),
                }

                narrative = generate_narrative(intel)

                intel["narrative"] = narrative

                if topic and narrative:
                    results.append(intel)

            except:
                continue

        return results
