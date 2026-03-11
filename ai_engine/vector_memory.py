import math
from collections import Counter

MEMORY = []


def tokenize(text):

    if not text:
        return []

    words = text.lower().split()

    tokens = []

    for w in words:
        if len(w) > 3:
            tokens.append(w)

    return tokens


def vectorize(text):

    tokens = tokenize(text)

    return Counter(tokens)


def cosine_similarity(v1, v2):

    intersection = set(v1.keys()) & set(v2.keys())

    dot = sum(v1[x] * v2[x] for x in intersection)

    mag1 = math.sqrt(sum(v ** 2 for v in v1.values()))
    mag2 = math.sqrt(sum(v ** 2 for v in v2.values()))

    if mag1 == 0 or mag2 == 0:
        return 0

    return dot / (mag1 * mag2)


def store_vector(post):

    text = post.get("content", "")

    vector = vectorize(text)

    MEMORY.append({
        "topic": post.get("topic"),
        "vector": vector,
        "text": text
    })

    print("vector stored:", len(MEMORY))


def search_similar(text, top_k=3):

    query_vector = vectorize(text)

    scores = []

    for item in MEMORY:

        sim = cosine_similarity(query_vector, item["vector"])

        scores.append((sim, item))

    scores.sort(reverse=True, key=lambda x: x[0])

    return scores[:top_k]
