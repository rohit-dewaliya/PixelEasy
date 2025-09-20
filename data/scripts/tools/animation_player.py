import pygame


def load_animations(path):
    return {}, [0, 0]


class AnimationPlayer(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = [0, 0]
        self.flip = False
        self.animation_data = {}
        self.animation_frame = 0
        self.animation_state = 'explosion'
        self.previous_animation_state = 'explosion'
        self.animation = None
        self.start_animation = False

    # Loading the Animations-------------------------------------------------#
    def animations(self, path):
        self.animation_data, self.size = load_animations(path)
        self.current_animation()

    # Setting the Current Animation----------------------------------------#
    def current_animation(self):
        self.animation = self.animation_data[self.animation_state]

    # Playing the Animation-----------------------------------------#
    def play_animation(self, display, scroll):
        if self.start_animation:
            if self.animation_state == self.previous_animation_state:
                if self.animation_frame == len(self.animation):
                    self.animation_frame = 0
                    self.start_animation = False

            else:
                self.animation_frame = 0
                self.previous_animation_state = self.animation_state
                self.current_animation()

            display.blit(pygame.transform.flip(self.animation[self.animation_frame], self.flip, False),
                         (self.x - scroll[0] - self.size[0] // 2, self.y - scroll[1] - self.size[1]))
            self.animation_frame += 1