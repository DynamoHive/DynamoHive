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
    "more", "there", "first", "time", "very", "just",
    "some", "many", "such", "than", "also"
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
# 🔥 SEMANTIC FILTER
# -------------------------

def is_meaningful(phrase):

    words = phrase.split()

    if len(words) < 2:
        return False

    if any(w in BAD_PATTERNS for w in words):
        return False

    if sum(len(w) >= 5 for w in words) < 1:
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
# 🔥 CLUSTER MERGE (OPTIMIZED)
# -------------------------

def merge_topics(counter, scores, texts):

    clusters = []

    for kw in counter:

        best_match = None
        best_score = 0

        for cluster in clusters:
            sim = similarity(cluster["topic"], kw)

            if sim > SIM_THRESHOLD and sim > best_score:
                best_match = cluster
                best_score = sim

        if best_match:
            best_match["count"] += counter[kw]
            best_match["score"] += scores[kw]
            best_match["samples"].extend(texts[kw])
        else:
            clusters.append({
                "topic": kw,
                "count": counter[kw],
                "score": scores[kw],
                "samples": texts[kw][:]
            })

    return clusters


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
    # 1. COLLECT
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

        phrases = []

        # BIGRAM
        for i in range(len(words) - 1):
            phrases.append(words[i] + " " + words[i+1])

        # TRIGRAM
        for i in range(len(words) - 2):
            phrases.append(words[i] + " " + words[i+1] + " " + words[i+2])

        keywords = phrases[:25] if phrases else words[:12]

        for kw in keywords:

            kw = normalize(kw)

            if len(kw) < 5:
                continue

            if not is_meaningful(kw):
                continue

            keyword_counter[kw] += 1
            keyword_scores[kw] += score
            keyword_texts[kw].append(text)

    # -------------------------
    # 2. CLUSTER
    # -------------------------

    clusters = merge_topics(
        keyword_counter,
        keyword_scores,
        keyword_texts
    )

    # -------------------------
    # 3. BUILD SIGNALS
    # -------------------------

    signals = []

    for c in clusters:

        count = c["count"]
        total_score = c["score"]

        if count < MIN_COUNT and total_score < MIN_SCORE:
            continue

        avg_score = total_score / count

        # 🔥 SMART BOOST (non-linear)
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
    # 4. HARD FALLBACK
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
    # 5. FINAL SORT
    # -------------------------

    signals.sort(
        key=lambda x: (x["boost"], x["score"], x["count"]),
        reverse=True
    )

    print("signals detected:", len(signals))

    return signals
