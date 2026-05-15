import time
import traceback

from backend.logger import logger
from backend.storage import save_signal
from backend.cache import set_last_data, get_last_data, is_duplicate

from ai_engine.multi_crawler import crawl
from ai_engine.data_pipeline import process_data
from ai_engine.signal_detector import detect_signals
from ai_engine.signal_ranking_engine import merge_ranked_signals
from ai_engine.signal_cluster import cluster_signals

from ai_engine.global_intelligence_engine import GlobalIntelligenceEngine
from ai_engine.decision_engine import DecisionEngine
from ai_engine.global_crisis_radar import detect_crisis_signals


class Orchestrator:

    def __init__(self):
        self.cycle = 0
        self.intelligence = GlobalIntelligenceEngine()
        self.decision = DecisionEngine()

    # =====================================================
    # MAIN PIPELINE
    # =====================================================
    def run_cycle(self):

        start = time.time()
        self.cycle += 1

        logger.info(f"[ORCHESTRATOR] Cycle {self.cycle} started")

        try:
            # -----------------------------
            # 1. CRAWL
            # -----------------------------
            raw = crawl()

            if not raw:
                raw = get_last_data() or []

            # -----------------------------
            # 2. PROCESS
            # -----------------------------
            raw = process_data(raw)

            if not raw:
                return []

            set_last_data(raw[:100])

            # -----------------------------
            # 3. CRISIS DETECTION
            # -----------------------------
            crisis_signals = detect_crisis_signals(raw)

            crisis_map = {
                str(c.get("title", "")).lower().strip(): c
                for c in crisis_signals
                if c.get("title")
            }

            # -----------------------------
            # 4. SIGNAL DETECTION
            # -----------------------------
            signals = detect_signals(raw)

            if not signals:
                signals = [
                    {"topic": x.get("title", ""), "score": 0.5}
                    for x in raw[:10]
                ]

            signals = merge_ranked_signals(signals)
            signals = cluster_signals(signals)

            if not signals:
                return []

            # -----------------------------
            # 5. CRISIS BOOST
            # -----------------------------
            for s in signals:
                topic = str(s.get("topic", "")).lower()

                for k, v in crisis_map.items():
                    if k and k in topic:
                        s["urgency"] = v.get("urgency", "high")
                        s["score"] = min(float(s.get("score", 0.5)) + 0.3, 1.0)
                        break

            # -----------------------------
            # 6. DECISION ENGINE
            # -----------------------------
            decisions = self.decision.evaluate(signals)

            if not decisions:
                return []

            # -----------------------------
            # 7. INTELLIGENCE ENGINE
            # -----------------------------
            intel = self.intelligence.run(decisions)

            if not intel:
                return []

            for i, item in enumerate(intel):
                if i < len(decisions):
                    item["decision"] = decisions[i]

            # -----------------------------
            # 8. OUTPUT GENERATION
            # -----------------------------
            output = []

            for item in intel:

                topic = str(item.get("topic", "")).strip()
                if not topic:
                    continue

                decision = item.get("decision", {})

                if not decision.get("publish", True):
                    continue

                # duplicate protection (NOW EXTERNAL CACHE)
                if is_duplicate(topic):
                    continue

                narrative = item.get("narrative") or {}

                payload = {
                    "title": narrative.get("title") or topic[:80],
                    "topic": topic,
                    "content": narrative.get("content") or topic,
                    "priority": float(decision.get("priority", 0.5)),
                    "published": True,
                    "timestamp": int(time.time())
                }

                try:
                    save_signal(payload)
                except Exception as e:
                    logger.error(f"[DB ERROR] {e}")

                output.append(payload)

                logger.info(f"[GENERATED] {topic}")

            return output

        except Exception as e:
            traceback.print_exc()
            logger.error(f"[ORCHESTRATOR ERROR] {str(e)}")
            return []

        finally:
            logger.info(
                f"[ORCHESTRATOR] Cycle finished in {round(time.time() - start, 2)}s"
            )
