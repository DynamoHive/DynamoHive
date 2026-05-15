import time
import traceback
import hashlib

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

LAST_DATA = {}
duplicate_cache = {}

DEBUG = True


def is_duplicate(topic: str) -> bool:
    try:
        key = hashlib.md5(
            (topic.lower()).encode()
        ).hexdigest()
    except Exception:
        return False

    now = time.time()

    if key in duplicate_cache:
        if now - duplicate_cache[key] < 300:
            if DEBUG:
                logger.info(f"[DUPLICATE] {topic}")
            return True

    duplicate_cache[key] = now

    if len(duplicate_cache) > 5000:
        duplicate_cache.clear()

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

        logger.info(f"\n[ORCHESTRATOR] CYCLE {self.cycle} START")

        try:

            # =================================================
            # 1. CRAWL
            # =================================================
            raw = crawl() or []

            logger.info(f"[DEBUG] crawl: {len(raw)}")

            if not raw:
                raw = [{
                    "title": "fallback signal",
                    "content": "system fallback"
                }]

            # =================================================
            # 2. PROCESS (SAFE)
            # =================================================
            processed = process_data(raw) or raw

            logger.info(f"[DEBUG] processed: {len(processed)}")

            LAST_DATA["raw"] = processed[:100]

            # =================================================
            # 3. CRISIS DETECTION
            # =================================================
            crisis = detect_crisis_signals(processed) or []
            crisis_map = {
                str(c.get("title", "")).lower(): c
                for c in crisis
            }

            logger.info(f"[DEBUG] crisis: {len(crisis)}")

            # =================================================
            # 4. SIGNAL DETECTION (SAFE)
            # =================================================
            signals = detect_signals(processed) or []

            logger.info(f"[DEBUG] signals: {len(signals)}")

            # 🔥 HARD FALLBACK (CRITICAL FIX)
            if not signals:
                signals = [
                    {
                        "topic": x.get("title", "unknown"),
                        "score": 0.3
                    }
                    for x in processed[:20]
                ]

            # =================================================
            # 5. RANK + CLUSTER (SAFE)
            # =================================================
            signals = merge_ranked_signals(signals) or signals
            signals = cluster_signals(signals) or signals

            logger.info(f"[DEBUG] clustered: {len(signals)}")

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
            # 7. DECISION ENGINE (SAFE)
            # =================================================
            decisions = self.decision.evaluate(signals) or []

            if not decisions:
                decisions = [{
                    "publish": True,
                    "priority": 0.3
                }]

            logger.info(f"[DEBUG] decisions: {len(decisions)}")

            # =================================================
            # 8. INTELLIGENCE (SAFE)
            # =================================================
            intel = self.intelligence.run(decisions) or []

            if not intel:
                intel = [{
                    "topic": "system_active",
                    "narrative": {
                        "title": "System Running",
                        "content": "No strong signals detected"
                    }
                }]

            logger.info(f"[DEBUG] intelligence: {len(intel)}")

            # =================================================
            # 9. GENERATION
            # =================================================
            output = []

            for i, item in enumerate(intel):

                topic = str(item.get("topic", "")).strip()
                if not topic:
                    continue

                decision = decisions[i] if i < len(decisions) else {}

                if not decision.get("publish", True):
                    continue

                if is_duplicate(topic):
                    continue

                narrative = item.get("narrative") or {}

                payload = {
                    "title": narrative.get("title", topic[:80]),
                    "topic": topic,
                    "content": narrative.get("content", topic),
                    "priority": decision.get("priority", 0.5),
                    "published": True,
                    "timestamp": int(time.time())
                }

                save_signal(payload)
                output.append(payload)

                logger.info(f"[GENERATED] {topic}")

            # =================================================
            # FINAL OUTPUT GUARANTEE
            # =================================================
            logger.info(f"[DEBUG] output: {len(output)}")

            return output

        except Exception as e:
            traceback.print_exc()
            logger.error(f"[ORCHESTRATOR ERROR] {str(e)}")
            return []

        finally:
            logger.info(
                f"[ORCHESTRATOR] Cycle finished in {round(time.time() - start, 2)}s"
            )
