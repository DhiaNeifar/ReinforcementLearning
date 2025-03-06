from colors import Color
from config import HEIGHT, WIDTH
from game import GameManager
from cube import Cube


def main() -> None:
    game_caption = 'cube'

    game_manager = GameManager(game_caption, height=HEIGHT, width=WIDTH, BackgroundColor=Color.BEIGE.value)
    game_surface = game_manager.surface

    cube = Cube(game_surface)
    cube.draw()
    game_manager.AddObjects([cube])
    game_manager.run()


if __name__ == '__main__':
    main()
