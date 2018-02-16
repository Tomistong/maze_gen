""" Maze player """
import maze_gen
import json

from inputmanager import InputManager
from mazegameenvironment import MazeGameEnvironment
from qlearningagent import QLearningAgent
from targetagent import TargetAgent


def main():
    input_manager = InputManager()
    maze = maze_gen.Maze(10, 10)

    player_agent =\
        QLearningAgent(
            initial_q=0.1,
            learning_rate=0.9,
            discount_factor=0.9)

    count = 0
    while True:
        target_agent = TargetAgent(maze)

        game =\
            MazeGameEnvironment(
                count,
                maze,
                player_agent,
                target_agent,
                input_manager)
        game.run()
        print(len(game.get_record()["a"]))

        with open("log/{0}.txt".format(count), "w") as f:
            f.write(json.dumps(game.get_record()))

        count += 1


if __name__ == "__main__":
    main()
