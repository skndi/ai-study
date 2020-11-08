import numpy
import random

def generate_puzzle():

    puzzle = numpy.zeros(shape = (4, 4), dtype = numpy.int32);
    counter = 1;
    for i in range(4):
        for j in range(4):
            puzzle[i][j] = counter;
            counter += 1;

    puzzle[3][3] = 0;

    for i in range(100):
        randomize(puzzle);
        randomize(puzzle);

    return puzzle;

def randomize(puzzle):
    
    first_x = random.randint(0, 3);
    first_y = random.randint(0, 3);
    second_x = random.randint(0, 3);
    second_y = random.randint(0, 3);

    puzzle[first_x][first_y], puzzle[second_x][second_y] = puzzle[second_x][second_y], puzzle[first_x][first_y];
