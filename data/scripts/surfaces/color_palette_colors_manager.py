import pygame
import json
from tkinter import filedialog

from data.scripts.ui.button import ColorIconButton


class ColorPaletteColorsManager:
    def __init__(self, display, display_pos, display_size, color_size=50):
        self.display = display
        self.display_pos = display_pos
        self.display_size = display_size

        self.color_palette = {}
        self.selected_color = None
        self.button_size = [50, 50]
        self.color_size = color_size
        self.scroll = [0, 0]
        self.min_scroll = 60

    def reset_display(self, display, display_pos, display_size):
        self.display = display
        self.display_pos = display_pos
        self.display_size = display_size

    def export_palette(self):
        file_path = filedialog.asksaveasfilename(
            title="Export Palette",
            defaultextension=".txt",
            filetypes=[("TXT File", "*.txt"), ("All Files", "*.*")]
        )
        if file_path:
            try:
                palette_data = ''
                for button in self.color_palette:
                    palette_data += str(button) + '\n'
                with open(file_path, 'w') as file:
                    file.write(palette_data)
            except Exception as e:
                print(f"Error exporting palette: {e}")

    def import_palette(self):
        self.color_palette = {}
        file_path = filedialog.askopenfilename(
            title="Import Palette",
            filetypes=[("JSON Files", "*.txt"), ("All Files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, 'r') as file:
                    palette_data = file.readlines()
                    for color in palette_data:
                        if color:
                            color = eval(color)
                            self.add_color(tuple(color))
            except Exception as e:
                print(f"Error importing palette: {e}")

    def add_color(self, color):
        if color not in self.color_palette:
            num = len(self.color_palette)
            y = (num // 4) * self.color_size
            x = (num % 4) * self.color_size
            self.color_palette[tuple(color)] = ColorIconButton(x, y, self.button_size[0], self.button_size[1], color)
            height = ((num) // 4 + 1) * self.color_size
            self.min_scroll = max(0, (height - self.display_size[1]))

    def rearrage_colors(self):
        colors = list(self.color_palette.keys())
        self.color_palette = {}

        for color in colors:
            self.add_color(color)

    def remove_color(self, color):
        if color in self.color_palette:
            del self.color_palette[color]

        self.rearrage_colors()

    def display_buttons(self, mouse_pos, events, selected_button, scroll = (0, 0)):
        _hover = self.display_pos[0] < mouse_pos[0] < self.display_pos[0] + self.display.get_width() and self.display_pos[
            1] < mouse_pos[1] < self.display_pos[1] + self.display.get_height()
        if _hover:
            for e in events:
                if e.type == pygame.MOUSEBUTTONDOWN:
                    if e.button == 4 and self.scroll[1] < self.min_scroll:
                        self.scroll[1] += 20
                    elif e.button == 5 and self.scroll[1] > 0:
                        self.scroll[1] -= 20

        for color, button in list(self.color_palette.items()):
            clicked, removed = button.display(self.display, _hover, mouse_pos, events, self.scroll)
            if removed:
                self.remove_color(color)
                continue
            if clicked and _hover:
                self.selected_color = color
                selected_button.color = color
                selected_button.recolor_foreground()

            if self.selected_color == color:
                pygame.draw.rect(self.display, (255, 255, 255), (button.x - self.scroll[0], button.y - self.scroll[1],
                                                                 button.width, button.height), 5)