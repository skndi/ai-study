from voronoi_graph import graph
import random
from scipy.spatial import ConvexHull

def get_regions(width, height, points_count):
    voro = graph.get_voronoi(width, height, points_count);
    valid_regions = sort_regions(voro.regions);

    regions = get_region_coordinates(valid_regions, voro, width, height);

    return regions;

def sort_regions(regions):
    valid_regions = [];
    valid = True;

    for region in regions:
        if region == []:
            continue;
        for x in region:
            if x == -1:
                valid = False;
        if valid:
            valid_regions.append(region);
        valid = True;

    return valid_regions;

def get_region_coordinates(regions, voro, width, height):
    
    obstacles = [];
    for region in regions:
        new_obstacle = [];
        for vertex in region:
            new_obstacle.append(tuple(voro.vertices[vertex]));
        if check_valid(new_obstacle, width, height):
            obstacles.append(new_obstacle);

    return obstacles;

def check_valid(region, width, height):

    for i in range(-1, len(region) - 1):
        if not graph.check_valid((region[i], region[i + 1]), width, height):
            return False;

    return True;

def choose_random_points(region):
    points = [];

    for i in range(-1, len(region) - 1):
        u = random.uniform(0, 1);
        x_coord = ((1 - u) * region[i][0]) + (u * region[i + 1][0]);
        y_coord = ((1 - u) * region[i][1]) + (u * region[i + 1][1]);
        points.append((x_coord, y_coord));

    return points;

def create_hull_points(regions):
    hull_points = [];

    for region in regions:
       point_set = choose_random_points(region);
       hull_points.append(point_set);

    return hull_points;

def create_obstacles(hull_points):
    convex_hull_set = [];

    for point_set in hull_points:
        new_obstacle = ConvexHull(point_set);
        convex_hull_set.append(new_obstacle);

    return convex_hull_set;

def convert_to_lines(convex_hulls):
    hull_lines = [];

    for hull in convex_hulls:
        new_lines = [];
        centroid = [0, 0];
        for i in range(len(hull.points)):
            centroid[0] +=  hull.points[i][0];
            centroid[1] += hull.points[i][1];

        centroid[0] /= len(hull.points);
        centroid[1] /= len(hull.points);
        u = random.uniform(0.2, 0.4);

        for i in range(-1, len(hull.vertices) - 1):
            shrinked_point1_x = (1 - u) * hull.points[hull.vertices[i]][0] + (u * centroid[0]);
            shrinked_point1_y = (1 - u) * hull.points[hull.vertices[i]][1] + (u * centroid[1]);
            shrinked_point2_x = (1 - u) * hull.points[hull.vertices[i + 1]][0] + (u * centroid[0]);
            shrinked_point2_y = (1 - u) * hull.points[hull.vertices[i + 1]][1] + (u * centroid[1]);
            new_lines.append(((shrinked_point1_x, shrinked_point1_y), (shrinked_point2_x, shrinked_point2_y)));
        hull_lines.append(new_lines);

    return hull_lines;

def get_obstacles(width, height, points_count):
    regions = get_regions(width, height, points_count);
    hull_points = create_hull_points(regions);

    obstacles = create_obstacles(hull_points);
    return convert_to_lines(obstacles);