import pygame

from source.object_manager import *

class Utils:
    @staticmethod
    def get_screen_size():
        return pygame.display.get_surface().get_size()

    @staticmethod
    def wrap_body(space, body, radius=0):
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
            space.reindex_shapes_for_body(body)


class TextLabel:
    def __init__(self, label, pos, object_manager, lifetime = 1000):
        print(label)
        self.font = pygame.font.SysFont(None, 20)

        self.pos = pos
        self.label = self.font.render(str(label), 1, (255,255,0))

        self.object_manager = object_manager
        self.object_manager.register(self)

        self.birth = pygame.time.get_ticks()
        self.lifetime = lifetime

    def update(self, space):
        age = pygame.time.get_ticks() - self.birth
        if age > self.lifetime:
            self.object_manager.unregister(self)

    def draw(self, screen):
        screen.blit(self.label, self.pos)
