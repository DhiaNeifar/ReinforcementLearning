# plane.py

# -*- coding: utf-8 -*-
# Author: Dhia Neifar <neifar@umich.edu>


import numpy as np
import pygame
from typing import List


from point import Point3d
from edge import Edge


class Plane(object):
    def __init__(self,
                 vertices: List[Point3d],
                 edges: List[Edge],
                 Coordinates,
                 surface:pygame.Surface,
                 PlaneColor) -> None:
        """
        Constructor for Plane. A cube contains 6 planes. A plane contains 4 vertices and 4 edges.

        :param vertices: Vertices of the plane
        :param edges:  Edges of the plane
        :param Coordinates: Coordinates of the vertices
        :param surface: pygame.Surface we use to draw the plane
        :param PlaneColor: Color of the plane
        """

        self.vertices = vertices
        self.edges = edges
        self.Coordinates = Coordinates
        self.surface = surface
        self.PlaneColor = PlaneColor

        assert self.vertices.__len__() == 4, \
            f"Expected number of Points defining a plane is 4 instead of {self.vertices.__len__()}."
        assert self.edges.__len__() == 4, \
            f"Expected number of Edges defining a plane is 4 instead of {self.edges.__len__()}."
        assert self.Coordinates.shape == (4, 3), \
            f"Expected shape of Coordinates passed to the plane (4, 3) instead of {self.Coordinates.shape}"

    def GetAverageZ(self) -> np.float64:
        """
        Method used to calculate the average z value of the 4 vertices of plane.

        :return: Average z value of the 4 vertices of plane.
        """

        return np.average(self.Coordinates[:, 2], axis=0)

    def GetNormal(self) -> np.ndarray:
        """
        Method used to calculate the normal vector of the 4 vertices of plane.
        For example, for first plane, we calculate the Normal of plane 0 which is Front. Front Plane contains vertices 0, 1, 2, 3.
        (Check the shape of the cube in cube.py for reference).
        We use point 0 and point 1 to create vector0: point1 - point0
        We use point 0 and point 3 to create vector1: point3 - point0
        We use vect0 and vect1 to create Normal.

        :return: We return normalized Normal vector
        """

        point0 = self.Coordinates[0, :]
        point1 = self.Coordinates[1, :]
        point3 = self.Coordinates[3, :]

        vector0 = point1 - point0
        vector1 = point3 - point0

        Normal = np.cross(vector1, vector0)
        return Normal / np.linalg.norm(Normal)


    def draw(self, CameraPosition=Point3d(0, 0, 0)) -> None:
        """
        Method used to draw the plane on the surface.
        CameraPosition is always initiated to Point3d(0, 0, 0).
        First, we measure the normal of a plane.
        Second, we measure the vector: point0 - CameraPosition
        Third, we measure the similarity between Normal and vector using the dot product.
        If the dot product is positive, we draw the plane which has the shape of a Polygon with 4 vertices.
        if the dot product is negative, we refrain from drawing the plane.
        Finally, we draw the edges and the vertices to make the cube look clear.
        :param CameraPosition:

        :return: None
        """
        Normal = self.GetNormal()

        point0 = self.Coordinates[0, :]
        vector = point0 - CameraPosition.to_numpy()

        dot_product = np.dot(Normal, vector)

        if dot_product < 0:
            pygame.draw.polygon(self.surface, self.PlaneColor, [(vertex.x, vertex.y) for vertex in self.vertices], 0)
            for edge in self.edges:
                edge.draw(self.surface)
            for vertex in self.vertices:
                vertex.draw(self.surface)
