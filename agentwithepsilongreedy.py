import random


class AgentWithEpsilonGreedy:
    def __init__(self, agent, epsilon):
        self._epsilon = epsilon
        self._agent = agent

    def get_action(self, state):
        if random.random() < self._epsilon:
            return random.randrange(4)
        else:
            return self._agent.get_action(state)

    def update(self, state_i, action, state_j, reward, is_done):
        return self._agent.update(state_i, action, state_j, reward, is_done)