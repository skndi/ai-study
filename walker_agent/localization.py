from math import pi
from random import uniform
from random import choices
from walker_agent import agent
from math import cos
from math import sin
from math import radians
from math import pi

def particle_filter(agent, map):

    action = agent.last_movement;
    observation = agent.visible;
    particles = MCL(agent.particles, action, observation, map);
    pose = average(particles);

    return (pose, particles);

def MCL(particles, last_movement, last_observation, map):
    size = len(particles[0])
    new_particles = choices(particles[0], particles[1], k = size);
    weights = [];

    for particle in new_particles:
        if last_observation:
            add_noise(particle);
            update(particle, last_movement, map);
            weight = weigh(particle, last_observation);
            weights.append(1 / weight);
        else:
            add_noise(particle);
            weights.append(1/size);

    normalize(weights);

    return (new_particles, weights);

def generate_particles(width, height, vision_range, map, particle_count):
    particles = [];
    weights = [];

    for x in range(particle_count):
        new_particle = agent.particle([uniform(2, 598), uniform(2, 598)], uniform(-pi, pi), vision_range, map);
        particles.append(new_particle);
        weights.append(1/particle_count);

    return (particles, weights);

def update(particle, last_movement, map):
    if last_movement == (0, 0):
        return;
    particle.update_position(last_movement, map);

def weigh(particle, last_observation):
    particle_vertices = particle.visible
    weight = 0;

    if len(particle.visible) != len(last_observation):
       return 50;

    else:
        for i in range(len(particle.visible)):
            angle_error = cos(particle_vertices[i][1]) - cos(last_observation[i][1]) + sin(particle_vertices[i][1]) - sin(last_observation[i][1]);
            distance_error = particle_vertices[i][0] - last_observation[i][0]
            weight += distance_error ** 2 * angle_error ** 2;
            
    return weight;

def normalize(weights):
    sum_of_weights = sum(weights);

    for i in range(len(weights)):
        weights[i] /= sum_of_weights;

def average(particles):
    size = len(particles[0]);
    x_sum = 0;
    y_sum = 0;
    angle_sum = 0;

    for i in range(len(particles[0])):
        x_sum += particles[0][i].position[0] * particles[1][i];
        y_sum += particles[0][i].position[1] * particles[1][i];
        angle_sum += particles[0][i].orientation * particles[1][i];

    return (x_sum, y_sum, angle_sum);

def add_noise(particle):
    particle.position[0] += uniform(-1, 1);
    particle.position[1] += uniform(-1, 1);
    angle = uniform(-5, 5);
    angle = radians(angle);
    if -pi < particle.orientation + angle < pi:
        particle.orientation += angle;
