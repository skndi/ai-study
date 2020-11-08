from math import ceil
from math import floor
from collections import defaultdict

class spatial_hash(object):

    """description of class"""
    def __init__(self, min, max, cell_size):
        self.table = defaultdict(lambda: []);
        self.min = min;
        self.max = max;
        self.cell_size = cell_size;
        self.width = (self.max - self.min) / self.cell_size;
        number_of_buckets = self.width * self.width;
        self.conversion_factor = 1 / self.cell_size;

    def hash(self, map):
        self.table.clear();
        for obstacle in map:
            for wall in obstacle:
                start_x = wall[0][0];
                start_y = wall[0][1];
                end_x = wall[1][0];
                end_y = wall[1][1]

                if start_y > end_y:
                    start_x, end_x = end_x, start_x;
                    start_y, end_y = end_y, start_y;
                
                start_index = [floor(start_y * self.conversion_factor), floor(start_x * self.conversion_factor)];
                end_index = [floor(end_y * self.conversion_factor), floor(end_x * self.conversion_factor)];
                if start_index == end_index:
                    self.table[(start_index[0], start_index[1])].append(wall);
                    continue;

                dy = abs(end_index[0] - start_index[0]);
                dx = abs(end_index[1] - start_index[1]);

                if start_index[1] <= end_index[1]:
                    for y in range(dy + 1):
                        for x in range(0, dx + 1):
                            self.table[(start_index[0] + y, start_index[1] + x)].append(wall);

                elif start_index[1] > end_index[1]:
                    for y in range(dy + 1):
                        for x in range(0, dx + 1):
                            self.table[(start_index[0] + y, start_index[1] - x)].append(wall);

    def get_cell_objects(self, cell):
        return self.table[cell];

    def get_traversed_zones(self, ray):
                traversed = [];
                start_x = ray[0][0];
                start_y = ray[0][1];
                end_x = ray[1][0];
                end_y = ray[1][1];

                if start_y > end_y:
                    start_x, end_x = end_x, start_x;
                    start_y, end_y = end_y, start_y;
                
                start_index = [floor(start_y * self.conversion_factor), floor(start_x * self.conversion_factor)];
                end_index = [floor(end_y * self.conversion_factor), floor(end_x * self.conversion_factor)];

                if start_index == end_index:
                    traversed.append((end_index[0], end_index[1]));
                    return traversed;

                dy = abs(end_index[0] - start_index[0]);
                dx = abs(end_index[1] - start_index[1]);

                if start_index[1] <= end_index[1]:
                    for y in range(dy + 1):
                        for x in range(dx + 1):
                            traversed.append((start_index[0] + y, start_index[1] + x));

                elif start_index[1] > end_index[1]:
                    for y in range(dy + 1):
                        for x in range(dx + 1):
                            traversed.append((start_index[0] + y, start_index[1] - x));

                return traversed;
