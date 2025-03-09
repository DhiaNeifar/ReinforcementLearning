# game.py

from typing import List
import pygame

from colors import Color


class GameManager(object):
    def __init__(self, caption, height=960, width=1280, BackgroundColor=Color.WHITE.value, fps=120):
        pygame.init()

        self.CAPTION = caption
        pygame.display.set_caption(self.CAPTION)

        self.WIDTH = width
        self.HEIGHT = height
        self._surface = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

        self.BackgroundColor = BackgroundColor

        self.clock = pygame.time.Clock()
        self.FPS = fps
        self._fps = None

        self.running = True

        self.objects = []

    @property
    def surface(self) -> pygame.Surface:
        """
        Surface Getter
        :return: Surface of the game
        """

        return self._surface


    def run(self) -> None:
        """
        Main Game Loop. Controlled by attribute running.
        :return: None
        """

        while self.running:
            self._handle_events()
            self._update()
            self._fps = self.clock.get_fps()
            self._draw()
            self.clock.tick(self.FPS)


    def _handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.running = False
                else:
                    for _object in self.objects:
                        _object.KeyTrigger(event.key)


    def _update(self) -> None:
        # Update all game objects
        for _object in self.objects:
            _object.update()
        pass


    def _draw(self) -> None:
        # Clear the screen
        self._surface.fill(self.BackgroundColor)

        # Display FPS
        font = pygame.font.Font(None, 30)
        fps_text = font.render(f"FPS: {self._fps:.2f}", True, Color.BLACK.value)
        self._surface.blit(fps_text, (10, 10))

        # Draw all game objects
        # e.g., self.all_sprites.draw(self.screen)
        for _object in self.objects:
            _object.draw()

        # Flip the display to show the new frame
        pygame.display.flip()

    def AddObjects(self, objects: List):
        self.objects += objects

def main():
    game = GameManager('Game Manager')
    game.run()
    pass


if __name__ == '__main__':
    main()
