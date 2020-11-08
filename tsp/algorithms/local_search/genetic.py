import random
from tsp.algorithms.local_search import local_search_tools as lst
import sys
import math
import array

def create_first_generation(encoded_cities, number_of_individuals):
    individuals = [];
    reference = list(encoded_cities);

    for i in range (0, number_of_individuals):
        unvisited_cities = list(encoded_cities);
        current_individual = [];

        while unvisited_cities:
            current_city = random.choice(unvisited_cities);
            current_individual.append(reference.index(current_city) + 1);
            unvisited_cities.remove(current_city);

        individuals.append(encode(current_individual));

    return individuals;

def random_selection(individuals, encoded_cities):
    fitness = [];
    probability = [];
    individuals_count = len(individuals);
    mating_couples = [];

    for i in range(0, individuals_count):
        fitness.append(1 / cost_of_solution(individuals[i], encoded_cities));
    sum_of_fitness = sum(fitness, 0);
    for i in range(0, individuals_count):
        probability.append(fitness[i] / sum_of_fitness);

    individuals_for_mating = random.choices(individuals, probability, k = (individuals_count * 2));

    for i in range(0, individuals_count):
        mating_couples.append((individuals_for_mating[2 * i], individuals_for_mating[(2 * i) + 1]));

    return mating_couples;

def cost_of_solution(individual, encoded_cities):
    path = decode_solution(individual, encoded_cities);

    cost = 0;
    length_of_solution = len(path);

    for i in range(0, length_of_solution - 1):
        cost += path[i].get_weight(path[i + 1]);

    return cost;

def reproduce(mating_couples):
    new_generation = [];

    for couple in mating_couples:
        new_individual = crossover(couple[0], couple[1]);
        if random.uniform(0, 1) <= 0.05:
            mutate(new_individual);
        new_generation.append(new_individual);

    return new_generation;

def crossover(first_mate, second_mate):
    length_of_individuals = len(first_mate);
    crossover_point = random.randint(1, length_of_individuals - 1);

    new_individual = [];
    for i in range(0, crossover_point):
        new_individual.append(first_mate[i]);

    for i in range(crossover_point, length_of_individuals):
        new_individual.append(second_mate[i]);

    return new_individual;

def mutate(individual):
    length = len(individual) - 1;
    decoded_individual = decode(individual);

    random_index1 = random.randint(1, length - 1);
    random_index2 = random.randint(1, length - 1);

    decoded_individual[random_index1], decoded_individual[random_index2] = decoded_individual[random_index2], decoded_individual[random_index1];
    individual = encode(decoded_individual);

def encode(cities):
    length = len(cities);
    inversion = array.array('I');

    for i in range(length):
        inversion.append(0);
        m = 0;
        while cities[m] != i + 1:
            if cities[m] > i:
                inversion[i] += 1;
            m += 1;

    return inversion;

def decode(encoded_cities):
    length = len(encoded_cities);
    position = array.array("I");
    cities = array.array("I");
    for i in range(length):
        cities.append(0);
        position.append(0);

    for i in range(length - 1, -1, -1):
        for m in range(i + 1, length):
            if position[m] >= encoded_cities[i] + 1:  
                position[m] += 1;

        position[i] = encoded_cities[i] + 1;

    for i in range(length):
        cities[position[i] - 1] = i + 1;

    return cities;

def get_best_individual(individuals, encoded_cities):
    min = sys.maxsize;
    best_individual = [];

    for x in individuals:
        if (1 / cost_of_solution(x, encoded_cities)) < min:
            min = cost_of_solution(x, encoded_cities);
            best_individual = x;

    return best_individual;

def decode_solution(individual, encoded_cities):
    decoded_individual = decode(individual);

    path = [];
    for x in decoded_individual:
        path.append(encoded_cities[x - 1]);

    path.append(path[0]);
    return path

def search(graph, number_of_individuals):

    encoded_cities = list(graph.vert_dict.values());
    current_generation = create_first_generation(encoded_cities, number_of_individuals);

    for i in range(100):
        mating_couples = random_selection(current_generation, encoded_cities);
        current_generation = reproduce(mating_couples);

    best_individual = get_best_individual(current_generation, encoded_cities);
    return decode_solution(best_individual, encoded_cities);



