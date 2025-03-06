import numpy as np
from typing import List

from config import WIDTH, HEIGHT
from point import Point3d
from edge import Edge


class Plane(object):
    def __init__(self, vertices: List[Point3d], edges: List[Edge], Coordinates, surface, PlaneColor):
        self._vertices = vertices
        self._edges = edges
        self._Coordinates = Coordinates
        self._surface = surface
        self.PlaneColor = PlaneColor
        assert self._vertices.__len__() == 4, \
            f"Expected number of Points defining a plane is 4 instead of {self._vertices.__len__()}."
        assert self._edges.__len__() == 4, \
            f"Expected number of Edges defining a plane is 4 instead of {self._edges.__len__()}."
        assert self._Coordinates.shape == (4, 3), \
            f"Expected shape of Coordinates passed to the plane (4, 3) instead of {self._Coordinates.shape}"


    def GetNormal(self):
        point0 = self._Coordinates[0, :]
        point1 = self._Coordinates[1, :]
        point3 = self._Coordinates[3, :]
        Normal = np.cross((point3 - point0), (point1 - point0))
        return Normal / np.linalg.norm(Normal)


    def draw(self, CameraPosition=Point3d(0, 0, 0)):
        Normal = self.GetNormal()
        dot_product = np.dot(Normal, (self._Coordinates[0, :] - CameraPosition.to_numpy()))
        # print("Point coordinates ", self._Coordinates[0, :])
        # print("Normal vector ", Normal)
        # print("dot_product ", dot_product)

        if dot_product < 0:
            for edge in self._edges:
                edge.draw(self._surface)
            for vertex in self._vertices:
                vertex.draw(self._surface)
        pass