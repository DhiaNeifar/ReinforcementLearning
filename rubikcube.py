# rubikcube.py

# -*- coding: utf-8 -*-
# Author: Dhia Neifar <neifar@umich.edu>


import numpy as np
import pygame
from typing import List

from game import Game
from cube import Cube
from point import Point3d
from config import FPS, sides, Axes
from actions.front import RotateFront
from actions.right import RotateRight
from actions.back import RotateBack
from actions.left import RotateLeft
from actions.up import RotateUp
from actions.down import RotateDown


class RubikCube(Game):
    def __init__(self, surface: pygame.Surface) -> None:
        """
        Constructor for RubikCube.
        A Rubik's Cube is designed as a combination of 27 cubes.
        :param surface: It is the canvas used to draw objects on. surface is passed down from Game Manager. Type: pygame.Surface
        """
        super().__init__(surface)
        self.surface = surface
        self.RotationSpeed = 3 * FPS # Multiply by 0.5 to double the speed!
        self.RotationAngle = np.pi / self.RotationSpeed
        self.cubes = [
            Cube(self.surface, Point3d(x=-1.0, y=-1.0, z=-1.0), diameter=1),
            Cube(self.surface, Point3d(x=-1.0, y=-1.0, z= 0.0), diameter=1),
            Cube(self.surface, Point3d(x=-1.0, y=-1.0, z= 1.0), diameter=1),
            Cube(self.surface, Point3d(x=-1.0, y= 0.0, z=-1.0), diameter=1),
            Cube(self.surface, Point3d(x=-1.0, y=0.0,  z= 0.0), diameter=1),      # LEFT SIDE   | INDEX 5
            Cube(self.surface, Point3d(x=-1.0, y=0.0,  z= 1.0), diameter=1),
            Cube(self.surface, Point3d(x=-1.0, y=1.0,  z=-1.0), diameter=1),
            Cube(self.surface, Point3d(x=-1.0, y=1.0,  z= 0.0), diameter=1),
            Cube(self.surface, Point3d(x=-1.0, y=1.0,  z= 1.0), diameter=1),

            Cube(self.surface, Point3d(x=0.0,  y=-1.0, z=-1.0), diameter=1),
            Cube(self.surface, Point3d(x=0.0,  y=-1.0, z= 0.0), diameter=1),      # UP SIDE     | INDEX 11
            Cube(self.surface, Point3d(x=0.0,  y=-1.0, z= 1.0), diameter=1),
            Cube(self.surface, Point3d(x=0.0,  y=0.0,  z=-1.0), diameter=1),      # FRONT SIDE  | INDEX 13
            Cube(self.surface, Point3d(x=0.0,  y=0.0,  z= 0.0), diameter=1),
            Cube(self.surface, Point3d(x=0.0,  y=0.0,  z= 1.0), diameter=1),      # BACK SIDE   | INDEX 15
            Cube(self.surface, Point3d(x=0.0,  y=1.0,  z=-1.0), diameter=1),
            Cube(self.surface, Point3d(x=0.0,  y=1.0,  z= 0.0), diameter=1),      # DOWN SIDE   | INDEX 17
            Cube(self.surface, Point3d(x=0.0,  y=1.0,  z= 1.0), diameter=1),

            Cube(self.surface, Point3d(x=1.0,  y=-1.0, z=-1.0), diameter=1),
            Cube(self.surface, Point3d(x=1.0,  y=-1.0, z= 0.0), diameter=1),
            Cube(self.surface, Point3d(x=1.0,  y=-1.0, z= 1.0), diameter=1),
            Cube(self.surface, Point3d(x=1.0,  y=0.0,  z=-1.0), diameter=1),
            Cube(self.surface, Point3d(x=1.0,  y=0.0,  z= 0.0), diameter=1),      # RIGHT SIDE  | INDEX 23
            Cube(self.surface, Point3d(x=1.0,  y=0.0,  z= 1.0), diameter=1),
            Cube(self.surface, Point3d(x=1.0,  y=1.0,  z=-1.0), diameter=1),
            Cube(self.surface, Point3d(x=1.0,  y=1.0,  z= 0.0), diameter=1),
            Cube(self.surface, Point3d(x=1.0,  y=1.0,  z= 1.0), diameter=1),
        ]
        self.state = self.InitialState()
        self.actions = []
        self.counter = []
        self.scrambling = False


    def draw(self) -> None:
        """
        Method that draws the Rubik's Cube.
        First, we extract planes from all cubes, sort in descending order the planes based on z axis.
        We draw planes from furthest to nearest to screen.

        :return: None
        """

        Planes = [plane for cube in self.cubes if cube.draw for plane in cube.GetPlanes()]
        Planes.sort(key=lambda plane_: plane_.GetAverageZ(), reverse=True)
        for plane in Planes:
            plane.draw()

    @staticmethod
    def InitialState() -> np.ndarray:
        """
            Creates a 6x3x3 (Face, Row, Column) numpy array for a Rubik's Cube in initial State:
            Face 0 represents Front | Color: Yellow
            Face 1 represents Right | Color: Red
            Face 2 represents Back  | Color: White
            Face 3 represents Left  | Color: Orange
            Face 4 represents Up    | Color: Green
            Face 5 represents Down  | Color: Blue

            ith Face has all stickers = i.
        """

        state = np.zeros((6, 3, 3), dtype=np.int8)
        for face in range(6):
            state[face, :, :] = face
        return state


    def KeyTrigger(self, key: pygame.key) -> None:
        """
        Method needs to exist. This is passed along from Game Manager. Every game requires a KeyTrigger method
        to process the event (Key or mouse) triggered.
        KeyPressed is a bool that checks if the key pressed is a key that would trigger an action. Pressing any other key would be ignored.

        :param key: A key triggering an event.

        :return: None
        """

        # Key p is for scrambling
        if key == pygame.K_p:
            self.scrambling = True
            self.scramble()
            return

        KeyPressed = False
        if key == pygame.K_f or key == pygame.K_g:
            Clockwise = 0.5 - (key - pygame.K_f) / (pygame.K_g - pygame.K_f) < 0
            RotateFront(clockwise=Clockwise).ApplyRotation(self)
            KeyPressed = True

        if key == pygame.K_r or key == pygame.K_e:
            Clockwise = 0.5 - (key - pygame.K_e) / (pygame.K_r - pygame.K_e) < 0
            RotateRight(clockwise=Clockwise).ApplyRotation(self)
            KeyPressed = True

        if key == pygame.K_b or key == pygame.K_v:
            Clockwise = 0.5 - (key - pygame.K_b) / (pygame.K_v - pygame.K_b) < 0
            RotateBack(clockwise=Clockwise).ApplyRotation(self)
            KeyPressed = True

        if key == pygame.K_l or key == pygame.K_k:
            Clockwise = 0.5 - (key - pygame.K_k) / (pygame.K_l - pygame.K_k) < 0
            RotateLeft(clockwise=Clockwise).ApplyRotation(self)
            KeyPressed = True

        if key == pygame.K_u or key == pygame.K_y:
            Clockwise = 0.5 - (key - pygame.K_y) / (pygame.K_u - pygame.K_y) < 0
            RotateUp(clockwise=Clockwise).ApplyRotation(self)
            KeyPressed = True

        if key == pygame.K_d or key == pygame.K_s:
            Clockwise = 0.5 - (key - pygame.K_d) / (pygame.K_s - pygame.K_d) < 0
            RotateDown(clockwise=Clockwise).ApplyRotation(self)
            KeyPressed = True

        if KeyPressed:
            self.actions.append(key)
            self.counter.append(self.RotationSpeed)


    def update(self) -> None:
        """
        Similar to KeyTrigger, this method is enforced by Game Manager.
        It is responsible for updating the Rubik's Cube every frame.
        First part handles the position of the cubes if an action is triggered.
        Second part handles the global rotation of the cubes.

        :return:
        """

        if self.actions:
            key = self.actions[0]

            if key == pygame.K_p:
                self.actions = self.actions[1:]
                self.scramble()

            if key == pygame.K_f or key == pygame.K_g:
                key = 0.5 - (key - pygame.K_f) / (pygame.K_g - pygame.K_f)
                FrontCubes = self.GetSideCubes(sides["FRONT"])
                for CubeIndex in FrontCubes:
                    self.cubes[CubeIndex].LocalUpdate(-key * self.RotationAngle, Axes["Z axis"])

            if key == pygame.K_r or key == pygame.K_e:
                key = 0.5 - (key - pygame.K_e) / (pygame.K_r - pygame.K_e)
                RightCubes = self.GetSideCubes(sides["RIGHT"])
                for CubeIndex in RightCubes:
                    self.cubes[CubeIndex].LocalUpdate(-key * self.RotationAngle, Axes["X axis"])

            if key == pygame.K_b or key == pygame.K_v:
                key = 0.5 - (key - pygame.K_b) / (pygame.K_v - pygame.K_b)
                BackCubes = self.GetSideCubes(sides["BACK"])
                for CubeIndex in BackCubes:
                    self.cubes[CubeIndex].LocalUpdate(key * self.RotationAngle, Axes["Z axis"])

            if key == pygame.K_l or key == pygame.K_k:
                key = 0.5 - (key - pygame.K_k) / (pygame.K_l - pygame.K_k)
                LeftCubes = self.GetSideCubes(sides["LEFT"])
                for CubeIndex in LeftCubes:
                    self.cubes[CubeIndex].LocalUpdate(key * self.RotationAngle, Axes["X axis"])

            if key == pygame.K_u or key == pygame.K_y:
                key = 0.5 - (key - pygame.K_y) / (pygame.K_u - pygame.K_y)
                UpCubes = self.GetSideCubes(sides["UP"])
                for CubeIndex in UpCubes:
                    self.cubes[CubeIndex].LocalUpdate(key * self.RotationAngle, Axes["Y axis"])

            if key == pygame.K_d or key == pygame.K_s:
                key = 0.5 - (key - pygame.K_d) / (pygame.K_s - pygame.K_d)
                DownCubes = self.GetSideCubes(sides["DOWN"])
                for CubeIndex in DownCubes:
                    self.cubes[CubeIndex].LocalUpdate(key * self.RotationAngle, Axes["Y axis"])

            # an action spans on two seconds in total, counter keeps track of how many times we need to update the cubes before the action is burned.
            self.counter[0] -= 1
            if self.counter[0] < 1:
                self.actions = self.actions[1:]
                self.counter = self.counter[1:]

        # Updating the global rotation of cubes
        for cube in self.cubes:
            cube.update()
        pass

    def GetSideCubes(self, side: str) -> List[int]:
        """
        The method returns a list of cubes on the side from the argument.
        :param side: str can only be FRONT | RIGHT | BACK | LEFT | UP | DOWN

        :return: List[int: indices of the cubes of the side of the Rubik's Cube]
        """

        if side == sides["FRONT"]:
            return [CubeIndex for (CubeIndex, cube) in enumerate(self.cubes) if round(cube.center.z) == -1]
        if side == sides["RIGHT"]:
            return [CubeIndex for (CubeIndex, cube) in enumerate(self.cubes) if round(cube.center.x) == 1]
        if side == sides["BACK"]:
            return [CubeIndex for (CubeIndex, cube) in enumerate(self.cubes) if round(cube.center.z) == 1]
        if side == sides["LEFT"]:
            return [CubeIndex for (CubeIndex, cube) in enumerate(self.cubes) if round(cube.center.x) == -1]
        if side == sides["UP"]:
            return [CubeIndex for (CubeIndex, cube) in enumerate(self.cubes) if round(cube.center.y) == -1]
        if side == sides["DOWN"]:
            return [CubeIndex for (CubeIndex, cube) in enumerate(self.cubes) if round(cube.center.y) == 1]

    def scramble(self):
        """"
        Method that scrambles the Rubik's Cube randomly.
        TODO: Parameters it should have:
            :param: speed -> float: Speed of scrambling | Affects self.RotationSpeed
            :param: NumberActions -> int: Number of random actions
            :param: draw -> bool: if True, we draw the actions used to scramble the Rubik's Cube on canvas else ignore.
        """
        while self.actions:
            self.update()
        print("Starting to Scramble")
        # cube.update
        pass
