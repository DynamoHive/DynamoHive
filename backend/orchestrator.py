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
        def seen_before(self, *a, **k): return False
        def store(self, *a, **k): pass

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
# DUPLICATE CACHE
# -------------------------

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
# SAFE GENERATION
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
        "content": f"{topic} is emerging as a relevant global signal."
    }


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
                logger.warning("[ORCHESTRATOR] No data from crawler")
                return

            raw = process_data(raw)

            # -------------------------
            # 2. SIGNALS
            # -------------------------
            signals = detect_signals(raw)

            if not signals:
                logger.warning("[ORCHESTRATOR] No signals detected")
                return

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
            # 4. GENERATE
            # -------------------------
            self._generate(signals)

        except Exception:
            traceback.print_exc()

        finally:
            duration = round(time.time() - start, 2)
            logger.info(f"[ORCHESTRATOR] Cycle finished in {duration}s")

    # -------------------------
    # GENERATION ENGINE
    # -------------------------

    def _generate(self, signals):

        generated = 0
        MAX_POSTS = 5

        for intel in signals:

            if generated >= MAX_POSTS:
                break

            topic = str(intel.get("topic", "")).strip()

            if len(topic) < 5:
                continue

            if is_duplicate(topic):
                continue

            if self.memory.seen_before(topic):
                continue

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

        if generated == 0:
            logger.warning("[ORCHESTRATOR] Nothing generated")
