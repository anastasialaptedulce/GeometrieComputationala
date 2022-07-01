from graph import Graph, Edge
from shortest_path import shortest_path
from visible_vertices import visible_vertices


class VisGraph(object):

    def __init__(self):
        self.graph = None
        self.visgraph = None

    def build(self, input): 
        self.graph = Graph(input)
        self.visgraph = Graph([])

        points = self.graph.get_points()
        batch_size = 10 
        
        for edge in _vis_graph(self.graph, points):
            self.visgraph.add_edge(edge)


    def find_visible(self, point):
        return visible_vertices(point, self.graph)

    def update(self, points, origin=None, destination=None):
        for p in points:
            for v in visible_vertices(p, self.graph, origin=origin,
                                      destination=destination):
                self.visgraph.add_edge(Edge(p, v))

    def shortest_path(self, origin, destination):
        origin_exists = origin in self.visgraph
        dest_exists = destination in self.visgraph
        if origin_exists and dest_exists:
            return shortest_path(self.visgraph, origin, destination)
        orgn = None if origin_exists else origin
        dest = None if dest_exists else destination
        add_to_visg = Graph([])
        if not origin_exists:
            for v in visible_vertices(origin, self.graph, destination=dest):
                add_to_visg.add_edge(Edge(origin, v))
        if not dest_exists:
            for v in visible_vertices(destination, self.graph, origin=orgn):
                add_to_visg.add_edge(Edge(destination, v))
        return shortest_path(self.visgraph, origin, destination, add_to_visg)


def _vis_graph(graph, points):
    visible_edges = []
    for p1 in points:
        for p2 in visible_vertices(p1, graph):
            visible_edges.append(Edge(p1, p2))
    return visible_edges
