import time
import traceback
import hashlib

from backend.logger import logger

from ai_engine.multi_crawler import crawl
from ai_engine.data_pipeline import process_data
from ai_engine.signal_detector import detect_signals
from ai_engine.signal_ranking_engine import merge_ranked_signals

from ai_engine.global_intelligence_engine import GlobalIntelligenceEngine
from ai_engine.decision_engine import DecisionEngine
from ai_engine.signal_cluster import cluster_signals
from ai_engine.global_crisis_radar import detect_crisis_signals

from backend.storage import save_post


# =====================================================
# MEMORY
# =====================================================

LAST_DATA = []
duplicate_cache = {}


# =====================================================
# DUPLICATE CONTROL
# =====================================================

def is_duplicate(topic):

    try:

        time_bucket = int(time.time() / 300)

        h = hashlib.md5(
            (
                str(topic).lower() + str(time_bucket)
            ).encode()
        ).hexdigest()

    except Exception:

        return False

    now = time.time()

    if h in duplicate_cache:

        if now - duplicate_cache[h] < 300:
            return True

    duplicate_cache[h] = now

    return False


# =====================================================
# ORCHESTRATOR
# =====================================================

class Orchestrator:

    def __init__(self):

        self.cycle = 0

        self.intelligence = GlobalIntelligenceEngine()
        self.decision = DecisionEngine()

    # =================================================
    # MAIN LOOP
    # =================================================

    def run_cycle(self):

        start = time.time()

        self.cycle += 1

        logger.info(
            f"[ORCHESTRATOR] Cycle {self.cycle} started"
        )

        try:

            # -------------------------------------------------
            # 1. CRAWL
            # -------------------------------------------------

            raw = crawl()

            print(
                f"crawler collected: "
                f"{len(raw) if raw else 0}"
            )

            # fallback
            if not raw:

                raw = LAST_DATA or [
                    {
                        "title": "fallback signal",
                        "content": "fallback"
                    }
                ]

            # -------------------------------------------------
            # 2. PROCESS
            # -------------------------------------------------

            raw = process_data(raw)

            print(
                f"pipeline processed: "
                f"{len(raw) if raw else 0}"
            )

            if not raw:

                logger.warning(
                    "[ORCHESTRATOR] No processed data"
                )

                return []

            # cache
            LAST_DATA.clear()
            LAST_DATA.extend(raw[:100])

            # -------------------------------------------------
            # 3. CRISIS DETECTION
            # -------------------------------------------------

            crisis_signals = detect_crisis_signals(raw)

            print(
                f"CRISIS SIGNALS: "
                f"{len(crisis_signals)}"
            )

            crisis_map = {}

            for c in crisis_signals:

                key = str(
                    c.get("title", "")
                ).lower()

                crisis_map[key] = c

            # -------------------------------------------------
            # 4. SIGNAL DETECTION
            # -------------------------------------------------

            signals = detect_signals(raw)

            print(
                f"signals detected: "
                f"{len(signals) if signals else 0}"
            )

            # fallback signals
            if not signals:

                signals = []

                for x in raw[:10]:

                    signals.append({
                        "topic": str(
                            x.get("title") or "fallback"
                        ),
                        "score": 0.5
                    })

            # -------------------------------------------------
            # 5. RANKING
            # -------------------------------------------------

            signals = merge_ranked_signals(signals)

            if not signals:

                logger.warning(
                    "[ORCHESTRATOR] Ranking failed"
                )

                return []

            # -------------------------------------------------
            # 6. CLUSTERING
            # -------------------------------------------------

            signals = cluster_signals(signals)

            if not signals:

                logger.warning(
                    "[ORCHESTRATOR] No signals after clustering"
                )

                return []

            # -------------------------------------------------
            # 7. CRISIS BOOST
            # -------------------------------------------------

            for s in signals:

                topic = str(
                    s.get("topic", "")
                ).lower()

                if topic in crisis_map:

                    crisis = crisis_map[topic]

                    s["urgency"] = crisis.get(
                        "urgency",
                        "high"
                    )

                    s["score"] = min(
                        s.get("score", 0.5) + 0.3,
                        1.0
                    )

            # -------------------------------------------------
            # 8. DECISION ENGINE
            # -------------------------------------------------

            decisions = self.decision.evaluate(signals)

            if not decisions:

                logger.warning(
                    "[ORCHESTRATOR] No decisions"
                )

                return []

            # -------------------------------------------------
            # 9. INTELLIGENCE ENGINE
            # -------------------------------------------------

            intel_items = self.intelligence.run(decisions)

            if not intel_items:

                logger.warning(
                    "[ORCHESTRATOR] No intelligence output"
                )

                return []

            print(
                f"INTEL OUTPUT COUNT: "
                f"{len(intel_items)}"
            )

            # -------------------------------------------------
            # 10. DECISION MERGE
            # -------------------------------------------------

            for i, item in enumerate(intel_items):

                if i < len(decisions):

                    item["decision"] = decisions[i].get(
                        "decision",
                        {}
                    )

            # -------------------------------------------------
            # 11. GENERATION
            # -------------------------------------------------

            generated = 0

            final_output = []

            for item in intel_items:

                try:

                    topic = str(
                        item.get("topic") or ""
                    ).strip()

                    if not topic:
                        continue

                    print(f"PROCESSING: {topic}")

                    decision = item.get("decision", {})

                    publish = decision.get(
                        "publish",
                        True
                    )

                    if not publish:

                        print(f"SKIPPED: {topic}")

                        continue

                    if is_duplicate(topic):

                        print(f"DUPLICATE: {topic}")

                        continue

                    narrative = item.get(
                        "narrative",
                        {}
                    )

                    title = narrative.get(
                        "title",
                        topic[:80]
                    )

                    content = narrative.get(
                        "content",
                        topic
                    )

                    print(f"GENERATING: {title}")

                    # SAVE
                    save_post(title, content)

                    generated += 1

                    # FRONTEND OUTPUT
                    final_output.append({

                        "title": title,

                        "topic": topic,

                        "content": content,

                        "priority": decision.get(
                            "priority",
                            0.5
                        ),

                        "published": True,

                        "timestamp": int(time.time())
                    })

                    logger.info(
                        f"[GENERATED] "
                        f"{topic} | "
                        f"priority="
                        f"{decision.get('priority', 'N/A')}"
                    )

                except Exception as e:

                    print("GEN ERROR:", e)

                    continue

            # -------------------------------------------------
            # 12. EMPTY FALLBACK
            # -------------------------------------------------

            if generated == 0:

                logger.warning(
                    "[ORCHESTRATOR] NOTHING GENERATED"
                )

                # fallback output
                for item in intel_items[:10]:

                    final_output.append({

                        "title": item.get(
                            "topic",
                            "signal"
                        ),

                        "topic": item.get(
                            "topic",
                            "signal"
                        ),

                        "content": str(item),

                        "priority": 0.1,

                        "published": False,

                        "timestamp": int(time.time())
                    })

            print(
                f"GENERATED COUNT: {generated}"
            )

            print(
                f"RETURNING: {len(final_output)} items"
            )

            # =================================================
            # RETURN FIX
            # =================================================

            return final_output

        except Exception:

            traceback.print_exc()

            return []

        finally:

            duration = round(
                time.time() - start,
                2
            )

            logger.info(
                f"[ORCHESTRATOR] "
                f"Cycle finished in {duration}s"
            )
