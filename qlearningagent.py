import random


class QLearningAgent:
    def __init__(self, initial_q, learning_rate, discount_factor):
        self._INITIAL_Q = initial_q
        self._LEARNING_RATE = learning_rate
        self._DISCOUNT_FACTOR = discount_factor
        self.q = {}

    def reset(self):
        pass

    def get_action(self, state):
        best_q = None
        action = None
        directions = list(range(4))
        random.shuffle(directions)
        for direction in directions:
            state_action = (state, direction)
            if state_action not in self.q:
                self.q[state_action] = self._INITIAL_Q
            if best_q is None or self.q[state_action] > best_q:
                best_q = self.q[state_action]
                action = direction

        return action

    def update(self, state_i, action, state_j, reward, is_done):
        state_action_i = (state_i, action)
        if is_done:
            self.q[state_action_i] = \
                (1. - self._LEARNING_RATE) * self.q[state_action_i] + \
                self._LEARNING_RATE * reward
            print(self.q[state_action_i])
        else:
            best_q = None

            for direction in range(4):
                state_action_j = (state_j, direction)
                if state_action_j not in self.q:
                    self.q[state_action_j] = self._INITIAL_Q
                if best_q is None or self.q[state_action_j] > best_q:
                    best_q = self.q[state_action_j]

            if state_action_i not in self.q:
                self.q[state_action_i] = self._INITIAL_Q

            self.q[state_action_i] = \
                (1. - self._LEARNING_RATE) * self.q[state_action_i] + \
                self._LEARNING_RATE * (reward + self._DISCOUNT_FACTOR * best_q)

#            print("{0}: {1}, {2}, {3}, {4}".format(state_action_i, state_j, self.q[state_action_i], best_q, reward))
