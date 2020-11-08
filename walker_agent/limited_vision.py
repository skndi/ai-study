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
BEHIND = 0;
WITHIN = 1;
OUTSIDE = 2;
SEMICIRCLE = 3;
BLOCKING = 0;
MIGHT_BLOCK = 1;
MIGHT_INTERSECT_ARC = 2;

def calculate_visible_vertices(agent, map):
	visible_vertices = [];
	elements = get_rays(agent, map);
	rays = elements[0];
	walls = elements[1];

	for ray in rays:
		intersection = get_closest_intersection(agent, ray, walls);
		
		if intersection:
			visible_vertices.append(intersection);
	
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
	rays = set();

	obstacles = narrow_culling(agent, map);
	points = obstacles[0];
	walls = obstacles[1];

	for point in points:
		rays.add((agent.position, point));

		#offset = determine_overlap(start, middle, end, (agent, middle));
		#if offset: rays.add(get_rotated_ray((agent, middle), map, offset * 0.00001));
	
	return (rays, walls);

def narrow_culling(agent, map):
	sector_elements = broad_culling(agent, map);
	angle_points = sector_elements[0];
	walls = sector_elements[1];
	blocking_walls = [];

	for wall in walls[BLOCKING]:
		blocking_walls.append(wall);
	arc_intersects = get_arc_intersections(agent, walls[MIGHT_INTERSECT_ARC]);
	for angle_point in arc_intersects[0]:
		angle_points.add(angle_point);
	for wall in arc_intersects[1]:
		blocking_walls.append(wall);
	edge_intersects = get_sector_edge_intersections(agent, walls[MIGHT_BLOCK]);
	for wall in edge_intersects:
		blocking_walls.append(wall);

	return (angle_points, blocking_walls)

def broad_culling(agent, map):
	walls_in_circle = bounding_circle_walls(agent, map);
	sector_elements = get_sector_elements(agent, walls_in_circle);
	
	return sector_elements;

def bounding_circle_walls(agent, map):
	walls_in_bounding_circle = [];

	for obstacle in map:
		for wall in obstacle:
			if intersects_bounding_circle(agent, wall):
				walls_in_bounding_circle.append(wall);

	return walls_in_bounding_circle;

def get_sector_elements(agent, walls):
	radius = agent.vision_range;
	v = ((agent.main_ray[1][0] - agent.main_ray[0][0]), (agent.main_ray[1][1] - agent.main_ray[0][1]));
	e1 = ((agent.clockwise_ray[1][0] - agent.clockwise_ray[0][0]), (agent.clockwise_ray[1][1] - agent.clockwise_ray[0][1]));
	e2 = ((agent.counterclockwise_ray[1][0] - agent.counterclockwise_ray[0][0]), (agent.counterclockwise_ray[1][1] - agent.counterclockwise_ray[0][1]));
	center = agent.position;
	points_in_sector = set();
	walls_by_type =  defaultdict(lambda: set());

	for wall in walls:
		first_vertex = -1;
		for vertex in wall:
			u = ((vertex[0] - center[0]), (vertex[1] - center[1]));
			if (u[0] * v[0] + u[1] * v[1]) < 0:
				if first_vertex == BEHIND:
					continue;
				elif first_vertex == OUTSIDE:
					walls_by_type[MIGHT_INTERSECT_ARC].add(wall);
					walls_by_type[MIGHT_BLOCK].add(wall);
				elif first_vertex == SEMICIRCLE:
					walls_by_type[MIGHT_BLOCK].add(wall);
				first_vertex = BEHIND;

			elif (u[0] * u[0] + u[1] * u[1]) > radius * radius:
				if first_vertex == OUTSIDE or first_vertex == BEHIND or first_vertex == SEMICIRCLE:
					walls_by_type[MIGHT_BLOCK].add(wall);
					walls_by_type[MIGHT_INTERSECT_ARC].add(wall);
				elif first_vertex == WITHIN:
					walls_by_type[MIGHT_INTERSECT_ARC].add(wall);
				first_vertex = OUTSIDE;

			elif sign(e1[0] * u[1] - e1[1] * u[0]) == sign(u[0] * e2[1] - u[1] * e2[0]):
				points_in_sector.add(vertex);
				walls_by_type[BLOCKING].add(wall);
				if first_vertex == OUTSIDE:
					walls_by_type[MIGHT_INTERSECT_ARC].add(wall);
				first_vertex = WITHIN;

			else:
				if first_vertex == BEHIND or first_vertex == SEMICIRCLE:
					walls_by_type[MIGHT_BLOCK].add(wall);
				elif first_vertex == OUTSIDE:
					walls_by_type[MIGHT_BLOCK].add(wall);
					walls_by_type[MIGHT_INTERSECT_ARC].add(wall);
				first_vertex = SEMICIRCLE;
			

	return (points_in_sector, walls_by_type);

def intersects_bounding_circle(agent, wall):
	vec = ((wall[1][0] - wall[0][0]), (wall[1][1] - wall[0][1]));
	center = agent.position;
	pt_v = ((center[0] - wall[0][0]), (center[1] - wall[0][1]));
	vec_magn = sqrt(vec[0] * vec[0] + vec[1] * vec[1]);
	unit_v = ((vec[0] / vec_magn), (vec[1] / vec_magn));
	scalar_projection = pt_v[0] * unit_v[0] + pt_v[1] * unit_v[1];
	if scalar_projection < 0: closest = wall[0];
	elif scalar_projection > vec_magn: closest = wall[1];
	else:
		proj_v = ((unit_v[0] * scalar_projection), (unit_v[1] * scalar_projection));
		closest = ((wall[0][0] + proj_v[0]), (wall[0][1] + proj_v[1]));
	dist_v = sqrt((center[0] - closest[0]) * (center[0] - closest[0]) + (center[1] - closest[1]) * (center[1] - closest[1]));
	if dist_v < agent.vision_range:
	   return 1;
	return 0;

