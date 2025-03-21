# referential.py

# -*- coding: utf-8 -*-
# Author: Dhia Neifar <neifar@umich.edu>


import pygame
import numpy as np

from game import Game
from point import Point3d
from enums.colors import Color


class Referential(Game):
    def __init__(self,
                 surface: pygame.Surface,
                 XAxis=Point3d(x=2, y=0, z=0),
                 YAxis=Point3d(x=0, y=2, z=0),
                 ZAxis=Point3d(x=0, y=0, z=2),
                 ) -> None:
        """
        Constructor for Referential class.
        Use this in main if a referential is needed to keep up with the orientation of the objects and axes.
        :param surface: pygame.Surface
        :param XAxis: X Axis and where it points to. Initialized at Point3d(2, 0, 0)
        :param YAxis: Y Axis and where it points to. Initialized at Point3d(0, 2, 0)
        :param ZAxis: Z Axis and where it points to. Initialized at Point3d(0, 0, 2)
        """

        super().__init__(surface)
        self.XAxis = XAxis
        self.YAxis = YAxis
        self.ZAxis = ZAxis
        self.surface = surface
        self.GlobalRotation = [0.0, 0.0, 0.0]

    def to_numpy(self) -> np.ndarray:
        """
        Adds the Origin O Point3d(0, 0, 0) to the referential and transforms all points to numpy matrix for coordinates.

        :return: Coordinates Matrix np.ndarray
        """

        return np.array([point.to_numpy() for point in [Point3d(0, 0, 0), self.XAxis, self.YAxis, self.ZAxis]], dtype=np.float16)


    def draw(self):
        """
        Method that draws the Referential on the surface.

        :return:
        """

        ScaledRef, ZTranslated = self.transform()
        pygame.draw.line(self.surface, Color.RED.value,
                         (ScaledRef[0, 0], ScaledRef[0, 1]),  # start at origin
                         (ScaledRef[1, 0], ScaledRef[1, 1]),  # end 100 px to the right
                         5)  # thickness

        # Draw Y-axis (green, going up)
        pygame.draw.line(self.surface, Color.GREEN.value,
                         (ScaledRef[0, 0], ScaledRef[0, 1]),  # start at origin
                         (ScaledRef[2, 0], ScaledRef[2, 1]),
                         5)

        # Draw Z-axis (blue, diagonal down-right)
        # This is just a visual approximation to convey depth.
        pygame.draw.line(self.surface, Color.MAGENTA.value,
                         (ScaledRef[0, 0], ScaledRef[0, 1]),  # start at origin
                         (ScaledRef[3, 0], ScaledRef[3, 1]),
                         5)

    def update(self):
        pass


    def KeyTrigger(self, key):
        pass