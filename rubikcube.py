import numpy as np
import pygame

from cube import Cube
from point import Point3d
from config import RotationAngle, Axes
from actions.right import RotateRight


class RubikCube(object):
    def __init__(self, surface):
        self._surface = surface
        self._RotationSpeed = 0.001
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
        ]
        self.state = self.InitState()


    def draw(self):
        Planes = [plane for cube in self.cubes for plane in cube.GetPlanes()]
        Planes.sort(key=lambda plane_: plane_.GetAverageZ(), reverse=True)
        for plane in Planes:
            plane.draw()

    @staticmethod
    def InitState():
        """
            Create a 6x3x3 numpy array for a "solved" cube:
              ith Face has all stickers = i.
        """
        cube = np.zeros((6, 3, 3), dtype=np.int8)
        for face in range(6):
            cube[face, :, :] = face
        return cube


    def ActionRequired(self, key):
        if key == pygame.K_r:
            self.Rotate(RotateRight())
            print(self.state)
            for cube in self.cubes[18:]:
                cube.rotation[Axes["X axis"]] += RotationAngle

    def Rotate(self, action):
        action.ApplyRotation(self)



    def update(self):
        for cube in self.cubes:
            for i in range(1):
                cube.rotation[i] += self._RotationSpeed
        pass
