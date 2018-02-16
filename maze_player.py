""" Maze player """
import maze_gen
import json
import random

from inputmanager import InputManager
from mazegame import MazeGame
from qlearningcontroller import QLearningController


def main():
    input_manager = InputManager()
    maze = maze_gen.Maze(15, 15)
    controller = QLearningController()
    count = 0
    target = (random.randrange(15), random.randrange(15))
    while True:
        game = MazeGame(count, maze, target, controller, input_manager)
        game.run()
        print(len(game.get_record()["a"]))
        with open("{0}.txt".format(count), "w") as f:
            f.write(json.dumps(game.get_record()))

        count += 1


if __name__ == "__main__":
    main()
