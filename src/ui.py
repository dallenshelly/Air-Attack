"""
UI System - All user interface elements
"""

import pygame

class UIManager:
    def __init__(self, game):
        self.game = game
        
    def draw(self, screen):
        """Draw all UI elements"""
        self.draw_health_bar(screen)
        self.draw_shield_bar(screen)
        self.draw_score(screen)
        self.draw_level(screen)
        self.draw_lives(screen)
        self.draw_missiles(screen)
        self.draw_combo(screen)
        self.draw_fps(screen)
        
        # Draw boss health bar if boss active
        if self.game.boss_manager.active and self.game.boss_manager.bosses:
            for boss in self.game.boss_manager.bosses:
                self.draw_boss_health_bar(screen, boss)
                
    def draw_health_bar(self, screen):
        """Draw player health bar"""
        bar_width = 300
        bar_height = 20
        x = 20
        y = 20
        
        # Background
        pygame.draw.rect(screen, (100, 0, 0), (x, y, bar_width, bar_height))
        
        # Health
        health_percent = self.game.player.health / self.game.player.max_health
        pygame.draw.rect(screen, (0, 255, 0), 
                        (x, y, bar_width * health_percent, bar_height))
        
        # Border
        pygame.draw.rect(screen, (255, 255, 255), (x, y, bar_width, bar_height), 2)
        
        # Text
        health_text = self.game.font_small.render(f"Health: {self.game.player.health}", 
                                                  True, (255, 255, 255))
        screen.blit(health_text, (x, y - 20))
        
    def draw_shield_bar(self, screen):
        """Draw player shield bar"""
        if self.game.player.shield > 0:
            bar_width = 300
            bar_height = 15
            x = 20
            y = 55
            
            # Background
            pygame.draw.rect(screen, (50, 50, 100), (x, y, bar_width, bar_height))
            
            # Shield
            shield_percent = self.game.player.shield / self.game.player.max_shield
            pygame.draw.rect(screen, (0, 100, 255), 
                            (x, y, bar_width * shield_percent, bar_height))
            
            # Border
            pygame.draw.rect(screen, (255, 255, 255), (x, y, bar_width, bar_height), 1)
            
            # Text
            shield_text = self.game.font_tiny.render("Shield", True, (255, 255, 255))
            screen.blit(shield_text, (x, y - 15))
            
    def draw_score(self, screen):
        """Draw current score and high score"""
        score_text = self.game.font_medium.render(f"Score: {self.game.score}", 
                                                   True, (255, 255, 255))
        screen.blit(score_text, (self.game.settings.width - 250, 20))
        
        high_score_text = self.game.font_small.render(f"High: {self.game.player_data.get('high_score', 0)}", 
                                                       True, (255, 255, 0))
        screen.blit(high_score_text, (self.game.settings.width - 250, 60))
        
    def draw_level(self, screen):
        """Draw current level"""
        level_text = self.game.font_medium.render(f"Level: {self.game.level_manager.current_level}", 
                                                   True, (255, 255, 255))
        screen.blit(level_text, (self.game.settings.width // 2 - 60, 20))
        
    def draw_lives(self, screen):
        """Draw remaining lives"""
        for i in range(self.game.player.lives):
            x = 20 + i * 30
            y = 100
            pygame.draw.polygon(screen, (0, 255, 0), [
                (x + 10, y),
                (x + 20, y + 20),
                (x, y + 20)
            ])
            
    def draw_missiles(self, screen):
        """Draw missile count"""
        missile_text = self.game.font_small.render(f"Missiles: {self.game.player.missiles}", 
                                                    True, (255, 165, 0))
        screen.blit(missile_text, (20, 140))
        
    def draw_combo(self, screen):
        """Draw combo meter"""
        if self.game.combo > 0:
            combo_text = self.game.font_large.render(f"{self.game.combo}x COMBO!", 
                                                      True, (255, 255, 0))
            # Flash effect
            if int(pygame.time.get_ticks() * 0.01) % 2:
                combo_text.set_alpha(200)
            else:
                combo_text.set_alpha(255)
                
            rect = combo_text.get_rect(center=(self.game.settings.width // 2, 
                                               self.game.settings.height // 2 - 100))
            screen.blit(combo_text, rect)
            
    def draw_fps(self, screen):
        """Draw FPS counter"""
        fps = int(self.game.clock.get_fps())
        fps_text = self.game.font_tiny.render(f"FPS: {fps}", True, (150, 150, 150))
        screen.blit(fps_text, (self.game.settings.width - 60, 10))
        
    def draw_boss_health_bar(self, screen, boss):
        """Draw boss health bar"""
        bar_width = 600
        bar_height = 30
        x = self.game.settings.width // 2 - bar_width // 2
        y = self.game.settings.height - 50
        
        # Background
        pygame.draw.rect(screen, (100, 0, 0), (x, y, bar_width, bar_height))
        
        # Health
        health_percent = boss.health / boss.max_health
        # Color changes based on health
        if health_percent > 0.66:
            color = (0, 255, 0)
        elif health_percent > 0.33:
            color = (255, 255, 0)
        else:
            color = (255, 0, 0)
            
        pygame.draw.rect(screen, color, 
                        (x, y, bar_width * health_percent, bar_height))
        
        # Border
        pygame.draw.rect(screen, (255, 255, 255), (x, y, bar_width, bar_height), 3)
        
        # Text
        boss_text = self.game.font_medium.render(f"BOSS HEALTH", True, (255, 255, 255))
        screen.blit(boss_text, (x + bar_width // 2 - 70, y - 30))