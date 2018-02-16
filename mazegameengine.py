from mazeplayer import MazePlayer


class MazeGameEngine:
    def __init__(self, maze):
        self.player = MazePlayer(0, maze.length - 1)
        self.target = None
        self.maze = maze
        self.record = {"o": [(self.player.x, self.player.y)], "a": []}

    def get_number_of_steps(self):
        return len(self.record["a"])

    def get_observation(self):
        return self.player.x, self.player.y, self.target[0], self.target[1]

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
        return self.player.x == self.target[0] and self.player.y == self.target[1]