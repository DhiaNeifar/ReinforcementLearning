from actions.action import Action
from config import sides


class RotateDown(Action):
    def __init__(self, clockwise=True):
        super().__init__()
        self.clockwise = clockwise

    def ApplyRotation(self, Rcube):
        # Rotate the Right face (layer 1) using the provided rotate function.
        self.RotateFace(Rcube, sides["RIGHT"], self.clockwise)

        # Save a copy of the affected stickers from the UP face's right column.
        temp = Rcube.state[sides["UP"], :, 2].copy()

        if self.clockwise:
            # For a clockwise R move:
            # UP right column becomes the FRONT right column.
            Rcube.state[sides["UP"], :, 2] = Rcube.state[sides["FRONT"], :, 2].copy()
            # FRONT right column becomes the DOWN right column.
            Rcube.state[sides["FRONT"], :, 2] = Rcube.state[sides["DOWN"], :, 2].copy()
            # DOWN right column becomes the reversed BACK left column.
            Rcube.state[sides["DOWN"], :, 2] = Rcube.state[sides["BACK"], :, 0][::-1]
            # BACK left column becomes the reversed saved UP right column.
            Rcube.state[sides["BACK"], :, 0] = temp[::-1]
        else:
            # For a counterclockwise R move:
            # UP right column gets the reversed BACK left column.
            Rcube.state[sides["UP"], :, 2] = Rcube.state[sides["BACK"], :, 0][::-1]
            # BACK left column gets the reversed DOWN right column.
            Rcube.state[sides["BACK"], :, 0] = Rcube.state[sides["DOWN"], :, 2][::-1]
            # DOWN right column becomes the FRONT right column.
            Rcube.state[sides["DOWN"], :, 2] = Rcube.state[sides["FRONT"], :, 2].copy()
            # FRONT right column gets the saved UP right column.
            Rcube.state[sides["FRONT"], :, 2] = temp.copy()

        return Rcube
