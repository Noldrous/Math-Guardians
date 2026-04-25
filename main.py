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
            "wall": load_image_alpha("game_world/wall.webp")
        }
    
    def start_menu(self):
        while True:

            self.screen.fill((40, 40, 40))
            mouse = pygame.mouse.get_pos()

            play_button = pygame.Rect(width//2 - 70, height - 400, 140, 50)
            quit_button = pygame.Rect(width //2 - 70, height - 325, 140, 50)

            pygame.draw.rect(self.screen, "skyblue" if play_button.collidepoint(mouse) else "darkgray", play_button)
            pygame.draw.rect(self.screen, "skyblue" if quit_button.collidepoint(mouse) else "darkgray", quit_button)

            play_text = self.font.render("Play", True, "white")
            quit_text = self.font.render("Quit", True, "white")

            self.screen.blit(play_text, (width//2 - 70, height - 400))
            self.screen.blit(quit_text, (width //2 - 70, height - 325))

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_buttons = pygame.mouse.get_pressed()
                    if play_button.collidepoint(mouse) and mouse_buttons[0]:
                        self.game()

                    if quit_button.collidepoint(mouse) and mouse_buttons[0]:
                        pygame.quit()
                        sys.exit()

            pygame.display.update()
            fps = self.clock.tick(60)

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
    #