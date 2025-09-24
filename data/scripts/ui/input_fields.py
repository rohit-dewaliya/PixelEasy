import pygame

from data.scripts.tools.font import Font

text_color=(255, 0, 0)
slider_text = Font('small_font.png', text_color, 3)

class Slider:
    def __init__(self, x, y, w, h, min_val, max_val, start_val, color=(200,200,200), knob_color=(50,150,250)):
        self.text_height = slider_text.image_height
        self.rect = pygame.Rect(x, y, w, h)
        self.min_val = min_val
        self.max_val = max_val
        self.value = start_val
        self.color = color
        self.knob_color = knob_color
        self.knob_radius = h // 2 + 10
        self.dragging = False

    def draw(self, surface, scroll = (0, 0)):
        slider_text.display_fonts(surface, str(int(self.value)), [self.rect.x - scroll[0] + self.rect.width + 20,
                                    self.rect.y - scroll[1] - (self.text_height - self.rect.height) // 2], 5)
        pygame.draw.rect(surface, self.color, (self.rect.x - scroll[0], self.rect.y - scroll[1], self.rect.width,
                                               self.rect.height))

        knob_x = int(self.rect.x + (self.value - self.min_val) / (self.max_val - self.min_val) * self.rect.w)
        knob_y = self.rect.centery

        pygame.draw.circle(surface, self.knob_color, (knob_x - scroll[0], knob_y - scroll[1]), self.knob_radius)

    def handle_event(self, mouse_pos, event, scroll = (0, 0)):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = mouse_pos
            knob_x = int(self.rect.x + (self.value - self.min_val) / (self.max_val - self.min_val) * self.rect.w)
            knob_y = self.rect.centery
            if (mx - knob_x + scroll[0]) ** 2 + (my - knob_y + scroll[1]) ** 2 <= self.knob_radius**2:
                self.dragging = True

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging = False

        elif event.type == pygame.MOUSEMOTION and self.dragging:
            mx, _ = mouse_pos
            mx = max(self.rect.x, min(mx, self.rect.x + self.rect.w))
            self.value = self.min_val + (mx - self.rect.x) / self.rect.w * (self.max_val - self.min_val)
            return self.value

        return None
#
# if __name__ == "__main__":
#     pygame.init()
#     screen = pygame.display.set_mode((500, 200))
#     pygame.display.set_caption("Slider Example")
#     clock = pygame.time.Clock()
#
#     slider = Slider(50, 80, 300, 8, 0, 100, 50)  # x, y, w, h, min, max, start
#
#     font = pygame.font.SysFont("Arial", 22)
#
#     running = True
#     while running:
#         screen.fill((30, 30, 30))
#
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False
#             value = slider.handle_event(event)
#             if value is not None:
#                 print("Value:", int(value))
#
#         slider.draw(screen)
#
#         # Draw current value as text
#         text = font.render(f"Value: {int(slider.value)}", True, (255,255,255))
#         screen.blit(text, (380, 75))
#
#         pygame.display.flip()
#         clock.tick(60)
#
#     pygame.quit()
