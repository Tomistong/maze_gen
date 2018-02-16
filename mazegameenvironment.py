from mazegameengine import MazeGameEngine


class MazeGameEnvironment:
    def __init__(self, maze, player_agent, target_agent):
        self._player_agent = player_agent
        self._target_agent = target_agent
        self._maze = maze
        self._engine = MazeGameEngine(maze)

    def reset(self):
        self._target_agent.reset()
        self._engine = MazeGameEngine(self._maze)

    def get_state(self, row_index, col_index):
        return self._engine.maze.grid[row_index, col_index]

    def get_player(self):
        return self._engine.player.x, self._engine.player.y

    def get_record(self):
        return self._engine.record

    def get_number_of_steps(self):
        return self._engine.get_number_of_steps()

    def get_target(self):
        return self._engine.target

    def get_maze_length(self):
        return self._engine.maze.length

    def get_maze_width(self):
        return self._engine.maze.width

    def step(self):
        state_i = self._engine.get_observation()

        target_moving_direction = self._target_agent.get_action(state_i)

        self._engine.move_target(target_moving_direction)

        state_j = self._engine.get_observation()

        player_moving_direction = self._player_agent.get_action(state_j)

        done = self._engine.move_player(player_moving_direction)

        state_k = self._engine.get_observation()

        reward = 0 if not done else 1

        self._player_agent.update(
            state_j,
            player_moving_direction,
            state_k,
            reward)

        self._target_agent.update(
            state_i,
            target_moving_direction,
            state_j,
            -reward)

        return done
