import random

import pymunk

from source.constants import *
from source.utilities import *

class Asteroid:
    def __init__(self, size):
        self.radius = size * size
        mass = ASTEROID_BASE_MASS * size
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

        game.space.add(self.body, self.shape)

        self.strength = ASTEROID_BASE_STRENGTH * size

    def hit(self, damage):
        self.strength -= damage
        if self.strength < 0:
            print("Asteroid destroyed")
            game.object_manager.unregister(self)

    def delete(self):
        game.space.remove(self.body, self.shape)
        # if self.size > 3:
            # Spawn between 2 and 5 smaller asteroids
            # Find a way to split the size into

    def update(self):
        Utils.wrap_body(self.body, radius=self.radius)

    def draw(self):
        pass
