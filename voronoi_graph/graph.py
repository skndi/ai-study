import pytess
import numpy
import scipy
import matplotlib.pyplot as plt
from scipy.spatial import *
import generate_points
from data_structures.graph import Graph
import line_tools

def get_voronoi(screen_width, screen_height, point_count):
    return scipy.spatial.Voronoi(generate_points.generate_points(screen_width, screen_height, point_count));

def check_valid(line, width, height):
    currentLineStartX = line[0][0];
    currentLineStartY = line[0][1];
    currentLineEndX = line[1][0];
    currentLineEndY = line[1][1];

    if((currentLineStartX > - 1 and currentLineStartX < width) and (currentLineStartY > -1 and currentLineStartY < height)
       and (currentLineEndX > - 1 and currentLineEndX < width) and (currentLineEndY > - 1 and currentLineEndY < height)):
        return True;

    return False;

def sort_lines(voronoi, width, height):
    listLength = (len(voronoi.ridge_vertices));

    lines = [(voronoi.vertices[voronoi.ridge_vertices[0][0]], voronoi.vertices[voronoi.ridge_vertices[0][1]])];
    lines.clear();

    for i in range(0, listLength):
        if(voronoi.ridge_vertices[i][0] > -1 and voronoi.ridge_vertices[i][1] > -1):
            newLine = (tuple(voronoi.vertices[voronoi.ridge_vertices[i][0]]), tuple(voronoi.vertices[voronoi.ridge_vertices[i][1]]));
            
            if(check_valid(newLine, width, height)):
                lines.append(tuple(newLine));

    return lines

def generate_graph(voro, width, height):
    line_list = sort_lines(voro, width, height);
    g = Graph.Graph();

    for line in line_list:
        g.add_vertex(line[0]);
        g.add_vertex(line[1]);
        g.add_edge(line[0], line[1], line_tools.calc_length(line));
        
    return g

def get_graph(screen_width, screen_height, point_count):
    voro = get_voronoi(screen_width, screen_height, point_count);
    g = generate_graph(voro, screen_width, screen_height);
    return g;
