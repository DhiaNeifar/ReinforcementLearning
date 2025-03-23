import random
import pygame

import numpy as np
from rubikcube import RubikCube


class RubiksCube:
    def __init__(self):
        # Initialize cube state: 6 faces (F, R, B, L, U, D), each a 3x3 grid.
        # Each face is initially filled with its index.
        self.state = np.zeros((6, 3, 3), dtype=np.int8)
        for face in range(6):
            self.state[face, :, :] = face

    def rotate_face(self, face, clockwise=True):
        # Rotate the face 90°.
        # np.rot90 rotates counterclockwise by default.
        # For a clockwise rotation, we use k=-1.
        if clockwise:
            self.state[face] = np.rot90(self.state[face], k=-1)
        else:
            self.state[face] = np.rot90(self.state[face], k=1)

    def move_F(self, clockwise=True):
        # F (Front) move: rotate face 0.
        self.rotate_face(0, clockwise)
        # The four adjacent edges affected are:
        # - Up (face 4): bottom row (row index 2)
        # - Right (face 1): left column (column index 0)
        # - Down (face 5): top row (row index 0)
        # - Left (face 3): right column (column index 2)
        if clockwise:
            temp = self.state[4, 2, :].copy()
            # Up bottom row becomes reversed Left right column.
            self.state[4, 2, :] = self.state[3, :, 2][::-1]
            # Left right column becomes Down top row.
            self.state[3, :, 2] = self.state[5, 0, :].copy()
            # Down top row becomes reversed Right left column.
            self.state[5, 0, :] = self.state[1, :, 0][::-1]
            # Right left column becomes saved Up bottom row.
            self.state[1, :, 0] = temp
        else:
            temp = self.state[4, 2, :].copy()
            # Up bottom row gets Right left column (directly).
            self.state[4, 2, :] = self.state[1, :, 0].copy()
            # Right left column gets reversed Down top row.
            self.state[1, :, 0] = self.state[5, 0, :][::-1]
            # Down top row gets Left right column.
            self.state[5, 0, :] = self.state[3, :, 2].copy()
            # Left right column gets reversed saved Up bottom row.
            self.state[3, :, 2] = temp[::-1]

    def move_R(self, clockwise=True):
        # R (Right) move: rotate face 1.
        self.rotate_face(1, clockwise)
        # Affected adjacent edges:
        # - Up (face 4): right column (col index 2)
        # - Back (face 2): left column (col index 0) – note: back face orientation requires reversal
        # - Down (face 5): right column (col index 2)
        # - Front (face 0): right column (col index 2)
        if clockwise:
            temp = self.state[4, :, 2].copy()
            self.state[4, :, 2] = self.state[0, :, 2].copy()
            self.state[0, :, 2] = self.state[5, :, 2].copy()
            self.state[5, :, 2] = self.state[2, :, 0][::-1]
            self.state[2, :, 0] = temp[::-1]
        else:
            temp = self.state[4, :, 2].copy()
            self.state[4, :, 2] = self.state[2, :, 0][::-1]
            self.state[2, :, 0] = self.state[5, :, 2][::-1]
            self.state[5, :, 2] = self.state[0, :, 2].copy()
            self.state[0, :, 2] = temp

    def move_L(self, clockwise=True):
        # L (Left) move: rotate face 3.
        self.rotate_face(3, clockwise)
        # Affected adjacent edges:
        # - Up (face 4): left column (col index 0)
        # - Front (face 0): left column (col index 0)
        # - Down (face 5): left column (col index 0)
        # - Back (face 2): right column (col index 2) – with reversal
        if clockwise:
            temp = self.state[4, :, 0].copy()
            self.state[4, :, 0] = self.state[2, :, 2][::-1]
            self.state[2, :, 2] = self.state[5, :, 0][::-1]
            self.state[5, :, 0] = self.state[0, :, 0].copy()
            self.state[0, :, 0] = temp
        else:
            temp = self.state[4, :, 0].copy()
            self.state[4, :, 0] = self.state[0, :, 0].copy()
            self.state[0, :, 0] = self.state[5, :, 0].copy()
            self.state[5, :, 0] = self.state[2, :, 2][::-1]
            self.state[2, :, 2] = temp[::-1]

    def move_U(self, clockwise=True):
        # U (Up) move: rotate face 4.
        self.rotate_face(4, clockwise)
        # Adjacent edges on the side faces (F=0, R=1, B=2, L=3).
        # When viewed from above:
        # Clockwise U move should cycle:
        #   Front top row -> Right top row -> Back top row -> Left top row -> Front top row.
        if clockwise:
            temp = self.state[0, 0, :].copy()  # save Front top row
            self.state[0, 0, :] = self.state[1, 0, :].copy()  # Front gets Left
            self.state[1, 0, :] = self.state[2, 0, :].copy()  # Left gets Back
            self.state[2, 0, :] = self.state[3, 0, :].copy()  # Back gets Right
            self.state[3, 0, :] = temp  # Right gets old Front
        else:
            temp = self.state[0, 0, :].copy()  # save Front top row
            self.state[0, 0, :] = self.state[3, 0, :].copy()  # Front gets Right
            self.state[3, 0, :] = self.state[2, 0, :].copy()  # Right gets Back
            self.state[2, 0, :] = self.state[1, 0, :].copy()  # Back gets Left
            self.state[1, 0, :] = temp  # Left gets old Front

    def move_D(self, clockwise=True):
        # D (Down) move: rotate face 5.
        self.rotate_face(5, clockwise)
        # Affected adjacent edges:
        # - Front (face 0): bottom row (row index 2)
        # - Right (face 1): bottom row (row index 2)
        # - Back (face 2): bottom row (row index 2)
        # - Left (face 3): bottom row (row index 2)
        if clockwise:
            temp = self.state[0, 2, :].copy()
            self.state[0, 2, :] = self.state[3, 2, :].copy()

            self.state[3, 2, :] = self.state[2, 2, :].copy()

            self.state[2, 2, :] = self.state[1, 2, :].copy()

            self.state[1, 2, :] = temp
        else:
            temp = self.state[0, 2, :].copy()
            self.state[0, 2, :] = self.state[1, 2, :].copy()

            self.state[1, 2, :] = self.state[2, 2, :].copy()

            self.state[2, 2, :] = self.state[3, 2, :].copy()

            self.state[3, 2, :] = temp

    def move_B(self, clockwise=True):
        # B (Back) move: rotate face 2.
        self.rotate_face(2, clockwise)
        # Affected adjacent edges:
        # For the Back face, the affected edges are:
        # - Up (face 4): top row (row index 0)
        # - Right (face 1): right column (col index 2)
        # - Down (face 5): bottom row (row index 2)
        # - Left (face 3): left column (col index 0)
        # Note: due to the back face’s orientation, some reversals are necessary.
        if clockwise:
            temp = self.state[4, 0, :].copy()
            self.state[4, 0, :] = self.state[1, :, 2].copy()
            self.state[1, :, 2] = self.state[5, 2, :][::-1]
            self.state[5, 2, :] = self.state[3, :, 0].copy()
            self.state[3, :, 0] = temp[::-1]
        else:
            temp = self.state[4, 0, :].copy()
            self.state[4, 0, :] = self.state[3, :, 0][::-1]
            self.state[3, :, 0] = self.state[5, 2, :].copy()
            self.state[5, 2, :] = self.state[1, :, 2][::-1]
            self.state[1, :, 2] = temp

    def execute_move(self, move, clockwise=True):
        # Executes a move given by a character: 'F', 'R', 'L', 'U', 'D', or 'B'.
        if move == 'F':
            self.move_F(clockwise)
        elif move == 'R':
            self.move_R(clockwise)
        elif move == 'L':
            self.move_L(clockwise)
        elif move == 'U':
            self.move_U(clockwise)
        elif move == 'D':
            self.move_D(clockwise)
        elif move == 'B':
            self.move_B(clockwise)
        else:
            raise ValueError("Invalid move. Use one of 'F', 'R', 'L', 'U', 'D', or 'B'.")

    def __str__(self):
        # Returns a simple string representation for debugging.
        face_names = ['F', 'R', 'B', 'L', 'U', 'D']
        result = ""
        for i, name in enumerate(face_names):
            result += f"{name} face:\n{self.state[i]}\n\n"
        return result


# Example usage:
if __name__ == '__main__':
    pygame.init()
    Rcube = RubikCube(pygame.display.set_mode((0, 0)))
    Rcube.InitializeRubikCube()


    cube = RubiksCube()

    message = "L' R D U' B U' U U D L' L D L U' F' F' R' B U' R R D U U' D R U F U F R U U F L D L' D R' U' F' F D D F' F B R' R' F'"
    message = message.split(' ')[:15]
    print(" ".join(message))
    moves = [(move[0], True) if len(move) == 1 else (move[0], False) for move in message]
    face_names = ['F', 'R', 'B', 'L', 'U', 'D']
    for ind, (move, cw) in enumerate(moves):
        cube.execute_move(move, clockwise=cw)
        Rcube.AlterState(face_names.index(move), int(cw))
    print(cube.state)
        # if not np.all(cube.state == Rcube.state):
        #     print("not working")
        #     break





