from setting import *
from enemies import *
from waves import *
from wall import *
from towers import *
from tilemap1 import TileMap

class Game:
    def __init__(self):
        pygame.init()

        #setup
        self.width, self.height = width, height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Tempest Vector")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 40)
        self.running = True
    
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


        while True:
            self.screen.fill((40, 40, 40))
            dt = self.clock.tick(60) / 1000


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:                            
                        # Ipapasa natin ang click sa TileMap
                        level_map.handle_click(pygame.mouse.get_pos())

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

<<<<<<< HEAD
            # Update towers (kunin ang placed_towers mula sa level_map)
=======
# Update towers (kunin ang placed_towers mula sa level_map)
>>>>>>> f0012c61fae2664127376c9a33f5a3615fa5a15a
            for tower in level_map.placed_towers:
                tower.update(all_enemies, tower_projectiles)

            # Update projectiles (move toward targets)
            for tower_proj in tower_projectiles[:]:
                tower_proj.update()

            # Tower projectiles damage enemies
            for tower_proj in tower_projectiles[:]:
                if tower_proj.active and tower_proj.target and tower_proj.target.health > 0:
                    # Check if projectile is close to target
                    dist = math.hypot(tower_proj.x - tower_proj.target.pos_x, tower_proj.y - tower_proj.target.pos_y)
                    if dist < tower_proj.radius + 15:
                        tower_proj.target.health -= tower_proj.damage
                        tower_proj.active = False

<<<<<<< HEAD
            # draw
=======
# draw
>>>>>>> f0012c61fae2664127376c9a33f5a3615fa5a15a
            level_map.draw(self.screen)
            wall.draw(self.screen)

            for enemy in all_enemies:
                enemy.draw(self.screen)

            for tower_proj in tower_projectiles:
                tower_proj.draw(self.screen)

            for proj in projectiles:
                proj.draw(self.screen)

            # removers
            for enemy in all_enemies[:]:
                if enemy.health <= 0:
                    wave_manager.remove_enemy(enemy)

            for proj in projectiles[:]:
                alive = proj.update(wall)
                if not alive:
                    projectiles.remove(proj)

            for tower_proj in tower_projectiles[:]:
                if not tower_proj.active or tower_proj.target is None or tower_proj.target.health <= 0:
                    tower_projectiles.remove(tower_proj)

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