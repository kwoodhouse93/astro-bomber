import math

import pygame
import pymunk

from source import game
from source.asteroid import *
from source.constants import *
from source.utilities import TextLabel

class CollisionManager:
    def __init__(self):
        self.om = game.object_manager
        self.screen = game.screen
        game.space.add_collision_handler(CT_BOMBER, CT_ASTEROID).post_solve = self.bomber_asteroid
        game.space.add_collision_handler(CT_ASTEROID, CT_ASTEROID).post_solve = self.asteroid_asteroid
        game.space.add_collision_handler(CT_BULLET, CT_ASTEROID).post_solve = self.bullet_asteroid
        game.space.add_collision_handler(CT_BLAST, CT_ASTEROID).begin = self.blast_asteroid

    def impact_damage(self, arbiter):
        damage = math.sqrt(arbiter.total_ke)

        if damage > MIN_DAMAGE:
            label_x, label_y = arbiter.contact_point_set.points[0].point_a
            label_y = SCREEN_HEIGHT - label_y
            label = TextLabel(str(int(damage)), (label_x, label_y))

            for shape in arbiter.shapes:
                game.object_manager.get_object_from_shape(shape).hit(damage)

    def bomber_asteroid(self, arbiter, space, data):
        if arbiter.is_first_contact:
            self.impact_damage(arbiter)

    def asteroid_asteroid(self, arbiter, space, data):
        if arbiter.is_first_contact:
            pass
            # print(arbiter.shapes)
            # print(arbiter.total_ke)

    def bullet_asteroid(self, arbiter, space, data):
        if arbiter.is_first_contact:
            self.impact_damage(arbiter)

    def blast_asteroid(self, arbiter, space, data):
        print('Blast hit asteroid')
        damage = BOMB_DAMAGE

        label_x, label_y = arbiter.contact_point_set.points[0].point_a
        label_y = SCREEN_HEIGHT - label_y
        label = TextLabel(str(int(damage)), (label_x, label_y))

        print(arbiter.shapes)
        for shape in arbiter.shapes:
            print(shape)
            obj = game.object_manager.get_object_from_shape(shape)
            print(obj)
            if hasattr(obj, 'hit'):
                obj.hit(damage)
        return False
