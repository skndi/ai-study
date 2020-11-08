from data_structures.graph import Graph
from data_structures.graph import Vertex
import random
from tsp.algorithms import a_star
from tsp.algorithms.local_search import local_search_tools as lst

def generate_starting_solution(graph):
    unvisited_list = list(graph.vert_dict.values());
    path = [];

    while unvisited_list:
        current_city = random.choice(unvisited_list);
        path.append(current_city);
        unvisited_list.remove(current_city);
    path.append(path[0]);
    return path;



def randomize_solution(solution):
    randomized_solution = list(solution);

    length = len(randomized_solution) - 1;
    random_index1 = random.randint(1, length - 1);
    random_index2 = random.randint(1, length - 1);

    randomized_solution[random_index1], randomized_solution[random_index2] = randomized_solution[random_index2], randomized_solution[random_index1];

    return randomized_solution;

def search(graph : Graph.Graph):
    optimal_solution = a_star.search(list(graph.vert_dict.values())[0], graph);
    cost_of_optimal = lst.cost_of_solution(optimal_solution);

    solution = generate_starting_solution(graph);

    while(lst.cost_of_solution(solution) - cost_of_optimal > 50):

        tentative_solution = randomize_solution(solution);
        if lst.cost_of_solution(tentative_solution) < lst.cost_of_solution(solution):
           solution = tentative_solution;

    return solution;