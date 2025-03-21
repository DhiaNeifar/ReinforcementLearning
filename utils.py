# import random
# import numpy as np
#
# ###############################################################################
# # FACE INDICES (you can adapt if you prefer a different labeling):
# #   0 = FRONT  (initially all 0: "Yellow"?)
# #   1 = RIGHT  (initially all 1: "Red"?)
# #   2 = BACK   (initially all 2: "White"?)
# #   3 = LEFT   (initially all 3: "Orange"?)
# #   4 = TOP    (initially all 4: "Green"?)
# #   5 = BOTTOM (initially all 5: "Blue"?)
# ###############################################################################
#
# def init_cube():
#     """
#     Create a 6x3x3 numpy array for a "solved" cube:
#       Face i has all stickers = i.
#     """
#     cube = np.zeros((6, 3, 3), dtype=int)
#     for face in range(6):
#         cube[face, :, :] = face
#     return cube
#
# def rotate_face_90(cube, face, clockwise=True):
#     """
#     Rotate the 3x3 sub-array for `face` by 90°.
#       - If clockwise=True, that is np.rot90(..., k=3)
#         (since np.rot90(..., k=1) is a 90° CCW).
#       - If clockwise=False, do a 90° CCW rotation.
#     """
#     print(cube.shape)
#     if clockwise:
#         print(cube[face].shape)
#         cube[face] = np.rot90(cube[face], k=3)  # 90° clockwise
#
#     else:
#         cube[face] = np.rot90(cube[face], k=1)  # 90° counterclockwise
#
#     print(cube.shape)
#
# ###############################################################################
# # FRONT (F) face turn
# ###############################################################################
# def rotate_F(cube, clockwise=True):
#     """
#     Turn the FRONT face 90° in either clockwise or counterclockwise direction.
#     """
#     FRONT, RIGHT, BACK, LEFT, TOP, BOTTOM = 0, 1, 2, 3, 4, 5
#
#     # 1) Rotate the FRONT face itself
#     old_cube = np.copy(cube)
#     rotate_face_90(cube, FRONT, clockwise)
#     if np.array_equal(old_cube, cube):
#         print("change here")
#     # 2) Cycle the adjacent edge strips:
#     if clockwise:
#         # Save the bottom row of TOP
#         temp = cube[TOP, 2, :].copy()
#         # TOP's bottom row <- LEFT's right column (reversed top-to-bottom)
#         cube[TOP, 2, :] = cube[LEFT, :, 2][::-1]
#         # LEFT's right column <- BOTTOM's top row
#         cube[LEFT, :, 2] = cube[BOTTOM, 0, :]
#         # BOTTOM's top row <- RIGHT's left column (reversed top-to-bottom)
#         cube[BOTTOM, 0, :] = cube[RIGHT, :, 0][::-1]
#         # RIGHT's left column <- (old) TOP's bottom row
#         cube[RIGHT, :, 0] = temp
#     else:
#         # Counterclockwise (the inverse cycle)
#         temp = cube[TOP, 2, :].copy()
#         # TOP's bottom row <- RIGHT's left column
#         cube[TOP, 2, :] = cube[RIGHT, :, 0]
#         # RIGHT's left column <- BOTTOM's top row (reversed)
#         cube[RIGHT, :, 0] = cube[BOTTOM, 0, :][::-1]
#         # BOTTOM's top row <- LEFT's right column
#         cube[BOTTOM, 0, :] = cube[LEFT, :, 2]
#         # LEFT's right column <- (old) TOP's bottom row (reversed)
#         cube[LEFT, :, 2] = temp[::-1]
#
# ###############################################################################
# # BACK (B) face turn
# ###############################################################################
# def rotate_B(cube, clockwise=True):
#     """
#     Turn the BACK face 90° in either clockwise or counterclockwise direction.
#     """
#     FRONT, RIGHT, BACK, LEFT, TOP, BOTTOM = 0, 1, 2, 3, 4, 5
#
#     # Rotate the BACK face
#     old_cube = np.copy(cube)
#     rotate_face_90(cube, FRONT, clockwise)
#     if np.array_equal(old_cube, cube):
#         print("change here")
#     # Cycle adjacent strips
#     if clockwise:
#         temp = cube[TOP, 0, :].copy()
#         # TOP's top row <- RIGHT's right column
#         cube[TOP, 0, :] = cube[RIGHT, :, 2]
#         # RIGHT's right column <- BOTTOM's bottom row (reversed)
#         cube[RIGHT, :, 2] = cube[BOTTOM, 2, :][::-1]
#         # BOTTOM's bottom row <- LEFT's left column
#         cube[BOTTOM, 2, :] = cube[LEFT, :, 0][::-1]
#         # LEFT's left column <- old TOP's top row
#         cube[LEFT, :, 0] = temp
#     else:
#         temp = cube[TOP, 0, :].copy()
#         # TOP's top row <- LEFT's left column
#         cube[TOP, 0, :] = cube[LEFT, :, 0]
#         # LEFT's left column <- BOTTOM's bottom row (reversed)
#         cube[LEFT, :, 0] = cube[BOTTOM, 2, :][::-1]
#         # BOTTOM's bottom row <- RIGHT's right column (reversed)
#         cube[BOTTOM, 2, :] = cube[RIGHT, :, 2][::-1]
#         # RIGHT's right column <- old TOP's top row
#         cube[RIGHT, :, 2] = temp
#
# ###############################################################################
# # RIGHT (R) face turn
# ###############################################################################
# def rotate_R(cube, clockwise=True):
#     """
#     Turn the RIGHT face 90° in either clockwise or counterclockwise direction.
#     """
#     FRONT, RIGHT, BACK, LEFT, TOP, BOTTOM = 0, 1, 2, 3, 4, 5
#
#     old_cube = np.copy(cube)
#     rotate_face_90(cube, FRONT, clockwise)
#     if np.array_equal(old_cube, cube):
#         print("change here")
#     if clockwise:
#         temp = cube[TOP, :, 2].copy()  # right column of TOP
#         # TOP's right column <- FRONT's right column
#         cube[TOP, :, 2] = cube[FRONT, :, 2]
#         # FRONT's right column <- BOTTOM's right column
#         cube[FRONT, :, 2] = cube[BOTTOM, :, 2]
#         # BOTTOM's right column <- BACK's left column (reversed vertically)
#         cube[BOTTOM, :, 2] = cube[BACK, ::-1, 0]
#         # BACK's left column <- old TOP's right column (reversed vertically)
#         cube[BACK, ::-1, 0] = temp
#     else:
#         temp = cube[TOP, :, 2].copy()
#         # TOP's right column <- BACK's left column (reversed vertically)
#         cube[TOP, :, 2] = cube[BACK, ::-1, 0]
#         # BACK's left column <- BOTTOM's right column (reversed vertically)
#         cube[BACK, ::-1, 0] = cube[BOTTOM, :, 2]
#         # BOTTOM's right column <- FRONT's right column
#         cube[BOTTOM, :, 2] = cube[FRONT, :, 2]
#         # FRONT's right column <- old TOP's right column
#         cube[FRONT, :, 2] = temp
#
# ###############################################################################
# # LEFT (L) face turn
# ###############################################################################
# def rotate_L(cube, clockwise=True):
#     """
#     Turn the LEFT face 90° in either clockwise or counterclockwise direction.
#     """
#     FRONT, RIGHT, BACK, LEFT, TOP, BOTTOM = 0, 1, 2, 3, 4, 5
#
#     old_cube = np.copy(cube)
#     rotate_face_90(cube, FRONT, clockwise)
#     if np.array_equal(old_cube, cube):
#         print("change here")
#     if clockwise:
#         temp = cube[TOP, :, 0].copy()  # left column of TOP
#         # TOP's left column <- BACK's right column (reversed vertically)
#         cube[TOP, :, 0] = cube[BACK, ::-1, 2]
#         # BACK's right column <- BOTTOM's left column (reversed vertically)
#         cube[BACK, ::-1, 2] = cube[BOTTOM, :, 0]
#         # BOTTOM's left column <- FRONT's left column
#         cube[BOTTOM, :, 0] = cube[FRONT, :, 0]
#         # FRONT's left column <- old TOP's left column
#         cube[FRONT, :, 0] = temp
#     else:
#         temp = cube[TOP, :, 0].copy()
#         # TOP's left column <- FRONT's left column
#         cube[TOP, :, 0] = cube[FRONT, :, 0]
#         # FRONT's left column <- BOTTOM's left column
#         cube[FRONT, :, 0] = cube[BOTTOM, :, 0]
#         # BOTTOM's left column <- BACK's right column (reversed vertically)
#         cube[BOTTOM, :, 0] = cube[BACK, ::-1, 2]
#         # BACK's right column <- old TOP's left column (reversed vertically)
#         cube[BACK, ::-1, 2] = temp
#
# ###############################################################################
# # UP (U) face turn
# ###############################################################################
# def rotate_U(cube, clockwise=True):
#     """
#     Turn the TOP face 90° in either clockwise or counterclockwise direction.
#     """
#     FRONT, RIGHT, BACK, LEFT, TOP, BOTTOM = 0, 1, 2, 3, 4, 5
#
#     old_cube = np.copy(cube)
#     rotate_face_90(cube, FRONT, clockwise)
#     if np.array_equal(old_cube, cube):
#         print("change here")
#     if clockwise:
#         temp = cube[FRONT, 0, :].copy()
#         # FRONT's top row <- RIGHT's top row
#         cube[FRONT, 0, :] = cube[RIGHT, 0, :]
#         # RIGHT's top row <- BACK's top row
#         cube[RIGHT, 0, :] = cube[BACK, 0, :]
#         # BACK's top row <- LEFT's top row
#         cube[BACK, 0, :] = cube[LEFT, 0, :]
#         # LEFT's top row <- old FRONT's top row
#         cube[LEFT, 0, :] = temp
#     else:
#         temp = cube[FRONT, 0, :].copy()
#         # FRONT's top row <- LEFT's top row
#         cube[FRONT, 0, :] = cube[LEFT, 0, :]
#         # LEFT's top row <- BACK's top row
#         cube[LEFT, 0, :] = cube[BACK, 0, :]
#         # BACK's top row <- RIGHT's top row
#         cube[BACK, 0, :] = cube[RIGHT, 0, :]
#         # RIGHT's top row <- old FRONT's top row
#         cube[RIGHT, 0, :] = temp
#
# ###############################################################################
# # DOWN (D) face turn
# ###############################################################################
# def rotate_D(cube, clockwise=True):
#     """
#     Turn the BOTTOM face 90° in either clockwise or counterclockwise direction.
#     """
#     FRONT, RIGHT, BACK, LEFT, TOP, BOTTOM = 0, 1, 2, 3, 4, 5
#     old_cube = np.copy(cube)
#     rotate_face_90(cube, FRONT, clockwise)
#     if np.array_equal(old_cube, cube):
#         print("change here")
#     if clockwise:
#         temp = cube[FRONT, 2, :].copy()
#         # FRONT's bottom row <- LEFT's bottom row
#         cube[FRONT, 2, :] = cube[LEFT, 2, :]
#         # LEFT's bottom row <- BACK's bottom row
#         cube[LEFT, 2, :] = cube[BACK, 2, :]
#         # BACK's bottom row <- RIGHT's bottom row
#         cube[BACK, 2, :] = cube[RIGHT, 2, :]
#         # RIGHT's bottom row <- old FRONT's bottom row
#         cube[RIGHT, 2, :] = temp
#     else:
#         temp = cube[FRONT, 2, :].copy()
#         # FRONT's bottom row <- RIGHT's bottom row
#         cube[FRONT, 2, :] = cube[RIGHT, 2, :]
#         # RIGHT's bottom row <- BACK's bottom row
#         cube[RIGHT, 2, :] = cube[BACK, 2, :]
#         # BACK's bottom row <- LEFT's bottom row
#         cube[BACK, 2, :] = cube[LEFT, 2, :]
#         # LEFT's bottom row <- old FRONT's bottom row
#         cube[LEFT, 2, :] = temp
#
#
# ###############################################################################
# # DEMO USAGE
# ###############################################################################
# if __name__ == "__main__":
#     Action = {
#         0: rotate_F,
#         1: rotate_R,
#         2: rotate_B,
#         3: rotate_L,
#         4: rotate_U,
#         5: rotate_D,
#     }
#     CLOCK = {
#         0: True,
#         1: False,
#     }
#     # Create a solved cube
#     cube = init_cube()
#
#     NumActions = 30
#     for _ in range(NumActions):
#         action = Action[random.randint(0, 5)]
#         action(cube, clockwise=CLOCK[random.randint(0, 1)])



