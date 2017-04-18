import math

import pygame
import pymunk

from source.constants import *
from source.utilities import TextLabel

class CollisionManager:
    def __init__(self, space, object_manager, screen):
        self.om = object_manager
        self.screen = screen
        space.add_collision_handler(CT_BOMBER, CT_ASTEROID).post_solve = self.bomber_asteroid
        space.add_collision_handler(CT_ASTEROID, CT_ASTEROID).post_solve = self.asteroid_asteroid

    def bomber_asteroid(self, arbiter, space, data):
        if arbiter.is_first_contact:
            damage = math.sqrt(arbiter.total_ke)

            if damage > MIN_DAMAGE:
                label_x, label_y = arbiter.contact_point_set.points[0].point_a
                label_y = SCREEN_HEIGHT - label_y
                label = TextLabel(str(int(damage)), (label_x, label_y), self.om)

                for shape in arbiter.shapes:
                    self.om.get_object_from_shape(shape).hit(damage)

    def asteroid_asteroid(self, arbiter, space, data):
        if arbiter.is_first_contact:
            pass
            # print(arbiter.shapes)
            # print(arbiter.total_ke)
