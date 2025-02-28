import pygame
import random
from tetromino import Tetromino
from colors import Colors

class Tetris:
    def __init__(self):
        pygame.init()
        self.BLOCK_SIZE = 30
        self.GRID_WIDTH = 10
        self.GRID_HEIGHT = 20
        self.SCREEN_WIDTH = self.BLOCK_SIZE * (self.GRID_WIDTH + 6)
        self.SCREEN_HEIGHT = self.BLOCK_SIZE * self.GRID_HEIGHT
        
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Tetris")
        
        self.clock = pygame.time.Clock()
        self.game_grid = [[0 for _ in range(self.GRID_WIDTH)] for _ in range(self.GRID_HEIGHT)]
        self.current_piece = None
        self.next_piece = None
        self.score = 0
        self.game_over = False
        self.font = pygame.font.Font(None, 36)
        
    def new_piece(self):
        if not self.next_piece:
            self.next_piece = Tetromino()
        self.current_piece = self.next_piece
        self.next_piece = Tetromino()
        
        if self.check_collision(self.current_piece):
            self.game_over = True
    
    def check_collision(self, piece):
        for y, row in enumerate(piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    new_x = piece.x + x
                    new_y = piece.y + y
                    if (new_x < 0 or new_x >= self.GRID_WIDTH or 
                        new_y >= self.GRID_HEIGHT or 
                        (new_y >= 0 and self.game_grid[new_y][new_x])):
                        return True
        return False
    
    def merge_piece(self):
        for y, row in enumerate(self.current_piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    self.game_grid[self.current_piece.y + y][self.current_piece.x + x] = self.current_piece.color
    
    def clear_lines(self):
        lines_cleared = 0
        y = self.GRID_HEIGHT - 1
        while y >= 0:
            if all(self.game_grid[y]):
                lines_cleared += 1
                del self.game_grid[y]
                self.game_grid.insert(0, [0 for _ in range(self.GRID_WIDTH)])
            else:
                y -= 1
        
        if lines_cleared:
            self.score += (lines_cleared * 100) * lines_cleared
    
    def draw(self):
        self.screen.fill(Colors.BLACK)
        
        # Draw game grid
        for y, row in enumerate(self.game_grid):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(self.screen, cell,
                                   (x * self.BLOCK_SIZE,
                                    y * self.BLOCK_SIZE,
                                    self.BLOCK_SIZE - 1,
                                    self.BLOCK_SIZE - 1))
        
        # Draw current piece
        if self.current_piece:
            for y, row in enumerate(self.current_piece.shape):
                for x, cell in enumerate(row):
                    if cell:
                        pygame.draw.rect(self.screen, self.current_piece.color,
                                       ((self.current_piece.x + x) * self.BLOCK_SIZE,
                                        (self.current_piece.y + y) * self.BLOCK_SIZE,
                                        self.BLOCK_SIZE - 1,
                                        self.BLOCK_SIZE - 1))
        
        # Draw next piece preview
        preview_x = self.GRID_WIDTH * self.BLOCK_SIZE + 30
        preview_y = 50
        if self.next_piece:
            for y, row in enumerate(self.next_piece.shape):
                for x, cell in enumerate(row):
                    if cell:
                        pygame.draw.rect(self.screen, self.next_piece.color,
                                       (preview_x + x * self.BLOCK_SIZE,
                                        preview_y + y * self.BLOCK_SIZE,
                                        self.BLOCK_SIZE - 1,
                                        self.BLOCK_SIZE - 1))
        
        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, Colors.WHITE)
        self.screen.blit(score_text, (preview_x, preview_y + 150))
        
        # Draw game over text
        if self.game_over:
            game_over_text = self.font.render("GAME OVER", True, Colors.RED)
            self.screen.blit(game_over_text, (preview_x, preview_y + 200))
        
        pygame.display.flip()
    
    def run(self):
        self.new_piece()
        fall_time = 0
        fall_speed = 0.5  # seconds
        
        while True:
            self.clock.tick(60)
            fall_time += self.clock.get_rawtime() / 1000
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                
                if not self.game_over:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            self.current_piece.x -= 1
                            if self.check_collision(self.current_piece):
                                self.current_piece.x += 1
                        
                        elif event.key == pygame.K_RIGHT:
                            self.current_piece.x += 1
                            if self.check_collision(self.current_piece):
                                self.current_piece.x -= 1
                        
                        elif event.key == pygame.K_DOWN:
                            self.current_piece.y += 1
                            if self.check_collision(self.current_piece):
                                self.current_piece.y -= 1
                                self.merge_piece()
                                self.clear_lines()
                                self.new_piece()
                        
                        elif event.key == pygame.K_UP:
                            self.current_piece.rotate()
                            if self.check_collision(self.current_piece):
                                self.current_piece.rotate_back()
            
            if not self.game_over:
                if fall_time >= fall_speed:
                    self.current_piece.y += 1
                    if self.check_collision(self.current_piece):
                        self.current_piece.y -= 1
                        self.merge_piece()
                        self.clear_lines()
                        self.new_piece()
                    fall_time = 0
            
            self.draw()

if __name__ == "__main__":
    game = Tetris()
    game.run() 