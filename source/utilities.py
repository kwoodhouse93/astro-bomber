import pygame

from source import game
from source.constants import *
from source.object_manager import *

class Utils:
    @staticmethod
    def get_screen_size():
        return pygame.display.get_surface().get_size()

    @staticmethod
    def wrap_body(body, radius=0):
        width, height = Utils.get_screen_size()
        new_x = body.position.x
        new_y = body.position.y
        change_pos = False

        if body.position.x < (0 - radius):
            new_x = body.position.x + width + (2*radius)
            change_pos = True
        elif body.position.x > (width + radius):
            new_x = body.position.x - (width + (2*radius))
            change_pos = True
        if body.position.y < (0 - radius):
            new_y = body.position.y + height + (2*radius)
            change_pos = True
        elif body.position.y > (height + radius):
            new_y = body.position.y - (height + (2*radius))
            change_pos = True

        if change_pos:
            body.position = (new_x, new_y)
            game.space.reindex_shapes_for_body(body)

    @staticmethod
    def outside_game_area(body, radius=0):
        width, height = Utils.get_screen_size()
        return body.position.x < (0 - radius) or \
            body.position.x > (width + radius) or \
            body.position.y < (0 - radius) or \
            body.position.y > (height + radius)

    @staticmethod
    def remove_if_outside_game_area(body, obj, radius=0):
        if Utils.outside_game_area(body, radius):
            game.object_manager.unregister(obj)

    @staticmethod
    def vec2d_to_draw_tuple(vec2d):
        x = int(vec2d.x)
        y = int(SCREEN_HEIGHT - vec2d.y)
        return (x, y)

class TextLabel:
    def __init__(self, label, pos, lifetime = 1000):
        # print(label)
        self.font = pygame.font.SysFont(None, 20)

        self.pos = pos
        self.label = self.font.render(str(label), 1, (255,255,0))

        game.object_manager.register(self)

        self.birth = pygame.time.get_ticks()
        self.lifetime = lifetime

    def update(self):
        age = pygame.time.get_ticks() - self.birth
        if age > self.lifetime:
            game.object_manager.unregister(self)

    def delete(self):
        del(self)

    def draw(self):
        game.screen.blit(self.label, self.pos)
