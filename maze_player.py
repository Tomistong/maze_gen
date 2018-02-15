""" Maze player """
import sys
import pygame
import maze_gen


class MazePlayer:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class MazeGame:
    _WALL_WIDTH = 2
    _CELL_WIDTH = 36
    _PLAYER_COLOR = (0, 255, 0)
    _GOAL_COLOR = (255, 255, 255)
    _WALL_COLOR = (128, 128, 128)

    def __init__(self, width, length):
        pygame.init()
        pygame.display.set_caption('Maze Player')

        self._player = MazePlayer(0, length - 1)
        self._goal = (width-1, 0)
        self._maze = maze_gen.create_maze(length, width)
        self._screen =\
            pygame.display.set_mode(
                (width * self._CELL_WIDTH + 2 * self._WALL_WIDTH,
                 length * self._CELL_WIDTH + 2 * self._WALL_WIDTH))

        self._clock = pygame.time.Clock()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP \
                            and self._player.y > 0 \
                            and self._maze[self._player.y, self._player.x] & 1:
                        self._player.y -= 1
                    elif event.key == pygame.K_DOWN \
                            and self._player.y < self._maze.shape[0] \
                            and self._maze[self._player.y, self._player.x] & 4:
                        self._player.y += 1
                    elif event.key == pygame.K_LEFT \
                            and self._player.x > 0 \
                            and self._maze[self._player.y, self._player.x] & 8:
                        self._player.x -= 1
                    elif event.key == pygame.K_RIGHT \
                            and self._player.x < self._maze.shape[1] \
                            and self._maze[self._player.y, self._player.x] & 2:
                        self._player.x += 1

            self._screen.fill((0, 0, 0))

            self._draw_maze()
            self._draw_goal()
            self._draw_player()

            pygame.display.flip()

            if self._player.x == self._goal[0] and self._player.y == self._goal[1]:
                break

            self._clock.tick(30)

        while True:
            self._clock.tick(30)

    def _draw_goal(self):
        shift = 2 * self._WALL_WIDTH
        left = self._goal[0] * self._CELL_WIDTH + self._WALL_WIDTH + 2 * shift
        top = self._goal[1] * self._CELL_WIDTH + self._WALL_WIDTH + 2 * shift

        shrink_width = self._CELL_WIDTH - shift * 4

        pygame.draw.rect(
            self._screen,
            self._GOAL_COLOR,
            [left, top, shrink_width, shrink_width])

    def _draw_player(self):
        shift = 2 * self._WALL_WIDTH
        left = self._player.x * self._CELL_WIDTH + self._WALL_WIDTH + 2 * shift
        top = self._player.y * self._CELL_WIDTH + self._WALL_WIDTH + 2 * shift

        shrink_width = self._CELL_WIDTH - shift * 4

        pygame.draw.rect(
            self._screen,
            self._PLAYER_COLOR,
            [left, top, shrink_width, shrink_width])

    def _draw_maze(self):
        for row_index in range(self._maze.shape[0]):
            for col_index in range(self._maze.shape[1]):
                self._draw_cell(row_index, col_index)

    def _draw_cell(self, row_index, col_index):
        top = row_index * self._CELL_WIDTH + self._WALL_WIDTH
        left = col_index * self._CELL_WIDTH + self._WALL_WIDTH
        doubled_wall_width = 2 * self._WALL_WIDTH
        shrink_cell_width = self._CELL_WIDTH - doubled_wall_width

        state = self._maze[row_index, col_index]

        if state & 1 == 0:
            self._draw_wall(
                [left + self._WALL_WIDTH,
                 top,
                 shrink_cell_width,
                 self._WALL_WIDTH])

        if state & 2 == 0:
            self._draw_wall(
                [left + self._CELL_WIDTH - self._WALL_WIDTH,
                 top + self._WALL_WIDTH,
                 self._WALL_WIDTH,
                 shrink_cell_width])

        if state & 4 == 0:
            self._draw_wall(
                [left + self._WALL_WIDTH,
                 top + self._CELL_WIDTH - self._WALL_WIDTH,
                 shrink_cell_width,
                 self._WALL_WIDTH])

        if state & 8 == 0:
            self._draw_wall(
                [left,
                 top + self._WALL_WIDTH,
                 self._WALL_WIDTH,
                 shrink_cell_width])

    def _draw_wall(self, rect):
        pygame.draw.rect(self._screen, self._WALL_COLOR, rect)


def main():
    player = MazeGame(20, 15)
    player.run()


if __name__ == "__main__":
    main()
