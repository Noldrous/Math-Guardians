from setting import *
from enemies import *
from waves import *
from wall import *
from towers import *

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
        wave_manager = WaveManager()
        last_announced_wave = 0

        wall = Wall()
        projectiles = []
        towers = []
        tower_projectiles = []
        
        # Tower placement state
        selected_tower_type = None
        tower_types = {
            '1': RedTower,
            '2': BlueTower,
            '3': GreenTower,
            '4': YellowTower
        }

        while True:
            self.screen.fill((40, 40, 40))
            dt = self.clock.tick(60) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                # Tower selection with number keys
                if event.type == pygame.KEYDOWN:
                    if event.unicode in tower_types:
                        selected_tower_type = event.unicode
                
                # Tower placement on mouse click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if selected_tower_type:
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        tower_class = tower_types[selected_tower_type]
                        towers.append(tower_class(mouse_x, mouse_y))

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

            # Update towers (they shoot projectiles)
            for tower in towers:
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

            # draw
            wall.draw(self.screen)

            for enemy in all_enemies:
                enemy.draw(self.screen)

            # Draw towers
            for tower in towers:
                tower.draw(self.screen)

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