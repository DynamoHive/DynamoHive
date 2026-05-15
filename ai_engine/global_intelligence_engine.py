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
                # 1. TOPIC SAFE EXTRACTION
                # =================================================
                topic = str(
                    signal.get("topic")
                    or signal.get("title")
                    or signal.get("text")
                    or ""
                ).strip()

                if not topic:
                    continue

                # =================================================
                # 2. MEMORY LAYER (SAFE)
                # =================================================
                mem = {}
                try:
                    mem = self.memory.load(signal) or {}
                except:
                    mem = {}

                # =================================================
                # 3. CONTEXT LAYER (SAFE)
                # =================================================
                ctx = {}
                try:
                    ctx = self.context.build(signal, mem) or {}
                except:
                    ctx = {}

                # =================================================
                # 4. REASONING LAYER
                # =================================================
                reasoning = {}
                try:
                    reasoning = self.reasoning.analyze(signal, ctx) or {}
                except:
                    reasoning = {}

                ctx["insight"] = reasoning.get("insight", "")

                # =================================================
                # 5. PREDICTION LAYER
                # =================================================
                prediction = {}
                try:
                    prediction = self.prediction.forecast(signal, ctx) or {}
                except:
                    prediction = {}

                # =================================================
                # 6. INTEL OBJECT
                # =================================================
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

                # =================================================
                # 7. NARRATIVE (CRITICAL FIX)
                # =================================================
                narrative = None
                try:
                    narrative = generate_narrative(intel)
                except:
                    narrative = None

                if not narrative:
                    narrative = {
                        "title": topic[:80],
                        "content": topic,
                        "meta": {
                            "fallback": True
                        }
                    }

                intel["narrative"] = narrative

                results.append(intel)

            except Exception:
                # NEVER BREAK PIPELINE
                continue

        return results
