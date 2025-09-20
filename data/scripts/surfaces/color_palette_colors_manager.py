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
        self.color_palette_colors = []
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
                print(f"Palette exported successfully to {file_path}")
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

    def remove_color(self, color):
        if color in self.color_palette:
            del self.color_palette[color]

    def display_buttons(self, mouse_pos, events, scroll=(0, 0)):
        if self.display_pos[0] < mouse_pos[0] < self.display_pos[0] + self.display.get_width() and self.display_pos[
            1] < mouse_pos[1] < self.display_pos[1] + self.display.get_height():

            for e in events:
                if e.type == pygame.MOUSEBUTTONDOWN:
                    if e.button == 4 and self.scroll[1] < self.min_scroll:
                        self.scroll[1] += 20
                    elif e.button == 5 and self.scroll[1] > 0:
                        self.scroll[1] -= 20

        pos = [mouse_pos[0] - self.display_pos[0], mouse_pos[1] - self.display_pos[1]]
        for color, button in self.color_palette.items():
            button.display(self.display, mouse_pos, events, self.scroll)
