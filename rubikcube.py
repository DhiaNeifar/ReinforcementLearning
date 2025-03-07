from cube import Cube
from point import Point3d


class RubikCube(object):
    def __init__(self, surface):
        self._surface = surface
        self._RotationSpeed = 0.0001 * 60
        self.cubes = [
            Cube(self._surface, Point3d(-1, -1, -1), diameter=1),
            Cube(self._surface, Point3d(-1, -1, 0), diameter=1),
            Cube(self._surface, Point3d(-1, -1, 1), diameter=1),
            Cube(self._surface, Point3d(-1, 0, -1), diameter=1),
            Cube(self._surface, Point3d(-1, 0, 0), diameter=1),
            Cube(self._surface, Point3d(-1, 0, 1), diameter=1),
            Cube(self._surface, Point3d(-1, 1, -1), diameter=1),
            Cube(self._surface, Point3d(-1, 1,  0), diameter=1),
            Cube(self._surface, Point3d(-1, 1, 1), diameter=1),

            Cube(self._surface, Point3d(0, -1, -1), diameter=1),
            Cube(self._surface, Point3d(0, -1, 0), diameter=1),
            Cube(self._surface, Point3d(0, -1, 1), diameter=1),
            Cube(self._surface, Point3d(0, 0, -1), diameter=1),
            Cube(self._surface, Point3d(0, 0, 0), diameter=1),
            Cube(self._surface, Point3d(0, 0, 1), diameter=1),
            Cube(self._surface, Point3d(0, 1, -1), diameter=1),
            Cube(self._surface, Point3d(0, 1, 0), diameter=1),
            Cube(self._surface, Point3d(0, 1, 1), diameter=1),

            Cube(self._surface, Point3d(1, -1, -1), diameter=1),
            Cube(self._surface, Point3d(1, -1, 0), diameter=1),
            Cube(self._surface, Point3d(1, -1, 1), diameter=1),
            Cube(self._surface, Point3d(1, 0, -1), diameter=1),
            Cube(self._surface, Point3d(1, 0, 0), diameter=1),
            Cube(self._surface, Point3d(1, 0, 1), diameter=1),
            Cube(self._surface, Point3d(1, 1, -1), diameter=1),
            Cube(self._surface, Point3d(1, 1, 0), diameter=1),
            Cube(self._surface, Point3d(1, 1, 1), diameter=1),
            # Cube(surface, Point3d(-1, 0, -1), diameter=0.5),
            # Cube(surface, Point3d(0, 0, 0), diameter=0.5),
            # Cube(surface, Point3d(0, 0, 0), diameter=0.5),
            # Cube(surface, Point3d(0, 0, 0), diameter=0.5),
            # Cube(surface, Point3d(0, 0, 0), diameter=0.5),
            # Cube(surface, Point3d(0, 0, 0), diameter=0.5),
            # Cube(surface, Point3d(0, 0, 0), diameter=0.5),
            # Cube(surface, Point3d(0, 0, 0), diameter=0.5),
            # Cube(surface, Point3d(0, 0, 0), diameter=0.5),
            #
            # Cube(surface, Point3d(0, 0, 0), diameter=0.5),
            # Cube(surface, Point3d(0, 0, 0), diameter=0.5),
            # Cube(surface, Point3d(0, 0, 0), diameter=0.5),
            # Cube(surface, Point3d(0, 0, 0), diameter=0.5),
            # Cube(surface, Point3d(0, 0, 0), diameter=0.5),
            # Cube(surface, Point3d(0, 0, 0), diameter=0.5),
            # Cube(surface, Point3d(0, 0, 0), diameter=0.5),
            # Cube(surface, Point3d(0, 0, 0), diameter=0.5),
            # Cube(surface, Point3d(0, 0, 0), diameter=0.5),
        ]

    def draw(self):
        Planes = [plane for cube in self.cubes for plane in cube.GetPlanes()]
        Planes.sort(key=lambda plane_: plane_.GetAverageZ(), reverse=True)
        for plane in Planes:
            plane.draw()


    def update(self):
        for cube in self.cubes:
            for i in range(3):
                cube.rotation[i] += self._RotationSpeed
        pass