def get_arc_intersections(agent, walls):
	angle_points = [];
	blocking_walls = [];

	for wall in walls:
		intersection = intersects_arc(agent, wall);
		if intersection:
			blocking_walls.append(wall);
			for x in intersection:
				if x != -1:
					angle_points.append(x);

	return (angle_points, blocking_walls);

def intersects_arc(agent, wall):
	center = agent.position;
	radius = agent.vision_range;
	v = ((agent.main_ray[1][0] - agent.main_ray[0][0]), (agent.main_ray[1][1] - agent.main_ray[0][1]));
	d = ((wall[1][0] - wall[0][0]), (wall[1][1] - wall[0][1]));
	f = ((wall[0][0] - center[0]), (wall[0][1] - center[1]));
	a = d[0] * d[0] + d[1] * d[1];
	b = 2 * (f[0] * d[0] + f[1] * d[1]);
	c = (f[0] * f[0] + f[1] * f[1]) - radius * radius;
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
		clockwise_vec = ((agent.clockwise_ray[1][0] - agent.clockwise_ray[0][0]), (agent.clockwise_ray[1][1] - agent.clockwise_ray[0][1]));
		counterclockwise_vec = ((agent.counterclockwise_ray[1][0] - agent.counterclockwise_ray[0][0]), (agent.counterclockwise_ray[1][1] - agent.counterclockwise_ray[0][1]));
		start_angle = -atan2(clockwise_vec[1], clockwise_vec[0]);
		end_angle = -atan2(counterclockwise_vec[1], counterclockwise_vec[0]);
		point1_angle = -atan2(point1[1], point1[0]);
		point2_angle = -atan2(point2[1], point2[0]);
		u1 = ((point1[0] - center[0]), (point1[1] - center[1]));
		u2 = ((point2[0] - center[0]), (point2[1] - center[1]));

		if start_angle < end_angle:

			if (t1 >= 0 and t1 <= 1) and (t2 >= 0 and t2 <= 1):
				if u1[0] * v[0] + u1[1] * v[1] < 0 and u2[0] * v[1] + u2[1] * v[1]< 0:
					return None;
				elif end_angle <= point1_angle <= start_angle and not end_angle <= point2_angle <= start_angle:
					return (point1, -1);
				elif not end_angle <= point1_angle <= start_angle and end_angle < point2_angle <= start_angle:
					return (-1, point2);
				elif end_angle <= point1_angle <= start_angle and end_angle <= point2_angle <= start_angle:
					return (point1, point2);
			
			elif (t1 >= 0 and t1 <= 1) and (t2 < 0 or t2 > 1):
				if end_angle <= point1_angle <= start_angle:
					return (point1, -1);

			elif (t1 < 0 or t1 > 1) and (t2 >= 0 and t2 <= 1):
				if end_angle <= point2_angle <= start_angle:
					return (-1, point2);
		else:
			if (t1 >= 0 and t1 <= 1) and (t2 >= 0 and t2 <= 1):
				if u1[0] * v[0] + u1[1] * v[1] < 0 and u2[0] * v[1] + u2[1] * v[1]< 0:
					return None;
				elif end_angle >= point1_angle >= start_angle and not end_angle >= point2_angle >= start_angle:
					return (point1, -1);
				elif not end_angle >= point1_angle >= start_angle and end_angle >= point2_angle >= start_angle:
					return (-1, point2);
				elif end_angle >= point1_angle >= start_angle and end_angle >= point2_angle >= start_angle:
					return (point1, point2);
			
			elif (t1 >= 0 and t1 <= 1) and (t2 < 0 or t2 > 1):
				if end_angle >= point1_angle >= start_angle:
					return (point1, -1);

			elif (t1 < 0 or t1 > 1) and (t2 >= 0 and t2 <= 1):
				if end_angle >= point2_angle >= start_angle:
					return (-1, point2);
			
	return None;

def get_sector_edge_intersections(agent, walls):
	blocking_walls = [];
	for wall in walls:
		intersection1 = get_intersection(agent, agent.counterclockwise_ray, wall);
		intersection2 = get_intersection(agent, agent.clockwise_ray, wall);
		if intersection1 or intersection2:
			blocking_walls.append(wall);
	return blocking_walls;

def get_intersection(agent, ray, segment):

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

	factor = t1;

	if t1 <= 0:
		return None;
	if t2 < 0 or t2 > 1:
		return None
	if t1 * t1 * (r_dx * r_dx + r_dy * r_dy) > agent.vision_range * agent.vision_range:
		factor = sqrt(agent.vision_range / (r_dx * r_dx + r_dy * r_dy));

	x = r_ptx + r_dx * factor;
	y = r_pty + r_dy * factor;

	return ((x, y), t1);

def get_rotated_ray(ray, radians):
	ray_start = ray[0];
	ray_end = ray[1];
	angle = radians
	st_x = ray_start[0];
	st_y = ray_start[1];
	e_x = ray_end[0];
	e_y = ray_end[1];
	sin_a = sin(angle);
	cos_a = cos(angle);
	x_out = ((cos_a *  e_x) - (sin_a *  e_y) + st_x - (cos_a * ( st_x)) + (sin_a * (st_y)));
	y_out = ((sin_a *  e_x) + (cos_a *  e_y) + st_y - (sin_a * ( st_x)) - (cos_a * ( st_y)));

	return ((st_x, st_y), (x_out, y_out));

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
