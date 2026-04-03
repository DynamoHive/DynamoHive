from collections import defaultdict
import time


WINDOW = 3600


STOPWORDS = {
    "the","and","for","with","that","this","from","are","was","were",
    "has","have","had","but","not","you","your","about","into","over",
    "after","before","between","will","would","could","should"
}


def normalize(text):
    try:
        text = str(text).lower().strip()

        # 🔥 EXTRA CLEAN
        text = text.replace("’", "").replace("'", "")

        return text
    except:
        return ""


def safe_float(x, default=0.0):
    try:
        return float(x)
    except:
        return default


# -------------------------
# 🔥 SIMILARITY (CLUSTER CORE)
# -------------------------
def similarity(a, b):

    a_words = set(a.split())
    b_words = set(b.split())

    if not a_words or not b_words:
        return 0

    inter = len(a_words & b_words)
    union = len(a_words | b_words)

    return inter / union


# -------------------------
# 🔥 CLUSTER MERGE
# -------------------------
def merge_topics(keyword_counter, keyword_scores, keyword_texts):

    clusters = []

    for kw in keyword_counter:

        added = False

        for cluster in clusters:

            # 🔥 FIXED THRESHOLD
            if similarity(cluster["topic"], kw) > 0.45:
                cluster["count"] += keyword_counter[kw]
                cluster["score"] += keyword_scores[kw]
                cluster["samples"].extend(keyword_texts[kw])
                added = True
                break

        if not added:
            clusters.append({
                "topic": kw,
                "count": keyword_counter[kw],
                "score": keyword_scores[kw],
                "samples": keyword_texts[kw][:]
            })

    return clusters


# -------------------------
# 🔥 MAIN
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

        phrases = []

        # BIGRAM
        for i in range(len(words) - 1):
            phrases.append(words[i] + " " + words[i+1])

        # TRIGRAM
        for i in range(len(words) - 2):
            phrases.append(words[i] + " " + words[i+1] + " " + words[i+2])

        keywords = phrases[:20] if phrases else words[:10]

        for kw in keywords:
            kw = normalize(kw)

            if not kw or len(kw) < 4:
                continue

            keyword_counter[kw] += 1
            keyword_scores[kw] += score
            keyword_texts[kw].append(text)

    # -------------------------
    # 2. CLUSTERING
    # -------------------------
    clusters = merge_topics(keyword_counter, keyword_scores, keyword_texts)

    # -------------------------
    # 3. BUILD SIGNALS
    # -------------------------
    signals = []

    for c in clusters:

        count = c["count"]
        total_score = c["score"]

        # 🔥 SOFT THRESHOLD
        if count < 2 and total_score < 2:
            continue

        avg_score = total_score / count

        signals.append({
            "topic": c["topic"],
            "keywords": c["topic"].split(),
            "count": count,
            "score": round(avg_score, 2),
            "boost": max(1, count * 2),
            "samples": c["samples"][:3]
        })

    # -------------------------
    # 4. FALLBACK
    # -------------------------
    if len(signals) <= 2:

        signals = []

        for item in analysis:

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
    # 5. SORT
    # -------------------------
    signals.sort(
        key=lambda x: (x.get("count", 0), x.get("score", 0)),
        reverse=True
    )

    print("signals detected:", len(signals))

    return signals
