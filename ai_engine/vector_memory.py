from sentence_transformers import SentenceTransformer
import numpy as np


model = SentenceTransformer("all-MiniLM-L6-v2")

memory_vectors = []
memory_texts = []


def store_vector(post):

    text = ""

    if isinstance(post, dict):

        title = post.get("title", "")
        content = post.get("content", "")

        text = title + " " + content

    if not text:
        return

    vector = model.encode(text)

    memory_vectors.append(vector)
    memory_texts.append(text)


def search_similar(query, top_k=3):

    if not memory_vectors:
        return []

    query_vector = model.encode(query)

    scores = []

    for i, vec in enumerate(memory_vectors):

        score = np.dot(query_vector, vec)

        scores.append((score, memory_texts[i]))

    scores.sort(reverse=True)

    return scores[:top_k]
