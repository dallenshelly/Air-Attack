"""
Image Loading System - Centralized asset management
"""

import pygame
import os

class ImageLoader:
    def __init__(self, game):
        self.game = game
        self.images = {}
        
    def load_all_images(self):
        """Load all game images from assets/images/"""
        print("Loading images...")
        
        # Define all images with their filenames
        image_files = {
            # Player images
            'player': 'player.png',
            'player_animation_1': 'player_animation.png',
            'player_animation_2': 'player_animation2.png',
            
            # Enemy images
            'enemy_basic': 'enemy.png',
            'enemy_fast': 'enemy_fast.png',
            'enemy_heavy': 'enemy_heavy.png',
            'enemy_helicopter': 'enemy_helicopter.png',
            'enemy_missile': 'enemy_missile.png',
            'enemy_kamikaze': 'enemy_kamikaze.png',
            'enemy_stealth': 'enemy_stealth.png',
            'enemy_miniboss': 'enemy_miniboss.png',
            
            # Boss images
            'boss': 'boss.png',
            'boss_1': 'boss.png',
            'boss_2': 'boss.png',
            'boss_3': 'boss_5.png',
            'boss_4': 'boss_5.png',
            'boss_5': 'boss_5.png',
            'boss_6': 'boss_7.png',
            'boss_7': 'boss_7.png',
            'boss_8': 'boss_7.png',
            'boss_9': 'boss_9.png',
            'boss_10': 'boss_9.png',
            
            # Powerup images
            'powerup_double': 'powerup_double.png',
            'powerup_triple': 'powerup_triple.png',
            'powerup_laser': 'powerup_laser.png',
            'powerup_shield': 'shield_icon.png',
            'powerup_health': 'heart.png',
            'powerup_missile': 'powerup_missile.png',
            'powerup_speed': 'powerup_speed.png',
            'powerup_magnet': 'powerup_magnet.png',
            'powerup_life': 'powerup_life.png',
            
            # Bullet images
            'bullet_player': 'bullet_player.png',
            'bullet_enemy': 'bullet_enemy.png',
            'missile_player': 'missilep.png',
            'missile_enemy': 'missilee_enemy.png',
            'laser': 'laser.png',
            
            # Effect images
            'explosion_1': 'explosion_1.png',
            'explosion_2': 'explosion_2.png',
            'explosion_3': 'explosion_3.png',
            'smoke': 'smoke.png',
            'flash': 'flash.png',
            
            # UI images
            'heart': 'heart.png',
            'shield_icon': 'shield_icon.png',
            'missile_icon': 'powerup_missile.png',
            'star': 'star.png'
        }
        
        # Load each image
        for key, filename in image_files.items():
            self.images[key] = self.load_image(filename, key)
            
        # Load background images
        backgrounds = ['bg_day', 'bg_night', 'bg_ocean', 'bg_desert', 'bg_city', 'bg_space']
        for bg in backgrounds:
            self.images[bg] = self.load_image(f'{bg}.png', bg, is_background=True)
            
        print(f"Loaded {len([v for v in self.images.values() if v is not None])} images successfully")
        return self.images
        
    def load_image(self, filename, key, is_background=False):
        """Load a single image from file"""
        # Check multiple possible paths
        paths = [
            os.path.join('assets', 'images', filename),
            os.path.join('assets', 'images', filename.lower()),
            os.path.join('assets', 'images', key, filename),
            filename
        ]
        
        for path in paths:
            if os.path.exists(path):
                try:
                    image = pygame.image.load(path).convert_alpha()
                    print(f"  Loaded: {key} from {path}")
                    
                    # Scale background to screen size
                    if is_background:
                        image = pygame.transform.scale(image, 
                            (self.game.settings.width, self.game.settings.height))
                    # Scale small images to reasonable sizes
                    elif key in ['player', 'enemy_basic', 'enemy_fast', 'enemy_heavy']:
                        if image.get_width() > 100:
                            image = pygame.transform.scale(image, (50, 50))
                    elif key.startswith('boss'):
                        if image.get_width() > 200:
                            image = pygame.transform.scale(image, (120, 120))
                            
                    return image
                except pygame.error as e:
                    print(f"  Error loading {key} from {path}: {e}")
                    
        # Return placeholder if image not found
        print(f"  Warning: Could not find {key} image, using placeholder")
        return self.create_placeholder(key, is_background)
        
    def create_placeholder(self, key, is_background=False):
        """Create a colored placeholder for missing images"""
        if is_background:
            surf = pygame.Surface((self.game.settings.width, self.game.settings.height))
            surf.fill((0, 0, 0))
            return surf
            
        # Create colored rectangles based on image type
        if key == 'player':
            surf = pygame.Surface((40, 40), pygame.SRCALPHA)
            pygame.draw.polygon(surf, (0, 255, 0), [(20, 0), (0, 40), (40, 40)])
            pygame.draw.polygon(surf, (0, 200, 0), [(20, 5), (5, 35), (35, 35)])
            
        elif key.startswith('enemy'):
            surf = pygame.Surface((35, 35), pygame.SRCALPHA)
            pygame.draw.polygon(surf, (255, 0, 0), [(17, 0), (0, 35), (35, 35)])
            pygame.draw.polygon(surf, (200, 0, 0), [(17, 5), (5, 30), (30, 30)])
            
        elif key.startswith('boss'):
            surf = pygame.Surface((100, 100), pygame.SRCALPHA)
            pygame.draw.ellipse(surf, (150, 0, 0), surf.get_rect())
            pygame.draw.circle(surf, (255, 0, 0), (50, 30), 15)
            
        elif key.startswith('powerup'):
            surf = pygame.Surface((20, 20), pygame.SRCALPHA)
            colors = {
                'double': (0, 255, 255),
                'triple': (255, 255, 0),
                'laser': (255, 0, 255),
                'shield': (0, 100, 255),
                'health': (0, 255, 0),
                'missile': (255, 165, 0),
                'speed': (255, 0, 0),
                'magnet': (255, 255, 255),
                'life': (255, 215, 0)
            }
            color = colors.get(key.split('_')[1] if '_' in key else 'double', (255, 255, 255))
            pygame.draw.circle(surf, color, (10, 10), 8)
            pygame.draw.circle(surf, (255, 255, 255), (10, 10), 8, 2)
            
        elif key == 'bullet_player':
            surf = pygame.Surface((5, 10))
            surf.fill((255, 255, 0))
            
        elif key == 'bullet_enemy':
            surf = pygame.Surface((5, 10))
            surf.fill((255, 0, 0))
            
        elif key == 'missile_player':
            surf = pygame.Surface((8, 15), pygame.SRCALPHA)
            pygame.draw.ellipse(surf, (255, 100, 0), surf.get_rect())
            pygame.draw.polygon(surf, (255, 0, 0), [(4, 0), (8, 8), (4, 15), (0, 8)])
            
        else:
            surf = pygame.Surface((30, 30))
            surf.fill((100, 100, 100))
            
        return surf
        
    def get_image(self, key):
        """Get an image by key"""
        return self.images.get(key)
        
    def get_enemy_image(self, enemy_type):
        """Get enemy image based on type"""
        type_map = {
            'basic': 'enemy_basic',
            'fast': 'enemy_fast',
            'heavy': 'enemy_heavy',
            'helicopter': 'enemy_helicopter',
            'missile_carrier': 'enemy_missile',
            'kamikaze': 'enemy_kamikaze',
            'stealth': 'enemy_stealth',
            'mini_boss': 'enemy_miniboss'
        }
        key = type_map.get(enemy_type, 'enemy_basic')
        return self.images.get(key, self.images.get('enemy_basic'))
        
    def get_boss_image(self, level):
        """Get boss image based on level"""
        boss_num = (level // 10)
        if boss_num <= 10:
            key = f'boss_{boss_num}'
            if key in self.images and self.images[key]:
                return self.images[key]
        return self.images.get('boss', self.images.get('enemy_heavy'))