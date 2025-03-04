import numpy as np

from __init__ import TranslationMatrix, WIDTH, HEIGHT

def Translate(vector, TranslationVector):
    TranslationVector = np.array([*TranslationVector, 1])
    TranslationMatrix[:, -1] = TranslationVector
    return np.dot(TranslationMatrix, vector)

def Scale(vector, axis, length):
    vector[axis] = vector[axis] * length * 0.5
    return vector

def Denormalize(vector):
    # factor = 2
    # if vector[-1]:
        # factor /= vector[-1]
    # Translated = Translate(vector, [factor, factor, 0])
    # Scaled = Scale(Translated, 0, WIDTH)
    # Scaled = Scale(Scaled, 1, HEIGHT)
    # return Scaled
    vector[0] += 1
    vector[1] += 1
    vector[0] *= 0.5 * WIDTH
    vector[1] *= 0.5 * HEIGHT
    return vector