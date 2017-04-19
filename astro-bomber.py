import random
import sys

import pygame
from pygame.locals import *

import pymunk
from pymunk import pygame_util

from source import game
from source.asteroid import *
from source.bomber import *
from source.collision_manager import *
from source.constants import *
from source.event_manager import *
from source.hud import *
from source.object_manager import *

def main():
    pygame.init()
    game.screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("AstroBomber")
    clock = pygame.time.Clock()

    game.space = pymunk.Space()
    game.space.gravity = (0.0, 0.0)

    game.event_manager = em = EventManager()
    em.register(QUIT, lambda e: sys.exit(0))
    em.register_keydown(K_ESCAPE, lambda e: sys.exit(0))

    game.object_manager = om = ObjectManager()
    bomber = Bomber()
    om.register_player(bomber)

    game.collision_manager = CollisionManager()

    for i in range(10):
        rand_factor = ASTEROID_MAX_SIZE - ASTEROID_MIN_SIZE
        size = (random.random() * rand_factor) + ASTEROID_MIN_SIZE
        Asteroid(size)
        
    hud = HeadsUpDisplay()
    om.register(hud)

    draw_options = pymunk.pygame_util.DrawOptions(game.screen)

    while True:
        game.event_manager.handle_events()
        game.object_manager.update_all()
        for x in range(10):
            game.space.step(1/500.0)

        game.screen.fill((0,0,0))
        game.space.debug_draw(draw_options)
        game.object_manager.draw_all()

        pygame.display.flip()
        clock.tick(50)

if __name__ == '__main__':
    sys.exit(main())
