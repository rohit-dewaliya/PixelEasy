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

    def reset_cursors(self, type):
        self.cursor_type = type

        self.load_cursors()

    def display_cursor(self, display, mouse_pos):
        if self.selected_cursor in ["pointer", "handwriting"]:
            display.blit(self.cursors[self.selected_cursor], mouse_pos)
        else:
            display.blit(self.cursors[self.selected_cursor], [mouse_pos[0] - self.cursor_size[0] // 2, mouse_pos[1] -
                                                              self.cursor_size[1] // 2])