""" Maze player """
import sys
import pygame
import maze_gen
import json
import random


class InputManager:
    def __init__(self):
        self.up = False
        self.down = False
        self.left = False
        self.right = False

    def clear(self):
        self.up = False
        self.down = False
        self.left = False
        self.right = False


class QLearningController:
    _INITIAL_Q = 0.5
    _LEARNING_RATE = 0.5
    _GAMMA = 0.9

    def __init__(self):
        self.q = {}

    def get_direction(self, state):
        best_q = None
        action = None
        directions = list(range(4))
        random.shuffle(directions)
        for direction in directions:
            state_action = (state, direction)
            if state_action not in self.q:
                self.q[state_action] = self._INITIAL_Q
            if best_q is None or self.q[state_action] > best_q:
                best_q = self.q[state_action]
                action = direction

        print(best_q)
        print(action)
        return action

    def update(self, from_state, action, to_state, reward):
        from_state_action = (from_state, action)
        if reward != 0:
            self.q[from_state_action] =\
                (1.-self._LEARNING_RATE) * self.q[from_state_action] +\
                self._LEARNING_RATE * reward
            print(self.q[from_state_action])
        else:
            best_q = None

            for direction in range(4):
                to_state_action = (to_state, direction)
                if to_state_action not in self.q:
                    self.q[to_state_action] = self._INITIAL_Q
                if best_q is None or self.q[to_state_action] > best_q:
                    best_q = self.q[to_state_action]

            self.q[from_state_action] = \
                (1.-self._LEARNING_RATE) * self.q[from_state_action] + \
                self._LEARNING_RATE * self._GAMMA * best_q


class KeyboardController:
    def __init__(self, input_manager):
        self._input_manager = input_manager

    def get_direction(self):
        if self._input_manager.up:
            return 0
        if self._input_manager.right:
            return 1
        if self._input_manager.down:
            return 2
        if self._input_manager.left:
            return 3


class RandomController:
    @staticmethod
    def get_direction():
        return random.randrange(4)


class MazeGameEngine:
    def __init__(self, maze):
        self.player = MazePlayer(0, maze.length - 1)
        self.goal = (maze.width-1, 0)
        self.maze = maze
        self.record = {"o": [(self.player.x, self.player.y)], "a": []}

    def get_number_of_steps(self):
        return len(self.record["a"])

    def get_observation(self):
        return self.player.x, self.player.y

    def move_up(self):
        if self.player.y > 0 and self.maze.grid[self.player.y, self.player.x] & 1:
            self.player.y -= 1
        self.record["o"].append((self.player.x, self.player.y))
        self.record["a"] += [0]

    def move_down(self):
        if self.player.y < self.maze.length and self.maze.grid[self.player.y, self.player.x] & 4:
            self.player.y += 1
        self.record["o"].append((self.player.x, self.player.y))
        self.record["a"] += [2]

    def move_left(self):
        if self.player.x > 0 and self.maze.grid[self.player.y, self.player.x] & 8:
            self.player.x -= 1
        self.record["o"].append((self.player.x, self.player.y))
        self.record["a"] += [3]

    def move_right(self):
        if self.player.x < self.maze.width and self.maze.grid[self.player.y, self.player.x] & 2:
            self.player.x += 1
        self.record["o"].append((self.player.x, self.player.y))
        self.record["a"] += [1]

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

    def __init__(self, maze, controller, input_manager):
        pygame.init()
        pygame.display.set_caption('Maze Game')

        self._input_manager = input_manager
        self._controller = controller
        self._engine = MazeGameEngine(maze)
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

            from_state = self._engine.get_observation()

            direction =\
                self._controller.get_direction(from_state)

            if direction == 0:
                self._engine.move_up()
            elif direction == 1:
                self._engine.move_right()
            elif direction == 2:
                self._engine.move_down()
            elif direction == 3:
                self._engine.move_left()

#            reward = 0 if not self._engine.is_finished() else -len(self._engine.record["a"])
            reward = 0 if not self._engine.is_finished() else 1

            self._controller.update(
                from_state,
                direction,
                self._engine.get_observation(),
                reward)

            self._screen.fill((0, 0, 0))

            self._draw_maze()
            self._draw_goal()
            self._draw_player()
            self._draw_game_info()

            pygame.display.flip()

#            self._clock.tick(60)

            if self._engine.is_finished():
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
        label = self._font.render(str(self._engine.get_number_of_steps()), 1, (255, 255, 0))
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


def main():
    input_manager = InputManager()
    maze = maze_gen.Maze(15, 15)
    controller = QLearningController()
    count = 0
    while True:
        game = MazeGame(maze, controller, input_manager)
        game.run()
        print(len(game.get_record()["a"]))
        with open("{0}.txt".format(count), "w") as f:
            f.write(json.dumps(game.get_record()))

        count += 1


if __name__ == "__main__":
    main()
