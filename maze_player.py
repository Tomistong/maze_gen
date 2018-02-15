""" Maze player """
import sys
import pygame
import maze_gen


class MazeGameEngine:
    def __init__(self, width, length):
        self.steps = 0
        self.player = MazePlayer(0, length - 1)
        self.goal = (width-1, 0)
        self.maze = maze_gen.create_maze(length, width)

    def move_up(self):
        if self.player.y > 0 and self.maze[self.player.y, self.player.x] & 1:
            self.player.y -= 1
            self.steps += 1

    def move_down(self):
        if self.player.y < self.maze.shape[0] and self.maze[self.player.y, self.player.x] & 4:
            self.player.y += 1
            self.steps += 1

    def move_left(self):
        if self.player.x > 0 and self.maze[self.player.y, self.player.x] & 8:
            self.player.x -= 1
            self.steps += 1

    def move_right(self):
        if self.player.x < self.maze.shape[1] and self.maze[self.player.y, self.player.x] & 2:
            self.player.x += 1
            self.steps += 1

    def is_finished(self):
        return self.player.x == self.goal[0] and self.player.y == self.goal[1]


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

        self._engine = MazeGameEngine(width, length)
        self._font = pygame.font.SysFont("monospace", 24)
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
                    if event.key == pygame.K_UP:
                        self._engine.move_up()
                    elif event.key == pygame.K_DOWN:
                        self._engine.move_down()
                    elif event.key == pygame.K_LEFT:
                        self._engine.move_left()
                    elif event.key == pygame.K_RIGHT:
                        self._engine.move_right()

            self._screen.fill((0, 0, 0))

            self._draw_maze()
            self._draw_goal()
            self._draw_player()
            self._draw_game_info()

            pygame.display.flip()

            self._clock.tick(30)

            if self._engine.is_finished():
                break

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            self._clock.tick(30)

    def _draw_game_info(self):
        label = self._font.render(str(self._engine.steps), 1, (255, 255, 0))
        self._screen.blit(label, (10, 10))

    def _draw_goal(self):
        shift = 2 * self._WALL_WIDTH
        left = self._engine.goal[0] * self._CELL_WIDTH + self._WALL_WIDTH + 2 * shift
        top = self._engine.goal[1] * self._CELL_WIDTH + self._WALL_WIDTH + 2 * shift

        shrink_width = self._CELL_WIDTH - shift * 4

        pygame.draw.rect(
            self._screen,
            self._GOAL_COLOR,
            [left, top, shrink_width, shrink_width])

    def _draw_player(self):
        shift = 2 * self._WALL_WIDTH
        left = self._engine.player.x * self._CELL_WIDTH + self._WALL_WIDTH + 2 * shift
        top = self._engine.player.y * self._CELL_WIDTH + self._WALL_WIDTH + 2 * shift

        shrink_width = self._CELL_WIDTH - shift * 4

        pygame.draw.rect(
            self._screen,
            self._PLAYER_COLOR,
            [left, top, shrink_width, shrink_width])

    def _draw_maze(self):
        for row_index in range(self._engine.maze.shape[0]):
            for col_index in range(self._engine.maze.shape[1]):
                self._draw_cell(row_index, col_index)

    def _draw_cell(self, row_index, col_index):
        top = row_index * self._CELL_WIDTH + self._WALL_WIDTH
        left = col_index * self._CELL_WIDTH + self._WALL_WIDTH
        doubled_wall_width = 2 * self._WALL_WIDTH
        shrink_cell_width = self._CELL_WIDTH - doubled_wall_width

        state = self._engine.maze[row_index, col_index]

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
