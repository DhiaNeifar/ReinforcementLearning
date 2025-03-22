# config.py

# -*- coding: utf-8 -*-
# Author: Dhia Neifar <neifar@umich.edu>


import numpy as np

from enums.colors import Color

HEIGHT, WIDTH = 960, 1280
FPS = 60
AspectRatio = HEIGHT / WIDTH

theta = np.pi * 0.5
FieldOfView = theta * 0.5
FieldOfViewRad = 1 / np.tan(FieldOfView)

Z_near, Z_far = 0.1, 1000
Lambda = Z_far / (Z_far - Z_near)


FRONT  = {"Vertices": [0, 1, 2, 3], "Edges": [0, 3, 6, 9],   "Color": Color.YELLOW.value}
RIGHT  = {"Vertices": [1, 5, 6, 2], "Edges": [5, 4, 8, 3],   "Color": Color.RED.value}
BACK   = {"Vertices": [5, 4, 7, 6], "Edges": [1, 10, 7, 4],  "Color": Color.WHITE.value}
LEFT   = {"Vertices": [4, 0, 3, 7], "Edges": [2, 9, 11, 10], "Color": Color.ORANGE.value}
UP     = {"Vertices": [4, 5, 1, 0], "Edges": [1, 5, 0, 2],   "Color": Color.GREEN.value}
DOWN   = {"Vertices": [3, 2, 6, 7], "Edges": [6, 8, 7, 11],  "Color": Color.BLUE.value}

PLANES = [FRONT, RIGHT, BACK, LEFT, UP, DOWN]

sides = {"FRONT": 0, "RIGHT": 1, "BACK": 2, "LEFT": 3, "UP": 4, "DOWN": 5, }

Axes = {"X axis": 0, "Y axis": 1, "Z axis": 2}




def Translate(Matrix: np.ndarray, Tx: float, Ty: float, Tz: float) -> np.ndarray:
    """
    Performs translation to Matrix according to vector Tx, Ty and Tz.
    :param Matrix: The Matrix to translate.
    :param Tx: Translate x-axis by Tx.
    :param Ty: Translate y-axis by Ty.
    :param Tz: Translate z-axis by Tz.

    :return: Matrix translated.
    """

    TranslationMatrix = np.array([
        [1,       0,       0,      0],
        [0,       1,       0,      0],
        [0,       0,       1,      0],
        [Tx,     Ty,      Tz,      1]
    ], dtype=np.float16)

    return Matrix @ TranslationMatrix


def Project(Matrix: np.ndarray) -> np.ndarray:
    """
    Performs perspective projection of Matrix  using ProjectionMatrix.
    :param Matrix: The Matrix to project.
    :return: Matrix projected.
    """

    ProjectionMatrix = np.array([
        [AspectRatio * FieldOfView,             0,                     0,           0],
        [                        0,   FieldOfView,                     0,           0],
        [                        0,             0,                Lambda,           1],
        [                        0,             0,      -Lambda * Z_near,           0]
    ], dtype=np.float16)

    Matrix = Matrix @ ProjectionMatrix
    mask = Matrix[:, 3] != 0
    Matrix[mask, :] /= Matrix[mask, 3, np.newaxis]

    return Matrix


def Scale(Matrix: np.ndarray) -> np.ndarray:
    """
    Performs scaling of Matrix. First, the Matrix is translated by 1 along x and y axes.
    Proceed to multiplying the x-axis and y-axis by Half the Width and the Height of the Screen respectively.
    :param Matrix: The Matrix to scale.
    :return: Scaled Matrix.
    """

    Matrix = Translate(Matrix, Tx=1, Ty=1, Tz=0)

    Matrix[:, 0] *= 0.5 * WIDTH
    Matrix[:, 1] *= 0.5 * HEIGHT

    return Matrix.astype(np.float64)

def LocalRotate(Matrix: np.ndarray, angle: float, axis) -> np.ndarray:
    """
    Function for Local Rotation.
    Applied to the cube when an event is triggered like F or R'.

    :param Matrix: Coordinates of the vertices of the cube.
    :param angle: Angle used for rotation.
    :param axis: Following axis (X X Axis, Y Axis, Z Axis)

    :return: New coordinates of the vertices of the cube after applying local rotation.
    """

    if axis == Axes["X axis"]:
        XRotationMatrix = np.array([
            [1, 0, 0],
            [0, np.cos(angle), -np.sin(angle)],
            [0, np.sin(angle), np.cos(angle)],
        ])
        return Matrix @ XRotationMatrix
    if axis == Axes["Y axis"]:
        YRotationMatrix = np.array([
            [np.cos(angle), 0, np.sin(angle)],
            [0, 1, 0],
            [-np.sin(angle), 0, np.cos(angle)],
        ])
        return Matrix @ YRotationMatrix
    if axis == Axes["Z axis"]:
        ZRotationMatrix = np.array([
            [np.cos(angle), -np.sin(angle), 0],
            [np.sin(angle), np.cos(angle), 0],
            [0, 0, 1],
        ])
        return Matrix @ ZRotationMatrix

def GlobalRotation(Matrix: np.ndarray, alpha: float, beta: float, gamma:float) -> np.ndarray:
    """
    Function for Global Rotation.
    Applied to all the points assigned to an object. The function used for rotating an object for 3d rendering.

    :param Matrix: Coordinates of the points assigned to an object.
    :param alpha: Angle to rotate along X Axis
    :param beta: Angle to rotate along Y Axis
    :param gamma: Angle to rotate along Z Axis

    :return: New coordinates of the points of the object after applying global rotation.
    """

    XRotationMatrix = np.array([
        [1,                 0,                   0],
        [0,     np.cos(alpha),      -np.sin(alpha)],
        [0,     np.sin(alpha),       np.cos(alpha)],
    ])

    YRotationMatrix = np.array([
        [ np.cos(beta),      0,      np.sin(beta)],
        [            0,      1,                 0],
        [-np.sin(beta),      0,      np.cos(beta)],
    ])

    ZRotationMatrix = np.array([
        [np.cos(gamma),      -np.sin(gamma),    0],
        [np.sin(gamma),       np.cos(gamma),    0],
        [0,                               0,    1],
    ])
    return Matrix @ XRotationMatrix @ YRotationMatrix @ ZRotationMatrix

def Pad(Matrix: np.ndarray) -> np.ndarray:
    """
    Function for Padding. Add a column of ones at the end.

    :param Matrix:  Matrix to pad.
    :return: Padded Matrix.
    """
    shape = Matrix.shape
    return np.concatenate((Matrix, np.ones((shape[0], 1))), axis=1)
