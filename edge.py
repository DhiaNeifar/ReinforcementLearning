# edge.py

# -*- coding: utf-8 -*-
# Author: Dhia Neifar <neifar@umich.edu>


import pygame

from point import Point3d
from enums.colors import Color



class Edge(object):
    def __init__(self,
                 point1: Point3d,
                 point2: Point3d,
                 EdgeColor=Color.BLACK.value) -> None:
        """
        Constructor of Edge.
        :param point1:
        :param point2:
        :param EdgeColor:
        """

        self.start = (point1.x, point1.y)
        self.end = (point2.x, point2.y)
        self.EdgeColor = EdgeColor

    def draw(self, surface: pygame.Surface, width=2) -> None:
        """
        Draw method of Edge.
        :param surface: pygame.Surface
        :param width: Width of the edge

        :return: None
        """

        pygame.draw.line(surface, self.EdgeColor, self.start, self.end, width)