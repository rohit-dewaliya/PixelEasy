import pygame
import os

from data.scripts.tools.image_functions import scale_image_size, load_image

class Cursor:
    def __init__(self, cursor_type = 'dark', cursor_size = (32, 32)):
        pygame.mouse.set_visible(False)

        self.cursor_type = cursor_type
        self.cursors = {}
        self.selected_cursor = "pointer"
        self.cursor_size = cursor_size

        self.load_cursors()

    def load_cursors(self):
        cursors = os.listdir('data/images/cursors/' + self.cursor_type + '/')

        for cursor in cursors:
            cursor = cursor.replace('.png', '')
            self.cursors[cursor] = scale_image_size(load_image("cursors/" + self.cursor_type + "/" + cursor + ".png"),
                                                    *self.cursor_size)

    def display_cursor(self, display, mouse_pos):
        display.blit(self.cursors[self.selected_cursor], mouse_pos)