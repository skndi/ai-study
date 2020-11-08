from data_structures.graph import Graph
from data_structures.graph import Vertex
import collections
from collections import defaultdict
from data_structures.priority_queue import PriorityQueue
import sys

def mst(g : Graph.Graph):
    min_tree = Graph.Graph();
    open_list = PriorityQueue.PriorityQueue();
    cost = collections.defaultdict(lambda: sys.maxsize);
    for x in g.vert_dict.values():
        open_list.add_task(x, cost[x]);
    edge = collections.defaultdict(lambda: False);

    while open_list:
        current = open_list.pop_task();
        min_tree.add_vertex(current.get_id());
        if edge[current]:
            min_tree.add_edge(current.get_id(), edge[current][0].get_id(), edge[current][1]);
        for x in current.get_neighbors():
            if x in open_list and current.get_weight(x) < cost[x]:
                cost[x] = current.get_weight(x);
                edge[x] = (current, cost[x]);
                open_list.add_task(x, cost[x]);
    return min_tree;

