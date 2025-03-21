# main.py
from numpy.core.defchararray import center

# -*- coding: utf-8 -*-
# Author: Dhia Neifar <neifar@umich.edu>


from config import HEIGHT, WIDTH, FPS
from enums.colors import Color
from game_manager import GameManager
from point import Point3d
from rubikcube import RubikCube
from cube import Cube
from referential import Referential


def main() -> None:
    game_caption = "rubik's cube"

    game_manager = GameManager(game_caption, height=HEIGHT, width=WIDTH, fps=FPS, BackgroundColor=Color.BEIGE.value)
    game_surface = game_manager.surface

    RCube = RubikCube(game_surface)
    cube = Cube(game_surface, center=Point3d(2, 0, 0))
    ref = Referential(game_surface)
    game_manager.AddObjects([
        RCube,
        # cube,
        # ref
    ])
    game_manager.run()


if __name__ == '__main__':
    main()
