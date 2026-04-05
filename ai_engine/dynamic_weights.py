WEIGHTS = {
    "geopolitical escalation": 2.5,
    "system instability": 1.5,
    "ai power shift": 2.2,
    "technological acceleration": 1.3,
    "economic expansion": 1.2,
    "social unrest": 1.4,
    "emerging pattern": 1.0
}

def get_weight(label):
    return WEIGHTS.get(label, 1.0)
