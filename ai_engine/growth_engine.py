growth_map = {}


def update_growth(topic):

    if topic not in growth_map:
        growth_map[topic] = 1
    else:
        growth_map[topic] += 1


def get_growth():

    return growth_map
