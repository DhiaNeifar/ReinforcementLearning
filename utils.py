import random
import numpy as np

###############################################################################
# FACE INDICES (you can adapt if you prefer a different labeling):
#   0 = FRONT  (initially all 0: "Yellow"?)
#   1 = RIGHT  (initially all 1: "Red"?)
#   2 = BACK   (initially all 2: "White"?)
#   3 = LEFT   (initially all 3: "Orange"?)
#   4 = TOP    (initially all 4: "Green"?)
#   5 = BOTTOM (initially all 5: "Blue"?)
###############################################################################

def init_cube():
    """
    Create a 6x3x3 numpy array for a "solved" cube:
      Face i has all stickers = i.
    """
    cube = np.zeros((6, 3, 3), dtype=int)
    for face in range(6):
        cube[face, :, :] = face
    return cube

def rotate_face_90(cube, face, clockwise=True):
    """
    Rotate the 3x3 sub-array for `face` by 90°.
      - If clockwise=True, that is np.rot90(..., k=3)
        (since np.rot90(..., k=1) is a 90° CCW).
      - If clockwise=False, do a 90° CCW rotation.
    """
    print(cube.shape)
    if clockwise:
        print(cube[face].shape)
        cube[face] = np.rot90(cube[face], k=3)  # 90° clockwise

    else:
        cube[face] = np.rot90(cube[face], k=1)  # 90° counterclockwise

    print(cube.shape)

###############################################################################
# FRONT (F) face turn
###############################################################################
def rotate_F(cube, clockwise=True):
    """
    Turn the FRONT face 90° in either clockwise or counterclockwise direction.
    """
    FRONT, RIGHT, BACK, LEFT, TOP, BOTTOM = 0, 1, 2, 3, 4, 5

    # 1) Rotate the FRONT face itself
    old_cube = np.copy(cube)
    rotate_face_90(cube, FRONT, clockwise)
    if np.array_equal(old_cube, cube):
        print("change here")
    # 2) Cycle the adjacent edge strips:
    if clockwise:
        # Save the bottom row of TOP
        temp = cube[TOP, 2, :].copy()
        # TOP's bottom row <- LEFT's right column (reversed top-to-bottom)
        cube[TOP, 2, :] = cube[LEFT, :, 2][::-1]
        # LEFT's right column <- BOTTOM's top row
        cube[LEFT, :, 2] = cube[BOTTOM, 0, :]
        # BOTTOM's top row <- RIGHT's left column (reversed top-to-bottom)
        cube[BOTTOM, 0, :] = cube[RIGHT, :, 0][::-1]
        # RIGHT's left column <- (old) TOP's bottom row
        cube[RIGHT, :, 0] = temp
    else:
        # Counterclockwise (the inverse cycle)
        temp = cube[TOP, 2, :].copy()
        # TOP's bottom row <- RIGHT's left column
        cube[TOP, 2, :] = cube[RIGHT, :, 0]
        # RIGHT's left column <- BOTTOM's top row (reversed)
        cube[RIGHT, :, 0] = cube[BOTTOM, 0, :][::-1]
        # BOTTOM's top row <- LEFT's right column
        cube[BOTTOM, 0, :] = cube[LEFT, :, 2]
        # LEFT's right column <- (old) TOP's bottom row (reversed)
        cube[LEFT, :, 2] = temp[::-1]

