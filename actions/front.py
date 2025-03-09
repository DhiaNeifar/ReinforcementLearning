from actions.action import Action
from config import layers


class RotateFront(Action):
    def __init__(self, clockwise=True):
        super().__init__()
        self.clockwise = clockwise


    def ApplyRotation(self, Rcube):
        self.RotateFace(Rcube, layers["RIGHT"], self.clockwise)
        temp = Rcube.state[layers["UP"], :, 2].copy()
        if self.clockwise:
            # TOP's bottom row <- LEFT's right column (reversed top-to-bottom)
            Rcube.state[layers["UP"], :, 2] = Rcube.state[layers["LEFT"], :, 2]
            # LEFT's right column <- BOTTOM's top row
            Rcube.state[layers["LEFT"], :, 2] = Rcube.state[layers["DOWN"], :, 2]
            # BOTTOM's top row <- RIGHT's left column (reversed top-to-bottom)
            Rcube.state[layers["DOWN"], :, 2] = Rcube.state[layers["RIGHT"], ::-1, 0]
            # RIGHT's left column <- (old) TOP's bottom row
            Rcube.state[layers["RIGHT"], ::-1, 0] = temp
        else:
            # TOP's bottom row <- RIGHT's left column
            Rcube.state[layers["UP"], :, 2] = Rcube.state[layers["RIGHT"], ::-1, 0]
            # RIGHT's left column <- BOTTOM's top row (reversed)
            Rcube.state[layers["RIGHT"], ::-1, 0] = Rcube.state[layers["DOWN"], :, 2]
            # BOTTOM's top row <- LEFT's right column
            Rcube.state[layers["DOWN"], :, 2] = Rcube.state[layers["LEFT"], :, 2]
            # LEFT's right column <- (old) TOP's bottom row (reversed)
            Rcube.state[layers["LEFT"], :, 2] = temp

