from point import Point3d
from edge import Edge

from colors import Color

class Cube:
    def __init__(self, x, y, z, a, PointsColor=Color.WHITE.value, EdgesColor=Color.WHITE.value):
        self.x = x
        self.y = y
        self.z = z
        self.a = a
        self.PointsColor = PointsColor
        self.EdgesColor = EdgesColor
    
    def GetPoints(self):
        return [
            Point3d(self.x - self.a / 2, self.y - self.a / 2, self.z - (self.a / 2), self.PointsColor),
            Point3d(self.x - self.a / 2, self.y + self.a / 2, self.z - (self.a / 2), self.PointsColor),
            Point3d(self.x + self.a / 2, self.y - self.a / 2, self.z - (self.a / 2), self.PointsColor),
            Point3d(self.x + self.a / 2, self.y + self.a / 2, self.z - (self.a / 2), self.PointsColor),
            Point3d(self.x - self.a / 2, self.y - self.a / 2, self.z + (self.a / 2), self.PointsColor),
            Point3d(self.x - self.a / 2, self.y + self.a / 2, self.z + (self.a / 2), self.PointsColor),
            Point3d(self.x + self.a / 2, self.y - self.a / 2, self.z + (self.a / 2), self.PointsColor),
            Point3d(self.x + self.a / 2, self.y + self.a / 2, self.z + (self.a / 2), self.PointsColor),
        ]

    def GetEdges(self):
        vertices = self.GetPoints()
        edges = []
        for i in range(4):
            j = i + 1
            k = j % 4
            l = i + 4
            edges.append(Edge(vertices[i], vertices[k], self.EdgesColor))
            edges.append(Edge(vertices[l], vertices[k + 4], self.EdgesColor))
            edges.append(Edge(vertices[i], vertices[l], self.EdgesColor))
        pass