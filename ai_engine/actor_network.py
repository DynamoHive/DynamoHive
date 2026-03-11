actor_graph = {}

def update_actor_network(entities):

    persons = entities.get("persons", [])

    for p in persons:

        if p not in actor_graph:
            actor_graph[p] = []

        for other in persons:

            if other != p and other not in actor_graph[p]:
                actor_graph[p].append(other)


def get_actor_network():

    return actor_graph
