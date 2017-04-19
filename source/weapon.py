import pygame
import pymunk
from pymunk.vec2d import Vec2d

from source import game
from source.constants import *
from source.utilities import *

class Projectile:
    def __init__(self, position, velocity, impulse):
        self.radius = BULLET_RADIUS
        mass = BULLET_MASS
        moment = pymunk.moment_for_circle(mass, 0, self.radius)
        self.body = pymunk.Body(mass, moment)
        self.body.position = position

        self.shape = pymunk.Circle(self.body, self.radius)
        self.shape.collision_type = CT_BULLET

        game.space.add(self.body, self.shape)
        self.strength = BULLET_STRENGTH

        self.body.velocity = velocity
        self.body.apply_impulse_at_world_point(impulse)

        game.object_manager.register(self)

    def update(self):
        Utils.remove_if_outside_game_area(self.body, self, self.radius)

    def hit(self, damage):
        self.strength -= damage
        if self.strength < 0:
            game.object_manager.unregister(self)

    def delete(self):
        # print('Bullet removed')
        game.space.remove(self.body, self.shape)

    def draw(self):
        draw_tuple = Utils.vec2d_to_draw_tuple(self.body.position)
        pygame.draw.circle(game.screen, (255, 255, 255), draw_tuple, self.radius)

class Bomb:
    def __init__(self, position, velocity, impulse):
        self.radius = BOMB_RADIUS
        mass = BOMB_MASS
        moment = pymunk.moment_for_circle(mass, 0, self.radius)
        self.body = pymunk.Body(mass, moment)
        self.body.position = position

        self.shape = pymunk.Circle(self.body, self.radius)
        self.shape.collision_type = CT_BOMB

        game.space.add(self.body, self.shape)
        self.strength = BOMB_STRENGTH

        self.body.velocity = velocity
        self.body.apply_impulse_at_world_point(impulse)

        game.object_manager.register(self)

        self.birth = pygame.time.get_ticks()
        self.lifetime = BOMB_TIMER
        self.exploded = False

    def explode(self):
        print('BANG!')
        # BOMB_BLAST_RADIUS

        # # Create blast sensor shape
        self.blast_shape = pymunk.Circle(self.body, BOMB_BLAST_RADIUS)
        self.blast_shape.sensor = True
        self.blast_shape.collision_type = CT_BLAST
        game.space.add(self.blast_shape)
        # game.object_manager.unregister(self)
        self.exploded = True

    def update(self):
        if self.exploded:
            game.object_manager.unregister(self)
        age = pygame.time.get_ticks() - self.birth
        if age > self.lifetime and not self.exploded:
            self.explode()
        Utils.remove_if_outside_game_area(self.body, self, BOMB_BLAST_RADIUS)

    def hit(self, damage):
        self.strength -= damage
        if self.strength < 0:
            self.explode()
            game.object_manager.unregister(self)

    def delete(self):
        print('Bomb removed')
        if hasattr(self, 'blast_shape'):
            game.space.remove(self.blast_shape)
        game.space.remove(self.body, self.shape)

    def draw(self):
        draw_tuple = Utils.vec2d_to_draw_tuple(self.body.position)
        pygame.draw.circle(game.screen, (0, 255, 0), draw_tuple, self.radius)

class PrimaryCannon:
    def __init__(self, parent):
        self.parent = parent
        game.object_manager.register(self)
        self.cannon_power = CANNON_POWER

    def activate(self):
        position = self.pos
        local_impulse = Vec2d(0, CANNON_POWER)
        parent_angle = self.parent.body.angle
        impulse = local_impulse.rotated(parent_angle)
        velocity = self.parent.body.velocity
        Projectile(position, velocity, impulse)

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

class SecondaryBombLauncher:
    def __init__(self, parent):
        self.parent = parent
        game.object_manager.register(self)

    def activate(self):
        position = self.pos
        local_impulse = Vec2d(0, -BOMB_LAUNCHER_POWER)
        parent_angle = self.parent.body.angle
        impulse = local_impulse.rotated(parent_angle)
        velocity = self.parent.body.velocity
        Bomb(position, velocity, impulse)

    def update(self):
        parent_pos = self.parent.body.position
        parent_angle = self.parent.body.angle
        local_offset = Vec2d(0, -BOMBER_HEIGHT/2)
        self.pos = parent_pos + (local_offset.rotated(parent_angle))
        self.draw_pos = Utils.vec2d_to_draw_tuple(self.pos)

    def delete(self):
        pass

    def draw(self):
        pygame.draw.circle(game.screen, (0, 0, 255), self.draw_pos, 3)
