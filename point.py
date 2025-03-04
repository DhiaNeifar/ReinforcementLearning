import numpy as np
import pygame

from __init__ import ProjectionMatrix, TranslationMatrix
from colors import Color
from utils import Translate, Denormalize


class Point3d:
    def __init__(self, x, y, z, PointsColor=Color.WHITE.value):
        self.x = x
        self.y = y
        self.z = z
        self.PointsColor = PointsColor

    def to_numpy(self) -> np.ndarray:
        return np.array([self.x, self.y, self.z, 1], dtype=np.float16)

    def transform(self) -> np.ndarray:
        vector = self.to_numpy()
        ZTranslatedVector = Translate(vector, [0, 0, 2])
        ProjectedVector = np.dot(ProjectionMatrix, ZTranslatedVector)
        print(ProjectedVector)
        if ProjectedVector[-1]:
            ProjectedVector[0] /= ProjectedVector[-1]
            ProjectedVector[1] /= ProjectedVector[-1]
        DenormalizedVector = Denormalize(ProjectedVector)
        return DenormalizedVector.astype(np.int16)

    def draw(self, surface, width=5) -> None:
        point = self.transform()
        pygame.draw.circle(surface, self.PointsColor, (point[0], point[1]), width)