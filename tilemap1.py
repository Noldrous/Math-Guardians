import pygame
from towers import *
from assets import *

class TileMap:
    def __init__(self):
        # =========================
        # GRID CONFIG
        # =========================
        self.cell_size = 120  # big enough for towers

        self.cols = 3
        self.rows = 5

        self.offset_x = 220 # LEFT SIDE BUILD ZONE
        self.offset_y = 120

        self.grid_width = self.cols * self.cell_size
        self.grid_height = self.rows * self.cell_size

        # (col, row) -> tower
        self.occupied = {}
        self.placed_towers = []

        # =========================
        # UI (tower selection boxes)
        # =========================
        self.tower_types = ["machinegun", "sniper", "bazooka"]
        self.tower_labels = ["Machine Gun Tower", "Sniper Tower", "Bazooka Tower"]
        self.boxes = []
        for i in range(3):
            self.boxes.append(pygame.Rect(20, 250 + (i * 90), 50, 50))

        self.colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
        self.color_labels = ["Red", "Green", "Blue"]

        self.holding_tower_type = None
        self.holding_color = None
        self.selected_box_index = -1
        self.show_menu = False

    # =========================
    # GRID CONVERSION
    # =========================
    def get_grid_pos(self, pos):
        x, y = pos

        # apply offsets
        x -= self.offset_x
        y -= self.offset_y

        if x < 0 or y < 0:
            return None

        col = x // self.cell_size
        row = y // self.cell_size

        if col < 0 or col >= self.cols or row < 0 or row >= self.rows:
            return None

        return int(col), int(row)


    def get_world_pos(self, grid_pos):
        col, row = grid_pos

        x = self.offset_x + col * self.cell_size + self.cell_size // 2
        y = self.offset_y + row * self.cell_size + self.cell_size // 2

        return x, y

    # =========================
    # INPUT
    # =========================
    def handle_click(self, pos):

        # -------------------------
        # PLACE TOWER
        # -------------------------
        if self.holding_color is not None and self.holding_tower_type is not None:

            grid = self.get_grid_pos(pos)

            if grid is None:
                self.holding_color = None
                self.holding_tower_type = None
                return

            if grid in self.occupied:
                self.holding_color = None
                self.holding_tower_type = None
                return

            x, y = self.get_world_pos(grid)

            if self.holding_color == (255, 0, 0):
                tower = RedTower(x, y, gun_type=self.holding_tower_type)
            elif self.holding_color == (0, 255, 0):
                tower = GreenTower(x, y, gun_type=self.holding_tower_type)
            elif self.holding_color == (0, 0, 255):
                tower = BlueTower(x, y, gun_type=self.holding_tower_type)
            else:
                return

            self.occupied[grid] = tower
            self.placed_towers.append(tower)

            self.holding_color = None
            self.holding_tower_type = None
            return

        # -------------------------
        # COLOR MENU
        # -------------------------
        if self.show_menu:
            box = self.boxes[self.selected_box_index]

            for i in range(len(self.colors)):
                menu_btn = pygame.Rect(box.right + 10 + (i * 45), box.top + 15, 35, 35)

                if menu_btn.collidepoint(pos):
                    self.holding_color = self.colors[i]
                    self.holding_tower_type = self.tower_types[self.selected_box_index]

            self.show_menu = False
            return

        # -------------------------
        # SELECT UI BOX
        # -------------------------
        for i, box in enumerate(self.boxes):
            if box.collidepoint(pos):
                self.selected_box_index = i
                self.show_menu = True

    # =========================
    # DRAW
    # =========================
    def draw(self, screen):
        grid_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        pygame.draw.rect(
            grid_surface,
            (25, 25, 25, 100), 
            (self.offset_x, self.offset_y, self.grid_width, self.grid_height)
        )
        for c in range(self.cols + 1):
            x = self.offset_x + c * self.cell_size
            pygame.draw.line(
                grid_surface,
                (60, 60, 60, 150),
                (x, self.offset_y),
                (x, self.offset_y + self.grid_height)
            )

        for r in range(self.rows + 1):
            y = self.offset_y + r * self.cell_size
            pygame.draw.line(
                grid_surface, 
                (60, 60, 60, 150),
                (self.offset_x, y),
                (self.offset_x + self.grid_width, y)
            )

        screen.blit(grid_surface, (0, 0))

        # UI boxes with tower type labels
        font_small = pygame.font.SysFont("Arial", 9)
        for i, box in enumerate(self.boxes):
            # Highlight selected box
            if i == self.selected_box_index and self.show_menu:
                pygame.draw.rect(screen, (100, 200, 255), box)
            else:
                pygame.draw.rect(screen, (200, 200, 200), box)
            
            pygame.draw.rect(screen, (0, 0, 0), box, 2)
            
            # Draw tower type label
            label = self.tower_labels[i]
            lines = label.split()
            for j, line in enumerate(lines):
                text = font_small.render(line, True, (0, 0, 0))
                text_rect = text.get_rect(center=(box.centerx, box.centery - 5 + j * 10))
                screen.blit(text, text_rect)

        # color menu
        if self.show_menu:
            box = self.boxes[self.selected_box_index]
            font_tiny = pygame.font.SysFont("Arial", 8)

            for i, col in enumerate(self.colors):
                menu_rect = pygame.Rect(box.right + 10 + (i * 45), box.top + 15, 35, 35)
                pygame.draw.rect(screen, col, menu_rect)
                pygame.draw.rect(screen, (0, 0, 0), menu_rect, 2)
                
                # Draw color label
                color_label = self.color_labels[i]
                label_text = font_tiny.render(color_label, True, (255, 255, 255) if sum(col) < 383 else (0, 0, 0))
                label_rect = label_text.get_rect(center=(menu_rect.centerx, menu_rect.centery + 20))
                screen.blit(label_text, label_rect)

        # towers
        for tower in self.placed_towers:
            tower.draw(screen)

        # preview
        if self.holding_color is not None and self.holding_tower_type is not None:
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