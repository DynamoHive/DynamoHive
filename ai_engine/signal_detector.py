from collections import defaultdict
import math
import re

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
    "some","many","such","than","also","new"
}

MIN_COUNT = 2
MIN_SCORE = 1.5
SIM_THRESHOLD = 0.65


# -------------------------
# HELPERS
# -------------------------

def normalize(text):
    try:
        text = str(text).lower()

        # html/artifacts temizle
        text = text.replace("…", " ")
        text = text.replace("8230", " ")

        # punctuation temizle
        text = re.sub(r"[^\w\s]", " ", text)

        # fazla boşluk temizle
        text = re.sub(r"\s+", " ", text)

        return text.strip()
    except:
        return ""


def safe_float(x, default=0.0):
    try:
        return float(x)
    except:
        return default


# -------------------------
# 🔥 MEANING FILTER (GÜÇLÜ)
# -------------------------

def is_meaningful(phrase):

    words = phrase.split()

    if len(words) < 3:
        return False

    # çok kısa kelime varsa direkt çöpe
    if any(len(w) <= 3 for w in words):
        return False

    # kötü pattern varsa çöpe
    if any(w in BAD_PATTERNS for w in words):
        return False

    # en az 2 güçlü kelime şart
    strong = [w for w in words if len(w) >= 5]

    if len(strong) < 2:
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
# 🔥 SMART PHRASE EXTRACTION (DAHA TEMİZ)
# -------------------------

def extract_phrases(words):

    phrases = []

    # sadece 3 ve 4 kelimelik phrase kullan (noise azaltıldı)
    for i in range(len(words)):

        chunk3 = words[i:i+3]
        chunk4 = words[i:i+4]

        if len(chunk3) == 3:
            phrases.append(" ".join(chunk3))

        if len(chunk4) == 4:
            phrases.append(" ".join(chunk4))

    return phrases


# -------------------------
# 🔥 CLUSTER MERGE (DAHA AGRESİF)
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

            # daha temiz ve uzun olanı seç
            if len(kw.split()) > len(best["topic"].split()):
                best["topic"] = kw

        else:
            clusters.append({
                "topic": kw,
                "count": counter[kw],
                "score": scores[kw],
                "samples": texts[kw][:]
            })

    return clusters


# -------------------------
# 🔥 MAIN ENGINE (TEMİZ AKIŞ)
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

        # 🔥 minimum kalite
        if len(words) < 4:
            continue

        phrases = extract_phrases(words)

        for kw in phrases:

            # 🔥 çok kısa phrase yok
            if len(kw.split()) < 3:
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

        boost = int(math.log1p(count) * 6)

        signals.append({
            "topic": c["topic"],
            "keywords": c["topic"].split(),
            "count": count,
            "score": round(avg_score, 2),
            "boost": max(1, boost),
            "samples": list(set(c["samples"]))[:3]
        })

    # -------------------------
    # FALLBACK (TEMİZ)
    # -------------------------

    if len(signals) == 0:

        for item in analysis[:10]:

            text = normalize(item.get("text") or item.get("title") or "")

            if not text:
                continue

            words = [w for w in text.split() if len(w) > 4]

            if len(words) < 3:
                continue

            topic = " ".join(words[:6])

            signals.append({
                "topic": topic,
                "keywords": topic.split(),
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
