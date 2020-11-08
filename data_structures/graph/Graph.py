from data_structures.graph import Vertex
import line_tools
import copy

class Graph():
    """description of class"""

    def __init__(self):
        self.vert_dict = {};
        self.vert_count = 0;

    @classmethod
    def from_vertices(cls, vertices):
        graph = cls();
        for x in vertices:
            graph.vert_count += 1;
            for y in x.get_neighbors():
                first_point = x.get_id();
                second_point = y.get_id();
                graph.add_vertex(first_point);
                graph.add_vertex(second_point);
                graph.add_edge(first_point, second_point, line_tools.calc_length((first_point, second_point)));
        return graph;

    def __iter__(self):
        return iter(self.vert_dict.keys());

    def add_vertex(self, node):
        if node not in self.vert_dict:
            self.vert_count += 1;
            new_vertex = Vertex.Vertex(node);
            self.vert_dict[node] = new_vertex;
            return new_vertex;
        else:
            return None;

    def get_vertex(self, node):
        if node in self.vert_dict:
            return self.vert_dict[node];
        else:
            return None;

    def add_edge(self, frm, to, cost = 0):

        if frm not in self.vert_dict:
            self.add_vertex(frm);
        if to not in self.vert_dict:
            self.add_vertex(to);

        self.vert_dict[frm].add_neighbor(self.vert_dict[to], cost);
        self.vert_dict[to].add_neighbor(self.vert_dict[frm], cost);

    def get_vertices(self):
        return self.vert_dict.keys();