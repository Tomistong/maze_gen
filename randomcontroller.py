import random


class RandomController:
    @staticmethod
    def get_direction():
        return random.randrange(4)