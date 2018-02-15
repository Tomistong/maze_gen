""" Convert a maze to a string in ASCII format """
import sys
import maze_gen


def convert_to_ascii(maze):
    """ Convert a maze to a string in ASCII format """
    output = ''
    for row in maze:
        for col in row:
            if col & 1:
                output += '+ '
            else:
                output += '+-'
        output += '+\n'
        for col in row:
            if col & 8:
                output += '  '
            else:
                output += '| '
        output += '|\n'
    for _ in range(maze.shape[1]):
        output += '+-'
    output += '+\n'
    return output


def main():
    """ Main function """
    rows = int(sys.argv[1])
    cols = int(sys.argv[2])
    maze = maze_gen.create_maze(rows, cols)
    print(convert_to_ascii(maze))


if __name__ == "__main__":
    main()
