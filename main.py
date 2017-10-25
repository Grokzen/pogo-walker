from math import cos, asin, sqrt
from collections import defaultdict, deque
import itertools

points = {
    2: {'lat': 59.378610, 'lon': 17.9356071},
    4: {'lat': 59.378252, 'lon': 17.9355041},
    5: {'lat': 59.378190, 'lon': 17.9359410},
    7: {'lat': 59.377704, 'lon': 17.9347777},
    17: {'lat': 59.378427, 'lon': 17.9382074},
    27: {'lat': 59.379410, 'lon': 17.9365200},
}


def distance(lat1, lon1, lat2, lon2):
    p = 0.017453292519943295  # Pi/180
    a = 0.5 - cos((lat2 - lat1) * p)/2 + cos(lat1 * p) * cos(lat2 * p) * (1 - cos((lon2 - lon1) * p)) / 2
    return 12742 * asin(sqrt(a))  # 2*R*asin...


for subset in itertools.combinations(points.keys(), 2):
    a = points[subset[0]]
    b = points[subset[1]]
    print('' + str(subset[0]) + '->' + str(subset[1]) + ': ' +
        str(distance(
            a['lat'], a['lon'],
            b['lat'], a['lon'],
        ) * 1000)
    )


class Graph:
    def __init__(self):
        self.nodes = set()
        self.edges = defaultdict(list)
        self.distances = {}

    def add_node(self, value):
        self.nodes.add(value)

    def add_edge(self, from_node, to_node, distance):
        self.edges[from_node].append(to_node)
        # self.edges[to_node].append(from_node)
        self.distances[(from_node, to_node)] = distance
        self.distances[(to_node, from_node)] = distance


def dijsktra(graph, initial):
    visited = {initial: 0}
    path = {}

    nodes = set(graph.nodes)

    while nodes:
        min_node = None
        for node in nodes:
            if node in visited:
                if min_node is None:
                    min_node = node
                elif visited[node] < visited[min_node]:
                    min_node = node

        if min_node is None:
            break

        nodes.remove(min_node)
        current_weight = visited[min_node]

        for edge in graph.edges[min_node]:
            weight = current_weight + graph.distances[(min_node, edge)]
            if edge not in visited or weight < visited[edge]:
                visited[edge] = weight
                path[edge] = min_node

    return visited, path


def shortest_path(graph, origin, destination):
    visited, paths = dijsktra(graph, origin)
    full_path = deque()
    _destination = paths[destination]

    while _destination != origin:
        full_path.appendleft(_destination)
        _destination = paths[_destination]

    full_path.appendleft(origin)
    full_path.append(destination)

    return visited[destination], list(full_path)


# g = Graph()
# g.add_node('a')
# g.add_node('b')
# g.add_node('c')

# g.add_edge('a', 'b', 10)
# g.add_edge('b', 'c', 10)
# g.add_edge('a', 'c', 15)

# print(dijsktra(g, 'a'))


g = Graph()
for k, v in points.items():
    g.add_node(str(k))

keys = points.keys()
for i in range(0, len(keys)):
    for j in range(0, len(keys)):
        if i != j:
            a = points[keys[i]]
            b = points[keys[j]]
            g.add_edge(str(keys[i]), str(keys[j]), distance(a['lat'], a['lon'], b['lat'], b['lon']) * 1000)

# for subset in itertools.combinations(points.keys(), 2):
#     a = points[subset[0]]
#     b = points[subset[1]]
#     g.add_edge(str(subset[0]), str(subset[1]), distance(a['lat'], a['lon'], b['lat'], b['lon'])*1000)

from pprint import pprint
for k, v in points.items():
    print("Key: " + str(k))
    # result = dijsktra(g, str(k))
    #pprint(result)
    # total = 0
    # for k, v in result[0].items():
    #     total += v
    # print(total)
    print(shortest_path(g, '7', '27'))
    print("")


pprint(g.nodes)
pprint(g.edges)
pprint(g.distances)
