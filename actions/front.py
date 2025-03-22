from actions.action import Action
from config import sides


class RotateFront(Action):
    def __init__(self, clockwise=True):
        super().__init__()
        self.clockwise = clockwise

    def ApplyRotation(self, Rcube):
        # Rotate the front face (face 0) using the given rotate function.
        self.RotateFace(Rcube, sides["FRONT"], self.clockwise)

        # Save the affected stickers from the UP face's bottom row.
        temp = Rcube.state[sides["UP"], 2, :].copy()

        if self.clockwise:
            # For a clockwise F move:
            # UP bottom row becomes the reversed LEFT right column.
            Rcube.state[sides["UP"], 2, :] = Rcube.state[sides["LEFT"], :, 2][::-1]
            # LEFT right column becomes DOWN top row.
            Rcube.state[sides["LEFT"], :, 2] = Rcube.state[sides["DOWN"], 0, :].copy()
            # DOWN top row becomes the reversed RIGHT left column.
            Rcube.state[sides["DOWN"], 0, :] = Rcube.state[sides["RIGHT"], :, 0][::-1]
            # RIGHT left column becomes the saved UP bottom row.
            Rcube.state[sides["RIGHT"], :, 0] = temp
        else:
            # For a counterclockwise F move:
            # UP bottom row gets RIGHT left column.
            Rcube.state[sides["UP"], 2, :] = Rcube.state[sides["RIGHT"], :, 0].copy()
            # RIGHT left column gets the reversed DOWN top row.
            Rcube.state[sides["RIGHT"], :, 0] = Rcube.state[sides["DOWN"], 0, :][::-1]
            # DOWN top row gets LEFT right column.
            Rcube.state[sides["DOWN"], 0, :] = Rcube.state[sides["LEFT"], :, 2].copy()
            # LEFT right column gets the reversed saved UP bottom row.
            Rcube.state[sides["LEFT"], :, 2] = temp[::-1]
        return Rcube
