# import pygame
# # from tower import Tower

# class TileMap:
#     def __init__(self):
#         self.tile_size = 80
#         self.towers_list = []
#         self.selected_type = 0

#         self.button_1 = pygame.Rect(300, 640, 60, 60) # Red Button
#         self.button_2 = pygame.Rect(600, 640, 60, 60) # Green Button
#         self.button_3 = pygame.Rect(900, 640, 60, 60) # Blue Button

#     def handle_click(self, mouse_pos):   
#         x = mouse_pos[0]
#         y = mouse_pos[1]

#         if self.button_1.collidepoint(x, y):
#             self.selected_type = 1
            
#         elif self.button_2.collidepoint(x, y):
#             self.selected_type = 2
            
#         elif self.button_3.collidepoint(x, y):
#             self.selected_type = 3
   
#         elif self.selected_type > 0 and y < 640:
            
#             grid_x = (x // self.tile_size) * self.tile_size
#             grid_y = (y // self.tile_size) * self.tile_size

#             may_laman_na = False
#             for tower in self.towers_list:
#                 if tower.x == grid_x and tower.y == grid_y:
#                     may_laman_na = True
            
#             if may_laman_na == False:
#                 bagong_tower = Tower(grid_x, grid_y, self.tile_size, self.tile_size, self.selected_type)

#                 self.towers_list.append(bagong_tower)
                
#                 self.selected_type = 0 

#     def draw(self, surface):
#         pygame.draw.rect(surface, (80, 80, 80), (0, 640, 1280, 80))

#         pygame.draw.rect(surface, (255, 50, 50), self.button_1) # Red
#         pygame.draw.rect(surface, (50, 255, 50), self.button_2) # Green
#         pygame.draw.rect(surface, (50, 50, 255), self.button_3) # Blue


#         if self.selected_type == 1:
#             pygame.draw.rect(surface, (255, 255, 255), self.button_1, 3) #border
#         elif self.selected_type == 2:
#             pygame.draw.rect(surface, (255, 255, 255), self.button_2, 3) #border
#         elif self.selected_type == 3:
#             pygame.draw.rect(surface, (255, 255, 255), self.button_3, 3) #border


#         for tower in self.towers_list:
#             tower.draw(surface)