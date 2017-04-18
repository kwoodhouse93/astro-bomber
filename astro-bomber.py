import sys

import pygame
from pygame.locals import *

import pymunk
from pymunk import pygame_util

from source.asteroid import *
from source.bomber import *
from source.event_manager import *

def main():
    pygame.init()
    screen = pygame.display.set_mode((1000,600))
    pygame.display.set_caption("AstroBomber")
    clock = pygame.time.Clock()

    space = pymunk.Space()
    space.gravity = (0.0, 0.0)

    event_manager = EventManager()
    event_manager.register(QUIT, lambda e: sys.exit(0))
    event_manager.register_keydown(K_ESCAPE, lambda e: sys.exit(0))


    bomber = Bomber(event_manager)
    space.add(bomber.body, bomber.shape)
    asteroid = Asteroid(8)
    space.add(asteroid.body, asteroid.shape)
    draw_options = pymunk.pygame_util.DrawOptions(screen)

    i = 0

    while True:
        event_manager.handle_events()
        bomber.update(space)
        asteroid.update(space)
        # print('Step ' + unicode(i))
        space.step(1/50.0)

        screen.fill((0,0,0))
        # bomber.draw(screen)
        space.debug_draw(draw_options)

        pygame.display.flip()
        clock.tick(50)
        i += 1

if __name__ == '__main__':
    sys.exit(main())
