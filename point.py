import numpy as np
import pygame

from colors import Color


class Point3d:
    def __init__(self, x, y, z, PointsColor=Color.BLACK.value):
        self.x = x
        self.y = y
        self.z = z
        self.PointsColor = PointsColor


    def __repr__(self) -> str:
        """
        Use print Point3d to display the coordinates of the points.
        :return: string
        """

        return f"x = {self.x}, y = {self.y}, z = {self.z}"


    def to_numpy(self) -> np.ndarray:
        """
        Transform Point3d into a numpy array with shape (4,).
        :return: numpy array representing the coordinates of the Point3d.
        """

        return np.array([self.x, self.y, self.z], dtype=np.float16)


    def draw(self, surface, width=5) -> None:
        """
        The Point3d leverages Surface and the circle shape from pygame.
        :param surface: pygame.Surface used for drawing.
        :param width: width of the circle representing the Point3d.
        :return: None
        """

        pygame.draw.circle(surface, self.PointsColor, (self.x, self.y), width)