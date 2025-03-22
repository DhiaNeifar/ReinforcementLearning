from actions.action import Action
from config import layers


class RotateLeft(Action):
    def __init__(self, clockwise=True):
        super().__init__()
        self.clockwise = clockwise

    def ApplyRotation(self, Rcube):
        # Rotate the Left face (layer 3) using the provided rotate function.
        self.RotateFace(Rcube, layers["LEFT"], self.clockwise)

        # Save a copy of the affected stickers from the UP face's left column.
        temp = Rcube.state[layers["UP"], :, 0].copy()

        if self.clockwise:
            # For a clockwise L move:
            # UP left column becomes the reversed BACK right column.
            Rcube.state[layers["UP"], :, 0] = Rcube.state[layers["BACK"], :, 2][::-1]
            # BACK right column becomes the reversed DOWN left column.
            Rcube.state[layers["BACK"], :, 2] = Rcube.state[layers["DOWN"], :, 0][::-1]
            # DOWN left column becomes the FRONT left column.
            Rcube.state[layers["DOWN"], :, 0] = Rcube.state[layers["FRONT"], :, 0].copy()
            # FRONT left column becomes the saved UP left column.
            Rcube.state[layers["FRONT"], :, 0] = temp
        else:
            # For a counterclockwise L move:
            # UP left column gets the FRONT left column.
            Rcube.state[layers["UP"], :, 0] = Rcube.state[layers["FRONT"], :, 0].copy()
            # FRONT left column gets the DOWN left column.
            Rcube.state[layers["FRONT"], :, 0] = Rcube.state[layers["DOWN"], :, 0].copy()
            # DOWN left column gets the reversed BACK right column.
            Rcube.state[layers["DOWN"], :, 0] = Rcube.state[layers["BACK"], :, 2][::-1]
            # BACK right column gets the reversed saved UP left column.
            Rcube.state[layers["BACK"], :, 2] = temp[::-1]

        return Rcube
