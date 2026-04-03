from collections import defaultdict
import math

# -------------------------
# CONFIG
# -------------------------

STOPWORDS = {
    "the","and","for","with","that","this","from","are","was","were",
    "has","have","had","but","not","you","your","about","into","over",
    "after","before","between","will","would","could","should"
}

BAD_PATTERNS = {
    "more","there","first","time","very","just",
    "some","many","such","than","also"
}

MIN_COUNT = 2
MIN_SCORE = 1.5
SIM_THRESHOLD = 0.55


# -------------------------
# HELPERS
# -------------------------

def normalize(text):
    try:
        return str(text).lower().strip()
    except:
        return ""


def safe_float(x, default=0.0):
    try:
        return float(x)
    except:
        return default


# -------------------------
# 🔥 STRONG MEANING FILTER
# -------------------------

def is_meaningful(phrase):

    words = phrase.split()

    if len(words) < 2:
        return False

    # stopword yoğunluğu
    if sum(w in STOPWORDS for w in words) > len(words) / 2:
        return False

    # kısa kelime spam
    if any(len(w) <= 3 for w in words):
        return False

    # en az 2 güçlü kelime
    if sum(len(w) >= 5 for w in words) < 2:
        return False

    # kötü pattern
    if any(w in BAD_PATTERNS for w in words):
        return False

    return True


# -------------------------
# 🔥 SIMILARITY
# -------------------------

def similarity(a, b):

    a_words = set(a.split())
    b_words = set(b.split())

    if not a_words or not b_words:
        return 0

    return len(a_words & b_words) / len(a_words | b_words)


# -------------------------
# 🔥 CLUSTER MERGE
# -------------------------

def merge_topics(counter, scores, texts):

    clusters = []

    for kw in counter:

        best = None
        best_score = 0

        for c in clusters:
            sim = similarity(c["topic"], kw)

            if sim > SIM_THRESHOLD and sim > best_score:
                best = c
                best_score = sim

        if best:
            best["count"] += counter[kw]
            best["score"] += scores[kw]
            best["samples"].extend(texts[kw])
        else:
            clusters.append({
                "topic": kw,
                "count": counter[kw],
                "score": scores[kw],
                "samples": texts[kw][:]
            })

    return clusters


# -------------------------
# 🔥 CONTEXT EXTRACTION (CRITICAL)
# -------------------------

def extract_phrases(words):

    phrases = []

    # 3 kelimelik çekirdek
    if len(words) >= 3:
        phrases.append(" ".join(words[:3]))

    # 5 kelimelik geniş context
    if len(words) >= 5:
        phrases.append(" ".join(words[:5]))

    # fallback
    if not phrases:
        phrases = [" ".join(words[:3])]

    return phrases


# -------------------------
# 🔥 MAIN ENGINE
# -------------------------

def detect_signals(analysis):

    if not analysis or not isinstance(analysis, list):
        print("signals detected: 0")
        return []

    keyword_counter = defaultdict(int)
    keyword_scores = defaultdict(float)
    keyword_texts = defaultdict(list)

    # -------------------------
    # COLLECT
    # -------------------------

    for item in analysis:

        if not isinstance(item, dict):
            continue

        text = normalize(item.get("text") or item.get("title") or "")
        score = safe_float(item.get("score", 1))

        if not text:
            continue

        words = [
            w for w in text.split()
            if len(w) > 3 and w not in STOPWORDS
        ]

        if not words:
            continue

        phrases = extract_phrases(words)

        for kw in phrases:

            kw = normalize(kw)

            if len(kw) < 6:
                continue

            # HARD spam kes
            if kw.startswith(("there","more","first","new")):
                continue

            if not is_meaningful(kw):
                continue

            keyword_counter[kw] += 1
            keyword_scores[kw] += score
            keyword_texts[kw].append(text)

    # -------------------------
    # CLUSTER
    # -------------------------

    clusters = merge_topics(
        keyword_counter,
        keyword_scores,
        keyword_texts
    )

    # -------------------------
    # BUILD SIGNALS
    # -------------------------

    signals = []

    for c in clusters:

        count = c["count"]
        total_score = c["score"]

        if count < MIN_COUNT and total_score < MIN_SCORE:
            continue

        avg_score = total_score / count
        boost = int(math.log1p(count) * 5)

        signals.append({
            "topic": c["topic"],
            "keywords": c["topic"].split(),
            "count": count,
            "score": round(avg_score, 2),
            "boost": max(1, boost),
            "samples": list(set(c["samples"]))[:3]
        })

    # -------------------------
    # FALLBACK
    # -------------------------

    if len(signals) == 0:

        for item in analysis[:10]:

            text = normalize(item.get("text") or item.get("title") or "")

            if not text:
                continue

            signals.append({
                "topic": text,
                "keywords": text.split()[:5],
                "count": 1,
                "score": 1.0,
                "boost": 1,
                "samples": [text]
            })

    # -------------------------
    # SORT
    # -------------------------

    signals.sort(
        key=lambda x: (x["boost"], x["score"], x["count"]),
        reverse=True
    )

    print("signals detected:", len(signals))

    return signals
