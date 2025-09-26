import pygame

from data.scripts.tools.image_functions import load_image, scale_image_size
from data.scripts.tools.font import Font
from data.scripts.canvas import Canvas

mouse_pos_text = Font('small_font.png', (255, 255, 255, 255), 2)


class CanvasManager:
    def __init__(self, display, display_pos, cursor, surface_size = [32, 32], scale = 2, max_scale = 3, min_scale =1):
        self.display = display
        self.display_size = self.display.get_size()
        self.display_pos = display_pos
        self.cursor = cursor

        self.surface_size = surface_size
        self.scale = scale
        self.max_scale = max_scale
        self.min_scale = min_scale
        self.surface = pygame.Surface(self.surface_size)
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
        self.image = self.canvas.image
        self.canvas_operations = {"pencil": False, "eraser": False, "line": False}
        self.border = 2
        self.border_color = (255, 0, 0)
        self.drawing_fixed_pos = None
        self.preview = None
        # self.layer = self.canvas.image[self.canvas.seleced_layer]
        # self.frame = self.layer.frames[self.layer.selected_frame]


    def reset_display(self, display, display_pos):
        self.display = display
        self.display_pos = display_pos

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
                    self.change_pos = True
                    self.fixed_pos = mouse_pos

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 2:
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

    def paint_canvas(self, selected, mouse_pos, events):
        x, y = self.get_mouse_pos_on_canvas(mouse_pos)
        layer = self.image[self.canvas.selected_layer]
        frame = layer.frames[layer.selected_frame]

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if selected == "pencil":
                        self.canvas_operations["pencil"] = True
                    elif selected == "line":
                        if not self.canvas_operations["line"]:
                            self.canvas_operations["line"] = True
                            self.drawing_fixed_pos = x, y
                            self.preview = frame.surface.copy()
                elif event.button == 3:
                    if selected == "pencil":
                        self.canvas_operations["eraser"] = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    layer = self.image[self.canvas.selected_layer]
                    frame = layer.frames[layer.selected_frame]
                    pygame.draw.line(frame.surface, (255, 0, 0),
                                     self.drawing_fixed_pos, [x, y], 1)
                    self.canvas_operations["pencil"] = False
                    self.canvas_operations["line"] = False
                    self.drawing_fixed_pos = None
                    self.preview = None
                elif event.button == 3:
                    self.canvas_operations["eraser"] = False



        if self.canvas_operations["pencil"]:
            frame.add_color((x, y), (255, 0, 0))
        elif self.canvas_operations["eraser"]:
            frame.remove_color((x, y))
        elif self.canvas_operations["line"]:
            self.preview.fill(self.surface_color)
            pygame.draw.line(self.preview, (255, 0, 0), self.drawing_fixed_pos, (x, y), 1)

        if self.preview is not None:
            self.surface.blit(self.preview, (0, 0))



    def display_surface(self, selected, mouse_pos, events = None):
        self.surface.fill(self.surface_color)
        mouse_pos = [mouse_pos[0] - self.display_pos[0], mouse_pos[1] - self.display_pos[1]]
        self.move_canvas(mouse_pos, events)
        self.surface.blit(self.canvas.render(), (0, 0))
        self.paint_canvas("line", mouse_pos, events)
        self.display.blit(pygame.transform.scale(self.surface, [self.surface_size[0] * self.scale, self.surface_size[
            1] * self.scale]), self.surface_pos)
        pygame.draw.rect(self.display, self.border_color, (self.surface_pos[0] - self.border, self.surface_pos[1] -
                                                   self.border, self.surface_size[0] * self.scale + self.border * 2,
                                                   self.surface_size[1] * self.scale + self.border * 2), self.border)
        if self.surface_rect.collidepoint(mouse_pos):
            self.zoom_in_and_out(mouse_pos, events)
            self.show_mouse_pos(mouse_pos)
