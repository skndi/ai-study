import sys
from math import cos
from math import sin
from math import degrees
from math import sqrt
import time
import vector_operations as vo

def calculate_visible_vertices(agent, map, hash_table):
    visible_vertices = [];
    agent_position = agent.position;
    rays = get_rays(agent_position, map);

    for ray in rays:
        intersection = get_closest_intersection(ray, map, hash_table);
        
        if intersection and intersection == ray[1]:
            intersection_vector = ((intersection[0] - agent.position[0]), (intersection[1] - agent.position[1]));
            angle = vo.get_relative_angle(agent.orientation_reference_vector, intersection_vector);
            distance = vo.magnitude(intersection_vector);
            visible_vertices.append((angle, distance));

    visible_vertices.sort(key = lambda x: x[0]);
    
    return visible_vertices;

def get_closest_intersection(ray, map, hash_table):
    closest_intersection = None;
    min_t1 = sys.maxsize;  
    traversed_zones = hash_table.get_traversed_zones(ray);
    length = len(traversed_zones);
    visited = set();
    
    for i in range(length):
        current_zone = hash_table.get_cell_objects(traversed_zones[i]);
        for wall in current_zone:
            if wall not in visited:
                visited.add(wall);
                intersection = get_intersection(ray, wall);
                if intersection:
                    t1 = intersection[1];
                    intersection_coords = intersection[0];
                    if t1 < min_t1:
                        closest_intersection = intersection_coords;
                        min_t1 = t1;
  
    return closest_intersection;

def get_intersection(ray, segment):

    r_ptx = ray[0][0];
    r_pty = ray[0][1];
    r_dx = ray[1][0] - ray[0][0];
    r_dy = ray[1][1] - ray[0][1];

    sg_ptx = segment[0][0];
    sg_pty = segment[0][1];
    sg_dx = segment[1][0] - segment[0][0];
    sg_dy = segment[1][1] - segment[0][1];

    r_mag = sqrt((r_dx * r_dx) + (r_dy * r_dy));
    sg_mag = sqrt((sg_dx * sg_dx) + (sg_dy * sg_dy));
    if (r_dx / r_mag == sg_dx / sg_mag) and (r_dy / r_mag == sg_dy / sg_mag):
        return None;

    t2 = (r_dx * (sg_pty - r_pty) + r_dy * (r_ptx - sg_ptx)) / (sg_dx * r_dy - sg_dy * r_dx);
    t1 = (sg_ptx + sg_dx * t2 - r_ptx) / (r_dx);

    if t1 <= 0:
        return None;
    if t2 < 0 or t2 > 1:
        return None

    x = r_ptx + r_dx * t1;
    y = r_pty + r_dy * t1;

    return ((x, y), t1);

def get_rays(agent, map):
    rays = set();

    for obstacle in map:
        length = len(obstacle);
        for i in range(-1, length - 1):
            start = obstacle[i][0];
            middle = obstacle[i][1];
            end = obstacle[i + 1][1];

            rays.add((agent, start));
            rays.add((agent, middle));
            if i != length - 2:
                rays.add((agent, end));
    
    return rays;

def determine_overlap(start, middle, end, ray):
    ray_vec = (ray[1][0] - ray[0][0], ray[1][1] - ray[0][1]);
    orthogonal_vec = (ray_vec[1], -ray_vec[0]);
    ortho_mag_factor = 1 / sqrt(orthogonal_vec[0] * orthogonal_vec[0] + orthogonal_vec[1] * orthogonal_vec[1]);
    unit_ortho = (orthogonal_vec[0] * ortho_mag_factor, orthogonal_vec[1] * ortho_mag_factor);
    first_vec = (middle[0] - start[0], middle[1] - start[1]);
    second_vec = (end[0] - middle[0], end[1] - middle[1]);

    projection1 = first_vec[0] * unit_ortho[0]  + first_vec[1] * unit_ortho[1];
    projection2 = second_vec[0] * unit_ortho[0]  + second_vec[1] * unit_ortho[1];

    if projection1 < 0 and projection2 < 0:
        return 0;

    elif projection1 < 0:
        return 1;

    return -1;
