""" Maze player """
import sys
import pygame
import maze_gen


class MazePlayer:
    WALL_WIDTH = 2
    CELL_WIDTH = 36

    def __init__(self, width, length):
        pygame.init()
        pygame.display.set_caption('Maze Player')

        self._maze = maze_gen.create_maze(length, width)
        self._screen =\
            pygame.display.set_mode(
                (width * self.CELL_WIDTH + 2 * self.WALL_WIDTH,
                 length* self.CELL_WIDTH + 2 * self.WALL_WIDTH))

        self._clock = pygame.time.Clock()

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
        top = row_index * self.CELL_WIDTH + self.WALL_WIDTH
        left = col_index * self.CELL_WIDTH + self.WALL_WIDTH
        doubled_wall_width = 2 * self.WALL_WIDTH
        shrink_cell_width = self.CELL_WIDTH - doubled_wall_width

        state = self._maze[row_index, col_index]

        if state & 1 == 0:
            self._draw_wall(
                [left + self.WALL_WIDTH,
                 top,
                 shrink_cell_width,
                 self.WALL_WIDTH])

        if state & 2 == 0:
            self._draw_wall(
                [left + self.CELL_WIDTH - self.WALL_WIDTH,
                 top + self.WALL_WIDTH,
                 self.WALL_WIDTH,
                 shrink_cell_width])

        if state & 4 == 0:
            self._draw_wall(
                [left + self.WALL_WIDTH,
                 top + self.CELL_WIDTH - self.WALL_WIDTH,
                 shrink_cell_width,
                 self.WALL_WIDTH])

        if state & 8 == 0:
            self._draw_wall(
                [left,
                 top + self.WALL_WIDTH,
                 self.WALL_WIDTH,
                 shrink_cell_width])

    def _draw_wall(self, rect):
        wall_color = (128, 128, 128)
        pygame.draw.rect(self._screen, wall_color, rect)


def main():
    player = MazePlayer(20, 15)
    player.run()


if __name__ == "__main__":
    main()
