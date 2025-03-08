import numpy as np

from colors import Color

HEIGHT, WIDTH = 960, 1280

AspectRatio = HEIGHT / WIDTH

theta = np.pi * 0.5
FieldOfView = theta * 0.5
FieldOfViewRad = 1 / np.tan(FieldOfView)

Z_near, Z_far = 0.1, 1000
Lambda = Z_far / (Z_far - Z_near)

ProjectionMatrix = np.array([
    [AspectRatio * FieldOfView,             0,                     0,           0],
    [                        0,   FieldOfView,                     0,           0],
    [                        0,             0,                Lambda,           1],
    [                        0,             0,      -Lambda * Z_near,           0]
], dtype=np.float16)

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
        [1,     0,      0,      0],
        [0,     1,      0,      0],
        [0,     0,      1,      0],
        [0,     0,      0,      1]
    ], dtype=np.float16)

    TranslationMatrix[3, 0] = Tx
    TranslationMatrix[3, 1] = Ty
    TranslationMatrix[3, 2] = Tz

    return Matrix @ TranslationMatrix


def Project(Matrix: np.ndarray) -> np.ndarray:
    """
    Performs perspective projection of Matrix  using ProjectionMatrix.
    :param Matrix: The Matrix to project.
    :return: Matrix projected.
    """

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


def Rotate(Matrix: np.ndarray, alpha, beta, gamma):

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
    shape = Matrix.shape
    return np.concatenate((Matrix, np.ones((shape[0], 1))), axis=1)



FRONT = {
    "Vertices": [0, 1, 2, 3],
    "Edges": (0, 3, 6, 9),
    "Color": Color.YELLOW.value
}

RIGHT = {
    "Vertices": [1, 5, 6, 2],
    "Edges": [5, 4, 8, 3],
    "Color": Color.RED.value
}

BACK = {
    "Vertices": [5, 4, 7, 6],
    "Edges": [1, 10, 7, 4],
    "Color": Color.WHITE.value
}

LEFT = {
    "Vertices": [4, 0, 3, 7],
    "Edges": [2, 9, 11, 10],
    "Color": Color.ORANGE.value
}

UP = {
    "Vertices": [4, 5, 1, 0],
    "Edges": [1, 5, 0, 2],
    "Color": Color.GREEN.value
}

DOWN = {
    "Vertices": [3, 2, 6, 7],
    "Edges": [6, 8, 7, 11],
    "Color": Color.BLUE.value
}
layers = {
    "FRONT": 0,
    "RIGHT": 1,
    "BACK": 2,
    "LEFT": 3,
    "UP": 4,
    "DOWN": 5,
}
LAYERS = [FRONT, RIGHT, BACK, LEFT, UP, DOWN]

RotationAngle = np.pi / 2

Axes = {
    "X axis": 0,
    "Y axis": 1,
    "Z axis": 2,
}