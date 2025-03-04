from point import Point3d
from edge import Edge

from colors import Color

class Cube:
    def __init__(self, center: Point3d, diameter: float, surface, PointsColor=Color.BLACK.value, EdgesColor=Color.GREEN.value):
        self.center = center
        self.diameter = diameter
        self.surface = surface
        self.PointsColor = PointsColor
        self.EdgesColor = EdgesColor
        self.vertices = self.GetPoints()
        self.edges = self.GetEdges()

    def GetPoints(self):
        return [
            Point3d(self.center.x - self.diameter / 2, self.center.y - self.diameter / 2, self.center.z - (self.diameter / 2), self.PointsColor),
            Point3d(self.center.x + self.diameter / 2, self.center.y - self.diameter / 2, self.center.z - (self.diameter / 2), self.PointsColor),
            Point3d(self.center.x + self.diameter / 2, self.center.y + self.diameter / 2, self.center.z - (self.diameter / 2), self.PointsColor),
            Point3d(self.center.x - self.diameter / 2, self.center.y + self.diameter / 2, self.center.z - (self.diameter / 2), self.PointsColor),
            Point3d(self.center.x - self.diameter / 2, self.center.y - self.diameter / 2, self.center.z + (self.diameter / 2), self.PointsColor),
            Point3d(self.center.x + self.diameter / 2, self.center.y - self.diameter / 2, self.center.z + (self.diameter / 2), self.PointsColor),
            Point3d(self.center.x + self.diameter / 2, self.center.y + self.diameter / 2, self.center.z + (self.diameter / 2), self.PointsColor),
            Point3d(self.center.x - self.diameter / 2, self.center.y + self.diameter / 2, self.center.z + (self.diameter / 2), self.PointsColor),
        ]

    def GetEdges(self):
        edges = []
        for i in range(4):
            j = i + 1
            k = j % 4
            l = i + 4
            edges.append(Edge(self.vertices[i], self.vertices[k], self.EdgesColor))
            edges.append(Edge(self.vertices[l], self.vertices[k + 4], self.EdgesColor))
            edges.append(Edge(self.vertices[i], self.vertices[l], self.EdgesColor))
        return edges

    def draw(self):
        # for edge in self.edges:
            # edge.draw(self.surface)
        for vertice in self.vertices:
            # vertice.transform()
            vertice.draw(self.surface)
