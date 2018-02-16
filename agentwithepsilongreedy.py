import random


class AgentWithEpsilonGreedy:
    def __init__(self, agent, epsilon):
        self._epsilon = epsilon
        self._agent = agent

    def get_direction(self, state):
        if random.random() < self._epsilon:
            return random.randrange(4)
        else:
            return self._agent.get_direction(state)

    def update(self, from_state, action, to_state, reward):
        return self._agent.update(from_state, action, to_state, reward)