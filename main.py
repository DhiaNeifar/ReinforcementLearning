from game import GameManager
from cube import Cube
from point import Point3d

def main():
    game_caption = 'cube'

    game_manager = GameManager(game_caption)
    game_surface = game_manager.surface


    center = Point3d(0, 0, 0)
    diameter = 1

    cube = Cube(center, diameter, game_surface)

    game_manager.AddObjects([cube])
    game_manager.run()


    pass


if __name__ == '__main__':
    main()
