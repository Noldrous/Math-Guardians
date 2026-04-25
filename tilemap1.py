import pygame
from towers import *

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
        self.boxes = []
        for i in range(3):
            self.boxes.append(pygame.Rect(20, 250 + (i * 90), 50, 50))

        self.colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]

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

            for i in range(len(self.colors)):
                menu_btn = pygame.Rect(box.right + 10 + (i * 45), box.top + 15, 35, 35)

                if menu_btn.collidepoint(pos):
                    self.holding_color = self.colors[i]

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

        # grid background (shifted RIGHT by offset_x)
        pygame.draw.rect(
            screen,
            (25, 25, 25),
            (self.offset_x, self.offset_y, self.grid_width, self.grid_height)
        )

        # vertical lines
        for c in range(self.cols + 1):
            x = self.offset_x + c * self.cell_size
            pygame.draw.line(
                screen,
                (60, 60, 60),
                (x, self.offset_y),
                (x, self.offset_y + self.grid_height)
            )

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
