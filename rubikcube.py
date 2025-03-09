import numpy as np
import pygame

from actions.front import RotateFront
from cube import Cube
from point import Point3d
from config import Axes, FPS
from actions.right import RotateRight


class RubikCube(object):
    def __init__(self, surface):
        self._surface = surface
        self._RotationSpeed = FPS
        self.RotationAngle = np.pi / self._RotationSpeed
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
        self.actions = []
        self.counter = []
        self.RotationOrder = [Axes["X axis"], Axes["Y axis"], Axes["Z axis"]]


    def draw(self):
        Planes = [plane for cube in self.cubes for plane in cube.GetPlanes(self.RotationOrder)]
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


    def KeyTrigger(self, key):
        self.actions.append(key)
        self.counter.append(self._RotationSpeed)


    def Rotate(self, action):
        action.ApplyRotation(self)



    def update(self):
        if self.actions:
            key = self.actions[0]

            if key == pygame.K_f or key == pygame.K_g:
                key = 0.5 - (key - pygame.K_f) / (pygame.K_g - pygame.K_f)
                # Z @ X @ Y ||  Rot 2
                self.Rotate(RotateFront(clockwise=key < 0))
                for cube in self.cubes[::3]:
                    cube.rotation[Axes["Z axis"]] -= key * self.RotationAngle
                self.RotationOrder = [Axes["Z axis"], Axes["X axis"], Axes["Y axis"]]

            if key == pygame.K_r or key == pygame.K_e:
                key = 0.5 - (key - pygame.K_e) / (pygame.K_r - pygame.K_e)
                # X @ Y @ Z ||  Rot 0
                self.Rotate(RotateRight(clockwise=key < 0))
                for cube in self.cubes[18:]:
                    cube.rotation[Axes["X axis"]] -= key * self.RotationAngle
                self.RotationOrder = [Axes["X axis"], Axes["Y axis"], Axes["Z axis"]]


            if key == pygame.K_b or key == pygame.K_v:
                key = 0.5 - (key - pygame.K_b) / (pygame.K_v - pygame.K_b)
                # Z @ X @ Y ||  Rot 2
                self.Rotate(RotateRight(clockwise=key > 0))
                for cube in self.cubes[2::3]:
                    cube.rotation[Axes["Z axis"]] += key * self.RotationAngle
                self.RotationOrder = [Axes["Z axis"], Axes["X axis"], Axes["Y axis"]]

            if key == pygame.K_l or key == pygame.K_k:
                key = 0.5 - (key - pygame.K_k) / (pygame.K_l - pygame.K_k)
                # X @ Y @ Z ||  Rot 0
                self.Rotate(RotateRight(clockwise=key > 0))
                for cube in self.cubes[:9]:
                    cube.rotation[Axes["X axis"]] += key * self.RotationAngle
                self.RotationOrder = [Axes["X axis"], Axes["Y axis"], Axes["Z axis"]]

            if key == pygame.K_u or key == pygame.K_y:
                key = 0.5 - (key - pygame.K_y) / (pygame.K_u - pygame.K_y)
                # Y @ Z @ X ||  Rot 1
                self.Rotate(RotateRight(clockwise=key > 0))
                for cube in self.cubes[:3] + self.cubes[9: 12] + self.cubes[18: 21]:
                    cube.rotation[Axes["Y axis"]] += key * self.RotationAngle
                self.RotationOrder = [Axes["Y axis"], Axes["Z axis"], Axes["X axis"]]

            if key == pygame.K_d or key == pygame.K_s:
                key = 0.5 - (key - pygame.K_d) / (pygame.K_s - pygame.K_d)
                # Y @ Z @ X ||  Rot 1
                self.Rotate(RotateRight(clockwise=key > 0))
                for cube in self.cubes[6: 9] + self.cubes[15: 18] + self.cubes[24:]:
                    cube.rotation[Axes["Y axis"]] += key * self.RotationAngle
                self.RotationOrder = [Axes["Y axis"], Axes["Z axis"], Axes["X axis"]]

            self.counter[0] -= 1
            if self.counter[0] < 1:
                self.actions = self.actions[1:]
                self.counter = self.counter[1:]
        # for cube in self.cubes:
        #     for i in range(3):
        #         cube.rotation[i] += 0.01
        pass
