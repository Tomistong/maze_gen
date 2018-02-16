""" Maze player """
from pympler.tracker import SummaryTracker

import maze_gen
import json

from inputmanager import InputManager
from mazegameguienvironment import MazeGameGuiEnvironment
from qlearningagent import QLearningAgent
from targetagent import TargetAgent


def main():
    maze = maze_gen.Maze(15, 15)
    input_manager = InputManager()

    player_agent =\
        QLearningAgent(
            initial_q=0.1,
            learning_rate=0.9,
            discount_factor=0.9)

    target_agent = TargetAgent(maze)

    env = \
        MazeGameGuiEnvironment(
            maze,
            player_agent,
            target_agent,
            input_manager)

    while True:
        done = env.step()
        while not done:
            done = env.step()

        print(len(env.get_record()["a"]))

        with open("log/{0}.txt".format(env.count), "w") as f:
            f.write(json.dumps(env.get_record()))

        env.reset()


if __name__ == "__main__":
    main()
