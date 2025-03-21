# main.py

# -*- coding: utf-8 -*-
# Author: Dhia Neifar <neifar@umich.edu>


from config import HEIGHT, WIDTH, FPS
from enums.colors import Color
from game_manager import GameManager
from rubikcube import RubikCube
from cube import Cube


def main() -> None:
    game_caption = "rubik's cube"

    game_manager = GameManager(game_caption, height=HEIGHT, width=WIDTH, fps=FPS, BackgroundColor=Color.BEIGE.value)
    game_surface = game_manager.surface

    RCube = RubikCube(game_surface)
    game_manager.AddObjects([
        RCube,
    ])
    game_manager.run()


if __name__ == '__main__':
    main()
