import pygame

class Frame:
    def __init__(self, surface_size):
        self.surface_size = surface_size
        self.surface = pygame.Surface(surface_size, pygame.SRCALPHA)

    def check_pos(self, pos):
        if 0 <= pos[0] < self.surface_size[0] and 0 <= pos[1] < self.surface_size[1]:
            return True
        return False

    def add_color(self, pos, color):
        if self.check_pos(pos):
            self.surface.set_at(pos, color)

    def remove_color(self, pos):
        if self.check_pos(pos):
            self.surface.set_at(pos, (0, 0, 0, 0))

    def copy(self):
        new_frame = Frame(self.surface_size)
        new_frame.surface.blit(self.surface, (0, 0))
        return new_frame

    def resize(self, new_size):
        new_surface = pygame.Surface(new_size, pygame.SRCALPHA)
        new_surface.blit(self.surface, (0, 0))
        self.surface = new_surface

class Layer:
    def __init__(self, surface_size):
        self.surface_size = surface_size
        self.frames = [Frame(surface_size)]
        self.selected_frame = 0

    @property
    def total_frames(self):
        return len(self.frames)

    def add_frame(self, frame=None):
        if frame:
            self.frames.append(frame.copy())
        else:
            width, height = self.frames[0].surface_size
            self.frames.append(Frame((width, height)))
        self.selected_frame = self.total_frames - 1

    def remove_frames(self, frame_index):
        if self.total_frames > 1 and 0 <= frame_index < self.total_frames:
            self.frames.pop(frame_index)
            self.selected_frame = max(0, self.selected_frame - 1)

    def get_active_frame(self):
        return self.frames[self.selected_frame]

    def resize(self, new_size):
        for frame in self.frames:
            frame.resize(new_size)

class Canvas:
    def __init__(self, surface_size):
        self.surface_size = surface_size
        self.image = [Layer(self.surface_size)]
        self.selected_layer = 0

    @property
    def total_layers(self):
        return len(self.image)

    def add_layer(self, layer = None):
        if layer:
            self.image.append(layer)
        else:
            width, height = self.image[0].surface_size
            self.image.append(Layer((width, height)))
        self.selected_layer = self.total_layers - 1

    def remove_layer(self, layer_index):
        if self.total_layers > 1 and 0 <= layer_index < self.total_layers:
            self.image.pop(layer_index)
            self.selected_layer = self.total_layers - 1

    def render(self):
        final_surface = pygame.Surface(self.surface_size, pygame.SRCALPHA)
        for layer in self.image:
            final_surface.blit(layer.get_active_frame().surface, (0, 0))
        return final_surface

    def resize(self, new_size):
        for layer in self.image:
            layer.resize(new_size)
