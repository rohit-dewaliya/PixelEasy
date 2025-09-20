import pygame

from data.scripts.tools.image_functions import load_image, scale_image_size, add_border
from data.scripts.tools.font import Font

background = load_image('background.png', 100)
background_hover = load_image('background.png', 150)

icon_background = load_image('background.png', 180)
icon_background_hover = load_image('background.png', 255)

tooltip_text = Font('small_font.png', (255, 255, 0), 2)

class Button:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.orginal_x  = self.x
        self.original_y = self.y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)

    def set_pos(self, new_x, new_y):
        self.x = self.orginal_x + new_x
        self.y = self.original_y + new_y
        self.rect.topleft = (new_x, new_y)

    def hover(self, mouse_pos, scroll=(0, 0)):
        local_pos = (mouse_pos[0] + scroll[0], mouse_pos[1] + scroll[1])
        return self.rect.collidepoint(local_pos)

    def click(self, mouse_pos, events, scroll=(0, 0)):
        for e in events:
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                return True
        return False


class TextButton(Button):
    def __init__(self, x, y, width, height, text, function = None,
                 text_color=(255, 255, 255), text_hover_color=(255, 255, 0)):
        super().__init__(x, y, width, height)
        self.text = text
        self.text_color = text_color
        self.text_hover_color = text_hover_color
        self.function = function

        self.text_font = Font('small_font.png', self.text_color, 2)
        self.text_hover_font = Font('small_font.png', self.text_hover_color, 2)

        self.text_width = self.text_font.get_width(self.text)

        self.text_bg = scale_image_size(background, self.width, self.height)
        self.text_bg_hover = scale_image_size(background_hover, self.width, self.height)

    def display(self, display, mouse_pos, events, scroll=(0, 0)):
        clicked = False
        if self.hover(mouse_pos, scroll):
            if self.click(mouse_pos, events, scroll):
                self.function()
            display.blit(self.text_bg_hover, (self.x - scroll[0], self.y - scroll[1]))
            self.text_hover_font.display_fonts(
                display,
                self.text,
                [self.x + (self.width - self.text_width) / 2 - scroll[0],
                 self.y + (self.height - self.text_font.image_height) / 2 - scroll[1]],
                5
            )
            pygame.draw.rect(display, (255, 255, 255), self.rect, 2)
        else:
            display.blit(self.text_bg, (self.x - scroll[0], self.y - scroll[1]))
            self.text_font.display_fonts(
                display,
                self.text,
                [self.x + (self.width - self.text_width) / 2 - scroll[0],
                 self.y + (self.height - self.text_font.image_height) / 2 - scroll[1]],
                5
            )
        return clicked

class ColorChooseButton(Button):
    def __init__(self, x, y, width, height, color, margin = 5):
        super().__init__(x, y, width, height)
        self.color = color
        self.margin = margin

        self.text_bg = scale_image_size(background, self.width, self.height)
        self.text_bg_hover = scale_image_size(background_hover, self.width, self.height)

    def display(self, display, mouse_pos, events, scroll=(0, 0)):
        clicked = False
        if self.hover(mouse_pos, scroll):
            if self.click(mouse_pos, events, scroll):
                clicked = True
            display.blit(self.text_bg_hover, (self.x - scroll[0], self.y - scroll[1]))
            pygame.draw.rect(display, (255, 255, 255), [self.x - scroll[0], self.y - scroll[1], self.width,
                                                        self.height], 5)
        else:
            display.blit(self.text_bg, (self.x - scroll[0], self.y - scroll[1]))
        pygame.draw.rect(display, self.color, (self.x + self.margin // 2 - scroll[0], self.y + self.margin // 2 - scroll[1],
                                               self.width - self.margin, self.height - self.margin))
        return clicked

class IconButton(Button):
    def __init__(self, x, y, width, height, image):
        super().__init__(x, y, width, height)
        self.image = load_image("icons/" + image + ".png")
        self.image_name = image.replace("_", " ")
        self.text_width = tooltip_text.get_width(self.image_name, 5)
        self.image_size = self.image.get_size()
        self.bg = scale_image_size(icon_background, width, height)
        self.bg_hover = scale_image_size(icon_background_hover, self.width, self.height)
        self.bg_size = [width, height]
        self.offset = [(self.bg_size[0] - self.image_size[0]) // 2, (self.bg_size[1] - self.image_size[1]) // 2]
        self.tooltip_offset_text = [20, 16]
        self.tooltip_size = [self.text_width + self.tooltip_offset_text[0], tooltip_text.image_height +
                             self.tooltip_offset_text[1]]
        self.tooltip_bg = scale_image_size(background, *self.tooltip_size)
        self.border_image = add_border(self.image)

    def display(self, display, surface_hover, tooltip_display, mouse_pos, events, scroll=(0, 0)):
        if self.hover(mouse_pos, scroll) and surface_hover:
            if self.click(mouse_pos, events, scroll):
                print(self.image_name)
            display.blit(self.bg_hover, [self.x - scroll[0], self.y - scroll[1], self.width, self.height])
            pygame.draw.rect(display, (255, 255, 255), [self.x - scroll[0], self.y - scroll[1], self.width,
                                                        self.height], 2)
            pos = [tooltip_display.get_width() - self.tooltip_size[0] + self.x - scroll[0], self.y - scroll[1] + (
                self.bg_size[1] - self.tooltip_size[1]) // 2]
            tooltip_display.blit(self.tooltip_bg, pos)
            tooltip_text.display_fonts(tooltip_display, self.image_name, [pos[0] + self.tooltip_offset_text[0] // 2,
                                                pos[1] + self.tooltip_offset_text[1] // 2], 5)
            pygame.draw.rect(tooltip_display, (255, 255, 255), [*pos, *self.tooltip_size], 2)
        else:
            display.blit(self.bg, [self.x - scroll[0], self.y - scroll[1], self.width, self.height])
        display.blit(self.image, [self.x + self.offset[0] - scroll[0], self.y + self.offset[1] - scroll[1]])

class ColorIconButton(Button):
    def __init__(self, x, y, width, height, color, offset = (1, 60), margin = 2):
        super().__init__(x, y, width, height)
        self.color = color
        self.margin = margin
        self.offset = offset

        self.text_bg = scale_image_size(background, self.width, self.height)
        self.text_bg_hover = scale_image_size(background_hover, self.width, self.height)

    def display(self, display, surface_hover, mouse_pos, events, scroll=(0, 0)):
        clicked = False
        mouse_pos = [mouse_pos[0] - self.offset[0], mouse_pos[1] - self.offset[1]]
        if self.hover(mouse_pos, scroll) and surface_hover:
            if self.click(mouse_pos, events, scroll):
                clicked = True
            display.blit(self.text_bg_hover, (self.x - scroll[0], self.y - scroll[1]))
            pygame.draw.rect(display, (255, 255, 255), [self.x - scroll[0], self.y - scroll[1], self.width,
                                                        self.height], 2)
        else:
            display.blit(self.text_bg, (self.x - scroll[0], self.y - scroll[1]))
        pygame.draw.rect(display, self.color, (self.x + self.margin // 2 - scroll[0], self.y + self.margin // 2 - scroll[1],
                                               self.width - self.margin, self.height - self.margin))
        return clicked