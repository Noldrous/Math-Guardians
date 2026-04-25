from setting import *
import spritesheet

def distance(a, b):
    return math.sqrt((a.pos_x - b.pos_x)**2 + (a.pos_y - b.pos_y)**2)

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
        self.pos = pygame.Vector2(self.pos_x, self.pos_y)

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
        self.type = "attacker"
        self.cooldown = 0
        self.color = (255, 0, 0)  # Red
        self.sprite_sheet_image = load_image_alpha("enemies/redguy.png")
        self.sprite_sheet = spritesheet.SpriteSheet(self.sprite_sheet_image)
        self.animations = {
            "moving":  [],
            "punch": []
        }
        self.animation_cooldowns = {
            "moving": 150,
            "punch": 250
        }
        

        self.last_update = pygame.time.get_ticks()
        self.frame = 0
        for x in range(4):
            self.animations["moving"].append(self.sprite_sheet.get_image(x, 0, 357, 446, 0.15))
        for x in range(3):
            self.animations["punch"].append(self.sprite_sheet.get_image(x, 1, 357, 446, 0.15))

        self.animation_list = self.animations[self.state]
        self.animation_cooldown = self.animation_cooldowns[self.state]


    def draw(self, screen):
        flip_image = pygame.transform.flip(self.animation_list[self.frame], True, False)
        rect = flip_image.get_rect(center=self.pos)
        screen.blit(flip_image, rect.topleft)

    def update(self, wall):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update >= self.animation_cooldown:
            self.frame += 1
            self.last_update = current_time
            if self.frame >= len(self.animation_list):
                self.frame = 0

        self.animation_list = self.animations[self.state]
        self.animation_cooldown = self.animation_cooldowns[self.state]
        
        if self.state == "moving":
            self.pos_x -= self.speed * self.speed_multiplier

            if self.pos_x <= wall.x + wall.width:
                self.state = "punch"

        elif self.state == "punch":

            if self.cooldown <= 0:
                wall.take_damage(self.damage * self.damage_multiplier)
                self.cooldown = 45

        if self.cooldown > 0:
            self.cooldown -= 1


        self.pos.x = self.pos_x
        self.pos.y = self.pos_y

class BlueEnemy(Enemy):
    def __init__(self, y, number):
        super().__init__(health=80, speed=1.5, damage=8, y=y)
        self.attack_range = random.randint(250, 400)
        self.cooldown = 0
        self.state = "moving"
        self.type = "attacker"
        self.color = (0, 0, 255)  # Blue
        self.sprite_sheet_image = load_image_alpha("enemies/blueguy.png")
        self.sprite_sheet = spritesheet.SpriteSheet(self.sprite_sheet_image)
        self.animations = {
            "moving":  [],
            "shoot": []
        }
        self.animation_cooldowns = {
            "moving": 150,
            "shoot": 250
        }
        

        self.last_update = pygame.time.get_ticks()
        self.frame = 0
        for x in range(4):
            self.animations["moving"].append(self.sprite_sheet.get_image(x, 0, 448, 560, 0.12))
        for x in range(3):
            self.animations["shoot"].append(self.sprite_sheet.get_image(x, 1, 448, 560, 0.12))
        

        self.animation_list = self.animations[self.state]
        self.animation_cooldown = self.animation_cooldowns[self.state]

    def draw(self, screen):
        flip_image = pygame.transform.flip(self.animation_list[self.frame], True, False)
        rect = flip_image.get_rect(center=self.pos)
        screen.blit(flip_image, rect.topleft)

    def update(self, wall, projectiles):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update >= self.animation_cooldown:
            self.frame += 1
            self.last_update = current_time
            if self.frame >= len(self.animation_list):
                self.frame = 0

        self.animation_list = self.animations[self.state]
        self.animation_cooldown = self.animation_cooldowns[self.state]

        if self.state == "moving":
            self.pos_x -= self.speed * self.speed_multiplier

            if self.pos_x - wall.x < self.attack_range:
                self.state = "shoot"
                self.frame = 0

        elif self.state == "shoot":
            if self.cooldown <= 0:
                # shoot projectile
                proj = Projectile(
                    self.pos_x,
                    self.pos_y + 10,
                    speed=6,
                    damage=self.damage * self.damage_multiplier,
                )
                self.cooldown = 45
                projectiles.append(proj)

        if self.cooldown > 0:
            self.cooldown -= 1

        self.pos.x = self.pos_x
        self.pos.y = self.pos_y
    
class GreenEnemy(Enemy):
    def __init__(self, y, number):
        super().__init__(health=100, speed=1, damage=2, y=y)

        self.state = "moving"
        self.type = "healer"

        self.heal_amount = 5
        self.heal_range = 300

        self.attack_range = random.randint(40, 80)
        self.cooldown = 0
        self.color = (0, 255, 0)  # Green

        self.sprite_sheet_image = load_image_alpha("enemies/greenguy.png")
        self.sprite_sheet = spritesheet.SpriteSheet(self.sprite_sheet_image)
        self.animations = {
            "moving":  [],
            "healing": [],
            "attacking": []
        }
        self.animation_cooldowns = {
            "moving": 150,
            "healing": 200,
            "attacking": 50
        }
        

        self.last_update = pygame.time.get_ticks()
        self.frame = 0
        for x in range(4):
            self.animations["moving"].append(self.sprite_sheet.get_image(x, 0, 447, 558, 0.12))
        for x in range(3):
            self.animations["healing"].append(self.sprite_sheet.get_image(x, 1, 447, 558, 0.12))
        for x in range(3):
            self.animations["attacking"].append(self.sprite_sheet.get_image(x, 1, 447, 558, 0.12))

        self.animation_list = self.animations[self.state]
        self.animation_cooldown = self.animation_cooldowns[self.state]

    def draw(self, screen):
        flip_image = pygame.transform.flip(self.animation_list[self.frame], True, False)
        rect = flip_image.get_rect(center=self.pos)
        screen.blit(flip_image, rect.topleft)

    def update(self, wall, enemies):
        self.animation_list = self.animations[self.state]
        self.animation_cooldown = self.animation_cooldowns[self.state]

        current_time = pygame.time.get_ticks()
        if current_time - self.last_update >= self.animation_cooldown:
            self.frame += 1
            self.last_update = current_time
            if self.frame >= len(self.animation_list):
                self.frame = 0
                
        distance_to_wall = self.pos_x - (wall.x + wall.width)

        if any(
            enemy != self and distance(self, enemy) < self.heal_range
            for enemy in enemies
        ):

            self.state = "healing"
        else:

            self.state = "moving"

        if distance_to_wall <= self.attack_range:

            self.state = "attacking"

        if self.state == "moving":

            self.pos_x -= self.speed * self.speed_multiplier

        elif self.state == "healing":

            if self.cooldown <= 0:
                for enemy in enemies:
                    if enemy != self and enemy.color != (0, 255, 0)  and distance(self, enemy) < self.heal_range:
                        enemy.health = min(
                            enemy.health + self.heal_amount,
                            enemy.max_health
                        )

                self.cooldown = 120
            else:
                self.cooldown -= 1

        elif self.state == "attacking":

            if self.cooldown <= 0:
                wall.take_damage(self.damage * self.damage_multiplier)
                self.cooldown = 90  # attack speed
            else:
                self.cooldown -= 1

            if any(
                enemy != self and distance(self, enemy) < self.heal_range
                for enemy in enemies
            ):
                self.state = "healing"

        self.pos.x = self.pos_x
        self.pos.y = self.pos_y