import numpy as np
from scipy.spatial.transform import Rotation as R

# ------------------------------------
# 1) Define original angles and order
#    Let's say original order is Z->Y->X,
#    with angles [gamma, beta, alpha].
# ------------------------------------
alpha = 0.3
beta  = 1.0
gamma = 0.5

# Create the original rotation with sequence 'ZYX'
# This means apply Rz(gamma), then Ry(beta), then Rx(alpha).
# (Make sure the angle list corresponds to [Z_angle, Y_angle, X_angle])
R_old = R.from_euler('ZYX', [gamma, beta, alpha], degrees=False)

print("Original rotation matrix:\n", R_old.as_matrix())

# ------------------------------------
# 2) Convert to a new Euler sequence,
#    e.g. 'YXZ' => R_y(...) * R_x(...) * R_z(...).
# ------------------------------------
# This gives us the angles [yAngle, xAngle, zAngle] that reproduce
# the same overall 3D rotation when applied in Y->X->Z order.
# new_angles = R_old.as_euler('YXZ', degrees=False)
#
# print("\nNew angles in 'Y->X->Z' sequence:")
# print(f"beta' = {new_angles[0]:.6f}")
# print(f"alpha' = {new_angles[1]:.6f}")
# print(f"gamma' = {new_angles[2]:.6f}")
#
# # ------------------------------------
# # 3) Verify they match the same rotation
# # ------------------------------------
# R_new = R.from_euler('YXZ', new_angles, degrees=False)
#
# print("\nNew rotation matrix (should match original):\n", R_new.as_matrix())
#
# # Compare numerically
# difference = R_old.as_matrix() - R_new.as_matrix()
# print("\nDifference (R_old - R_new):\n", difference)
# print("Should be very close to a zero matrix.")

