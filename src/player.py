"""
Player class - Controls player aircraft
"""

import pygame
import math
import random

class Player(pygame.sprite.Sprite):
    def __init__(self, game, weapon_system):
        super().__init__()
        self.game = game
        self.settings = game.settings
        self.weapon_system = weapon_system
        
        # Player stats
        self.max_health = 100
        self.health = 100
        self.max_shield = 50
        self.shield = 0
        self.lives = 1  # No respawn, just 1 life
        self.missiles = 5
        self.max_missiles = 10
        self.speed = 400  # pixels per second
        self.base_speed = 400
        
        # Buffs
        self.shield_active = 0
        self.speed_boost_active = 0
        self.magnet_active = 0
        self.invincible_timer = 0
        
        # Load player image
        self.original_image = None
        self.image = None
        self.load_image()
        
        # Set position
        if self.image:
            self.rect = self.image.get_rect()
            self.width = self.image.get_width()
            self.height = self.image.get_height()
        else:
            self.width = 40
            self.height = 40
            self.rect = pygame.Rect(0, 0, self.width, self.height)
            
        self.rect.centerx = self.settings.width // 2
        self.rect.bottom = self.settings.height - 80
        
        # Movement - only left/right
        self.velocity_x = 0
        
        # Cooldowns
        self.shoot_cooldown = 0
        self.missile_cooldown = 0
        
        # Animation
        self.engine_particles = []
        
    def load_image(self):
        """Load player image from centralized system"""
        self.original_image = self.game.images.get('player')
        if self.original_image:
            self.image = self.original_image
            print("Player image loaded from central system")
        else:
            print("No player image found, using default")
            self.original_image = None
            # Create default player image
            self.image = pygame.Surface((40, 40), pygame.SRCALPHA)
            pygame.draw.polygon(self.image, (0, 255, 0), [(20, 0), (0, 40), (40, 40)])
            pygame.draw.polygon(self.image, (0, 200, 0), [(20, 5), (5, 35), (35, 35)])
        
    def handle_event(self, event):
        """Handle player input events"""
        if event.type == pygame.KEYDOWN:
            if event.key in self.settings.key_shoot:
                self.shoot()
            elif event.key in self.settings.key_missile:
                self.fire_missile()
                
    def update(self, dt):
        """Update player state"""
        # Update cooldowns
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= dt
        if self.missile_cooldown > 0:
            self.missile_cooldown -= dt
        if self.invincible_timer > 0:
            self.invincible_timer -= dt
            
        # Update buff timers
        if self.shield_active > 0:
            self.shield_active -= dt
            if self.shield_active <= 0:
                self.shield = 0
        if self.speed_boost_active > 0:
            self.speed_boost_active -= dt
            if self.speed_boost_active <= 0:
                self.speed = self.base_speed
        if self.magnet_active > 0:
            self.magnet_active -= dt
            if self.magnet_active <= 0 and hasattr(self, 'magnet_radius'):
                delattr(self, 'magnet_radius')
                
        # Handle input - ONLY LEFT AND RIGHT movement
        keys = pygame.key.get_pressed()
        self.velocity_x = 0
        
        if any(keys[key] for key in self.settings.key_left):
            self.velocity_x = -self.speed
        if any(keys[key] for key in self.settings.key_right):
            self.velocity_x = self.speed
            
        # Update position (X only)
        self.rect.x += self.velocity_x * dt
        
        # Keep player on screen horizontally
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.settings.width:
            self.rect.right = self.settings.width
        
        # Continuous shooting
        if any(keys[key] for key in self.settings.key_shoot):
            self.shoot()
            
        # Update engine particles
        self.update_engine_particles(dt)
        
        # Magnet effect
        if hasattr(self, 'magnet_active') and self.magnet_active > 0:
            self.attract_powerups()
            
    def shoot(self):
        """Shoot primary weapon"""
        if self.shoot_cooldown <= 0:
            self.weapon_system.shoot(self.rect.centerx, self.rect.top)
            self.shoot_cooldown = self.weapon_system.fire_rate
            self.game.bullets_fired += 1
            self.game.play_sound('shoot')
            
    def fire_missile(self):
        """Fire missile weapon"""
        if self.missiles > 0 and self.missile_cooldown <= 0:
            self.weapon_system.fire_missile(self.rect.centerx, self.rect.top)
            self.missiles -= 1
            self.missile_cooldown = 1.0
            self.game.play_sound('missile')
            
    def take_damage(self, damage):
        """Handle player taking damage"""
        if self.invincible_timer > 0:
            return
            
        if self.shield > 0:
            shield_damage = min(damage, self.shield)
            self.shield -= shield_damage
            damage -= shield_damage
            
        if damage > 0:
            self.health -= damage
            self.invincible_timer = 1.0
            self.game.play_sound('hit')
            self.game.effect_system.add_flash()
            
            if self.health <= 0:
                self.die()
                
    def heal(self, amount):
        """Heal player"""
        self.health = min(self.max_health, self.health + amount)
        
    def activate_shield(self, duration):
        """Activate shield powerup"""
        self.shield = self.max_shield
        self.shield_active = duration
        
    def activate_speed_boost(self, duration):
        """Activate speed boost powerup"""
        self.speed = self.base_speed * 1.5
        self.speed_boost_active = duration
        
    def activate_magnet(self, duration):
        """Activate magnet powerup"""
        self.magnet_active = duration
        self.magnet_radius = 200
        
    def die(self):
        """Handle player death - go to game over screen"""
        self.game.game_over()
        
    def update_engine_particles(self, dt):
        """Update engine particle effects"""
        for _ in range(2):
            particle = {
                'x': self.rect.centerx + (random.randint(-5, 5)),
                'y': self.rect.bottom - 5,
                'vx': random.uniform(-30, 30),
                'vy': random.uniform(50, 150),
                'life': 0.5,
                'size': random.randint(2, 4)
            }
            self.engine_particles.append(particle)
                
        for particle in self.engine_particles[:]:
            particle['x'] += particle['vx'] * dt
            particle['y'] += particle['vy'] * dt
            particle['life'] -= dt
            if particle['life'] <= 0:
                self.engine_particles.remove(particle)
                
    def attract_powerups(self):
        """Attract nearby powerups"""
        if not hasattr(self, 'magnet_radius'):
            return
            
        for powerup in self.game.weapon_system.powerups:
            dx = powerup.rect.centerx - self.rect.centerx
            dy = powerup.rect.centery - self.rect.centery
            distance = math.sqrt(dx*dx + dy*dy)
            
            if distance < self.magnet_radius and distance > 5:
                angle = math.atan2(dy, dx)
                powerup.rect.x += math.cos(angle) * 300 * self.game.dt
                powerup.rect.y += math.sin(angle) * 300 * self.game.dt
                
    def draw(self, screen):
        """Draw player"""
        # Draw engine particles
        for particle in self.engine_particles:
            alpha = int(255 * (particle['life'] / 0.5))
            r = min(255, max(0, 255))
            g = min(255, max(0, 165 - alpha))
            b = min(255, max(0, 0))
            color = (r, g, b)
            
            pygame.draw.circle(screen, color, 
                             (int(particle['x']), int(particle['y'])), 
                             particle['size'])
                             
        # Draw player image (no rotation)
        if self.image:
            if self.invincible_timer > 0 and int(self.invincible_timer * 10) % 2:
                # Make semi-transparent when invincible
                temp_image = self.image.copy()
                temp_image.set_alpha(128)
                screen.blit(temp_image, self.rect)
            else:
                screen.blit(self.image, self.rect)
        else:
            # Draw simple player shape
            points = [
                (self.rect.centerx, self.rect.top),
                (self.rect.left + 5, self.rect.bottom - 10),
                (self.rect.centerx, self.rect.bottom - 5),
                (self.rect.right - 5, self.rect.bottom - 10)
            ]
            pygame.draw.polygon(screen, (0, 255, 0), points)
            
        # Draw shield effect
        if self.shield > 0:
            shield_surf = pygame.Surface((self.rect.width + 20, self.rect.height + 20), 
                                        pygame.SRCALPHA)
            pygame.draw.ellipse(shield_surf, (0, 100, 255, 100), 
                               shield_surf.get_rect())
            screen.blit(shield_surf, (self.rect.x - 10, self.rect.y - 10))