""" Maze player """
import maze_gen
import numpy as np

from inputmanager import InputManager
from mazegameguienvironment import MazeGameGuiEnvironment
from qlearningagent import QLearningAgent


def main():
    maze = maze_gen.Maze(5, 5)
    input_manager = InputManager()

    player_agent =\
        QLearningAgent(
            initial_q=0.1,
            learning_rate=0.9,
            discount_factor=0.9)

#    target_agent =\
#        WaitAndRunAgent(
#            100000,
#            QLearningAgent(
#                initial_q=0,
#                learning_rate=0.9,
#                discount_factor=0.9))

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

    count = 0
    while count < 10000:
        env.reset()

        done = env.step()
        while not done:
            done = env.step()

        print(len(env.get_record()["a"]))

        count += 1

    np.save("q_state_action", np.array((list(k[0] + (k[1], ) for k in player_agent.q))))
    np.save("q_target_value", np.array((list((v,) for k, v in player_agent.q.items()))))

#        with open("log/{0}.txt".format(env.count), "w") as f:
#            f.write(json.dumps(env.get_record()))


if __name__ == "__main__":
    main()
