import random


class TargetAgent:
    def __init__(self, maze):
        self._position = (random.randrange(maze.width), random.randrange(maze.length))

    def get_position(self):
        return self._position

    @staticmethod
    def get_direction():
        return random.randrange(4)

    def update(self, position):
        self._position = position

