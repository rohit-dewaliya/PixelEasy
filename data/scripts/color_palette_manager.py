import pygame
import json

from tkinter import colorchooser
from data.scripts.image_functions import load_image, scale_image_size
from data.scripts.font import Font
from tkinter import filedialog

class ColorPaletteManager:
    def __init__(self, display, display_pos, color_palette_display, color_palette_display_pos):
        self.display = display
        self.display_pos = display_pos
        self.color_palette_display = color_palette_display
        self.color_palette_display_pos = color_palette_display_pos
        self.background_color = (255, 0, 0)
        self.foreground_color = (255, 255, 255)
        self.color_choosen = None
        self.selected_color = True
        self.text = Font('small_font.png', (255, 255, 255), 2)
        self.bg = scale_image_size(load_image('background.png', 150), 100, 30)
        self.button_bg = scale_image_size(load_image('background.png', 200), 200, 30)
        self.hover_button_bg = scale_image_size(load_image('background.png', 150), 200, 30)
        self.selection_bg = scale_image_size(load_image('white_background.png', 255), 100, 30)
        self.minus_button = scale_image_size(load_image('icons/minus.png', 255), 10, 5)
        self.minus_button_bg = scale_image_size(load_image('white_background.png', 150), 16, 9)
        self.minus_button_hover_bg = scale_image_size(load_image('white_background.png', 200), 16, 9)
        self.buttons = {
            'Add Color to Palette': [self.button_bg, self.hover_button_bg, [1, 30],
                                     self.text.get_width('Add Color to Palette'), self.add_color_palette],
            'Export Palette': [self.button_bg, self.hover_button_bg, [1, self.display.get_height() - 64],
                               self.text.get_width('Export Palette'), self.export_palette],
            'Import Palette': [self.button_bg, self.hover_button_bg, [1, self.display.get_height() - 32],
                               self.text.get_width('Import Palette'), self.import_palette]
        }
        self.color_palette = {}
        self.color_palette_color_size = 50
        self.scroll_y = 0
        self.previous_color = self.background_color

    def color_chooser(self):
        self.color_choosen = colorchooser.askcolor(title="Choose Color")
        return self.color_choosen[0]

    def export_palette(self):
        file_path = filedialog.asksaveasfilename(
            title="Export Palette",
            defaultextension=".json",
            filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")]
        )
        if file_path:
            try:
                palette_data = [{"color": color, "position": pos} for color, pos in self.color_palette.items()]
                with open(file_path, 'w') as file:
                    json.dump(palette_data, file, indent=4)
                print(f"Palette exported successfully to {file_path}")
            except Exception as e:
                print(f"Error exporting palette: {e}")

    def import_palette(self):
        file_path = filedialog.askopenfilename(
            title="Import Palette",
            filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, 'r') as file:
                    palette_data = json.load(file)
                    self.color_palette = {tuple(color): position for item in palette_data for color, position in
                                          [(tuple(item["color"]), item["position"])]}
            except Exception as e:
                print(f"Error importing palette: {e}")

    def add_color_palette(self):
        if self.selected_color:
            color = self.background_color
        else:
            color = self.foreground_color

        if color not in self.color_palette:
            num = len(self.color_palette)
            y = (num // 4) * self.color_palette_color_size
            x = (num % 4) * self.color_palette_color_size
            self.color_palette[tuple(color)] = [x, y]

    def display_bacground_color(self, mouse_pos):
        if 0 < mouse_pos[0] < 100 and 0 < mouse_pos[1] < 30:
            self.display.blit(self.bg, (0, 0))
            if pygame.mouse.get_pressed(5)[0]:
                color = self.color_chooser()
                if color:
                    self.background_color = color
                    self.selected_color = True
        pygame.draw.rect(self.display, self.background_color, (5, 5, 90, 20))

    def display_foregound_color(self, mouse_pos):
        if 100 < mouse_pos[0] < 200 and 0 < mouse_pos[1] < 30:
            self.display.blit(self.bg, (100, 0))
            if pygame.mouse.get_pressed(5)[0]:
                color = self.color_chooser()
                if color:
                    self.foreground_color = color
                    self.selected_color = False
        pygame.draw.rect(self.display, self.foreground_color, (105, 5, 90, 20))

    def display_buttons(self, mouse_pos):
        for button, properties in self.buttons.items():
            if properties[2][0] <= mouse_pos[0] <= properties[2][0] + properties[3] and \
                    properties[2][1] <= mouse_pos[1] <= properties[2][1] + 30:
                bg = self.hover_button_bg
                if pygame.mouse.get_pressed(5)[0]:
                    properties[4]()
            else:
                bg = self.button_bg

            self.display.blit(bg, properties[2])
            self.text.display_fonts(self.display, button, [properties[2][0] + (bg.get_width() - properties[3])
                                                           // 2, properties[2][1] + (bg.get_height() - self.text.image_height) // 2])

    def displya_colors(self, mouse_pos):
        if (self.color_palette_display_pos[0] < mouse_pos[0] < self.color_palette_display_pos[0] +
                self.color_palette_display.get_width() and self.color_palette_display_pos[1] < mouse_pos[1] <
                self.color_palette_display_pos[1] + self.color_palette_display.get_height()):
            global event
            event = pygame.event.get()
            if event and event[0].type == pygame.MOUSEBUTTONDOWN:
                    if event[0].button == 4:
                        self.scroll_y -= 10
                    elif event[0].button == 5 and self.scroll_y < 0:
                        self.scroll_y += 10

        mouse_pos = mouse_pos[0] - self.color_palette_display_pos[0], mouse_pos[1] - self.color_palette_display_pos[1]
        for color, pos in list(self.color_palette.items()):
            if (pos[0] < mouse_pos[0] < pos[0] + 50 and pos[1] + self.scroll_y < mouse_pos[1] < pos[1] + 50 +
                    self.scroll_y):
                if (self.color_palette_display_pos[0] < mouse_pos[0] < self.color_palette_display_pos[0] +
                        self.color_palette_display.get_width() and self.color_palette_display_pos[1] - 60 <
                        mouse_pos[1] < self.color_palette_display_pos[1] - 60 +
                        self.color_palette_display.get_height()):
                    pygame.draw.rect(self.color_palette_display, (255, 255, 255), (pos[0], pos[1] + self.scroll_y, 50, 50))
                    if event and event[0].type == pygame.MOUSEBUTTONDOWN and event[0].button == 1:
                        if self.selected_color:
                            if not self.previous_color:
                                self.previous_color = (255, 0, 0)
                            else:
                                self.previous_color = self.background_color
                            self.background_color = color
                        else:
                            self.foreground_color = color
            pygame.draw.rect(self.color_palette_display, color, (pos[0] + 2, pos[1] + 2 + self.scroll_y, 46, 46))

            if (pos[0] + 29 < mouse_pos[0] < pos[0] + 29 + self.minus_button_bg.get_width() and
                    pos[1] + 3  + self.scroll_y < mouse_pos[1] < pos[1] + 3 + self.minus_button_bg.get_height() +
                    self.scroll_y):
                self.color_palette_display.blit(self.minus_button_hover_bg, (pos[0] + 29, pos[1] + 3 + self.scroll_y))
                if event and event[0].type == pygame.MOUSEBUTTONDOWN and event[0].button == 1:
                    del self.color_palette[color]
                    pygame.mouse.get_rel()
                    if self.selected_color:
                        self.background_color = self.previous_color
            self.color_palette_display.blit(self.minus_button_bg, (pos[0] + 29, pos[1] + 3 + self.scroll_y))
            self.color_palette_display.blit(self.minus_button, (pos[0] + 32, pos[1] + 5 + self.scroll_y))

        reordered_palette = {}
        for i, (color, _) in enumerate(self.color_palette.items()):
            y = (i // 4) * self.color_palette_color_size
            x = (i % 4) * self.color_palette_color_size
            reordered_palette[color] = [x, y]

        self.color_palette = reordered_palette

    def display_color_paletter(self, mouse_pos):
        if self.selected_color:
            self.display.blit(self.selection_bg, (0, 0))
        else:
            self.display.blit(self.selection_bg, (100, 0))

        self.display_bacground_color(mouse_pos)
        self.display_foregound_color(mouse_pos)

        self.display_buttons(mouse_pos)
        self.displya_colors(mouse_pos)