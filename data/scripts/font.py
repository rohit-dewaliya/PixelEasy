import pygame
from data.scripts.image_functions import load_image, swap_color, scale_image_ratio, clip_surface

class Font():
    def __init__(self, path, color = (255, 0, 0), size_ratio = 1):
        self.size_ratio = size_ratio
        self.image = load_image('fonts/' + path, )
        self.image = swap_color(self.image, (255, 0, 0), color)
        self.image_size = [self.image.get_width(), self.image.get_height()]
        self.image = scale_image_ratio(self.image, size_ratio)
        self.image_height = self.image.get_height()
        self.character_size = {}
        self.image_characters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '.', '-', ',', ':', '+', "'", '!', '?', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '(', ')', '/', '_', '=', '\\', '[', ']', '*', '"', '<', '>', ';', ' ']
        self.image_character_dict = {}
        self.image_character = 0
        self.image_x = 0
        self.image_x_size = 0

        for pixel in range(0, self.image.get_width()):
            pixel_color = self.image.get_at((pixel, 0))

            if pixel_color == (127, 127, 127):
                if self.image_x_size == 0:
                    continue
                self.image_character_dict[self.image_characters[self.image_character]] = [clip_surface(self.image, pixel - self.image_x_size, 0, self.image_x_size, self.image_height), self.image_x_size]
                self.character_size[self.image_characters[self.image_character]] = self.image_x_size
                self.image_x_size = 0
                self.image_character += 1
                continue
            else:
                self.image_x_size += 1

    def get_width(self, string, text_spacing = 3):
        width = 0
        for character in string:
            if character == ' ':
                width += 5 * self.size_ratio
            else:
                width += self.image_character_dict[character][1] + text_spacing
        return width

    def display_fonts(self, surface, string, pos, text_spacing = 3):
        for character in string:
            if character == ' ':
                pos[0] += 5 * self.size_ratio
            else:
                surface.blit(self.image_character_dict[character][0], pos)
                pos[0] += self.image_character_dict[character][1] + text_spacing