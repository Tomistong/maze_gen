import random


class TargetAgent:
    def __init__(self, maze):
        self._position = None
        self._maze_width = maze.width
        self._maze_length = maze.length
        self.reset()

    def reset(self):
        self._position = (random.randrange(self._maze_width), random.randrange(self._maze_length))

    def get_position(self):
        return self._position

    @staticmethod
    def get_direction():
        return random.randrange(4)

    def update(self, position):
        self._position = position

