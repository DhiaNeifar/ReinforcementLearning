import numpy as np
import pygame

from cube import Cube
from point import Point3d
from config import Axes, FPS, layers


class RubikCube(object):
    def __init__(self, surface):
        self._surface = surface
        self._RotationSpeed = FPS
        self.RotationAngle = np.pi / self._RotationSpeed
        self.cubes = [
            Cube(self._surface, Point3d(x=-1.0, y=-1.0, z=-1.0), diameter=1, draw=True, Face=layers["FRONT"]),
            Cube(self._surface, Point3d(x=-1.0, y=-1.0, z= 0.0), diameter=1, draw=True, Face=layers["LEFT"]),
            Cube(self._surface, Point3d(x=-1.0, y=-1.0, z= 1.0), diameter=1, draw=True, Face=layers["FRONT"]),
            Cube(self._surface, Point3d(x=-1.0, y= 0.0, z=-1.0), diameter=1, draw=True, Face=layers["FRONT"]),
            Cube(self._surface, Point3d(x=-1.0, y=0.0,  z= 0.0), diameter=1, draw=True, Face=layers["FRONT"]),      # LEFT SIDE   | INDEX 5
            Cube(self._surface, Point3d(x=-1.0, y=0.0,  z= 1.0), diameter=1, draw=True, Face=layers["FRONT"]),
            Cube(self._surface, Point3d(x=-1.0, y=1.0,  z=-1.0), diameter=1, draw=True, Face=layers["FRONT"]),
            Cube(self._surface, Point3d(x=-1.0, y=1.0,  z= 0.0), diameter=1, draw=True, Face=layers["FRONT"]),
            Cube(self._surface, Point3d(x=-1.0, y=1.0,  z= 1.0), diameter=1, draw=True, Face=layers["FRONT"]),

            Cube(self._surface, Point3d(x=0.0,  y=-1.0, z=-1.0), diameter=1, draw=True, Face=layers["FRONT"]),
            Cube(self._surface, Point3d(x=0.0,  y=-1.0, z= 0.0), diameter=1, draw=True, Face=layers["FRONT"]),      # UP SIDE     | INDEX 11
            Cube(self._surface, Point3d(x=0.0,  y=-1.0, z= 1.0), diameter=1, draw=True, Face=layers["FRONT"]),
            Cube(self._surface, Point3d(x=0.0,  y=0.0,  z=-1.0), diameter=1, draw=True, Face=layers["FRONT"]),      # FRONT SIDE  | INDEX 13
            Cube(self._surface, Point3d(x=0.0,  y=0.0,  z= 0.0), diameter=1, draw=True, Face=layers["FRONT"]),
            Cube(self._surface, Point3d(x=0.0,  y=0.0,  z= 1.0), diameter=1, draw=True, Face=layers["FRONT"]),      # BACK SIDE   | INDEX 15
            Cube(self._surface, Point3d(x=0.0,  y=1.0,  z=-1.0), diameter=1, draw=True, Face=layers["FRONT"]),
            Cube(self._surface, Point3d(x=0.0,  y=1.0,  z= 0.0), diameter=1, draw=True, Face=layers["FRONT"]),      # DOWN SIDE   | INDEX 17
            Cube(self._surface, Point3d(x=0.0,  y=1.0,  z= 1.0), diameter=1, draw=True, Face=layers["FRONT"]),

            Cube(self._surface, Point3d(x=1.0,  y=-1.0, z=-1.0), diameter=1, draw=True, Face=layers["FRONT"]),
            Cube(self._surface, Point3d(x=1.0,  y=-1.0, z= 0.0), diameter=1, draw=True, Face=layers["FRONT"]),
            Cube(self._surface, Point3d(x=1.0,  y=-1.0, z= 1.0), diameter=1, draw=True, Face=layers["FRONT"]),
            Cube(self._surface, Point3d(x=1.0,  y=0.0,  z=-1.0), diameter=1, draw=True, Face=layers["FRONT"]),
            Cube(self._surface, Point3d(x=1.0,  y=0.0,  z= 0.0), diameter=1, draw=True, Face=layers["FRONT"]),      # RIGHT SIDE  | INDEX 23
            Cube(self._surface, Point3d(x=1.0,  y=0.0,  z= 1.0), diameter=1, draw=True, Face=layers["FRONT"]),
            Cube(self._surface, Point3d(x=1.0,  y=1.0,  z=-1.0), diameter=1, draw=True, Face=layers["FRONT"]),
            Cube(self._surface, Point3d(x=1.0,  y=1.0,  z= 0.0), diameter=1, draw=True, Face=layers["FRONT"]),
            Cube(self._surface, Point3d(x=1.0,  y=1.0,  z= 1.0), diameter=1, draw=True, Face=layers["FRONT"]),
        ]
        self.state = self.InitState()
        self.actions = []
        self.counter = []
        self.RotationOrder = [Axes["X axis"], Axes["Y axis"], Axes["Z axis"]]
        # self.NCubes = self.to_numpy()


    def draw(self):
        Planes = [plane for cube in self.cubes if cube.draw for plane in cube.GetPlanes(self.RotationOrder)]
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
                FrontCubes = self.GetSideCubes("FRONT")
                for CubeIndex in FrontCubes:
                    self.cubes[CubeIndex].update(-key * self.RotationAngle, "Z axis")

            if key == pygame.K_r or key == pygame.K_e:
                key = 0.5 - (key - pygame.K_e) / (pygame.K_r - pygame.K_e)
                RightCubes = self.GetSideCubes("RIGHT")
                for CubeIndex in RightCubes:
                    self.cubes[CubeIndex].update(-key * self.RotationAngle, "X axis")

            if key == pygame.K_b or key == pygame.K_v:
                key = 0.5 - (key - pygame.K_b) / (pygame.K_v - pygame.K_b)
                BackCubes = self.GetSideCubes("BACK")
                for CubeIndex in BackCubes:
                    self.cubes[CubeIndex].update(-key * self.RotationAngle, "Z axis")

            if key == pygame.K_l or key == pygame.K_k:
                key = 0.5 - (key - pygame.K_k) / (pygame.K_l - pygame.K_k)
                LeftCubes = self.GetSideCubes("LEFT")
                for CubeIndex in LeftCubes:
                    self.cubes[CubeIndex].update(-key * self.RotationAngle, "X axis")

            if key == pygame.K_u or key == pygame.K_y:
                key = 0.5 - (key - pygame.K_y) / (pygame.K_u - pygame.K_y)
                UpCubes = self.GetSideCubes("UP")
                for CubeIndex in UpCubes:
                    self.cubes[CubeIndex].update(-key * self.RotationAngle, "Y axis")

            if key == pygame.K_d or key == pygame.K_s:
                key = 0.5 - (key - pygame.K_d) / (pygame.K_s - pygame.K_d)
                DownCubes = self.GetSideCubes("DOWN")
                for CubeIndex in DownCubes:
                    self.cubes[CubeIndex].update(-key * self.RotationAngle, "Y axis")

            self.counter[0] -= 1
            if self.counter[0] < 1:
                self.actions = self.actions[1:]
                self.counter = self.counter[1:]
        for cube in self.cubes:
            for i in range(3):
                cube.GlobalRotation[i] += 0.005
        pass

    def GetSideCubes(self, side):
        if side == "FRONT":
            return [CubeIndex for (CubeIndex, cube) in enumerate(self.cubes) if round(cube.center.z) == -1]
        if side == "RIGHT":
            return [CubeIndex for (CubeIndex, cube) in enumerate(self.cubes) if round(cube.center.x) == 1]
        if side == "BACK":
            return [CubeIndex for (CubeIndex, cube) in enumerate(self.cubes) if round(cube.center.z) == 1]
        if side == "LEFT":
            return [CubeIndex for (CubeIndex, cube) in enumerate(self.cubes) if round(cube.center.x) == -1]
        if side == "UP":
            return [CubeIndex for (CubeIndex, cube) in enumerate(self.cubes) if round(cube.center.y) == -1]
        if side == "DOWN":
            return [CubeIndex for (CubeIndex, cube) in enumerate(self.cubes) if round(cube.center.y) == 1]


    def to_numpy(self):
        return np.array(self.cubes).reshape((3, 3, 3))