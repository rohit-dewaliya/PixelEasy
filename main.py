import pygame

from pygame.locals import *
from data.scripts.tools.image_functions import scale_image_size, load_image
from data.scripts.surfaces.color_palette_manager import ColorPaletteManager
from data.scripts.surfaces.menu_manager import MenuManager

pygame.init()


class Game:
    def __init__(self):
        self.MIN_SCREEN_SIZE = [800, 600]
        self.color_palette_manager = None
        self.menu_manager = None

        self.screen_size([1300, 800])
        pygame.display.set_icon(load_image('design.png'))
        pygame.display.set_caption("PixelEasy")

        self.CLOCK = pygame.time.Clock()
        self.FPS = 30

        self.run = True

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

        self.COLOR_PALETTE_POS = [1, 1]
        self.COLOR_PALETTE_COLORS_POS = [1, 60]
        self.FRAME_POS = [self.COLOR_PALETTE_POS[0], self.COLOR_PALETTE_SIZE[1] + 2]
        self.CANVAS_POS = [self.COLOR_PALETTE_SIZE[0] + 2, self.COLOR_PALETTE_POS[1]]
        self.MENU_POS = [self.COLOR_PALETTE_SIZE[0] + self.CANVAS_SIZE[0] + 3, self.COLOR_PALETTE_POS[1]]

        self.COLOR_PALETTE_DISPLAY = pygame.Surface(self.COLOR_PALETTE_SIZE)
        self.COLOR_PALETTE_COLORS_DISPLAY = pygame.Surface(self.COLOR_PALETTE_COLORS_SIZE)
        self.MENU_DISPLAY = pygame.Surface(self.MENU_SIZE)
        self.FRAME_DISPLAY = pygame.Surface(self.FRAME_SIZE)
        self.CANVAS_DISPLAY = pygame.Surface(self.CANVAS_SIZE)

        if not self.color_palette_manager:
            self.color_palette_manager = ColorPaletteManager(self.COLOR_PALETTE_DISPLAY, self.COLOR_PALETTE_POS,
                                                  self.COLOR_PALETTE_COLORS_DISPLAY, self.COLOR_PALETTE_COLORS_POS)
        else:
            self.color_palette_manager.reset_displays(self.COLOR_PALETTE_DISPLAY, self.COLOR_PALETTE_POS,
                                                      self.COLOR_PALETTE_COLORS_DISPLAY, self.COLOR_PALETTE_COLORS_POS)

        if not self.menu_manager:
            self.menu_manager = MenuManager(self.MENU_DISPLAY, self.MENU_POS, self.CANVAS_DISPLAY)
        else:
            self.menu_manager.reset_displays(self.MENU_DISPLAY, self.MENU_POS, self.CANVAS_DISPLAY)

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

                for event in events:
                    if event.type == QUIT:
                        self.run = False
                    elif event.type == VIDEORESIZE:
                        self.screen_size(list(event.size))

                self.SCREEN.blit(scale_image_size(self.COLOR_PALETTE_DISPLAY, *self.COLOR_PALETTE_SIZE), self.COLOR_PALETTE_POS)
                self.SCREEN.blit(scale_image_size(self.COLOR_PALETTE_COLORS_DISPLAY, *self.COLOR_PALETTE_COLORS_SIZE),
                                 self.COLOR_PALETTE_COLORS_POS)
                self.SCREEN.blit(scale_image_size(self.FRAME_DISPLAY, *self.FRAME_SIZE), self.FRAME_POS)
                self.SCREEN.blit(scale_image_size(self.CANVAS_DISPLAY, *self.CANVAS_SIZE), self.CANVAS_POS)
                self.SCREEN.blit(scale_image_size(self.MENU_DISPLAY, *self.MENU_SIZE), self.MENU_POS)

                pygame.display.flip()
                self.CLOCK.tick(self.FPS)
        except KeyboardInterrupt:
            print("Game interrupted by user.")
        finally:
            pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.main()