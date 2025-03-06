import pygame

from point import Point3d
from colors import Color



class Edge(object):
    def __init__(self, point1: Point3d, point2: Point3d, EdgeColor=Color.GREEN.value):
        self.start = (point1.x, point1.y)
        self.end = (point2.x, point2.y)
        self.EdgeColor = EdgeColor

    def draw(self, surface, width=5):
        pygame.draw.line(surface, self.EdgeColor, self.start, self.end, width)