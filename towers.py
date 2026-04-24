from setting import *
from abc import ABC, abstractmethod
from typing import List, Tuple, Optional

class BaseTower(ABC):
    """Abstract base class for all towers"""
    
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
        self.target: Optional['Enemy'] = None
        
    @abstractmethod
    def is_valid_target(self, enemy: 'Enemy') -> bool:      # DEFINE VALID TARGETS FOR EACH TOWER TYPE
        """Define targeting logic for each tower type"""
        pass
    
    def update(self, enemies: List['Enemy'], projectiles: List['Projectile']):
        """Common update logic for all towers"""
        self.target = self.find_target(enemies)
        
        if self.cooldown > 0:
            self.cooldown -= 1
            return
            
        if self.target and self.cooldown == 0:
            self.shoot(projectiles)
            self.cooldown = self.fire_rate
            
    def find_target(self, enemies: List['Enemy']) -> Optional['Enemy']: # FINDS CLOSEST VALID TARGET 
        """Find closest valid target in range"""
        closest_enemy = None
        closest_dist = float('inf')
        
        for enemy in enemies:
            if not self.is_valid_target(enemy):
                continue
                
            dist = math.hypot(self.x - enemy.x, self.y - enemy.y)
            if dist <= self.range_radius and dist < closest_dist:
                closest_dist = dist
                closest_enemy = enemy
                
        return closest_enemy
        
    def shoot(self, projectiles: List['Projectile']):
        """Create projectile targeting enemy"""
        proj = Projectile(self.x, self.y, self.target, self.damage, self.color)
        projectiles.append(proj)
        
    def draw_range(self, screen: pygame.Surface):
        """Draw attack range preview"""
        if pygame.mouse.get_pressed()[0]:
            range_surface = pygame.Surface((self.range_radius * 2, self.range_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(range_surface, (*self.color, 40), 
                             (self.range_radius, self.range_radius), self.range_radius)
            screen.blit(range_surface, (self.x - self.range_radius, self.y - self.range_radius))
            
    def draw(self, screen: pygame.Surface):
        """Draw tower and targeting line"""
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.size//2)
        pygame.draw.circle(screen, (255, 255, 255), (self.x, self.y), self.size//2, 3)
        
        if self.target:
            pygame.draw.line(screen, (255, 255, 0), (self.x, self.y), 
                           (self.target.x, self.target.y), 2)
            
class RedTower(BaseTower):
    """ONLY TARGETS EXACT RED ENEMIES"""
    VALID_TARGET = (255, 0, 0)

    def __init__(self, x: int, y: int):
        super().__init__(x, y,
                        range_radius=150,
                        damage=20,
                        fire_rate=30,
                        cost=100,
                        color=(255, 0, 0))

    def target_color(self) -> Tuple[int, int, int]:
        """Return the color of valid targets for this tower"""
        return self.VALID_TARGET
    
class BlueTower(BaseTower):
    """ONLY TARGETS EXACT BLUE ENEMIES"""
    VALID_TARGET = (0, 0, 255)

    def __init__(self, x: int, y: int):
        super().__init__(x, y,
                        range_radius=150,
                        damage=20,
                        fire_rate=30,
                        cost=100,
                        color=(0, 0, 255))

    def target_color(self) -> Tuple[int, int, int]:
        """Return the color of valid targets for this tower"""
        return self.VALID_TARGET
    

class Projectiles:
    pass
