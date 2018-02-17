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

    def update(self, state_i, action, state_j, reward, is_done):
        if self._count < self._threshold:
            pass
        else:
            return self._agent.update(state_i, action, state_j, reward, is_done)

    def reset(self):
        self._count += 1