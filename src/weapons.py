"""
Weapon system - Bullets, missiles, and powerups
"""

import pygame
import math
import random

class Bullet(pygame.sprite.Sprite):
    def __init__(self, game, x, y, angle, speed, damage, owner, is_missile=False):
        super().__init__()
        self.game = game
        self.angle = angle  # Angle in degrees (0 = right, 90 = down, -90 = up)
        self.speed = speed
        self.damage = damage
        self.owner = owner  # "player" or "enemy"
        self.is_missile = is_missile
        
        # Convert angle to radians and calculate velocity
        rad = math.radians(angle)
        self.velocity_x = math.cos(rad) * speed
        self.velocity_y = math.sin(rad) * speed
        
        # Size based on type
        if is_missile:
            self.width = 10
            self.height = 20
        else:
            self.width = 5
            self.height = 10
            
        self.rect = pygame.Rect(x - self.width // 2, y - self.height // 2, 
                               self.width, self.height)
                               
        # Homing missile properties
        if is_missile and owner == "player":
            self.target = None
            self.find_target()
            
        # Load image from centralized image system
        self.image = self.load_image()
        if not self.image:
            self.image = self.create_placeholder_image()
        
    def load_image(self):
        """Load bullet/missile image from centralized image system"""
        if self.is_missile:
            if self.owner == "player":
                return self.game.images.get('missile_player')
            else:
                return self.game.images.get('missile_enemy')
        else:
            if self.owner == "player":
                return self.game.images.get('bullet_player')
            else:
                return self.game.images.get('bullet_enemy')
                
    def create_placeholder_image(self):
        """Create placeholder if image not found"""
        if self.is_missile:
            surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            if self.owner == "player":
                # Player missile - orange
                pygame.draw.ellipse(surf, (255, 100, 0), surf.get_rect())
                pygame.draw.polygon(surf, (255, 0, 0), [
                    (self.width // 2, 0),
                    (self.width // 2 + 3, self.height // 2),
                    (self.width // 2, self.height),
                    (self.width // 2 - 3, self.height // 2)
                ])
            else:
                # Enemy missile - red
                pygame.draw.ellipse(surf, (200, 0, 0), surf.get_rect())
                pygame.draw.polygon(surf, (100, 0, 0), [
                    (self.width // 2, 0),
                    (self.width // 2 + 3, self.height // 2),
                    (self.width // 2, self.height),
                    (self.width // 2 - 3, self.height // 2)
                ])
            return surf
        else:
            # Regular bullet
            surf = pygame.Surface((self.width, self.height))
            if self.owner == "player":
                surf.fill((255, 255, 0))  # Yellow for player
            else:
                surf.fill((255, 0, 0))    # Red for enemy
            return surf
            
    def find_target(self):
        """Find nearest enemy for homing missile"""
        closest_distance = float('inf')
        self.target = None
        for enemy in self.game.enemy_manager.enemies:
            dx = enemy.rect.centerx - self.rect.centerx
            dy = enemy.rect.centery - self.rect.centery
            distance = math.sqrt(dx*dx + dy*dy)
            if distance < closest_distance:
                closest_distance = distance
                self.target = enemy
                
    def update(self, dt):
        """Update bullet position"""
        if self.is_missile and self.owner == "player" and self.target:
            # Homing behavior
            if self.target and self.target.alive():
                dx = self.target.rect.centerx - self.rect.centerx
                dy = self.target.rect.centery - self.rect.centery
                if dx != 0 or dy != 0:
                    target_angle = math.degrees(math.atan2(dy, dx))
                    
                    # Smooth rotation towards target
                    angle_diff = target_angle - self.angle
                    if angle_diff > 180:
                        angle_diff -= 360
                    elif angle_diff < -180:
                        angle_diff += 360
                        
                    self.angle += angle_diff * dt * 5
                    
                    # Update velocity
                    rad = math.radians(self.angle)
                    self.velocity_x = math.cos(rad) * self.speed
                    self.velocity_y = math.sin(rad) * self.speed
            elif self.target and not self.target.alive():
                # Target died, find new target
                self.find_target()
                
        # Update position
        self.rect.x += self.velocity_x * dt
        self.rect.y += self.velocity_y * dt
        
        # Check if off screen
        if (self.rect.right < -50 or self.rect.left > self.game.settings.width + 50 or
            self.rect.bottom < -50 or self.rect.top > self.game.settings.height + 50):
            self.kill()
            
    def draw(self, screen):
        """Draw bullet"""
        if self.image:
            if self.is_missile:
                # Rotate missile image to face direction
                rotated = pygame.transform.rotate(self.image, -self.angle)
                rect = rotated.get_rect(center=self.rect.center)
                screen.blit(rotated, rect)
            else:
                screen.blit(self.image, self.rect)
                
                # Add glow effect for player bullets
                if self.owner == "player":
                    glow = pygame.Surface((self.width * 3, self.height * 3), pygame.SRCALPHA)
                    pygame.draw.ellipse(glow, (255, 255, 0, 100), glow.get_rect())
                    screen.blit(glow, (self.rect.centerx - glow.get_width() // 2,
                                      self.rect.centery - glow.get_height() // 2))

class Powerup(pygame.sprite.Sprite):
    def __init__(self, game, x, y, powerup_type):
        super().__init__()
        self.game = game
        self.type = powerup_type
        self.width = 25
        self.height = 25
        self.rect = pygame.Rect(x, y, self.width, self.height)
        
        # Movement
        self.velocity_y = 50
        self.rotation = 0
        
        # Load image from centralized system
        self.image = self.load_image()
        if not self.image:
            self.image = self.create_placeholder_image()
        
    def load_image(self):
        """Load powerup image from centralized system"""
        image_key = f'powerup_{self.type}'
        return self.game.images.get(image_key)
        
    def create_placeholder_image(self):
        """Create placeholder powerup image"""
        surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
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
        
        color = colors.get(self.type, (255, 255, 255))
        
        # Draw star shape
        center = (self.width // 2, self.height // 2)
        for i in range(5):
            angle = i * 72 - 90
            rad = math.radians(angle)
            x = center[0] + math.cos(rad) * self.width // 3
            y = center[1] + math.sin(rad) * self.height // 3
            pygame.draw.circle(surf, color, (int(x), int(y)), 3)
            
        pygame.draw.circle(surf, color, center, self.width // 3, 2)
        
        return surf
        
    def update(self, dt):
        """Update powerup position"""
        self.rect.y += self.velocity_y * dt
        self.rotation += dt * 180
        
        if self.rect.top > self.game.settings.height:
            self.kill()
            
    def draw(self, screen):
        """Draw powerup"""
        if self.image:
            rotated = pygame.transform.rotate(self.image, self.rotation)
            rect = rotated.get_rect(center=self.rect.center)
            screen.blit(rotated, rect)
        else:
            rotated = pygame.transform.rotate(self.image, self.rotation)
            rect = rotated.get_rect(center=self.rect.center)
            screen.blit(rotated, rect)

class WeaponSystem:
    def __init__(self, game):
        self.game = game
        self.bullets = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        
        # Weapon stats
        self.weapon_type = "single"  # single, double, triple, laser
        self.fire_rate = 0.15
        self.damage = 20
        self.weapon_timer = 0  # For temporary weapon upgrades
        
    def shoot(self, x, y):
        """
        Shoot from player position - bullets go UP (angle = -90)
        Angle reference: 0 = right, 90 = down, -90 = up, 180 = left
        """
        if self.weapon_type == "single":
            # Single bullet straight UP
            bullet = Bullet(self.game, x, y, -90, 500, self.damage, "player")
            self.bullets.add(bullet)
            
        elif self.weapon_type == "double":
            # Two bullets slightly spread UP
            bullet1 = Bullet(self.game, x - 15, y, -90, 500, self.damage, "player")
            bullet2 = Bullet(self.game, x + 15, y, -90, 500, self.damage, "player")
            self.bullets.add(bullet1, bullet2)
            
        elif self.weapon_type == "triple":
            # Three bullets spread UP
            bullet1 = Bullet(self.game, x - 20, y, -90, 500, self.damage, "player")
            bullet2 = Bullet(self.game, x, y, -90, 500, self.damage, "player")
            bullet3 = Bullet(self.game, x + 20, y, -90, 500, self.damage, "player")
            self.bullets.add(bullet1, bullet2, bullet3)
            
        elif self.weapon_type == "laser":
            # Laser beam (multiple bullets in line UP)
            for i in range(5):
                bullet = Bullet(self.game, x + (i - 2) * 8, y, -90, 800, self.damage * 1.5, "player")
                self.bullets.add(bullet)
                
    def fire_missile(self, x, y):
        """Fire homing missile from player - goes UP initially"""
        if hasattr(self.game.player, 'missiles') and self.game.player.missiles > 0:
            missile = Bullet(self.game, x, y, -90, 350, 50, "player", is_missile=True)
            self.bullets.add(missile)
            self.game.player.missiles -= 1
            self.game.play_sound('missile')
            return True
        return False
        
    def fire_enemy_bullet(self, x, y, angle, is_boss=False):
        """
        Fire enemy bullet - should go DOWN (angle around 90)
        Angle reference: 90 = straight down
        """
        damage = 10 if not is_boss else 20
        # Ensure angle is downward (between 45 and 135 degrees)
        if angle < 45:
            angle = 45
        if angle > 135:
            angle = 135
        bullet = Bullet(self.game, x, y, angle, 200, damage, "enemy")
        self.bullets.add(bullet)
        
    def fire_enemy_missile(self, x, y, target, is_boss=False):
        """Fire enemy homing missile - goes DOWN initially"""
        damage = 25 if not is_boss else 40
        missile = Bullet(self.game, x, y, 90, 150, damage, "enemy", is_missile=True)
        missile.target = target
        self.bullets.add(missile)
        
    def spawn_powerup(self, x, y):
        """Spawn a random powerup"""
        powerup_types = ['double', 'triple', 'laser', 'shield', 'health', 
                         'missile', 'speed', 'magnet', 'life']
        # Weighted random - some powerups are rarer
        weights = [15, 10, 5, 10, 15, 15, 10, 10, 5]  # life and laser are rare
        powerup_type = random.choices(powerup_types, weights=weights)[0]
        powerup = Powerup(self.game, x, y, powerup_type)
        self.powerups.add(powerup)
        
    def upgrade_weapon(self, weapon_type, duration=10.0):
        """Upgrade to new weapon type for duration"""
        self.weapon_type = weapon_type
        self.weapon_timer = duration
        
    def reset_weapon(self):
        """Reset to default weapon"""
        self.weapon_type = "single"
        self.weapon_timer = 0
        
    def update(self, dt):
        """Update all weapons and powerups"""
        # Update weapon timer
        if self.weapon_timer > 0:
            self.weapon_timer -= dt
            if self.weapon_timer <= 0:
                self.reset_weapon()
                
        # Update bullets and powerups
        self.bullets.update(dt)
        self.powerups.update(dt)
        
    def draw(self, screen):
        """Draw all weapons and powerups"""
        self.bullets.draw(screen)
        self.powerups.draw(screen)