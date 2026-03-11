import re

def extract_entities(text):

    entities = {
        "persons": [],
        "organizations": [],
        "locations": []
    }

    words = text.split()

    for w in words:

        if w.istitle() and len(w) > 3:

            if w.endswith("Inc") or w.endswith("Corp"):
                entities["organizations"].append(w)

            elif w in ["USA","China","Russia","EU","Europe"]:
                entities["locations"].append(w)

            else:
                entities["persons"].append(w)

    return entities
