import pygame

from data.scripts.tools.font import Font
from data.scripts.ui.button import IconButton


def demo_functions():
    print("Demo function called")

def quit_function():
    pygame.quit()
    quit()


class MenuManager:
    def __init__(self, display, display_pos, tooltip_screen, button_names=None, tooltip_offset=(0, 0)):
        self.display = display
        self.display_pos = display_pos
        self.tooltip_screen = tooltip_screen
        self.tooltip_offset = tooltip_offset
        self.text = Font('small_font.png', (255, 255, 255), 2)
        self.button_names =  button_names
        self.scroll = [0, 0]
        self.offset = 2
        self.button_len = len(self.button_names)
        self.min_scroll = (self.button_len * 50 + (self.button_len - 2) * self.offset) - self.display.get_height()

        self.selected_button = 'pencil'

        self.create_buttons()


    def reset_displays(self, display, display_pos, tooltip_screen):
        self.display = display
        self.display_pos = display_pos
        self.tooltip_screen = tooltip_screen

        self.scroll = [0, 0]

        self.min_scroll = (self.button_len * 50 + (self.button_len - 2) * self.offset) - self.display.get_height()

        self.create_buttons()

    def create_buttons(self):
        self.menu_buttons = {}
        y = 0
        size = [50, 50]
        for name in self.button_names:
            self.menu_buttons[name] = IconButton(0, y, size[0], size[1], name, self.tooltip_offset)
            y += size[1] + self.offset

    def display_buttons(self, mouse_pos, events):
        _hover = self.display_pos[0] < mouse_pos[0] < self.display_pos[0] + self.display.get_width() and self.display_pos[
            1] < mouse_pos[1] < self.display_pos[1] + self.display.get_height()
        if _hover:
            for e in events:
                if e.type == pygame.MOUSEBUTTONDOWN:
                    if e.button == 4 and self.scroll[1] < self.min_scroll:
                        self.scroll[1] += 20
                    elif e.button == 5 and self.scroll[1] > 0:
                        self.scroll[1] -= 20

        pos = [mouse_pos[0] - self.display_pos[0], mouse_pos[1] - self.display_pos[1]]
        for index, button in enumerate(self.menu_buttons.items()):
            name, button = button
            if button.display(self.display, _hover, self.tooltip_screen, pos, events, self.scroll):
                self.selected_button = name
                if name == 'exit':
                    quit()
            if name == self.selected_button:
                pygame.draw.rect(self.display, (255, 255, 255), (button.x - self.scroll[0], button.y -
                                                                 self.scroll[1], button.width, button.height), 3)
