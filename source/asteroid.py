import math
import random

import pymunk

from source.constants import *
from source.utilities import *

class Asteroid:
    def __init__(self, size, position=None):
        print('Creating Asteroid (size='+str(size)+',position='+str(position)+')')
        self.size = size
        self.radius = size * size
        mass = ASTEROID_BASE_MASS * size
        moment = pymunk.moment_for_circle(mass, 0, self.radius)
        self.body = pymunk.Body(mass, moment)

        if position == None:
            width, height = Utils.get_screen_size()
            x_pos = random.randint(0, width)
            y_pos = random.randint(0, height)
            self.body.position = (x_pos, y_pos)
        else:
            self.body.position = position

        x_vel = random.uniform(-ASTEROID_VEL_LIMIT, ASTEROID_VEL_LIMIT)
        y_vel = random.uniform(-ASTEROID_VEL_LIMIT, ASTEROID_VEL_LIMIT)
        self.body.velocity = (x_vel, y_vel)

        self.shape = pymunk.Circle(self.body, self.radius)
        self.shape.collision_type = CT_ASTEROID
        self.shape.friction = ASTEROID_FRICTION

        game.space.add(self.body, self.shape)

        self.strength = ASTEROID_BASE_STRENGTH * size

    def hit(self, damage):
        self.strength -= damage
        if self.strength < 0:
            print("Asteroid destroyed")
            game.object_manager.unregister(self)

    def delete(self):
        # print('Deleting asteroid')
        game.space.remove(self.body, self.shape)

        print('Destroyed radius was ' + str(self.radius))


        # if self.size > (ASTEROID_MIN_SIZE * 3):
        #     new_size = math.sqrt((self.size*self.size) / 3)
        #     print('Spawning 3 asteroids of size ' + str(new_size))
        #     for i in range(3):
        #         rand_factor = random.random()
        #         game.object_manager.register(Asteroid(new_size + rand_factor, self.body.position))
        # if self.size > (ASTEROID_MIN_SIZE * 2):
        #     print('Spawning 2 asteroids of size ' + str(self.size / 2))
        #     for i in range(2):
        #         game.object_manager.register(Asteroid(self.size / 2, self.body.position))

        if self.radius > (ASTEROID_MIN_SIZE * 2)**2:
        # Take the size of the just-destroyed asteroid
            max_radius = remaining = self.radius

            while remaining > ASTEROID_MIN_SIZE**2:
                print('Radius remaining: ' + str(remaining))
                # Take a valid-asteroid-sized chunk that is no bigger than:
                #   half the one just destroyed
                #   the remaining amount of asteroid to build with
                max_new_size = remaining
                # Pick a size between min-size and our new max size
                rand_factor = max_new_size - (ASTEROID_MIN_SIZE**2)
                new_size = (random.random() * rand_factor) + (ASTEROID_MIN_SIZE**2)
                # Take the new size away from the remaining amount
                remaining -= new_size
                # Create the new asteroid
                game.object_manager.register(Asteroid(math.sqrt(new_size), self.body.position))

    def update(self):
        Utils.wrap_body(self.body, radius=self.radius)

    def draw(self):
        pass
