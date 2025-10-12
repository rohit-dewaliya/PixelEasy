import pygame

from data.scripts.tools.font import Font
from data.scripts.tools.image_functions import load_image, scale_image_size, recolor_image

fonts = Font('small_font.png', (255, 255, 255), 2)
background = load_image('background.png', 100)


class ErrorMessage:
    instances = []
    def __init__(self, text, screen_size, time = 5000):
        self.text = text
        self.text_pos = [30, 5]
        self.text_size = [fonts.get_width(self.text, 5), fonts.image_height]
        self.start_time = pygame.time.get_ticks()
        self.time = time
        self.background_size = [self.text_size[0] + self.text_pos[0] * 2, self.text_size[1] + self.text_pos[1] * 2]
        self.background = recolor_image(scale_image_size(background, *self.background_size), (255, 0, 0), 100)

        self.reset_screen(screen_size)

        ErrorMessage.instances.append(self)

    def reset_screen(self, screen_size):
        self.background_pos = [(screen_size[0] - self.background_size[0]) // 2, 50]

    @classmethod
    def reset_instances(cls, screen_size):
        for instance in cls.instances:
            instance.reset_screen(screen_size)

    def display_error(self, display):
        if pygame.time.get_ticks() - self.start_time > self.time:
            return True
        display.blit(self.background, self.background_pos)
        fonts.display_fonts(display, self.text, [self.background_pos[0] + self.text_pos[0],
                                                 self.background_pos[1] + self.text_pos[1]], 5)
        pygame.draw.rect(display, (255, 255, 255), (*self.background_pos, *self.background_size), 1)
        return False


class ErrorMessageManager:
    def __init__(self, screen, screen_size):
        self.screen = screen
        self.screen_size = screen_size
        self.errors = []

    def reset_screen(self, screen_size):
        self.screen_size = screen_size
        ErrorMessage.reset_instances(screen_size)

    def add_error(self, message):
        error = ErrorMessage(message, self.screen_size)
        self.errors.append(error)

    def display_errors(self):
        if self.errors:
            error = self.errors[0]
            status = error.display_error(self.screen)
            if status:
                self.errors.pop(0)

