import numpy as np
import pygame

from __init__ import WIDTH, HEIGHT
from colors import Color

TranslationVector = np.array([WIDTH / 2, HEIGHT / 2, 0])


class Point3d:
    def __init__(self, x, y, z, PointsColor=Color.WHITE.value):
        self.x = x
        self.y = y
        self.z = z
        self.PointsColor = PointsColor

    def to_numpy(self):
        return np.array([self.x, self.y, self.z])

    def translate(self):
        return (self.to_numpy() + TranslationVector).astype(int)[:2]

    def draw(self, surface, width=10):
        point = self.translate()
        pygame.draw.circle(surface, self.PointsColor, (point[0], point[1]), width)