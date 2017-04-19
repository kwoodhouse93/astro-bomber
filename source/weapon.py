import pygame
import pymunk
from pymunk.vec2d import Vec2d

from source import game
from source.constants import *
from source.utilities import *

class Projectile:
    def __init__(self, position, impulse):
        self.radius = BULLET_RADIUS
        mass = BULLET_MASS
        moment = pymunk.moment_for_circle(mass, 0, self.radius)
        self.body = pymunk.Body(mass, moment)
        self.body.position = position

        self.shape = pymunk.Circle(self.body, self.radius)
        self.shape.collision_type = CT_BULLET

        game.space.add(self.body, self.shape)
        self.strength = BULLET_STRENGTH

        self.body.apply_impulse_at_world_point(impulse)

        game.object_manager.register(self)

    def update(self):
        Utils.remove_if_outside_game_area(self.body, self, self.radius)

    def hit(self, damage):
        self.strength -= damage
        if self.strength < 0:
            game.object_manager.unregister(self)

    def delete(self):
        print('Bullet removed')
        game.space.remove(self.body, self.shape)

    def draw(self):
        draw_tuple = Utils.vec2d_to_draw_tuple(self.body.position)
        pygame.draw.circle(game.screen, (255, 255, 255), draw_tuple, self.radius)

class PrimaryCannon:
    def __init__(self, parent):
        self.parent = parent
        game.object_manager.register(self)
        self.cannon_power = CANNON_POWER

    def activate(self):
        position = self.pos
        local_impulse = Vec2d(0, CANNON_POWER)
        parent_angle = self.parent.body.angle
        impulse = self.parent.body.velocity + local_impulse.rotated(parent_angle)

        Projectile(position, impulse)

    def update(self):
        parent_pos = self.parent.body.position
        parent_angle = self.parent.body.angle
        local_offset = Vec2d(0, BOMBER_HEIGHT/2)
        self.pos = parent_pos + (local_offset.rotated(parent_angle))
        self.draw_pos = Utils.vec2d_to_draw_tuple(self.pos)

    def delete(self):
        pass

    def draw(self):
        pygame.draw.circle(game.screen, (255, 0, 0), self.draw_pos, 1)
