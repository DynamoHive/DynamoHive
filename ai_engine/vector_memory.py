import os
import json
import numpy as np

try:
    from sentence_transformers import SentenceTransformer
    MODEL_AVAILABLE = True
except:
    MODEL_AVAILABLE = False


# -------------------------
# MODEL
# -------------------------
if MODEL_AVAILABLE:
    model = SentenceTransformer("all-MiniLM-L6-v2")
else:
    model = None


# -------------------------
# STORAGE
# -------------------------
MEMORY_PATH = "vector_memory.json"

memory_vectors = []
memory_texts = []


# -------------------------
# LOAD / SAVE
# -------------------------
def _save():
    try:
        data = [
            {
                "text": memory_texts[i],
                "vector": memory_vectors[i].tolist()
            }
            for i in range(len(memory_texts))
        ]

        with open(MEMORY_PATH, "w") as f:
            json.dump(data, f)

    except Exception as e:
        print("[VECTOR SAVE ERROR]", e)


def _load():
    global memory_vectors, memory_texts

    if not os.path.exists(MEMORY_PATH):
        return

    try:
        with open(MEMORY_PATH, "r") as f:
            data = json.load(f)

        for item in data:
            memory_texts.append(item["text"])
            memory_vectors.append(np.array(item["vector"]))

    except Exception as e:
        print("[VECTOR LOAD ERROR]", e)


# load on startup
_load()


# -------------------------
# UTILS
# -------------------------
def _normalize(v):
    norm = np.linalg.norm(v)
    return v / norm if norm != 0 else v


def _safe_encode(text):

    if not MODEL_AVAILABLE:
        # fallback: random vector (sistemi kırmaz)
        return np.random.rand(384)

    try:
        return model.encode(text)
    except Exception as e:
        print("[ENCODE ERROR]", e)
        return np.random.rand(384)


# -------------------------
# STORE
# -------------------------
def store_vector(post):

    text = ""

    if isinstance(post, dict):

        title = post.get("title", "")
        content = post.get("content", "")

        text = (title + " " + content).strip()

    if not text or len(text) < 10:
        return

    vector = _safe_encode(text)
    vector = _normalize(vector)

    memory_vectors.append(vector)
    memory_texts.append(text)

    # limit memory size (important)
    if len(memory_texts) > 2000:
        memory_texts.pop(0)
        memory_vectors.pop(0)

    _save()


# -------------------------
# SEARCH
# -------------------------
def search_similar(query, top_k=3):

    if not memory_vectors:
        return []

    query_vector = _normalize(_safe_encode(query))

    scores = []

    for i, vec in enumerate(memory_vectors):

        score = float(np.dot(query_vector, vec))

        scores.append({
            "score": score,
            "text": memory_texts[i]
        })

    scores.sort(key=lambda x: x["score"], reverse=True)

    return scores[:top_k]


# -------------------------
# DEBUG
# -------------------------
def memory_size():
    return len(memory_texts)
