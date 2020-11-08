import path_search_algorithms
from path_search_algorithms import best_first_search
from data_structures.graph import Graph
from data_structures.graph import Vertex


def ucs(start: Vertex.Vertex, goal: Vertex.Vertex, graph: Graph.Graph):
    return path_search_algorithms.best_first_search.best_first(graph.vert_dict[start.get_id()], graph.vert_dict[goal.get_id()], graph, lambda x, y: x + y, lambda x, y: graph.vert_dict[x.get_id()].get_weight(y), lambda x, y: 0);