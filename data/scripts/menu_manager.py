import pygame

from data.scripts.image_functions import load_image, scale_image_size


class MenuManager:
    def __init__(self, display, display_pos):
        self.display = display
        self.display_pos = display_pos
        self.menu_buttons = {
            'pencil' : [load_image('icons/pencil.png')],
            'eraser' : [load_image('icons/eraser.png')],
            'move' : [load_image('icons/move.png')],
            'fill paint': [load_image('icons/paint_bucket.png')],
            'selection': [load_image('icons/selection.png')],
            'rectangle': [load_image('icons/rectangle.png')],
            'line': [load_image('icons/line.png')],
            'export' : [load_image('icons/export.png')],
            'import' : [load_image('icons/import.png')],
            'save' : [load_image('icons/save.png')],
            'setting' : [load_image('icons/setting.png')],
            'exit' : [load_image('icons/exit.png')],
        }
        self.offset = 2
        self.button_bg = scale_image_size(load_image('white_background.png', 100), 50, 50)
        self.button_hover_bg = scale_image_size(load_image('white_background.png', 200), 50, 50)
        self.bg_size = self.button_bg.get_height()
        self.scroll_y = 0
        self.len_buttons = len(self.menu_buttons)
        self.min_scroll = -((self.len_buttons * 50 + self.len_buttons * self.offset) - self.display.get_height() -
                            self.offset * 5)

    def display_buttons(self, mouse_pos):
        if self.display_pos[0] < mouse_pos[0] < self.display_pos[0] + self.display.get_width() and self.display_pos[
            1] < mouse_pos[1] < self.display_pos[1] + self.display.get_height():

            event = pygame.event.get()
            if event and event[0].type == pygame.MOUSEBUTTONDOWN:
                if event[0].button == 4 and self.scroll_y > self.min_scroll:
                    self.scroll_y -= 10
                elif event[0].button == 5 and self.scroll_y < 0:
                    self.scroll_y += 10
        i = 1
        pos = [mouse_pos[0] - self.display_pos[0], mouse_pos[1] - self.display_pos[1]]
        pos_y = 0
        for name, properties in self.menu_buttons.items():
            if 0 < pos[0] < 50 and pos_y + self.scroll_y < pos[1] < pos_y + self.scroll_y + self.bg_size:
                self.display.blit(self.button_hover_bg, (0, pos_y + self.scroll_y))
                if pygame.mouse.get_pressed(3)[0]:
                    print(name)
            else:
                self.display.blit(self.button_bg, (0, pos_y + self.scroll_y))
            self.display.blit(properties[0], ((self.bg_size - properties[0].get_width()) // 2,
                                              pos_y + (self.bg_size - properties[0].get_height()) // 2
                                              + self.scroll_y))
            pos_y += 50 * i + self.offset
