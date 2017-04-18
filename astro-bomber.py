import random
import sys

import pygame
from pygame.locals import *

import pymunk
from pymunk import pygame_util

from source.asteroid import *
from source.bomber import *
from source.collision_manager import *
from source.constants import *
from source.event_manager import *
from source.object_manager import *

def main():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("AstroBomber")
    clock = pygame.time.Clock()

    space = pymunk.Space()
    space.gravity = (0.0, 0.0)

    event_manager = EventManager()
    event_manager.register(QUIT, lambda e: sys.exit(0))
    event_manager.register_keydown(K_ESCAPE, lambda e: sys.exit(0))

    object_manager = ObjectManager(screen, space)
    bomber = Bomber(space, event_manager)
    object_manager.register(bomber)

    collision_manager = CollisionManager(space, object_manager, screen)

    for i in range(10):
        size = (random.random() * 5) + 4
        object_manager.register(Asteroid(space, size))
    # asteroid = Asteroid(space, 6)
    # object_manager.register(asteroid)

    draw_options = pymunk.pygame_util.DrawOptions(screen)

    i = 0

    while True:
        event_manager.handle_events()
        # bomber.update(space)
        # asteroid.update(space)
        object_manager.update_all()
        # print('Step ' + unicode(i))
        for x in range(10):
            space.step(1/500.0)

        screen.fill((0,0,0))
        # bomber.draw(screen)
        space.debug_draw(draw_options)
        object_manager.draw_all()

        pygame.display.flip()
        clock.tick(50)
        i += 1

if __name__ == '__main__':
    sys.exit(main())
