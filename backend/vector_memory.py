from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

memory_vectors = []
memory_texts = []


def store(text):

    global memory_vectors, memory_texts

    v = model.encode(text)

    memory_vectors.append(v)
    memory_texts.append(text)

    print("Stored vector:", text)


def search(query):

    if not memory_vectors:
        return []

    q = model.encode(query)

    sims = []

    for i, v in enumerate(memory_vectors):

        sim = np.dot(q, v) / (np.linalg.norm(q) * np.linalg.norm(v))
        sims.append((sim, memory_texts[i]))

    sims.sort(reverse=True)

    return sims[:3]


def run():

    example = "AI regulation in Europe"

    store(example)

    print("Vector search:", search("AI policy"))
