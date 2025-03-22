import pygame
import numpy as np


from config import Translate, Project, Scale, GlobalRotation, Pad


class Game(object):
    def __init__(self, surface: pygame.Surface) -> None:
        self.surface = surface
        self.GlobalRotation = [0.0, 0.0, 0.0]

    def to_numpy(self) -> np.ndarray:
        pass

    def transform(self, tz=10.0) -> (np.ndarray, np.ndarray):
        """
        Applies the transformation of the vertices of the cube.
        Coordinates of the cube are extracted in np.ndarray.
        Global Rotation of the cube is applied.
        Padding is added to the Coordinates of the cube to facilitates Translation.
        Translation of z-axis by value :param:tz to be in the field of view Frustum.
        Projects the Matrix using Perspective Projection Matrix.
        Scales the Matrix to pygame screen.
        :param tz: Translation of the cube.

        :return: Coordinates of Points of cube scaled & ZTranslatedCube.
        We keep track of ZTranslatedCube because we have not divided by the Z axis.
        """

        Coordinates = self.to_numpy()
        Rotated = GlobalRotation(Coordinates, *self.GlobalRotation)
        Padded = Pad(Rotated)
        ZTranslated = Translate(Padded, Tx=0.0, Ty=0.0, Tz=tz)
        Projected = Project(ZTranslated)
        Scaled = Scale(Projected)
        return Scaled, ZTranslated

    def draw(self):
        pass

    def update(self):
        pass

    def KeyTrigger(self, key: pygame.key):
        pass
