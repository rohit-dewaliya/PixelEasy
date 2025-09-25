import pygame

from data.scripts.tools.image_functions import load_image, scale_image_size


class CanvasManager:
    def __init__(self, display, display_pos, cursor, surface_size = [32, 32], scale = 2, max_scale = 3, min_scale =1):
        self.display = display
        self.display_size = self.display.get_size()
        self.display_pos = display_pos
        self.cursor = cursor

        self.surface_size = surface_size
        self.scale = scale
        self.max_scale = max_scale
        self.min_scale = min_scale
        self.surface = pygame.Surface(self.surface_size)
        self.surface_color = (255, 255, 255)
        self.surface_pos = [(self.display_size[0] - self.surface_size[0] * 2) // 2, (self.display_size[1]  -
                                                                                     self.surface_size[1]) // 2]
        self.surface_rect = pygame.Rect(*self.surface_pos, self.surface_size[0] * self.scale, self.surface_size[1] *
                                        self.scale)
        self.incease_size = 0.3
        self.change_pos = False
        self.fixed_pos = self.surface_pos


    def reset_display(self, display, display_pos):
        self.display = display
        self.display_pos = display_pos

    def repos_surface_rect(self, new_pos):
        self.surface_rect.topleft = new_pos

    def reset_surface_rect(self):
        self.surface_rect.width, self.surface_rect.height = [int(self.surface_size[0] * self.scale),
                                                           int(self.surface_size[1] * self.scale)]

    def zoom_in_and_out(self, mouse_pos, events):
        if self.surface_rect.collidepoint(mouse_pos):
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4:
                        self.scale = min(10, self.scale + self.incease_size)
                    elif event.button == 5:
                        self.scale = max(1, self.scale - self.incease_size)
            self.reset_surface_rect()

    def move_canvas(self, mouse_pos, events):
        # if self.surface_rect.collidepoint(mouse_pos):
        #     self.surface.fill((255, 0, 0))

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 2:
                    self.change_pos = True
                    self.fixed_pos = mouse_pos

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 2:
                    self.change_pos = False

            if event.type == pygame.MOUSEMOTION:
                if self.change_pos:
                    dx = mouse_pos[0] - self.fixed_pos[0]
                    dy = mouse_pos[1] - self.fixed_pos[1]

                    # move canvas
                    self.surface_pos[0] += dx
                    self.surface_pos[1] += dy

                    self.repos_surface_rect(self.surface_pos)
                    self.fixed_pos = mouse_pos

    def display_surface(self, mouse_pos, events = None):
        self.surface.fill(self.surface_color)
        mouse_pos = [mouse_pos[0] - self.display_pos[0], mouse_pos[1] - self.display_pos[1]]
        self.zoom_in_and_out(mouse_pos, events)
        self.move_canvas(mouse_pos, events)
        self.display.blit(pygame.transform.scale(self.surface, [self.surface_size[0] * self.scale, self.surface_size[
            1] * self.scale]), self.surface_pos)

#         self.surface_size = [320, 320]
#         self.scale_size = 2
#         self.surface = pygame.Surface(self.surface_size)
#         self.surface_pos = [0, 0]
#         self.find_pos()
#         self.increase_size = 0.3
#         self.alpha_image = load_image('alpha_background.png').convert()
#         self.fixed_pos = [0, 0]
#         self.change_pos = False
#
#     def find_mouse_pos(self, mouse_pos):
#         x = int((mouse_pos[0] - (self.surface_pos[0] + self.display_pos[0])) // self.scale_size)
#         y = int((mouse_pos[1] - (self.surface_pos[1] + self.display_pos[1])) // self.scale_size)
#         return x, y
#
#     def find_pos(self):
#         self.surface_pos[0] = ((self.display.get_width() - self.surface_size[0] * self.scale_size) // 2 -
#                                self.display_pos[0])
#         self.surface_pos[1] = ((self.display.get_height() - self.surface_size[1] * self.scale_size) // 2 -
#                                self.display_pos[1])
#
#     def move_canvas(self, mouse_pos, event):
#         if event.type == pygame.MOUSEBUTTONUP and event.button == 2:
#             self.change_pos = False
#
#         elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:
#             self.change_pos = True
#             self.fixed_pos = mouse_pos
#
#         if self.change_pos and event.type == pygame.MOUSEMOTION:
#             self.surface_pos[0] += mouse_pos[0] - self.fixed_pos[0]
#             self.surface_pos[1] += mouse_pos[1] - self.fixed_pos[1]
#             self.fixed_pos = mouse_pos
#
#     def zoom(self, pos):
#         self.surface_pos[0] = ((self.display.get_width() - pos[0] * self.scale_size) // 2 - self.display_pos[0])
#         self.surface_pos[1] = ((self.display.get_height() - pos[1] * self.scale_size) // 2 - self.display_pos[1])
#
#     def zoom_canvas(self, mouse_pos, event):
#         # Adjust the mouse position relative to the display
#         mouse_pos = [mouse_pos[0] - self.display_pos[0], mouse_pos[1] - self.display_pos[1]]
#
#         # Check if the mouse is within the canvas boundaries
#         if (self.surface_pos[0] + self.display_pos[0] <= mouse_pos[0] <= self.surface_pos[0] + self.display_pos[0] +
#                 self.surface_size[0] * self.scale_size and self.surface_pos[1] + self.display_pos[1] <= mouse_pos[1]
#                 <= self.surface_pos[1] + self.display_pos[1] + self.surface_size[1] * self.scale_size):
#
#             if event.type == pygame.MOUSEBUTTONDOWN:
#                 if event.button == 4:
#                     self.scale_size = min(10, self.scale_size + self.increase_size)
#                 elif event.button == 5:
#                     self.scale_size = max(1, self.scale_size - self.increase_size)
#                 x, y = self.find_mouse_pos(mouse_pos)
#                 pos = [x // 2, y // 2]
#                 self.zoom([pos[0], pos[1]])
#
#     def display_surface(self, mouse_pos):
#         if self.display_pos[0] < mouse_pos[0] < self.display_pos[0] + self.display.get_width() and self.display_pos[
#             1] < mouse_pos[1] < self.display_pos[1] + self.display.get_height():
#             events = pygame.event.get()
#             for event in events:
#                 self.move_canvas(mouse_pos, event)
#                 self.zoom_canvas(mouse_pos, event)
#
#         self.surface.blit(self.alpha_image, (0, 0))
#         self.display.blit(scale_image_size(self.surface, self.surface_size[0] * self.scale_size,
#                              self.surface_size[1] * self.scale_size),
#             [self.surface_pos[0] + self.display_pos[0], self.surface_pos[1] + self.display_pos[1]])