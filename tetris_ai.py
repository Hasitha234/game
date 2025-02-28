import numpy as np
from collections import defaultdict
import random

class TetrisAI:
    def __init__(self, learning_rate=0.1, discount_factor=0.95, epsilon=1.0, epsilon_decay=0.995):
        self.q_table = defaultdict(lambda: defaultdict(float))
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.possible_actions = ['left', 'right', 'rotate', 'down']

    def get_state_features(self, game):
        # Extract relevant features from the game state
        heights = self._get_column_heights(game)
        holes = self._count_holes(game)
        bumpiness = self._get_bumpiness(heights)
        complete_lines = self._count_complete_lines(game)
        
        return (
            tuple(heights),
            holes,
            bumpiness,
            complete_lines
        )

    def _get_column_heights(self, game):
        heights = [0] * game.GRID_WIDTH
        for x in range(game.GRID_WIDTH):
            for y in range(game.GRID_HEIGHT):
                if game.game_grid[y][x]:
                    heights[x] = game.GRID_HEIGHT - y
                    break
        return heights

    def _count_holes(self, game):
        holes = 0
        for x in range(game.GRID_WIDTH):
            found_block = False
            for y in range(game.GRID_HEIGHT):
                if game.game_grid[y][x]:
                    found_block = True
                elif found_block and not game.game_grid[y][x]:
                    holes += 1
        return holes

    def _get_bumpiness(self, heights):
        bumpiness = 0
        for i in range(len(heights) - 1):
            bumpiness += abs(heights[i] - heights[i + 1])
        return bumpiness

    def _count_complete_lines(self, game):
        complete_lines = 0
        for y in range(game.GRID_HEIGHT):
            if all(game.game_grid[y]):
                complete_lines += 1
        return complete_lines

    def choose_action(self, state):
        if random.random() < self.epsilon:
            return random.choice(self.possible_actions)
        
        state_actions = self.q_table[state]
        return max(self.possible_actions, key=lambda a: state_actions[a])

    def update(self, state, action, reward, next_state):
        best_next_value = max(self.q_table[next_state].values(), default=0)
        current_value = self.q_table[state][action]
        
        # Q-learning update formula
        self.q_table[state][action] = current_value + self.learning_rate * (
            reward + self.discount_factor * best_next_value - current_value
        )
        
        # Decay epsilon
        self.epsilon *= self.epsilon_decay

    def get_reward(self, game, lines_cleared, game_over):
        reward = 0
        
        if game_over:
            reward -= 100
        else:
            # Reward for clearing lines
            if lines_cleared > 0:
                reward += lines_cleared * lines_cleared * 10
            
            # Penalize for holes and bumpiness
            holes = self._count_holes(game)
            heights = self._get_column_heights(game)
            bumpiness = self._get_bumpiness(heights)
            
            reward -= holes * 2
            reward -= bumpiness * 0.5
            
        return reward 