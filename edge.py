import pygame
import numpy as np

from point import Point3d
from __init__ import WIDTH, HEIGHT
from colors import Color

TranslationVector = np.array([WIDTH // 2, HEIGHT // 2], dtype=np.int32)


class Edge:
    def __init__(self, point1: Point3d, point2: Point3d, EdgeColor: Color.GREEN.value):
        self.start = (point1.x, point1.y)
        self.end = (point2.x, point2.y)
        self.EdgeColor = EdgeColor

    def to_numpy(self):
        return np.array([self.start, self.end], dtype=np.int32)

    def translate(self):
        return self.to_numpy() + TranslationVector

    def draw(self, surface, width=5):
        edge = self.translate()
        pygame.draw.line(surface, self.EdgeColor, edge[0,:], edge[1, :], width)