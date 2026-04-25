from setting import *
from abc import ABC, abstractmethod
from typing import List, Tuple, Optional
from enemies import Enemy

class TowerProjectile:
    # Bullet that travels from tower to enemy
    
    def __init__(self, x: int, y: int, target, damage: int, color: Tuple[int, int, int]):
        self.x = x
        self.y = y
        self.target = target
        self.damage = damage
        self.color = color
        self.speed = 8  # pixels per frame
        self.radius = 5
        self.active = True
        
    def update(self) -> bool:
        # Move bullet toward target. Returns True if bullet is still active
        if not self.target or not self.active:
            self.active = False
            return False
        
        # Check if target is still alive
        if not hasattr(self.target, 'health') or self.target.health <= 0:
            self.active = False
            return False
            
        # Calculate direction to target
        dx = self.target.pos_x - self.x
        dy = self.target.pos_y - self.y
        dist = math.hypot(dx, dy)
        
        if dist < self.radius + 15:  # Hit the target
            self.active = False
            return False
        
        if dist > 0:
            # Move toward target
            self.x += (dx / dist) * self.speed
            self.y += (dy / dist) * self.speed
            
        return True
        
    def draw(self, screen: pygame.Surface):
        # Draw bullet
        if self.active:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
            pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), self.radius, 1)

class BaseTower(ABC):
    # Abstract base class for all towers
    
    def __init__(self, x: int, y: int, range_radius: int, damage: int, 
                 fire_rate: int, cost: int, color: Tuple[int, int, int]):
        self.x = x
        self.y = y
        self.range_radius = range_radius
        self.damage = damage
        self.fire_rate = fire_rate  # frames between shots
        self.cooldown = 0
        self.cost = cost
        self.color = color
        self.size = 40
        self.target = None
        
    @abstractmethod
    def is_valid_target(self, enemy) -> bool:      # DEFINE VALID TARGETS FOR EACH TOWER TYPE
        # Define targeting logic for each tower type
        pass
    
    def update(self, enemies: List, projectiles: List):
        # Common update logic for all towers
        self.target = self.find_target(enemies)
        
        if self.cooldown > 0:
            self.cooldown -= 1
            return
            
        if self.target and self.cooldown == 0:
            self.shoot(projectiles)
            self.cooldown = self.fire_rate
            
    def find_target(self, enemies: List) -> Optional: # FINDS CLOSEST VALID TARGET 
        # Find closest valid target in range
        closest_enemy = None
        closest_dist = float('inf')
        
        for enemy in enemies:
            if not self.is_valid_target(enemy):
                continue
            
            # Check if enemy has required position attributes
            if not hasattr(enemy, 'pos_x') or not hasattr(enemy, 'pos_y'):
                continue
                
            dist = math.hypot(self.x - enemy.pos_x, self.y - enemy.pos_y)
            if dist <= self.range_radius and dist < closest_dist:
                closest_dist = dist
                closest_enemy = enemy
                
        return closest_enemy
        
    def shoot(self, projectiles: List):
        # Create projectile targeting enemy
        proj = TowerProjectile(self.x, self.y, self.target, self.damage, self.color)
        projectiles.append(proj)
        
    def draw_range(self, screen: pygame.Surface):
        # Draw attack range preview
        if pygame.mouse.get_pressed()[0]:
            range_surface = pygame.Surface((self.range_radius * 2, self.range_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(range_surface, (*self.color, 40), 
                             (self.range_radius, self.range_radius), self.range_radius)
            screen.blit(range_surface, (self.x - self.range_radius, self.y - self.range_radius))
            
    def draw(self, screen: pygame.Surface):
        # Draw tower and targeting line
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.size//2)
        pygame.draw.circle(screen, (255, 255, 255), (self.x, self.y), self.size//2, 3)
        
        if self.target:
            pygame.draw.line(screen, (255, 255, 0), (self.x, self.y), 
                           (self.target.pos_x, self.target.pos_y), 2)
            
class RedTower(BaseTower):
    #ONLY TARGETS EXACT RED ENEMIES
    VALID_TARGET = (255, 0, 0)

    def __init__(self, x: int, y: int):
        super().__init__(x, y,
                        range_radius=999,
                        damage=20,
                        fire_rate=30,
                        cost=100,
                        color=(255, 0, 0))

    def is_valid_target(self, enemy) -> bool:
        # Only target red enemies
        return hasattr(enemy, 'color') and enemy.color == self.VALID_TARGET

    def target_color(self) -> Tuple[int, int, int]:
        # Return the color of valid targets for this tower
        return self.VALID_TARGET
    
    def shoot(self, projectiles: List):
        # Override shoot to add red glow effect
        super().shoot(projectiles)
        # Add red glow effect (could be implemented as a temporary visual effect on the tower)
    
class BlueTower(BaseTower):
    # ONLY TARGETS EXACT BLUE ENEMIES
    VALID_TARGET = (0, 0, 255)

    def __init__(self, x: int, y: int):
        super().__init__(x, y,
                        range_radius=999,
                        damage=20,
                        fire_rate=30,
                        cost=100,
                        color=(0, 0, 255))

    def is_valid_target(self, enemy) -> bool:
        # Only target blue enemies
        return hasattr(enemy, 'color') and enemy.color == self.VALID_TARGET

    def target_color(self) -> Tuple[int, int, int]:
        # Return the color of valid targets for this tower
        return self.VALID_TARGET
    
    def shoot(self, projectiles: List):
        # Override shoot to add blue glow effect
        super().shoot(projectiles)
        # Add blue glow effect (could be implemented as a temporary visual effect on the tower)

class GreenTower(BaseTower):
    # ONLY TARGETS EXACT GREEN ENEMIES
    VALID_TARGET = (0, 255, 0)

    def __init__(self, x: int, y: int):
        super().__init__(x, y,
                        range_radius=999,
                        damage=20,
                        fire_rate=30,
                        cost=100,
                        color=(0, 255, 0))

    def is_valid_target(self, enemy) -> bool:
        # Only target green enemies
        return hasattr(enemy, 'color') and enemy.color == self.VALID_TARGET

    def target_color(self) -> Tuple[int, int, int]:
        # Return the color of valid targets for this tower
        return self.VALID_TARGET
    
    def shoot(self, projectiles: List):
        # Override shoot to add green glow effect
        super().shoot(projectiles)
        # Add green glow effect (could be implemented as a temporary visual effect on the tower)

class YellowTower(BaseTower):
    # ONLY TARGETS EXACT YELLOW ENEMIES
    VALID_TARGET = (255, 255, 0)

    def __init__(self, x: int, y: int):
        super().__init__(x, y,
                        range_radius=999,
                        damage=20,
                        fire_rate=30,
                        cost=100,
                        color=(255, 255, 0))

    def is_valid_target(self, enemy) -> bool:
        # Only target yellow enemies
        return hasattr(enemy, 'color') and enemy.color == self.VALID_TARGET

    def target_color(self) -> Tuple[int, int, int]:
        # Return the color of valid targets for this tower
        return self.VALID_TARGET

    def shoot(self, projectiles: List):
        # Override shoot to add yellow glow effect
        super().shoot(projectiles)
        #Add yellow glow effect (could be implemented as a temporary visual effect on the tower) #