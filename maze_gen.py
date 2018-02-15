"""Simple 2D maze generation tool """
import random
import numpy as np


class Maze:
    def __init__(self, width, length):
        """ Maze constructor """
        self.width = width
        self.length = length
        self.grid = np.zeros([length, width], dtype=int)
        self._create_maze_recursively(random.randrange(length), random.randrange(width))

    def _is_available(self, current_row, current_cols):
        """ Check if the cell of the maze is available """
        if current_cols < 0:
            return False
        if current_row < 0:
            return False
        if current_cols >= self.grid.shape[1]:
            return False
        if current_row >= self.grid.shape[0]:
            return False
        if self.grid[current_row, current_cols] != 0:
            return False
        return True

    def _create_maze_recursively(self, current_row, current_cols):
        """ Recursively create the maze """
        directions = list(range(4))
        random.shuffle(directions)

        for direction in directions:
            if direction == 0:
                next_row = current_row-1
                next_col = current_cols
            elif direction == 1:
                next_row = current_row
                next_col = current_cols+1
            elif direction == 2:
                next_row = current_row+1
                next_col = current_cols
            elif direction == 3:
                next_row = current_row
                next_col = current_cols-1

            if self._is_available(next_row, next_col):
                self.grid[current_row, current_cols] |= 1 << direction
                self.grid[next_row, next_col] |= 1 << (direction+2) % 4
                self._create_maze_recursively(next_row, next_col)


def main():
    """ Main function """
    maze = Maze(5, 5)
    print(maze)


if __name__ == "__main__":
    main()
