# cube.py

# -*- coding: utf-8 -*-
# Author: Dhia Neifar <neifar@umich.edu>


import numpy as np
from typing import List

from game import Game
from enums.colors import Color
from point import Point3d
from edge import Edge
from plane import Plane
from config import LocalRotate, PLANES


class Cube(Game):
    def __init__(self,
                 surface,
                 center: Point3d = Point3d(0, 0, 0),
                 diameter: float = 1,
                 VerticesColor=Color.BLACK.value,
                 EdgesColor=Color.GREEN.value,
                 draw_=True) -> None:
        """
        Constructor of class Cube.

        :param surface: pygame.Surface. It is passed as argument to draw cube.
        :param center: Center of the cube initialized to vertex x = 0, y = 0, z = 0.
        :param diameter: Diameter of the cube initialized to 1.
        :param VerticesColor: Color assigned to the vertices of the cube.
        :param EdgesColor: Color assigned to the edges of the cube.
        """

        super().__init__(surface)
        self.center = center
        self.diameter = diameter
        self.surface = surface
        self.vertices = self.GetPoints()
        self.GlobalRotation = [np.pi * 0.0, np.pi * 0.0, np.pi * 0.0]
        self.VerticesColor = VerticesColor
        self.EdgesColor = EdgesColor
        self.draw_ = draw_

    def to_numpy(self) -> np.ndarray:
        """
        Transforms vertices and center of the cube from Point3d to np.ndarray.
        The size of the matrix is (9, 3). Forth column is ones.

        :return: np.ndarray
        """

        vertices: List[Point3d] = self.vertices
        return np.array([vertex.to_numpy() for vertex in vertices], dtype=np.float16)

    @staticmethod
    def from_numpy(CoordinatesMatrix: np.ndarray) -> List[Point3d]:
        """
        The opposite of to_numpy method.
        Transforms a Matrix (9, 3) that contains all 8 vertices of a cube as well as the center into a List[Point3d].
        The list will be used to update self.vertices.
        :param CoordinatesMatrix: Matrix containing Coordinates of all vertices and center of the cube. size is (9, 3).

        :return: List of points
        """
        NumVertices, _ = CoordinatesMatrix.shape
        return [Point3d(*CoordinatesMatrix[row, :3]) for row in range(NumVertices)]

    def GetPoints(self) -> List[Point3d]:
        """
        Extracts the vertices coordinates of the cube.

        :return: List[Point3d] | Length = 9
        """

        return [
            Point3d(self.center.x - self.diameter / 2, self.center.y - self.diameter / 2, self.center.z - (self.diameter / 2)),
            Point3d(self.center.x + self.diameter / 2, self.center.y - self.diameter / 2, self.center.z - (self.diameter / 2)),
            Point3d(self.center.x + self.diameter / 2, self.center.y + self.diameter / 2, self.center.z - (self.diameter / 2)),
            Point3d(self.center.x - self.diameter / 2, self.center.y + self.diameter / 2, self.center.z - (self.diameter / 2)),
            Point3d(self.center.x - self.diameter / 2, self.center.y - self.diameter / 2, self.center.z + (self.diameter / 2)),
            Point3d(self.center.x + self.diameter / 2, self.center.y - self.diameter / 2, self.center.z + (self.diameter / 2)),
            Point3d(self.center.x + self.diameter / 2, self.center.y + self.diameter / 2, self.center.z + (self.diameter / 2)),
            Point3d(self.center.x - self.diameter / 2, self.center.y + self.diameter / 2, self.center.z + (self.diameter / 2)),
            self.center,
        ]

    @staticmethod
    def GetEdges(Vertices: List[Point3d]) -> List[Edge]:
        """
        Method used to get the edges of the cube.

        Shape of the cube:

                    4--------------5
                   /|             /|
                  / |            / |
                 /  |           /  |
                0--------------1   |
                |   |          |   |
                |   7----------|---6
                |  /           |  /
                | /            | /
                3/-------------2/

        Vertex 0 - vertex 1 ==> Edge 1
        Vertex 4 - vertex 5 ==> Edge 2
        Vertex 0 - vertex 4 ==> Edge 3
        Vertex 1 - vertex 2 ==> Edge 4
        Vertex 5 - vertex 6 ==> Edge 5
        Vertex 1 - vertex 5 ==> Edge 6
        Vertex 2 - vertex 3 ==> Edge 7
        Vertex 6 - vertex 7 ==> Edge 8
        Vertex 2 - vertex 6 ==> Edge 9
        Vertex 3 - vertex 0 ==> Edge 10
        Vertex 7 - vertex 4 ==> Edge 11
        Vertex 3 - vertex 7 ==> Edge 12


        :param Vertices: List of Point3d indicating the vertices of the cube.

        :return: List of edges linking the vertices.
        """

        Edges = []
        for i in range(4):
            j = i + 1
            k = j % 4
            l = i + 4
            Edges.append(Edge(Vertices[i], Vertices[k]))
            Edges.append(Edge(Vertices[l], Vertices[k + 4]))
            Edges.append(Edge(Vertices[i], Vertices[l]))
        return Edges


    def GetPlanes(self) -> List[Plane]:
        """
        Method that returns all planes of the cube.
        First, we transform all the vertices of the cube. We keep track of the ZTranslatedCube.
        :return: List of planes
        """

        ScaledCube, ZTranslatedCube = self.transform()
        Vertices: List[Point3d] = self.from_numpy(ScaledCube)
        Edges: List[Edge] = self.GetEdges(Vertices)
        ZTranslatedCube = ZTranslatedCube[:, :3]
        return [Plane([Vertices[i] for i in plane["Vertices"]],
                      [Edges[i] for i in plane["Edges"]],
                      ZTranslatedCube[plane["Vertices"]],
                      self.surface,
                      plane["Color"],) for plane in PLANES]


    def draw(self) -> None:
        """
        Draws the cube.
        Transforms the cube and draws the edges and the points.

        :return: None
        """
        Planes: List[Plane] = self.GetPlanes()
        Planes.sort(key=lambda plane_: plane_.GetAverageZ(), reverse=True)
        for plane in Planes:
            plane.draw()

    def update(self, yaw=0.0001, pitch=0.0001, roll=0.0001):
        self.GlobalRotation[0] +=  yaw
        self.GlobalRotation[1] += pitch
        self.GlobalRotation[2] += roll



    def LocalUpdate(self, RotationAngle, axis):
        Coordinates = self.to_numpy()
        RotatedCube = LocalRotate(Coordinates, RotationAngle, axis)
        self.vertices = self.from_numpy(RotatedCube)
        self.center = self.vertices[-1]

    def GetLayers(self):
        pass

    def __repr__(self):
        print(self.center)