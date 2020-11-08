from data_structures.priority_queue import PriorityQueue
from data_structures.graph import Graph
from data_structures.graph import Vertex
from path_search_algorithms import generate_path
import collections
import sys

def search(start: Vertex.Vertex, goal: Vertex.Vertex, graph: Graph.Graph, f, g, h):
    f_score = dict();
    f_score[start] = h(start, goal);
    g_score = collections.defaultdict(lambda: sys.maxsize);
    g_score[start] = 0;
    open_list = PriorityQueue.PriorityQueue();
    open_list.add_task(start);
    came_from = dict();
    discovered = collections.defaultdict(lambda: False);
    discovered[start] = True;

    while open_list:
        current = open_list.pop_task();
        discovered[current] = True;

        if(current == goal):
            return generate_path.reconstruct_path(came_from, current);

        neighbors = current.get_neighbors();
        for x in neighbors:

            tentative_gScore =  g_score[current] + g(current, x);
            if tentative_gScore < g_score[x]:
                came_from[x] = current;
                g_score[x] = tentative_gScore;
                f_score[x] = f(g_score[x], h(x, goal));

                if not discovered[x]:
                    open_list.add_task(x, f_score[x]);
    return None;