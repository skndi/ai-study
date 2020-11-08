import math

def calc_length(line):
    start_x = line[0][0];
    start_y = line[0][1];
    end_x = line[1][0];
    end_y = line[1][1];

    x_2 = math.pow((start_x - end_x), 2);
    y_2 = math.pow((start_y - end_y), 2);

    return int(math.sqrt(x_2 + y_2));
