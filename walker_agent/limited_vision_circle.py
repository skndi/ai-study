import sys
from math import cos
from math import sin
from math import degrees
from math import sqrt
import time
from numpy import sign
from math import atan2
from collections import defaultdict
from math import degrees
import vector_operations as vo
from math import floor

OUTSIDE = 0;
WITHIN = 1;
BLOCKING = 0;
INTERSECT_CIRCLE = 1;

def calculate_visible_vertices(agent, map):
	elements = get_rays(agent, map);
	rays = elements[0];
	walls = elements[1];
	visible_vertices = [];

	for ray in rays:
		intersection = get_closest_intersection(agent, ray, walls);

		if intersection and intersection == ray[1]:
			intersection_vector = ((intersection[0] - agent.position[0]), (intersection[1] - agent.position[1]));
			angle = vo.get_relative_angle(agent.orientation_reference_vector, intersection_vector);
			distance = vo.magnitude(intersection_vector);
			visible_vertices.append((angle, distance));
	visible_vertices.sort(key = lambda x: x[0]);
	return visible_vertices;

def get_closest_intersection(agent, ray, walls):
	closest_intersection = None;
	min_t1 = sys.maxsize;

	for wall in walls:
		intersection = get_intersection(agent, ray, wall);
		if intersection:
			t1 = intersection[1];
			intersection_coords = intersection[0];
			if t1 < min_t1:
				closest_intersection = intersection_coords;
				min_t1 = t1;

	return closest_intersection;

def get_rays(agent, map):
	rays = [];

	obstacles = narrow_culling(agent, map);
	points = list(obstacles[0]);
	walls = obstacles[1];

	for point in points:
			rays.append((agent.position, point));
	
	return (rays, walls);

def narrow_culling(agent, map):
	circle_elements = broad_culling(agent, map);
	angle_points = circle_elements[0];
	walls = circle_elements[1];
	blocking_walls = walls[BLOCKING];

	circle_intersects = get_circle_intersections(agent, walls[INTERSECT_CIRCLE]);
	for angle_point in circle_intersects[0]:
		angle_points.add(angle_point);
	for wall in circle_intersects[1]:
		blocking_walls.add(wall);

	return (angle_points, blocking_walls)

def broad_culling(agent, map):
	walls_in_visible_range = get_visible_walls(agent, map);
	circle_elements = sort_elements(agent, walls_in_visible_range);
	
	return circle_elements;

def get_visible_walls(agent, map):
	walls_in_visible_range = [];

	for obstacle in map:
		for wall in obstacle:
			if inside_bounding_circle(agent, wall):
				walls_in_visible_range.append(wall);

	return walls_in_visible_range;

def sort_elements(agent, walls):
	radius = agent.vision_range;
	center = agent.position;
	angle_points = set();
	walls_by_type =  defaultdict(lambda: set());

	for wall in walls:
		first_vertex = -1;
		for vertex in wall:
			u = ((vertex[0] - center[0]), (vertex[1] - center[1]));

			if vo.dot_product(u, u) > radius * radius:
					walls_by_type[INTERSECT_CIRCLE].add(wall);
					first_vertex = OUTSIDE;

			else:
				walls_by_type[BLOCKING].add(wall);
				angle_points.add(vertex);
				if first_vertex == OUTSIDE:
					walls_by_type[INTERSECT_CIRCLE].add(wall);
				first_vertex = WITHIN;

	return (angle_points, walls_by_type);

def inside_bounding_circle(agent, wall):
	v = ((wall[1][0] - wall[0][0]), (wall[1][1] - wall[0][1]));
	center = agent.position;
	pt_v = ((center[0] - wall[0][0]), (center[1] - wall[0][1]));
	v_magn = vo.magnitude(v);
	unit_v = vo.unit_vector(v)
	scalar_projection = pt_v[0] * unit_v[0] + pt_v[1] * unit_v[1];
	if scalar_projection < 0: closest = wall[0];
	elif scalar_projection > v_magn: closest = wall[1];
	else:
		proj_v = ((unit_v[0] * scalar_projection), (unit_v[1] * scalar_projection));
		closest = ((wall[0][0] + proj_v[0]), (wall[0][1] + proj_v[1]));
	dist_v = vo.magnitude(((center[0] - closest[0]), (center[1] - closest[1])));
	if dist_v < agent.vision_range:
	   return True;
	return False;

def get_circle_intersections(agent, walls):
	angle_points = [];
	blocking_walls = [];

	for wall in walls:
		intersection = intersects_circle(agent, wall);
		if intersection:
			blocking_walls.append(wall);
			for x in intersection:
				if x != -1:
					angle_points.append(x);

	return (angle_points, blocking_walls);

def intersects_circle(agent, wall):
	center = agent.position;
	radius = agent.vision_range;
	d = ((wall[1][0] - wall[0][0]), (wall[1][1] - wall[0][1]));
	f = ((wall[0][0] - center[0]), (wall[0][1] - center[1]));
	a = vo.dot_product(d, d);
	b = 2 * vo.dot_product(d, f);
	c = vo.dot_product(f, f) - radius * radius;
	discriminant = b*b - 4*a*c;

	if discriminant < 0:
		return None;
	else:
		factor = 1 / (2*a);
		discriminant = sqrt(discriminant);
		t1 = (-b - discriminant) * factor;
		t2 = (-b + discriminant) * factor;
		point1 = ((wall[0][0] + t1 * d[0]), (wall[0][1] + t1 * d[1]));
		point2 = ((wall[0][0] + t2 * d[0]), (wall[0][1] + t2 * d[1]));

		if (t1 >= 0 and t1 <= 1) and (t2 >= 0 and t2 <= 1):
			return (point1, point2);
			
		elif (t1 >= 0 and t1 <= 1) and (t2 < 0 or t2 > 1):
			return (point1, -1);

		elif (t1 < 0 or t1 > 1) and (t2 >= 0 and t2 <= 1):
			return (-1, point2);

	return None;

def get_intersection(agent, ray, segment):

	r_ptx = ray[0][0];
	r_pty = ray[0][1];
	r_dx = ray[1][0] - ray[0][0];
	r_dy = ray[1][1] - ray[0][1];

	sg_ptx = segment[0][0];
	sg_pty = segment[0][1];
	sg_dx = segment[1][0] - segment[0][0];
	sg_dy = segment[1][1] - segment[0][1];

	r_mag = vo.magnitude((r_dx, r_dy));
	sg_mag = vo.magnitude((sg_dx, sg_dy));
	if (r_dx / r_mag == sg_dx / sg_mag) and (r_dy / r_mag == sg_dy / sg_mag):
		return None;

	t2 = (r_dx * (sg_pty - r_pty) + r_dy * (r_ptx - sg_ptx)) / (sg_dx * r_dy - sg_dy * r_dx);
	t1 = (sg_ptx + sg_dx * t2 - r_ptx) / (r_dx);

	factor = t1;

	if t1 <= 0:
		return None;
	if t2 < 0 or t2 > 1:
		return None
	#if t1 * t1 * (r_dx * r_dx + r_dy * r_dy) > agent.vision_range * agent.vision_range:
		#factor = sqrt(agent.vision_range / (r_dx * r_dx + r_dy * r_dy));

	x = r_ptx + r_dx * factor;
	y = r_pty + r_dy * factor;

	return ((x, y), t1);