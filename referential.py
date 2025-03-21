# referential.py

# -*- coding: utf-8 -*-
# Author: Dhia Neifar <neifar@umich.edu>


import pygame
import numpy as np

from point import Point3d
from enums.colors import Color
from config import Translate, Project, Scale, Rotate, Pad


class Referential:
    def __init__(self, surface,
                 x=Point3d(x=2, y=0, z=0),
                 y=Point3d(x=0, y=2, z=0),
                 z=Point3d(x=0, y=0, z=2),
                 ):
        self.x = x
        self.y = y
        self.z = z
        self.surface = surface

    def to_numpy(self):
        return np.array([point.to_numpy() for point in [Point3d(0, 0, 0), self.x, self.y, self.z]], dtype=np.float16)


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
        RotatedRef = Rotate(Coordinates, np.pi * 0.0, np.pi * 0.0, np.pi * 0.0, [0, 1, 2])
        PaddedRef = Pad(RotatedRef)
        ZTranslatedRef = Translate(PaddedRef, Tx=0.0, Ty=0.0, Tz=10.0)
        ProjectedRef = Project(ZTranslatedRef)
        ScaledRef = Scale(ProjectedRef)
        return ScaledRef

    def draw(self):
        ScaledRef = self.transform()
        pygame.draw.line(self.surface, Color.RED.value,
                         (ScaledRef[0, 0], ScaledRef[0, 1]),  # start at origin
                         (ScaledRef[1, 0], ScaledRef[1, 1]),  # end 100 px to the right
                         5)  # thickness

        # Draw Y-axis (green, going up)
        pygame.draw.line(self.surface, Color.GREEN.value,
                         (ScaledRef[0, 0], ScaledRef[0, 1]),  # start at origin
                         (ScaledRef[2, 0], ScaledRef[2, 1]),
                         5)

        # Draw Z-axis (blue, diagonal down-right)
        # This is just a visual approximation to convey depth.
        pygame.draw.line(self.surface, Color.MAGENTA.value,
                         (ScaledRef[0, 0], ScaledRef[0, 1]),  # start at origin
                         (ScaledRef[3, 0], ScaledRef[3, 1]),
                         5)

    def update(self):
        pass


    def KeyTrigger(self, key):
        pass