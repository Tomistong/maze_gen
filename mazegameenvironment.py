from mazegameengine import MazeGameEngine


class MazeGameEnvironment:
    def __init__(self, maze, player_agent, target_agent):
        self._player_agent = player_agent
        self._target_agent = target_agent
        self._maze = maze
        self._engine = MazeGameEngine(maze, target_agent.get_position())

    def reset(self):
        self._target_agent.reset()
        self._engine = MazeGameEngine(self._maze, self._target_agent.get_position())

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
        target_moving_direction = \
            self._target_agent.get_direction()

        self._engine.move_target(target_moving_direction)

        self._target_agent.update(self._engine.target)

        from_state = self._engine.get_observation()

        player_moving_direction = \
            self._player_agent.get_direction(from_state)

        done = self._engine.move_player(player_moving_direction)

        reward = 0 if not done else 1

        self._player_agent.update(
            from_state,
            player_moving_direction,
            self._engine.get_observation(),
            reward)

        return done