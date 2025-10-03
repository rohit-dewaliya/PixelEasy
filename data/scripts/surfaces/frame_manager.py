import pygame

from data.scripts.surfaces.menu_manager import MenuManager
from data.scripts.surfaces.pop_up_windows import ask_layer_name


class FrameManager():
    def __init__(self, display, display_pos, canvas):
        self.display = display
        self.display_pos = display_pos
        self.display_size = display.get_size()

        self.canvas = canvas

        self.button_surface_size = [50, self.display_size[1]]
        self.button_surface_pos = [self.display_size[0] - self.button_surface_size[0], 0]
        self.button_surface = pygame.Surface(self.button_surface_size)
        self.border = 1

        self.menu_buttons = ['add new frame', 'add new layer']
        self.tooltip_offset = [self.button_surface_size[0], 0]
        self.menu_manager = MenuManager(self.button_surface, self.button_surface_pos, self.display,
                                        self.menu_buttons, self.tooltip_offset)

    def reset_display(self, display, display_pos):
        self.display = display
        self.display_size = display.get_size()
        self.display_pos = display_pos

        self.button_surface_size = [50, self.display_size[1]]
        self.button_surface_pos = [self.display_size[0] - self.button_surface_size[0], 0]
        self.button_surface = pygame.Surface(self.button_surface_size)

        self.menu_manager.reset_displays(self.button_surface, self.button_surface_pos, self.display)

    def display_components(self, mouse_pos, events, scroll=(0, 0)):
        mouse_pos = [mouse_pos[0] - self.display_pos[0], mouse_pos[1] - self.display_pos[1]]
        self.button_surface.fill((0, 0, 0))
        pygame.draw.line(self.display, (255, 255, 255), (self.button_surface_pos[0] - self.border,
            self.button_surface_pos[1]), (self.button_surface_pos[0] - self.border, self.button_surface_size[1]),
                         self.border)

        self.menu_manager.display_buttons(mouse_pos, events)

        if self.menu_manager.selected_button == "add new layer":
            name = ask_layer_name()
            if name:
                self.canvas.add_layer(name)
            self.menu_manager.selected_button = None
            print(self.canvas.image)
        elif self.menu_manager.selected_button == "add new frame":
            self.canvas.image[self.canvas.selected_layer].add_frame()
            print("\n\n\n")
            for layer in self.canvas.image:
                print(layer.frames)
            self.menu_manager.selected_button = None

        self.display.blit(self.button_surface, self.button_surface_pos)

