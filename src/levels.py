"""
Level system - Manages all 140 levels and level progression
"""

import json
import random

class LevelManager:
    def __init__(self, game):
        self.game = game
        self.current_level = 1
        self.level_complete = False
        self.level_timer = 0
        self.enemies_to_spawn = []
        self.wave_index = 0
        
        # Level themes
        self.themes = ['day', 'night', 'ocean', 'desert', 'city', 'space']
        self.current_theme = 'day'
        
        # Load level data
        self.level_data = self.generate_levels()
        
    def generate_levels(self):
        """Generate data for all 140 levels"""
        levels = {}
        
        for level_num in range(1, 141):
            level_data = {
                'enemies': [],
                'boss': level_num % 10 == 0,  # Boss every 10 levels
                'theme': self.get_theme_for_level(level_num),
                'difficulty': self.get_difficulty_for_level(level_num),
                'enemy_count': self.get_enemy_count(level_num),
                'spawn_rate': self.get_spawn_rate(level_num),
                'background_speed': self.get_background_speed(level_num)
            }
            levels[level_num] = level_data
            
        return levels
        
    def get_theme_for_level(self, level):
        """Get theme based on level number"""
        if level <= 30:
            return 'day'
        elif level <= 60:
            return 'ocean'
        elif level <= 90:
            return 'desert'
        elif level <= 110:
            return 'night'
        elif level <= 130:
            return 'city'
        else:
            return 'space'
            
    def get_difficulty_for_level(self, level):
        """Get difficulty multiplier for level"""
        if level <= 20:
            return 'easy'
        elif level <= 60:
            return 'normal'
        elif level <= 100:
            return 'hard'
        else:
            return 'extreme'
            
    def get_enemy_count(self, level):
        """Get number of enemies for level"""
        base_count = 10
        count = base_count + (level // 5)
        return min(count, 50)  # Cap at 50 enemies
        
    def get_spawn_rate(self, level):
        """Get enemy spawn rate for level"""
        base_rate = 1.5
        rate = base_rate - (level / 200)
        return max(rate, 0.3)  # Minimum 0.3 seconds between spawns
        
    def get_background_speed(self, level):
        """Get background scroll speed for level"""
        base_speed = 50
        speed = base_speed + (level // 10)
        return min(speed, 200)  # Cap at 200
        
    def start_level(self, level_num):
        """Start a specific level"""
        self.current_level = level_num
        self.level_complete = False
        self.wave_index = 0
        
        # Set theme
        level_info = self.level_data[level_num]
        self.current_theme = level_info['theme']
        
        # Clear existing entities
        self.game.enemy_manager.clear()
        self.game.boss_manager.bosses.empty()
        
        # Set spawn rates
        self.game.enemy_manager.spawn_delay = level_info['spawn_rate']
        
        # Spawn boss if this is a boss level
        if level_info['boss']:
            self.game.boss_manager.spawn_boss(level_num)
            
        # Update difficulty
        self.update_difficulty_settings(level_info['difficulty'])
        
        # Play appropriate music
        if level_info['boss']:
            self.game.play_music('boss')
        else:
            self.game.play_music('game')
            
        # Show level start message
        self.show_level_start()
        
    def update_difficulty_settings(self, difficulty):
        """Update game difficulty based on level"""
        if difficulty == 'easy':
            self.game.settings.enemy_spawn_multiplier = 0.7
            self.game.settings.enemy_health_multiplier = 0.7
            self.game.settings.enemy_damage_multiplier = 0.6
        elif difficulty == 'normal':
            self.game.settings.enemy_spawn_multiplier = 1.0
            self.game.settings.enemy_health_multiplier = 1.0
            self.game.settings.enemy_damage_multiplier = 1.0
        elif difficulty == 'hard':
            self.game.settings.enemy_spawn_multiplier = 1.3
            self.game.settings.enemy_health_multiplier = 1.2
            self.game.settings.enemy_damage_multiplier = 1.2
        else:  # extreme
            self.game.settings.enemy_spawn_multiplier = 1.6
            self.game.settings.enemy_health_multiplier = 1.5
            self.game.settings.enemy_damage_multiplier = 1.4
            
    def update(self, dt):
        """Update level manager"""
        if not self.level_complete:
            # Check if level is complete
            if not self.game.boss_manager.active and self.game.enemy_manager.is_empty():
                self.level_complete = True
                
    def next_level(self):
        """Advance to next level"""
        if self.current_level < 140:
            self.current_level += 1
            self.start_level(self.current_level)
        else:
            # Game completed
            self.game.game_state = "victory"
            self.game.play_music('victory')
            
    def boss_defeated(self):
        """Handle boss defeat"""
        self.level_complete = True
        
    def show_level_start(self):
        """Show level start message"""
        # This will be handled in UI
        pass
        
    def get_current_theme(self):
        """Get current level theme"""
        return self.current_theme
        
    def get_level_info(self):
        """Get current level information"""
        return self.level_data.get(self.current_level, {})