import numpy as np

from colors import Color
from config import HEIGHT, WIDTH, FPS
from game import GameManager
from referential import Referential
from rubikcube import RubikCube


def main() -> None:
    game_caption = 'cube'

    game_manager = GameManager(game_caption, height=HEIGHT, width=WIDTH, fps=FPS, BackgroundColor=Color.BEIGE.value)
    game_surface = game_manager.surface

    RCube = RubikCube(game_surface)
    # for cube in RCube.cubes[::3]:
    #     cube.rotation[2] -= np.pi * 0.5
    # cube.draw()
    referential = Referential(game_surface)
    game_manager.AddObjects([
        RCube,
        # referential,
    ])
    game_manager.run()


if __name__ == '__main__':
    main()
