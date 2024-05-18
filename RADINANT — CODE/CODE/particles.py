import random, pygame


class Particles:
    def __init__(self, quantity):
        self.bool = []
        self.particles = []
        
        for list in range(0, quantity):
            list = []
            self.particles.append(list)
            self.bool.append(False)

    def particle1(self, screen, particle_number, x, y, speed, size, quantity, decrease_ratio, color):
        if self.bool[particle_number - 1]:
            for i in range(quantity):
                self.particles[particle_number - 1].append([[x, y], [random.randint(-speed, speed) / (speed / (speed / 6)), random.randint(-speed, speed) / (speed / (speed / 6))], random.randint(size[0], size[1])])

        for particle in self.particles[particle_number - 1]:
            particle[0][0] += particle[1][0] * ((particle[2] / decrease_ratio) / 2)
            particle[0][1] += particle[1][1] * ((particle[2] / decrease_ratio) / 2)
            particle[2] -= 0.5 / decrease_ratio

            pygame.draw.circle(screen, color, particle[0], particle[2])

            if particle[2] <= 0:
                self.particles[particle_number - 1].remove(particle)