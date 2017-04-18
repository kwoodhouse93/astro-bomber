import random

import pymunk

from source.utilities import *

ASTEROID_VEL_LIMIT = 100

class Asteroid:
    def __init__(self, size):
        radius = size * size
        mass = size
        moment = pymunk.moment_for_circle(mass, 0, radius)
        self.body = pymunk.Body(mass, moment)
        self.body.position = (200, 100)
        x_vel = random.uniform(-ASTEROID_VEL_LIMIT, ASTEROID_VEL_LIMIT)
        y_vel = random.uniform(-ASTEROID_VEL_LIMIT, ASTEROID_VEL_LIMIT)
        self.body.velocity = (x_vel, y_vel)

        self.shape = pymunk.Circle(self.body, radius)

    def update(self, space):
        Utils.wrap_body(space, self.body)
