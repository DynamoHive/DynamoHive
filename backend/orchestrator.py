import time
import traceback
import hashlib

from backend.logger import logger

# -------------------------
# SAFE IMPORTS
# -------------------------

try:
    from ai_engine.multi_crawler import crawl
except:
    def crawl(): return []

try:
    from ai_engine.data_pipeline import process_data
except:
    def process_data(x): return x

try:
    from ai_engine.signal_detector import detect_signals
except:
    def detect_signals(x): return []

try:
    from ai_engine.intelligence_layer import enrich_intelligence
except:
    def enrich_intelligence(x): return x

try:
    from ai_engine.power_mapping_engine import map_power
except:
    def map_power(x): return {}

try:
    from backend.user_profile_engine import get_user_profile, compute_final_score
except:
    def get_user_profile(*a, **k): return {}
    def compute_final_score(s, p): return s.get("score", 1.0)

try:
    from backend.storage import save_post
except:
    def save_post(*a, **k): pass

try:
    from backend.distribution_engine import distribute
except:
    def distribute(*a, **k): pass

try:
    from ai_engine.memory_pattern_engine import MemoryPatternEngine
except:
    class MemoryPatternEngine:
        def __init__(self):
            self.memory = set()
        def seen_before(self, x): return False
        def store(self, x): pass
        def pattern_score(self, x): return 0

try:
    from ai_engine.content_filter import is_low_quality
except:
    def is_low_quality(x): return False

try:
    from ai_engine.vector_memory import search_similar, store_vector
except:
    def search_similar(*a, **k): return []
    def store_vector(*a, **k): pass

try:
    from ai_engine.narrative_engine import generate_narrative
except:
    generate_narrative = None


# -------------------------
# GLOBAL FALLBACK STORAGE
# -------------------------

LAST_DATA = []
duplicate_cache = {}


def is_duplicate(topic):
    try:
        h = hashlib.md5(topic.lower().encode()).hexdigest()
    except:
        return False

    now = time.time()

    if h in duplicate_cache and now - duplicate_cache[h] < 3600:
        return True

    duplicate_cache[h] = now
    return False


# -------------------------
# SAFE GENERATE
# -------------------------

def safe_generate(intel):

    if generate_narrative:
        try:
            c = generate_narrative(intel)
            if c and c.get("title") and c.get("content"):
                return c
        except:
            pass

    topic = str(intel.get("topic", ""))

    return {
        "title": topic[:80],
        "content": f"{topic} is emerging as a significant global signal."
    }


# -------------------------
# FORCE SIGNAL
# -------------------------

def force_signals(raw):
    out = []
    for item in raw[:5]:
        text = item.get("title") or item.get("text")
        if text:
            out.append({
                "topic": text,
                "score": 1.0
            })
    return out


# -------------------------
# ORCHESTRATOR
# -------------------------

class Orchestrator:

    def __init__(self):
        self.cycle = 0
        self.memory = MemoryPatternEngine()

    def run_cycle(self):

        start = time.time()
        self.cycle += 1

        logger.info(f"[ORCHESTRATOR] Cycle {self.cycle} started")

        try:
            # -------------------------
            # 1. DATA
            # -------------------------
            raw = crawl()

            if not raw:
                if LAST_DATA:
                    logger.warning("[ORCHESTRATOR] Using LAST_DATA")
                    raw = LAST_DATA
                else:
                    logger.warning("[ORCHESTRATOR] No data → fallback")
                    raw = [{"title": "global fallback signal"}]

            raw = process_data(raw)

            LAST_DATA.clear()
            LAST_DATA.extend(raw[:100])

            # -------------------------
            # 2. SIGNALS
            # -------------------------
            signals = detect_signals(raw)

            if not signals:
                logger.warning("[ORCHESTRATOR] No signals → forcing")
                signals = force_signals(raw)

            # -------------------------
            # 3. PERSONALIZATION
            # -------------------------
            profile = get_user_profile("global_user")

            for s in signals:
                try:
                    s["score"] = compute_final_score(s, profile)
                except:
                    pass

            # -------------------------
            # 4. INTELLIGENCE
            # -------------------------
            intel = enrich_intelligence(signals)

            enriched = []
            for i in intel:
                try:
                    i["power"] = map_power(i)
                except:
                    i["power"] = {}
                enriched.append(i)

            # -------------------------
            # 5. GENERATE
            # -------------------------
            self._generate(enriched)

        except Exception:
            traceback.print_exc()

        finally:
            duration = round(time.time() - start, 2)
            logger.info(f"[ORCHESTRATOR] Cycle finished in {duration}s")

    # -------------------------
    # GENERATION
    # -------------------------

    def _generate(self, items):

        generated = 0
        MAX_POSTS = 5

        for intel in items:

            if generated >= MAX_POSTS:
                break

            topic = str(intel.get("topic", "")).strip()

            if len(topic) < 5:
                continue

            if is_duplicate(topic):
                continue

            if self.memory.seen_before(topic):
                continue

            # pattern check
            try:
                if self.memory.pattern_score(topic) > 3:
                    continue
            except:
                pass

            # semantic duplicate
            try:
                sims = search_similar(topic)
                if sims and sims[0].get("score", 0) > 0.95:
                    continue
            except:
                pass

            content = safe_generate(intel)

            title = content.get("title")
            body = content.get("content")

            if not title or not body:
                continue

            if is_low_quality(body):
                continue

            if len(body) < 40:
                body += "."

            try:
                save_post(title, body)
            except:
                continue

            try:
                store_vector(content)
            except:
                pass

            try:
                distribute(content)
            except:
                pass

            self.memory.store(topic)
            generated += 1

            logger.info(f"[ORCHESTRATOR] GENERATED: {topic}")

        # 🔥 HARD FAIL SAFE
        if generated == 0:
            topic = "forced fallback signal"
            try:
                save_post(topic, topic)
            except:
                pass

            logger.warning("[ORCHESTRATOR] GENERATED (FORCED)")
