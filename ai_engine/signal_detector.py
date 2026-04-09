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
        score = float(count) * 2

        strong = [
            "war", "attack", "crisis", "collapse",
            "ai", "nuclear", "sanction", "conflict"
        ]

        if any(w in t for w in strong):
            score += 3

        return score

    except:
        return float(count or 1)


def detect_signals(analysis):

    try:
        if not isinstance(analysis, list) or not analysis:
            print("signals detected: 0")
            return []

        counter = defaultdict(int)
        seen = set()

        for item in analysis:

            try:
                if not isinstance(item, dict):
                    continue

                raw = item.get("title") or item.get("text") or item.get("topic") or ""
                raw = str(raw).strip()

                if not raw:
                    continue

                text = normalize(raw)

                if not text or text in seen:
                    continue

                seen.add(text)

                topic = raw[:120]
                counter[topic] += 1

            except:
                continue

        signals = []

        for topic, count in counter.items():

            try:
                if not topic:
                    continue

                score = compute_score(topic, count)

                signals.append({
                    "topic": topic,
                    "title": topic,   # 🔥 EKLENDİ (GLOBAL UYUMLULUK)
                    "score": score,
                    "count": count
                })

            except:
                continue

        # 🔥 HARD FALLBACK (ASLA BOŞ DÖNME)
        if not signals:

            for item in analysis[:10]:

                try:
                    raw = item.get("title") or item.get("text") or ""

                    if not raw:
                        continue

                    raw = str(raw).strip()

                    signals.append({
                        "topic": raw[:120],
                        "title": raw[:120],
                        "score": 1.0,
                        "count": 1
                    })

                except:
                    continue

        # 🔥 SON GARANTİ
        if not signals:
            signals = [{
                "topic": "fallback signal",
                "title": "fallback signal",
                "score": 1.0,
                "count": 1
            }]

        signals.sort(key=lambda x: x.get("score", 0), reverse=True)

        print("signals detected:", len(signals))

        return signals

    except:
        # 🔥 FULL FAILSAFE
        return [{
            "topic": "fallback signal",
            "title": "fallback signal",
            "score": 1.0,
            "count": 1
        }]
