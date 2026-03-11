import re
from collections import Counter


STOPWORDS = {

    "the","a","an","and","or","but","if","then",
    "of","in","on","for","to","with","by","is",
    "are","was","were","this","that","these","those"

}


def tokenize(text):

    text = text.lower()

    text = re.sub(r"[^a-z0-9\s]", " ", text)

    words = text.split()

    tokens = []

    for w in words:

        if w not in STOPWORDS and len(w) > 2:
            tokens.append(w)

    return tokens



def analyse(data):

    results = []

    for item in data:

        text = item.get("text", "")

        tokens = tokenize(text)

        word_freq = Counter(tokens)

        score = len(tokens)

        results.append({

            "text": text,
            "tokens": tokens,
            "keywords": word_freq.most_common(5),
            "score": score

        })

    print("analytics analysed:", len(results))

    return results
