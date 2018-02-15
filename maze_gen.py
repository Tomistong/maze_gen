"""Simple 2D maze generation tool """
import sys
import random
import numpy as np


def create_maze(rows, cols):
    """ Maze constructor """
    maze = np.zeros([rows, cols], dtype=int)
    _create_maze_recursively(maze, random.randrange(rows), random.randrange(cols))
    return maze


def _is_available(maze, current_row, current_cols):
    """ Check if the cell of the maze is available """
    if current_cols < 0:
        return False
    if current_row < 0:
        return False
    if current_cols >= maze.shape[1]:
        return False
    if current_row >= maze.shape[0]:
        return False
    if maze[current_row, current_cols] != 0:
        return False
    return True


def _create_maze_recursively(maze, current_row, current_cols):
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

        if _is_available(maze, next_row, next_col):
            maze[current_row, current_cols] |= 1 << direction
            maze[next_row, next_col] |= 1 << (direction+2)%4
            _create_maze_recursively(maze, next_row, next_col)


def main():
    """ Main function """
    rows = int(sys.argv[1])
    cols = int(sys.argv[2])
    maze = create_maze(rows, cols)
    print(maze)


if __name__ == "__main__":
    main()
