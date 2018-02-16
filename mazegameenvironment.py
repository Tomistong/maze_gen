import sys

import pygame

from mazegameengine import MazeGameEngine


class MazeGameEnvironment:
    _WALL_WIDTH = 2
    _CELL_WIDTH = 36
    _PLAYER_COLOR = (0, 255, 0)
    _GOAL_COLOR = (255, 255, 255)
    _WALL_COLOR = (128, 128, 128)

    def __init__(self, count, maze, player_agent, target_agent, input_manager):
        pygame.init()
        pygame.display.set_caption('Maze Game')

        self._count = count
        self._input_manager = input_manager
        self._player_agent = player_agent
        self._target_agent = target_agent
        self._engine = MazeGameEngine(maze, target_agent.get_position())
        self._font = pygame.font.SysFont("monospace", 24)
        self._screen =\
            pygame.display.set_mode(
                (maze.width * self._CELL_WIDTH + 2 * self._WALL_WIDTH,
                 maze.length * self._CELL_WIDTH + 2 * self._WALL_WIDTH))

        self._clock = pygame.time.Clock()

    def run(self):
        while True:
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

            target_moving_direction =\
                self._target_agent.get_direction()

            self._engine.move_target(target_moving_direction)

            self._target_agent.update(self._engine.target)

            from_state = self._engine.get_observation()

            player_moving_direction =\
                self._player_agent.get_direction(from_state)

            done = self._engine.move_player(player_moving_direction)

            reward = 0 if not done else 1

            self._player_agent.update(
                from_state,
                player_moving_direction,
                self._engine.get_observation(),
                reward)

            self._screen.fill((0, 0, 0))

            self._draw_maze()
            self._draw_goal()
            self._draw_player()
            self._draw_game_info()

            pygame.display.flip()

#            self._clock.tick(60)

            if done:
                break

#        is_paused = True
#        while is_paused:
#            for event in pygame.event.get():
#                if event.type == pygame.QUIT:
#                    sys.exit()
#                if event.type == pygame.KEYUP:
#                    if event.key == pygame.K_SPACE:
#                        is_paused = False
#            self._clock.tick(30)

    def get_record(self):
        return self._engine.record

    def _draw_game_info(self):
        label = self._font.render("{0}: {1}".format(self._count, self._engine.get_number_of_steps()), 1, (255, 255, 0))
        self._screen.blit(label, (10, 10))

    def _draw_goal(self):
        shift = 2 * self._WALL_WIDTH
        left = self._engine.target[0] * self._CELL_WIDTH + self._WALL_WIDTH + 2 * shift
        top = self._engine.target[1] * self._CELL_WIDTH + self._WALL_WIDTH + 2 * shift

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
        for row_index in range(self._engine.maze.length):
            for col_index in range(self._engine.maze.width):
                self._draw_cell(row_index, col_index)

    def _draw_cell(self, row_index, col_index):
        top = row_index * self._CELL_WIDTH + self._WALL_WIDTH
        left = col_index * self._CELL_WIDTH + self._WALL_WIDTH
        doubled_wall_width = 2 * self._WALL_WIDTH
        shrink_cell_width = self._CELL_WIDTH - doubled_wall_width

        state = self._engine.maze.grid[row_index, col_index]

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
