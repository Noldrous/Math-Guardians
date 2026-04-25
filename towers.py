from setting import *
from abc import ABC, abstractmethod
from typing import List, Tuple, Optional
from enemies import Enemy

class TowerProjectile:
    # Base class for all tower projectiles
    
    def __init__(self, x: int, y: int, target, damage: int, color: Tuple[int, int, int], 
                 radius: int = 5, speed: int = 8, projectile_type: str = "default"):
        self.x = x
        self.y = y
        self.prev_x = x  # For trail effects
        self.prev_y = y
        self.target = target
        self.damage = damage
        self.color = color
        self.speed = speed
        self.radius = radius
        self.active = True
        self.projectile_type = projectile_type
        self.impact_radius = 0  # For AOE effects like bazooka
        
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
            # Store previous position for trail effects
            self.prev_x = self.x
            self.prev_y = self.y
            # Move toward target
            self.x += (dx / dist) * self.speed
            self.y += (dy / dist) * self.speed
            
        return True
        
    def draw(self, screen: pygame.Surface):
        # Draw bullet with type-specific visuals
        if self.active:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
            pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), self.radius, 1)


class MachineGunRound(TowerProjectile):
    # Fast-firing, low damage, small projectile
    def __init__(self, x: int, y: int, target, damage: int = 5):
        super().__init__(x, y, target, damage, color=(255, 100, 100), 
                        radius=3, speed=10, projectile_type="machinegun")
        
    def draw(self, screen: pygame.Surface):
        if self.active:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
            pygame.draw.circle(screen, (255, 200, 200), (int(self.x), int(self.y)), self.radius, 1)


class SniperRound(TowerProjectile):
    # Slow-firing, high damage, medium projectile, draws trailing line
    def __init__(self, x: int, y: int, target, damage: int = 35):
        super().__init__(x, y, target, damage, color=(100, 255, 100), 
                        radius=6, speed=12, projectile_type="sniper")
        
    def draw(self, screen: pygame.Surface):
        if self.active:
            # Draw trailing line
            pygame.draw.line(screen, (150, 200, 150), (int(self.prev_x), int(self.prev_y)), 
                           (int(self.x), int(self.y)), 2)
            # Draw projectile
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
            pygame.draw.circle(screen, (200, 255, 200), (int(self.x), int(self.y)), self.radius, 2)


class BazookaRound(TowerProjectile):
    # Slow-firing, high damage, large projectile, explosion on impact
    def __init__(self, x: int, y: int, target, damage: int = 40, splash_radius: int = 150):
        super().__init__(x, y, target, damage, color=(100, 150, 255), 
                        radius=12, speed=9, projectile_type="bazooka")
        self.impact_radius = 200  # Explosion radius for visual effect
        self.splash_radius = splash_radius  # Radius for splash damage
        self.has_exploded = False  # Track if projectile has already dealt splash damage
        
    def draw(self, screen: pygame.Surface):
        if self.active:
            # Draw projectile with glow
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
            pygame.draw.circle(screen, (200, 200, 255), (int(self.x), int(self.y)), self.radius, 3)

