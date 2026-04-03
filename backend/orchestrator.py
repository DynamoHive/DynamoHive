import time
import traceback
import hashlib

from backend.logger import logger

# =========================
# SAFE IMPORT SYSTEM
# =========================
def safe_import(module_path, attr=None):
    try:
        module = __import__(module_path, fromlist=[attr] if attr else [])
        return getattr(module, attr) if attr else module
    except Exception as e:
        print(f"[IMPORT ERROR] {module_path}.{attr} -> {e}")
        return None


# =========================
# ENGINE IMPORTS (SAFE)
# =========================
crawl = safe_import("ai_engine.multi_crawler", "crawl")
process_data = safe_import("ai_engine.data_pipeline", "process_data")
signal_module = safe_import("ai_engine.signal_detector")

GlobalIntelligenceEngine = safe_import("ai_engine.global_intelligence_engine", "GlobalIntelligenceEngine")
update_trends = safe_import("ai_engine.predictive_engine", "update_trends")
generate_narrative = safe_import("ai_engine.narrative_engine", "generate_narrative")

register_event = safe_import("backend.events", "register_event")
detect_event_spikes = safe_import("backend.events", "detect_event_spikes")

get_user_profile = safe_import("backend.user_profile_engine", "get_user_profile")
compute_final_score = safe_import("backend.user_profile_engine", "compute_final_score")

save_post = safe_import("backend.storage", "save_post")
get_posts = safe_import("backend.storage", "get_posts")

distribute = safe_import("backend.distribution_engine", "distribute")

detect_anomalies = safe_import("ai_engine.anomaly_engine", "detect_anomalies")
compute_dominance = safe_import("ai_engine.dominance_engine", "compute_dominance")

MemoryPatternEngine = safe_import("ai_engine.memory_pattern_engine", "MemoryPatternEngine")
is_low_quality = safe_import("ai_engine.content_filter", "is_low_quality")

search_similar = safe_import("ai_engine.vector_memory", "search_similar")
store_vector = safe_import("ai_engine.vector_memory", "store_vector")


# =========================
# GLOBALS
# =========================
GLOBAL_DATA = []

intel_engine = GlobalIntelligenceEngine() if GlobalIntelligenceEngine else None
duplicate_cache = {}


# =========================
# DUPLICATE
# =========================
def is_duplicate_local(topic):
    try:
        topic = str(topic).lower().strip()
        h = hashlib.md5(topic.encode()).hexdigest()
    except:
        return False

    now = time.time()

    if h in duplicate_cache:
        if now - duplicate_cache[h] < 7200:
            return True

    duplicate_cache[h] = now
    return False


# =========================
# SIGNAL MERGE
# =========================
def merge_signals(signals):
    merged = {}

    for s in signals:
        topic = s.get("topic", "")
        if not topic:
            continue

        if topic not in merged:
            merged[topic] = s
        else:
            merged[topic]["score"] += s.get("score", 1.0)

    return list(merged.values())


