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
        self.surface_size = new_size
        self.surface = new_surface


class Layer:
    instances = []

    def __init__(self, surface_size, name = "main"):
        self.surface_size = surface_size
        self.name = name
        self.frames = [Frame(surface_size)]
        self.selected_frame = 0
        self.hide = False

        Layer.instances.append(self)

    @property
    def total_frames(self):
        return len(self.frames)

    @classmethod
    def reset_frames(cls, frame_number):
        for instance in cls.instances:
            instance.selected_frame = frame_number

    @classmethod
    def add_frames_to_all_layers(cls):
        for instance in cls.instances:
            frame = instance.frames[-1].copy()
            instance.frames.append(frame)

    def add_frame(self, frame=None):
        Layer.add_frames_to_all_layers()
        self.selected_frame = self.total_frames - 1

    def remove_frames(self, frame_index):
        if self.total_frames > 1 and 0 <= frame_index < self.total_frames:
            self.frames.pop(frame_index)
            self.selected_frame = max(0, self.selected_frame - 1)

    def get_active_frame(self):
        return self.frames[self.selected_frame]

    def resize(self, new_size):
        self.surface_size = new_size
        for frame in self.frames:
            frame.resize(new_size)

    def copy(self):
        new_layer = Layer(self.surface_size)
        new_layer.frames = [frame.copy() for frame in self.frames]
        new_layer.selected_frame = self.selected_frame
        return new_layer


class Canvas:
    def __init__(self, surface_size):
        self.surface_size = surface_size
        self.image = [Layer(self.surface_size, "main")]
        self.selected_layer = 0
        self.selected_frame = 0

    @property
    def total_layers(self):
        return len(self.image)

    def set_frames(self, frame_number):
        Layer.reset_frames(frame_number)

    def create_new_image(self):
        self.image = [Layer(self.surface_size)]
        self.selected_layer = 0

    def add_layer(self, name = "", layer=None):
        if layer:
            self.image.append(layer)
        else:
            width, height = self.image[0].surface_size
            new_layer = Layer((width, height), name)
            len_frame = self.image[0].total_frames
            for i in range(len_frame - 1):
                new_layer.frames.append(Frame((width, height)))
            self.image.append(new_layer)
        self.selected_layer = self.total_layers - 1
        self.set_frames(self.image[0].selected_frame)

    def remove_layer(self, layer_index):
        if self.total_layers > 1 and 0 <= layer_index < self.total_layers:
            self.image.pop(layer_index)
            self.selected_layer = self.total_layers - 1

    def render(self):
        final_surface = pygame.Surface(self.surface_size, pygame.SRCALPHA)
        for layer in self.image:
            if not layer.hide:
                final_surface.blit(layer.get_active_frame().surface, (0, 0))
        return final_surface

    def resize(self, new_size):
        self.surface_size = new_size
        for layer in self.image:
            layer.resize(new_size)

    def move_layer_up(self, layer_index):
        if layer_index > 0:
            self.image[layer_index - 1], self.image[layer_index] = self.image[layer_index], self.image[layer_index - 1]

    def move_layer_down(self, layer_index):
        if layer_index < len(self.image) - 1:
            self.image[layer_index + 1], self.image[layer_index] = self.image[layer_index], self.image[layer_index + 1]

    def copy(self):
        new_canvas = Canvas(self.surface_size)
        new_canvas.image = [layer.copy() for layer in self.image]
        new_canvas.selected_layer = self.selected_layer
        return new_canvas
