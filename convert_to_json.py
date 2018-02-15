''' Convert a maze to a string in JSON format '''
import sys
import json
import maze_gen

def convert_to_json(maze):
    ''' Convert a maze to a string in JSON format '''
    return json.dumps(maze.tolist())

def main():
    ''' Main function '''
    rows = int(sys.argv[1])
    cols = int(sys.argv[2])
    maze = maze_gen.create_maze(rows, cols)
    print(convert_to_json(maze))

if __name__ == "__main__":
    main()
