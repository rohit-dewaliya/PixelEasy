import pygame
import numpy as np

from data.scripts.tools.font import Font
from data.scripts.canvas import Canvas
from data.scripts.ui.input_fields import Slider

mouse_pos_text = Font('small_font.png', (255, 255, 255, 255), 2)


def flood_fill(surface, position, fill_color):
    fill_color_int = surface.map_rgb(fill_color) & 0xFFFFFFFF
    surf_array = pygame.surfarray.pixels2d(surface)
    x0, y0 = position
    current_color = surf_array[x0, y0]

    if current_color != fill_color_int:
        frontier = [(x0, y0)]
        while frontier:
            x, y = frontier.pop()
            try:
                if surf_array[x, y] != current_color:
                    continue
            except IndexError:
                continue

            surf_array[x, y] = fill_color_int

            frontier.extend([(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)])

    pygame.surfarray.blit_array(surface, surf_array)


def rotate_rect_90_from_center(rect):
    new_rect = pygame.Rect(rect.x, rect.y, rect.height, rect.width)
    new_rect.center = rect.center
    return new_rect


class CanvasManager:
    def __init__(self, display, display_pos, cursor, history_manager, error_manager, surface_size = [32, 32],
                 scale = 2, max_scale = 3, min_scale =1):
        self.display = display
        self.display_size = self.display.get_size()
        self.display_pos = display_pos
        self.error_manager = error_manager
        self.cursor = cursor

        self.history_manager = history_manager

        self.surface_size = surface_size
        self.scale = scale
        self.max_scale = max_scale
        self.min_scale = min_scale
        self.surface = pygame.Surface(self.surface_size, pygame.SRCALPHA)
        self.surface_color = (255, 255, 255)
        self.surface_pos = [(self.display_size[0] - self.surface_size[0] * 2) // 2, (self.display_size[1]  -
                                                                                     self.surface_size[1]) // 2]
        self.surface_rect = pygame.Rect(*self.surface_pos, self.surface_size[0] * self.scale, self.surface_size[1] *
                                        self.scale)
        self.incease_size = 0.3
        self.change_pos = False
        self.fixed_pos = self.surface_pos

        self.mouse_pos_text_pos = [5, self.display_size[1]  - 5]

        self.canvas = Canvas(self.surface_size)
        self.canvas_operations = {"pencil": False, "eraser": False, "line": False, 'rectangle': False,
                                  "circle": False, "selection": False, "flip horizontally": False, "flip vertically":
                                False, "move selection": False, "rotate selection left": False,
                                  "rotate selection right": False, "resize selection": False, "fill paint": False}
        self.border = 2
        self.border_color = (255, 0, 0)
        self.drawing_fixed_pos = None
        self.preview = None
        self.canvas_selection = False
        self.selection_rect = None
        self.selected_surface = None

        self.options_surface_pos = [10, 10]

        self.slider_size = [120, 10]
        self.draw_size = 1
        self.draw_size_selection = True

        self.rotate_angle = 0
        self.rotate_angle_selection = False


        self.options_surface_size = [200, self.slider_size[1] + 30]
        self.options_surface = pygame.Surface(self.options_surface_size)
        self.slider_pos = [20, (self.options_surface_size[1] - self.slider_size[1]) // 2]

        self.draw_size_slider = Slider(*self.slider_pos, self.slider_size[0], self.slider_size[1], 0, 25,
                                       self.draw_size)

    def reset_display(self, display, display_pos):
        self.display = display
        self.display_pos = display_pos
        self.display_size = self.display.get_size()

        self.surface_pos = [(self.display_size[0] - self.surface_size[0] * self.scale) // 2, (self.display_size[1] -
                                                                                     self.surface_size[1] * self.scale) // 2]
        self.surface_rect = pygame.Rect(*self.surface_pos, self.surface_size[0] * self.scale, self.surface_size[1] *
                                        self.scale)

    def resize_canvas(self, new_size):
        self.surface_size = new_size
        self.surface = pygame.Surface(self.surface_size, pygame.SRCALPHA)
        self.reset_surface_rect()
        self.canvas.resize(new_size)

    def repos_surface_rect(self, new_pos):
        self.surface_rect.topleft = new_pos

    def reset_surface_rect(self):
        self.surface_rect.width, self.surface_rect.height = [int(self.surface_size[0] * self.scale),
                                                           int(self.surface_size[1] * self.scale)]

    def get_mouse_pos_on_canvas(self, mouse_pos):
        x = int((mouse_pos[0] - self.surface_pos[0]) // self.scale)
        y = int((mouse_pos[1] - self.surface_pos[1]) // self.scale)
        return x, y

    def show_mouse_pos(self, mouse_pos):
        x, y = self.get_mouse_pos_on_canvas(mouse_pos)
        mouse_pos_text.display_fonts(self.display, f"X: {x}, Y: {y}", [5, self.display_size[1] -
                                                                   mouse_pos_text.image_height - 5])

    def zoom_in_and_out(self, mouse_pos, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    self.scale = min(10, self.scale + self.incease_size)
                elif event.button == 5:
                    self.scale = max(1, self.scale - self.incease_size)
        self.reset_surface_rect()

    def move_canvas(self, mouse_pos, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 2:
                    self.cursor.selected_cursor = "move"
                    self.change_pos = True
                    self.fixed_pos = mouse_pos

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 2:
                    self.cursor.selected_cursor = "pointer"
                    self.change_pos = False

            if event.type == pygame.MOUSEMOTION:
                if self.change_pos:
                    dx = mouse_pos[0] - self.fixed_pos[0]
                    dy = mouse_pos[1] - self.fixed_pos[1]

                    # move canvas
                    self.surface_pos[0] += dx
                    self.surface_pos[1] += dy

                    self.repos_surface_rect(self.surface_pos)
                    self.fixed_pos = mouse_pos

    def set_scaling_cursor(self, pos):
        fixed_pos_x, fixed_pos_y = self.drawing_fixed_pos
        new_pos_x, new_pos_y = pos

        if new_pos_x > fixed_pos_x and new_pos_y > fixed_pos_y:
            self.cursor.selected_cursor = "dgn1"
        elif new_pos_x < fixed_pos_x and new_pos_y > fixed_pos_y:
            self.cursor.selected_cursor = "dgn2"
        elif new_pos_x > fixed_pos_x and new_pos_y < fixed_pos_y:
            self.cursor.selected_cursor = "dgn2"
        elif new_pos_x < fixed_pos_x and new_pos_y < fixed_pos_y:
            self.cursor.selected_cursor = "dgn1"
        elif new_pos_x == fixed_pos_x and new_pos_y > fixed_pos_y:
            self.cursor.selected_cursor = "vert"
        elif new_pos_x == fixed_pos_x and new_pos_y < fixed_pos_y:
            self.cursor.selected_cursor = "vert"
        elif new_pos_y == fixed_pos_y and new_pos_x > fixed_pos_x:
            self.cursor.selected_cursor = "horz"
        elif new_pos_y == fixed_pos_y and new_pos_x < fixed_pos_x:
            self.cursor.selected_cursor = "horz"
        else:
            self.cursor.selected_cursor = "precision"

    def paint_canvas(self, selected, color, mouse_pos, events):
        x, y = self.get_mouse_pos_on_canvas(mouse_pos)
        layer = self.canvas.image[self.canvas.selected_layer]
        frame = layer.frames[layer.selected_frame]

        for event in events:
            if self.draw_size_selection:
                value = self.draw_size_slider.handle_event(mouse_pos, event, [0, 0])
                if value:
                    self.draw_size = int(value)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # if selected in ['flip horizontally', 'flip vertically', 'rotate left 90 degree', 'rotate right 90 degree']:
                    #     print('y', self.canvas_operations)
                    #     if self.canvas_operations['selection']:
                    #         self.canvas_operations['selection'] = False
                    #         print('hello')
                    #         continue
                    if selected == "pencil":
                        self.canvas_operations["pencil"] = True
                        self.cursor.selected_cursor = 'handwriting'
                        self.draw_size_selection = True
                        self.canvas_selection = False
                        self.canvas_operations["fill paint"] = False
                    elif selected == "eraser":
                        self.canvas_operations["eraser"] = True
                        self.canvas_selection = False
                        self.canvas_operations["fill paint"] = False
                    elif selected == "line":
                        if not self.canvas_operations["line"]:
                            self.canvas_operations["line"] = True
                            self.drawing_fixed_pos = x, y
                            self.preview = frame.surface.copy()
                            self.preview.set_colorkey(self.surface_color)
                            self.draw_size_selection = True
                        self.canvas_selection = False
                        self.canvas_operations["fill paint"] = False
                    elif selected == "rectangle":
                        if not self.canvas_operations["rectangle"]:
                            self.canvas_operations["rectangle"] = True
                            self.drawing_fixed_pos = x, y
                            self.preview = frame.surface.copy()
                            self.preview.set_colorkey(self.surface_color)
                            self.draw_size_selection = True
                        self.canvas_selection = False
                        self.canvas_operations["fill paint"] = False
                    elif selected == "circle":
                        pass
                        self.rotate_angle_selection = False
                        self.draw_size_selection = True
                        self.canvas_selection = False
                        self.canvas_operations["fill paint"] = False
                    elif selected == "selection":
                        if not self.canvas_operations["selection"]:
                            self.canvas_operations["selection"] = True
                            print('y', self.canvas_operations)
                            self.drawing_fixed_pos = x, y
                            self.preview = frame.surface.copy()
                            self.preview.set_colorkey(self.surface_color)
                        self.canvas_operations["fill paint"] = False
                    elif selected == "flip horizontally":
                        self.canvas_operations["flip horizontally"] = True
                        self.canvas_operations["fill paint"] = False
                    elif selected == "flip vertically":
                        self.canvas_operations["flip vertically"] = True
                        self.canvas_operations["fill paint"] = False
                    elif selected == "fill paint":
                        self.canvas_selection = False
                        if self.canvas_operations["fill paint"] and self.surface_rect.collidepoint(mouse_pos):
                            flood_fill(frame.surface, (x, y), color)
                        self.canvas_operations["fill paint"] = True
                        # get_pixel(frame.surface, (x, y), color)
                    elif selected == "rotate left 90 degree":
                        self.canvas_operations["rotate selection left"] = True
                        self.canvas_operations["fill paint"] = False
                    elif selected == "rotate right 90 degree":
                        self.canvas_operations["rotate selection right"] = True
                        self.canvas_operations["fill paint"] = False

                elif event.button == 3:
                    self.canvas_operations["eraser"] = True
            elif event.type == pygame.MOUSEBUTTONUP:
                self.cursor.selected_cursor = 'pointer'
                if event.button == 1:
                    layer = self.canvas.image[self.canvas.selected_layer]
                    frame = layer.frames[layer.selected_frame]
                    if self.canvas_operations["line"]:
                        pygame.draw.line(frame.surface, color,
                                         self.drawing_fixed_pos, [x, y], self.draw_size)
                    if self.canvas_operations["rectangle"]:
                        rect = pygame.Rect(self.drawing_fixed_pos,
                                           (x - self.drawing_fixed_pos[0], y - self.drawing_fixed_pos[1]))
                        rect.normalize()
                        pygame.draw.rect(frame.surface, color, rect, self.draw_size)
                    if self.canvas_operations["selection"]:
                        self.canvas_selection = True
                        self.selection_rect = pygame.Rect(self.drawing_fixed_pos,
                                           (x - self.drawing_fixed_pos[0], y - self.drawing_fixed_pos[1]))


                    self.canvas_operations["pencil"] = False
                    self.canvas_operations["line"] = False
                    self.canvas_operations["rectangle"] = False
                    self.canvas_operations["eraser"] = False
                    self.canvas_operations["selection"] = False
                    self.canvas_operations["flip horizontally"] = False
                    self.canvas_operations["flip vertically"] = False
                    self.canvas_operations["rotate selection right"] = False
                    self.canvas_operations["rotate selection left"] = False
                    self.drawing_fixed_pos = None
                    self.preview = None
                    self.history_manager.save_state(self.canvas.copy())
                elif event.button == 3:
                    self.canvas_operations["eraser"] = False
                    self.history_manager.save_state(self.canvas.copy())

        if self.canvas_operations["pencil"]:
            frame.add_color((x, y), color)
        elif self.canvas_operations["eraser"]:
            frame.remove_color((x, y))
        elif self.canvas_operations["line"]:
            self.preview.fill(self.surface_color)
            pygame.draw.line(self.preview, color, self.drawing_fixed_pos, (x, y), self.draw_size)
        elif self.canvas_operations["rectangle"]:
            self.preview.fill(self.surface_color)
            rect = pygame.Rect(self.drawing_fixed_pos, (x - self.drawing_fixed_pos[0], y - self.drawing_fixed_pos[1]))
            rect.normalize()
            pygame.draw.rect(self.preview, color, rect, self.draw_size)
        elif self.canvas_operations["selection"]:
            self.preview.fill(self.surface_color)
            rect = pygame.Rect(self.drawing_fixed_pos, (x - self.drawing_fixed_pos[0], y - self.drawing_fixed_pos[1]))
            rect.normalize()
            pygame.draw.rect(self.preview, (255, 0, 255, 100), rect, 1)
        if self.canvas_selection:
            if self.canvas_operations["flip horizontally"]:
                selected_surface = frame.surface.subsurface(self.selection_rect).copy()
                flipped_surface = pygame.transform.flip(selected_surface, True, False)
                frame.surface.fill((0, 0, 0, 0), self.selection_rect)
                frame.surface.blit(flipped_surface, (self.selection_rect.x, self.selection_rect.y))
                self.canvas_operations["flip horizontally"] = False
            elif self.canvas_operations["flip vertically"]:
                selected_surface = frame.surface.subsurface(self.selection_rect).copy()
                flipped_surface = pygame.transform.flip(selected_surface, False, True)
                frame.surface.fill((0, 0, 0, 0), self.selection_rect)
                frame.surface.blit(flipped_surface, (self.selection_rect.x, self.selection_rect.y))
                self.canvas_operations["flip vertically"] = False
            elif self.canvas_operations["rotate selection left"]:
                selected_surface = frame.surface.subsurface(self.selection_rect).copy()
                flipped_surface = pygame.transform.rotate(selected_surface, 90)
                frame.surface.fill((0, 0, 0, 0), self.selection_rect)
                self.selection_rect = rotate_rect_90_from_center(self.selection_rect)
                frame.surface.blit(flipped_surface, (self.selection_rect.x,  self.selection_rect.y))
                self.canvas_operations["rotate selection left"] = False
            elif self.canvas_operations["rotate selection right"]:
                selected_surface = frame.surface.subsurface(self.selection_rect).copy()
                flipped_surface = pygame.transform.rotate(selected_surface, -90)
                frame.surface.fill((0, 0, 0, 0), self.selection_rect)
                self.selection_rect = rotate_rect_90_from_center(self.selection_rect)
                frame.surface.blit(flipped_surface, (self.selection_rect.x, self.selection_rect.y))
                self.canvas_operations["rotate selection right"] = False
            selected = 'pencil'

        if self.preview is not None:
            self.set_scaling_cursor([x, y])
            self.surface.blit(self.preview, (0, 0))

        if self.draw_size_selection:
            self.draw_size_slider.draw(self.options_surface, (0, 0))


    def display_surface(self, selected, color, mouse_pos, events = None):
        self.surface.fill(self.surface_color)
        self.options_surface.fill((0, 0, 0))

        mouse_pos = [mouse_pos[0] - self.display_pos[0], mouse_pos[1] - self.display_pos[1]]
        self.move_canvas(mouse_pos, events)

        self.surface.blit(self.canvas.render(), (0, 0))

        self.paint_canvas(selected, color, mouse_pos, events)

        if self.canvas_selection and self.selection_rect:
            self.selection_rect.normalize()
            pygame.draw.rect(self.surface, (255, 0, 255, 100), self.selection_rect, 1)

        self.display.blit(pygame.transform.scale(self.options_surface, [self.options_surface_size[0],
                                               self.options_surface_size[1]]), self.options_surface_pos)
        pygame.draw.rect(self.display, (255, 255, 255), (*self.options_surface_pos, *self.options_surface_size), 1)

        self.display.blit(pygame.transform.scale(self.surface, [self.surface_size[0] * self.scale, self.surface_size[
            1] * self.scale]), self.surface_pos)
        pygame.draw.rect(self.display, self.border_color, (self.surface_pos[0] - self.border, self.surface_pos[1] -
                                                   self.border, self.surface_size[0] * self.scale + self.border * 2,
                                                   self.surface_size[1] * self.scale + self.border * 2), self.border)

        if self.surface_rect.collidepoint(mouse_pos):
            self.zoom_in_and_out(mouse_pos, events)
            self.show_mouse_pos(mouse_pos)
