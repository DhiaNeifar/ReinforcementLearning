from colors import Color
from config import HEIGHT, WIDTH, FPS
from game import GameManager
from rubikcube import RubikCube


def main() -> None:
    game_caption = 'cube'

    game_manager = GameManager(game_caption, height=HEIGHT, width=WIDTH, fps=FPS, BackgroundColor=Color.BEIGE.value)
    game_surface = game_manager.surface

    RCube = RubikCube(game_surface)
    # cube.draw()
    game_manager.AddObjects([
        RCube
    ])
    game_manager.run()


if __name__ == '__main__':
    main()
