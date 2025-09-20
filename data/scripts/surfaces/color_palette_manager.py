import pygame

from data.scripts.surfaces.color_palette_colors_manager import ColorPaletteColorsManager
from data.scripts.ui.button import *

from tkinter import colorchooser


class ColorPaletteManager:
    def __init__(self, display, display_pos, colors_palette, color_palette_pos):
        self.display = display
        self.display_size = display.get_size()
        self.display_pos = display_pos
        self.colors_palette_display = colors_palette
        self.color_palette_display_size = self.colors_palette_display.get_size()
        self.color_palette_display_pos = color_palette_pos

        self.color_palette_color_manager = ColorPaletteColorsManager(self.colors_palette_display,
                                                                     self.color_palette_display_pos, self.color_palette_display_size)

        self.color_paletter = {}

        # Text Button------------#
        self.text_buttons_text = [('Import Colors', self.color_palette_color_manager.import_palette), ('Export Colors',
                                                         self.color_palette_color_manager.export_palette)]
        self.create_text_buttons()

        # Color Button-------------#
        self.add_color_button = TextButton(0, 32, self.display_size[0], 25, "Add Color", self.add_color_to_palette)

        # Background and Foreground Button---------#
        self.color_buttons = [(255, 0, 0), (255, 255, 255)]
        self.create_select_color_buttons()

    def reset_displays(self, display, display_pos, colors_palette, color_palette_pos):
        self.display = display
        self.display_size = display.get_size()
        self.display_pos = display_pos
        self.colors_palette_display = colors_palette
        self.color_palette_display_size = self.colors_palette_display.get_size()
        self.color_palette_display_pos = color_palette_pos

        self.create_text_buttons()
        self.create_select_color_buttons()
        self.color_palette_color_manager.reset_display(self.colors_palette_display, self.color_palette_display_pos,
                                                       self.color_palette_display_size)


    def create_select_color_buttons(self):
        self.select_color_buttons = []
        width = self.display_size[0] // 2
        x = 0
        for color in self.color_buttons:
            b = ColorChooseButton(x, 0, width, 32, color)
            self.select_color_buttons.append(b)
            x += width

    def create_text_buttons(self):
        self.text_buttons = []
        button_height = 32
        y = len(self.text_buttons_text) * button_height
        for text, function in self.text_buttons_text:
            self.text_buttons.append(TextButton(0, self.display_size[1] - y, self.display_size[0] - 1, button_height,
                                                text, function))
            y -= button_height

    def add_color_to_palette(self):
        self.color_palette_color_manager.add_color(self.select_color_buttons[0].color)

    def display_text_buttons(self, mouse_pos, events, scroll = (0, 0)):
        for button in self.text_buttons:
            button.display(self.display, mouse_pos, events)

    def display_add_color_button(self, mouse_pos, events, scroll = (0, 0)):
        self.add_color_button.display(self.display, mouse_pos, events, scroll)

    def color_chooser(self):
        self.color_choosen = colorchooser.askcolor(title="Choose Color")
        return self.color_choosen[0]

    def display_select_color_button(self, mouse_pos, events, scroll = (0, 0)):
        for button in self.select_color_buttons:
            if button.display(self.display, mouse_pos, events, scroll):
                button.color = self.color_chooser()

    def display_buttons(self, mouse_pos, events, scroll = (0, 0)):
        self.display_text_buttons(mouse_pos, events, scroll)
        self.display_add_color_button(mouse_pos, events, scroll)
        self.display_select_color_button(mouse_pos, events, scroll)

        self.color_palette_color_manager.display_buttons(mouse_pos, events, scroll)