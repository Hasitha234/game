import pygame
from tetris import Tetris
from tetris_ai import TetrisAI
import time

def play_ai_game(ai, delay=100):
    game = Tetris()
    game.new_piece()  # Initialize the first piece
    moves = 0
    start_time = time.time()
    
    while not game.game_over:
        current_state = ai.get_state_features(game)
        action = ai.choose_action(current_state)
        
        # Execute the chosen action
        if action == 'left':
            game.current_piece.x -= 1
            if game.check_collision(game.current_piece):
                game.current_piece.x += 1
        elif action == 'right':
            game.current_piece.x += 1
            if game.check_collision(game.current_piece):
                game.current_piece.x -= 1
        elif action == 'rotate':
            game.current_piece.rotate()
            if game.check_collision(game.current_piece):
                game.current_piece.rotate_back()
        
        # Always move down after any action
        game.current_piece.y += 1
        if game.check_collision(game.current_piece):
            game.current_piece.y -= 1
            game.merge_piece()
            game.clear_lines()
            game.new_piece()
        
        moves += 1
        game.draw()
        pygame.time.delay(delay)  # Control game speed
        
        # Handle pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return
                elif event.key == pygame.K_UP:
                    delay = min(delay + 50, 500)  # Slow down
                elif event.key == pygame.K_DOWN:
                    delay = max(delay - 50, 0)  # Speed up
    
    duration = time.time() - start_time
    print("\nGame Over!")
    print(f"Final Score: {game.score}")
    print(f"Moves Made: {moves}")
    print(f"Duration: {duration:.2f}s")
    print(f"Average Speed: {moves/duration:.2f} moves/second")

if __name__ == "__main__":
    # Create and load a pre-trained AI
    ai = TetrisAI()
    ai.epsilon = 0  # Set to 0 for pure exploitation (no random moves)
    
    print("Controls:")
    print("ESC - Quit game")
    print("UP - Slow down")
    print("DOWN - Speed up")
    print("\nStarting game in 3 seconds...")
    time.sleep(3)
    
    play_ai_game(ai) 