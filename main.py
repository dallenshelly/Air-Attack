"""
Air Attack - Arcade Aerial Combat Game
Main entry point
"""

import pygame
import sys
import os
from src.game import Game

def main():
    """Main game entry point"""
    try:
        # Initialize pygame
        pygame.init()
        pygame.mixer.init()
        
        # Create and run game
        game = Game()
        game.run()
        
    except Exception as e:
        print(f"Error starting game: {e}")
        import traceback
        traceback.print_exc()
    finally:
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()