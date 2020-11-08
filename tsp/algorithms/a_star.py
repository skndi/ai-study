from data_structures.priority_queue import PriorityQueue
from data_structures.graph import Graph
from data_structures.graph import Vertex
from data_structures.graph import graph_tools
from path_search_algorithms import generate_path
from mst import Prim
import collections
import sys

def create_city_list(tsp_graph):
    s = [];
    for x in tsp_graph.vert_dict.values():
       s.append(x);

def get_neighbors(city_list):
    neighbors = set();
    for x in city_list:
        curr_city_neighbors = x.get_neighbors();
        for y in curr_city_neighbors:
            neighbors.add(y);
    return neighbors;

def mst_heuristic(start, current, unvisited_set):
    #min_unvisited_current = min_unvisited_start = min_mst = sys.maxsize;
    mst_list = [];

    for x in unvisited_set:
        mst_list.append(x);
        #if current.get_weight(x) < min_unvisited_current:
            #min_unvisited_current = current.get_weight(x);
        #if start.get_weight(x) < min_unvisited_start:
            #min_unvisited_start = start.get_weight(x);
    mst = Prim.mst(Graph.Graph.from_vertices(mst_list));
    
    return graph_tools.sum_edges(mst);
    #min_unvisited_current + min_unvisited_start +

def search(start: Vertex.Vertex, graph: Graph.Graph):
    unvisited_set = set(graph.vert_dict.values());
    goal = set(graph.vert_dict.values());
    f_score = collections.defaultdict(lambda: sys.maxsize);
    visited_set = set();
    f_score[start] = 0;
    open_list = PriorityQueue.PriorityQueue();
    open_list.add_task(start);
    came_from = dict();

    while open_list:
        current = open_list.pop_task();
        visited_set.add(current);
        unvisited_set.remove(current);

        if visited_set == goal:
            path = generate_path.reconstruct_path(came_from, current);
            path.append(list(graph.vert_dict.values())[0]);
            return path;

        for x in unvisited_set:
            tentative_fscore = graph.vert_dict[current.get_id()].get_weight(x) + mst_heuristic(start, current, unvisited_set);
            if x not in open_list or x not in visited_set:
                f_score[x] = tentative_fscore;
                open_list.add_task(x, f_score[x]);

            if x in open_list or x in visited_set and tentative_fscore < f_score[x]:
                came_from[x] = current;
                f_score[x] = tentative_fscore;
                if(x in visited_set):
                    unvisited_set.add(x);
                    
    return None;