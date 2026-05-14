"""
Main game class - Orchestrates all game systems
"""

import pygame
import sys
import os
import random
from datetime import datetime
from src.settings import Settings
from src.player import Player
from src.enemy import EnemyManager
from src.boss import BossManager
from src.levels import LevelManager
from src.ui import UIManager
from src.save_system import SaveSystem
from src.weapons import WeaponSystem
from src.effects import EffectSystem
from src.menu import MenuSystem
from src.img_load import ImageLoader

class Game:
    def __init__(self):
        """Initialize game systems"""
        self.settings = Settings()
        self.random = random
        
        self.screen = pygame.display.set_mode(
            (self.settings.width, self.settings.height),
            pygame.DOUBLEBUF | pygame.HWSURFACE
        )
        pygame.display.set_caption("Air Attack - Aerial Combat")
        
        # Game state
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_state = "menu"
        self.dt = 0
        
        # Initialize systems
        self.save_system = SaveSystem()
        self.player_data = self.save_system.load_game()
        
        # Initialize image loader
        self.image_loader = ImageLoader(self)
        
        # Load assets FIRST
        self.load_assets()
        
        # Initialize managers
        self.player = None
        self.enemy_manager = None
        self.boss_manager = None
        self.level_manager = None
        self.ui_manager = None
        self.weapon_system = None
        self.effect_system = None
        self.menu_system = None
        
        # Score tracking
        self.score = 0
        self.combo = 0
        self.combo_timer = 0
        self.kills = 0
        self.bullets_fired = 0
        self.bullets_hit = 0
        
        # Background scroll
        self.bg_scroll = 0
        self.stars = []
        
        # Current background theme
        self.current_bg_theme = 'day'
        
        # Initialize subsystems
        self.init_subsystems()
        
    def init_subsystems(self):
        """Initialize all game subsystems"""
        self.effect_system = EffectSystem(self)
        self.weapon_system = WeaponSystem(self)
        self.player = Player(self, self.weapon_system)
        self.enemy_manager = EnemyManager(self)
        self.boss_manager = BossManager(self)
        self.level_manager = LevelManager(self)
        self.ui_manager = UIManager(self)
        self.menu_system = MenuSystem(self)
        
    def load_assets(self):
        """Load all game assets"""
        self.create_asset_dirs()
        
        # Initialize containers
        self.images = {}
        self.sounds = {}
        self.music = {}
        
        # Load fonts
        try:
            self.font_large = pygame.font.Font(None, 72)
            self.font_medium = pygame.font.Font(None, 48)
            self.font_small = pygame.font.Font(None, 36)
            self.font_tiny = pygame.font.Font(None, 24)
        except:
            self.font_large = pygame.font.SysFont('Arial', 72)
            self.font_medium = pygame.font.SysFont('Arial', 48)
            self.font_small = pygame.font.SysFont('Arial', 36)
            self.font_tiny = pygame.font.SysFont('Arial', 24)
        
        # Load images using ImageLoader
        self.load_images()
        
        # Load sounds and music
        self.load_sounds()
        self.load_music()
        
    def create_asset_dirs(self):
        """Create necessary asset directories"""
        dirs = ['assets/images', 'assets/sounds', 'assets/music', 'assets/fonts', 'data']
        for dir_path in dirs:
            os.makedirs(dir_path, exist_ok=True)
            
    def load_images(self):
        """Load all images using ImageLoader"""
        print("Loading images from centralized system...")
        self.images = self.image_loader.load_all_images()
        
    def load_sounds(self):
        """Load sound effects"""
        sound_files = {
            'shoot': 'shoot.wav',
            'explosion': 'explosion.wav',
            'powerup': 'powerup.wav',
            'hit': 'hit.wav',
            'laser': 'laser.wav',
            'missile': 'missile.wav',
            'boss_alarm': 'alarm.wav',
            'ui_click': 'click.wav',
            'game_over': 'game_over.wav',
            'level_up': 'level_up.wav'
        }
        
        for sound_name, sound_file in sound_files.items():
            try:
                sound_path = os.path.join('assets', 'sounds', sound_file)
                if os.path.exists(sound_path):
                    self.sounds[sound_name] = pygame.mixer.Sound(sound_path)
                else:
                    self.sounds[sound_name] = None
            except:
                self.sounds[sound_name] = None
                
    def load_music(self):
        """Load background music"""
        music_files = {
            'menu': 'menu_music.mp3',
            'game': 'game_music.mp3',
            'boss': 'boss_music.mp3',
            'victory': 'victory_music.mp3'
        }
        
        for music_name, music_file in music_files.items():
            try:
                music_path = os.path.join('assets', 'music', music_file)
                if os.path.exists(music_path):
                    self.music[music_name] = music_path
            except:
                pass
                
    def set_background_theme(self, theme):
        """Set the current background theme"""
        self.current_bg_theme = theme
                
    def run(self):
        """Main game loop"""
        while self.running:
            self.dt = self.clock.tick(self.settings.fps) / 1000.0
            if self.dt > 0.033:
                self.dt = 0.033
                
            self.handle_events()
            
            if self.game_state == "playing":
                self.update()
            elif self.game_state == "menu":
                self.menu_system.update()
            elif self.game_state == "paused":
                self.menu_system.update_pause()
            elif self.game_state == "game_over":
                self.menu_system.update_game_over()
            elif self.game_state == "victory":
                self.menu_system.update_victory()
                
            self.render()
            
        self.save_system.save_game(self.player_data)
        
    def handle_events(self):
        """Handle all input events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.game_state == "playing":
                        self.game_state = "paused"
                    elif self.game_state == "paused":
                        self.game_state = "playing"
                        
                if event.key == pygame.K_F1:
                    self.score += 1000
                elif event.key == pygame.K_F2:
                    if hasattr(self, 'level_manager'):
                        self.level_manager.next_level()
                        
            if self.game_state == "menu":
                self.menu_system.handle_event(event)
            elif self.game_state == "playing" and self.player:
                self.player.handle_event(event)
                
    def update(self):
        """Update game logic"""
        if self.combo_timer > 0:
            self.combo_timer -= self.dt
            if self.combo_timer <= 0:
                self.combo = 0
                
        self.player.update(self.dt)
        self.enemy_manager.update(self.dt)
        self.boss_manager.update(self.dt)
        self.weapon_system.update(self.dt)
        self.effect_system.update(self.dt)
        self.level_manager.update(self.dt)
        
        self.check_collisions()
        
        if self.enemy_manager.is_empty() and not self.boss_manager.active and self.level_manager.level_complete:
            self.level_complete()
            
        if self.player.health <= 0:
            self.game_over()
            
    def check_collisions(self):
        """Handle all collision detection"""
        # Player bullets vs enemies
        for bullet in self.weapon_system.bullets:
            if bullet.owner == "player":
                hit_enemies = pygame.sprite.spritecollide(bullet, self.enemy_manager.enemies, False)
                hit_boss = pygame.sprite.spritecollide(bullet, self.boss_manager.bosses, False)
                
                for enemy in hit_enemies:
                    if enemy.hit(bullet.damage):
                        self.add_score(enemy.score_value)
                        self.kills += 1
                        self.bullets_hit += 1
                        self.combo += 1
                        self.combo_timer = 3.0
                        self.effect_system.add_explosion(enemy.rect.center)
                        self.play_sound('explosion')
                    bullet.kill()
                    break
                    
                for boss in hit_boss:
                    if boss.hit(bullet.damage):
                        self.add_score(boss.score_value)
                        self.bullets_hit += 1
                        self.combo += 1
                        self.combo_timer = 3.0
                        self.effect_system.add_explosion(boss.rect.center)
                        self.play_sound('hit')
                    bullet.kill()
                    break
                    
        # Enemy bullets vs player
        for bullet in self.weapon_system.bullets:
            if bullet.owner == "enemy":
                if self.player.rect.colliderect(bullet.rect):
                    self.player.take_damage(bullet.damage)
                    bullet.kill()
                    self.play_sound('hit')
                    
        # Enemies vs player
        if self.player:
            enemy_collisions = pygame.sprite.spritecollide(self.player, self.enemy_manager.enemies, True)
            for enemy in enemy_collisions:
                self.player.take_damage(enemy.damage)
                self.effect_system.add_explosion(enemy.rect.center)
                self.play_sound('explosion')
                self.add_score(enemy.score_value // 2)
                
        # Powerups
        if self.player:
            powerup_collisions = pygame.sprite.spritecollide(self.player, self.weapon_system.powerups, True)
            for powerup in powerup_collisions:
                self.apply_powerup(powerup.type)
                self.play_sound('powerup')
                
    def apply_powerup(self, powerup_type):
        """Apply powerup effects"""
        if powerup_type == "double":
            self.weapon_system.upgrade_weapon("double")
        elif powerup_type == "triple":
            self.weapon_system.upgrade_weapon("triple")
        elif powerup_type == "laser":
            self.weapon_system.upgrade_weapon("laser")
        elif powerup_type == "shield":
            self.player.activate_shield(10.0)
        elif powerup_type == "health":
            self.player.heal(20)
        elif powerup_type == "missile":
            self.player.missiles += 3
        elif powerup_type == "speed":
            self.player.activate_speed_boost(5.0)
        elif powerup_type == "magnet":
            self.player.activate_magnet(8.0)
        elif powerup_type == "life":
            self.player.lives += 1
            
    def add_score(self, points):
        """Add points to score with combo multiplier"""
        multiplier = 1 + (self.combo // 10)
        added_points = points * multiplier
        self.score += added_points
        
        if self.score > self.player_data.get('high_score', 0):
            self.player_data['high_score'] = self.score
            
    def level_complete(self):
        """Handle level completion"""
        survival_bonus = self.player.health * 10
        accuracy = (self.bullets_hit / max(1, self.bullets_fired)) * 100
        accuracy_bonus = int(accuracy * 5)
        combo_bonus = self.combo * 10
        
        total_bonus = survival_bonus + accuracy_bonus + combo_bonus
        self.score += total_bonus
        
        self.player_data['total_score'] = self.score
        self.player_data['current_level'] = self.level_manager.current_level + 1
        self.save_system.save_game(self.player_data)
        
        self.level_manager.next_level()
        self.reset_level_stats()
        
    def reset_level_stats(self):
        """Reset level-specific stats"""
        self.combo = 0
        self.combo_timer = 0
        self.bullets_fired = 0
        self.bullets_hit = 0
        
        if self.player:
            self.player.heal(10)
        
    def game_over(self):
        """Handle game over"""
        self.game_state = "game_over"
        self.play_sound('game_over')
        
        self.player_data['total_score'] = self.score
        if self.score > self.player_data.get('high_score', 0):
            self.player_data['high_score'] = self.score
        self.save_system.save_game(self.player_data)
        
    def play_sound(self, sound_name):
        """Play a sound effect"""
        sound = self.sounds.get(sound_name)
        if sound and self.settings.sound_volume > 0:
            sound.set_volume(self.settings.sound_volume / 100.0)
            sound.play()
            
    def play_music(self, music_name):
        """Play background music"""
        music_path = self.music.get(music_name)
        if music_path and self.settings.music_volume > 0:
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.set_volume(self.settings.music_volume / 100.0)
            pygame.mixer.music.play(-1)
            
    def render(self):
        """Render everything to screen"""
        # Clear screen
        self.screen.fill((0, 0, 0))
        
        # Render based on game state
        if self.game_state == "playing":
            self.render_background()
            self.enemy_manager.draw(self.screen)
            self.boss_manager.draw(self.screen)
            self.player.draw(self.screen)
            self.weapon_system.draw(self.screen)
            self.effect_system.draw(self.screen)
            self.ui_manager.draw(self.screen)
        elif self.game_state == "menu":
            self.menu_system.render(self.screen)
        elif self.game_state == "paused":
            self.render_background()
            self.enemy_manager.draw(self.screen)
            self.boss_manager.draw(self.screen)
            self.player.draw(self.screen)
            self.weapon_system.draw(self.screen)
            self.effect_system.draw(self.screen)
            self.menu_system.render_pause_overlay(self.screen)
        elif self.game_state == "game_over":
            self.render_background()
            self.menu_system.render_game_over(self.screen, self.score)
        elif self.game_state == "victory":
            self.menu_system.render_victory(self.screen, self.score)
            
        # Update display
        pygame.display.flip()
        
    def render_background(self):
        """Render scrolling background using ImageLoader"""
        # Get current theme from level manager or use stored theme
        if hasattr(self, 'level_manager') and self.level_manager:
            theme = self.level_manager.get_current_theme()
            self.current_bg_theme = theme
        else:
            theme = self.current_bg_theme
            
        # Get background image from images dictionary (loaded by ImageLoader)
        bg_image = self.images.get(f'bg_{theme}', self.images.get('bg_day', self.images.get('background')))
        
        # Fallback to direct loading if not found in images
        if bg_image is None:
            # Try to load directly using ImageLoader's methods
            try:
                if hasattr(self, 'image_loader'):
                    bg_image = self.image_loader.load_background(theme)
                    if bg_image:
                        self.images[f'bg_{theme}'] = bg_image
                    else:
                        bg_image = self.image_loader.load_default_background()
            except:
                bg_image = None
        
        if bg_image:
            # Scroll background
            self.bg_scroll += self.dt * 50
            
            # Draw tiled background (multiple copies for seamless scrolling)
            bg_height = bg_image.get_height()
            scroll_mod = int(self.bg_scroll) % bg_height
            
            # Draw first copy
            self.screen.blit(bg_image, (0, scroll_mod - bg_height))
            # Draw second copy
            self.screen.blit(bg_image, (0, scroll_mod))
            
            # Draw third copy if needed for smoother scrolling
            if scroll_mod < self.settings.height:
                self.screen.blit(bg_image, (0, scroll_mod + bg_height))
        else:
            # Fallback solid color background with theme colors
            fallback_colors = {
                'day': (135, 206, 235),      # Sky blue
                'night': (25, 25, 50),        # Dark blue/black
                'ocean': (0, 100, 150),       # Deep ocean blue
                'desert': (210, 180, 140),    # Sand color
                'city': (50, 50, 70),         # Dark city night
                'space': (0, 0, 0),           # Black
                'fire': (139, 0, 0),          # Dark red
                'ice': (173, 216, 230)        # Light blue
            }
            self.screen.fill(fallback_colors.get(theme, (0, 0, 0)))
            
        # Draw stars for night/space themes
        if theme in ['night', 'space']:
            self.draw_stars()
            
    def draw_stars(self):
        """Draw star field"""
        if not self.stars:
            self.stars = [(random.randint(0, self.settings.width),
                          random.randint(0, self.settings.height),
                          random.randint(1, 3)) for _ in range(200)]
                          
        for x, y, size in self.stars:
            pygame.draw.circle(self.screen, (255, 255, 255), (int(x), int(y)), size)
