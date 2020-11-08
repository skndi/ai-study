import random
import numpy

def solve(puzzle):
    moves = [];
    zero_coordinates = find_zero(puzzle);
    current = puzzle
    while not solved(current):
        cost_of_current = calculate_cost(current);
        new_arrangement = numpy.ndarray.copy(current);
        move = make_move(new_arrangement, zero_coordinates);
        if calculate_cost(new_arrangement)  < cost_of_current:
            current = new_arrangement;
            update_zero_coords(zero_coordinates, move);
            moves.append(move);

    return str(moves + '\n');

def update_zero_coords(zero_coordinates, move):
    if move == "Up":
        zero_coordinates[0] -= 1;

    elif move == "Down":
        zero_coordinates[0] += 1;

    elif move == "Right":
        zero_coordinates[1] += 1;

    elif move == "Left":
        zero_coordinates[1] -= 1;

def solved(puzzle):
    solved = True;
    counter = 1;

    for i in range(4):
        for j in range(4):
            if i == 3 and j == 3:
                return solved;
            if puzzle[i][j] != counter:
                solved = False;
            counter += 1;

def make_move(puzzle, zero_coordinates):
    valid = False;
    move = str();

    while not valid:
        block_to_move = random.randint(1, 4);

        if block_to_move == 1 and zero_coordinates[0] != 0:
            valid = True;
            puzzle[zero_coordinates[0] - 1][zero_coordinates[1]], puzzle[zero_coordinates[0]][zero_coordinates[1]] = puzzle[zero_coordinates[0]][zero_coordinates[1]], puzzle[zero_coordinates[0] - 1][zero_coordinates[1]];
            move = "Up";

        if block_to_move == 2 and zero_coordinates[1] != 3:
            valid = True;
            puzzle[zero_coordinates[0]][zero_coordinates[1] + 1], puzzle[zero_coordinates[0]][zero_coordinates[1]] = puzzle[zero_coordinates[0]][zero_coordinates[1]], puzzle[zero_coordinates[0]][zero_coordinates[1] + 1];
            move = "Right";

        if block_to_move == 3 and zero_coordinates[0] != 3:
            valid = True;
            puzzle[zero_coordinates[0] + 1][zero_coordinates[1]], puzzle[zero_coordinates[0]][zero_coordinates[1]] = puzzle[zero_coordinates[0]][zero_coordinates[1]], puzzle[zero_coordinates[0] + 1][zero_coordinates[1]];
            move = "Down";

        if block_to_move == 4 and zero_coordinates[1] != 0:
            valid = True;
            puzzle[zero_coordinates[0]][zero_coordinates[1] - 1], puzzle[zero_coordinates[0]][zero_coordinates[1]] = puzzle[zero_coordinates[0]][zero_coordinates[1]], puzzle[zero_coordinates[0]][zero_coordinates[1] - 1];
            move = "Left";
    
    return move;

def calculate_cost(solution):
    cost = 0;
 
    for i in range(4):
        for j in range(4):
            if solution[i][j] == 0:
                continue;
            correct_position = position(solution[i][j]);
            cost += abs(correct_position[0] - i) + (abs(correct_position[1] - j));

    return cost;

def find_zero(puzzle):
    for i in range(4):
        for j in range(4):
            if puzzle[i][j] == 0:
                return [i, j];

def position(number):
    first_coord = 0;
    second_coord = 0;
    while number > 4:
        number -= 4;
        first_coord += 1;

    while number > 1:
        number -= 1;
        second_coord += 1;

    return (first_coord, second_coord);