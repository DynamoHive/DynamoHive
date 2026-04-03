from collections import defaultdict

# -------------------------
# 🔥 GLOBAL STORAGE
# -------------------------
NARRATIVE_MEMORY = defaultdict(int)
ACTOR_MEMORY = defaultdict(int)


# -------------------------
# 🚀 MAIN ENGINE
# -------------------------
def update_global_map(intelligence):

    global NARRATIVE_MEMORY, ACTOR_MEMORY

    for intel in intelligence:

        # -------------------------
        # NARRATIVES
        # -------------------------
        iw = intel.get("information_warfare", {})
        narratives = iw.get("narratives", [])

        for n in narratives:
            NARRATIVE_MEMORY[n] += 1

        # -------------------------
        # ACTORS
        # -------------------------
        power = intel.get("power", {})
        actors = power.get("actors", [])

        for a in actors:
            ACTOR_MEMORY[a] += 1


# -------------------------
# 📊 GET MAP
# -------------------------
def get_global_map():

    top_narratives = sorted(
        NARRATIVE_MEMORY.items(),
        key=lambda x: x[1],
        reverse=True
    )[:5]

    top_actors = sorted(
        ACTOR_MEMORY.items(),
        key=lambda x: x[1],
        reverse=True
    )[:5]

    return {
        "top_narratives": [
            {"name": n, "strength": c}
            for n, c in top_narratives
        ],
        "top_actors": [
            {"name": a, "presence": c}
            for a, c in top_actors
        ]
    }


# -------------------------
# 🔥 RESET (opsiyonel)
# -------------------------
def reset_map():
    global NARRATIVE_MEMORY, ACTOR_MEMORY
    NARRATIVE_MEMORY.clear()
    ACTOR_MEMORY.clear()
