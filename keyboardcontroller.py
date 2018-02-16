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