from actions.action import Action
from config import sides


class RotateBack(Action):
    def __init__(self, clockwise=True):
        super().__init__()
        self.clockwise = clockwise

    def ApplyRotation(self, Rcube):
        # Rotate the Back face (layer BACK) using the provided rotate function.
        self.RotateFace(Rcube, sides["BACK"], self.clockwise)

        # Save the affected stickers from the UP top row.
        temp = Rcube.state[sides["UP"], 0, :].copy()

        if self.clockwise:
            # For a clockwise B move:
            # UP top row becomes the RIGHT right column.
            Rcube.state[sides["UP"], 0, :] = Rcube.state[sides["RIGHT"], :, 2].copy()
            # RIGHT right column becomes the reversed DOWN bottom row.
            Rcube.state[sides["RIGHT"], :, 2] = Rcube.state[sides["DOWN"], 2, :][::-1]
            # DOWN bottom row becomes the LEFT left column.
            Rcube.state[sides["DOWN"], 2, :] = Rcube.state[sides["LEFT"], :, 0].copy()
            # LEFT left column becomes the reversed saved UP top row.
            Rcube.state[sides["LEFT"], :, 0] = temp[::-1]
        else:
            # For a counterclockwise B move:
            # UP top row gets the reversed LEFT left column.
            Rcube.state[sides["UP"], 0, :] = Rcube.state[sides["LEFT"], :, 0][::-1]
            # LEFT left column gets the DOWN bottom row.
            Rcube.state[sides["LEFT"], :, 0] = Rcube.state[sides["DOWN"], 2, :].copy()
            # DOWN bottom row gets the reversed RIGHT right column.
            Rcube.state[sides["DOWN"], 2, :] = Rcube.state[sides["RIGHT"], :, 2][::-1]
            # RIGHT right column gets the saved UP top row.
            Rcube.state[sides["RIGHT"], :, 2] = temp
        return Rcube
