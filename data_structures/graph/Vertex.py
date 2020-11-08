import sys
class Vertex:
    """description of class"""
    def __init__(self, node):
        self.id = node;
        self.adjacent = {};
    
    def __str__(self):
        return str(self.id) + " Adjacent: " + str([x.id for x in self.adjacent]) + "\n\n\n";

    __repr__ = __str__;

    def add_neighbor(self, node, weight = sys.maxsize):
        self.adjacent[node] = weight;

    def get_neighbors(self):
        return self.adjacent.keys();

    def get_id(self):
        return self.id;

    def get_weight(self, neighbor):
        if self == neighbor: return 0;
        return self.adjacent[neighbor];