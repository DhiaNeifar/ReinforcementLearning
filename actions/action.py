# -*- coding: utf-8 -*-
# Author: Dhia Neifar <neifar@umich.edu>

import numpy as np

# from rubikcube import RubikCube


class Action(object):
    def __init__(self):
        pass

    @staticmethod
    def RotateFace(cube, face, clockwise=True):
        """
        Rotate the 3x3 sub-array for `face` by 90°.
          - If clockwise=True, that is np.rot90(..., k=3)
            (since np.rot90(..., k=1) is a 90° CCW).
          - If clockwise=False, do a 90° CCW rotation.
        """
        if clockwise:
            cube.state[face] = np.rot90(cube.state[face], k=-1)  # 90° clockwise
        else:
            cube.state[face] = np.rot90(cube.state[face], k=1)  # 90° counterclockwise


    @staticmethod
    def ApplyRotation(Rcube):
        pass