from setting import *
from enemies import *
from waves import *
from wall import *

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

        while True:
            self.screen.fill((40, 40, 40))
            dt = self.clock.tick(60) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

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

            # draw
            wall.draw(self.screen)

            for enemy in all_enemies:
                enemy.draw(self.screen)

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

            # GAME OVER CHECK
            if wall.health <= 0:
                self.game_over()
                return

            pygame.display.update()
            
if __name__ == "__main__":
    Game().start_menu() 