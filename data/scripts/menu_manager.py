import pygame

from data.scripts.image_functions import load_image, scale_image_size
from data.scripts.font import Font

def demo_functions():
    print('yes')

def quit_function():
    pygame.quit()
    quit()


class MenuManager:
    def __init__(self, display, display_pos, canvas_screen):
        self.display = display
        self.display_pos = display_pos
        self.canvas_screen = canvas_screen
        self.text = Font('small_font.png', (255, 255, 255), 2)
        self.menu_buttons = {
            'pencil' : [load_image('icons/pencil.png'), self.text.get_width('pencil'), demo_functions],
            'eraser' : [load_image('icons/eraser.png'), self.text.get_width('eraser'), demo_functions],
            'rotate': [load_image('icons/rotate.png'), self.text.get_width('rotate'), demo_functions],
            'canvas move': [load_image('icons/canvas_move.png'), self.text.get_width('canvas move'), demo_functions],
            'move' : [load_image('icons/move.png'), self.text.get_width('move'), demo_functions],
            'fill paint': [load_image('icons/paint_bucket.png'), self.text.get_width('fill paint'), demo_functions],
            'selection': [load_image('icons/selection.png'), self.text.get_width('selection'), demo_functions],
            'flip horizontally': [load_image('icons/flip_horizontally.png'), self.text.get_width('flip horizontally'), demo_functions],
            'flip vertically': [load_image('icons/flip_vertically.png'), self.text.get_width('flip vertically'), demo_functions],
            'rectangle': [load_image('icons/rectangle.png'), self.text.get_width('rectangle'), demo_functions],
            'line': [load_image('icons/line.png'), self.text.get_width('line'), demo_functions],
            'export' : [load_image('icons/export.png'), self.text.get_width('export'), demo_functions],
            'import' : [load_image('icons/import.png'), self.text.get_width('import'), demo_functions],
            'save' : [load_image('icons/save.png'), self.text.get_width('save'), demo_functions],
            'setting' : [load_image('icons/setting.png'), self.text.get_width('setting'), demo_functions],
            'exit' : [load_image('icons/exit.png'), self.text.get_width('exit'), quit_function],
        }
        self.offset = 2
        self.button_bg = scale_image_size(load_image('background.png', 200), 50, 50)
        self.button_hover_bg = scale_image_size(load_image('background.png', 250), 50, 50)
        self.bg_size = self.button_bg.get_height()
        self.tooltip_bg = load_image('background.png', 100)
        self.tooltip_bg_extra_width = 20
        self.tooltip_bg_extra_height = 10
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
                    self.scroll_y -= 20
                elif event[0].button == 5 and self.scroll_y < 0:
                    self.scroll_y += 20
        i = 1
        pos = [mouse_pos[0] - self.display_pos[0], mouse_pos[1] - self.display_pos[1]]
        pos_y = 0
        for name, properties in self.menu_buttons.items():
            if 0 < pos[0] < 50 and pos_y + self.scroll_y < pos[1] < pos_y + self.scroll_y + self.bg_size:
                self.display.blit(self.button_hover_bg, (0, pos_y + self.scroll_y))
                img = scale_image_size(self.tooltip_bg, properties[1] + self.tooltip_bg_extra_width,
                                       self.text.image_height + self.tooltip_bg_extra_height)
                tooltip_pos = (self.canvas_screen.get_width() - img.get_width(), pos_y + 13 + self.scroll_y)
                self.canvas_screen.blit(img, tooltip_pos)
                self.text.display_fonts(self.canvas_screen, name, [tooltip_pos[0] + self.tooltip_bg_extra_width // 2,
                                                                 tooltip_pos[1] + self.tooltip_bg_extra_height // 2])
                if pygame.mouse.get_pressed(3)[0]:
                    properties[2]()
            else:
                self.display.blit(self.button_bg, (0, pos_y + self.scroll_y))
            self.display.blit(properties[0], ((self.bg_size - properties[0].get_width()) // 2,
                                              pos_y + (self.bg_size - properties[0].get_height()) // 2
                                              + self.scroll_y))
            pos_y += 50 * i + self.offset
