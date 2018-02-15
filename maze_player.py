""" Maze player """
import sys
import pygame
import maze_gen


class MazePlayer:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Maze Player')

        self._screen = pygame.display.set_mode((640, 640))
        self._clock = pygame.time.Clock()
        self._maze = maze_gen.create_maze(15, 15)

    def run(self):
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            self._screen.fill((0, 0, 0))

            self._draw_maze()

            pygame.display.flip()

            self._clock.tick(30)

    def _draw_maze(self):
        for row_index in range(self._maze.shape[0]):
            for col_index in range(self._maze.shape[1]):
                self._draw_cell(row_index, col_index)

    def _draw_cell(self, row_index, col_index):
        wall_width = 2
        cell_width = 36

        top = row_index * cell_width + wall_width
        left = col_index * cell_width + wall_width
        doubled_wall_width = 2 * wall_width
        shrink_cell_width = cell_width - doubled_wall_width

        state = self._maze[row_index, col_index]

        if state & 1 == 0:
            self._draw_wall(
                [left + wall_width, top, shrink_cell_width, wall_width])

        if state & 2 == 0:
            self._draw_wall(
                [left + cell_width - wall_width, top + wall_width, wall_width, shrink_cell_width])

        if state & 4 == 0:
            self._draw_wall(
                [left + wall_width, top + cell_width - wall_width, shrink_cell_width, wall_width])

        if state & 8 == 0:
            self._draw_wall(
                [left, top + wall_width, wall_width, shrink_cell_width])

    def _draw_wall(self, rect):
        wall_color = (128, 128, 128)
        pygame.draw.rect(self._screen, wall_color, rect)


def main():
    player = MazePlayer()
    player.run()


if __name__ == "__main__":
    main()
