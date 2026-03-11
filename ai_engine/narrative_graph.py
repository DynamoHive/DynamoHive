from collections import defaultdict

narrative_graph = defaultdict(list)


def update_narrative_graph(entities, narratives):

    actors = entities.get("persons", []) + entities.get("organizations", [])

    for actor in actors:

        for narrative in narratives:

            if narrative not in narrative_graph[actor]:

                narrative_graph[actor].append(narrative)


def get_narrative_graph():

    return narrative_graph
