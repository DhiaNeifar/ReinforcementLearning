# game_manager.py

# -*- coding: utf-8 -*-
# Author: Dhia Neifar <neifar@umich.edu>


from typing import List
import pygame

from enums.colors import Color


class GameManager(object):
    def __init__(self, caption, height=960, width=1280, BackgroundColor=Color.WHITE.value, fps=120) -> None:
        """
        Constructor of class GameManager.
        Game Manager is used to regulate the global parameters, handle the objects to be drawn i.e. Rubik's Cube.
        It provides surface needed for objects to be drawn on similar to a canvas.
        It handles events such as mouse, keyboard events.

        :param caption: Name of the game
        :param height: Height of the window
        :param width: Width of the window
        :param BackgroundColor: Default background color of the window
        :param fps: Frames per second for buffering the window
        """

        pygame.init()

        self.CAPTION = caption
        pygame.display.set_caption(self.CAPTION)

        self.WIDTH = width
        self.HEIGHT = height
        self.Surface: pygame.Surface = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

        self.BackgroundColor = BackgroundColor

        self.clock = pygame.time.Clock()
        self.FPS = fps
        self.clock_fps = None

        self.running = True

        self.objects = []

    @property
    def surface(self) -> pygame.Surface:
        """
        Surface Getter
        :return: Surface of the game
        """

        return self.Surface


    def run(self) -> None:
        """
        Main Game Loop. Controlled by attribute running.
        :return: None
        """

        while self.running:
            self.handle_events()
            self.update()
            self.clock_fps = self.clock.get_fps()
            self.draw()
            self.clock.tick(self.FPS)


    def handle_events(self) -> None:
        """
        Method that handles events triggered by keyboard.
        When Q key is clicked, the game is quit.

        :return: None
        """

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.running = False
                else:
                    for object_ in self.objects:
                        object_.KeyTrigger(event.key)


    def update(self) -> None:
        """
        Method update is used to update the objects for the game.
        The method is called for every frame.

        :return: None
        """

        for object_ in self.objects:
            object_.update()
        pass


    def draw(self) -> None:
        """
        Method draw is responsible for drawing the objects on the surface.
        First, it clears the surface and fills it with default background color.
        It includes also the fps drawn in the top-left corner of the window.

        :return: None
        """

        self.Surface.fill(self.BackgroundColor)

        # Display FPS
        font = pygame.font.Font(None, 30)
        fps_text = font.render(f"FPS: {self.clock_fps:.2f}", True, Color.BLACK.value)
        self.Surface.blit(fps_text, (10, 10))

        # Draw all game objects
        for object_ in self.objects:
            object_.draw()

        # Flip the display to show the new frame
        pygame.display.flip()

    def AddObjects(self, objects: List) -> None:
        """
        Method AddObjects basically adds the objects (in the form of a list) and saves them.

        :param objects: List of objects to be added.
        :return: None
        """

        self.objects += objects
