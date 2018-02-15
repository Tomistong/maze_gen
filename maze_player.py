""" Maze player """
import sys
import pygame
import maze_gen


def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 640))
    pygame.display.set_caption('Maze Player')

    clock = pygame.time.Clock()

    maze = maze_gen.create_maze(15, 15)
    print(maze)

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.fill((0, 0, 0))

        _draw_maze(screen, maze)

        pygame.display.flip()
        clock.tick(30)


def _draw_maze(screen, maze):
    for row_index in range(maze.shape[0]):
        for col_index in range(maze.shape[1]):
            _draw_cell(screen, maze, row_index, col_index)


def _draw_cell(screen, maze, row_index, col_index):
    wall_width = 2
    cell_width = 36

    top = row_index * cell_width + wall_width
    left = col_index * cell_width + wall_width
    doubled_wall_width = 2 * wall_width
    shrink_cell_width = cell_width - doubled_wall_width

    state = maze[row_index, col_index]

    if state & 1 == 0:
        _draw_wall(screen, [left + wall_width, top, shrink_cell_width, wall_width])

    if state & 2 == 0:
        _draw_wall(screen, [left + cell_width - wall_width, top + wall_width, wall_width, shrink_cell_width])

    if state & 4 == 0:
        _draw_wall(screen, [left + wall_width, top + cell_width - wall_width, shrink_cell_width, wall_width])

    if state & 8 == 0:
        _draw_wall(screen, [left, top + wall_width, wall_width, shrink_cell_width])


def _draw_wall(screen, rect):
    wall_color = (128, 128, 128)
    pygame.draw.rect(screen, wall_color, rect)


if __name__ == "__main__":
    main()
