import random


class TargetAgent:
    def __init__(self, maze):
        self.position = (random.randrange(maze.width), random.randrange(maze.length))

    def get_position(self):
        return self.position