import sys
import pygame 
from pygame.locals import QUIT
from data_structures.graph import graph_tools
from voronoi_graph import graph
from obstacles import convex_obstacles
from walker_agent import unlimited_vision
import spatial_hash
import time
from walker_agent import agent
from math import floor
from walker_agent import limited_vision
from math import atan2
import vector_operations as vo

def round(num):
	if (num > 0):
		return int(num+.5)
	else:
		return int(num-.5)

def draw_graph(graphlines, color):
    for x in graphlines:
        pygame.draw.line(win, color, x[0], x[1]);

def draw_vertices(vertices, color):
    for x in vertices:
        pygame.draw.circle(win, color, x, 5);

def draw_map(obstacles, color):
    for obstacle in obstacles:
        for i in range(len(obstacle)):
            draw_graph(obstacle, color);

def draw_grid_lines(width, height):
    for x in range(0, height, 200):
        pygame.draw.line(win, (255, 0, 0), (x, 0), (x, 600))
    for y in range(0, width, 200):
        pygame.draw.line(win, (255, 0, 0), (0, y), (600, y));

def draw_hash_table_zone(hash_table, cell):
    lines = hash_table.get_cell_objects(cell);
    for line in lines:
        pygame.draw.line(win, (0, 255, 0), line[0], line[1]);

def update():
    ag.update_position((1, 0), map);

def render():
    win.fill((0, 0, 0));
    draw_map(map, (255, 255, 255));
    ag.draw_agent(win);
    ag.draw_particles(win);
    pygame.display.update();
    
width = 600;
height = 600;

pygame.init();
pygame.font.init();

win = pygame.display.set_mode((width, height));

def draw_path(path, color):

    for i in range (0, len(path) - 1):
        first_coord = path[i].get_id();
        second_coord = path[i + 1].get_id();
        pygame.draw.line(win, color, first_coord, second_coord, 3);
        pygame.display.update();
        pygame.time.wait(200);

map = convex_obstacles.get_obstacles(width, height, 17);
#map = [(())];
map.append([((1, 1), (width - 1, 1)), ((width - 1, 1), (width - 1, height - 1)), ((width - 1, height - 1), (1, height - 1)), ((1, height - 1), (1, 1))]);
#map.append([((200, 200), (400, 200)), ((400, 200), (200, 400)), ((200, 400), (200, 200))]);
ag = agent.agent([200, 200], (0, 0, 255), map, 100, 1);

pygame.key.set_repeat(10,10);
clock = pygame.time.Clock();

while True:
    
    dt = clock.get_time();
    
    for ev in pygame.event.get():  
        if ev.type == pygame.QUIT: 
            pygame.quit();

    update();
    render();
    
    clock.tick(60);
    

    
    


