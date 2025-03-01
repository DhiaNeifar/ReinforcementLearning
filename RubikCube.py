import pygame

from colors import Color


HEIGHT, WIDTH = 640, 480


def  main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    clock = pygame.time.Clock()

    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(Color.WHITE.value)

        pygame.draw.line(screen, Color.BLUE.value, (100, 0), (WIDTH, HEIGHT))

        pygame.display.flip()
        clock.tick(60)



if __name__ == "__main__":
    main()
