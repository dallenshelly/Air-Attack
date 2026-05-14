"""
Game settings and configuration
"""

import pygame
import json
import os

class Settings:
    def __init__(self):
        """Initialize game settings"""
        self.width = 1280
        self.height = 720
        self.fps = 60
        self.fullscreen = False
        
        # Volume settings (0-100)
        self.music_volume = 70
        self.sound_volume = 80
        
        # Difficulty settings
        self.difficulty = "normal"  # easy, normal, hard, extreme
        self.get_difficulty_multipliers()
        
        # Key bindings
        self.key_up = [pygame.K_UP, pygame.K_w]
        self.key_down = [pygame.K_DOWN, pygame.K_s]
        self.key_left = [pygame.K_LEFT, pygame.K_a]
        self.key_right = [pygame.K_RIGHT, pygame.K_d]
        self.key_shoot = [pygame.K_SPACE]
        self.key_missile = [pygame.K_LSHIFT, pygame.K_RSHIFT]
        self.key_pause = [pygame.K_ESCAPE]
        
        # Load saved settings
        self.load_settings()
        
    def get_difficulty_multipliers(self):
        """Set difficulty multipliers"""
        if self.difficulty == "easy":
            self.enemy_spawn_multiplier = 0.7
            self.enemy_health_multiplier = 0.7
            self.enemy_damage_multiplier = 0.6
            self.player_damage_multiplier = 1.3
            self.score_multiplier = 0.8
        elif self.difficulty == "normal":
            self.enemy_spawn_multiplier = 1.0
            self.enemy_health_multiplier = 1.0
            self.enemy_damage_multiplier = 1.0
            self.player_damage_multiplier = 1.0
            self.score_multiplier = 1.0
        elif self.difficulty == "hard":
            self.enemy_spawn_multiplier = 1.3
            self.enemy_health_multiplier = 1.2
            self.enemy_damage_multiplier = 1.2
            self.player_damage_multiplier = 0.9
            self.score_multiplier = 1.2
        else:  # extreme
            self.enemy_spawn_multiplier = 1.6
            self.enemy_health_multiplier = 1.5
            self.enemy_damage_multiplier = 1.4
            self.player_damage_multiplier = 0.8
            self.score_multiplier = 1.5
            
    def load_settings(self):
        """Load settings from file"""
        try:
            if os.path.exists('data/settings.json'):
                with open('data/settings.json', 'r') as f:
                    data = json.load(f)
                    self.music_volume = data.get('music_volume', 70)
                    self.sound_volume = data.get('sound_volume', 80)
                    self.difficulty = data.get('difficulty', 'normal')
                    self.fullscreen = data.get('fullscreen', False)
                    self.get_difficulty_multipliers()
        except:
            pass
            
    def save_settings(self):
        """Save settings to file"""
        try:
            data = {
                'music_volume': self.music_volume,
                'sound_volume': self.sound_volume,
                'difficulty': self.difficulty,
                'fullscreen': self.fullscreen
            }
            os.makedirs('data', exist_ok=True)
            with open('data/settings.json', 'w') as f:
                json.dump(data, f, indent=4)
        except:
            pass
            
    def toggle_fullscreen(self):
        """Toggle fullscreen mode"""
        self.fullscreen = not self.fullscreen
        self.save_settings()