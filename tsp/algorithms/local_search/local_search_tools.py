
def cost_of_solution(solution):
    cost = 0;
    length_of_solution = len(solution);

    for i in range(0, length_of_solution - 1):
        cost += solution[i].get_weight(solution[i + 1]);

    return cost;