from collections import defaultdict
import re


def normalize(text):
    try:
        text = str(text).lower()
        text = re.sub(r"[^\w\s]", " ", text)
        text = re.sub(r"\s+", " ", text)
        return text.strip()
    except:
        return ""


def compute_score(text, count):

    try:
        t = str(text).lower()

        base = float(count) * 2.0

        strong_signals = {
            "war": 3,
            "attack": 3,
            "crisis": 3,
            "collapse": 2.5,
            "nuclear": 3.5,
            "sanction": 2,
            "conflict": 2.5,
            "ai": 1.5
        }

        boost = 0

        for k, v in strong_signals.items():
            if k in t:
                boost = max(boost, v)

        return base + boost

    except:
        return float(count or 1)


def detect_signals(analysis):

    try:
        if not isinstance(analysis, list) or not analysis:
            return []

        counter = defaultdict(int)
        seen = set()

        # ----------------------------
        # 1. NORMALIZE + GROUP
        # ----------------------------
        for item in analysis:

            if not isinstance(item, dict):
                continue

            raw = (
                item.get("title")
                or item.get("text")
                or item.get("topic")
                or ""
            )

            raw = str(raw).strip()
            if not raw:
                continue

            norm = normalize(raw)

            if not norm or norm in seen:
                continue

            seen.add(norm)

            topic = raw[:140]
            counter[topic] += 1

        # ----------------------------
        # 2. BUILD SIGNALS
        # ----------------------------
        signals = []

        for topic, count in counter.items():

            if not topic:
                continue

            score = compute_score(topic, count)

            signals.append({
                "topic": topic,
                "title": topic,
                "score": round(score, 3),
                "count": count,
                "confidence": min(1.0, count / 10)
            })

        # ----------------------------
        # 3. FALLBACK SAFETY
        # ----------------------------
        if not signals:

            signals = []

            for item in analysis[:10]:

                raw = item.get("title") or item.get("text") or "fallback"

                signals.append({
                    "topic": raw[:140],
                    "title": raw[:140],
                    "score": 1.0,
                    "count": 1,
                    "confidence": 0.3
                })

        # ----------------------------
        # 4. FINAL GUARANTEE
        # ----------------------------
        if not signals:
            return [{
                "topic": "fallback signal",
                "title": "fallback signal",
                "score": 1.0,
                "count": 1,
                "confidence": 0.1
            }]

        signals.sort(key=lambda x: x["score"], reverse=True)

        return signals

    except:
        return [{
            "topic": "fallback signal",
            "title": "fallback signal",
            "score": 1.0,
            "count": 1,
            "confidence": 0.1
        }]
