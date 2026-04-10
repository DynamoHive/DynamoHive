import hashlib
from collections import defaultdict


def normalize(text):
    return text.lower().strip()


def simple_similarity(a, b):
    a_words = set(a.split())
    b_words = set(b.split())
    return len(a_words & b_words) / max(len(a_words), 1)


def group_similar(signals, threshold=0.5):
    clusters = []
    used = set()

    for i, s1 in enumerate(signals):
        if i in used:
            continue

        cluster = [s1]
        used.add(i)

        for j, s2 in enumerate(signals):
            if j in used:
                continue

            sim = simple_similarity(
                normalize(s1.get("title", "")),
                normalize(s2.get("title", ""))
            )

            if sim > threshold:
                cluster.append(s2)
                used.add(j)

        clusters.append(cluster)

    return clusters


def merge_cluster(cluster):
    # en yüksek score olanı seç
    best = max(cluster, key=lambda x: x.get("score", 0))

    merged = {
        "title": best.get("title"),
        "content": best.get("content"),
        "score": best.get("score", 0),
        "sources": [s.get("source") for s in cluster],
        "cluster_size": len(cluster)
    }

    return merged


def cluster_signals(signals):
    grouped = group_similar(signals)
    merged = [merge_cluster(c) for c in grouped]

    return merged
