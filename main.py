import pygame

from pygame.locals import *

from data.scripts.tools.file_manager import write_json_file
from data.scripts.tools.image_functions import scale_image_size, load_image, recolor_image
from data.scripts.surfaces.color_palette_manager import ColorPaletteManager
from data.scripts.surfaces.menu_manager import MenuManager
from data.scripts.surfaces.canvas_manager import CanvasManager
from data.scripts.ui.input_fields import Slider, Dropdown, RadioButtonGroup
from data.scripts.ui.button import ColorChooseButton, TextButton
from data.scripts.tools.font import Font
from data.scripts.ui.cursor import Cursor

from tkinter import colorchooser, Toplevel, Scale, HORIZONTAL, Button

pygame.init()


class Game:
    def __init__(self):
        self.MIN_SCREEN_SIZE = [800, 500]
        self.color_palette_manager = None
        self.menu_manager = None
        self.canvas_manager = None

        self.cursor = Cursor(cursor_size=(16, 16))

        self.screen_size([1300, 800])
        pygame.display.set_icon(load_image('design.png'))
        pygame.display.set_caption("PixelEasy")

        self.CLOCK = pygame.time.Clock()
        self.FPS = 30

        self.run = True

        self.configure_text = Font('small_font.png', pygame.Color((255, 255, 255, 100)), 3)
        self.configure_text_hover = Font('small_font.png', pygame.Color((255, 255, 255, 250)), 3)
        self.config_data = {}

        # self.text_input = TextInput(50, 80, 300, 40)

    def screen_size(self, screen_size):
        self.SCREEN_SIZE = (max(screen_size[0], self.MIN_SCREEN_SIZE[0]),
                            max(screen_size[1], self.MIN_SCREEN_SIZE[1]))
        self.SCREEN = pygame.display.set_mode(self.SCREEN_SIZE, pygame.RESIZABLE)

        self.FRAME_SIZE = [self.SCREEN_SIZE[0] - 2, 200]
        self.COLOR_PALETTE_SIZE = [200, self.SCREEN_SIZE[1] - self.FRAME_SIZE[1] - 3]
        self.COLOR_PALETTE_COLORS_SIZE = [200, self.COLOR_PALETTE_SIZE[1] - 124]
        self.MENU_SIZE = [50, self.SCREEN_SIZE[1] - self.FRAME_SIZE[1] - 3]
        self.CANVAS_SIZE = [self.SCREEN_SIZE[0] - self.COLOR_PALETTE_SIZE[0] - self.MENU_SIZE[0] - 4,
                            self.SCREEN_SIZE[1] - self.FRAME_SIZE[1] - 3]
        self.config_margin = 100
        self.CONFIG_DISPLAY_SIZE = [self.SCREEN_SIZE[0] - self.config_margin, self.SCREEN_SIZE[1] - self.config_margin]

        self.COLOR_PALETTE_POS = [1, 1]
        self.COLOR_PALETTE_COLORS_POS = [1, 60]
        self.FRAME_POS = [self.COLOR_PALETTE_POS[0], self.COLOR_PALETTE_SIZE[1] + 2]
        self.CANVAS_POS = [self.COLOR_PALETTE_SIZE[0] + 2, self.COLOR_PALETTE_POS[1]]
        self.MENU_POS = [self.COLOR_PALETTE_SIZE[0] + self.CANVAS_SIZE[0] + 3, self.COLOR_PALETTE_POS[1]]
        self.CONFIG_DISPLAY_POS = [self.config_margin // 2, self.config_margin // 2]

        self.COLOR_PALETTE_DISPLAY = pygame.Surface(self.COLOR_PALETTE_SIZE)
        self.COLOR_PALETTE_COLORS_DISPLAY = pygame.Surface(self.COLOR_PALETTE_COLORS_SIZE)
        self.MENU_DISPLAY = pygame.Surface(self.MENU_SIZE)
        self.FRAME_DISPLAY = pygame.Surface(self.FRAME_SIZE)
        self.CANVAS_DISPLAY = pygame.Surface(self.CANVAS_SIZE)
        self.CONFIG_DISPLAY = pygame.Surface(self.CONFIG_DISPLAY_SIZE)

        if not self.color_palette_manager:
            self.color_palette_manager = ColorPaletteManager(self.COLOR_PALETTE_DISPLAY, self.COLOR_PALETTE_POS,
                                                             self.COLOR_PALETTE_COLORS_DISPLAY,
                                                             self.COLOR_PALETTE_COLORS_POS)
        else:
            self.color_palette_manager.reset_displays(self.COLOR_PALETTE_DISPLAY, self.COLOR_PALETTE_POS,
                                                      self.COLOR_PALETTE_COLORS_DISPLAY, self.COLOR_PALETTE_COLORS_POS)

        if not self.menu_manager:
            self.menu_manager = MenuManager(self.MENU_DISPLAY, self.MENU_POS, self.CANVAS_DISPLAY)
        else:
            self.menu_manager.reset_displays(self.MENU_DISPLAY, self.MENU_POS, self.CANVAS_DISPLAY)

        if not self.canvas_manager:
            self.canvas_manager = CanvasManager(self.CANVAS_DISPLAY, self.CANVAS_POS, self.cursor)
        else:
            self.canvas_manager.reset_display(self.CANVAS_DISPLAY, self.CANVAS_POS)

    def configure_setting(self):
        from data.scripts.tools.file_manager import read_json_file, write_json_file

        self.config_data = read_json_file('data/config.json')
        configure_data = {}

        pos_y = 50
        option_dis = 80
        text_x = 50
        button_size = 40
        slider_size = [150, 10]
        offset_width = self.configure_text.get_width("a" * 60, 5)
        sliders = {}
        radio_groups = {}

        for key, values in self.config_data.items():
            name = key
            _input = None
            slider = None
            rect = None
            distance = 0

            text_width = self.configure_text.get_width(name, 5)

            if values['type'] == 'dropdown':
                radio_group_x = self.CONFIG_DISPLAY_SIZE[0] - 200  # text_x + text_width + (offset_width - text_width)
                radio_group_y = pos_y + (self.configure_text.image_height - button_size) // 2

                radio_group = RadioButtonGroup(values['options'], radio_group_x, radio_group_y,
                                               selected_option=values['options'].index(values['value']))

                rect = pygame.Rect(text_x - 20, radio_group.height, radio_group_x + radio_group.width + 30,
                                   radio_group.height + 10)

                radio_groups[name] = [text_x, pos_y, radio_group, rect, values['value']]
                distance = radio_group.height + 50

            if values['type'] == 'color':
                button_x = self.CONFIG_DISPLAY_SIZE[0] - 200 # text_x + text_width + (offset_width - text_width)
                button_y = pos_y + (self.configure_text.image_height - button_size) // 2

                slider_x = button_x - (slider_size[0] - button_size) // 2
                slider_y = button_y + button_size + 10

                color = values['value'][0 : 3]
                alpha = values['value'][-1]

                _input = ColorChooseButton(button_x, button_y, button_size, button_size, color, alpha)
                slider = Slider(slider_x, slider_y, slider_size[0], slider_size[1], 0, 255, alpha)
                rect = pygame.Rect(text_x - 20, button_y, button_x + 30 + slider_size[0], button_size + slider_size[1]
                                   + 10)
                sliders[name] = [text_x, pos_y, _input, rect, slider, (*color, alpha)]
                distance = button_size + slider_size[1] + 50

            pos_y += distance

        min_scroll = pos_y - self.CONFIG_DISPLAY_SIZE[1]

        return sliders, radio_groups, min_scroll

    def color_chooser(self, color):
        hex_color = "#{:02x}{:02x}{:02x}".format(color[0], color[1], color[2])
        self.color_chosen = colorchooser.askcolor(color=hex_color, title="Choose Color")
        return self.color_chosen[0]

    def retrun_main_screen(self, args):
        self.setting_run = False
        config = {}
        for arg in args:
            for key, value in arg.items():
                self.config_data[key]["value"] = value[-1]

        write_json_file('data/config.json', self.config_data)

    def setting_screen(self):
        self.setting_run = True

        bg = scale_image_size(load_image('background.png', 50), *self.CONFIG_DISPLAY_SIZE)

        sliders, radio_groups, min_scroll = self.configure_setting()

        config_window_border = 6

        text_button = TextButton(self.SCREEN_SIZE[0] - 200, self.SCREEN_SIZE[1] - 45, 100, 40, "Apply",
                                 self.retrun_main_screen, (200, 200, 200), (255, 0, 0), sliders, radio_groups)

        scroll_y = 0

        while self.setting_run:
            self.SCREEN.fill((0, 0, 0))
            pygame.draw.rect(self.SCREEN, (255, 255, 255), (self.CONFIG_DISPLAY_POS[0] - config_window_border // 2,
                                                            self.CONFIG_DISPLAY_POS[1] - config_window_border // 2,
                                                            self.CONFIG_DISPLAY_SIZE[0] + config_window_border,
                                                            self.CONFIG_DISPLAY_SIZE[1] + config_window_border),
                             border_radius=5)
            self.CONFIG_DISPLAY.fill((0, 0, 0))
            mouse_pos = pygame.mouse.get_pos()
            local_mouse_pos = [mouse_pos[0] - self.CONFIG_DISPLAY_POS[0], mouse_pos[1] - self.CONFIG_DISPLAY_POS[1]]

            events = pygame.event.get()

            self.CONFIG_DISPLAY.blit(bg, (0, 0))

            text_button.display(self.SCREEN, mouse_pos, events, [0, 0])

            for name, _input in sliders.items():
                if _input is None:
                    continue

                button = _input[2]
                rect = _input[3]
                slider = _input[4]

                for event in events:
                    value = slider.handle_event(local_mouse_pos, event, [0, scroll_y])
                    if value:
                        button.reset_alpha(value)
                        _input[-1] = (*button.color, value)

                slider.draw(self.CONFIG_DISPLAY, [0, scroll_y])

                if rect.collidepoint([local_mouse_pos[0], local_mouse_pos[1] + scroll_y]):
                    self.configure_text_hover.display_fonts(
                        self.CONFIG_DISPLAY, name, [_input[0], _input[1] - scroll_y], 10
                    )
                else:
                    self.configure_text.display_fonts(
                        self.CONFIG_DISPLAY, name, [_input[0], _input[1] - scroll_y], 10
                    )

                if button.display(self.CONFIG_DISPLAY, local_mouse_pos, events, [0, scroll_y]):
                    color = self.color_chooser(button.color)
                    if color:
                        button.color = color
                        button.recolor_foreground(color)
                        _input[-1] = (*color, button.alpha)
                        print(_input)

            for name, _input in radio_groups.items():
                if _input is None:
                    continue

                radio_group = _input[2]
                rect = _input[3]

                if rect.collidepoint([local_mouse_pos[0], local_mouse_pos[1] + scroll_y]):
                    self.configure_text_hover.display_fonts(
                        self.CONFIG_DISPLAY, name, [_input[0], _input[1] - scroll_y], 10
                    )
                else:
                    self.configure_text.display_fonts(
                        self.CONFIG_DISPLAY, name, [_input[0], _input[1] - scroll_y], 10
                    )

                for event in events:
                    res = radio_group.handle_event(local_mouse_pos, event, [0,scroll_y])
                    if res is not None:
                        type = radio_group.get_selected()
                        self.cursor.reset_cursors(type)
                        _input[-1] = type

                radio_group.draw(self.CONFIG_DISPLAY, [0, scroll_y])

            for event in events:
                if event.type == pygame.QUIT:
                    self.setting_run = False
                    self.run = False
                elif event.type == VIDEORESIZE:
                    self.screen_size(list(event.size))
                    text_button.x = self.SCREEN_SIZE[0] - 200
                    text_button.y = self.SCREEN_SIZE[1] - 45
                    bg = scale_image_size(load_image('background.png', 50), *self.CONFIG_DISPLAY_SIZE)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4 and scroll_y < min_scroll:
                        scroll_y += 20
                    elif event.button == 5 and scroll_y > 0:
                        scroll_y -= 20

            self.SCREEN.blit(self.CONFIG_DISPLAY, self.CONFIG_DISPLAY_POS)
            self.cursor.display_cursor(self.SCREEN, mouse_pos)
            pygame.display.flip()
            self.CLOCK.tick(self.FPS)

    def main(self):
        try:
            while self.run:
                mouse_pos = pygame.mouse.get_pos()

                self.SCREEN.fill((255, 255, 255))
                self.COLOR_PALETTE_DISPLAY.fill((0, 0, 0))
                self.COLOR_PALETTE_COLORS_DISPLAY.fill((0, 0, 0))
                self.MENU_DISPLAY.fill((0, 0, 0))
                self.FRAME_DISPLAY.fill((0, 0, 0))
                self.CANVAS_DISPLAY.fill((0, 0, 0))

                events = pygame.event.get()

                self.color_palette_manager.display_buttons(mouse_pos, events)
                self.menu_manager.display_buttons(mouse_pos, events)
                self.canvas_manager.display_surface(mouse_pos, events)

                for event in events:
                    if event.type == QUIT:
                        self.run = False
                    if event.type == KEYDOWN:
                        if event.key == pygame.K_a:
                            self.setting_screen()
                    elif event.type == VIDEORESIZE:
                        self.screen_size(list(event.size))

                    # choice = self.dropdown.handle_event(event, self.CANVAS_POS, mouse_pos)
                    # if choice:
                    #     color = self.colors[choice]
                    #     print("Selected:", self.colors[choice])

                # self.dropdown.draw(self.CANVAS_DISPLAY, self.CANVAS_POS, mouse_pos)

                self.SCREEN.blit(scale_image_size(self.COLOR_PALETTE_DISPLAY, *self.COLOR_PALETTE_SIZE),
                                 self.COLOR_PALETTE_POS)
                self.SCREEN.blit(scale_image_size(self.COLOR_PALETTE_COLORS_DISPLAY, *self.COLOR_PALETTE_COLORS_SIZE),
                                 self.COLOR_PALETTE_COLORS_POS)
                self.SCREEN.blit(scale_image_size(self.FRAME_DISPLAY, *self.FRAME_SIZE), self.FRAME_POS)
                self.SCREEN.blit(scale_image_size(self.CANVAS_DISPLAY, *self.CANVAS_SIZE), self.CANVAS_POS)
                self.SCREEN.blit(scale_image_size(self.MENU_DISPLAY, *self.MENU_SIZE), self.MENU_POS)
                self.cursor.display_cursor(self.SCREEN, mouse_pos)

                pygame.display.flip()
                self.CLOCK.tick(self.FPS)
        except KeyboardInterrupt:
            print("Game interrupted by user.")
        finally:
            pygame.quit()


if __name__ == "__main__":
    game = Game()
    # game.setting_screen()
    game.main()
