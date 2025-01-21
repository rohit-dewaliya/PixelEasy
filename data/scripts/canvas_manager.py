import pygame

from data.scripts.image_functions import scale_image_size, load_image


class CanvasManager:
    def __init__(self, display, display_pos):
        self.display = display
        self.display_pos = display_pos
        self.surface_size = [32, 32]
        self.scale_size = 15
        self.surface = pygame.Surface(self.surface_size)
        self.surface_pos = [0, 0]
        self.find_pos()
        self.increase_size = 0.3
        self.alpha_image = load_image('alpha_background.png').convert()

    def find_pos(self):
        self.surface_pos[0] = ((self.display.get_width() - self.surface_size[0] * self.scale_size) // 2 -
                            self.display_pos[0])
        self.surface_pos[1] = ((self.display.get_height() - self.surface_size[1] * self.scale_size) // 2 -
                             self.display_pos[1])

    def display_surface(self, mouse_pos):
        if self.display_pos[0] < mouse_pos[0] < self.display_pos[0] + self.display.get_width() and self.display_pos[
            1] < mouse_pos[1] < self.display_pos[1] + self.display.get_height():
            event = pygame.event.get()
            if event and event[0].type == pygame.MOUSEBUTTONDOWN:
                if event[0].button == 4:
                    self.scale_size += self.increase_size
                    if self.scale_size == 15:
                        self.scale_size = 15
                elif event[0].button == 5:
                    self.scale_size -= self.increase_size
                    if self.scale_size <= 1:
                        self.scale_size = 1
                self.find_pos()

        self.surface.blit(self.alpha_image, (0, 0))
        self.display.blit(scale_image_size(self.surface, self.surface_size[0] * self.scale_size, self.surface_size[1] *
            self.scale_size), [self.surface_pos[0] + self.display_pos[0], self.surface_pos[1] + self.display_pos[1]])

