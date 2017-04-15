import sys
import pygame
from pygame.locals import *
import pymunk

def main():
    pygame.init()
    screen = pygame.display.set_mode((800,600))
    pygame.display.set_caption("AstroBomber")
    clock = pygame.time.Clock()

    space = pymunk.Space()
    space.gravity = (0.0, 0.0)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                sys.exit(0)

            screen.fill((0,0,0))

            space.step(1/50.0)

            pygame.display.flip()
            clock.tick(50)

if __name__ == '__main__':
    sys.exit(main())
