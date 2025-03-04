import numpy as np

HEIGHT, WIDTH = 960, 1280
AspectRatio = HEIGHT / WIDTH
FieldOfView = np.pi / 2
FieldOfViewRad = 1 / np.tan(FieldOfView / 2)
Znear, Zfar = 0.1, 1000
Lambda = Zfar / (Zfar - Znear)

ProjectionMatrix = np.array([
    [AspectRatio * FieldOfView,             0,              0,                    0],
    [0,                                     FieldOfView,    0,                    0],
    [0,                                     0,         Lambda,      -Lambda * Znear],
    [0,                                     0,              1,                    0]
], dtype=np.float16)




TranslationMatrix = np.array([
    [1,     0,      0,      0],
    [0,     1,      0,      0],
    [0,     0,      1,      0],
    [0,     0,      0,      1]
], dtype=np.float16)