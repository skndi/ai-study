import sys 

def find_leftmost(graph):
    min_point = (sys.maxsize, 0);

    for x in graph.vert_dict:
        if x[0] < min_point[0]:
            min_point = x;

    return min_point;

def find_rightmost(graph):
    max_point = (-1000, 0);

    for x in graph.vert_dict:
        if x[0] > max_point[0]:
            max_point = x;

    return max_point;

def generate_line_coords(graph):
    lines = []
    for x in graph.vert_dict.values():
        for y in x.get_neighbors():
            lines.append((x.get_id(), y.get_id()));
    return lines;

def generate_vertice_coords(graph):
    vertices = [];
    for x in graph.vert_dict.keys():
        vertices.append(x);

    return vertices;

def sum_edges(graph):
    sum = 0;
    for x in graph.vert_dict.values():
        for y in x.get_neighbors():
            sum += x.get_weight(y);

    return sum / 2;
