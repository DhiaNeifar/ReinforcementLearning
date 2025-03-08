from actions.action import Action
from config import layers


class RotateRight(Action):
    def __init__(self, ActionType='R', clockwise=True):
        super().__init__(ActionType)
        self.clockwise = clockwise
        assert self.type in ["R", "R'"]
        assert self.type == "R" and clockwise == True or self.type == "R'" and clockwise == False


    def ApplyRotation(self, Rcube):
        self.RotateFace(Rcube, layers["RIGHT"], self.clockwise)
        if self.clockwise:
            temp = Rcube.state[layers["UP"], :, 2].copy()  # right column of TOP
            # TOP's right column <- FRONT's right column
            Rcube.state[layers["UP"], :, 2] = Rcube.state[layers["FRONT"], :, 2]
            # FRONT's right column <- BOTTOM's right column
            Rcube.state[layers["FRONT"], :, 2] = Rcube.state[layers["DOWN"], :, 2]
            # BOTTOM's right column <- BACK's left column (reversed vertically)
            Rcube.state[layers["DOWN"], :, 2] = Rcube.state[layers["BACK"], ::-1, 0]
            # BACK's left column <- old TOP's right column (reversed vertically)
            Rcube.state[layers["BACK"], ::-1, 0] = temp
        else:
            temp = Rcube.state[layers["UP"], :, 2].copy()
            # TOP's right column <- BACK's left column (reversed vertically)
            Rcube.state[layers["UP"], :, 2] = Rcube.state[layers["BACK"], ::-1, 0]
            # BACK's left column <- BOTTOM's right column (reversed vertically)
            Rcube.state[layers["BACK"], ::-1, 0] = Rcube.state[layers["DOWN"], :, 2]
            # BOTTOM's right column <- FRONT's right column
            Rcube.state[layers["DOWN"], :, 2] = Rcube.state[layers["UP"], :, 2]
            # FRONT's right column <- old TOP's right column
            Rcube.state[layers["UP"], :, 2] = temp

