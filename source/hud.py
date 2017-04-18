import pygame

from source import game
from source.constants import *

class HeadsUpDisplay:
    def __init__(self):
        self.elements = []

        hb_pos = (20, 20)
        hb_size = (40, 5)
        hb = HealthBar(hb_pos, hb_size, tracking=game.object_manager.get_player(), max_val=BOMBER_STRENGTH)
        self.elements.append(hb)

    def update(self):
        for el in self.elements:
            el.update()

    def draw(self):
        for el in self.elements:
            el.draw()

class HealthBar:
    def __init__(self, pos, size, tracking=None, max_val=1):
        self.pos = pos
        self.size = size
        self.bg_rect = pygame.Rect(self.pos, self.size)

        self.tracking = tracking
        self.max_val = max_val
        self.tracked_value = self.tracking.strength

        self.value = self.tracked_value / self.max_val

        self.bg_color = (255, 0, 0)
        self.fg_color = (0, 255, 0)

    # Update the size of the foreground rectangle
    def update(self):
        if hasattr(self.tracking, 'strength'):
            self.tracked_value = self.tracking.strength
        else:
            self.tracked_value = 0
        self.value = self.tracked_value / self.max_val

        fg_width = self.size[0] * self.value
        fg_size = (fg_width, self.size[1])
        self.fg_rect = pygame.Rect(self.pos, (fg_width, self.size[1]))

    def draw(self):
        pygame.draw.rect(game.screen, self.bg_color, self.bg_rect)
        pygame.draw.rect(game.screen, self.fg_color, self.fg_rect)