# =========================
# ORCHESTRATOR
# =========================
class Orchestrator:

    def __init__(self):
        self.cycle_count = 0
        self.last_run = None
        self.last_duration = 0
        self.last_signal_count = 0
        self.last_event_count = 0
        self.last_anomalies = []
        self.last_dominance = []

        self.pattern_memory = MemoryPatternEngine() if MemoryPatternEngine else None

    def run_cycle(self):

        start = time.time()
        self.cycle_count += 1
        self.last_run = start

        logger.info(f"[ORCHESTRATOR] Cycle {self.cycle_count} started")

        try:

            # -------------------------
            # DATA
            # -------------------------
            raw_data = []
            try:
                if crawl:
                    raw_data = crawl()
            except Exception as e:
                logger.warning(f"[CRAWL ERROR] {e}")

            if not raw_data:
                try:
                    raw_data = get_posts() if get_posts else []
                except:
                    raw_data = []

            if not raw_data:
                raw_data = [{"text": "bootstrap signal"}]

            try:
                if process_data:
                    raw_data = process_data(raw_data)
            except Exception as e:
                logger.warning(f"[PIPELINE ERROR] {e}")

            GLOBAL_DATA.clear()
            GLOBAL_DATA.extend(raw_data[:100])

            # -------------------------
            # SIGNAL
            # -------------------------
            signals = []
            try:
                if signal_module and hasattr(signal_module, "detect_signals"):
                    signals = signal_module.detect_signals(raw_data)
            except Exception as e:
                logger.warning(f"[SIGNAL ERROR] {e}")

            if not signals:
                for item in raw_data[:20]:
                    text = item.get("title") or item.get("text")
                    if text:
                        signals.append({"topic": text, "score": 1.0})

            signals = merge_signals(signals)

            # -------------------------
            # NORMALIZE
            # -------------------------
            normalized = []
            for s in signals:

                topic = str(
                    s.get("topic")
                    or s.get("text")
                    or s.get("title")
                    or ""
                ).strip()

                if len(topic) < 5:
                    continue

                normalized.append({
                    "topic": topic,
                    "score": float(s.get("score", 1.0))
                })

            signals = normalized
            self.last_signal_count = len(signals)

            # -------------------------
            # EVENTS
            # -------------------------
            if register_event:
                for s in signals:
                    try:
                        register_event(s["topic"])
                    except:
                        pass

            events = []
            if detect_event_spikes:
                try:
                    events = detect_event_spikes()
                except:
                    events = []

            self.last_event_count = len(events)

            # -------------------------
            # PERSONALIZATION
            # -------------------------
            profile = {}
            if get_user_profile:
                try:
                    profile = get_user_profile("global_user")
                except:
                    profile = {}

            if compute_final_score:
                for s in signals:
                    try:
                        s["score"] = compute_final_score(s, profile)
                    except:
                        pass

            # -------------------------
            # ANOMALY + DOMINANCE
            # -------------------------
            try:
                if detect_anomalies:
                    self.last_anomalies = detect_anomalies(signals, events)
            except Exception as e:
                logger.warning(f"[ANOMALY ERROR] {e}")

            try:
                if compute_dominance:
                    self.last_dominance = compute_dominance(signals)
            except Exception as e:
                logger.warning(f"[DOMINANCE ERROR] {e}")

            # -------------------------
            # INTELLIGENCE
            # -------------------------
            intelligence = signals

            try:
                if intel_engine:
                    intelligence = intel_engine.process(intelligence)
            except Exception as e:
                logger.warning(f"[INTEL ERROR] {e}")

            try:
                if update_trends:
                    update_trends(intelligence)
            except Exception as e:
                logger.warning(f"[PREDICT ERROR] {e}")

            # -------------------------
            # CONTENT
            # -------------------------
            self._generate_content(intelligence)

        except Exception:
            traceback.print_exc()

        finally:
            duration = round(time.time() - start, 2)
            self.last_duration = duration
            logger.info(f"[ORCHESTRATOR] Cycle finished in {duration}s")

    # -------------------------
    # CONTENT
    # -------------------------
    def _generate_content(self, intelligence):

        for intel in intelligence:

            topic = str(intel.get("topic", "")).strip()

            if not topic or len(topic) < 5:
                continue

            if is_duplicate_local(topic):
                continue

            if self.pattern_memory and self.pattern_memory.seen_before(topic):
                continue

            if search_similar:
                try:
                    similar = search_similar(topic)
                    if similar and similar[0].get("score", 0) > 0.92:
                        continue
                except:
                    pass

            # SAFE NARRATIVE
            try:
                if generate_narrative:
                    content = generate_narrative(intel)
                else:
                    content = {"title": topic, "content": topic}
            except Exception as e:
                logger.warning(f"[NARRATIVE ERROR] {e}")
                content = {"title": topic, "content": topic}

            if not content:
                continue

            title = content.get("title")
            body = content.get("content")

            if not title or not body:
                continue

            if is_low_quality:
                try:
                    if is_low_quality(body):
                        continue
                except:
                    pass

            if len(body) < 80:
                continue

            if save_post:
                try:
                    save_post(title, body)
                except:
                    logger.warning("[SAVE ERROR]")
                    continue

            if self.pattern_memory:
                try:
                    self.pattern_memory.store(topic)
                except:
                    pass

            if store_vector:
                try:
                    store_vector(content)
                except:
                    logger.warning("[VECTOR ERROR]")

            if distribute:
                try:
                    distribute(content)
                except:
                    logger.warning("[DISTRIBUTION ERROR]")

            logger.info(f"[ORCHESTRATOR] GENERATED: {topic}")

    # -------------------------
    # STATUS
    # -------------------------
    def get_status(self):
        return {
            "cycle_count": self.cycle_count,
            "last_run": self.last_run,
            "last_duration": self.last_duration,
            "last_signal_count": self.last_signal_count,
            "last_event_count": self.last_event_count,
            "anomalies": self.last_anomalies,
            "dominance": self.last_dominance[:5] if self.last_dominance else []
        }
