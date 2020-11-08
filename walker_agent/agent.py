from math import atan2
from math import degrees
from walker_agent import limited_vision_circle
from walker_agent import unlimited_vision
import vector_operations as vo
from math import radians
from pygame.draw import circle
from pygame.draw import line
import copy
from walker_agent import localization
import spatial_hash

class agent(object):
    """description of class"""

    def __init__(self, position, color, map, vision_range, orientation):
        self.estimated_position = (-1, -1);
        self.estimated_orientation = -69;
        self.position = position;
        self.last_position = position;
        self.last_movement = (0, 0);
        self.color = color;
        self.circle = 10;
        self.color = color
        self.orientation = orientation;
        self.vision_range = vision_range;
        self.orientation_reference = ((self.position[0], self.position[1]), (self.position[0] + 1, self.position[1]));
        self.orientation_reference = vo.get_rotated_vector(self.orientation_reference, self.orientation);
        self.orientation_reference_vector = ((self.orientation_reference[1][0] - self.orientation_reference[0][0]), (self.orientation_reference[1][1] - self.orientation_reference[0][1]));
        self.visible = limited_vision_circle.calculate_visible_vertices(self, map);
        self.particles = localization.generate_particles(600, 600, self.vision_range,  map, 500);
        self.localize(map);

    def update_position(self, movement, map):
        self.last_position = copy.copy(self.position);
        self.last_movement = movement;
        position = [0, 0];
        distance = movement[0];
        angle = -radians(movement[1]);
        movement_vector = vo.get_rotated_vector(self.orientation_reference, angle);
        movement_vector = (movement_vector[1][0] - movement_vector[0][0], movement_vector[1][1] - movement_vector[0][1]);
        movement_vector = vo.unit_vector(movement_vector);
        position[0] = self.position[0] + distance * movement_vector[0];
        position[1] = self.position[1] + distance * movement_vector[1];
        if position[0] < 598 and position[0] > 2:
            self.position = (position[0], self.position[1]);
        if position[1] < 598  and position[1] > 2:
            self.position = (self.position[0], position[1]);
        
        self.update_orientation();
        self.update_visible(map);
        self.localize(map);

    def update_orientation(self):
        vec = ((self.position[0] - self.last_position[0]), (self.position[1] - self.last_position[1]));
        self.orientation = atan2(vec[1], vec[0]);
        self.orientation_reference = ((self.position[0], self.position[1]), (self.position[0] + 1, self.position[1]));
        self.orientation_reference = vo.get_rotated_vector(self.orientation_reference, self.orientation);
        self.orientation_reference_vector = ((self.orientation_reference[1][0] - self.orientation_reference[0][0]), (self.orientation_reference[1][1] - self.orientation_reference[0][1]));

    def update_visible(self, map):
        self.visible = limited_vision_circle.calculate_visible_vertices(self, map);

    def localize(self, map):
        results = localization.particle_filter(self, map);
        self.estimated_position = (results[0][0], results[0][1]);
        self.estimated_orientation = results[0][2];
        self.particles = results[1];

    def draw_agent(self, screen):
        circle(screen, self.color, (round(self.position[0]), round(self.position[1])), self.circle, 1);
        circle(screen, self.color, (round(self.position[0]), round(self.position[1])), self.vision_range, 1);
        line(screen, self.color, self.orientation_reference[0], self.orientation_reference[1]);

    def draw_particles(self, screen):
        for x in self.particles[0]:
            circle(screen, (255, 0, 0), (round(x.position[0]), round(x.position[1])), 10, 1);
            line(screen, (255, 0, 0), x.orientation_reference[0], x.orientation_reference[1]);

class particle(object):
    
    def __init__(self, position, orientation, vision_range, map):
        self.position = position;
        self.last_position = position;
        self.orientation = orientation;
        self.orientation_reference = ((self.position[0], self.position[1]), (self.position[0] + 1, self.position[1]));
        self.orientation_reference = vo.get_rotated_vector(self.orientation_reference, self.orientation);
        self.orientation_reference_vector = ((self.orientation_reference[1][0] - self.orientation_reference[0][0]), (self.orientation_reference[1][1] - self.orientation_reference[0][1]));
        self.vision_range = vision_range;
        self.visible = limited_vision_circle.calculate_visible_vertices(self, map);

        
    def update_position(self, movement, map):
        self.last_position = copy.copy(self.position);
        position = [0, 0];
        distance = movement[0];
        angle = -radians(movement[1]);
        movement_vector = vo.get_rotated_vector(self.orientation_reference, angle);
        movement_vector = (movement_vector[1][0] - movement_vector[0][0], movement_vector[1][1] - movement_vector[0][1]);
        movement_vector = vo.unit_vector(movement_vector);
        position[0] = self.position[0] + distance * movement_vector[0];
        position[1] = self.position[1] + distance * movement_vector[1];
        if position[0] < 598 and position[0] > 2:
            self.position = [position[0], self.position[1]];
        if position[1] < 598  and position[1] > 2:
            self.position = [self.position[0], position[1]];
        self.update_orientation();
        self.update_visible(map);
    
    def update_orientation(self):
        vec = ((self.position[0] - self.last_position[0]), (self.position[1] - self.last_position[1]));
        self.orientation = atan2(vec[1], vec[0]);
        self.orientation_reference = ((self.position[0], self.position[1]), (self.position[0] + 1, self.position[1]));
        self.orientation_reference = vo.get_rotated_vector(self.orientation_reference, self.orientation);
        self.orientation_reference_vector = ((self.orientation_reference[1][0] - self.orientation_reference[0][0]), (self.orientation_reference[1][1] - self.orientation_reference[0][1]));

    def update_visible(self, map):
        self.visible = limited_vision_circle.calculate_visible_vertices(self, map);

    