from setting import *
import pygame

class Projectile:
    def __init__(self, x, y, speed, damage):
        self.pos = pygame.Vector2(x, y)
        self.speed = speed
        self.damage = damage
        self.radius = 5

    def update(self, wall):
        self.pos.x -= self.speed

        # collision with wall
        if (
            wall.x < self.pos.x < wall.x + wall.width and
            wall.y < self.pos.y < wall.y + wall.height
        ):
            wall.take_damage(self.damage)
            return False  # destroy projectile

        return self.pos.x > 0

    def draw(self, screen):
        pygame.draw.circle(screen, "cyan", (int(self.pos.x), int(self.pos.y)), self.radius)

class Enemy:
    def __init__(self, health, speed, damage, y):
        self.base_health = health
        self.base_speed = speed
        self.base_damage = damage

        self.health = health
        self.pos_x = width + 200
        self.pos_y = y

        self.speed = speed
        self.damage = damage
        
        self.health_multiplier = 1
        self.speed_multiplier = 1
        self.damage_multiplier = 1
        
    @property
    def max_health(self):
        return self.base_health * self.health_multiplier

    @property
    def max_speed(self):
        return self.base_speed * self.speed_multiplier

    @property
    def max_damage(self):
        return self.base_damage * self.damage_multiplier

    def take_damage(self, damage):
        self.health -= damage

class RedEnemy(Enemy):
    def __init__(self, y, number):
        super().__init__(health=120, speed=2, damage=10, y=y)
        self.state = "moving"
        self.cooldown = 0

    def draw(self, screen):
        pygame.draw.rect(screen, "RED", (self.pos_x, self.pos_y, 20, 20))

    def update(self, gate):

        if self.state == "moving":
            self.pos_x -= self.speed * self.speed_multiplier

            if self.pos_x <= gate.x + gate.width:
                self.state = "punch"

        elif self.state == "punch":

            if self.cooldown <= 0:
                gate.take_damage(self.damage * self.damage_multiplier)
                self.cooldown = 60

        if self.cooldown > 0:
            self.cooldown -= 1

class BlueEnemy(Enemy):
    def __init__(self, y, number):
        super().__init__(health=80, speed=1.5, damage=8, y=y)
        self.attack_range = 300
        self.cooldown = 0
        self.state = "moving"

    def draw(self, screen):
        pygame.draw.rect(screen, "BLUE", (self.pos_x, self.pos_y, 20, 20))

    def update(self, gate, projectiles):
        if self.state == "moving":
            self.pos_x -= self.speed * self.speed_multiplier

            if self.pos_x - gate.x < self.attack_range:
                self.state = "shoot"

        elif self.state == "shoot":
            if self.cooldown <= 0:
                # shoot projectile
                proj = Projectile(
                    self.pos_x,
                    self.pos_y + 10,
                    speed=6,
                    damage=self.damage * self.damage_multiplier
                )
                projectiles.append(proj)

                self.cooldown = 60  # fire rate

        if self.cooldown > 0:
            self.cooldown -= 1
    
class GreenEnemy(Enemy):
    def __init__(self, y, number):
        super().__init__(health=100, speed=1.8, damage=2, y=y)
        self.heal_amount = 5
        self.heal_range = 150
        self.cooldown = 0

    def draw(self, screen):
        pygame.draw.rect(screen, "GREEN", (self.pos_x, self.pos_y, 20, 20))

    def update(self, enemies):

        self.pos_x -= self.speed * self.speed_multiplier

        if self.cooldown <= 0:

            for enemy in enemies:

                distance = abs(enemy.pos_x - self.pos_x)

                if distance < self.heal_range and enemy != self:
                    enemy.health = min(enemy.health + self.heal_amount, enemy.max_health)

            self.cooldown = 120

        if self.cooldown > 0:
            self.cooldown -= 1