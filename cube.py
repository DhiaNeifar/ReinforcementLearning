import numpy as np
from typing import List

from colors import Color
from point import Point3d
from edge import Edge
from plane import Plane
from config import Translate, Project, Scale, Rotate, Pad, LAYERS


class Cube(object):
    def __init__(self, surface, center: Point3d=Point3d(0, 0, 0),
                 diameter: float=1,
                 VerticesColor=Color.BLACK.value,
                 EdgesColor=Color.GREEN.value) -> None:
        """
        Constructor of class Cube.

        :param surface: pygame.Surface. It is passed as argument to draw cube.
        :param center: Center of the cube initialized to point x = 0, y = 0, z = 0.
        :param diameter: Diameter of the cube initialized to 1.
        :param VerticesColor: Color assigned to the vertices of the cube.
        :param EdgesColor: Color assigned to the edges of the cube.
        """

        self.center = center
        self.diameter = diameter
        self.surface = surface
        self.rotation = [0, 0, 0]
        self.VerticesColor = VerticesColor
        self.EdgesColor = EdgesColor


    def to_numpy(self) -> np.ndarray:
        """
        Transforms vertices of the cube from Point3d to NumPy.Ndarray.
        The size of the matrix is (8, 4). Forth column is ones.
        :return: np.ndarray
        """

        vertices: List[Point3d] = self.GetPoints()
        return np.array([vertice.to_numpy() for vertice in vertices], dtype=np.float16)

    @staticmethod
    def from_numpy(array):
        NumVertices = array.shape[0]
        return [Point3d(array[row, 0], array[row, 1], array[row, 2]) for row in range(NumVertices)]

    def GetPoints(self) -> List[Point3d]:
        """
        Extracts the vertices coordinates of the cube.
        :return: List[Point3d]
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
        ]


    def transform(self) -> np.ndarray:
        """
        #TODO: Update the text for ZAxis
        Applies the transformation to the vertices of the cube.
        Translation of z-axis by 3 to be in the field of view Frustum.
        Projects the Matrix using Perspective Projection Matrix.
        Scales the Matrix to pygame screen.

        :return: Coordinates of Points of cube scaled.
        """

        Coordinates = self.to_numpy()
        RotatedCube = Rotate(Coordinates, *self.rotation)
        PaddedCube = Pad(RotatedCube)
        ZTranslatedCube = Translate(PaddedCube, Tx=0.0, Ty=0.0, Tz=10.0)
        ProjectedCube = Project(ZTranslatedCube)
        ScaledCube = Scale(ProjectedCube)
        return ScaledCube, ZTranslatedCube

    @staticmethod
    def GetEdges(Vertices: List[Point3d]) -> List[Edge]:
        Edges = []
        for i in range(4):
            j = i + 1
            k = j % 4
            l = i + 4
            Edges.append(Edge(Vertices[i], Vertices[k]))
            Edges.append(Edge(Vertices[l], Vertices[k + 4]))
            Edges.append(Edge(Vertices[i], Vertices[l]))
        return Edges


    def GetPlanes(self):
        ScaledCube, ZTranslatedCube = self.transform()
        Vertices: List[Point3d] = self.from_numpy(ScaledCube)
        Edges: List[Edge] = self.GetEdges(Vertices)
        ZTranslatedCube = ZTranslatedCube[:, :3]
        return [Plane([Vertices[i] for i in plane["Vertices"]],
                      [Edges[i] for i in plane["Edges"]],
                      ZTranslatedCube[plane["Vertices"]],
                      self.surface,
                      plane["Color"],) for plane in LAYERS]


    def draw(self) -> None:
        """
        Draws the cube.
        Transforms the cube and draws the edges and the points.

        :return: None
        """
        pass
        # ScaledCube, ZTranslatedCube = self.transform()
        # Vertices: List[Point3d] = self.from_numpy(ScaledCube)
        # Edges: List[Edge] = self.GetEdges(Vertices)
        # Planes: List[Plane] = self.GetPlanes(Vertices, Edges, ZTranslatedCube)
        # Planes.sort(key=lambda plane_: plane_.GetAverageZ(), reverse=True)
        # for plane in Planes:
        #     plane.draw()

    def update(self):
        for i in range(3):
            self.rotation[i] += 0.01


    def GetLayers(self):
        pass
