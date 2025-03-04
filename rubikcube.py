import pygame

from colors import Color
from __init__ import WIDTH, HEIGHT
from cube import Cube
from point import Point3d


def  main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    clock = pygame.time.Clock()
    center = Point3d(0, 0, 0)
    diameter = 1
    cube = Cube(center, diameter, screen)
    cube.draw()

    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(Color.WHITE.value)
        cube.draw()
        pygame.display.flip()
        clock.tick(60)



if __name__ == "__main__":
    main()