###############################################################################
# BACK (B) face turn
###############################################################################
def rotate_B(cube, clockwise=True):
    """
    Turn the BACK face 90° in either clockwise or counterclockwise direction.
    """
    FRONT, RIGHT, BACK, LEFT, TOP, BOTTOM = 0, 1, 2, 3, 4, 5

    # Rotate the BACK face
    old_cube = np.copy(cube)
    rotate_face_90(cube, FRONT, clockwise)
    if np.array_equal(old_cube, cube):
        print("change here")
    # Cycle adjacent strips
    if clockwise:
        temp = cube[TOP, 0, :].copy()
        # TOP's top row <- RIGHT's right column
        cube[TOP, 0, :] = cube[RIGHT, :, 2]
        # RIGHT's right column <- BOTTOM's bottom row (reversed)
        cube[RIGHT, :, 2] = cube[BOTTOM, 2, :][::-1]
        # BOTTOM's bottom row <- LEFT's left column
        cube[BOTTOM, 2, :] = cube[LEFT, :, 0][::-1]
        # LEFT's left column <- old TOP's top row
        cube[LEFT, :, 0] = temp
    else:
        temp = cube[TOP, 0, :].copy()
        # TOP's top row <- LEFT's left column
        cube[TOP, 0, :] = cube[LEFT, :, 0]
        # LEFT's left column <- BOTTOM's bottom row (reversed)
        cube[LEFT, :, 0] = cube[BOTTOM, 2, :][::-1]
        # BOTTOM's bottom row <- RIGHT's right column (reversed)
        cube[BOTTOM, 2, :] = cube[RIGHT, :, 2][::-1]
        # RIGHT's right column <- old TOP's top row
        cube[RIGHT, :, 2] = temp

###############################################################################
# RIGHT (R) face turn
###############################################################################
def rotate_R(cube, clockwise=True):
    """
    Turn the RIGHT face 90° in either clockwise or counterclockwise direction.
    """
    FRONT, RIGHT, BACK, LEFT, TOP, BOTTOM = 0, 1, 2, 3, 4, 5

    old_cube = np.copy(cube)
    rotate_face_90(cube, FRONT, clockwise)
    if np.array_equal(old_cube, cube):
        print("change here")
    if clockwise:
        temp = cube[TOP, :, 2].copy()  # right column of TOP
        # TOP's right column <- FRONT's right column
        cube[TOP, :, 2] = cube[FRONT, :, 2]
        # FRONT's right column <- BOTTOM's right column
        cube[FRONT, :, 2] = cube[BOTTOM, :, 2]
        # BOTTOM's right column <- BACK's left column (reversed vertically)
        cube[BOTTOM, :, 2] = cube[BACK, ::-1, 0]
        # BACK's left column <- old TOP's right column (reversed vertically)
        cube[BACK, ::-1, 0] = temp
    else:
        temp = cube[TOP, :, 2].copy()
        # TOP's right column <- BACK's left column (reversed vertically)
        cube[TOP, :, 2] = cube[BACK, ::-1, 0]
        # BACK's left column <- BOTTOM's right column (reversed vertically)
        cube[BACK, ::-1, 0] = cube[BOTTOM, :, 2]
        # BOTTOM's right column <- FRONT's right column
        cube[BOTTOM, :, 2] = cube[FRONT, :, 2]
        # FRONT's right column <- old TOP's right column
        cube[FRONT, :, 2] = temp

###############################################################################
# LEFT (L) face turn
###############################################################################
def rotate_L(cube, clockwise=True):
    """
    Turn the LEFT face 90° in either clockwise or counterclockwise direction.
    """
    FRONT, RIGHT, BACK, LEFT, TOP, BOTTOM = 0, 1, 2, 3, 4, 5

    old_cube = np.copy(cube)
    rotate_face_90(cube, FRONT, clockwise)
    if np.array_equal(old_cube, cube):
        print("change here")
    if clockwise:
        temp = cube[TOP, :, 0].copy()  # left column of TOP
        # TOP's left column <- BACK's right column (reversed vertically)
        cube[TOP, :, 0] = cube[BACK, ::-1, 2]
        # BACK's right column <- BOTTOM's left column (reversed vertically)
        cube[BACK, ::-1, 2] = cube[BOTTOM, :, 0]
        # BOTTOM's left column <- FRONT's left column
        cube[BOTTOM, :, 0] = cube[FRONT, :, 0]
        # FRONT's left column <- old TOP's left column
        cube[FRONT, :, 0] = temp
    else:
        temp = cube[TOP, :, 0].copy()
        # TOP's left column <- FRONT's left column
        cube[TOP, :, 0] = cube[FRONT, :, 0]
        # FRONT's left column <- BOTTOM's left column
        cube[FRONT, :, 0] = cube[BOTTOM, :, 0]
        # BOTTOM's left column <- BACK's right column (reversed vertically)
        cube[BOTTOM, :, 0] = cube[BACK, ::-1, 2]
        # BACK's right column <- old TOP's left column (reversed vertically)
        cube[BACK, ::-1, 2] = temp