import pygame, sys, numpy as np, math
from pygame.locals import *

colors = {
    'U': (255, 255, 255),
    'D': (255, 255, 0),
    'F': (0, 255, 0),
    'B': (0, 0, 255),
    'L': (255, 165, 0),
    'R': (255, 0, 0)
}

def rotation_matrix_axis(angle, axis):
    axis = axis / np.linalg.norm(axis)
    cos_theta = math.cos(angle)
    sin_theta = math.sin(angle)
    one_minus_cos = 1 - cos_theta
    x, y, z = axis
    return np.array([
        [cos_theta + x*x*one_minus_cos,      x*y*one_minus_cos - z*sin_theta,  x*z*one_minus_cos + y*sin_theta],
        [y*x*one_minus_cos + z*sin_theta,      cos_theta + y*y*one_minus_cos,  y*z*one_minus_cos - x*sin_theta],
        [z*x*one_minus_cos - y*sin_theta,      z*y*one_minus_cos + x*sin_theta,  cos_theta + z*z*one_minus_cos]
    ])

def rotation_matrix_full(angle_x, angle_y, angle_z):
    rx = np.array([[1, 0, 0],
                   [0, math.cos(angle_x), -math.sin(angle_x)],
                   [0, math.sin(angle_x), math.cos(angle_x)]])
    ry = np.array([[math.cos(angle_y), 0, math.sin(angle_y)],
                   [0, 1, 0],
                   [-math.sin(angle_y), 0, math.cos(angle_y)]])
    rz = np.array([[math.cos(angle_z), -math.sin(angle_z), 0],
                   [math.sin(angle_z), math.cos(angle_z), 0],
                   [0, 0, 1]])
    return np.dot(rz, np.dot(ry, rx))

