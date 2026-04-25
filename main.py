from setting import *
from enemies import *
from waves import *
from wall import *
from towers import *
from tilemap1 import TileMap
from upgrade import UpgradeManager

class Game:
    def __init__(self):
        pygame.init()

        #setup
        self.width, self.height = width, height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Tempest Vector")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 40)
        self.announce_font = pygame.font.SysFont("Arial", 30, bold=True)
        self.running = True
        self.assets = {
            "game_background": load_image_alpha("game_world/background.webp"),
            "wall": load_image_alpha("game_world/wall.webp"),
            "menu_background": load_image_alpha("menu/background.png"),
            "title": load_image_alpha("menu/title.png"),
            "play_button": load_image_alpha("menu/play_button.png"),
            "instruction_button": load_image_alpha("menu/instructions_button.png"),
            "instruction": load_image_alpha("menu/instruction.png"),
            "exit_button": load_image_alpha("menu/exit_button.png")
        }        
        self.show_popup = False
    
    def draw_button(self, img, rect):
        mouse = pygame.mouse.get_pos()
        offset = 5 if rect.collidepoint(mouse) else 0
        self.screen.blit(img, (rect.x, rect.y - offset))

    # ---------------- MENU ----------------
    def start_menu(self):
        play_button = pygame.transform.scale(self.assets["play_button"], (300, 150))
        instruction_button = pygame.transform.scale(self.assets["instruction_button"], (300, 150))
        title = pygame.transform.scale(self.assets["title"], (950, 600))
        popup = pygame.transform.scale(self.assets["instruction"], (600, 660))
        exit_button = pygame.transform.scale(self.assets["exit_button"], (100, 50))

        play_rect = play_button.get_rect(center=(self.width // 2, self.height - 350))
        instruction_rect = instruction_button .get_rect(center=(self.width // 2, self.height - 220))
        title_rect = title.get_rect(center=(self.width // 2, 150))
        popup_rect = popup.get_rect(center=(self.width // 2, self.height // 2))

        bg_x = 0
        bg_speed = 0.5

        while True:

            # PARALLAX BACKGROUND
            bg_x -= bg_speed
            if bg_x <= -self.width:
                bg_x = 0

            self.screen.blit(self.assets["menu_background"], (bg_x, 0))
            self.screen.blit(self.assets["menu_background"], (bg_x + self.width, 0))

            # UI
            self.screen.blit(title, title_rect)
            self.draw_button(play_button, play_rect)
            self.draw_button(instruction_button, instruction_rect)

            # POPUP
            if self.show_popup:
                overlay = pygame.Surface((self.width, self.height))
                overlay.set_alpha(160)
                overlay.fill((0, 0, 0))
                self.screen.blit(overlay, (0, 0))

                self.screen.blit(popup, popup_rect)

                self.close_rect = exit_button.get_rect(
                    topright=popup_rect.topright
                )
                self.close_rect.x -= 20
                self.close_rect.y += 20

                self.screen.blit(exit_button, self.close_rect)

            # EVENTS
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:

                        # CLOSE POPUP
                        if self.show_popup and self.close_rect.collidepoint(event.pos):
                            self.show_popup = False

                        # OPEN POPUP
                        elif instruction_rect.collidepoint(event.pos):
                            self.show_popup = True

                        # START GAME
                        elif play_rect.collidepoint(event.pos) and not self.show_popup:
                            self.game()

            pygame.display.update()
            self.clock.tick(60)

    def game(self):
        level_map = TileMap()
        wave_manager = WaveManager()
        last_announced_wave = 0

        wall = Wall()
        projectiles = []
        tower_projectiles = []
        
        #loadimage
        game_background = self.assets["game_background"]
        game_background = pygame.transform.scale(game_background, (self.width, 725))

        coins = 100 
        upgrade_manager = UpgradeManager(self.height)

        coin_font = pygame.font.SysFont("Arial", 25, bold=True)

        while True:
            dt = self.clock.tick(60) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:                            
                        level_map.handle_click(pygame.mouse.get_pos())

                        coins = upgrade_manager.handle_click(pygame.mouse.get_pos(), coins, level_map.placed_towers)
            wave_manager.update(dt)
            all_enemies = wave_manager.all_enemies

            # wave logic
            current_wave = wave_manager.current_wave
            if current_wave != last_announced_wave:
                last_announced_wave = current_wave

            # enemy update
            for enemy in all_enemies:
                if isinstance(enemy, BlueEnemy):
                    enemy.update(wall, projectiles)
                elif isinstance(enemy, GreenEnemy):
                    enemy.update(wall, all_enemies)
                else:
                    enemy.update(wall)

            # Update towers (kunin ang placed_towers mula sa level_map)
            for tower in level_map.placed_towers:
                tower.update(all_enemies, tower_projectiles)

            # Remove towers with depleted ammo
            for tower in level_map.placed_towers[:]:
                if tower.current_ammo <= 0:
                    level_map.placed_towers.remove(tower)
                    # Also remove from occupied grid
                    for grid_pos, grid_tower in list(level_map.occupied.items()):
                        if grid_tower == tower:
                            del level_map.occupied[grid_pos]
                            break

            # Update projectiles (move toward targets)
            for tower_proj in tower_projectiles[:]:
                tower_proj.update()

            # Tower projectiles damage enemies
            for tower_proj in tower_projectiles[:]:
                if tower_proj.active and tower_proj.target and tower_proj.target.health > 0:
                    # Check if projectile is close to target
                    dist = math.hypot(tower_proj.x - tower_proj.target.pos_x, tower_proj.y - tower_proj.target.pos_y)
                    if dist < tower_proj.radius + 15:
                        # Handle splash damage for bazooka
                        if tower_proj.projectile_type == "bazooka" and not tower_proj.has_exploded:
                            # Apply splash damage to all enemies in range
                            explosion_x, explosion_y = tower_proj.target.pos_x, tower_proj.target.pos_y
                            for enemy in all_enemies:
                                if hasattr(enemy, 'pos_x') and hasattr(enemy, 'pos_y'):
                                    splash_dist = math.hypot(enemy.pos_x - explosion_x, enemy.pos_y - explosion_y)
                                    if splash_dist <= tower_proj.splash_radius:
                                        enemy.health -= tower_proj.damage
                            tower_proj.has_exploded = True
                        else:
                            # Normal damage for other projectiles
                            tower_proj.target.health -= tower_proj.damage
                        tower_proj.active = False

            # draw

            self.screen.blit(game_background, (0, 0))
            wall.draw(self.screen)
            level_map.draw(self.screen)

            for enemy in all_enemies:
                enemy.draw(self.screen)

            for tower_proj in tower_projectiles:
                tower_proj.draw(self.screen)

            for proj in projectiles:
                proj.draw(self.screen)

            # removers
            for enemy in all_enemies[:]:
                if enemy.health <= 0:
                    coins += 15  # Magdadagdag ng 15 coins
                    wave_manager.remove_enemy(enemy)

            for proj in projectiles[:]:
                alive = proj.update(wall)
                if not alive:
                    projectiles.remove(proj)

            for tower_proj in tower_projectiles[:]:
                if not tower_proj.active or tower_proj.target is None or tower_proj.target.health <= 0:
                    tower_projectiles.remove(tower_proj)

            upgrade_manager.draw(self.screen)

            #ALWAYS ON TOP
            wave_top_text = coin_font.render(f"Wave: {current_wave}", True, (255, 255, 255))
            self.screen.blit(wave_top_text, (self.width // 2 - wave_top_text.get_width() // 2, 20))
            
            # Current Coins
            coin_text = coin_font.render(f"Coins: {coins}", True, (255, 215, 0))
            self.screen.blit(coin_text, (1150, 20))

            if wave_manager.wave_complete and current_wave > 0:
                timer = wave_manager.wave_timer
                delay = wave_manager.wave_delay

                if timer < 1.0:
                    alpha = int((timer / 1.0) * 255)
                elif timer < delay - 1.0:
                    alpha = 255
                else:
                    alpha = int(((delay - timer) / 1.0) * 255)
   
                alpha = max(0, min(255, alpha))
                
                announce_surface = self.announce_font.render(f"WAVE {current_wave} CLEARED", True, (100, 255, 100))
                announce_surface.set_alpha(alpha)
                
                self.screen.blit(announce_surface, (self.width // 2 - announce_surface.get_width() // 2, self.height // 2 - 50))
            
            #Current Coins
            coin_text = coin_font.render(f"Coins: {coins}", True, (255, 215, 0))
            self.screen.blit(coin_text, (1150, 20))
            

            # GAME OVER CHECK
            if wall.health <= 0:
                self.game_over()
                return

            pygame.display.update()
            
    def game_over(self):
        """Display game over screen"""
        while True:
            self.screen.fill((40, 40, 40))
            mouse = pygame.mouse.get_pos()

            game_over_text = self.font.render("Game Over!", True, "red")
            restart_button = pygame.Rect(width//2 - 90, height - 300, 180, 50)
            menu_button = pygame.Rect(width//2 - 90, height - 200, 180, 50)

            pygame.draw.rect(self.screen, "skyblue" if restart_button.collidepoint(mouse) else "darkgray", restart_button)
            pygame.draw.rect(self.screen, "skyblue" if menu_button.collidepoint(mouse) else "darkgray", menu_button)

            restart_text = self.font.render("Restart", True, "white")
            menu_text = self.font.render("Menu", True, "white")

            self.screen.blit(game_over_text, (width//2 - 150, height - 500))
            self.screen.blit(restart_text, (width//2 - 80, height - 300))
            self.screen.blit(menu_text, (width//2 - 50, height - 200))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_buttons = pygame.mouse.get_pressed()
                    if restart_button.collidepoint(mouse) and mouse_buttons[0]:
                        self.game()
                        return

                    if menu_button.collidepoint(mouse) and mouse_buttons[0]:
                        return

            pygame.display.update()
            self.clock.tick(60)
            
if __name__ == "__main__":
    Game().start_menu()
    