###############################################################################
# UP (U) face turn
###############################################################################
def rotate_U(cube, clockwise=True):
    """
    Turn the TOP face 90° in either clockwise or counterclockwise direction.
    """
    FRONT, RIGHT, BACK, LEFT, TOP, BOTTOM = 0, 1, 2, 3, 4, 5

    old_cube = np.copy(cube)
    rotate_face_90(cube, FRONT, clockwise)
    if np.array_equal(old_cube, cube):
        print("change here")
    if clockwise:
        temp = cube[FRONT, 0, :].copy()
        # FRONT's top row <- RIGHT's top row
        cube[FRONT, 0, :] = cube[RIGHT, 0, :]
        # RIGHT's top row <- BACK's top row
        cube[RIGHT, 0, :] = cube[BACK, 0, :]
        # BACK's top row <- LEFT's top row
        cube[BACK, 0, :] = cube[LEFT, 0, :]
        # LEFT's top row <- old FRONT's top row
        cube[LEFT, 0, :] = temp
    else:
        temp = cube[FRONT, 0, :].copy()
        # FRONT's top row <- LEFT's top row
        cube[FRONT, 0, :] = cube[LEFT, 0, :]
        # LEFT's top row <- BACK's top row
        cube[LEFT, 0, :] = cube[BACK, 0, :]
        # BACK's top row <- RIGHT's top row
        cube[BACK, 0, :] = cube[RIGHT, 0, :]
        # RIGHT's top row <- old FRONT's top row
        cube[RIGHT, 0, :] = temp

###############################################################################
# DOWN (D) face turn
###############################################################################
def rotate_D(cube, clockwise=True):
    """
    Turn the BOTTOM face 90° in either clockwise or counterclockwise direction.
    """
    FRONT, RIGHT, BACK, LEFT, TOP, BOTTOM = 0, 1, 2, 3, 4, 5
    old_cube = np.copy(cube)
    rotate_face_90(cube, FRONT, clockwise)
    if np.array_equal(old_cube, cube):
        print("change here")
    if clockwise:
        temp = cube[FRONT, 2, :].copy()
        # FRONT's bottom row <- LEFT's bottom row
        cube[FRONT, 2, :] = cube[LEFT, 2, :]
        # LEFT's bottom row <- BACK's bottom row
        cube[LEFT, 2, :] = cube[BACK, 2, :]
        # BACK's bottom row <- RIGHT's bottom row
        cube[BACK, 2, :] = cube[RIGHT, 2, :]
        # RIGHT's bottom row <- old FRONT's bottom row
        cube[RIGHT, 2, :] = temp
    else:
        temp = cube[FRONT, 2, :].copy()
        # FRONT's bottom row <- RIGHT's bottom row
        cube[FRONT, 2, :] = cube[RIGHT, 2, :]
        # RIGHT's bottom row <- BACK's bottom row
        cube[RIGHT, 2, :] = cube[BACK, 2, :]
        # BACK's bottom row <- LEFT's bottom row
        cube[BACK, 2, :] = cube[LEFT, 2, :]
        # LEFT's bottom row <- old FRONT's bottom row
        cube[LEFT, 2, :] = temp


###############################################################################
# DEMO USAGE
###############################################################################
if __name__ == "__main__":
    Action = {
        0: rotate_F,
        1: rotate_R,
        2: rotate_B,
        3: rotate_L,
        4: rotate_U,
        5: rotate_D,
    }
    CLOCK = {
        0: True,
        1: False,
    }
    # Create a solved cube
    cube = init_cube()

    NumActions = 30
    for _ in range(NumActions):
        action = Action[random.randint(0, 5)]
        action(cube, clockwise=CLOCK[random.randint(0, 1)])
