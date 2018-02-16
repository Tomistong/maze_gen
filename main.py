""" Maze player """
import maze_gen
import json

from inputmanager import InputManager
from mazegameguienvironment import MazeGameGuiEnvironment
from qlearningagent import QLearningAgent


class StaticAgent:
    def __init__(self):
        pass

    def get_action(self, state):
        return 4

    def update(self, state_i, action, state_j, reward):
        pass

    def reset(self):
        pass


class WaitAndRunAgent:
    def __init__(self, threshold, agent):
        self._agent = agent
        self._threshold = threshold
        self._count = 0

    def get_action(self, state):
        if self._count < self._threshold:
            return 4
        else:
            return self._agent.get_action(state)

    def update(self, state_i, action, state_j, reward):
        if self._count < self._threshold:
            pass
        else:
            return self._agent.update(state_i, action, state_j, reward)

    def reset(self):
        self._count += 1


def main():
    maze = maze_gen.Maze(10, 10)
    input_manager = InputManager()

    player_agent =\
        QLearningAgent(
            initial_q=0.1,
            learning_rate=0.9,
            discount_factor=0.9)

    target_agent =\
        QLearningAgent(
            initial_q=0,
            learning_rate=0.9,
            discount_factor=0.9)

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
