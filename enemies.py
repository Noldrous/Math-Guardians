from setting import *
import spritesheet
from particle import Particle

def distance(a, b):
    return math.sqrt((a.pos_x - b.pos_x)**2 + (a.pos_y - b.pos_y)**2)

class Projectile:
    def __init__(self, x, y, speed, damage):
        self.pos = pygame.Vector2(x, y)
        self.speed = speed
        self.damage = damage
        self.radius = 6
        self.is_laser = False

    def update(self, wall, particles):
        self.pos.x -= self.speed

        # collision with wall
        if (
            wall.x < self.pos.x < wall.x + wall.width and
            wall.y < self.pos.y < wall.y + wall.height
        ):
            wall.take_damage(self.damage)

            for _ in range(10):
                particles.append(Particle(self.pos.x, self.pos.y))

            return False  # destroy projectile

        return self.pos.x > 0

    def draw_laser(self, screen):
        if not self.is_laser:
            # Regular projectile (shouldn't reach here)
            pygame.draw.circle(screen, "yellow", (int(self.pos.x), int(self.pos.y)), self.radius)
        else:
            # Laser beam
            pygame.draw.circle(screen, "yellow", (int(self.pos.x), int(self.pos.y)), self.radius)

class Laser(Projectile):
    def __init__(self, x, y, damage, wall):
        super().__init__(x, y, speed=0, damage=damage)
        self.is_laser = True
        self.laser_length = 500
        self.wall = wall
        self.duration = 12  # frames
        self.age = 0

    def update(self, wall, particles):
        self.age += 1
        # Laser damages wall if beam intersects with wall's y-range
        if wall.y < self.pos.y < wall.y + wall.height:
            wall.take_damage(self.damage)

            if self.age % 3 == 0:  
                hit_x = wall.x + wall.width 
                for _ in range(6):
                    particles.append(Particle(hit_x, self.pos.y))

        # Destroy laser after duration
        return self.age < self.duration

    def draw(self, screen):
        # Draw laser beam from source to wall
        end_x = self.wall.x + self.wall.width
        
        # Outer glow (cyan)
        pygame.draw.line(screen, "cyan", (int(self.pos.x), int(self.pos.y)), (int(end_x), int(self.pos.y)), 8)
        
        # Inner core (white)
        pygame.draw.line(screen, "white", (int(self.pos.x), int(self.pos.y)), (int(end_x), int(self.pos.y)), 4)

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
            "moving": 125,
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
        previous_state = self.state

        # STATE LOGIC
        if self.state == "moving":

            self.pos_x -= self.speed * self.speed_multiplier

            if self.pos_x <= wall.x + wall.width:
                self.state = "punch"


        elif self.state == "punch":

            if self.cooldown <= 0:
                wall.take_damage(self.damage * self.damage_multiplier)
                self.cooldown = 45

        # RESET FRAME IF STATE CHANGED
        if self.state != previous_state:
            self.frame = 0

        # ANIMATION SETUP
        self.animation_list = self.animations[self.state]
        self.animation_cooldown = self.animation_cooldowns[self.state]
        if self.frame >= len(self.animation_list):
            self.frame = 0

        # ANIMATION UPDATE
        current_time = pygame.time.get_ticks()

        if current_time - self.last_update >= self.animation_cooldown:
            self.frame += 1
            self.last_update = current_time

            if self.frame >= len(self.animation_list):
                self.frame = 0

        # COOLDOWN UPDATE
        if self.cooldown > 0:
            self.cooldown -= 1


        self.pos.x = self.pos_x
        self.pos.y = self.pos_y

class BlueEnemy(Enemy):
    def __init__(self, y, number):
        super().__init__(health=80, speed=1.5, damage=0.5, y=y)
        self.attack_range = random.randint(250,350)
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

        distance_to_wall = self.pos_x - (wall.x + wall.width)

        # STATE DECISION
        if distance_to_wall <= self.attack_range:
            self.state = "shoot"
        else:
            self.state = "moving"

        # ANIMATION SELECTION
        self.animation_list = self.animations[self.state]
        self.animation_cooldown = self.animation_cooldowns[self.state]
        if self.frame >= len(self.animation_list):
            self.frame = 0

        # ANIMATION UPDATE
        current_time = pygame.time.get_ticks()

        if current_time - self.last_update >= self.animation_cooldown:
            self.frame += 1
            self.last_update = current_time

            if self.frame >= len(self.animation_list):
                self.frame = 0

        # BEHAVIOR
        if self.state == "moving":

            self.pos_x -= self.speed * self.speed_multiplier


        elif self.state == "shoot":

            if self.cooldown <= 0:

                laser = Laser(
                    self.pos_x,
                    self.pos_y + 10,
                    damage=self.damage * self.damage_multiplier,
                    wall=wall,
                )

                projectiles.append(laser)

                self.cooldown = 45

            else:
                self.cooldown -= 1


        self.pos.x = self.pos_x
        self.pos.y = self.pos_y
    
class GreenEnemy(Enemy):
    def __init__(self, y, number):
        super().__init__(health=100, speed=1, damage=2, y=y)

        self.state = "moving"
        self.type = "healer"

        self.heal_amount = 5
        self.heal_range = 100

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

        distance_to_wall = self.pos_x - (wall.x + wall.width)

        # STATE DECISION
        previous_state = self.state

        if distance_to_wall <= self.attack_range:
            self.state = "attacking"

        elif any(
            enemy != self and enemy.type != "healer" and distance(self, enemy) < self.heal_range
            for enemy in enemies
        ):
            self.state = "healing"

        else:
            self.state = "moving"


        # reset animation if state changed
        if self.state != previous_state:
            self.frame = 0

        # ANIMATION SETUP
        self.animation_list = self.animations[self.state]
        self.animation_cooldown = self.animation_cooldowns[self.state]

        if self.frame >= len(self.animation_list):
            self.frame = 0

        # ANIMATION UPDATE
        current_time = pygame.time.get_ticks()

        if current_time - self.last_update >= self.animation_cooldown:
            self.frame += 1
            self.last_update = current_time

            if self.frame >= len(self.animation_list):
                self.frame = 0

        # BEHAVIOR
        if self.state == "moving":

            self.pos_x -= self.speed * self.speed_multiplier


        elif self.state == "healing":

            if self.cooldown <= 0:

                for enemy in enemies:
                    if enemy != self and enemy.type != "healer" and distance(self, enemy) < self.heal_range:
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
                self.cooldown = 10
            else:
                self.cooldown -= 1


        self.pos.x = self.pos_x
        self.pos.y = self.pos_y