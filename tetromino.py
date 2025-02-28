import random
from colors import Colors

class Tetromino:
    SHAPES = [
        [[1, 1, 1, 1]],  # I
        [[1, 1], [1, 1]],  # O
        [[1, 1, 1], [0, 1, 0]],  # T
        [[1, 1, 1], [1, 0, 0]],  # L
        [[1, 1, 1], [0, 0, 1]],  # J
        [[1, 1, 0], [0, 1, 1]],  # S
        [[0, 1, 1], [1, 1, 0]]   # Z
    ]
    
    COLORS = [
        Colors.CYAN,    # I
        Colors.YELLOW,  # O
        Colors.PURPLE,  # T
        Colors.ORANGE,  # L
        Colors.BLUE,    # J
        Colors.GREEN,   # S
        Colors.RED      # Z
    ]
    
    def __init__(self):
        self.shape_index = random.randint(0, len(self.SHAPES) - 1)
        self.shape = [row[:] for row in self.SHAPES[self.shape_index]]
        self.color = self.COLORS[self.shape_index]
        self.x = 3
        self.y = -len(self.shape)
    
    def rotate(self):
        self.shape = list(zip(*self.shape[::-1]))
    
    def rotate_back(self):
        self.shape = list(zip(*self.shape))[::-1] 