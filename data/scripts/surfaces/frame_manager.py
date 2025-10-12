import pygame

from data.scripts.surfaces.menu_manager import MenuManager
from data.scripts.surfaces.pop_up_windows import ask_layer_name
from data.scripts.tools.font import Font
from data.scripts.tools.image_functions import load_image, scale_image_size
from data.scripts.ui.button import IconButton, CircleButton, SurfaceButton

background = load_image('background.png', 100)
background_hover = load_image('background.png', 150)


class HorizontalButtons:
    def __init__(self, pos, size=(24, 24), buttons=()):
        self.pos = pos
        self.size = size
        self.buttons = buttons
        self.offset = [5, 0]
        self.selected_button = None

        self.create_buttons()

    def create_buttons(self):
        self.menu_buttons = {}
        x = 0
        for name in self.buttons:
            self.menu_buttons[name] = IconButton(self.pos[0] + x, self.pos[1], self.size[0], self.size[1], name)
            x += self.size[1] + self.offset[0]

    def display_buttons(self, display, mouse_pos, events, scroll=(0, 0)):
        for index, button in enumerate(self.menu_buttons.items()):
            name, button = button
            if button.display(display, True, mouse_pos, events, scroll):
                self.selected_button = name
            if name == self.selected_button:
                pygame.draw.rect(display, (255, 255, 255), (button.x - scroll[0], button.y -
                                                            scroll[1], button.width, button.height), 3)


class FrameButtons:
    def __init__(self, pos, size=(24, 24), buttons=(), selected_frame=0):
        self.pos = pos
        self.size = size
        self.buttons = buttons
        self.offset = [5, 0]
        self.selected_button = None

        self.create_buttons()

    def create_buttons(self):
        self.menu_buttons = {}
        x = 0
        for name in self.buttons:
            self.menu_buttons[name] = CircleButton(self.pos[0] + x, self.pos[1], self.size)
            x += self.size + self.offset[0]

    def display_buttons(self, display, mouse_pos, selected_button, events, scroll=(0, 0), function=None):
        for index, button in enumerate(self.menu_buttons.items()):
            name, button = button
            if button.display(display, True, mouse_pos, events, scroll):
                self.selected_button = name
                function(name)
            if name == selected_button:
                pygame.draw.rect(display, (255, 255, 0), (button.x - scroll[0], button.y -
                                                            scroll[1], button.width, button.height))

class SurfaceButtons:
    def __init__(self, pos, size=(24, 24), buttons=()):
        self.pos = pos
        self.size = size
        self.buttons = buttons
        self.offset = [10, 0]
        self.selected_button = None

        self.create_buttons()

    def create_buttons(self):
        self.menu_buttons = {}
        x = 0
        for i in range(self.buttons.total_frames):
            self.menu_buttons[i] = SurfaceButton(self.pos[0] + x, self.pos[1], self.size[0], self.size[1],
                                                 self.buttons.frames[i])

            x += self.size[0] + self.offset[0]

    def display_buttons(self, display, mouse_pos, selected_button, events, scroll=(0, 0), function=None):
        for index, button in enumerate(self.menu_buttons.items()):
            name, button = button
            if button.display(display, True, mouse_pos, events, scroll):
                self.selected_button = name
                function(name)
            if name == selected_button:
                pygame.draw.line(display, (255, 0, 0), (button.x + button.height, button.y - scroll[1]),
                                 (button.x + button.height, button.y + button.width - scroll[1]), 5)


