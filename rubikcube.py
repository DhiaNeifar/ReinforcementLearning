import numpy as np
import pygame
from pygame.cursors import diamond

from colors import Color
from __init__ import WIDTH, HEIGHT
from cube import Cube
from point import Point3d
from utils import draw_circle


def  main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    clock = pygame.time.Clock()
    center = Point3d(0, 0, 0)
    diameter = 50
    cube = Cube(center, diameter, screen)
    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(Color.WHITE.value)
        cube.draw()
        # draw_circle(screen, 245, 245, 200, Color.BLACK.value)
        # pygame.draw.line(screen, Color.BLUE.value, (100, 0), (WIDTH, HEIGHT))
        # point = np.array([265, 345])
        # pygame.draw.circle(screen, Color.BLACK.value, point, 30)
        pygame.display.flip()
        clock.tick(60)



if __name__ == "__main__":
    main()
