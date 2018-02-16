import sys

import pygame

from mazegameenvironment import MazeGameEnvironment


class MazeGameGuiEnvironment:
    _WALL_WIDTH = 2
    _CELL_WIDTH = 36
    _PLAYER_COLOR = (0, 255, 0)
    _GOAL_COLOR = (255, 255, 255)
    _WALL_COLOR = (128, 128, 128)

    def __init__(self, maze, player_agent, target_agent, input_manager):
        pygame.init()
        pygame.display.set_caption('Maze Game')

        self.count = 0
        self.is_visible = True
        self._env = MazeGameEnvironment(maze, player_agent, target_agent)
        self._input_manager = input_manager
        self._font = pygame.font.SysFont("monospace", 24)
        self._screen =\
            pygame.display.set_mode(
                (maze.width * self._CELL_WIDTH + 2 * self._WALL_WIDTH,
                 maze.length * self._CELL_WIDTH + 2 * self._WALL_WIDTH))

        self._clock = pygame.time.Clock()

    def reset(self):
        self.count += 1
        self._env.reset()

    def step(self):
        self._input_manager.clear()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    self._input_manager.up = True
                elif event.key == pygame.K_DOWN:
                    self._input_manager.down = True
                elif event.key == pygame.K_LEFT:
                    self._input_manager.left = True
                elif event.key == pygame.K_RIGHT:
                    self._input_manager.right = True
                elif event.key == pygame.K_g:
                    self.is_visible = not self.is_visible

        done = self._env.step()

        if not self.is_visible:
            return done

        self._screen.fill((0, 0, 0))

        self._draw_maze()
        self._draw_goal()
        self._draw_player()
        self._draw_game_info()

        pygame.display.flip()

        return done

    def get_record(self):
        return self._env.get_record()

    def _draw_game_info(self):
        label = self._font.render("{0}: {1}".format(self.count, self._env.get_number_of_steps()), 1, (255, 255, 0))
        self._screen.blit(label, (10, 10))

    def _draw_goal(self):
        target = self._env.get_target()
        shift = 2 * self._WALL_WIDTH
        left = target[0] * self._CELL_WIDTH + self._WALL_WIDTH + 2 * shift
        top = target[1] * self._CELL_WIDTH + self._WALL_WIDTH + 2 * shift

        shrink_width = self._CELL_WIDTH - shift * 4

        pygame.draw.rect(
            self._screen,
            self._GOAL_COLOR,
            [left, top, shrink_width, shrink_width])

    def _draw_player(self):
        player = self._env.get_player()

        shift = 2 * self._WALL_WIDTH
        left = player[0] * self._CELL_WIDTH + self._WALL_WIDTH + 2 * shift
        top = player[1] * self._CELL_WIDTH + self._WALL_WIDTH + 2 * shift

        shrink_width = self._CELL_WIDTH - shift * 4

        pygame.draw.rect(
            self._screen,
            self._PLAYER_COLOR,
            [left, top, shrink_width, shrink_width])

    def _draw_maze(self):
        for row_index in range(self._env.get_maze_length()):
            for col_index in range(self._env.get_maze_width()):
                self._draw_cell(row_index, col_index)

    def _draw_cell(self, row_index, col_index):
        top = row_index * self._CELL_WIDTH + self._WALL_WIDTH
        left = col_index * self._CELL_WIDTH + self._WALL_WIDTH
        doubled_wall_width = 2 * self._WALL_WIDTH
        shrink_cell_width = self._CELL_WIDTH - doubled_wall_width

        state = self._env.get_state(row_index, col_index)

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
