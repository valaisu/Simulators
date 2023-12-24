import pygame
import numpy as np
import random


# gravity and electric constanta
G, k = 10000, 1000
fps = 80
type_to_col = {0: (200, 50, 50), 1: (50, 200, 50), 2: (50, 50, 200)}


class Particle:
    def __init__(self, p_type, mass, x, y, vx, vy, charge):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.p_type = p_type
        self.mass = mass
        self.charge = charge

    def update_speed(self, dt, other_particles, attraction=[-1, -1], repulsion=[-1, -1]):
        """
        Updates the speed of the particle based on the other particles.
        Takes into consideration gravity, electric forces, and optionally other forces
        :param dt: float
        :param other_particles: list[particle]
            List of all particles
        :param attraction: (int, int)
            defines which different particle types attract each other
        :param repulsion: (int, int)
            defines which different particle types repel each other
        :return: None
        """

        for p in other_particles:
            if p.x == self.x and p.y == self.y:
                continue
            dx = p.x - self.x
            dy = p.y - self.y

            dist = np.sqrt(dx**2 + dy**2)
            r2 = dx**2 + dy**2

            # Electric forces
            # f = q1*q2 / r^2
            # Limiting the maximum force prevents massive accelerations when particles get close
            self.vx += dx * min(k * (p.charge * self.charge) / (r2 * dist), 0.001)
            self.vy += dy * min(k * (p.charge * self.charge) / (r2 * dist), 0.001)

            # other forces
            # Not sure if this part is useful, or if the charges do the same thing
            if p.p_type != self.p_type:
                if p.p_type in attraction and self.p_type in attraction:
                    normalized = (dx / dist, dy / dist)
                    self.vx += normalized[0] * 10 / dist
                    self.vy += normalized[1] * 10 / dist

                if p.p_type in repulsion and self.p_type in repulsion:
                    normalized = (dx / dist, dy / dist)
                    self.vx -= normalized[0] * 10 / dist
                    self.vy -= normalized[1] * 10 / dist

            # Gravitational forces
            # Not allowing too high accelerations is essential, otherwise
            # shit hits fan if particles got too close to each other
            f = min((p.mass * self.mass) * G / r2, 0.2)
            fx = f * dx / (np.abs(dx) + np.abs(dy))
            fy = f * dy / (np.abs(dx) + np.abs(dy))
            self.vx += fx / self.mass * dt
            self.vy += fy / self.mass * dt

    def update_position(self, dt):
        """
        Update the position of the particle based on its
        speed and the time step
        :param dt: float
        :return: None
        """
        self.x += self.vx * dt
        self.y += self.vy * dt
        if 0 > self.x or self.x > 800:
            self.vx = -self.vx
        if 0 > self.y or self.y > 600:
            self.vy = -self.vy


WHITE = (255, 255, 255)
RED = (200, 100, 100)


# Initialize Pygame
pygame.init()

# Set the dimensions of the window
width, height = 800, 600
screen = pygame.display.set_mode((width, height))

# Set a title for the window
pygame.display.set_caption('Pygame Window')
clock = pygame.time.Clock()

particles = []
for i in range(0):
    particles.append(Particle(1, 1, random.randint(0, 800), random.randint(0, 600), random.uniform(-10, 10), random.uniform(-10, 10), 0))

for i in range(0):
    particles.append(Particle(0, 1, random.randint(0, 800), random.randint(0, 600), random.uniform(-10, 10), random.uniform(-10, 10), 0))
particles.append(Particle(0, 1, 400, 300, -8, 0, 0))
particles.append(Particle(1, 1, 400, 400, 8, 0, 0))
particles.append(Particle(0, 1, 300, 300, -8, 0, 0))
particles.append(Particle(1, 1, 500, 400, 8, 0, 0))
particles.append(Particle(0, 1, 250, 350, 0, 5, 0))
particles.append(Particle(1, 1, 550, 350, 0, -5, 0))
particles.append(Particle(0, 1, 350, 350, 0, 7, 0))
particles.append(Particle(1, 1, 450, 350, 0, -7, 0))

running = True
while running:
    screen.fill(WHITE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # Update the particles
    for p in particles:
        p.update_speed(0.5, particles)
    for p in particles:
        p.update_position(0.5)
    # Draw
    for p in particles:
        pygame.draw.circle(screen, type_to_col[p.p_type], (int(p.x), int(p.y)), 5)
    pygame.display.flip()
    clock.tick(fps)

# Quit Pygame
pygame.quit()

