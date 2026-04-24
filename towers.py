from setting import *
from typing import List, Tuple
import math

class Tower():
    def __init__(self, x: int, y: int, tower_type: str = "basic"):
        self.x = x
        self.y = y
        self.tower_type = tower_type
        self.range = 150
        self.damage = 25
        self.fire_rate = 60  # frames between shots
        self.cooldown = 0
        self.cost = 50
        
        # Tower stats by type
        # tower_stats = {
        #     "basic": {"range": 150, "damage": 25, "fire_rate": 60, "cost": 50},
        #     "sniper": {"range": 250, "damage": 75, "fire_rate": 120, "cost": 100},
        #     "rapid": {"range": 100, "damage": 10, "fire_rate": 20, "cost": 75}
        # }
        
        # stats = tower_stats.get(tower_type, tower_stats["basic"])
        # self.range = stats["range"]
        # self.damage = stats["damage"]
        # self.fire_rate = stats["fire_rate"]
        # self.cost = stats["cost"]
        
        # Visual properties
        self.size = 40
        self.color = (100, 100, 255)
        self.target = None
        
    def update(self, enemies: List['Enemy'], projectiles: List['Projectile']):
        # Find nearest enemy in range
        self.target = self.find_target(enemies)
        
        # Update cooldown
        if self.cooldown > 0:
            self.cooldown -= 1
            return
            
        # Shoot if target in range
        if self.target:
            if self.cooldown == 0:
                self.shoot(projectiles)
                self.cooldown = self.fire_rate
                
    # def find_target(self, enemies: List['Enemy']) -> 'Enemy' or None:
    #     closest_enemy = None
    #     closest_dist = float('inf')
        
    #     for enemy in enemies:
    #         dist = math.hypot(self.x - enemy.x, self.y - enemy.y)
    #         if dist <= self.range and dist < closest_dist:
    #             closest_dist = dist
    #             closest_enemy = enemy
                
    #     return closest_enemy
        
    def shoot(self, projectiles: List['Projectile']):
        # Create projectile towards target
        proj = Projectile(self.x, self.y, self.target, self.damage)
        projectiles.append(proj)
        
    def draw_range(self, screen: pygame.Surface):
        # Draw attack range (optional, for debugging/placement)
        if pygame.mouse.get_pressed()[0]:  # Only show when placing
            range_surface = pygame.Surface((self.range * 2, self.range * 2), pygame.SRCALPHA)
            pygame.draw.circle(range_surface, (255, 255, 255, 30), 
                             (self.range, self.range), self.range)
            screen.blit(range_surface, (self.x - self.range, self.y - self.range))
            
    def draw(self, screen: pygame.Surface):
        # Draw tower
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.size//2)
        pygame.draw.circle(screen, (255, 255, 255), (self.x, self.y), self.size//2, 3)
        
        # Draw aiming line to target
        if self.target:
            pygame.draw.line(screen, (255, 0, 0), (self.x, self.y), 
                           (self.target.x, self.target.y), 2)
            

class EvenTower(Tower):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, tower_type="even")
        self.range = 120
        self.damage = 15
        self.fire_rate = 30
        self.cost = 75
        self.color = (0, 255, 255)

    def find_target(self, enemies: List['Enemy']) -> 'Enemy' or None:
        # Prioritize enemies with even number
        even_enemies = [e for e in enemies if e.number % 2 == 0]
        if even_enemies:
            return super().find_target(even_enemies)
        return super().find_target(enemies)

class OddTower(Tower):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, tower_type="odd")
        self.range = 120
        self.damage = 15
        self.fire_rate = 30
        self.cost = 75
        self.color = (255, 0, 255)

    def find_target(self, enemies: List['Enemy']) -> 'Enemy' or None:
        # Prioritize enemies with odd number
        odd_enemies = [e for e in enemies if e.number % 2 == 1]
        if odd_enemies:
            return super().find_target(odd_enemies)
        return super().find_target(enemies)



class Projectile:
    def __init__(self, x: int, y: int, target: 'Enemy', damage: int):
        self.x = x
        self.y = y
        self.target = target
        self.damage = damage
        self.speed = 8
        self.color = (255, 255, 0)
        self.size = 6
        
    def update(self, enemies: List['Enemy']):
        if not self.target or self.target.health <= 0:
            return False  # Remove this projectile
            
        # Move towards target
        dx = self.target.x - self.x
        dy = self.target.y - self.y
        dist = math.hypot(dx, dy)
        
        if dist < self.speed:
            # Hit target
            self.target.take_damage(self.damage)
            return False
            
        # Move towards target
        self.x += (dx / dist) * self.speed
        self.y += (dy / dist) * self.speed
        return True
        
    def draw(self, screen: pygame.Surface):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)