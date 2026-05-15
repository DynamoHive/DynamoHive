import time
import traceback

from backend.logger import logger
from backend.storage import save_signal

from ai_engine.multi_crawler import crawl
from ai_engine.data_pipeline import process_data
from ai_engine.signal_detector import detect_signals
from ai_engine.signal_ranking_engine import merge_ranked_signals
from ai_engine.signal_cluster import cluster_signals

from ai_engine.global_intelligence_engine import GlobalIntelligenceEngine
from ai_engine.decision_engine import DecisionEngine
from ai_engine.global_crisis_radar import detect_crisis_signals


# =====================================================
# MEMORY
# =====================================================
LAST_DATA = []
duplicate_cache = {}


def is_duplicate(topic: str) -> bool:
    now = time.time()

    # simple TTL cleanup
    if len(duplicate_cache) > 5000:
        duplicate_cache.clear()

    if topic in duplicate_cache:
        if now - duplicate_cache[topic] < 300:
            return True

    duplicate_cache[topic] = now
    return False


# =====================================================
# ORCHESTRATOR
# =====================================================
class Orchestrator:

    def __init__(self):
        self.cycle = 0
        self.intelligence = GlobalIntelligenceEngine()
        self.decision = DecisionEngine()

    def run_cycle(self):

        start = time.time()
        self.cycle += 1

        logger.info(f"[ORCHESTRATOR] Cycle {self.cycle} started")

        try:

            # =================================================
            # 1. CRAWL
            # =================================================
            raw = crawl()

            if not raw:
                raw = LAST_DATA or [{
                    "title": "system fallback signal",
                    "content": "no external data available",
                    "score": 0.3
                }]

            # =================================================
            # 2. PROCESS
            # =================================================
            raw = process_data(raw) if raw else raw

            if not raw:
                raw = [{
                    "title": "processed fallback signal",
                    "content": "pipeline recovery mode",
                    "score": 0.4
                }]

            LAST_DATA.clear()
            LAST_DATA.extend(raw[:100])

            # =================================================
            # 3. CRISIS DETECTION
            # =================================================
            try:
                crisis_signals = detect_crisis_signals(raw)
            except:
                crisis_signals = []

            crisis_map = {
                str(c.get("title", "")).lower(): c
                for c in crisis_signals
            }

            # =================================================
            # 4. SIGNAL DETECTION
            # =================================================
            signals = detect_signals(raw)

            if not signals:
                signals = [
                    {
                        "topic": x.get("title", "fallback signal"),
                        "score": 0.5
                    }
                    for x in raw[:10]
                ]

            # =================================================
            # 5. RANK + CLUSTER
            # =================================================
            signals = merge_ranked_signals(signals or [])
            signals = cluster_signals(signals or [])

            if not signals:
                signals = [{
                    "topic": "system fallback cluster",
                    "score": 0.5
                }]

            # =================================================
            # 6. CRISIS BOOST
            # =================================================
            for s in signals:
                topic = str(s.get("topic", "")).lower()

                if topic in crisis_map:
                    c = crisis_map[topic]
                    s["urgency"] = c.get("urgency", "high")
                    s["score"] = min(float(s.get("score", 0.5)) + 0.3, 1.0)

            # =================================================
            # 7. DECISION ENGINE
            # =================================================
            decisions = self.decision.evaluate(signals)

            if not decisions:
                decisions = [{
                    "publish": True,
                    "priority": 0.5
                }]

            # =================================================
            # 8. INTELLIGENCE LAYER
            # =================================================
            intel = self.intelligence.run(decisions)

            if not intel:
                intel = [{
                    "topic": "intelligence fallback",
                    "narrative": {
                        "title": "System Active",
                        "content": "Fallback intelligence generated"
                    }
                }]

            # merge decisions
            for i, item in enumerate(intel):
                if i < len(decisions):
                    item["decision"] = decisions[i]

            # =================================================
            # 9. GENERATION + PERSISTENCE
            # =================================================
            output = []

            for item in intel:

                topic = str(item.get("topic", "")).strip()
                if not topic:
                    continue

                decision = item.get("decision", {})

                if not decision.get("publish", True):
                    continue

                if is_duplicate(topic):
                    continue

                narrative = item.get("narrative") or {}

                title = narrative.get("title") or topic[:80]
                content = narrative.get("content") or topic

                payload = {
                    "title": title,
                    "topic": topic,
                    "content": content,
                    "priority": decision.get("priority", 0.5),
                    "published": 1,
                    "timestamp": int(time.time())
                }

                try:
                    save_signal(payload)
                except Exception as e:
                    logger.error(f"[STORAGE ERROR] {e}")

                output.append(payload)

                logger.info(f"[GENERATED] {topic}")

            # =================================================
            # FINAL RETURN (API SAFE)
            # =================================================
            return {
                "cycle": self.cycle,
                "timestamp": int(time.time()),
                "count": len(output),
                "signals": output
            }

        except Exception as e:
            traceback.print_exc()
            logger.error(f"[ORCHESTRATOR ERROR] {str(e)}")

            return {
                "cycle": self.cycle,
                "timestamp": int(time.time()),
                "count": 0,
                "signals": []
            }

        finally:
            logger.info(
                f"[ORCHESTRATOR] Cycle finished in {round(time.time() - start, 2)}s"
            )
