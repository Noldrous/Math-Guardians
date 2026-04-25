import pygame
from towers import *

class UpgradeManager:
    def __init__(self, screen_height):
        self.costs = {"machinegun": 50, "sniper": 100, "bazooka": 150}
        self.damage_bonus = {"machinegun": 3, "sniper": 15, "bazooka": 20}

        self.ammo_bonus = {"machinegun": 5, "sniper": 2, "bazooka": 1}
        
        # --- BAGONG DAGDAG: Ilang bala ang madadagdag kada upgrade ---
        self.ammo_bonus = {"machinegun": 5, "sniper": 2, "bazooka": 1}
        
        self.small_font = pygame.font.SysFont("Arial", 16)
        self.popup_font = pygame.font.SysFont("Arial", 20, bold=True)
        
        btn_y = screen_height - 700 
        btn_size = (80, 80)
        
        button_info = [
            ("machinegun", "assets/img/upgrade_button/upgrade_machine_gun.webp", 40),
            ("sniper", "assets/img/upgrade_button/upgrade_sniper.webp", 160),
            ("bazooka", "assets/img/upgrade_button/upgrade_bazooka.webp", 280)
        ]
        
        self.images = {}
        self.buttons = {}
        
        for gun, path, x_pos in button_info:
            img = pygame.image.load(path).convert_alpha()
            self.images[gun] = pygame.transform.scale(img, btn_size)
            self.buttons[gun] = pygame.Rect(x_pos, btn_y, btn_size[0], btn_size[1])

        self.popup_msg = ""
        self.popup_timer = -2000 
        self.duration = 1500
        self.fade_time = 300

    def draw(self, screen):
        for gun, rect in self.buttons.items():
            screen.blit(self.images[gun], rect)

            cost_text = self.small_font.render(f"{self.costs[gun]} Coins", True, (255, 215, 0))
            cost_rect = cost_text.get_rect(centerx=rect.centerx, top=rect.bottom + 5)
            screen.blit(cost_text, cost_rect)

        elapsed = pygame.time.get_ticks() - self.popup_timer
        

        if elapsed >= self.duration or self.popup_msg == "":
            return

        if elapsed < self.fade_time:
            alpha = (elapsed / self.fade_time) * 255                           
        elif elapsed > (self.duration - self.fade_time):
            alpha = 255 - ((elapsed - (self.duration - self.fade_time)) / self.fade_time) * 255 
        else:
            alpha = 255                    

        alpha = max(0, min(255, int(alpha))) 

        color = (50, 255, 50) if "UPGRADED" in self.popup_msg else (255, 50, 50)
        text = self.popup_font.render(self.popup_msg, True, color)
        shadow = self.popup_font.render(self.popup_msg, True, (0, 0, 0))

        fade_surface = pygame.Surface(text.get_size(), pygame.SRCALPHA)
        fade_surface.blit(shadow, (2, 2))
        fade_surface.blit(text, (0, 0))
        fade_surface.set_alpha(alpha)

        center_x, center_y = screen.get_width() // 2, screen.get_height() // 2
        screen.blit(fade_surface, fade_surface.get_rect(center=(center_x, center_y - 50)))

    def handle_click(self, mouse_pos, coins, placed_towers):
        for gun, rect in self.buttons.items():
            if rect.collidepoint(mouse_pos):
                cost = self.costs[gun]
                
                if coins >= cost:
                    coins -= cost
                    self.costs[gun] = int(cost * 1.5)
                    
                    BaseTower.GUN_CONFIGS[gun]["damage"] += self.damage_bonus[gun]
                    BaseTower.GUN_CONFIGS[gun]["max_ammo"] += self.ammo_bonus[gun]
                    

                    for tower in placed_towers:
                        if tower.gun_type == gun:
                            tower.damage = BaseTower.GUN_CONFIGS[gun]["damage"]
                            tower.max_ammo = BaseTower.GUN_CONFIGS[gun]["max_ammo"]
                            tower.current_ammo = tower.max_ammo
                    
                    self.trigger_popup(f"{gun.upper()} UPGRADED!")
                    print(f"{gun} upgraded! New damage: {BaseTower.GUN_CONFIGS[gun]['damage']}")
                else:
                    self.trigger_popup("NOT ENOUGH COINS!")
                    print("Not enough coins!")
                
                break 
                
        return coins

    def trigger_popup(self, message):
        self.popup_msg = message
        self.popup_timer = pygame.time.get_ticks()