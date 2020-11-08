import path_search_algorithms
from path_search_algorithms import best_first_search
from data_structures.graph import Graph
from data_structures.graph import Vertex


def search(start: Vertex.Vertex, goal: Vertex.Vertex, graph: Graph.Graph, w, h):
    return path_search_algorithms.best_first_search.search(graph.vert_dict[start.get_id()], graph.vert_dict[goal.get_id()], graph, lambda x, y: (2 - w) * x + (w * y), lambda x, y: graph.vert_dict[x.get_id()].get_weight(y), h);

