from math import sqrt 
from math import acos
from math import sin
from math import cos

def dot_product(u, v):
    return u[0] * v[0] + u[1] * v[1];

def magnitude(u):
    return sqrt(u[0] * u[0] + u[1] * u[1]);

def unit_vector(u):
    magn = magnitude(u);
    return ((u[0] / magn), (u[1] / magn));

def get_rotated_vector(vector, radians):
	vector_start = vector[0];
	vector_end = vector[1];
	angle = radians
	st_x = vector_start[0];
	st_y = vector_start[1];
	e_x = vector_end[0];
	e_y = vector_end[1];
	sin_a = sin(angle);
	cos_a = cos(angle);
	x_out = ((cos_a *  e_x) - (sin_a *  e_y) + st_x - (cos_a * ( st_x)) + (sin_a * (st_y)));
	y_out = ((sin_a *  e_x) + (cos_a *  e_y) + st_y - (sin_a * ( st_x)) - (cos_a * ( st_y)));

	return ((st_x, st_y), (x_out, y_out));

def get_relative_angle(u, v):
	factor = 1;
	d = v[0] * u[1] - v[1] * u[0];
	if d < 0:
		factor = -1;
	cos_a = (dot_product(u, v)) / (magnitude(u) * magnitude(v));

	return factor * acos(cos_a);