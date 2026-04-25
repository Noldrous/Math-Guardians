import pygame
import math
from towers import *

class TileMap:
    def __init__(self):
        self.boxes = []
        
        for i in range(5):
            self.boxes.append(pygame.Rect(20, 130 + (i * 90), 50, 50))
        
        # Dito na ma-i-store ang mga actual Tower objects (RedTower, GreenTower, etc.)
        self.placed_towers = [] 

        self.selected_box_index = -1 
        self.holding_color = None    
        self.show_menu = False        

        self.colors = [(255,0,0), (0,255,0), (0,0,255)] 

    def handle_click(self, pos):
        # Kapag may hawak nang kulay (ready na i-place ang tower)
        if self.holding_color != None:
            box = self.boxes[self.selected_box_index]
            
            # Check kung nasa loob ng valid placement row
            if pos[1] >= box.top and pos[1] <= box.bottom:
                if pos[0] > box.right and pos[0] <= 500:
                    
                    # Instantiate ang tamang Tower class base sa hawak na kulay
                    t_x, t_y = pos[0], pos[1] # Center position para sa tower
                    
                    if self.holding_color == (255, 0, 0):
                        self.placed_towers.append(RedTower(t_x, t_y))
                    elif self.holding_color == (0, 255, 0):
                        self.placed_towers.append(GreenTower(t_x, t_y))
                    elif self.holding_color == (0, 0, 255):
                        self.placed_towers.append(BlueTower(t_x, t_y))
            
            self.holding_color = None
            return

        # Kapag naka-open ang kulay na menu
        if self.show_menu == True:
            box = self.boxes[self.selected_box_index]
            for i in range(len(self.colors)):
                menu_btn = pygame.Rect(box.right + 10 + (i * 45), box.top + 15, 35, 35)
                if menu_btn.collidepoint(pos):
                    self.holding_color = self.colors[i]
            
            self.show_menu = False
            return

        # Kapag kinlick ang isa sa mga gray boxes
        for i in range(len(self.boxes)):
            if self.boxes[i].collidepoint(pos):
                self.selected_box_index = i
                self.show_menu = True

    def draw(self, screen):
        pygame.draw.line(screen, (255, 0, 0), (500, 0), (500, 720), 2)

        for box in self.boxes:
            pygame.draw.rect(screen, (200, 200, 200), box) # Gray box
            pygame.draw.rect(screen, (0, 0, 0), box, 2)    # Black border

        if self.show_menu == True:
            box = self.boxes[self.selected_box_index]
            for i in range(len(self.colors)): 
                pygame.draw.rect(screen, self.colors[i], (box.right + 10 + (i*45), box.top + 15, 35, 35))

        # Tatawagin na natin yung built-in draw() function ng mga Towers
        for tower in self.placed_towers:
            tower.draw(screen)

        # Preview box kapag hawak ng mouse ang tower bago ilagay
        if self.holding_color != None:
            m_pos = pygame.mouse.get_pos()
            pygame.draw.rect(screen, self.holding_color, (m_pos[0]-20, m_pos[1]-20, 40, 40), 2)