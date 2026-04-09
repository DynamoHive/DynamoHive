from ai_engine.memory_engine import MemoryEngine
from ai_engine.context_analyzer import ContextAnalyzer
from ai_engine.reasoning_engine import ReasoningEngine
from ai_engine.prediction_engine import PredictionEngine
from ai_engine.narrative_engine import NarrativeEngine


class GlobalIntelligenceEngine:

    def __init__(self):
        self.memory = MemoryEngine()
        self.context = ContextAnalyzer()
        self.reasoning = ReasoningEngine()
        self.prediction = PredictionEngine()
        self.narrative = NarrativeEngine()

    def run(self, signals):

        results = []

        for signal in signals:

            mem = self.memory.load(signal)
            ctx = self.context.build(signal, mem)

            reasoning = self.reasoning.analyze(signal, ctx)
            prediction = self.prediction.forecast(signal, ctx)

            narrative = self.narrative.generate(
                signal=signal,
                context=ctx,
                reasoning=reasoning,
                prediction=prediction
            )

            results.append({
                "topic": signal.get("topic"),
                "signal": signal,
                "context": ctx,
                "reasoning": reasoning,
                "prediction": prediction,
                "narrative": narrative
            })

        return results