class FrameManager:
    def __init__(self, display, display_pos, canvas, error_manager):
        self.display = display
        self.display_pos = display_pos
        self.display_size = display.get_size()
        self.error_manager = error_manager

        self.canvas = canvas


        self.button_surface_size = [50, self.display_size[1]]
        self.button_surface_pos = [self.display_size[0] - self.button_surface_size[0], 0]
        self.button_surface = pygame.Surface(self.button_surface_size)
        self.border = 1

        self.menu_buttons = ['play animation', 'pause animation', 'add new frame', 'add new layer']
        self.tooltip_offset = [self.button_surface_size[0], 0]
        self.menu_manager = MenuManager(self.button_surface, self.button_surface_pos, self.display,
                                        self.menu_buttons, self.tooltip_offset)

        self.layer_rect = [self.display_size[0] - self.button_surface_size[0], 30]
        self.background = scale_image_size(background, self.display_size[0], self.layer_rect[1])
        self.background_hover = scale_image_size(background_hover, self.display_size[0], self.layer_rect[1])

        self.text_font = Font('small_font.png', (255, 255, 255, 255), 2)
        self.text_hover_font = Font('small_font.png', (255, 255, 0, 255), 2)
        self.text_pos = [10, (self.layer_rect[1] - self.text_font.image_height) // 2]

        self.layer_buttons_offset = 3
        self.layer_buttons = ['cancel', 'up arrow', 'down arrow']
        self.layer_buttons_size = [self.layer_rect[1] - self.layer_buttons_offset * 2, self.layer_rect[1] - self.layer_buttons_offset * 2]
        self.layer_pos = [self.text_pos[0] + self.text_font.get_width(" " * 15), (self.layer_rect[1] -
                                                                                  self.layer_buttons_size[1]) // 2]

        self.layer_frame_button = ['frame circle']
        self.layer_frame_radius = self.layer_rect[1] - self.layer_buttons_offset * 2
        self.layer_frame_pos = [self.layer_pos[0] + self.layer_frame_radius * 5, (self.layer_rect[1] -
                                                                                  self.layer_frame_radius) // 2]

        self.scroll = [0, 0]
        self.min_scroll = 0

        self.add_layer_rect()

    def add_layer_rect(self):
        self.layer_background_rects = []
        self.layer_menu_buttons = []
        self.layer_frames = []
        pos = [0, 0]
        offset = 5
        for layer in self.canvas.image:
            rect = pygame.Rect(pos[0], pos[1], self.layer_rect[0], self.layer_rect[1])
            self.layer_background_rects.append(rect)

            self.layer_menu_buttons.append(HorizontalButtons([self.layer_pos[0], self.layer_pos[1] + pos[1]],
                                                             self.layer_buttons_size,
                                                             self.layer_buttons))

            self.layer_frames.append(SurfaceButtons([self.layer_frame_pos[0], self.layer_frame_pos[1] +
                                                           pos[1]], self.layer_buttons_size, layer))

            pos[1] += self.layer_rect[1] + offset

        self.min_scroll = pos[1] - self.display_size[1]

    def reset_display(self, display, display_pos):
        self.display = display
        self.display_size = display.get_size()
        self.display_pos = display_pos

        self.button_surface_size = [50, self.display_size[1]]
        self.button_surface_pos = [self.display_size[0] - self.button_surface_size[0], 0]
        self.button_surface = pygame.Surface(self.button_surface_size)

        self.menu_manager.reset_displays(self.button_surface, self.button_surface_pos, self.display)

        self.layer_rect[0] = self.display_size[0] - self.button_surface_size[0]

        for rect in self.layer_background_rects:
            rect.width = self.layer_rect[0]

        self.background = scale_image_size(background, self.display_size[0], 30)
        self.background_hover = scale_image_size(background_hover, self.display_size[0], 30)

    def display_layers(self, mouse_pos, events, scroll=(0, 0)):
        _hover = 0 < mouse_pos[0] < self.display.get_width() and  0 < mouse_pos[1] < self.display.get_height()
        if _hover:
            for e in events:
                if e.type == pygame.MOUSEBUTTONDOWN:
                    if e.button == 4 and self.scroll[1] < self.min_scroll:
                        self.scroll[1] += 20
                    elif e.button == 5 and self.scroll[1] > 0:
                        self.scroll[1] -= 20

        delete_index = None
        for layer_index in range(self.canvas.total_layers):
            rect = self.layer_background_rects[layer_index]
            layer = self.canvas.image[layer_index]
            menu_buttons = self.layer_menu_buttons[layer_index]
            layer_frames = self.layer_frames[layer_index]

            if rect.collidepoint([mouse_pos[0] - self.scroll[0], mouse_pos[1] - self.scroll[1]]):
                self.display.blit(self.background_hover, (rect.x, rect.y - self.scroll[1]))
                pygame.draw.rect(self.display, (255, 255, 0), (rect.x, rect.y - self.scroll[1], rect.width,
                                                               rect.height), 1)
                self.text_hover_font.display_fonts(self.display, layer.name, [rect.x + self.text_pos[0],
                                                                              rect.y + self.text_pos[1] - self.scroll[
                                                                                  1]])
                if pygame.mouse.get_pressed()[0]:
                    self.canvas.selected_layer = layer_index
            else:
                self.display.blit(self.background, (rect.x, rect.y - self.scroll[1]))
                self.text_font.display_fonts(self.display, layer.name, [rect.x + self.text_pos[0],
                                                                        rect.y + self.text_pos[1] - self.scroll[1]])

            if layer_index == self.canvas.selected_layer:
                pygame.draw.rect(self.display, (255, 255, 255), (rect.x, rect.y - self.scroll[1], rect.width,
                                                               rect.height), 1)

            menu_buttons.display_buttons(self.display, mouse_pos, events, self.scroll)

            if menu_buttons.selected_button == "cancel":
                delete_index = layer_index + 1
            elif menu_buttons.selected_button == "up arrow":
                self.canvas.move_layer_up(layer_index, self.error_manager)
            elif menu_buttons.selected_button == "down arrow":
                self.canvas.move_layer_down(layer_index, self.error_manager)

            menu_buttons.selected_button = None

            layer_frames.display_buttons(self.display, mouse_pos, layer.selected_frame, events, self.scroll, self.canvas.set_frames)

        if delete_index:
            delete_index -= 1
            self.canvas.remove_layer(delete_index, self.error_manager)
            delete_index = None

    def display_components(self, mouse_pos, events, scroll=(0, 0)):
        mouse_pos = [mouse_pos[0] - self.display_pos[0], mouse_pos[1] - self.display_pos[1]]
        self.button_surface.fill((0, 0, 0))
        pygame.draw.line(self.display, (255, 255, 255), (self.button_surface_pos[0] - self.border,
                                                         self.button_surface_pos[1]),
                         (self.button_surface_pos[0] - self.border, self.button_surface_size[1]),
                         self.border)

        self.display_layers(mouse_pos, events, scroll)

        self.menu_manager.display_buttons(mouse_pos, events)

        if self.menu_manager.selected_button == "add new layer":
            name = ask_layer_name()
            if name:
                self.canvas.add_layer(name)
                self.add_layer_rect()
            self.menu_manager.selected_button = None
        elif self.menu_manager.selected_button == "add new frame":
            self.canvas.image[self.canvas.selected_layer].add_frame()
            self.menu_manager.selected_button = None
            self.add_layer_rect()
        elif self.menu_manager.selected_button == "play animation":
            pass
        elif self.menu_manager.selected_button == "pause animation":
            pass

        self.display.blit(self.button_surface, self.button_surface_pos)
