import random

def generate_points(screen_width, screen_height, point_count):
    point_list = list();

    half_width = screen_width / 2;
    half_height = screen_height / 2;
    qt_width = half_width / 2;
    qt_height = half_height / 2;

    for x in range(0, point_count):
        point_list.append((random.randint(0, screen_width), random.randint(0, screen_height)));

    return point_list;
