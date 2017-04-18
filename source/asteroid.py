import random

import pymunk

from source.constants import *
from source.utilities import *

class Asteroid:
    def __init__(self, space, size):
        self.radius = size * size
        mass = size
        moment = pymunk.moment_for_circle(mass, 0, self.radius)
        self.body = pymunk.Body(mass, moment)

        width, height = Utils.get_screen_size()
        x_pos = random.randint(0, width)
        y_pos = random.randint(0, height)
        self.body.position = (x_pos, y_pos)

        x_vel = random.uniform(-ASTEROID_VEL_LIMIT, ASTEROID_VEL_LIMIT)
        y_vel = random.uniform(-ASTEROID_VEL_LIMIT, ASTEROID_VEL_LIMIT)
        self.body.velocity = (x_vel, y_vel)

        self.shape = pymunk.Circle(self.body, self.radius)
        self.shape.collision_type = CT_ASTEROID

        space.add(self.body, self.shape)

        self.strength = ASTEROID_BASE_STRENGTH * size

    def hit(self, damage):
        self.strength -= damage
        if self.strength < 0:
            print("Asteroid destroyed")
            

    def update(self, space):
        Utils.wrap_body(space, self.body, radius=self.radius)

    def draw(self, screen):
        pass
