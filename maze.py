''' Simple 2D maze generation tool '''
import sys
import numpy as np

def create_maze(rows, cols):
    ''' Maze constructor '''
    maze = np.zeros([rows, cols], dtype=int)
    maze[0, 0] = 2
    maze[0, 1] = 8
    maze[1, 0] = 1 ^ 2
    maze[1, 1] = 8
    return maze

def draw_in_ascii(maze):
    ''' Draw maze in ASCII format '''
    write = sys.stdout.write
    for row in maze:
        for col in row:
            if col & 1:
                write('+ ')
            else:
                write('+-')
        write('+\n')
        for col in row:
            if col & 8:
                write('  ')
            else:
                write('| ')
        write('|\n')
    for _ in range(maze.shape[1]):
        write('+-')
    write('+\n')

def main():
    ''' Main function '''
    rows = int(sys.argv[1])
    cols = int(sys.argv[2])
    maze = create_maze(rows, cols)
    print(maze)
    draw_in_ascii(maze)

if __name__ == "__main__":
    main()
