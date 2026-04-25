from setting import *

class Wall:
    def __init__(self):
        self.width = 120
        self.height = 600
        self.x = width // 2 - self.width // 2
        self.y = 120

        self.max_health = 1000
        self.health = self.max_health

        self.image = load_image_alpha("game_world/wall.webp")
        self.image = pygame.transform.scale(self.image, (self.width, self.height))


    def take_damage(self, damage):
        self.health -= damage

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

        # health bar
        health_ratio = self.health / self.max_health
        pygame.draw.rect(screen, "red", (width // 2 - 60, 600, self.width, 10))
        pygame.draw.rect(screen, "green", (width // 2 - 60, 600, self.width * health_ratio, 10))