class BaseTower(ABC):
    # Abstract base class for all towers
    # Gun type configs: {type: (damage, fire_rate, cost)}
    GUN_CONFIGS = {
        "machinegun": {"damage": 5, "fire_rate": 8, "cost": 80, "rounds": 3},
        "sniper": {"damage": 35, "fire_rate": 60, "cost": 120, "rounds": 1},
        "bazooka": {"damage": 40, "fire_rate": 50, "cost": 150, "rounds": 1}
    }
    
    def __init__(self, x: int, y: int, tower_color: Tuple[int, int, int], 
                 gun_type: str = "machinegun", range_radius: int = 999):
        self.x = x
        self.y = y
        self.tower_color = tower_color  # Color of the tower and enemies it targets
        self.gun_type = gun_type  # Type of gun: machinegun, sniper, bazooka
        
        # Get gun stats
        gun_config = self.GUN_CONFIGS.get(gun_type, self.GUN_CONFIGS["machinegun"])
        self.damage = gun_config["damage"]
        self.fire_rate = gun_config["fire_rate"]
        self.cost = gun_config["cost"]
        self.rounds = gun_config["rounds"]
        
        self.range_radius = range_radius
        self.cooldown = 0
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
        # Fire based on gun type
        if not self.target:
            return
        
        if self.gun_type == "machinegun":
            self._shoot_machinegun(projectiles)
        elif self.gun_type == "sniper":
            self._shoot_sniper(projectiles)
        elif self.gun_type == "bazooka":
            self._shoot_bazooka(projectiles)
    
    def _shoot_machinegun(self, projectiles: List):
        # Fire 3 machine gun rounds with slight angle spread
        dx = self.target.pos_x - self.x
        dy = self.target.pos_y - self.y
        base_angle = math.atan2(dy, dx)
        
        for angle_offset in [-0.087, 0, 0.087]:  # ±5 degrees in radians
            angle = base_angle + angle_offset
            offset_dist = 5
            proj_x = self.x + math.cos(angle) * offset_dist
            proj_y = self.y + math.sin(angle) * offset_dist
            
            proj = MachineGunRound(proj_x, proj_y, self.target, self.damage)
            projectiles.append(proj)
    
    def _shoot_sniper(self, projectiles: List):
        # Fire one sniper round with trailing effect
        proj = SniperRound(self.x, self.y, self.target, self.damage)
        projectiles.append(proj)
    
    def _shoot_bazooka(self, projectiles: List):
        # Fire one bazooka round with explosion radius
        # You can customize splash_radius here (default is 150)
        proj = BazookaRound(self.x, self.y, self.target, self.damage, splash_radius=150)
        projectiles.append(proj)
        
    def draw_range(self, screen: pygame.Surface):
        # Draw attack range preview
        if pygame.mouse.get_pressed()[0]:
            range_surface = pygame.Surface((self.range_radius * 2, self.range_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(range_surface, (*self.tower_color, 40), 
                             (self.range_radius, self.range_radius), self.range_radius)
            screen.blit(range_surface, (self.x - self.range_radius, self.y - self.range_radius))
            
    def draw(self, screen: pygame.Surface):
        # Draw tower (triangle) and targeting line
        # Create triangle points centered at tower position
        radius = self.size // 2
        
        # Calculate rotation angle based on target direction
        angle = 0
        if self.target:
            dx = self.target.pos_x - self.x
            dy = self.target.pos_y - self.y
            angle = math.atan2(dy, dx)
        
        # Create triangle points and rotate them
        local_points = [
            (0, -radius),  # Top point
            (radius, radius),  # Bottom right
            (-radius, radius)   # Bottom left
        ]
        
        # Rotate points around center
        rotated_points = []
        for px, py in local_points:
            rotated_x = px * math.cos(angle) - py * math.sin(angle)
            rotated_y = px * math.sin(angle) + py * math.cos(angle)
            rotated_points.append((self.x + rotated_x, self.y + rotated_y))
        
        pygame.draw.polygon(screen, self.tower_color, rotated_points)
        pygame.draw.polygon(screen, (255, 255, 255), rotated_points, 3)
        
        if self.target:
            pygame.draw.line(screen, (255, 255, 0), (self.x, self.y), 
                           (self.target.pos_x, self.target.pos_y), 2)
            
class RedTower(BaseTower):
    # Targets RED enemies with selectable gun type
    VALID_TARGET = (255, 0, 0)

    def __init__(self, x: int, y: int, gun_type: str = "machinegun"):
        super().__init__(x, y, 
                        tower_color=(255, 0, 0),
                        gun_type=gun_type,
                        range_radius=999)

    def is_valid_target(self, enemy) -> bool:
        # Only target red enemies
        return hasattr(enemy, 'color') and enemy.color == self.VALID_TARGET

    def target_color(self) -> Tuple[int, int, int]:
        # Return the color of valid targets for this tower
        return self.VALID_TARGET
    
class BlueTower(BaseTower):
    # Targets BLUE enemies with selectable gun type
    VALID_TARGET = (0, 0, 255)

    def __init__(self, x: int, y: int, gun_type: str = "bazooka"):
        super().__init__(x, y,
                        tower_color=(0, 0, 255),
                        gun_type=gun_type,
                        range_radius=999)

    def is_valid_target(self, enemy) -> bool:
        # Only target blue enemies
        return hasattr(enemy, 'color') and enemy.color == self.VALID_TARGET

    def target_color(self) -> Tuple[int, int, int]:
        # Return the color of valid targets for this tower
        return self.VALID_TARGET

class GreenTower(BaseTower):
    # Targets GREEN enemies with selectable gun type
    VALID_TARGET = (0, 255, 0)

    def __init__(self, x: int, y: int, gun_type: str = "sniper"):
        super().__init__(x, y,
                        tower_color=(0, 255, 0),
                        gun_type=gun_type,
                        range_radius=999)

    def is_valid_target(self, enemy) -> bool:
        # Only target green enemies
        return hasattr(enemy, 'color') and enemy.color == self.VALID_TARGET

    def target_color(self) -> Tuple[int, int, int]:
        # Return the color of valid targets for this tower
        return self.VALID_TARGET