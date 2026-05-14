"""
Effects system - Particle effects, screen shake, and visual effects
"""

import pygame
import math
import random

class Particle:
    def __init__(self, x, y, vx, vy, color, size, life):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color  # RGB tuple
        self.size = size
        self.life = life
        self.max_life = life
        
    def update(self, dt):
        """Update particle"""
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.vy += 300 * dt  # Gravity
        self.life -= dt
        return self.life > 0

class EffectSystem:
    def __init__(self, game):
        self.game = game
        self.particles = []
        self.screen_shake = 0
        self.flash_alpha = 0
        
    def add_explosion(self, position):
        """Add explosion effect"""
        for _ in range(30):
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(50, 200)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            
            color = random.choice([(255, 100, 0), (255, 50, 0), (255, 150, 0)])
            size = random.randint(3, 6)
            life = random.uniform(0.5, 1.0)
            
            particle = Particle(position[0], position[1], vx, vy, color, size, life)
            self.particles.append(particle)
            
    def add_large_explosion(self, position):
        """Add larger explosion effect for bosses"""
        for _ in range(60):
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(100, 300)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            
            color = random.choice([(255, 100, 0), (255, 50, 0), (255, 150, 0), (255, 200, 0)])
            size = random.randint(5, 10)
            life = random.uniform(0.8, 1.5)
            
            particle = Particle(position[0], position[1], vx, vy, color, size, life)
            self.particles.append(particle)
            
    def add_particle(self, x, y, vx, vy):
        """Add single particle"""
        color = (255, 200, 0)
        size = random.randint(2, 4)
        life = random.uniform(0.3, 0.8)
        particle = Particle(x, y, vx, vy, color, size, life)
        self.particles.append(particle)
        
    def add_screen_shake(self, intensity):
        """Add screen shake effect"""
        self.screen_shake = max(self.screen_shake, intensity)
        
    def add_flash(self):
        """Add flash effect"""
        self.flash_alpha = 100
        
    def add_smoke(self, x, y):
        """Add smoke effect"""
        for _ in range(5):
            vx = random.uniform(-20, 20)
            vy = random.uniform(-50, -20)
            color = (100, 100, 100)
            size = random.randint(3, 6)
            life = random.uniform(0.5, 1.0)
            particle = Particle(x, y, vx, vy, color, size, life)
            self.particles.append(particle)
            
    def add_trail(self, x, y, color):
        """Add trail effect for fast moving objects"""
        vx = random.uniform(-10, 10)
        vy = random.uniform(-10, 10)
        size = random.randint(2, 3)
        life = random.uniform(0.2, 0.4)
        particle = Particle(x, y, vx, vy, color, size, life)
        self.particles.append(particle)
        
    def update(self, dt):
        """Update all effects"""
        # Update particles
        for particle in self.particles[:]:
            if not particle.update(dt):
                self.particles.remove(particle)
                
        # Update screen shake
        if self.screen_shake > 0:
            self.screen_shake -= dt * 5
            if self.screen_shake < 0:
                self.screen_shake = 0
                
        # Update flash
        if self.flash_alpha > 0:
            self.flash_alpha -= dt * 500
            if self.flash_alpha < 0:
                self.flash_alpha = 0
                
    def draw(self, screen):
        """Draw all effects"""
        # Draw particles
        for particle in self.particles:
            # Ensure color values are valid
            r = min(255, max(0, particle.color[0]))
            g = min(255, max(0, particle.color[1]))
            b = min(255, max(0, particle.color[2]))
            
            # Calculate alpha (fade out as life decreases)
            alpha = int(255 * (particle.life / particle.max_life))
            alpha = min(255, max(0, alpha))
            
            # Create surface with alpha for particle
            particle_surf = pygame.Surface((particle.size * 2, particle.size * 2), pygame.SRCALPHA)
            
            # Draw with alpha on the surface
            # Outer glow for explosion particles
            if particle.size > 5:
                pygame.draw.circle(particle_surf, (r, g, b, alpha // 2), 
                                  (particle.size, particle.size), particle.size + 2)
            
            # Main particle
            pygame.draw.circle(particle_surf, (r, g, b, alpha), 
                              (particle.size, particle.size), particle.size)
            
            # Inner bright core for fire particles
            if particle.color[0] > 200 and particle.color[1] < 150:
                pygame.draw.circle(particle_surf, (255, 255, 200, alpha), 
                                  (particle.size, particle.size), particle.size // 2)
            
            screen.blit(particle_surf, (int(particle.x - particle.size), 
                                       int(particle.y - particle.size)))
            
        # Apply screen shake
        if self.screen_shake > 0:
            shake_intensity = int(self.screen_shake * 10)
            shake_x = random.randint(-shake_intensity, shake_intensity)
            shake_y = random.randint(-shake_intensity, shake_intensity)
            
            # Apply scroll with bounds checking to avoid errors
            if abs(shake_x) < screen.get_width() and abs(shake_y) < screen.get_height():
                try:
                    screen.scroll(shake_x, shake_y)
                except:
                    pass  # Ignore scroll errors
                
        # Apply flash effect
        if self.flash_alpha > 0:
            flash = pygame.Surface((self.game.settings.width, self.game.settings.height))
            flash_alpha = min(255, max(0, int(self.flash_alpha)))
            flash.set_alpha(flash_alpha)
            flash.fill((255, 255, 255))
            screen.blit(flash, (0, 0))
            
    def clear(self):
        """Clear all particles"""
        self.particles.clear()
        self.screen_shake = 0
        self.flash_alpha = 0