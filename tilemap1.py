import pygame
<<<<<<< HEAD
=======
import math
>>>>>>> f0012c61fae2664127376c9a33f5a3615fa5a15a
from towers import *

class TileMap:
    def __init__(self):
        # =========================
        # GRID CONFIG
        # =========================
        self.cell_size = 120  # big enough for towers

        self.cols = 3
        self.rows = 6

        self.offset_x = 220 # LEFT SIDE BUILD ZONE
        self.offset_y = 0

        self.grid_width = self.cols * self.cell_size
        self.grid_height = self.rows * self.cell_size

        # (col, row) -> tower
        self.occupied = {}
        self.placed_towers = []

        # =========================
        # UI (tower selection boxes)
        # =========================
        self.boxes = []
<<<<<<< HEAD
        for i in range(3):
            self.boxes.append(pygame.Rect(20, 250 + (i * 90), 50, 50))

        self.colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]

        self.holding_color = None
        self.selected_box_index = -1
        self.show_menu = False
=======
        
        for i in range(5):
            self.boxes.append(pygame.Rect(20, 130 + (i * 90), 50, 50))
        
        # Dito na ma-i-store ang mga actual Tower objects (RedTower, GreenTower, etc.)
        self.placed_towers = [] 

        self.selected_box_index = -1 
        self.holding_color = None    
        self.show_menu = False        

        self.colors = [(255,0,0), (0,255,0), (0,0,255)] 
>>>>>>> f0012c61fae2664127376c9a33f5a3615fa5a15a

    # =========================
    # GRID CONVERSION
    # =========================
    def get_grid_pos(self, pos):
        x, y = pos

        # apply offset
        x -= self.offset_x

        if x < 0:
            return None

        col = x // self.cell_size
        row = y // self.cell_size

        if col < 0 or col >= self.cols or row < 0 or row >= self.rows:
            return None

        return int(col), int(row)


    def get_world_pos(self, grid_pos):
        col, row = grid_pos

        x = self.offset_x + col * self.cell_size + self.cell_size // 2
        y = row * self.cell_size + self.cell_size // 2

        return x, y

    # =========================
    # INPUT
    # =========================
    def handle_click(self, pos):
<<<<<<< HEAD

        # -------------------------
        # PLACE TOWER
        # -------------------------
        if self.holding_color is not None:

            grid = self.get_grid_pos(pos)

            if grid is None:
                self.holding_color = None
                return

            if grid in self.occupied:
                self.holding_color = None
                return

            x, y = self.get_world_pos(grid)

            if self.holding_color == (255, 0, 0):
                tower = RedTower(x, y)
            elif self.holding_color == (0, 255, 0):
                tower = GreenTower(x, y)
            elif self.holding_color == (0, 0, 255):
                tower = BlueTower(x, y)
            else:
                return

            self.occupied[grid] = tower
            self.placed_towers.append(tower)

            self.holding_color = None
            return

        # -------------------------
        # COLOR MENU
        # -------------------------
        if self.show_menu:
            box = self.boxes[self.selected_box_index]

=======
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
>>>>>>> f0012c61fae2664127376c9a33f5a3615fa5a15a
            for i in range(len(self.colors)):
                menu_btn = pygame.Rect(box.right + 10 + (i * 45), box.top + 15, 35, 35)

                if menu_btn.collidepoint(pos):
                    self.holding_color = self.colors[i]

            self.show_menu = False
            return

<<<<<<< HEAD
        # -------------------------
        # SELECT UI BOX
        # -------------------------
        for i, box in enumerate(self.boxes):
            if box.collidepoint(pos):
=======
        # Kapag kinlick ang isa sa mga gray boxes
        for i in range(len(self.boxes)):
            if self.boxes[i].collidepoint(pos):
>>>>>>> f0012c61fae2664127376c9a33f5a3615fa5a15a
                self.selected_box_index = i
                self.show_menu = True

    # =========================
    # DRAW
    # =========================
    def draw(self, screen):

        # grid background (shifted RIGHT by offset_x)
        pygame.draw.rect(
            screen,
            (25, 25, 25),
            (self.offset_x, 0, self.grid_width, self.grid_height)
        )

        # vertical lines
        for c in range(self.cols + 1):
            x = self.offset_x + c * self.cell_size
            pygame.draw.line(screen, (60, 60, 60), (x, 0), (x, self.grid_height))

        # horizontal lines
        for r in range(self.rows + 1):
            y = r * self.cell_size
            pygame.draw.line(screen, (60, 60, 60),
                            (self.offset_x, y),
                            (self.offset_x + self.grid_width, y))

        # UI boxes
        for box in self.boxes:
            pygame.draw.rect(screen, (200, 200, 200), box)
            pygame.draw.rect(screen, (0, 0, 0), box, 2)

        # color menu
        if self.show_menu:
            box = self.boxes[self.selected_box_index]
<<<<<<< HEAD

            for i, col in enumerate(self.colors):
                pygame.draw.rect(
                    screen,
                    col,
                    (box.right + 10 + (i * 45), box.top + 15, 35, 35)
                )

        # towers
        for tower in self.placed_towers:
            tower.draw(screen)

        # preview
        if self.holding_color is not None:
            m = pygame.mouse.get_pos()
            grid = self.get_grid_pos(m)

            if grid:
                x, y = self.get_world_pos(grid)
                pygame.draw.rect(
                    screen,
                    self.holding_color,
                    (x - self.cell_size//2, y - self.cell_size//2,
                     self.cell_size, self.cell_size),
                    2
                )
=======
            for i in range(len(self.colors)): 
                pygame.draw.rect(screen, self.colors[i], (box.right + 10 + (i*45), box.top + 15, 35, 35))

        # Tatawagin na natin yung built-in draw() function ng mga Towers
        for tower in self.placed_towers:
            tower.draw(screen)

        # Preview box kapag hawak ng mouse ang tower bago ilagay
        if self.holding_color != None:
            m_pos = pygame.mouse.get_pos()
            pygame.draw.rect(screen, self.holding_color, (m_pos[0]-20, m_pos[1]-20, 40, 40), 2)
>>>>>>> f0012c61fae2664127376c9a33f5a3615fa5a15a
