"""
Enemy system - All enemy types and spawn management
"""

import pygame
import math
import random
from enum import Enum

class EnemyType(Enum):
    BASIC = 1
    FAST = 2
    HEAVY = 3
    HELICOPTER = 4
    MISSILE_CARRIER = 5
    KAMIKAZE = 6
    STEALTH = 7
    MINI_BOSS = 8

class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, enemy_type, x, y):
        super().__init__()
        self.game = game
        self.enemy_type = enemy_type
        self.set_stats()
        
        # Load enemy image
        self.image = None
        self.original_image = None
        self.load_image()
        
        # Position
        if self.image:
            self.rect = self.image.get_rect()
        else:
            self.rect = pygame.Rect(x, y, self.width, self.height)
        self.rect.x = x
        self.rect.y = y
        
        # Movement
        self.velocity_x = 0
        self.velocity_y = self.speed
        
        # Attack - shoot DOWNWARD
        self.shoot_timer = random.uniform(0, self.shoot_delay)
        self.attack_pattern = random.choice(['straight', 'spread'])
        
        # Animation
        self.animation_frame = 0
        
    def load_image(self):
        """Load enemy image from centralized system"""
        type_to_key = {
            EnemyType.BASIC: 'enemy_basic',
            EnemyType.FAST: 'enemy_fast',
            EnemyType.HEAVY: 'enemy_heavy',
            EnemyType.HELICOPTER: 'enemy_helicopter',
            EnemyType.MISSILE_CARRIER: 'enemy_missile',
            EnemyType.KAMIKAZE: 'enemy_kamikaze',
            EnemyType.STEALTH: 'enemy_stealth',
            EnemyType.MINI_BOSS: 'enemy_miniboss'
        }
        
        key = type_to_key.get(self.enemy_type, 'enemy_basic')
        self.original_image = self.game.images.get(key)
        
        if self.original_image:
            self.image = pygame.transform.scale(
                self.original_image, (self.width, self.height)
            )
        else:
            self.create_placeholder_image()
            
    def create_placeholder_image(self):
        """Create a colored placeholder for missing enemy images"""
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
        if self.enemy_type == EnemyType.BASIC:
            pygame.draw.rect(self.image, (255, 0, 0), self.image.get_rect())
        elif self.enemy_type == EnemyType.FAST:
            pygame.draw.polygon(self.image, (255, 100, 0), [
                (self.width // 2, 0),
                (self.width, self.height),
                (0, self.height)
            ])
        elif self.enemy_type == EnemyType.HEAVY:
            pygame.draw.ellipse(self.image, (150, 0, 0), self.image.get_rect())
        else:
            pygame.draw.rect(self.image, (255, 0, 0), self.image.get_rect())
            
        # Add eyes
        pygame.draw.circle(self.image, (255, 255, 255), (self.width // 3, self.height // 3), 5)
        pygame.draw.circle(self.image, (255, 255, 255), (2 * self.width // 3, self.height // 3), 5)
        pygame.draw.circle(self.image, (0, 0, 0), (self.width // 3, self.height // 3), 2)
        pygame.draw.circle(self.image, (0, 0, 0), (2 * self.width // 3, self.height // 3), 2)
        
    def set_stats(self):
        """Set enemy stats based on type"""
        if self.enemy_type == EnemyType.BASIC:
            self.health = 20
            self.max_health = 20
            self.damage = 10
            self.speed = 80
            self.width = 35
            self.height = 35
            self.score_value = 100
            self.shoot_delay = 1.5
            self.bullet_type = 'normal'
            
        elif self.enemy_type == EnemyType.FAST:
            self.health = 15
            self.max_health = 15
            self.damage = 8
            self.speed = 180
            self.width = 30
            self.height = 30
            self.score_value = 150
            self.shoot_delay = 1.0
            self.bullet_type = 'normal'
            
        elif self.enemy_type == EnemyType.HEAVY:
            self.health = 80
            self.max_health = 80
            self.damage = 20
            self.speed = 40
            self.width = 50
            self.height = 50
            self.score_value = 300
            self.shoot_delay = 2.0
            self.bullet_type = 'heavy'
            
        elif self.enemy_type == EnemyType.HELICOPTER:
            self.health = 40
            self.max_health = 40
            self.damage = 12
            self.speed = 60
            self.width = 40
            self.height = 30
            self.score_value = 200
            self.shoot_delay = 0.8
            self.bullet_type = 'normal'
            
        elif self.enemy_type == EnemyType.MISSILE_CARRIER:
            self.health = 50
            self.max_health = 50
            self.damage = 25
            self.speed = 50
            self.width = 45
            self.height = 40
            self.score_value = 250
            self.shoot_delay = 3.0
            self.bullet_type = 'missile'
            
        elif self.enemy_type == EnemyType.KAMIKAZE:
            self.health = 10
            self.max_health = 10
            self.damage = 40
            self.speed = 200
            self.width = 30
            self.height = 30
            self.score_value = 200
            self.shoot_delay = float('inf')
            self.bullet_type = 'none'
            
        elif self.enemy_type == EnemyType.STEALTH:
            self.health = 30
            self.max_health = 30
            self.damage = 15
            self.speed = 100
            self.width = 35
            self.height = 35
            self.score_value = 250
            self.shoot_delay = 1.2
            self.bullet_type = 'normal'
            self.stealth = True
            
        elif self.enemy_type == EnemyType.MINI_BOSS:
            self.health = 200
            self.max_health = 200
            self.damage = 30
            self.speed = 30
            self.width = 70
            self.height = 70
            self.score_value = 1000
            self.shoot_delay = 1.0
            self.bullet_type = 'spread'
            
        # Apply difficulty multipliers
        self.health = int(self.health * self.game.settings.enemy_health_multiplier)
        self.max_health = self.health
        self.damage = int(self.damage * self.game.settings.enemy_damage_multiplier)
        
    def update(self, dt):
        """Update enemy position and behavior"""
        self.rect.x += self.velocity_x * dt
        self.rect.y += self.velocity_y * dt
        
        self.update_movement_pattern(dt)
        
        # Shoot DOWNWARD at player
        if self.shoot_timer <= 0:
            self.shoot()
            self.shoot_timer = self.shoot_delay
        else:
            self.shoot_timer -= dt
            
        self.animation_frame += dt * 10
        
        # Apply stealth flicker
        if hasattr(self, 'stealth') and self.stealth and self.image:
            if int(pygame.time.get_ticks() * 0.01) % 4 < 2:
                self.image.set_alpha(128)
            else:
                self.image.set_alpha(255)
                
        if (self.rect.top > self.game.settings.height + 100 or 
            self.rect.bottom < -100 or
            self.rect.right < -100 or 
            self.rect.left > self.game.settings.width + 100):
            self.kill()
            
    def update_movement_pattern(self, dt):
        """Update special movement patterns"""
        if self.enemy_type == EnemyType.HELICOPTER:
            self.velocity_x = 50 * math.sin(pygame.time.get_ticks() * 0.002)
            
        elif self.enemy_type == EnemyType.KAMIKAZE:
            if self.game.player:
                dx = self.game.player.rect.centerx - self.rect.centerx
                dy = self.game.player.rect.centery - self.rect.centery
                distance = math.sqrt(dx*dx + dy*dy)
                if distance > 0:
                    self.velocity_x = (dx / distance) * self.speed
                    self.velocity_y = (dy / distance) * self.speed
                
    def shoot(self):
        """Shoot bullets DOWNWARD toward player"""
        if self.bullet_type == 'none':
            return
            
        if self.enemy_type == EnemyType.MISSILE_CARRIER:
            self.game.weapon_system.fire_enemy_missile(
                self.rect.centerx, self.rect.bottom, self.game.player
            )
        elif self.bullet_type == 'spread':
            # Spread shot DOWNWARD
            for angle in [80, 90, 100]:
                self.game.weapon_system.fire_enemy_bullet(
                    self.rect.centerx, self.rect.bottom, angle
                )
        else:
            # Normal shot - straight DOWN (90 degrees)
            angle = 90
                
            self.game.weapon_system.fire_enemy_bullet(
                self.rect.centerx, self.rect.bottom, angle
            )
            
        self.game.play_sound('shoot')
        
    def hit(self, damage):
        """Handle enemy being hit"""
        self.health -= damage
        if self.health <= 0:
            self.kill()
            return True
        return False

class EnemyManager:
    def __init__(self, game):
        self.game = game
        self.enemies = pygame.sprite.Group()
        self.spawn_timer = 0
        self.spawn_delay = 1.0
        
    def update(self, dt):
        """Update all enemies"""
        self.enemies.update(dt)
        
        if self.spawn_timer <= 0:
            self.spawn_enemy()
            self.spawn_timer = self.spawn_delay / self.game.settings.enemy_spawn_multiplier
        else:
            self.spawn_timer -= dt
            
    def spawn_enemy(self):
        """Spawn a random enemy type"""
        level = self.game.level_manager.current_level
        available_types = [EnemyType.BASIC]
        
        if level >= 5:
            available_types.append(EnemyType.FAST)
        if level >= 10:
            available_types.append(EnemyType.HEAVY)
        if level >= 15:
            available_types.append(EnemyType.HELICOPTER)
        if level >= 20:
            available_types.append(EnemyType.MISSILE_CARRIER)
        if level >= 25:
            available_types.append(EnemyType.KAMIKAZE)
        if level >= 30:
            available_types.append(EnemyType.STEALTH)
        if level >= 40 and level % 10 == 0:
            available_types.append(EnemyType.MINI_BOSS)
            
        enemy_type = random.choice(available_types)
        
        x = random.randint(50, self.game.settings.width - 50)
        y = -random.randint(20, 100)
        
        enemy = Enemy(self.game, enemy_type, x, y)
        self.enemies.add(enemy)
        
    def is_empty(self):
        """Check if no enemies remain"""
        return len(self.enemies) == 0
        
    def clear(self):
        """Clear all enemies"""
        self.enemies.empty()
        
    def draw(self, screen):
        """Draw all enemies"""
        # Draw health bars for enemies
        for enemy in self.enemies:
            if enemy.health < enemy.max_health:
                bar_width = enemy.rect.width
                bar_height = 4
                health_percent = enemy.health / enemy.max_health
                pygame.draw.rect(screen, (255, 0, 0),
                               (enemy.rect.x, enemy.rect.y - 8, bar_width, bar_height))
                pygame.draw.rect(screen, (0, 255, 0),
                               (enemy.rect.x, enemy.rect.y - 8, bar_width * health_percent, bar_height))
        
        # Draw enemies using sprite group
        self.enemies.draw(screen)