import random


class QLearningAgent:
    def __init__(self, initial_q, learning_rate, discount_factor):
        self._INITIAL_Q = initial_q
        self._LEARNING_RATE = learning_rate
        self._DISCOUNT_FACTOR = discount_factor
        self.q = {}

    def get_direction(self, state):
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

    def update(self, from_state, action, to_state, reward):
        from_state_action = (from_state, action)
        if reward != 0:
            self.q[from_state_action] = \
                (1. - self._LEARNING_RATE) * self.q[from_state_action] + \
                self._LEARNING_RATE * reward
            print(self.q[from_state_action])
        else:
            best_q = None

            for direction in range(4):
                to_state_action = (to_state, direction)
                if to_state_action not in self.q:
                    self.q[to_state_action] = self._INITIAL_Q
                if best_q is None or self.q[to_state_action] > best_q:
                    best_q = self.q[to_state_action]

            if from_state_action not in self.q:
                self.q[from_state_action] = self._INITIAL_Q

            self.q[from_state_action] = \
                (1. - self._LEARNING_RATE) * self.q[from_state_action] + \
                self._LEARNING_RATE * self._DISCOUNT_FACTOR * best_q
