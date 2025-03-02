import pygame

class Point3d:
    def __init__(self, x, y, z, PointsColor):
        self.x = x
        self.y = y
        self.z = z
        self.PointsColor = PointsColor

    def draw(self, surface, width=1):
        pygame.draw.circle(surface, self.PointsColor, (self.x, self.y), width)