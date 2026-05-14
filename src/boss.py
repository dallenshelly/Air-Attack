"""
Boss system - Boss enemies and boss fights
"""

import pygame
import math
import random

class Boss(pygame.sprite.Sprite):
    def __init__(self, game, level):
        super().__init__()
        self.game = game
        self.level = level
        self.image = None  # Required for pygame.sprite
        
        # Boss stats
        self.health = 500 + (level // 10) * 200
        self.max_health = self.health
        self.damage = 30
        self.score_value = 5000
        
        # Phase system
        self.phase = 1
        self.max_phases = 3
        self.phase_health_threshold = (0.66, 0.33)
        
        # Load boss image
        self.original_image = None
        self.load_image()
        
        # Set dimensions
        if self.image:
            self.width = self.image.get_width()
            self.height = self.image.get_height()
        else:
            self.width = 100
            self.height = 100
            self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            pygame.draw.ellipse(self.image, (150, 0, 0), self.image.get_rect())
            
        # Position
        self.rect = pygame.Rect(
            self.game.settings.width // 2 - self.width // 2,
            50,
            self.width,
            self.height
        )
        
        # Movement
        self.velocity_x = 100
        self.velocity_y = 0
        
        # Attack system
        self.attack_timer = 0
        self.attack_delay = 2.0
        self.attack_pattern = 0
        
        # Effects
        self.rotation = 0
        self.particles = []
        
    def load_image(self):
        """Load boss image from centralized system"""
        boss_num = (self.level // 10)
        specific_key = f'boss_{boss_num}'
        
        self.original_image = self.game.images.get(specific_key)
        
        if not self.original_image:
            self.original_image = self.game.images.get('boss')
            
        if self.original_image:
            self.image = pygame.transform.scale(
                self.original_image, (120, 120)
            )
            print(f"Loaded boss image for level {self.level}")
        
    def update(self, dt):
        """Update boss"""
        self.update_movement(dt)
        self.rect.x += self.velocity_x * dt
        self.rect.y += self.velocity_y * dt
        
        # Keep boss within bounds
        if self.rect.left < 50:
            self.rect.left = 50
            self.velocity_x = abs(self.velocity_x)
        elif self.rect.right > self.game.settings.width - 50:
            self.rect.right = self.game.settings.width - 50
            self.velocity_x = -abs(self.velocity_x)
            
        if self.rect.top < 50:
            self.rect.top = 50
        elif self.rect.bottom > self.game.settings.height // 2:
            self.rect.bottom = self.game.settings.height // 2
            
        # Update attacks
        if self.attack_timer <= 0:
            self.attack()
            self.attack_timer = self.attack_delay
        else:
            self.attack_timer -= dt
            
        # Update phase
        health_percent = self.health / self.max_health
        if health_percent <= self.phase_health_threshold[1] and self.phase < 3:
            self.phase = 3
            self.enter_new_phase()
        elif health_percent <= self.phase_health_threshold[0] and self.phase < 2:
            self.phase = 2
            self.enter_new_phase()
            
        for particle in self.particles[:]:
            particle['life'] -= dt
            if particle['life'] <= 0:
                self.particles.remove(particle)
                
    def update_movement(self, dt):
        """Update boss movement pattern"""
        self.velocity_x = 100 * math.sin(pygame.time.get_ticks() * 0.001)
        
        if self.phase == 2:
            self.velocity_x *= 1.5
        elif self.phase == 3:
            self.velocity_x *= 2
            
    def attack(self):
        """Execute boss attack based on phase - ALL DOWNWARD"""
        if self.phase == 1:
            self.basic_attack()
        elif self.phase == 2:
            self.aggressive_attack()
        else:
            self.desperation_attack()
            
        self.game.play_sound('shoot')
        
    def basic_attack(self):
        """Basic attack pattern - shoots DOWNWARD"""
        for angle in [85, 90, 95]:
            self.game.weapon_system.fire_enemy_bullet(
                self.rect.centerx, self.rect.bottom, angle, is_boss=True
            )
            
    def aggressive_attack(self):
        """Aggressive attack pattern - DOWNWARD spread"""
        for i in range(3):
            for angle in [80, 85, 90, 95, 100]:
                self.game.weapon_system.fire_enemy_bullet(
                    self.rect.centerx, self.rect.bottom, angle + i * 5, is_boss=True
                )
                
        for _ in range(3):
            self.game.weapon_system.fire_enemy_missile(
                self.rect.centerx, self.rect.bottom, self.game.player, is_boss=True
            )
            
    def desperation_attack(self):
        """Desperation attack pattern - DOWNWARD bullet hell"""
        for i in range(12):
            angle = 70 + (i * 3) + math.sin(pygame.time.get_ticks() * 0.01) * 10
            self.game.weapon_system.fire_enemy_bullet(
                self.rect.centerx, self.rect.bottom, angle, is_boss=True
            )
            
        self.game.effect_system.add_screen_shake(0.5)
        
    def enter_new_phase(self):
        """Enter a new boss phase"""
        for _ in range(20):
            self.game.effect_system.add_particle(
                self.rect.centerx + random.randint(-50, 50),
                self.rect.centery + random.randint(-50, 50),
                random.uniform(-100, 100),
                random.uniform(-100, 100)
            )
        self.attack_delay = max(0.5, self.attack_delay * 0.8)
        
    def hit(self, damage):
        """Handle boss taking damage"""
        damage = int(damage * self.game.settings.player_damage_multiplier)
        self.health -= damage
        
        self.game.effect_system.add_particle(
            self.rect.centerx + random.randint(-30, 30),
            self.rect.centery + random.randint(-30, 30),
            random.uniform(-50, 50),
            random.uniform(-50, 50)
        )
        self.game.effect_system.add_screen_shake(0.1)
        
        if self.health <= 0:
            self.kill()
            self.on_death()
            return True
        return False
        
    def on_death(self):
        """Handle boss death"""
        for _ in range(50):
            self.game.effect_system.add_particle(
                self.rect.centerx + random.randint(-100, 100),
                self.rect.centery + random.randint(-100, 100),
                random.uniform(-200, 200),
                random.uniform(-200, 200)
            )
            
        bonus = self.max_health * 10
        self.game.add_score(bonus)
        
        for _ in range(5):
            self.game.weapon_system.spawn_powerup(
                self.rect.centerx + random.randint(-50, 50),
                self.rect.centery + random.randint(-50, 50)
            )
            
        self.game.play_sound('explosion')
        self.game.effect_system.add_screen_shake(1.0)
        
    def draw_health_bar(self, screen):
        """Draw boss health bar"""
        bar_width = 400
        bar_height = 20
        bar_x = self.game.settings.width // 2 - bar_width // 2
        bar_y = 20
        
        pygame.draw.rect(screen, (255, 0, 0),
                        (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(screen, (0, 255, 0),
                        (bar_x, bar_y, bar_width * (self.health / self.max_health), bar_height))
        pygame.draw.rect(screen, (255, 255, 255),
                        (bar_x, bar_y, bar_width, bar_height), 2)
                        
        phase_text = self.game.font_small.render(f"Phase {self.phase}", True, (255, 255, 255))
        screen.blit(phase_text, (bar_x + bar_width - 80, bar_y - 25))
        
        boss_name = self.game.font_medium.render(f"BOSS: Level {self.level}", True, (255, 255, 0))
        screen.blit(boss_name, (bar_x, bar_y - 40))

class BossManager:
    def __init__(self, game):
        self.game = game
        self.bosses = pygame.sprite.Group()
        self.active = False
        self.warning_timer = 0
        self.intro_timer = 0
        self.boss_level = 0
        
    def spawn_boss(self, level):
        """Spawn a boss for the given level"""
        self.boss_level = level
        self.active = True
        self.warning_timer = 3.0
        self.intro_timer = 2.0
        
        self.game.play_music('boss')
        self.game.play_sound('boss_alarm')
        
    def update(self, dt):
        """Update boss system"""
        if not self.active:
            return
            
        if self.warning_timer > 0:
            self.warning_timer -= dt
            if self.warning_timer <= 0:
                boss = Boss(self.game, self.boss_level)
                self.bosses.add(boss)
                
        if self.intro_timer > 0:
            self.intro_timer -= dt
            
        self.bosses.update(dt)
        
        if len(self.bosses) == 0 and self.active and self.warning_timer <= 0:
            self.active = False
            self.game.level_manager.boss_defeated()
            self.game.play_music('game')
            
    def draw_warning(self, screen):
        """Draw boss warning message"""
        if self.warning_timer > 0:
            alpha = int(255 * (abs(math.sin(pygame.time.get_ticks() * 0.01))))
            warning_text = self.game.font_large.render("BOSS APPROACHING!", True, (255, 0, 0))
            warning_rect = warning_text.get_rect(center=(self.game.settings.width // 2,
                                                         self.game.settings.height // 2))
            
            overlay = pygame.Surface((self.game.settings.width, self.game.settings.height))
            overlay.set_alpha(alpha // 2)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))
            screen.blit(warning_text, warning_rect)
            
    def draw(self, screen):
        """Draw bosses"""
        self.draw_warning(screen)
        for boss in self.bosses:
            screen.blit(boss.image, boss.rect)
            boss.draw_health_bar(screen)