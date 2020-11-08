import generate_points
from data_structures.graph import Graph
import path_search_algorithms
import line_tools

def generate_graph(screen_width, screen_height, num_of_vertices):
    points = generate_points.generate_points(screen_width, screen_height, num_of_vertices)
    g = Graph.Graph();

    for x in points:
        for y in points:
            if x != y:
                g.add_vertex(x);
                g.add_vertex(y);
                g.add_edge(x, y, line_tools.calc_length((x, y)));
        
    return g