class RubiksCube3D:
    def __init__(self):
        self.state = {}
        for face in ['U','D','F','B','L','R']:
            self.state[face] = [[face for _ in range(3)] for _ in range(3)]
        self.face_info = {
            'U': (np.array([0,1.5,0]), np.array([0,1,0]), np.array([1,0,0]), np.array([0,0,-1])),
            'D': (np.array([0,-1.5,0]), np.array([0,-1,0]), np.array([1,0,0]), np.array([0,0,1])),
            'F': (np.array([0,0,1.5]), np.array([0,0,1]), np.array([1,0,0]), np.array([0,-1,0])),
            'B': (np.array([0,0,-1.5]), np.array([0,0,-1]), np.array([-1,0,0]), np.array([0,-1,0])),
            'R': (np.array([1.5,0,0]), np.array([1,0,0]), np.array([0,0,-1]), np.array([0,-1,0])),
            'L': (np.array([-1.5,0,0]), np.array([-1,0,0]), np.array([0,0,1]), np.array([0,-1,0]))
        }
        self.animations = {}  # keys are face letters; value is dict with 'move', 'progress', 'target', 'speed'
    def get_sticker_polygons(self, face):
        center, normal, right, up = self.face_info[face]
        half = 1.5
        face_corner = center - right*half - up*half
        stickers = []
        extra_angle_deg = 0
        if face in self.animations:
            extra_angle_deg = self.animations[face]['progress']
        extra_angle = math.radians(extra_angle_deg)
        if abs(extra_angle) > 1e-5:
            R_extra = rotation_matrix_axis(extra_angle, normal)
        else:
            R_extra = np.eye(3)
        for i in range(3):
            for j in range(3):
                tl = face_corner + right*j + up*i
                tr = tl + right
                bl = tl + up
                br = tl + right + up
                pts = [tl, tr, br, bl]
                # apply extra rotation about the face center if animating
                if face in self.animations:
                    pts = [np.dot(R_extra, (p - center)) + center for p in pts]
                stickers.append((pts, colors[self.state[face][i][j]]))
        return stickers
    def get_all_polygons(self):
        polys = []
        for face in ['U','D','F','B','L','R']:
            polys.extend(self.get_sticker_polygons(face))
        return polys
    def rotate_face(self, face, clockwise=True):
        old = self.state[face]
        new = [[None]*3 for _ in range(3)]
        if clockwise:
            for i in range(3):
                for j in range(3):
                    new[j][2-i] = old[i][j]
        else:
            for i in range(3):
                for j in range(3):
                    new[2-j][i] = old[i][j]
        self.state[face] = new
    def move_R(self, clockwise=True):
        self.rotate_face('R', clockwise)
        if clockwise:
            temp = [self.state['U'][i][2] for i in range(3)]
            for i in range(3):
                self.state['U'][i][2] = self.state['F'][i][2]
                self.state['F'][i][2] = self.state['D'][i][2]
                self.state['D'][i][2] = self.state['B'][2-i][0]
                self.state['B'][2-i][0] = temp[i]
        else:
            temp = [self.state['U'][i][2] for i in range(3)]
            for i in range(3):
                self.state['U'][i][2] = self.state['B'][2-i][0]
                self.state['B'][2-i][0] = self.state['D'][i][2]
                self.state['D'][i][2] = self.state['F'][i][2]
                self.state['F'][i][2] = temp[i]
    def move_L(self, clockwise=True):
        self.rotate_face('L', clockwise)
        if clockwise:
            temp = [self.state['U'][i][0] for i in range(3)]
            for i in range(3):
                self.state['U'][i][0] = self.state['B'][2-i][2]
                self.state['B'][2-i][2] = self.state['D'][i][0]
                self.state['D'][i][0] = self.state['F'][i][0]
                self.state['F'][i][0] = temp[i]
        else:
            temp = [self.state['U'][i][0] for i in range(3)]
            for i in range(3):
                self.state['U'][i][0] = self.state['F'][i][0]
                self.state['F'][i][0] = self.state['D'][i][0]
                self.state['D'][i][0] = self.state['B'][2-i][2]
                self.state['B'][2-i][2] = temp[i]
    def move_U(self, clockwise=True):
        self.rotate_face('U', clockwise)
        if clockwise:
            temp = self.state['B'][0][:]
            self.state['B'][0][:] = self.state['R'][0][:]
            self.state['R'][0][:] = self.state['F'][0][:]
            self.state['F'][0][:] = self.state['L'][0][:]
            self.state['L'][0][:] = temp
        else:
            temp = self.state['B'][0][:]
            self.state['B'][0][:] = self.state['L'][0][:]
            self.state['L'][0][:] = self.state['F'][0][:]
            self.state['F'][0][:] = self.state['R'][0][:]
            self.state['R'][0][:] = temp
    def move_D(self, clockwise=True):
        self.rotate_face('D', clockwise)
        if clockwise:
            temp = self.state['B'][2][:]
            self.state['B'][2][:] = self.state['L'][2][:]
            self.state['L'][2][:] = self.state['F'][2][:]
            self.state['F'][2][:] = self.state['R'][2][:]
            self.state['R'][2][:] = temp
        else:
            temp = self.state['B'][2][:]
            self.state['B'][2][:] = self.state['R'][2][:]
            self.state['R'][2][:] = self.state['F'][2][:]
            self.state['F'][2][:] = self.state['L'][2][:]
            self.state['L'][2][:] = temp
    def move_F(self, clockwise=True):
        self.rotate_face('F', clockwise)
        if clockwise:
            temp = self.state['U'][2][:]
            self.state['U'][2][:] = [self.state['L'][2-i][2] for i in range(3)]
            for i in range(3):
                self.state['L'][i][2] = self.state['D'][0][i]
            self.state['D'][0][:] = [self.state['R'][2-i][0] for i in range(3)]
            for i in range(3):
                self.state['R'][i][0] = temp[i]
        else:
            temp = self.state['U'][2][:]
            self.state['U'][2][:] = [self.state['R'][i][0] for i in range(3)]
            for i in range(3):
                self.state['R'][i][0] = self.state['D'][0][2-i]
            self.state['D'][0][:] = [self.state['L'][i][2] for i in range(3)]
            for i in range(3):
                self.state['L'][i][2] = temp[2-i]
    def move_B(self, clockwise=True):
        self.rotate_face('B', clockwise)
        if clockwise:
            temp = self.state['U'][0][:]
            self.state['U'][0][:] = [self.state['R'][i][2] for i in range(3)]
            for i in range(3):
                self.state['R'][i][2] = self.state['D'][2][2-i]
            self.state['D'][2][:] = [self.state['L'][i][0] for i in range(3)]
            for i in range(3):
                self.state['L'][i][0] = temp[2-i]
        else:
            temp = self.state['U'][0][:]
            self.state['U'][0][:] = [self.state['L'][2-i][0] for i in range(3)]
            for i in range(3):
                self.state['L'][i][0] = self.state['D'][2][i]
            self.state['D'][2][:] = [self.state['R'][2-i][2] for i in range(3)]
            for i in range(3):
                self.state['R'][i][2] = temp[i]
    def apply_move(self, move):
        if move in ["R", "R'", "L", "L'", "U", "U'", "D", "D'", "F", "F'", "B", "B'"]:
            face = move[0]
            if face in self.animations:
                return
            target = 90 if len(move) == 1 else -90
            self.animations[face] = {'move': move, 'progress': 0, 'target': target, 'speed': 3}

