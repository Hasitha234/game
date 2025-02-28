import pygame
from tetris import Tetris
from tetris_ai import TetrisAI
import time

def train_ai(num_episodes, display_game=True):
    ai = TetrisAI()
    stats = []
    
    for episode in range(num_episodes):
        game = Tetris()
        game.new_piece()  # Initialize the first piece
        total_reward = 0
        moves = 0
        start_time = time.time()
        
        while not game.game_over:
            current_state = ai.get_state_features(game)
            action = ai.choose_action(current_state)
            
            # Execute the chosen action
            old_score = game.score
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
                lines_cleared = game.clear_lines()
                game.new_piece()
            
            next_state = ai.get_state_features(game)
            reward = ai.get_reward(game, (game.score - old_score) // 100, game.game_over)
            total_reward += reward
            
            # Update Q-table
            ai.update(current_state, action, reward, next_state)
            
            moves += 1
            
            if display_game:
                game.draw()
                pygame.time.delay(50)  # Slow down the game to make it visible
        
        duration = time.time() - start_time
        stats.append({
            'episode': episode + 1,
            'score': game.score,
            'moves': moves,
            'total_reward': total_reward,
            'duration': duration,
            'epsilon': ai.epsilon
        })
        
        # Print episode statistics
        print(f"Episode {episode + 1}/{num_episodes}")
        print(f"Score: {game.score}")
        print(f"Moves: {moves}")
        print(f"Total Reward: {total_reward:.2f}")
        print(f"Duration: {duration:.2f}s")
        print(f"Epsilon: {ai.epsilon:.4f}")
        print("-" * 50)
    
    return stats

if __name__ == "__main__":
    # Set the number of training episodes
    NUM_EPISODES = 100
    
    # Ask if the user wants to display the game during training
    display_game = input("Display game during training? (y/n): ").lower() == 'y'
    
    # Train the AI
    stats = train_ai(NUM_EPISODES, display_game)
    
    # Print final statistics
    print("\nTraining Complete!")
    print(f"Best Score: {max(stat['score'] for stat in stats)}")
    print(f"Average Score: {sum(stat['score'] for stat in stats) / len(stats):.2f}")
    print(f"Total Training Time: {sum(stat['duration'] for stat in stats):.2f}s") 