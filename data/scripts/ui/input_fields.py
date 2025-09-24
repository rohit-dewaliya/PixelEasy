import pygame

from data.scripts.tools.font import Font

text_color=(255, 0, 0)
slider_text = Font('small_font.png', text_color, 3)
dropdown_text = Font('small_font.png', (255, 255, 255), 3)
radio_text = Font('small_font.png', (255, 255, 255), 3)

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

class Dropdown:
    def __init__(self, x, y, w, h, options, selected_index=0,
                 bg_color=(50,50,50), text_color=(255,255,255),
                 hover_color=(70,70,70), border_color=(200,200,200)):
        self.rect = pygame.Rect(x - w // 2, y, w, h)
        self.options = options
        self.selected_index = selected_index
        self.bg_color = bg_color
        self.text_color = text_color
        self.hover_color = hover_color
        self.border_color = border_color
        self.text_height = dropdown_text.image_height

        self.open = False
        self.option_rects = [pygame.Rect(x, y + (i+1)*h, w, h) for i in range(len(options))]

    def draw(self, surface, scroll=(0,0)):
        # Main box
        main_rect = self.rect.move(-scroll[0], -scroll[1])
        pygame.draw.rect(surface, self.bg_color, main_rect)
        pygame.draw.rect(surface, self.border_color, main_rect, 2)

        # Current selected text
        dropdown_text.display_fonts(surface, str(self.options[self.selected_index]),
            [main_rect.x + 5, main_rect.y + (main_rect.height - self.text_height)//2])

        # Options
        if self.open:
            for i, option in enumerate(self.options):
                rect = self.option_rects[i].move(-scroll[0], -scroll[1])
                if rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(surface, self.hover_color, rect)
                else:
                    pygame.draw.rect(surface, self.bg_color, rect)
                pygame.draw.rect(surface, self.border_color, rect, 2)

                dropdown_text.display_fonts(surface, option,
                    [rect.x + 5, rect.y + (rect.height - self.text_height)//2])

    def handle_event(self, mouse_pos, event, scroll=(0,0)):
        mx, my = mouse_pos
        adj_main = self.rect.move(-scroll[0], -scroll[1])

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if adj_main.collidepoint(mx, my):  # Toggle menu
                self.open = not self.open
                return None
            if self.open:  # Check options
                for i, rect in enumerate(self.option_rects):
                    adj_rect = rect.move(-scroll[0], -scroll[1])
                    if adj_rect.collidepoint(mx, my):
                        self.selected_index = i
                        self.open = False
                        return i
                # Clicked outside → close menu
                self.open = False
        return None


class RadioButton:
    def __init__(self, x, y, radius, label, selected=False,
                 circle_color=(200, 200, 200), fill_color=(50, 150, 250), text_color=(255, 255, 255)):
        self.x = x
        self.y = y
        self.radius = radius
        self.label = label
        self.circle_color = circle_color
        self.fill_color = fill_color
        self.text_color = text_color
        self.selected = selected
        self.text_height = radio_text.image_height
        self.width = radio_text.get_width(self.label, 5)

    def draw(self, surface, scroll=(0,0)):
        # Outer circle
        pygame.draw.circle(surface, self.circle_color,
                           (self.x - scroll[0], self.y - scroll[1]), self.radius, 2)
        # Inner filled circle if selected
        if self.selected:
            pygame.draw.circle(surface, self.fill_color,
                               (self.x - scroll[0], self.y - scroll[1]), self.radius - 4)

        radio_text.display_fonts(surface, self.label, [self.x + self.radius + 10 - scroll[0],
                      self.y - self.text_height // 2 - scroll[1]], 5)

    def handle_event(self, mouse_pos, event, scroll=(0,0)):
        mx, my = mouse_pos
        adj_x, adj_y = self.x - scroll[0], self.y - scroll[1]
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            dx, dy = mx - adj_x, my - adj_y
            if dx*dx + dy*dy <= self.radius*self.radius:
                return True
        return False


class RadioButtonGroup:
    def __init__(self, options, x, y, spacing = 10, radius = 15,
                 circle_color=(200,200,200), fill_color=(50,150,250), text_color=(255,255,255)):
        self.buttons = []
        self.height = 0
        self.widht = 0
        for i, label in enumerate(options):
            self.buttons.append(RadioButton(x, y + i*spacing + self.height, radius, label,
                                            selected=(i==0), # First one selected by default
                                            circle_color=circle_color,
                                            fill_color=fill_color,
                                            text_color=text_color))
            self.height += self.buttons[i].text_height + spacing
            self.width = max(self.widht, self.buttons[i].width)

    def draw(self, surface, scroll=(0,0)):
        for btn in self.buttons:
            btn.draw(surface, scroll)

    def handle_event(self, mouse_pos, event, scroll=(0,0)):
        for i, btn in enumerate(self.buttons):
            if btn.handle_event(mouse_pos, event, scroll):
                # Deselect all others
                for b in self.buttons:
                    b.selected = False
                btn.selected = True
                return i  # return selected index
        return None

    def get_selected(self):
        for i, btn in enumerate(self.buttons):
            if btn.selected:
                return i, btn.label
        return None, None

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
