"""
Menu system - Main menu, pause menu, and game over screens
"""

import pygame

class MenuSystem:
    def __init__(self, game):
        self.game = game
        self.selected_option = 0
        self.options = ["Start Game", "Continue", "Level Select", "Settings", "Credits", "Exit"]
        
        # Settings options
        self.settings_options = ["Music Volume", "Sound Volume", "Difficulty", "Fullscreen", "Back"]
        self.difficulties = ["Easy", "Normal", "Hard", "Extreme"]
        self.current_settings_selection = 0
        
        # Level select
        self.level_scroll = 0
        self.levels_per_page = 10
        self.showing_level_select = False
        self.showing_settings = False
        self.showing_credits = False
        
    def handle_event(self, event):
        """Handle menu events"""
        if self.showing_settings:
            self.handle_settings_event(event)
        elif self.showing_level_select:
            self.handle_level_select_event(event)
        elif self.showing_credits:
            self.handle_credits_event(event)
        else:
            self.handle_main_menu_event(event)
            
    def handle_main_menu_event(self, event):
        """Handle main menu events"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.options)
                self.game.play_sound('ui_click')
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.options)
                self.game.play_sound('ui_click')
            elif event.key == pygame.K_RETURN:
                self.select_option()
                self.game.play_sound('ui_click')
                
    def handle_settings_event(self, event):
        """Handle settings menu events"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.current_settings_selection = (self.current_settings_selection - 1) % len(self.settings_options)
                self.game.play_sound('ui_click')
            elif event.key == pygame.K_DOWN:
                self.current_settings_selection = (self.current_settings_selection + 1) % len(self.settings_options)
                self.game.play_sound('ui_click')
            elif event.key == pygame.K_LEFT:
                self.adjust_setting(-1)
                self.game.play_sound('ui_click')
            elif event.key == pygame.K_RIGHT:
                self.adjust_setting(1)
                self.game.play_sound('ui_click')
            elif event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                if self.settings_options[self.current_settings_selection] == "Back":
                    self.showing_settings = False
                self.game.play_sound('ui_click')
                
    def handle_level_select_event(self, event):
        """Handle level select events"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.showing_level_select = False
                self.game.play_sound('ui_click')
            elif event.key == pygame.K_RETURN:
                # Select level logic would go here
                self.showing_level_select = False
                self.game.play_sound('ui_click')
                
    def handle_credits_event(self, event):
        """Handle credits events"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                self.showing_credits = False
                self.game.play_sound('ui_click')
                
    def adjust_setting(self, direction):
        """Adjust a setting value"""
        setting = self.settings_options[self.current_settings_selection]
        
        if setting == "Music Volume":
            new_volume = self.game.settings.music_volume + (direction * 10)
            self.game.settings.music_volume = max(0, min(100, new_volume))
            pygame.mixer.music.set_volume(self.game.settings.music_volume / 100.0)
        elif setting == "Sound Volume":
            new_volume = self.game.settings.sound_volume + (direction * 10)
            self.game.settings.sound_volume = max(0, min(100, new_volume))
        elif setting == "Difficulty":
            current_index = self.difficulties.index(self.game.settings.difficulty.capitalize())
            new_index = (current_index + direction) % len(self.difficulties)
            self.game.settings.difficulty = self.difficulties[new_index].lower()
            self.game.settings.get_difficulty_multipliers()
        elif setting == "Fullscreen":
            if direction != 0:
                self.game.settings.toggle_fullscreen()
                pygame.display.toggle_fullscreen()
                
        self.game.settings.save_settings()
                
    def select_option(self):
        """Handle menu option selection"""
        if self.options[self.selected_option] == "Start Game":
            self.start_new_game()
        elif self.options[self.selected_option] == "Continue":
            self.continue_game()
        elif self.options[self.selected_option] == "Level Select":
            self.showing_level_select = True
        elif self.options[self.selected_option] == "Settings":
            self.showing_settings = True
        elif self.options[self.selected_option] == "Credits":
            self.showing_credits = True
        elif self.options[self.selected_option] == "Exit":
            self.game.running = False
            
    def start_new_game(self):
        """Start a new game"""
        self.game.score = 0
        self.game.combo = 0
        self.game.kills = 0
        self.game.bullets_fired = 0
        self.game.bullets_hit = 0
        self.game.player.health = 100
        self.game.player.shield = 0
        self.game.player.missiles = 5
        self.game.player.lives = 3
        self.game.level_manager.start_level(1)
        self.game.game_state = "playing"
        self.game.play_music('game')
        
    def continue_game(self):
        """Continue from saved game"""
        level = self.game.player_data.get('current_level', 1)
        self.game.score = self.game.player_data.get('total_score', 0)
        self.game.level_manager.start_level(level)
        self.game.game_state = "playing"
        self.game.play_music('game')
        
    def update(self):
        """Update menu"""
        pass
        
    def update_pause(self):
        """Update pause menu"""
        pass
        
    def update_game_over(self):
        """Update game over screen"""
        pass
        
    def update_victory(self):
        """Update victory screen"""
        pass
        
    def render(self, screen):
        """Render main menu"""
        if self.showing_settings:
            self.render_settings(screen)
        elif self.showing_level_select:
            self.render_level_select(screen)
        elif self.showing_credits:
            self.render_credits(screen)
        else:
            self.render_main_menu(screen)
            
    def render_main_menu(self, screen):
        """Render main menu"""
        # Background gradient
        for i in range(self.game.settings.height):
            color_value = int(30 + (i / self.game.settings.height) * 50)
            pygame.draw.line(screen, (0, 0, color_value), (0, i), (self.game.settings.width, i))
        
        # Title
        title = self.game.font_large.render("AIR ATTACK", True, (255, 255, 0))
        title_rect = title.get_rect(center=(self.game.settings.width // 2, 100))
        
        # Animate title
        y_offset = abs(pygame.time.get_ticks() * 0.001) % 20
        title_rect.y += y_offset
        screen.blit(title, title_rect)
        
        # Subtitle
        subtitle = self.game.font_small.render("Aerial Combat Arcade", True, (255, 255, 255))
        subtitle_rect = subtitle.get_rect(center=(self.game.settings.width // 2, 160))
        screen.blit(subtitle, subtitle_rect)
        
        # Menu options
        for i, option in enumerate(self.options):
            color = (255, 255, 0) if i == self.selected_option else (255, 255, 255)
            text = self.game.font_medium.render(option, True, color)
            rect = text.get_rect(center=(self.game.settings.width // 2, 250 + i * 50))
            screen.blit(text, rect)
            
            # Draw selector arrow
            if i == self.selected_option:
                arrow = self.game.font_medium.render(">", True, color)
                screen.blit(arrow, (rect.left - 30, rect.top))
                
        # Instructions
        instructions = self.game.font_tiny.render("Use ARROW KEYS to navigate, ENTER to select", 
                                                  True, (150, 150, 150))
        inst_rect = instructions.get_rect(center=(self.game.settings.width // 2, 
                                                  self.game.settings.height - 50))
        screen.blit(instructions, inst_rect)
        
    def render_settings(self, screen):
        """Render settings menu"""
        screen.fill((0, 0, 30))
        
        # Title
        title = self.game.font_medium.render("SETTINGS", True, (255, 255, 0))
        title_rect = title.get_rect(center=(self.game.settings.width // 2, 80))
        screen.blit(title, title_rect)
        
        # Settings options
        for i, option in enumerate(self.settings_options):
            color = (255, 255, 0) if i == self.current_settings_selection else (255, 255, 255)
            
            if option == "Music Volume":
                text = self.game.font_small.render(f"{option}: {self.game.settings.music_volume}%", True, color)
            elif option == "Sound Volume":
                text = self.game.font_small.render(f"{option}: {self.game.settings.sound_volume}%", True, color)
            elif option == "Difficulty":
                text = self.game.font_small.render(f"{option}: {self.game.settings.difficulty.capitalize()}", True, color)
            elif option == "Fullscreen":
                text = self.game.font_small.render(f"{option}: {'ON' if self.game.settings.fullscreen else 'OFF'}", True, color)
            else:
                text = self.game.font_small.render(option, True, color)
                
            rect = text.get_rect(center=(self.game.settings.width // 2, 180 + i * 50))
            screen.blit(text, rect)
            
            if i == self.current_settings_selection:
                arrow = self.game.font_small.render(">", True, color)
                screen.blit(arrow, (rect.left - 30, rect.top))
                
        # Instructions
        instructions = self.game.font_tiny.render("Use ARROW KEYS to adjust, ENTER/ESC to go back", 
                                                  True, (150, 150, 150))
        inst_rect = instructions.get_rect(center=(self.game.settings.width // 2, 
                                                  self.game.settings.height - 50))
        screen.blit(instructions, inst_rect)
        
    def render_level_select(self, screen):
        """Render level select screen"""
        screen.fill((0, 0, 30))
        
        title = self.game.font_medium.render("LEVEL SELECT", True, (255, 255, 0))
        title_rect = title.get_rect(center=(self.game.settings.width // 2, 80))
        screen.blit(title, title_rect)
        
        # Show available levels
        current_level = self.game.player_data.get('current_level', 1)
        unlocked_until = min(current_level + 5, 140)
        
        info_text = self.game.font_small.render(f"Unlocked: Level 1 - {unlocked_until}", True, (255, 255, 255))
        info_rect = info_text.get_rect(center=(self.game.settings.width // 2, 130))
        screen.blit(info_text, info_rect)
        
        # Display level grid
        start_level = self.level_scroll * self.levels_per_page + 1
        end_level = min(start_level + self.levels_per_page - 1, 140)
        
        for i in range(start_level, end_level + 1):
            x = 100 + ((i - start_level) % 5) * 200
            y = 200 + ((i - start_level) // 5) * 80
            
            if i <= unlocked_until:
                color = (0, 255, 0) if i <= current_level else (255, 255, 0)
                level_text = self.game.font_small.render(f"Level {i}", True, color)
            else:
                level_text = self.game.font_small.render(f"Level {i} (Locked)", True, (100, 100, 100))
                
            screen.blit(level_text, (x, y))
            
        # Instructions
        instructions = self.game.font_tiny.render("Press ESC to go back", 
                                                  True, (150, 150, 150))
        inst_rect = instructions.get_rect(center=(self.game.settings.width // 2, 
                                                  self.game.settings.height - 50))
        screen.blit(instructions, inst_rect)
        
    def render_credits(self, screen):
        """Render credits screen"""
        screen.fill((0, 0, 30))
        
        title = self.game.font_medium.render("CREDITS", True, (255, 255, 0))
        title_rect = title.get_rect(center=(self.game.settings.width // 2, 80))
        screen.blit(title, title_rect)
        
        credits = [
    "Air Attack - Aerial Combat Game",
    "",
    "Game Design & Development",
    "Created by M. Dallen Shelly",
    "",
    "Special Thanks:",
    "Pygame Community",
    "DeepSeek",
    "",
    "========== REQUEST TO ALL PLAYERS ==========",
    "Please do NOT copy or distribute this game.",
    "This game is made with hard work by a SINGLE person.",
    "Contains nearly 5,000 to 12,000 lines of code.",
    "Please use it with respect.",
    "===========================================",
    "",
    "Press ESC to return to main menu"
        ]
        
        for i, line in enumerate(credits):
            if i == 0:
                text = self.game.font_medium.render(line, True, (255, 215, 0))
            elif line == "":
                continue
            elif i == len(credits) - 1:
                text = self.game.font_small.render(line, True, (150, 150, 150))
            else:
                text = self.game.font_small.render(line, True, (255, 255, 255))
                
            rect = text.get_rect(center=(self.game.settings.width // 2, 150 + i * 35))
            screen.blit(text, rect)
            
    def render_pause_overlay(self, screen):
        """Render pause overlay"""
        # Darken screen
        overlay = pygame.Surface((self.game.settings.width, self.game.settings.height))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Pause text
        pause_text = self.game.font_large.render("PAUSED", True, (255, 255, 255))
        pause_rect = pause_text.get_rect(center=(self.game.settings.width // 2, 
                                                 self.game.settings.height // 2 - 50))
        screen.blit(pause_text, pause_rect)
        
        # Options
        options = ["Resume", "Restart Level", "Settings", "Main Menu"]
        for i, option in enumerate(options):
            color = (255, 255, 0) if i == self.selected_option else (255, 255, 255)
            text = self.game.font_medium.render(option, True, color)
            rect = text.get_rect(center=(self.game.settings.width // 2, 
                                         self.game.settings.height // 2 + i * 50))
            screen.blit(text, rect)
            
        # Instruction
        resume_text = self.game.font_small.render("Press ESC to Resume", True, (200, 200, 200))
        resume_rect = resume_text.get_rect(center=(self.game.settings.width // 2, 
                                                   self.game.settings.height - 80))
        screen.blit(resume_text, resume_rect)
        
    def render_game_over(self, screen, score):
        """Render game over screen"""
        screen.fill((0, 0, 0))
        
        # Game over text
        game_over = self.game.font_large.render("GAME OVER", True, (255, 0, 0))
        game_over_rect = game_over.get_rect(center=(self.game.settings.width // 2, 150))
        screen.blit(game_over, game_over_rect)
        
        # Final score
        score_text = self.game.font_medium.render(f"Final Score: {score}", True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(self.game.settings.width // 2, 250))
        screen.blit(score_text, score_rect)
        
        # High score
        high_score = self.game.player_data.get('high_score', 0)
        if score > high_score:
            high_score_text = self.game.font_medium.render(f"NEW HIGH SCORE: {score}", True, (255, 215, 0))
        else:
            high_score_text = self.game.font_medium.render(f"High Score: {high_score}", True, (255, 255, 0))
        high_rect = high_score_text.get_rect(center=(self.game.settings.width // 2, 300))
        screen.blit(high_score_text, high_rect)
        
        # Stats
        stats_text = self.game.font_small.render(f"Enemies Killed: {self.game.kills}  |  Accuracy: {int(self.game.bullets_hit / max(1, self.game.bullets_fired) * 100)}%", 
                                                  True, (200, 200, 200))
        stats_rect = stats_text.get_rect(center=(self.game.settings.width // 2, 370))
        screen.blit(stats_text, stats_rect)
        
        # Options
        options = ["Retry", "Main Menu"]
        for i, option in enumerate(options):
            color = (255, 255, 0) if i == self.selected_option else (255, 255, 255)
            text = self.game.font_medium.render(option, True, color)
            rect = text.get_rect(center=(self.game.settings.width // 2, 450 + i * 60))
            screen.blit(text, rect)
            
        # Handle selection in game over
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_DOWN]:
            self.selected_option = (self.selected_option + 1) % len(options)
            self.game.play_sound('ui_click')
            pygame.time.wait(200)
        elif keys[pygame.K_RETURN]:
            if options[self.selected_option] == "Retry":
                self.start_new_game()
            elif options[self.selected_option] == "Main Menu":
                self.game.game_state = "menu"
            self.game.play_sound('ui_click')
            
    def render_victory(self, screen, score):
        """Render victory screen"""
        screen.fill((0, 0, 0))
        
        # Victory text
        victory = self.game.font_large.render("VICTORY!", True, (255, 215, 0))
        victory_rect = victory.get_rect(center=(self.game.settings.width // 2, 150))
        screen.blit(victory, victory_rect)
        
        # Congratulations
        congrats = self.game.font_medium.render("You have completed all 140 levels!", True, (255, 255, 255))
        congrats_rect = congrats.get_rect(center=(self.game.settings.width // 2, 250))
        screen.blit(congrats, congrats_rect)
        
        # Final score
        score_text = self.game.font_medium.render(f"Final Score: {score}", True, (255, 255, 0))
        score_rect = score_text.get_rect(center=(self.game.settings.width // 2, 350))
        screen.blit(score_text, score_rect)
        
        # Endless mode unlocked
        endless = self.game.font_small.render("ENDLESS MODE UNLOCKED!", True, (0, 255, 0))
        endless_rect = endless.get_rect(center=(self.game.settings.width // 2, 450))
        screen.blit(endless, endless_rect)
        
        # Option to continue
        continue_text = self.game.font_medium.render("Press ENTER to return to Main Menu", True, (255, 255, 255))
        continue_rect = continue_text.get_rect(center=(self.game.settings.width // 2, 
                                                        self.game.settings.height - 100))
        screen.blit(continue_text, continue_rect)
        
        # Handle continue
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            self.game.game_state = "menu"
            pygame.time.wait(200)