def main():
    pygame.init()
    screen = pygame.display.set_mode((800,600))
    pygame.display.set_caption("3D Rubik's Cube")
    clock = pygame.time.Clock()
    cube = RubiksCube3D()
    center = (400,300)
    move_str = ""
    angle_x, angle_y, angle_z = 0.0, 0.0, 0.0
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == pygame.K_LEFT:
                    angle_y -= 0.1
                elif event.key == pygame.K_RIGHT:
                    angle_y += 0.1
                elif event.key == pygame.K_UP:
                    angle_x -= 0.1
                elif event.key == pygame.K_DOWN:
                    angle_x += 0.1
                elif event.key == pygame.K_r:
                    cube.apply_move("R")
                    move_str += " R"
                elif event.key == pygame.K_t:
                    cube.apply_move("R'")
                    move_str += " R'"
                elif event.key == pygame.K_f:
                    cube.apply_move("F")
                    move_str += " F"
                elif event.key == pygame.K_g:
                    cube.apply_move("F'")
                    move_str += " F'"
                elif event.key == pygame.K_u:
                    cube.apply_move("U")
                    move_str += " U"
                elif event.key == pygame.K_i:
                    cube.apply_move("U'")
                    move_str += " U'"
                elif event.key == pygame.K_d:
                    cube.apply_move("D")
                    move_str += " D"
                elif event.key == pygame.K_s:
                    cube.apply_move("D'")
                    move_str += " D'"
                elif event.key == pygame.K_l:
                    cube.apply_move("L")
                    move_str += " L"
                elif event.key == pygame.K_k:
                    cube.apply_move("L'")
                    move_str += " L'"
                elif event.key == pygame.K_b:
                    cube.apply_move("B")
                    move_str += " B"
                elif event.key == pygame.K_n:
                    cube.apply_move("B'")
                    move_str += " B'"
        # Update animations for any ongoing move
        faces_to_remove = []
        for face, anim in cube.animations.items():
            anim['progress'] += anim['speed']
            if abs(anim['progress']) >= abs(anim['target']):
                anim['progress'] = anim['target']
                if anim['move'] == "R":
                    cube.move_R(True)
                elif anim['move'] == "R'":
                    cube.move_R(False)
                elif anim['move'] == "L":
                    cube.move_L(True)
                elif anim['move'] == "L'":
                    cube.move_L(False)
                elif anim['move'] == "U":
                    cube.move_U(True)
                elif anim['move'] == "U'":
                    cube.move_U(False)
                elif anim['move'] == "D":
                    cube.move_D(True)
                elif anim['move'] == "D'":
                    cube.move_D(False)
                elif anim['move'] == "F":
                    cube.move_F(True)
                elif anim['move'] == "F'":
                    cube.move_F(False)
                elif anim['move'] == "B":
                    cube.move_B(True)
                elif anim['move'] == "B'":
                    cube.move_B(False)
                faces_to_remove.append(face)
        for face in faces_to_remove:
            del cube.animations[face]
        # Constant overall cube rotation
        angle_x += 0.005
        angle_y += 0.005
        angle_z += 0.005
        rot = rotation_matrix_full(angle_x, angle_y, angle_z)
        screen.fill((30,30,30))
        polys = cube.get_all_polygons()
        drawn = []
        for poly, col in polys:
            proj = [ (int((np.dot(rot, np.array(p))[0] * 500)/(np.dot(rot, np.array(p))[2]+8)+center[0]),
                      int((-np.dot(rot, np.array(p))[1] * 500)/(np.dot(rot, np.array(p))[2]+8)+center[1]) )
                     for p in poly ]
            avg_z = np.mean([np.dot(rot, np.array(p))[2] for p in poly])
            drawn.append((avg_z, proj, col))
        drawn.sort(key=lambda x: x[0], reverse=True)
        for _, pts, col in drawn:
            pygame.draw.polygon(screen, col, pts)
            pygame.draw.polygon(screen, (0,0,0), pts, 1)
        font = pygame.font.SysFont(None, 24)
        txt = font.render("Moves:" + move_str, True, (255,255,255))
        screen.blit(txt, (20,20))
        pygame.display.flip()
        clock.tick(30)

if __name__ == '__main__':
    main()
